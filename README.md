# NGFF RFC-8 collection validator

Proof of concept of validation tools for NGFF RFC-8 collections based on JSON Schemas - see https://ngff.openmicroscopy.org/rfc/8/index.html.

> ⚠️ **WARNING**: This project is a proof of concept. It is experimental, unstable, and not intended for production use.

## JSON Schemas

Schema files are available in the [`schemas` folder](./schemas).

> **NOTE**: This repository does not include any schema for the [HCS metadata](https://ngff.openmicroscopy.org/rfc/8/index.html#high-content-screening-hcs-metadata) yet.
> Also note that this is not a canonical definition of what may be part of the schemas, but a proof of concept of how such schemas may look like.

## Python package

The `ngff-rfc8` Python package contains the static JSON Schema files, and it exposes a simple validation function and a command-line interface.

A library-usage example looks like
```python
from ngff_rfc8.validate import validate_collection

data = {
    "ome": {
        "version": "0.x",
        "type": "collection",
        "name": "My Collection",
        "id": "some-collection-id",
        "attributes": {},
        "nodes": [],
    }
}
validate_collection(data)
```
while a command-line-interface example looks like
```bash
ngff-rfc-8-validate /some/collection.json
```
(from a Python environment where the package is installed).

## JavaScript package

To include the JavaScript package in other projects, install the library from the release artifacts:

```bash
npm install https://github.com/fractal-analytics-platform/ngff-rfc8-validator/releases/download/v0.0.1-a1/ngff-rfc8-validator-v0.0.1-a1.tgz
```

Then, import the validate function:

```javascript
import { validate } from '@fractal-analytics-platform/ngff-rfc8-validator';

validate(data);
```

## Considerations about the schema structure

The [main node schema](./schemas/node.json) needs to discriminate between various subschema according to the `type` field. The most natural approach would be using the `oneOf` keyword. Unfortunately, this solution tends to produce a large number of misleading errors, referring to branches which don't match the specified `type`. For this reason we produced an equivalent schema using a combination of `allOf` and `if`/`then` keywords. This resulted in a reduction of the number of errors.

The same logic has been applied to [collection schema](./schemas/collection.json) and [multiscale schema](./schemas/multiscale.json) to handle the `nodes`/`path` switch.

## Development

Python:

```bash
# Init
uv venv
uv sync --all-groups

# Run tests
uv run pytest python/tests

# Generate single-file JSON Schema
uv run python3 python/scripts/build_single_schema.py > ngff-rfc8.json
```

JavaScript:

```bash
# Init
cd javascript
npm ci
npm run build

# Run tests
npm run test
```

## Contributors and license

The Fractal project is developed by the [BioVisionCenter](https://www.biovisioncenter.uzh.ch/en.html) at the University of Zurich, who contracts [eXact lab s.r.l.](https://www.exact-lab.it/en/) for software engineering and development support.

Unless otherwise specified, Fractal components are released under the BSD 3-Clause License, and copyright is with the BioVisionCenter at the University of Zurich.
