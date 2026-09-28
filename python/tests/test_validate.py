import pytest
from jsonschema import ValidationError
from ngff_rfc8.validate import validate_collection

VALID_OME_PROPERTY = {
    "version": "0.x",
    "type": "collection",
    "name": "My Dataset",
    "id": "dataset",
    "attributes": {"fractal:dataset": {"user": "lorenzo", "project": "base-dataset"}},
    "nodes": [
        {
            "type": "collection",
            "name": "My Plate",
            "id": "plate",
            "path": {"type": "json", "path": "./plate/plate.json"},
        }
    ],
}


def test_ome_valid_inline():
    validate_collection({"ome": VALID_OME_PROPERTY})


def test_zarr_valid_inline():
    validate_collection(
        {
            "zarr_format": 3,
            "node_type": "group",
            "attributes": {"ome": VALID_OME_PROPERTY},
        }
    )


def test_missing_ome():
    with pytest.raises(
        ValueError,
        match="must include a 'ome' property",
    ):
        validate_collection({})


def test_missing_version():
    with pytest.raises(
        ValidationError,
        match="'version' is a required property",
    ):
        validate_collection({"ome": {"type": "collection", "name": "foo"}})


def test_missing_name():
    with pytest.raises(ValidationError):
        validate_collection({"ome": {"version": "0.x", "type": "collection"}})


def test_invalid_id():
    with pytest.raises(ValidationError):
        validate_collection(
            {"ome": {"version": "0.x", "type": "collection", "name": "foo", "id": ""}}
        )
    with pytest.raises(ValidationError):
        validate_collection(
            {"ome": {"version": "0.x", "type": "collection", "name": "foo", "id": "??"}}
        )


def test_invalid_attributes_type():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "type": "collection",
                    "name": "foo",
                    "attributes": [],
                }
            }
        )


def test_valid_empty_labels():
    validate_collection(
        {
            "ome": {
                "version": "0.x",
                "name": "root",
                "type": "collection",
                "nodes": [
                    {
                        "type": "multiscale",
                        "name": "foo",
                        "attributes": {
                            "labels": {},
                            "coordinateSystems": [
                                {
                                    "id": "x",
                                    "axes": [
                                        {
                                            "name": "x",
                                            "type": "space",
                                            "unit": "micrometer",
                                        },
                                        {
                                            "name": "y",
                                            "type": "space",
                                            "unit": "micrometer",
                                        },
                                    ],
                                }
                            ],
                        },
                        "path": {"type": "json", "path": "./foo.json"},
                    }
                ],
            }
        }
    )


def test_labels_attribute_missing_label_value():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "multiscale",
                            "name": "foo",
                            "attributes": {
                                "labels": {"labelAttributes": [{}]},
                                "coordinateSystems": [
                                    {
                                        "id": "x",
                                        "axes": [
                                            {
                                                "name": "x",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                            {
                                                "name": "y",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                        ],
                                    }
                                ],
                            },
                            "path": {"type": "json", "path": "./foo.json"},
                        }
                    ],
                }
            }
        )


def test_valid_labels_attribute():
    validate_collection(
        {
            "ome": {
                "version": "0.x",
                "name": "root",
                "type": "collection",
                "nodes": [
                    {
                        "type": "multiscale",
                        "name": "foo",
                        "attributes": {
                            "labels": {
                                "labelAttributes": [
                                    {"labelValue": 1, "color": [0, 255, 100, 255]}
                                ]
                            },
                            "coordinateSystems": [
                                {
                                    "id": "x",
                                    "axes": [
                                        {
                                            "name": "x",
                                            "type": "space",
                                            "unit": "micrometer",
                                        },
                                        {
                                            "name": "y",
                                            "type": "space",
                                            "unit": "micrometer",
                                        },
                                    ],
                                }
                            ],
                        },
                        "path": {"type": "json", "path": "./foo.json"},
                    }
                ],
            }
        }
    )


def test_invalid_labels_color():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "multiscale",
                            "name": "foo",
                            "attributes": {
                                "labels": {
                                    "labelAttributes": [{"labelValue": 1, "color": [0]}]
                                },
                                "coordinateSystems": [
                                    {
                                        "id": "x",
                                        "axes": [
                                            {
                                                "name": "x",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                            {
                                                "name": "y",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                        ],
                                    }
                                ],
                            },
                            "path": {"type": "json", "path": "./foo.json"},
                        }
                    ],
                }
            }
        )


def test_valid_singlescale():
    validate_collection(
        {
            "ome": {
                "version": "0.x",
                "name": "root",
                "type": "collection",
                "nodes": [
                    {
                        "type": "singlescale",
                        "name": "single",
                        "attributes": {
                            "coordinateTransformations": [
                                {
                                    "type": "translation",
                                    "translation": [0, 0, 100],
                                    "input": {
                                        "id": "physical",
                                        "path": {"type": "json", "path": "./foo.json"},
                                    },
                                    "output": {"id": "world"},
                                }
                            ]
                        },
                        "path": {"type": "json", "path": "./foo.json"},
                    }
                ],
            }
        }
    )


def test_missing_attributes_in_multiscale():
    data = {
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
    }
    with pytest.raises(ValidationError):
        validate_collection(data)
    with pytest.raises(ValidationError):
        validate_collection(data, ignore_nodes=False)
    validate_collection(data, ignore_nodes=True)


def test_invalid_coordinateTransformations_missing_type():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "singlescale",
                            "name": "single",
                            "attributes": {
                                "coordinateTransformations": [
                                    {
                                        "translation": [0, 0, 100],
                                        "input": {
                                            "id": "physical",
                                            "path": {
                                                "type": "json",
                                                "path": "./foo.json",
                                            },
                                        },
                                        "output": {"id": "world"},
                                    }
                                ]
                            },
                            "path": {"type": "json", "path": "./foo.json"},
                        }
                    ],
                }
            }
        )


def test_invalid_coordinateTransformations_missing_output_id():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "singlescale",
                            "name": "single",
                            "attributes": {
                                "coordinateTransformations": [
                                    {
                                        "type": "translation",
                                        "translation": [0, 0, 100],
                                        "input": {
                                            "id": "physical",
                                            "path": {
                                                "type": "json",
                                                "path": "./foo.json",
                                            },
                                        },
                                        "output": {},
                                    }
                                ]
                            },
                            "path": {"type": "json", "path": "./foo.json"},
                        }
                    ],
                }
            }
        )


def test_valid_scene():
    validate_collection(
        {
            "ome": {
                "version": "0.x",
                "name": "root",
                "type": "collection",
                "nodes": [
                    {
                        "type": "collection",
                        "name": "name",
                        "attributes": {
                            "scene": {
                                "coordinateTransformations": [
                                    {
                                        "type": "translation",
                                        "translation": [0, 0, 100],
                                        "input": {"id": "physical"},
                                        "output": {"id": "world"},
                                    }
                                ],
                                "coordinateSystems": [
                                    {
                                        "id": "physical",
                                        "name": "The physical coordinate system",
                                        "axes": [
                                            {
                                                "name": "x",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                            {
                                                "name": "y",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                        ],
                                    }
                                ],
                            }
                        },
                        "path": {"type": "json", "path": "./foo.json"},
                    }
                ],
            }
        }
    )


def test_invalid_scene_missing_coordinateTransformations():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "collection",
                            "name": "name",
                            "attributes": {
                                "scene": {
                                    "coordinateSystems": [
                                        {
                                            "id": "physical",
                                            "name": "The physical coordinate system",
                                            "axes": [
                                                {
                                                    "name": "x",
                                                    "type": "space",
                                                    "unit": "micrometer",
                                                },
                                                {
                                                    "name": "y",
                                                    "type": "space",
                                                    "unit": "micrometer",
                                                },
                                            ],
                                        }
                                    ],
                                }
                            },
                            "path": {"type": "json", "path": "./foo.json"},
                        }
                    ],
                }
            }
        )


def test_invalid_scene_missing_coordinateSystem_id():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "collection",
                            "name": "name",
                            "attributes": {
                                "scene": {
                                    "coordinateTransformations": [
                                        {
                                            "type": "translation",
                                            "translation": [0, 0, 100],
                                            "input": {"id": "physical"},
                                            "output": {"id": "world"},
                                        }
                                    ],
                                    "coordinateSystems": [
                                        {
                                            "name": "The physical coordinate system",
                                            "axes": [
                                                {
                                                    "name": "x",
                                                    "type": "space",
                                                    "unit": "micrometer",
                                                },
                                                {
                                                    "name": "y",
                                                    "type": "space",
                                                    "unit": "micrometer",
                                                },
                                            ],
                                        }
                                    ],
                                }
                            },
                            "path": {"type": "json", "path": "./foo.json"},
                        }
                    ],
                }
            }
        )


def test_invalid_multiscale_missing_nodes_or_path():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "multiscale",
                            "name": "multi",
                            "attributes": {
                                "coordinateSystems": [
                                    {
                                        "id": "coord",
                                        "axes": [
                                            {
                                                "name": "x",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                            {
                                                "name": "y",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                        ],
                                    }
                                ]
                            },
                        }
                    ],
                }
            }
        )


def test_invalid_multiscale_both_nodes_and_path():
    with pytest.raises(ValidationError):
        validate_collection(
            {
                "ome": {
                    "version": "0.x",
                    "name": "root",
                    "type": "collection",
                    "nodes": [
                        {
                            "type": "multiscale",
                            "name": "multi",
                            "attributes": {
                                "coordinateSystems": [
                                    {
                                        "id": "coord",
                                        "axes": [
                                            {
                                                "name": "x",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                            {
                                                "name": "y",
                                                "type": "space",
                                                "unit": "micrometer",
                                            },
                                        ],
                                    }
                                ]
                            },
                            "nodes": [],
                            "path": {"type": "json", "path": "./invalid.json"},
                        }
                    ],
                }
            }
        )
