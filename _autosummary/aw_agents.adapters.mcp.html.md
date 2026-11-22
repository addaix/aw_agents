# aw_agents.adapters.mcp

MCP (Model Context Protocol) adapter for AW agents.

This adapter wraps any AgentBase subclass to expose it as an MCP server
for use with Claude Desktop.

### Functions

| [`create_mcp_server_script`](#aw_agents.adapters.mcp.create_mcp_server_script)(agent_class, ...)   | Generate an MCP server script for an agent.   |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------|

### Classes

| [`MCPAdapter`](#aw_agents.adapters.mcp.MCPAdapter)(agent, server_name)   | Adapter to expose an AgentBase as an MCP server.   |
|-----------------------------------------------------------------------------------|----------------------------------------------------|

### *class* aw_agents.adapters.mcp.MCPAdapter(agent, server_name)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Adapter to expose an AgentBase as an MCP server.

Usage:

```default
agent = YourAgent()
adapter = MCPAdapter(agent, server_name="your-agent")
adapter.run()
```

#### *async* run()

Run the MCP server.

#### run_sync()

Run the MCP server (synchronous wrapper).

### aw_agents.adapters.mcp.create_mcp_server_script(agent_class, server_name, output_path)

Generate an MCP server script for an agent.

* **Parameters:**
  * **agent_class** – Agent class to wrap
  * **server_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name for the MCP server
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to write the script
