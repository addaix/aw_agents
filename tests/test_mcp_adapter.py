"""The MCP adapter serves an agent's tools through py2mcp (addaix/aw_agents#7)."""

import asyncio

import pytest

pytest.importorskip("py2mcp")

from aw_agents.adapters.mcp import MCPAdapter
from aw_agents.base import AgentBase, create_json_schema


class EchoAgent(AgentBase):
    """An agent with two tools."""

    def get_tools(self):
        return [
            {
                "name": "echo",
                "description": "Echo text back.",
                "parameters": create_json_schema(
                    {
                        "text": {"type": "string"},
                        "times": {"type": "integer"},
                    },
                    required=["text"],
                ),
            },
            {
                "name": "fail",
                "description": "Always fails.",
                "parameters": create_json_schema({}),
            },
        ]

    def execute_tool(self, name, arguments):
        if name == "echo":
            return {
                "success": True,
                "message": "echoed",
                "data": arguments["text"] * arguments.get("times", 1),
            }
        return {"success": False, "message": "nope"}


@pytest.fixture
def adapter():
    return MCPAdapter(EchoAgent(), "echo-agent")


def _call(adapter, name, args):
    return asyncio.run(adapter.server.call_tool(name, args)).content[0].text


def test_tools_are_listed_with_schema_and_description(adapter):
    tools = {t.name: t for t in asyncio.run(adapter.server.list_tools())}
    assert set(tools) == {"echo", "fail"}
    echo = tools["echo"]
    assert echo.description == "Echo text back."
    assert echo.parameters["required"] == ["text"]
    assert set(echo.parameters["properties"]) == {"text", "times"}


def test_success_and_optional_arguments(adapter):
    text = _call(adapter, "echo", {"text": "ab", "times": 2})
    assert "✓ echoed" in text and "abab" in text
    assert "ab" in _call(adapter, "echo", {"text": "ab"})


def test_failure_is_formatted(adapter):
    assert _call(adapter, "fail", {}) == "❌ Error: nope"


def test_server_name(adapter):
    assert adapter.server.name == "echo-agent"


class DescribedAgent(EchoAgent):
    """An agent whose tool schema carries descriptions, array item types and an enum."""

    def get_tools(self):
        return [
            {
                "name": "tag",
                "description": "Tag some URLs.",
                "parameters": create_json_schema(
                    {
                        "urls": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "URLs to tag",
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["fast", "slow"],
                            "description": "How to tag",
                        },
                    },
                    required=["urls"],
                ),
            }
        ]


def test_served_schema_keeps_descriptions_items_and_enums():
    """The served schema is the agent's schema, not a bare-type rebuild (addaix/aw_agents#9)."""
    adapter = MCPAdapter(DescribedAgent(), "described")
    (tool,) = asyncio.run(adapter.server.list_tools())
    props = tool.parameters["properties"]
    assert props["urls"]["description"] == "URLs to tag"
    assert props["urls"]["items"] == {"type": "string"}
    assert props["mode"]["description"] == "How to tag"
    assert {"enum": ["fast", "slow"], "type": "string"} in props["mode"]["anyOf"]
    assert tool.parameters["required"] == ["urls"]
