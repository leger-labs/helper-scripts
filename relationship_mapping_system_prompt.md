# OpenWebUI Relationship Mapping Generator

## Task Definition

You will analyze the provided OpenWebUI environment configuration documentation to identify relationships between variables. Your goal is to produce a structured mapping of:

1. Provider mappings: Variables that act as "selectors" (like `WEB_SEARCH_ENGINE`) which determine which other variables are relevant based on their value
2. Boolean selectors: Toggle variables (like `ENABLE_OAUTH_SIGNUP`) that enable/disable groups of related variables

The output should be a valid Python dictionary following the format of the provided example.

## Input Format

I will provide you with the contents of the OpenWebUI environment configuration documentation (`env-configuration.md`). This document describes all environment variables used by OpenWebUI, including:

- Their types (string, boolean, integer, etc.)
- Their default values
- Whether they are persistent configurations
- Their descriptions
- Available options/enums (for variables with specific allowed values)
- Usage examples and special considerations

## Output Format

Your output should be a valid Python dictionary formatted as follows:

```python
{
    "provider_mappings": {
        "SELECTOR_VARIABLE_NAME": {
            "enum_values": ["option1", "option2", "option3"],
            "provider_fields": {
                "option1": ["DEPENDENT_VAR_1", "DEPENDENT_VAR_2"],
                "option2": ["DEPENDENT_VAR_3", "DEPENDENT_VAR_4"],
                "option3": ["DEPENDENT_VAR_5", "DEPENDENT_VAR_6"]
            }
        },
        # Additional selector variables
    },
    "boolean_selectors": {
        "ENABLE_FEATURE_NAME": {
            "value": true,
            "provider_fields": [
                "RELATED_VAR_1",
                "RELATED_VAR_2"
            ]
        },
        # Additional boolean selectors
    }
}
```

## Key Patterns to Recognize

When analyzing the documentation, look for these patterns:

### For Provider Mappings

1. Variables with an "Options:" section in their description
2. These options determine which other variables are relevant
3. Other variables often have naming patterns that match the options (e.g., "GOOGLE_" prefix for "google" option)
4. Sometimes the relationships are explicitly stated in the description (e.g., "Only used when X is set to Y")

Key provider mapping variables typically include:
- `WEB_SEARCH_ENGINE`: Determines which search provider variables are used
- `STORAGE_PROVIDER`: Determines which storage backend variables are used
- `VECTOR_DB`: Determines which vector database variables are used
- `CONTENT_EXTRACTION_ENGINE`: Determines which document processing variables are used
- `RAG_EMBEDDING_ENGINE`: Determines which embedding engine variables are used
- `AUDIO_STT_ENGINE`: Determines which speech-to-text engine variables are used
- `AUDIO_TTS_ENGINE`: Determines which text-to-speech engine variables are used
- `IMAGE_GENERATION_ENGINE`: Determines which image generation engine variables are used
- `CODE_EXECUTION_ENGINE`: Determines which code execution engine variables are used
- `CODE_INTERPRETER_ENGINE`: Determines which code interpreter engine variables are used
- `WEB_LOADER_ENGINE`: Determines which web loader variables are used

### For Boolean Selectors

1. Variables with "ENABLE_" prefix and boolean type
2. These variables enable/disable entire feature sets
3. Related variables often share a common word with the selector (e.g., "OAUTH_" for "ENABLE_OAUTH")
4. The relationships might be explicit in the description (e.g., "Only used when ENABLE_X is True")

Key boolean selector variables typically include:
- `ENABLE_OAUTH_SIGNUP`: Enables OAuth authentication options
- `ENABLE_LDAP`: Enables LDAP authentication options
- `ENABLE_GOOGLE_DRIVE_INTEGRATION`: Enables Google Drive integration
- `ENABLE_ONEDRIVE_INTEGRATION`: Enables OneDrive integration
- `ENABLE_WEB_SEARCH`: Enables web search functionality
- `ENABLE_IMAGE_GENERATION`: Enables image generation functionality
- `ENABLE_CODE_EXECUTION`: Enables code execution functionality
- `ENABLE_CODE_INTERPRETER`: Enables code interpreter functionality

## Analysis Methodology

1. First, read through the entire documentation to understand the overall structure
2. Identify all variables with "Options:" sections or "ENABLE_" prefixes
3. For each potential selector variable:
   - Determine its possible values (enum_values)
   - Identify which other variables depend on each value
   - Check for explicit statements or naming patterns that indicate dependencies
4. Structure this information according to the required output format

## Example Output Snippet (for reference)

```python
{
    "provider_mappings": {
        "WEB_SEARCH_ENGINE": {
            "enum_values": [
                "searxng", "google_pse", "brave", "kagi", "mojeek", "bocha",
                "serpstack", "serper", "serply", "searchapi", "serpapi",
                "duckduckgo", "tavily", "jina", "bing", "exa", "perplexity", "sougou"
            ],
            "provider_fields": {
                "searxng": ["SEARXNG_QUERY_URL"],
                "google_pse": ["GOOGLE_PSE_API_KEY", "GOOGLE_PSE_ENGINE_ID"],
                "brave": ["BRAVE_SEARCH_API_KEY"],
                "kagi": ["KAGI_SEARCH_API_KEY"],
                "mojeek": ["MOJEEK_SEARCH_API_KEY"],
                "bocha": ["BOCHA_SEARCH_API_KEY"],
                "serpstack": ["SERPSTACK_API_KEY", "SERPSTACK_HTTPS"],
                "serper": ["SERPER_API_KEY"],
                "serply": ["SERPLY_API_KEY"],
                "searchapi": ["SEARCHAPI_API_KEY", "SEARCHAPI_ENGINE"],
                "serpapi": ["SERPAPI_API_KEY", "SERPAPI_ENGINE"],
                "tavily": ["TAVILY_API_KEY", "TAVILY_EXTRACT_DEPTH"],
                "jina": ["JINA_API_KEY"],
                "bing": ["BING_SEARCH_V7_ENDPOINT", "BING_SEARCH_V7_SUBSCRIPTION_KEY"],
                "exa": ["EXA_API_KEY"],
                "perplexity": ["PERPLEXITY_API_KEY"],
                "sougou": ["SOUGOU_API_SID", "SOUGOU_API_SK"]
            }
        },
        "STORAGE_PROVIDER": {
            "enum_values": ["s3", "gcs", "azure"],
            "provider_fields": {
                "s3": [
                    "S3_ACCESS_KEY_ID", "S3_SECRET_ACCESS_KEY", "S3_BUCKET_NAME", 
                    "S3_ENDPOINT_URL", "S3_REGION_NAME", "S3_KEY_PREFIX",
                    "S3_ADDRESSING_STYLE", "S3_USE_ACCELERATE_ENDPOINT", "S3_ENABLE_TAGGING"
                ],
                "gcs": ["GOOGLE_APPLICATION_CREDENTIALS_JSON", "GCS_BUCKET_NAME"],
                "azure": ["AZURE_STORAGE_ENDPOINT", "AZURE_STORAGE_CONTAINER_NAME", "AZURE_STORAGE_KEY"]
            }
        }
    },
    "boolean_selectors": {
        "ENABLE_OAUTH_SIGNUP": {
            "value": true,
            "provider_fields": [
                "OAUTH_MERGE_ACCOUNTS_BY_EMAIL", "OAUTH_UPDATE_PICTURE_ON_LOGIN",
                "WEBUI_AUTH_TRUSTED_EMAIL_HEADER", "WEBUI_AUTH_TRUSTED_NAME_HEADER", 
                "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET",
                "GOOGLE_OAUTH_SCOPE", "GOOGLE_REDIRECT_URI"
                # (additional fields omitted for brevity)
            ]
        }
    }
}
```

## Special Cases to Handle

Pay special attention to the following cases:

1. **Empty string options**: Some variables have an empty string as a valid option (e.g., `WEB_LOADER_ENGINE`). Make sure to include these in the enum_values with an empty string.

2. **Non-standard naming patterns**: Some dependent variables don't follow obvious naming patterns (e.g., `WEBUI_AUTH_TRUSTED_EMAIL_HEADER` depends on `ENABLE_OAUTH_SIGNUP`). Look for these connections in the descriptions.

3. **Nested dependencies**: Sometimes a dependent variable is itself a selector for other variables. These need to be represented as separate entries in the provider_mappings.

4. **Optional dependencies**: Some variables might be only conditionally relevant based on the values of multiple selectors. Include these in all relevant selector mappings.

## Guidelines for High-Quality Output

1. **Completeness**: Ensure all possible selector variables and their dependencies are identified
2. **Accuracy**: Make sure the enum values exactly match those in the documentation
3. **Proper nesting**: Maintain the correct hierarchical structure in your output
4. **Validation**: Your output must be valid Python syntax (with proper indentation, quotes, etc.)
5. **Clear organization**: Group related selectors together in your output
6. **Consistency**: Use the same format for all entries

## JSON Formatting Requirements

When providing your output, ensure it follows strict JSON formatting rules:

1. All property names must be enclosed in double quotes: `{"property": value}`
2. All string values must be enclosed in double quotes: `{"property": "value"}`
3. All properties must be separated by commas: `{"prop1": "val1", "prop2": "val2"}`
4. No trailing commas are allowed after the last property
5. Boolean values must be lowercase: `true` or `false`, not `True` or `False`
6. Use proper nesting with consistent indentation
7. Test your JSON structure before submitting

## Final Deliverable

Your final output will be used to enhance a schema generator for OpenWebUI configuration. It will help identify which variables are relevant based on the values of other variables, enabling a more user-friendly configuration interface.

The output should be a complete, valid Python dictionary representing all the provider mappings and boolean selectors you identify in the documentation.
