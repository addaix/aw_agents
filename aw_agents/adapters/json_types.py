"""JSON-schema ``type`` -> Python annotation, shared by the adapters.

A JSON-schema ``type`` is either one type name (``"string"``) or a union of them
(``["string", "integer", "null"]``). Every adapter that turns an agent's tool schema
into Python types (the MCP adapter's signatures, the OpenAPI adapter's request models)
goes through :func:`annotation_from_json_type`, so a union means the same thing on
every surface: a value any listed type accepts is accepted.
"""

from typing import Any, Dict, Optional, Union

#: JSON-schema ``type`` name -> the Python type pydantic turns back into that type.
JSON_TYPES: Dict[str, Any] = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def annotation_from_json_type(json_type: Any, *, items: Any = None, unknown: Any = Any):
    """The annotation for a JSON-schema ``type`` (one name or a list of names).

    A union is the ``Union`` of every known non-null type, in schema order, made
    ``Optional`` when ``"null"`` is listed; a single type stays plain. ``items``, when
    given, is the item annotation used for ``"array"``. When no listed type is known,
    the result is ``unknown`` (``Any`` by default).

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
    """
    names = json_type if isinstance(json_type, list) else [json_type]
    nullable = "null" in names
    known = list(dict.fromkeys(t for t in names if isinstance(t, str) and t in JSON_TYPES))
    if not known:
        return unknown
    annotations = tuple(
        list[items] if t == "array" and items is not None else JSON_TYPES[t]
        for t in known
    )
    annotation = annotations[0] if len(annotations) == 1 else Union[annotations]
    return Optional[annotation] if nullable else annotation
