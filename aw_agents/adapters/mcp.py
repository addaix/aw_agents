"""
MCP (Model Context Protocol) adapter for AW agents.

This adapter wraps any AgentBase subclass to expose it as an MCP server for use with
Claude Desktop. The server is built by ``py2mcp`` (the fleet's MCP surface adapter, the
same builder every other fleet MCP server goes through): each agent tool becomes one
function whose signature is derived from the tool's JSON schema, and
:func:`py2mcp.mk_mcp_server` turns those functions into a FastMCP server.
"""

import inspect
from typing import Annotated, Any, Callable, Dict, Literal, Optional
from pathlib import Path

from aw_agents.adapters.json_types import annotation_from_json_type
from aw_agents.base import AgentBase


def _format_success_response(result: Dict[str, Any]) -> str:
    """Format a successful tool execution response."""
    parts = []

    if result.get("message"):
        parts.append(f"✓ {result['message']}")
    else:
        parts.append("✓ Operation completed successfully")

    # Add data if present
    if result.get("data"):
        parts.append("")
        parts.append(str(result["data"]))

    # Add warnings if present
    if result.get("warnings"):
        parts.append("")
        parts.append("Warnings:")
        for warning in result["warnings"]:
            parts.append(f"  • {warning}")

    return "\n".join(parts)


def _format_error_response(result: Dict[str, Any]) -> str:
    """Format an error response."""
    message = result.get("message", "Unknown error")
    return f"❌ Error: {message}"


def _annotation_from_schema(spec: Dict[str, Any]) -> Any:
    """The Python annotation that FastMCP turns back into the JSON-schema ``spec``.

    Keeps what a bare type would lose: array item types (recursively) and enums. A
    union ``type`` (a list, as in ``["string", "integer"]``) is the ``Union`` of its
    known non-null types, made ``Optional`` when ``"null"`` is listed; a single type
    stays plain, and an unknown type is ``Any`` (see
    :func:`aw_agents.adapters.json_types.annotation_from_json_type`).

    >>> _annotation_from_schema({"type": "array", "items": {"type": "string"}})
    list[str]
    >>> _annotation_from_schema({"type": "string", "enum": ["a", "b"]})
    typing.Literal['a', 'b']
    >>> _annotation_from_schema({"type": ["string", "null"]})
    typing.Optional[str]
    >>> _annotation_from_schema({"type": ["string", "integer"]})
    typing.Union[str, int]
    >>> _annotation_from_schema({})
    typing.Any
    """
    if spec.get("enum"):
        return Literal[tuple(spec["enum"])]
    items = spec.get("items")
    return annotation_from_json_type(
        spec.get("type"),
        items=_annotation_from_schema(items) if isinstance(items, dict) else None,
    )


def _signature_from_schema(schema: Dict[str, Any]) -> inspect.Signature:
    """A keyword-only signature for a tool's JSON-schema ``parameters``.

    Required properties have no default; optional ones default to the schema's
    ``default`` (else ``None``). A property's ``description`` is carried as
    ``Annotated[..., Field(description=...)]`` so the served schema keeps it.

    >>> str(_signature_from_schema({"properties": {"url": {"type": "string"}, "n": {"type": "integer"}}, "required": ["url"]}))
    '(*, url: str, n: Optional[int] = None)'
    """
    from pydantic import Field

    required = set(schema.get("required", []))
    params = []
    for name, spec in schema.get("properties", {}).items():
        annotation = _annotation_from_schema(spec)
        if name in required:
            default = inspect.Parameter.empty
        else:
            default = spec.get("default")
            annotation = Optional[annotation]
        if spec.get("description"):
            annotation = Annotated[annotation, Field(description=spec["description"])]
        params.append(
            inspect.Parameter(
                name,
                inspect.Parameter.KEYWORD_ONLY,
                default=default,
                annotation=annotation,
            )
        )
    return inspect.Signature(params)


class MCPAdapter:
    """
    Adapter to expose an AgentBase as an MCP server.

    Usage:
        agent = YourAgent()
        adapter = MCPAdapter(agent, server_name="your-agent")
        adapter.run_sync()

    ``adapter.server`` is the ``py2mcp`` (FastMCP) server; ``adapter.tools`` the functions
    it serves, one per agent tool.
    """

    def __init__(self, agent: AgentBase, server_name: str, **server_options):
        """
        Initialize MCP adapter.

        Args:
            agent: Agent instance to wrap
            server_name: Name for the MCP server
            **server_options: Forwarded to :func:`py2mcp.mk_mcp_server` (``instructions``,
                ``middleware``, ``annotations``...)
        """
        from py2mcp import mk_mcp_server

        self.agent = agent
        self.tools = [self._mk_tool(tool) for tool in agent.get_tools()]
        self.server = mk_mcp_server(self.tools, name=server_name, **server_options)

    def _mk_tool(self, tool: Dict[str, Any]) -> Callable[..., str]:
        """The function that serves one agent tool: arguments in, formatted text out."""
        name = tool["name"]

        def call(**arguments):
            try:
                arguments = {k: v for k, v in arguments.items() if v is not None}
                result = self.agent.execute_tool(name, arguments)
                if result["success"]:
                    return self._format_success_response(result)
                return self._format_error_response(result)
            except Exception as e:
                return f"❌ Error executing {name}:\n{str(e)}"

        call.__name__ = call.__qualname__ = name
        call.__doc__ = tool["description"]
        signature = _signature_from_schema(tool["parameters"])
        call.__signature__ = signature
        call.__annotations__ = {
            p.name: p.annotation for p in signature.parameters.values()
        } | {"return": str}
        return call

    _format_success_response = staticmethod(_format_success_response)
    _format_error_response = staticmethod(_format_error_response)

    def run_sync(self):
        """Run the MCP server over stdio (blocking)."""
        self.server.run()

    async def run(self):
        """Run the MCP server over stdio (awaitable)."""
        await self.server.run_stdio_async()


def create_mcp_server_script(agent_class, server_name: str, output_path: Path):
    """
    Generate an MCP server script for an agent.

    Args:
        agent_class: Agent class to wrap
        server_name: Name for the MCP server
        output_path: Path to write the script
    """
    # Determine module path for import
    agent_module = agent_class.__module__
    if agent_module.startswith("aw_agents."):
        # Extract the submodule (e.g., 'agents.download' from 'aw_agents.agents.download.agent')
        parts = agent_module.split(".")
        if len(parts) > 3:
            import_module = ".".join(parts[:3])  # aw_agents.agents.download
        elif len(parts) > 2:
            import_module = ".".join(parts[:2])  # aw_agents.agents
        else:
            import_module = agent_module
    else:
        import_module = agent_module

    script_content = f'''"""
MCP Server for {agent_class.__name__}

Auto-generated MCP server script.

To use with Claude Desktop, add to your config:
{{
  "mcpServers": {{
    "{server_name}": {{
      "command": "python",
      "args": ["{output_path.absolute()}"]
    }}
  }}
}}
"""

from aw_agents.adapters.mcp import MCPAdapter
from {import_module} import {agent_class.__name__}


def main():
    agent = {agent_class.__name__}()
    adapter = MCPAdapter(agent, "{server_name}")
    adapter.run_sync()


if __name__ == "__main__":
    main()
'''

    output_path.write_text(script_content)
    output_path.chmod(0o755)

    return output_path
