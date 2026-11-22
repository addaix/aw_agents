# aw_agents.agents.download.download_core

Download Agent: Smart content downloader with context-aware naming and intelligent link handling.

This agent can download content from URLs with special handling for:

- Indirect download links (landing pages with actual download links)
- Scientific papers (PDFs from various sources)
- Data from HuggingFace, Kaggle, GitHub
- Context-aware file naming based on conversation context

### Functions

| [`download_content`](#aw_agents.agents.download.download_core.download_content)(url, \*[, context, download_dir])   | Convenience function to download a single URL and return the path.   |
|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|

### Classes

| [`DownloadEngine`](#aw_agents.agents.download.download_core.DownloadEngine)([default_download_dir, ...])   | Core download engine with smart link handling and context-aware naming.   |
|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|

### *class* aw_agents.agents.download.download_core.DownloadEngine(default_download_dir=None, , user_agent='DownloadAgent/1.0', timeout=30, max_redirects=5, extension_router=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Core download engine with smart link handling and context-aware naming.

```pycon
>>> engine = DownloadEngine()
>>> # engine.download("https://example.com/paper.pdf", context="Important ML Paper")
```

#### download(url, , context=None, download_dir=None, filename=None, force_redownload=False)

Download content from a URL with smart handling.

* **Parameters:**
  * **url** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – URL to download from
  * **context** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Context about the content (used for filename generation)
  * **download_dir** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path), [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – Directory to download to (default: self.default_download_dir)
  * **filename** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Override automatic filename generation
  * **force_redownload** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Force re-download even if cached
* **Returns:**
  - ‘path’: Path to downloaded file
  - ’url’: Final URL downloaded from
  - ’warnings’: List of warning messages
  - ’metadata’: Additional metadata
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]

### Example

```pycon
>>> engine = DownloadEngine()
>>> # result = engine.download("https://example.com/paper.pdf", context="ML Paper")
>>> # print(result['path'])
```

#### download_multiple(urls, , contexts=None, download_dir=None)

Download multiple URLs.

* **Parameters:**
  * **urls** ([`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – List of URLs to download
  * **contexts** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Optional list of contexts (same length as urls)
  * **download_dir** ([`Union`](https://docs.python.org/3/library/typing.html#typing.Union)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path), [`None`](https://docs.python.org/3/builtins/constants.html#None)]) – Directory to download to
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]
* **Returns:**
  List of result dictionaries (one per URL)

### aw_agents.agents.download.download_core.download_content(url, , context=None, download_dir=None)

Convenience function to download a single URL and return the path.

### Example

```pycon
>>> # path = download_content("https://example.com/file.pdf", context="Important doc")
```

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
