from typing import Any

import pytest
from devtools import debug
from jsonschema import ValidationError
from ngff_rfc8.validate import validate_collection

DATA_MESSAGE_PAIRS = [
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
    (
        {
            "ome": {
                "version": "0.x",
                "name": "root",
                "type": "collection",
                "nodes": [
                    {
                        "type": "multiscale",
                        "name": "foo",
                        "path": {"type": "json", "path": "./foo.json"},
                    }
                ],
            }
        },
        "'attributes' is a required property",
    ),
]


@pytest.mark.parametrize("data, expected_message", DATA_MESSAGE_PAIRS)
def test_error_handling(data: dict[str, Any], expected_message: str):
    debug(data)
    debug(expected_message)
    with pytest.raises(ValidationError) as exc_info:
        validate_collection(data)
    debug(exc_info.value)
    assert exc_info.value.message == expected_message
