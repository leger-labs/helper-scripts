## Description

Set of auxiliary python scripts that parse the [OWUI docs](https://raw.githubusercontent.com/open-webui/docs/refs/heads/main/docs/getting-started/env-configuration.md) into openapi spec compatible JSON file.
The two scripts expect `env-configuration.md` to be present in the same directory by default.
Output is not the final openapi spec, only the contents to be placed "schemas".

Run:
```
python variable_tracker.py
python schema_generator.py
```
