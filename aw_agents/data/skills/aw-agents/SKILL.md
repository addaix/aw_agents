---
name: aw-agents
description: >-
  Use the aw_agents package: download content from a URL with landing-page detection and
  context-aware file names (DownloadAgent, DownloadEngine, download_content), serve an agent
  to Claude as an MCP server or to ChatGPT as an OpenAPI/FastAPI service, and write a new
  agent once for both (AgentBase, create_json_schema, MCPAdapter, OpenAPIAdapter). Use when
  someone wants to "download this dataset/paper/PDF", "find the real download link behind a
  landing page", "serve an agent to Claude Desktop", "make a ChatGPT custom GPT action from
  an agent", or "write an agent for both Claude and ChatGPT" with aw_agents.
metadata:
  audience: users
---

# aw_agents: one agent, served to Claude and ChatGPT

An agent is a class with two methods: `get_tools()` (tool definitions with a JSON schema) and `execute_tool(name, arguments)`. An adapter serves it: `MCPAdapter` for Claude (MCP, stdio), `OpenAPIAdapter` for ChatGPT (FastAPI with an OpenAPI schema). The one agent shipped is `DownloadAgent`.

## Install

The base package is the download engine (it needs `requests`). The extras add the adapters' dependencies: `aw_agents[mcp]` to serve to Claude, `aw_agents[api]` to serve to ChatGPT (fastapi, uvicorn, pydantic), `aw_agents[all]` for both. An adapter raises `ImportError` naming the extra when its dependency is missing.

## Download content from Python

```python
from aw_agents.agents.download.download_core import DownloadEngine, download_content

path = download_content(
    "https://arxiv.org/abs/1706.03762", context="attention is all you need"
)

engine = DownloadEngine(default_download_dir="data/raw")  # default: ~/Downloads
result = engine.download(
    url, context="UCI adult dataset", filename=None, force_redownload=False
)
result["path"], result["url"], result["warnings"], result["metadata"]
engine.download_multiple(urls)  # one result per URL
```

What it does for you: detects an HTML landing page and follows the real download link; rewrites GitHub and Hugging Face page URLs to their raw files; infers the extension from the content type when the URL has none; builds the file name from `context`. Read `result["warnings"]`: a landing page it could not resolve is reported there, not raised.

## Serve the download agent

```bash
python -m aw_agents.agents.download.agent            # MCP server for Claude Desktop (default)
python -m aw_agents.agents.download.agent --api --port 8080
python -m aw_agents.agents.download.agent --api --server-url https://<tunnel>   # ChatGPT needs a public URL
```

Its tools: `download_content` (`url`, optional `context`, `download_dir`, `filename`), `download_multiple` (`urls`, optional `contexts` one per URL, `download_dir`), `list_downloads` (optional `download_dir`, glob `pattern`).

## Write a new agent

```python
from aw_agents import (
    AgentBase,
    ToolExecutionResult,
    create_json_schema,
    MCPAdapter,
    OpenAPIAdapter,
)


class WordCount(AgentBase):
    """Count words in a text."""

    def get_tools(self):
        return [
            {
                "name": "count_words",
                "description": "Count the words in a text.",
                "parameters": create_json_schema(
                    {"text": {"type": "string", "description": "The text"}},
                    required=["text"],
                ),
            }
        ]

    def execute_tool(self, name, arguments):
        if name != "count_words":
            return ToolExecutionResult.error_result(f"unknown tool {name!r}").to_dict()
        return ToolExecutionResult.success_result(
            len(arguments["text"].split())
        ).to_dict()


MCPAdapter(WordCount(), "word-count").run_sync()  # Claude
OpenAPIAdapter(WordCount(), title="Word count").run(port=8000)  # ChatGPT
```

`execute_tool` returns a dict with at least `success` and `data` (`message` and `warnings` optional); `ToolExecutionResult` builds it. `create_mcp_server_script(agent_class, name, path)` and `create_api_server_script(agent_class, path)` write a standalone launcher script.

## Gotchas

- The MCP server speaks over stdio: run it from Claude Desktop's config, not in a terminal you then type into.
- ChatGPT custom GPT actions need an HTTPS URL it can reach: pass `--server-url` (a tunnel) so the OpenAPI schema names it.
- `AW_AGENTS_DATA_DIR` (`aw_agents.util`, `djoin`) is the package's own data folder; downloads go to `~/Downloads` unless you pass `download_dir`.
