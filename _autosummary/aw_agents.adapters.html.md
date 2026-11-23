# aw_agents.adapters

Adapters for exposing agents to different platforms.

### Functions

| [`create_mcp_server_script`](#aw_agents.adapters.create_mcp_server_script)(agent_class, ...)        | Generate an MCP server script for an agent.   |
|----------------------------------------------------------------------------------------------------|-----------------------------------------------|
| [`create_api_server_script`](#aw_agents.adapters.create_api_server_script)(agent_class, ...[, ...]) | Generate an API server script for an agent.   |

### Classes

| [`MCPAdapter`](#aw_agents.adapters.MCPAdapter)(agent, server_name, \*\*server_options)   | Adapter to expose an AgentBase as an MCP server.             |
|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [`OpenAPIAdapter`](#aw_agents.adapters.OpenAPIAdapter)(agent, \*[, title, ...])              | Adapter to expose an AgentBase as a FastAPI/OpenAPI service. |

### *class* aw_agents.adapters.MCPAdapter(agent, server_name, \*\*server_options)

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

### *class* aw_agents.adapters.OpenAPIAdapter(agent, , title='AI Agent API', description='AI Agent exposed via OpenAPI', version='1.0.0', server_url=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Adapter to expose an AgentBase as a FastAPI/OpenAPI service.

Usage:

```default
agent = YourAgent()
adapter = OpenAPIAdapter(agent, title="Your Agent API")
adapter.run(port=8000)
```

#### run(host='0.0.0.0', port=8000, \*\*kwargs)

Run the FastAPI server.

* **Parameters:**
  * **host** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Host to bind to
  * **port** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Port to bind to
  * **\*\*kwargs** – Additional uvicorn arguments

### aw_agents.adapters.create_api_server_script(agent_class, output_path, , default_port=8000)

Generate an API server script for an agent.

* **Parameters:**
  * **agent_class** – Agent class to wrap
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to write the script
  * **default_port** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Default port for the server

### aw_agents.adapters.create_mcp_server_script(agent_class, server_name, output_path)

Generate an MCP server script for an agent.

* **Parameters:**
  * **agent_class** – Agent class to wrap
  * **server_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name for the MCP server
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to write the script

### Modules

| [`mcp`](aw_agents.adapters.mcp.html.md#module-aw_agents.adapters.mcp)         | MCP (Model Context Protocol) adapter for AW agents.   |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------|
| [`openapi`](aw_agents.adapters.openapi.html.md#module-aw_agents.adapters.openapi) | OpenAPI/FastAPI adapter for AW agents.                |
