# aw_agents

aw_agents - AI Agents for Agentic Workflows

A collection of AI agents that can be easily deployed to multiple chatbot
platforms (Claude, ChatGPT, etc.) through adapters.

Agents:

> - DownloadAgent: Smart content downloader with context-aware naming

Adapters:

> - MCPAdapter: For Claude Desktop (MCP protocol)
> - OpenAPIAdapter: For ChatGPT Custom GPTs (OpenAPI/FastAPI)

### Example

```pycon
>>> from aw_agents.agents.download import DownloadAgent
>>> from aw_agents.adapters import MCPAdapter
>>>
>>> agent = DownloadAgent()
>>> adapter = MCPAdapter(agent, "download-agent")
>>> # adapter.run() serves the agent via MCP for Claude (blocks; not run here)
```

### Functions

| [`create_json_schema`](#aw_agents.create_json_schema)(properties[, required])        | Helper to create JSON schema for tool parameters.   |
|----------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| [`create_mcp_server_script`](#aw_agents.create_mcp_server_script)(agent_class, ...)        | Generate an MCP server script for an agent.         |
| [`create_api_server_script`](#aw_agents.create_api_server_script)(agent_class, ...[, ...]) | Generate an API server script for an agent.         |

### Classes

| [`AgentBase`](#aw_agents.AgentBase)()                               | Base class for all AW agents.                                                 |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| [`ToolExecutionResult`](#aw_agents.ToolExecutionResult)(success[, data, ...]) | Standard result format for tool execution.                                    |
| [`MCPAdapter`](#aw_agents.MCPAdapter)(agent, server_name)            | Adapter to expose an AgentBase as an MCP server.                              |
| [`OpenAPIAdapter`](#aw_agents.OpenAPIAdapter)(agent, \*[, title, ...])   | Adapter to expose an AgentBase as a FastAPI/OpenAPI service.                  |
| [`DownloadAgent`](#aw_agents.DownloadAgent)([default_download_dir])     | Smart download agent with context-aware naming and intelligent link handling. |

### *class* aw_agents.AgentBase

Bases: [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Base class for all AW agents.

Agents should inherit from this and implement the core methods.
Adapters (MCP, OpenAPI) will wrap these agents for deployment.

#### *abstractmethod* execute_tool(name, arguments)

Execute a tool with given arguments.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Tool name
  * **arguments** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – Tool arguments
* **Returns:**
  - success: bool
  - data: Any
  - message: Optional[str]
  - warnings: Optional[list[str]]
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

#### get_metadata()

Get agent metadata.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Metadata including name, version, description

#### *abstractmethod* get_tools()

Return tool definitions for this agent.

Each tool should have:

- name: str
- description: str
- parameters: dict (JSON schema)

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]
* **Returns:**
  List of tool definitions

### *class* aw_agents.DownloadAgent(default_download_dir=None, \*\*kwargs)

Bases: [`AgentBase`](aw_agents.base.html.md#aw_agents.base.AgentBase)

Smart download agent with context-aware naming and intelligent link handling.

Features:

- Detects landing pages and finds actual download links
- Special handling for GitHub, HuggingFace, Kaggle
- Context-aware file naming
- Multiple content type support

```pycon
>>> agent = DownloadAgent()
>>> tools = agent.get_tools()
>>> len(tools) >= 3
True
```

#### execute_tool(name, arguments)

Execute a tool with given arguments.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

#### get_metadata()

Get agent metadata.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

#### get_tools()

Return tool definitions for this agent.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]

### *class* aw_agents.MCPAdapter(agent, server_name)

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

### *class* aw_agents.OpenAPIAdapter(agent, , title='AI Agent API', description='AI Agent exposed via OpenAPI', version='1.0.0', server_url=None)

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

### *class* aw_agents.ToolExecutionResult(success, data=None, message=None, warnings=None, metadata=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Standard result format for tool execution.

#### *classmethod* error_result(message, data=None, \*\*kwargs)

Create an error result.

* **Return type:**
  [`ToolExecutionResult`](aw_agents.base.html.md#aw_agents.base.ToolExecutionResult)

#### *classmethod* success_result(data, message=None, \*\*kwargs)

Create a success result.

* **Return type:**
  [`ToolExecutionResult`](aw_agents.base.html.md#aw_agents.base.ToolExecutionResult)

#### to_dict()

Convert to dictionary format.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

### aw_agents.create_api_server_script(agent_class, output_path, , default_port=8000)

Generate an API server script for an agent.

* **Parameters:**
  * **agent_class** – Agent class to wrap
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to write the script
  * **default_port** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Default port for the server

### aw_agents.create_json_schema(properties, required=None, \*\*kwargs)

Helper to create JSON schema for tool parameters.

```pycon
>>> schema = create_json_schema(
...     properties={
...         'url': {'type': 'string', 'description': 'URL to process'},
...         'context': {'type': 'string', 'description': 'Context info'}
...     },
...     required=['url']
... )
>>> schema['type']
'object'
>>> 'url' in schema['required']
True
```

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

### aw_agents.create_mcp_server_script(agent_class, server_name, output_path)

Generate an MCP server script for an agent.

* **Parameters:**
  * **agent_class** – Agent class to wrap
  * **server_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name for the MCP server
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to write the script

### Modules

| [`adapters`](aw_agents.adapters.html.md#module-aw_agents.adapters)   | Adapters for exposing agents to different platforms.   |
|---------------------------------------------------------------------------------------|--------------------------------------------------------|
| [`agents`](aw_agents.agents.html.md#module-aw_agents.agents)       | Agents for agentic workflows.                          |
| [`base`](aw_agents.base.html.md#module-aw_agents.base)           | Base classes and protocols for AW agents.              |
| [`util`](aw_agents.util.html.md#module-aw_agents.util)           | Utils for aw_agents                                    |
