"""The OpenAPI adapter builds request models from union JSON-schema types (addaix/aw_agents#13)."""

import pytest

pytest.importorskip("fastapi")

from aw_agents.adapters.openapi import OpenAPIAdapter


def _model(properties, required):
    adapter = OpenAPIAdapter.__new__(OpenAPIAdapter)  # model building needs no server
    return adapter._create_pydantic_model(
        "Request", {"properties": properties, "required": required}
    )


@pytest.mark.parametrize("value", [5, "five"])
def test_a_multi_type_union_accepts_every_listed_type(value):
    Request = _model({"a": {"type": ["string", "integer"]}}, ["a"])
    assert Request(a=value).a == value


def test_a_nullable_union_accepts_none():
    Request = _model({"note": {"type": ["string", "null"]}}, ["note"])
    assert Request(note=None).note is None


def test_a_single_or_missing_type_keeps_its_old_mapping():
    Request = _model({"n": {"type": "integer"}, "s": {}}, ["n", "s"])
    assert Request(n=3, s="x").n == 3
    with pytest.raises(Exception):
        Request(n="three", s="x")
