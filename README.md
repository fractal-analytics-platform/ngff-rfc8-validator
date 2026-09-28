# NGFF RFC-8 JSON Schemas

Preliminary JSON Schemas for NGFF RFC-8 (collections) - see https://ngff.openmicroscopy.org/rfc/8/index.html.

## Develpoment (Python)

```bash
uv venv
uv sync --all-extras
```

### Run tests

```bash
uv run pytest python/tests
```

## Validate JSON file

```bash
uv run ngff-rfc-8-validate <file>
```

## Generate single-file JSON Schema

```bash
uv run python3 python/scripts/build_single_schema.py > ngff-rfc8.json
```

## Development (JavaScript)

```bash
npm ci
npm run build
```

### Run tests

```bash
npm run test
```

### Include in other projects

Install the library from the release artifacts:

```bash
npm install https://github.com/fractal-analytics-platform/ngff-rfc8-validator/releases/download/v0.0.1-a1/ngff-rfc8-validator-v0.0.1-a1.tgz
```

Import the validate function in a JavaScript file:

```javascript
import { validate } from '@fractal-analytics-platform/ngff-rfc8-validator';
```
