---
name: aw-agents-dev
description: >-
  Develop and maintain the aw_agents package: its layout (AgentBase, the MCP and OpenAPI
  adapters, the download agent and its engine), adding an agent or an adapter, running the
  tests, and releasing through wads CI. Use when changing aw_agents' code, adding an agent
  under aw_agents/agents/, adding a platform adapter, fixing the download engine's
  landing-page or extension handling, or cutting a release.
metadata:
  audience: developers
---

# Working on aw_agents

## Layout

| Path | What it owns |
|---|---|
| `aw_agents/base.py` | `AgentBase` (the two abstract methods every agent implements), `ToolExecutionResult`, `create_json_schema` |
| `aw_agents/adapters/mcp.py` | `MCPAdapter`: maps `get_tools()` to MCP tools and `execute_tool` to tool calls; `create_mcp_server_script` |
| `aw_agents/adapters/openapi.py` | `OpenAPIAdapter`: one FastAPI POST route per tool, the schema from the tool's parameters; `create_api_server_script` |
| `aw_agents/agents/download/agent.py` | `DownloadAgent` (its three tools) and the `python -m` entry point (`--mcp`, `--api`, `--port`, `--server-url`) |
| `aw_agents/agents/download/download_core.py` | `DownloadEngine`: landing-page detection, GitHub and Hugging Face URL rewriting, extension inference, file naming |
| `aw_agents/util.py` | `AW_AGENTS_DATA_DIR`, `djoin` |
| `aw_agents/data/skills/` | the shipped agent skills (this one and `aw-agents`), linked from `.claude/skills/` |

The design rule: an agent knows nothing about a platform, and an adapter knows nothing about a particular agent. A new platform is a new adapter over `AgentBase`; a new agent is a new `AgentBase` subclass under `aw_agents/agents/<name>/`, exported from `aw_agents/__init__.py`. Adapters import their optional dependency in a try block and raise `ImportError` naming the extra (`mcp`, `api`) when it is missing; keep the base install free of them.

## Tests

```bash
python -m pytest -q tests aw_agents --doctest-modules
```

`tests/test_download.py` and `tests/test_extension_routing.py` cover the engine's naming, extension and landing-page logic. A test that would hit the network belongs behind a fake response, not a live URL. Keep the adapters importable without their extras: the doctest run imports every module.

## Release

wads CI: `.github/workflows/ci.yml` calls the reusable workflow from i2mint/wads, configured by `[tool.wads.ci]` in `pyproject.toml`. A merge to the default branch validates, bumps the version and publishes to PyPI; put `[skip publish]` in the merge commit for a change with no runtime effect (docs, tests, skill text).

## Skills

The two skills live in `aw_agents/data/skills/` (shipped in the wheel: hatchling includes the package's data) with one relative symlink each in `.claude/skills/`. When the public API changes, update `aw-agents/SKILL.md` in the same change.
