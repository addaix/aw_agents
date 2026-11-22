# aw_agents.agents

Agents for agentic workflows.

This module contains various AI agents that can be deployed to chatbot platforms.

### Classes

| [`DownloadAgent`](#aw_agents.agents.DownloadAgent)([default_download_dir])   | Smart download agent with context-aware naming and intelligent link handling.   |
|------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|

### *class* aw_agents.agents.DownloadAgent(default_download_dir=None, \*\*kwargs)

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

### Modules

| [`download`](aw_agents.agents.download.html.md#module-aw_agents.agents.download)   | Download Agent - Smart content downloader with context-aware naming.   |
|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
