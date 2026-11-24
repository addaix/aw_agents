# aw_agents.adapters.json_types

JSON-schema `type` -> Python annotation, shared by the adapters.

A JSON-schema `type` is either one type name (`"string"`) or a union of them
(`["string", "integer", "null"]`). Every adapter that turns an agent’s tool schema
into Python types (the MCP adapter’s signatures, the OpenAPI adapter’s request models)
goes through [`annotation_from_json_type()`](#aw_agents.adapters.json_types.annotation_from_json_type), so a union means the same thing on
every surface: a value any listed type accepts is accepted.

### Module Attributes

| [`JSON_TYPES`](#aw_agents.adapters.json_types.JSON_TYPES)   | JSON-schema `type` name -> the Python type pydantic turns back into that type.   |
|---------------------------------------------------------------|----------------------------------------------------------------------------------|

### Functions

| [`annotation_from_json_type`](#aw_agents.adapters.json_types.annotation_from_json_type)(json_type, \*[, ...])   | The annotation for a JSON-schema `type` (one name or a list of names).   |
|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|

### aw_agents.adapters.json_types.JSON_TYPES *: [Dict](https://docs.python.org/3/library/typing.html#typing.Dict)[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]* *= {'array': <class 'list'>, 'boolean': <class 'bool'>, 'integer': <class 'int'>, 'number': <class 'float'>, 'object': <class 'dict'>, 'string': <class 'str'>}*

JSON-schema `type` name -> the Python type pydantic turns back into that type.

### aw_agents.adapters.json_types.annotation_from_json_type(json_type, , items=None, unknown=typing.Any)

The annotation for a JSON-schema `type` (one name or a list of names).

A union is the `Union` of every known non-null type, in schema order, made
`Optional` when `"null"` is listed; a single type stays plain. `items`, when
given, is the item annotation used for `"array"`. When no listed type is known,
the result is `unknown` (`Any` by default).

```pycon
>>> annotation_from_json_type("integer")
<class 'int'>
>>> annotation_from_json_type(["string", "integer"])
typing.Union[str, int]
>>> annotation_from_json_type(["string", "integer", "null"])
typing.Union[str, int, NoneType]
>>> annotation_from_json_type(["null", "integer"])
typing.Optional[int]
>>> annotation_from_json_type(["array", "null"], items=str)
typing.Optional[list[str]]
>>> annotation_from_json_type(["mystery"])
typing.Any
>>> annotation_from_json_type(None, unknown=str)
<class 'str'>
```
