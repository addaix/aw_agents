# aw_agents.adapters.openapi

OpenAPI/FastAPI adapter for AW agents.

This adapter wraps any AgentBase subclass to expose it as a REST API
with OpenAPI spec for use with ChatGPT Custom GPTs.

### Functions

| [`create_api_server_script`](#aw_agents.adapters.openapi.create_api_server_script)(agent_class, ...[, ...])   | Generate an API server script for an agent.   |
|------------------------------------------------------------------------------------------------------|-----------------------------------------------|

### Classes

| [`OpenAPIAdapter`](#aw_agents.adapters.openapi.OpenAPIAdapter)(agent, \*[, title, ...])   | Adapter to expose an AgentBase as a FastAPI/OpenAPI service.   |
|--------------------------------------------------------------------------------------------|----------------------------------------------------------------|

### *class* aw_agents.adapters.openapi.OpenAPIAdapter(agent, , title='AI Agent API', description='AI Agent exposed via OpenAPI', version='1.0.0', server_url=None)

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

### aw_agents.adapters.openapi.create_api_server_script(agent_class, output_path, , default_port=8000)

Generate an API server script for an agent.

* **Parameters:**
  * **agent_class** – Agent class to wrap
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to write the script
  * **default_port** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Default port for the server
