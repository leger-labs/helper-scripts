#!/usr/bin/env python3
"""
OpenWebUI Configuration Schema Generator

A unified script that generates an OpenAPI schema from Markdown documentation
of OpenWebUI environment variables. It properly extracts types, defaults, enums,
and other metadata, then enhances the schema with provider relationships.

Usage:
  python openwebui_schema_generator.py [--input INPUT_MARKDOWN] [--output OUTPUT_SCHEMA]
"""

import re
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Regular expressions for extracting variable details
VARIABLE_PATTERN = r"^#### `([A-Z][A-Z0-9_]+)`$"
TYPE_PATTERN = r"- Type: `([^`]+)`"
DEFAULT_PATTERN = r"- Default: `?([^`\n]+)`?"
DEFAULT_PATTERN_EMPTY = r"- Default: Empty string \(''\), since `None` is set as default\."
PERSISTENCE_PATTERN = r"- Persistence: This environment variable is a `PersistentConfig` variable\."
DESCRIPTION_PATTERN = r"- Description: (.+?)(?=\n\n|\n-|$)"
OPTIONS_PATTERN = r"- Options:([\s\S]*?)(?=\n\n|\n-|$)"

# Python type mappings to JSON Schema types
TYPE_MAPPINGS = {
    "str": "string",
    "string": "string",
    "int": "integer",
    "integer": "integer",
    "float": "number",
    "number": "number",
    "bool": "boolean",
    "boolean": "boolean",
    "list": "array",
    "dict": "object"
}

# Hardcoded default templates (used for prompt templates)
DEFAULT_TEMPLATES = {
    "DEFAULT_TITLE_GENERATION_PROMPT_TEMPLATE": """### Task:
Generate a concise, 3-5 word title with an emoji summarizing the chat history.
### Guidelines:
- The title should clearly represent the main theme or subject of the conversation.
- Use emojis that enhance understanding of the topic, but avoid quotation marks or special formatting.
- Write the title in the chat's primary language; default to English if multilingual.
- Prioritize accuracy over excessive creativity; keep it clear and simple.
### Output:
JSON format: { "title": "your concise title here" }
### Examples:
- { "title": "📉 Stock Market Trends" },
- { "title": "🍪 Perfect Chocolate Chip Recipe" },
- { "title": "Evolution of Music Streaming" },
- { "title": "Remote Work Productivity Tips" },
- { "title": "Artificial Intelligence in Healthcare" },
- { "title": "🎮 Video Game Development Insights" }
### Chat History:
<chat_history>
{{MESSAGES:END:2}}
</chat_history>""",

    "DEFAULT_TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE": """Available Tools: {{TOOLS}}

Your task is to choose and return the correct tool(s) from the list of available tools based on the query. Follow these guidelines:

- Return only the JSON object, without any additional text or explanation.

- If no tools match the query, return an empty array: 
   {
     "tool_calls": []
   }

- If one or more tools match the query, construct a JSON response containing a "tool_calls" array with objects that include:
   - "name": The tool's name.
   - "parameters": A dictionary of required parameters and their corresponding values.

The format for the JSON response is strictly:
{
  "tool_calls": [
    {"name": "toolName1", "parameters": {"key1": "value1"}},
    {"name": "toolName2", "parameters": {"key2": "value2"}}
  ]
}""",

    "DEFAULT_TAGS_GENERATION_PROMPT_TEMPLATE": """### Task:
Generate 1-3 broad tags categorizing the main themes of the chat history, along with 1-3 more specific subtopic tags.

### Guidelines:
- Start with high-level domains (e.g. Science, Technology, Philosophy, Arts, Politics, Business, Health, Sports, Entertainment, Education)
- Consider including relevant subfields/subdomains if they are strongly represented throughout the conversation
- If content is too short (less than 3 messages) or too diverse, use only ["General"]
- Use the chat's primary language; default to English if multilingual
- Prioritize accuracy over specificity

### Output:
JSON format: { "tags": ["tag1", "tag2", "tag3"] }

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>""",

    "DEFAULT_RAG_TEMPLATE": """### Task:
Respond to the user query using the provided context, incorporating inline citations in the format [id] **only when the <source> tag includes an explicit id attribute** (e.g., <source id="1">).

### Guidelines:
- If you don't know the answer, clearly state that.
- If uncertain, ask the user for clarification.
- Respond in the same language as the user's query.
- If the context is unreadable or of poor quality, inform the user and provide the best possible answer.
- If the answer isn't present in the context but you possess the knowledge, explain this to the user and provide the answer using your own understanding.
- **Only include inline citations using [id] (e.g., [1], [2]) when the <source> tag includes an id attribute.**
- Do not cite if the <source> tag does not contain an id attribute.
- Do not use XML tags in your response.
- Ensure citations are concise and directly related to the information provided.

### Example of Citation:
If the user asks about a specific topic and the information is found in a source with a provided id attribute, the response should include the citation like in the following example:
* "According to the study, the proposed method increases efficiency by 20% [1]."

### Output:
Provide a clear and direct response to the user's query, including inline citations in the format [id] only when the <source> tag with id attribute is present in the context.

<context>
{{CONTEXT}}
</context>

<user_query>
{{QUERY}}
</user_query>""",

    "DEFAULT_QUERY_GENERATION_PROMPT_TEMPLATE": """### Task:
Analyze the chat history to determine the necessity of generating search queries, in the given language. By default, **prioritize generating 1-3 broad and relevant search queries** unless it is absolutely certain that no additional information is required. The aim is to retrieve comprehensive, updated, and valuable information even with minimal uncertainty. If no search is unequivocally needed, return an empty list.

### Guidelines:
- Respond **EXCLUSIVELY** with a JSON object. Any form of extra commentary, explanation, or additional text is strictly prohibited.
- When generating search queries, respond in the format: { "queries": ["query1", "query2"] }, ensuring each query is distinct, concise, and relevant to the topic.
- If and only if it is entirely certain that no useful results can be retrieved by a search, return: { "queries": [] }.
- Err on the side of suggesting search queries if there is **any chance** they might provide useful or updated information.
- Be concise and focused on composing high-quality search queries, avoiding unnecessary elaboration, commentary, or assumptions.
- Today's date is: {{CURRENT_DATE}}.
- Always prioritize providing actionable and broad queries that maximize informational coverage.

### Output:
Strictly return in JSON format: 
{
  "queries": ["query1", "query2"]
}

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>""",

    "DEFAULT_IMAGE_PROMPT_GENERATION_PROMPT_TEMPLATE": """### Task:
Generate a detailed prompt for am image generation task based on the given language and context. Describe the image as if you were explaining it to someone who cannot see it. Include relevant details, colors, shapes, and any other important elements.

### Guidelines:
- Be descriptive and detailed, focusing on the most important aspects of the image.
- Avoid making assumptions or adding information not present in the image.
- Use the chat's primary language; default to English if multilingual.
- If the image is too complex, focus on the most prominent elements.

### Output:
Strictly return in JSON format:
{
    "prompt": "Your detailed description here."
}

### Chat History:
<chat_history>
{{MESSAGES:END:6}}
</chat_history>"""
}

# Provider mappings for relationships
PROVIDER_MAPPINGS = {
    # Web Search Engines
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
    
    # Storage Providers
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
    },
    
    # Vector Databases
    "VECTOR_DB": {
        "enum_values": ["chroma", "elasticsearch", "milvus", "opensearch", "pgvector", "qdrant", "pinecone"],
        "provider_fields": {
            "chroma": [
                "CHROMA_TENANT", "CHROMA_DATABASE", "CHROMA_HTTP_HOST", 
                "CHROMA_HTTP_PORT", "CHROMA_HTTP_HEADERS", "CHROMA_HTTP_SSL",
                "CHROMA_CLIENT_AUTH_PROVIDER", "CHROMA_CLIENT_AUTH_CREDENTIALS"
            ],
            "elasticsearch": [
                "ELASTICSEARCH_API_KEY", "ELASTICSEARCH_CA_CERTS",
                "ELASTICSEARCH_CLOUD_ID", "ELASTICSEARCH_INDEX_PREFIX",
                "ELASTICSEARCH_PASSWORD", "ELASTICSEARCH_URL", "ELASTICSEARCH_USERNAME"
            ],
            "milvus": [
                "MILVUS_URI", "MILVUS_DB", "MILVUS_TOKEN", "MILVUS_INDEX_TYPE",
                "MILVUS_METRIC_TYPE", "MILVUS_HNSW_M", "MILVUS_HNSW_EFCONSTRUCTION",
                "MILVUS_IVF_FLAT_NLIST"
            ],
            "opensearch": [
                "OPENSEARCH_CERT_VERIFY", "OPENSEARCH_PASSWORD",
                "OPENSEARCH_SSL", "OPENSEARCH_URI", "OPENSEARCH_USERNAME"
            ],
            "pgvector": ["PGVECTOR_DB_URL", "PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH"],
            "qdrant": [
                "QDRANT_API_KEY", "QDRANT_URI", "QDRANT_ON_DISK",
                "QDRANT_PREFER_GRPC", "QDRANT_GRPC_PORT", "ENABLE_QDRANT_MULTITENANCY_MODE"
            ],
            "pinecone": [
                "PINECONE_API_KEY", "PINECONE_ENVIRONMENT", "PINECONE_INDEX_NAME",
                "PINECONE_DIMENSION", "PINECONE_METRIC", "PINECONE_CLOUD"
            ]
        }
    },
    
    # Content Extraction Engine
    "CONTENT_EXTRACTION_ENGINE": {
        "enum_values": ["tika", "docling", "document_intelligence", "mistral_ocr"],
        "provider_fields": {
            "tika": ["TIKA_SERVER_URL"],
            "docling": ["DOCLING_SERVER_URL", "DOCLING_OCR_ENGINE", "DOCLING_OCR_LANG"],
            "document_intelligence": ["DOCUMENT_INTELLIGENCE_ENDPOINT", "DOCUMENT_INTELLIGENCE_KEY"],
            "mistral_ocr": ["MISTRAL_OCR_API_KEY"]
        }
    },
    
    # RAG Embedding Engine
    "RAG_EMBEDDING_ENGINE": {
        "enum_values": ["ollama", "openai"],
        "provider_fields": {
            "ollama": ["RAG_OLLAMA_API_KEY", "RAG_OLLAMA_BASE_URL"],
            "openai": [
                "RAG_OPENAI_API_BASE_URL", "RAG_OPENAI_API_KEY",
                "RAG_EMBEDDING_OPENAI_BATCH_SIZE"
            ]
        }
    },
    
    # Speech-to-Text Engines
    "AUDIO_STT_ENGINE": {
        "enum_values": ["openai", "deepgram", "azure"],
        "provider_fields": {
            "openai": ["AUDIO_STT_MODEL", "AUDIO_STT_OPENAI_API_BASE_URL", "AUDIO_STT_OPENAI_API_KEY"],
            "deepgram": ["DEEPGRAM_API_KEY"],
            "azure": ["AUDIO_STT_AZURE_API_KEY", "AUDIO_STT_AZURE_REGION", "AUDIO_STT_AZURE_LOCALES"]
        }
    },
    
    # Text-to-Speech Engines
    "AUDIO_TTS_ENGINE": {
        "enum_values": ["azure", "elevenlabs", "openai", "transformers"],
        "provider_fields": {
            "azure": ["AUDIO_TTS_AZURE_SPEECH_REGION", "AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT", "AUDIO_TTS_API_KEY"],
            "elevenlabs": ["AUDIO_TTS_API_KEY"],
            "openai": [
                "AUDIO_TTS_MODEL", "AUDIO_TTS_VOICE", "AUDIO_TTS_SPLIT_ON",
                "AUDIO_TTS_OPENAI_API_BASE_URL", "AUDIO_TTS_OPENAI_API_KEY"
            ],
            "transformers": []
        }
    },
    
    # Image Generation Engines
    "IMAGE_GENERATION_ENGINE": {
        "enum_values": ["openai", "comfyui", "automatic1111", "gemini"],
        "provider_fields": {
            "openai": ["IMAGES_OPENAI_API_BASE_URL", "IMAGES_OPENAI_API_KEY"],
            "comfyui": ["COMFYUI_BASE_URL", "COMFYUI_API_KEY", "COMFYUI_WORKFLOW"],
            "automatic1111": [
                "AUTOMATIC1111_BASE_URL", "AUTOMATIC1111_API_AUTH", 
                "AUTOMATIC1111_CFG_SCALE", "AUTOMATIC1111_SAMPLER", "AUTOMATIC1111_SCHEDULER"
            ],
            "gemini": [
                "GEMINI_API_BASE_URL", "GEMINI_API_KEY",
                "IMAGES_GEMINI_API_BASE_URL", "IMAGES_GEMINI_API_KEY"
            ]
        }
    },
    
    # Code Execution Engine
    "CODE_EXECUTION_ENGINE": {
        "enum_values": ["pyodide", "jupyter"],
        "provider_fields": {
            "pyodide": [],
            "jupyter": [
                "CODE_EXECUTION_JUPYTER_URL", "CODE_EXECUTION_JUPYTER_AUTH",
                "CODE_EXECUTION_JUPYTER_AUTH_TOKEN", "CODE_EXECUTION_JUPYTER_AUTH_PASSWORD",
                "CODE_EXECUTION_JUPYTER_TIMEOUT"
            ]
        }
    },
    
    # Code Interpreter Engine
    "CODE_INTERPRETER_ENGINE": {
        "enum_values": ["pyodide", "jupyter"],
        "provider_fields": {
            "pyodide": [],
            "jupyter": [
                "CODE_INTERPRETER_JUPYTER_URL", "CODE_INTERPRETER_JUPYTER_AUTH",
                "CODE_INTERPRETER_JUPYTER_AUTH_TOKEN", "CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD",
                "CODE_INTERPRETER_JUPYTER_TIMEOUT"
            ]
        }
    },
    
    # Web Loader Engine
    "WEB_LOADER_ENGINE": {
        "enum_values": ["", "playwright"],
        "provider_fields": {
            "": [],
            "playwright": ["PLAYWRIGHT_WS_URL", "PLAYWRIGHT_TIMEOUT"]
        }
    }
}

# Boolean selectors (like ENABLE_OAUTH_SIGNUP, ENABLE_LDAP)
BOOLEAN_SELECTORS = {
    "ENABLE_OAUTH_SIGNUP": {
        "value": True,
        "provider_fields": [
            "OAUTH_MERGE_ACCOUNTS_BY_EMAIL", "OAUTH_UPDATE_PICTURE_ON_LOGIN",
            "WEBUI_AUTH_TRUSTED_EMAIL_HEADER", "WEBUI_AUTH_TRUSTED_NAME_HEADER", 
            "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET",
            "GOOGLE_OAUTH_SCOPE", "GOOGLE_REDIRECT_URI", "MICROSOFT_CLIENT_ID",
            "MICROSOFT_CLIENT_SECRET", "MICROSOFT_CLIENT_TENANT_ID", "MICROSOFT_OAUTH_SCOPE",
            "MICROSOFT_REDIRECT_URI", "GITHUB_CLIENT_ID", "GITHUB_CLIENT_SECRET",
            "GITHUB_CLIENT_SCOPE", "GITHUB_CLIENT_REDIRECT_URI", "OAUTH_CLIENT_ID",
            "OAUTH_CLIENT_SECRET", "OPENID_PROVIDER_URL", "OPENID_REDIRECT_URI",
            "OAUTH_SCOPES", "OAUTH_CODE_CHALLENGE_METHOD", "OAUTH_PROVIDER_NAME",
            "OAUTH_USERNAME_CLAIM", "OAUTH_EMAIL_CLAIM", "OAUTH_PICTURE_CLAIM",
            "OAUTH_GROUP_CLAIM", "ENABLE_OAUTH_ROLE_MANAGEMENT", "ENABLE_OAUTH_GROUP_MANAGEMENT",
            "OAUTH_ROLES_CLAIM", "OAUTH_ALLOWED_ROLES", "OAUTH_ADMIN_ROLES",
            "OAUTH_ALLOWED_DOMAINS"
        ]
    },
    "ENABLE_LDAP": {
        "value": True,
        "provider_fields": [
            "LDAP_SERVER_LABEL", "LDAP_SERVER_HOST", "LDAP_SERVER_PORT",
            "LDAP_ATTRIBUTE_FOR_MAIL", "LDAP_ATTRIBUTE_FOR_USERNAME",
            "LDAP_APP_DN", "LDAP_APP_PASSWORD", "LDAP_SEARCH_BASE",
            "LDAP_SEARCH_FILTER", "LDAP_SEARCH_FILTERS", "LDAP_USE_TLS",
            "LDAP_CA_CERT_FILE", "LDAP_VALIDATE_CERT", "LDAP_CIPHERS"
        ]
    },
    "ENABLE_GOOGLE_DRIVE_INTEGRATION": {
        "value": True,
        "provider_fields": [
            "GOOGLE_DRIVE_CLIENT_ID", "GOOGLE_DRIVE_API_KEY"
        ]
    },
    "ENABLE_ONEDRIVE_INTEGRATION": {
        "value": True,
        "provider_fields": [
            "ONEDRIVE_CLIENT_ID"
        ]
    }
}

def parse_markdown(file_path: str) -> Tuple[Dict[str, Dict], List[str]]:
    """
    Parse the Markdown file to extract environment variables information.
    
    Args:
        file_path: Path to the Markdown file
        
    Returns:
        A tuple of (variable_info, markdown_lines)
        variable_info is a dictionary of variables with their metadata
        markdown_lines is the list of lines from the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise
    
    # Split the content into lines
    lines = content.split('\n')
    
    # Dictionary to store variable information
    variable_info = {}
    
    # Track categories and current category
    current_category = None
    categories = {}
    variable_order = 1
    
    # Process each line
    for i, line in enumerate(lines):
        # Check for category (section) headers
        category_match = re.match(r"^##\s+(.+)$", line)
        if category_match:
            current_category = category_match.group(1).strip()
            if current_category not in categories:
                categories[current_category] = []
            continue
        
        # Check for subcategory headers
        subcategory_match = re.match(r"^###\s+(.+)$", line)
        if subcategory_match:
            current_subcategory = subcategory_match.group(1).strip()
            # Store subcategory as part of the category name
            if current_category:
                full_category = f"{current_category} - {current_subcategory}"
                if full_category not in categories:
                    categories[full_category] = []
                current_category = full_category
            continue
        
        # Check for variable headers
        var_match = re.match(VARIABLE_PATTERN, line)
        if var_match:
            var_name = var_match.group(1)
            if var_name not in variable_info:
                variable_info[var_name] = {
                    "line_number": i,
                    "category": current_category,
                    "order": variable_order
                }
                if current_category:
                    categories[current_category].append(var_name)
                variable_order += 1
    
    return variable_info, lines

def extract_options_from_section(section: str, var_name: str = None) -> tuple:
    """
    Extract options from a section and create enum values and descriptions.
    
    Args:
        section: The section text containing options
        var_name: Optional variable name for debugging
        
    Returns:
        A tuple containing (enum_values, options_description)
    """
    options_match = re.search(OPTIONS_PATTERN, section, re.DOTALL)
    if not options_match:
        return None, None
    
    options_text = options_match.group(1).strip()
    enum_values = []
    options_description = "Options:\n"
    
    # Special case handling for known variables with formatting issues
    if var_name == "ENV":
        # Manual extraction for ENV which we know has specific formatting issues
        enum_values = ["dev", "prod"]
        options_description = "Options:\n  - `dev` - Enables the FastAPI API documentation on `/docs`\n  - `prod` - Automatically configures several environment variables\n"
        return enum_values, options_description
    
    # Try multiple patterns to capture different formatting styles
    
    # First pattern: standard format with backticks and dash (with description)
    pattern1 = r"\s*[-*]\s+`([^`]*)`\s*-\s*(.*?)(?=\n\s*[-*]|\n\n|\n-|$)"
    
    # Second pattern: for empty string option that might be formatted differently
    pattern2 = r"\s*[-*]\s+Empty string\s*[-\(]?\s*(.*?)(?=\n\s*[-*]|\n\n|\n-|$)"
    
    # Third pattern: another format that might be used
    pattern3 = r"\s*[-*]\s+['\"](.*?)['\"]\s*-\s*(.*?)(?=\n\s*[-*]|\n\n|\n-|$)"
    
    # Fourth pattern: for options listed with backticks but no description
    pattern4 = r"\s*[-*]\s+`([^`]+)`\s*(?=\n|$)"
    
    # Combine patterns for better matching
    all_patterns = [pattern1, pattern2, pattern3, pattern4]
    
    for pattern in all_patterns:
        matches = list(re.finditer(pattern, options_text, re.DOTALL))
        
        for match in matches:
            if pattern == pattern1:  # Standard backtick format with description
                enum_value = match.group(1)
                enum_description = match.group(2).strip()
            elif pattern == pattern2:  # Empty string description
                enum_value = ""
                enum_description = match.group(1).strip()
            elif pattern == pattern3:  # Quote format
                enum_value = match.group(1)
                enum_description = match.group(2).strip()
            elif pattern == pattern4:  # Backticks without description
                enum_value = match.group(1)
                enum_description = ""  # No description provided
            
            # Check if this value is already in our list
            if enum_value not in enum_values:
                enum_values.append(enum_value)
                
                # Add the description to the options description
                if enum_value == "":
                    options_description += f"  - Empty string - {enum_description}\n"
                elif enum_description:
                    options_description += f"  - `{enum_value}` - {enum_description}\n"
                else:
                    options_description += f"  - `{enum_value}`\n"
    
    # Special case for WEB_LOADER_ENGINE - ensure empty string option is captured
    if var_name == "WEB_LOADER_ENGINE":
        # Check if we already have the empty string
        if not any(v == "" for v in enum_values):
            # Look for the empty string option specifically in the text
            empty_match = re.search(r"['\"]{2}|``\s*-\s*(.*?)(?=\n|$)", options_text, re.DOTALL)
            if empty_match:
                enum_values.insert(0, "")
                empty_desc = empty_match.group(1).strip() if len(empty_match.groups()) > 0 else "Uses the `requests` module with enhanced error handling."
                options_description = "Options:\n  - Empty string - " + empty_desc + "\n"
                
                # Add back the other options
                for i, v in enumerate(enum_values):
                    if v != "":
                        options_description += f"  - `{v}` - "
                        # Find the existing description for this value
                        desc_match = re.search(f"`{v}`\\s*-\\s*(.*?)(?=\\n\\s*[-*]|\\n\\n|\\n-|$)", section, re.DOTALL)
                        if desc_match:
                            options_description += f"{desc_match.group(1).strip()}\n"
    
    return (enum_values, options_description) if enum_values else (None, None)

def extract_variable_details(md_lines: List[str], var_name: str, line_number: int) -> Dict:
    """
    Extract detailed information for a variable from the Markdown content.
    
    Args:
        md_lines: The Markdown content as a list of lines
        var_name: The name of the variable to extract details for
        line_number: The line number where the variable is defined
        
    Returns:
        A dictionary with the extracted details
    """
    details = {
        "name": var_name,
        "type": "string",  # Default type
        "default": None,
        "references_var": None,
        "description": "",
        "enum": None,
        "options_description": None,
        "is_persistent_config": False,
        "sensitive": False
    }
    
    # Start from the variable definition and read until the next variable definition
    i = line_number
    section_text = []
    while i < len(md_lines):
        line = md_lines[i].strip()
        if i > line_number and re.match(r"^#### `[A-Z][A-Z0-9_]+`$", line):
            break
        section_text.append(md_lines[i])
        i += 1
    
    section = "\n".join(section_text)
    
    # Extract type
    type_match = re.search(TYPE_PATTERN, section, re.MULTILINE)
    raw_type = ""
    if type_match:
        raw_type = type_match.group(1).lower()
        if raw_type in TYPE_MAPPINGS:
            details["type"] = TYPE_MAPPINGS[raw_type]
        else:
            logger.warning(f"Unknown type '{raw_type}' for variable {var_name}. Using 'string' as default.")
    
    # Check for references to default templates
    default_ref_pattern = r"- Default: The value of `([A-Z][A-Z0-9_]+)` environment variable\."
    default_ref_match = re.search(default_ref_pattern, section, re.MULTILINE)
    
    if default_ref_match:
        # This variable references another variable as its default
        referenced_var = default_ref_match.group(1)
        details["references_var"] = referenced_var
        
        # Check if this is one of our hardcoded default templates
        if referenced_var in DEFAULT_TEMPLATES:
            # Use the default template content as the default value
            details["default"] = DEFAULT_TEMPLATES[referenced_var]
    else:
        # Extract regular default value
        default_match = re.search(DEFAULT_PATTERN, section, re.MULTILINE)
        empty_default_match = re.search(DEFAULT_PATTERN_EMPTY, section, re.MULTILINE)
        
        if empty_default_match:
            details["default"] = ""
        elif default_match:
            default_value = default_match.group(1).strip()
            
            # Convert default value to the appropriate type
            if details["type"] == "boolean":
                if default_value.lower() in ["true", "yes", "1"]:
                    details["default"] = True
                elif default_value.lower() in ["false", "no", "0"]:
                    details["default"] = False
                else:
                    # Keep as string if we can't determine the boolean value
                    details["default"] = default_value
            elif details["type"] == "integer":
                try:
                    details["default"] = int(default_value)
                except ValueError:
                    # If it's not a valid integer, keep the original string
                    details["default"] = default_value
            elif details["type"] == "number":
                try:
                    details["default"] = float(default_value)
                except ValueError:
                    # If it's not a valid number, keep the original string
                    details["default"] = default_value
            else:
                # For string and other types, keep as is
                details["default"] = default_value
    
    # Extract description
    desc_match = re.search(DESCRIPTION_PATTERN, section, re.MULTILINE | re.DOTALL)
    if desc_match:
        details["description"] = desc_match.group(1).strip()
    
    # Check if it's a PersistentConfig variable
    if re.search(PERSISTENCE_PATTERN, section, re.MULTILINE):
        details["is_persistent_config"] = True
    
    # Extract enum values and options description
    enum_values, options_description = extract_options_from_section(section, var_name)
    if enum_values:
        details["enum"] = enum_values
    if options_description:
        details["options_description"] = options_description
        # Append options description to main description if available
        if details["description"] and options_description:
            details["description"] = f"{details['description']}\n\n{options_description}"
    
    # Check if the variable is sensitive (contains words like "key", "password", "secret", "token")
    sensitive_keywords = ["key", "password", "secret", "token", "credentials"]
    if any(kw in var_name.lower() for kw in sensitive_keywords):
        details["sensitive"] = True
    
    return details

def create_schema_property(details: Dict) -> Dict:
    """
    Create an OpenAPI schema property for a variable.
    
    Args:
        details: The extracted details for the variable
        
    Returns:
        The schema property as a dictionary
    """
    prop = {
        "type": details["type"],
        "description": details["description"],
        "x-env-var": details["name"],
        "x-persistent-config": details["is_persistent_config"],
        "x-category": details.get("category", "Uncategorized"),
        "x-display-order": details.get("order", 0)
    }
    
    # Add default value if present
    if details["default"] is not None:
        prop["default"] = details["default"]
    
    # Add references to default templates if applicable
    if details.get("references_var") in DEFAULT_TEMPLATES:
        prop["x-references-var"] = details["references_var"]
        
        # Add helper property for .env file generation
        template_content = DEFAULT_TEMPLATES[details["references_var"]]
        escaped_content = template_content.replace('"', '\\"')
        prop["x-env-template"] = f'"{escaped_content}"'
    
    # Add enum values if present
    if details.get("enum"):
        prop["enum"] = details["enum"]
    
    # Add sensitive flag if applicable
    if details["sensitive"]:
        prop["x-sensitive"] = True
    
    return prop

def enhance_schema_with_providers(schema_properties: Dict) -> Dict:
    """
    Enhances the schema with provider relationships.
    
    Args:
        schema_properties: The schema properties to enhance
        
    Returns:
        The enhanced schema properties
    """
    # Copy the schema to avoid modifying the original
    properties = schema_properties.copy()
    
    # Add provider relationships from PROVIDER_MAPPINGS
    for selector_var, mapping in PROVIDER_MAPPINGS.items():
        if selector_var in properties:
            # Add enum values if they don't exist already
            if "enum" not in properties[selector_var] and "enum_values" in mapping:
                properties[selector_var]["enum"] = mapping["enum_values"]
            
            # Add x-provider-fields extension
            if "provider_fields" in mapping:
                properties[selector_var]["x-provider-fields"] = mapping["provider_fields"]
                
                # Add x-depends-on to all dependent fields
                for provider, fields in mapping["provider_fields"].items():
                    for field in fields:
                        if field in properties:
                            properties[field]["x-depends-on"] = {selector_var: provider}
    
    # Handle boolean selectors
    for selector_var, mapping in BOOLEAN_SELECTORS.items():
        if selector_var in properties:
            # Add x-provider-fields extension with the list of dependent fields
            properties[selector_var]["x-provider-fields"] = mapping["provider_fields"]
            
            # Add x-depends-on to all dependent fields
            for field in mapping["provider_fields"]:
                if field in properties:
                    properties[field]["x-depends-on"] = {selector_var: mapping["value"]}
    
    return properties

def generate_schema(md_file: str) -> Dict:
    """
    Generate a complete OpenAPI schema from the Markdown documentation.
    
    Args:
        md_file: Path to the Markdown file
        
    Returns:
        The complete OpenAPI schema
    """
    # Parse the Markdown file
    variable_info, markdown_lines = parse_markdown(md_file)
    
    # Extract details for each variable
    schema_properties = {}
    for var_name, var_info in variable_info.items():
        try:
            # Skip DEFAULT_*_TEMPLATE variables
            if var_name.startswith("DEFAULT_") and var_name.endswith("_TEMPLATE"):
                continue
            
            # Extract details
            details = extract_variable_details(markdown_lines, var_name, var_info["line_number"])
            
            # Add category and order
            details["category"] = var_info["category"]
            details["order"] = var_info["order"]
            
            # Create schema property
            schema_prop = create_schema_property(details)
            
            # Add to schema properties
            schema_properties[var_name] = schema_prop
            
        except Exception as e:
            logger.error(f"Error processing variable {var_name}: {e}")
    
    # Enhance schema with provider relationships
    enhanced_properties = enhance_schema_with_providers(schema_properties)
    
    # Create the full OpenAPI schema
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "OpenWebUI Configuration",
            "description": "Configuration schema for OpenWebUI environment variables",
            "version": "0.7.0"  # Update this version if needed
        },
        "paths": {},
        "components": {
            "schemas": {
                "OpenWebUIConfig": {
                    "type": "object",
                    "properties": enhanced_properties,
                    "required": []
                }
            }
        }
    }
    
    return schema

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate OpenAPI schema for OpenWebUI environment variables')
    parser.add_argument('--input', '-i', default='docs/getting-started/env-configuration.md', 
                        help='Path to the input Markdown file (default: docs/getting-started/env-configuration.md)')
    parser.add_argument('--output', '-o', default='openwebui-config-schema.json', 
                        help='Path to the output schema JSON file (default: openwebui-config-schema.json)')
    parser.add_argument('--properties-only', '-p', action='store_true',
                        help='Output only the properties section of the schema')
    args = parser.parse_args()
    
    try:
        # Generate the schema
        schema = generate_schema(args.input)
        
        # Save the schema
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.properties_only:
                # Extract only the properties
                properties = schema["components"]["schemas"]["OpenWebUIConfig"]["properties"]
                json.dump(properties, f, indent=2, ensure_ascii=False)
                logger.info(f"Schema properties saved to {args.output}")
            else:
                # Save the full schema
                json.dump(schema, f, indent=2, ensure_ascii=False)
                logger.info(f"Full schema saved to {args.output}")
        
        # Log statistics
        variable_count = len(schema["components"]["schemas"]["OpenWebUIConfig"]["properties"])
        categories = set(prop.get("x-category", "Uncategorized") 
                      for prop in schema["components"]["schemas"]["OpenWebUIConfig"]["properties"].values())
        
        print(f"Schema generation completed successfully!")
        print(f"Processed {variable_count} variables across {len(categories)} categories")
        
    except Exception as e:
        logger.error(f"Error generating schema: {e}")
        raise

if __name__ == "__main__":
    main()
