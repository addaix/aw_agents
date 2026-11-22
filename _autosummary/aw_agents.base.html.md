# aw_agents.base

Base classes and protocols for AW agents.

This module provides the foundation for building AI agents that can be
deployed to multiple chatbot platforms (Claude, ChatGPT, etc.).

### Functions

| [`create_json_schema`](#aw_agents.base.create_json_schema)(properties[, required])   | Helper to create JSON schema for tool parameters.   |
|-----------------------------------------------------------------------------------------------|-----------------------------------------------------|

### Classes

| [`AgentBase`](#aw_agents.base.AgentBase)()                               | Base class for all AW agents.              |
|--------------------------------------------------------------------------------------------|--------------------------------------------|
| [`ToolExecutionResult`](#aw_agents.base.ToolExecutionResult)(success[, data, ...]) | Standard result format for tool execution. |

### *class* aw_agents.base.AgentBase

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

### *class* aw_agents.base.ToolExecutionResult(success, data=None, message=None, warnings=None, metadata=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Standard result format for tool execution.

#### *classmethod* error_result(message, data=None, \*\*kwargs)

Create an error result.

* **Return type:**
  [`ToolExecutionResult`](#aw_agents.base.ToolExecutionResult)

#### *classmethod* success_result(data, message=None, \*\*kwargs)

Create a success result.

* **Return type:**
  [`ToolExecutionResult`](#aw_agents.base.ToolExecutionResult)

#### to_dict()

Convert to dictionary format.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

### aw_agents.base.create_json_schema(properties, required=None, \*\*kwargs)

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
