#!/usr/bin/env python3
"""
provider_enhancer.py - Enhances OpenWebUI schema with provider relationships

This script adds provider relationship information to the OpenWebUI configuration schema
by identifying selector variables and their dependent fields, then adding appropriate
extensions to make these relationships explicit in the schema.

For each multi-provider feature, it:
1. Identifies the "selector" variable that determines which provider is used
2. Adds proper enumerations to these selector variables if not already present
3. Adds an extension called x-provider-fields to each selector variable that maps
   provider options to their specific environment variables
4. Adds an extension called x-depends-on to all provider-specific variables to
   reference their selector variable and required value

Usage:
  python provider_enhancer.py input_schema.json output_schema.json
"""

import json
import sys
import os
from copy import deepcopy

def load_schema(file_path):
    """Load the schema from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_schema(schema, output_file):
    """Save the modified schema to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(schema, f, indent=2)
    print(f"Enhanced schema saved to {output_file}")

def enhance_schema(schema):
    """Add provider-related extensions to the schema."""
    properties = schema['components']['schemas']['OpenWebUIConfig']['properties']
    
    # Define the provider mappings: selector variables and their dependent fields
    # This is where we define all the relationships between selectors and their provider-specific fields
    provider_mappings = {
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
                    "S3_ADDRESSING_STYLE", "S3_USE_ACCELERATE_ENDPOINT"
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
                "milvus": ["MILVUS_URI", "MILVUS_DB", "MILVUS_TOKEN"],
                "opensearch": [
                    "OPENSEARCH_CERT_VERIFY", "OPENSEARCH_PASSWORD",
                    "OPENSEARCH_SSL", "OPENSEARCH_URI", "OPENSEARCH_USERNAME"
                ],
                "pgvector": ["PGVECTOR_DB_URL", "PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH"],
                "qdrant": [
                    "QDRANT_API_KEY", "QDRANT_URI", "QDRANT_ON_DISK",
                    "QDRANT_PREFER_GRPC", "QDRANT_GRPC_PORT"
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
                "docling": ["DOCLING_SERVER_URL"],
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
    
    # Additional auth-related selectors with boolean toggles
    boolean_selectors = {
        "ENABLE_OAUTH_SIGNUP": {
            "value": True,
            "provider_fields": [
                "OAUTH_MERGE_ACCOUNTS_BY_EMAIL", "WEBUI_AUTH_TRUSTED_EMAIL_HEADER",
                "WEBUI_AUTH_TRUSTED_NAME_HEADER", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET",
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
                "LDAP_CA_CERT_FILE", "LDAP_CIPHERS"
            ]
        }
    }
    
    # Add x-provider-fields extension to selector variables and ensure enums exist
    for selector_var, mapping in provider_mappings.items():
        if selector_var in properties:
            # Add enum values if they don't exist already
            if "enum" not in properties[selector_var]:
                properties[selector_var]["enum"] = mapping["enum_values"]
            
            # Add x-provider-fields extension
            properties[selector_var]["x-provider-fields"] = mapping["provider_fields"]
            
            # Add x-depends-on to all dependent fields
            for provider, fields in mapping["provider_fields"].items():
                for field in fields:
                    if field in properties:
                        properties[field]["x-depends-on"] = {selector_var: provider}
    
    # Handle boolean selectors (like ENABLE_OAUTH_SIGNUP, ENABLE_LDAP)
    for selector_var, mapping in boolean_selectors.items():
        if selector_var in properties:
            # Add x-provider-fields extension
            properties[selector_var]["x-provider-fields"] = mapping["provider_fields"]
            
            # Add x-depends-on to all dependent fields
            for field in mapping["provider_fields"]:
                if field in properties:
                    properties[field]["x-depends-on"] = {selector_var: mapping["value"]}
    
    return schema

def main():
    if len(sys.argv) < 2:
        print("Usage: python provider_enhancer.py <schema_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "enhanced_" + os.path.basename(input_file)
    
    schema = load_schema(input_file)
    enhanced_schema = enhance_schema(schema)
    save_schema(enhanced_schema, output_file)

if __name__ == "__main__":
    main()
