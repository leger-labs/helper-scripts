# OpenWebUI Configuration Schema Generator

Set of auxiliary Python scripts that parse the [OpenWebUI docs](https://raw.githubusercontent.com/open-webui/docs/refs/heads/main/docs/getting-started/env-configuration.md) into OpenAPI specification compatible JSON files.

## Description

These scripts process the OpenWebUI documentation on environment variables and convert it into a standardized OpenAPI schema format that can be used for configuration management, validation, and UI generation.

The process happens in two steps:
1. The `variable_tracker.py` script identifies and extracts all environment variables from the Markdown documentation
2. The `schema_generator.py` script uses this tracking data to create a complete OpenAPI schema with proper type definitions, descriptions, and metadata

## Features

- Extracts variable metadata including types, defaults, descriptions, and enums
- Preserves the detailed descriptions from "Options" sections in the documentation
- Properly handles empty enum values
- Creates both a properties-only output and a complete OpenAPI schema
- Tracks processing progress to allow for incremental updates
- Preserves all original metadata in the schema

## Requirements

- Python 3.6+
- Input Markdown file (`env-configuration.md` by default)

## Usage

1. First, run the variable tracker script to identify all environment variables:

```bash
python variable_tracker.py --input env-configuration.md --output variables_tracking.json
```

2. Then, run the schema generator to create the OpenAPI schema:

```bash
python schema_generator.py --tracking variables_tracking.json --markdown env-configuration.md --output-schema schema_properties.json --output-full-schema full_schema.json
```

## Command-line Arguments

### variable_tracker.py

- `--input`, `-i`: Path to the input Markdown file (default: `env-configuration.md`)
- `--output`, `-o`: Path to the output JSON file (default: `variables_tracking.json`)

### schema_generator.py

- `--tracking`, `-t`: Path to the tracking JSON file (default: `variables_tracking.json`)
- `--markdown`, `-m`: Path to the Markdown file (default: `env-configuration.md`)
- `--schema`, `-s`: Path to the existing schema JSON file (default: `openwebui-config.json`)
- `--output-schema`, `-o`: Path to the output properties JSON file (default: `schema_properties.json`)
- `--output-full-schema`, `-f`: Path to the output full schema JSON file (default: `full_schema.json`)
- `--output-tracking`: Path to the output tracking JSON file (default: same as tracking file)
- `--full-schema`: Save the full schema instead of just the properties

## Output Files

The scripts generate several output files:

1. `variables_tracking.json`: Contains metadata about all identified environment variables, including their order, category, and processing status
2. `schema_properties.json`: Contains just the properties section of the OpenAPI schema (for inclusion in an existing schema)
3. `full_schema.json`: Contains the complete OpenAPI schema with all required structure

## How It Works

### Variable Tracking

The variable tracker script:
1. Parses the Markdown file line by line
2. Identifies section headers (## headings) to determine categories
3. Finds all variable definitions (#### `VARIABLE_NAME`) patterns
4. Records metadata including the original line number, category, and processing order

### Schema Generation

The schema generator script:
1. Loads the tracking data and Markdown file
2. For each unprocessed variable:
   - Extracts its complete definition section from the Markdown
   - Parses details like type, default value, description, and options
   - Converts these details to OpenAPI schema format
   - Captures all enum values, including empty string values
   - Preserves option descriptions within the schema
3. Generates both a properties-only output and a complete schema

## Example

For a variable definition like:

```markdown
#### `WEB_LOADER_ENGINE`

- Type: `str`
- Default: `safe_web`
- Description: Specifies the loader to use for retrieving and processing web content.
- Options:
  - `` - Uses the `requests` module with enhanced error handling.
  - `playwright` - Uses Playwright for more advanced web page rendering and interaction.
- Persistence: This environment variable is a `PersistentConfig` variable.
```

The schema generator will produce:

```json
{
  "WEB_LOADER_ENGINE": {
    "type": "string",
    "description": "Specifies the loader to use for retrieving and processing web content.\n\nOptions:\n  - Empty string - Uses the `requests` module with enhanced error handling.\n  - `playwright` - Uses Playwright for more advanced web page rendering and interaction.",
    "x-env-var": "WEB_LOADER_ENGINE",
    "x-persistent-config": true,
    "x-category": "Web Search",
    "x-display-order": 201,
    "default": "safe_web",
    "enum": [
      "",
      "playwright"
    ]
  }
}
```

## Limitations

- The scripts assume a specific format for the Markdown documentation
- Variables must follow the pattern `#### \`VARIABLE_NAME\``
- Options must be indented with two spaces and enclosed in backticks
- References to other variables must follow the pattern "The value of `VARIABLE_NAME` environment variable"

## Contributing

Feel free to submit issues or pull requests for any improvements or bug fixes to the schema generation process.
