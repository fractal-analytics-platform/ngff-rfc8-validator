from typing import Any

import pytest
from jsonschema import ValidationError
from ngff_rfc8.validate import validate_collection

CASES = [
    (
        {
            "ome": {
                "version": "0.x",
                "type": "collection",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'name' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'name' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'coordinateSystems' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {"coordinateSystems": {}},
                "nodes": [],
            }
        },
        "{} is not of type 'array'",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {"coordinateSystems": []},
                "nodes": [],
            }
        },
        "[] should be non-empty",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "multiscale",
                "name": "name",
                "id": "dataset",
                "attributes": {"coordinateSystems": [{"id": "my-id", "axes": []}]},
                "nodes": [],
            }
        },
        "[] should be non-empty",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "singlescale",
                "name": "name",
                "id": "dataset",
                "attributes": {},
                "nodes": [],
            }
        },
        "'coordinateTransformations' is a required property",
    ),
    (
        {
            "ome": {
                "version": "0.x",
                "type": "collection",
                "name": "name",
                "id": "??",
                "attributes": {},
                "nodes": [],
            }
        },
        "'??' does not match '^[a-zA-Z0-9-_.]+$'",
    ),
    (
        {
            "ome": {
                "type": "collection",
                "name": "name",
                "id": "id",
                "attributes": {},
                "nodes": [],
            }
        },
        "'version' is a required property",
    ),
    (
        {
            "ome": {
                "version": 1234,
                "type": "collection",
                "name": "name",
                "id": "id",
                "attributes": {},
                "nodes": [],
            }
        },
        "1234 is not of type 'string'",
    ),
]


@pytest.mark.parametrize("data, message", CASES)
def test_error_handling(data: dict[str, Any], message: str):
    from devtools import debug

    debug("Expected message", message)
    with pytest.raises(ValidationError) as exc_info:
        validate_collection(data=data, verbose=True)
    debug(exc_info.value)
    assert exc_info.value.message == message
