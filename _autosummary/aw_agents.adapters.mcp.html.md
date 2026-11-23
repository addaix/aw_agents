# aw_agents.adapters.mcp

MCP (Model Context Protocol) adapter for AW agents.

This adapter wraps any AgentBase subclass to expose it as an MCP server for use with
Claude Desktop. The server is built by `py2mcp` (the fleet’s MCP surface adapter, the
same builder every other fleet MCP server goes through): each agent tool becomes one
function whose signature is derived from the tool’s JSON schema, and
`py2mcp.mk_mcp_server()` turns those functions into a FastMCP server.

### Functions

| [`create_mcp_server_script`](#aw_agents.adapters.mcp.create_mcp_server_script)(agent_class, ...)   | Generate an MCP server script for an agent.   |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------|

### Classes

| [`MCPAdapter`](#aw_agents.adapters.mcp.MCPAdapter)(agent, server_name, \*\*server_options)   | Adapter to expose an AgentBase as an MCP server.   |
|-------------------------------------------------------------------------------------------------------|----------------------------------------------------|

### *class* aw_agents.adapters.mcp.MCPAdapter(agent, server_name, \*\*server_options)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Adapter to expose an AgentBase as an MCP server.

Usage:

```default
agent = YourAgent()
adapter = MCPAdapter(agent, server_name="your-agent")
adapter.run_sync()
```

`adapter.server` is the `py2mcp` (FastMCP) server; `adapter.tools` the functions
it serves, one per agent tool.

#### *async* run()

Run the MCP server over stdio (awaitable).

#### run_sync()

Run the MCP server over stdio (blocking).

### aw_agents.adapters.mcp.create_mcp_server_script(agent_class, server_name, output_path)

Generate an MCP server script for an agent.

* **Parameters:**
  * **agent_class** – Agent class to wrap
  * **server_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name for the MCP server
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to write the script
