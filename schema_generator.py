#!/usr/bin/env python3
"""
Schema Generator - Creates an OpenAPI schema for environment variables.

This script processes the tracking data created by the Variable Tracker script,
extracts detailed information for each variable from the Markdown documentation,
and generates a complete OpenAPI schema with proper type definitions, descriptions,
and metadata.
"""

import re
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Regular expressions for extracting variable details
TYPE_PATTERN = r"- Type: `([^`]+)`"
DEFAULT_PATTERN = r"- Default: `?([^`\n]+)`?"
DEFAULT_PATTERN_EMPTY = r"- Default: Empty string \(''\), since `None` is set as default\."
PERSISTENCE_PATTERN = r"- Persistence: This environment variable is a `PersistentConfig` variable\."
DESCRIPTION_PATTERN = r"- Description: (.+?)(?=\n\n|\n-|$)"
ENUM_PATTERN = r"  - `([^`]*)`(.*?)(?=\n  -|\n\n|\n-|$)"
OPTIONS_PATTERN = r"- Options:([\s\S]*?)(?=\n\n|\n-|$)"

# Hardcoded default templates
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
</chat_history>"""
}

def load_tracking_data(file_path: str) -> Dict:
    """
    Load the tracking data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The tracking data as a dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading tracking data from {file_path}: {e}")
        raise

def load_markdown(file_path: str) -> List[str]:
    """
    Load the Markdown file as a list of lines.
    
    Args:
        file_path: Path to the Markdown file
        
    Returns:
        The Markdown content as a list of lines
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().split('\n')
    except Exception as e:
        logger.error(f"Error loading Markdown from {file_path}: {e}")
        raise

def load_existing_schema(file_path: str) -> Dict:
    """
    Load the existing OpenAPI schema from a JSON file or create a new one if it doesn't exist.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The schema as a dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Existing schema file {file_path} not found. Creating a new schema structure.")
        # Create a basic schema structure
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "OpenWebUI Configuration",
                "description": "Configuration schema for OpenWebUI environment variables",
                "version": "0.6.5"
            },
            "paths": {},
            "components": {
                "schemas": {
                    "OpenWebUIConfig": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        }
    except Exception as e:
        logger.error(f"Error loading schema from {file_path}: {e}")
        raise

def extract_options_from_section(section: str) -> tuple:
    """
    Extract options from a section and create enum values and descriptions.
    
    Args:
        section: The section text containing options
        
    Returns:
        A tuple containing (enum_values, options_description)
    """
    options_match = re.search(OPTIONS_PATTERN, section, re.DOTALL)
    if not options_match:
        return None, None
    
    options_text = options_match.group(1).strip()
    enum_values = []
    options_description = "Options:\n"
    
    # Find all enum patterns with their descriptions
    enum_matches = re.finditer(ENUM_PATTERN, options_text, re.DOTALL)
    for match in enum_matches:
        enum_value = match.group(1)
        enum_description = match.group(2).strip()
        
        # Add the enum value (even if it's empty)
        enum_values.append(enum_value)
        
        # Add the description to the options description
        if enum_value == "":
            options_description += f"  - Empty string - {enum_description}\n"
        else:
            options_description += f"  - `{enum_value}` - {enum_description}\n"
    
    return enum_values, options_description

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
    if type_match:
        raw_type = type_match.group(1).lower()
        if raw_type in ["str"]:
            details["type"] = "string"
        elif raw_type in ["bool", "boolean"]:
            details["type"] = "boolean"
        elif details["type"] == "integer":
            details["type"] = "integer"
        elif raw_type in ["float", "number"]:
            details["type"] = "number"
        else:
            details["type"] = "string"
    
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
            # Convert to appropriate type
            if details["type"] == "boolean":
                details["default"] = default_value.lower() == "true"
            elif details["type"] == "integer":
                try:
                    details["default"] = int(default_value)
                except ValueError:
                    details["default"] = default_value
            elif details["type"] == "number":
                try:
                    details["default"] = float(default_value)
                except ValueError:
                    details["default"] = default_value
            else:
                details["default"] = default_value
    
    # Extract description
    desc_match = re.search(DESCRIPTION_PATTERN, section, re.MULTILINE | re.DOTALL)
    if desc_match:
        details["description"] = desc_match.group(1).strip()
    
    # Check if it's a PersistentConfig variable
    if re.search(PERSISTENCE_PATTERN, section, re.MULTILINE):
        details["is_persistent_config"] = True
    
    # Extract enum values and options description
    enum_values, options_description = extract_options_from_section(section)
    if enum_values:
        details["enum"] = enum_values
    if options_description:
        details["options_description"] = options_description
        # Append options description to main description if available
        if details["description"] and options_description:
            details["description"] = f"{details['description']}\n\n{options_description}"
    
    # Check if the variable is sensitive (contains words like "key", "password", "secret", "token")
    sensitive_keywords = ["key", "password", "secret", "token", "credentials"]
    if var_name.lower() in sensitive_keywords or any(kw in var_name.lower() for kw in sensitive_keywords):
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
        "x-category": "TBD",  # Will be filled in from tracking data
        "x-display-order": 0  # Will be filled in from tracking data
    }
    
    # Add default value if present
    if details["default"] is not None:
        prop["default"] = details["default"]
    
    # Add references to default templates if applicable
    if details["references_var"] in DEFAULT_TEMPLATES:
        prop["x-references-var"] = details["references_var"]
        
        # Add helper property for .env file generation
        template_content = DEFAULT_TEMPLATES[details["references_var"]]
        escaped_content = template_content.replace('"', '\\"')
        prop["x-env-template"] = f'"{escaped_content}"'
    
    # Add enum values if present
    if details["enum"]:
        prop["enum"] = details["enum"]
    
    # Add sensitive flag if applicable
    if details["sensitive"]:
        prop["x-sensitive"] = True
    
    return prop

def update_schema(tracking_data: Dict, md_lines: List[str], existing_schema: Dict) -> Dict:
    """
    Update the OpenAPI schema with details for all variables.
    
    Args:
        tracking_data: The tracking data with variable information
        md_lines: The Markdown content as a list of lines
        existing_schema: The existing OpenAPI schema
        
    Returns:
        The updated schema as a dictionary
    """
    properties = existing_schema["components"]["schemas"]["OpenWebUIConfig"]["properties"]
    processed_count = 0
    added_count = 0
    updated_count = 0
    
    for var_name, var_info in tracking_data["variables"].items():
        if var_info["processed"] == "yes":
            processed_count += 1
            continue
        
        try:
            details = extract_variable_details(md_lines, var_name, var_info["line_number"] - 1)
            schema_prop = create_schema_property(details)
            
            # Set category and display order from tracking data
            schema_prop["x-category"] = var_info["category"]
            schema_prop["x-display-order"] = var_info["order"]
            
            # Add or update the property in the schema
            if var_name in properties:
                # Update existing property, preserving any fields not in our schema
                for key, value in schema_prop.items():
                    properties[var_name][key] = value
                updated_count += 1
            else:
                properties[var_name] = schema_prop
                added_count += 1
            
            # Mark as processed in tracking data
            var_info["processed"] = "yes"
            processed_count += 1
            
        except Exception as e:
            logger.error(f"Error processing variable {var_name}: {e}")
    
    # Update the tracking data with processed information
    tracking_data["processed_count"] = processed_count
    tracking_data["added_count"] = added_count
    tracking_data["updated_count"] = updated_count
    
    return existing_schema

def save_tracking_data(tracking_data: Dict, output_file: str) -> None:
    """
    Save the updated tracking data to a JSON file.
    
    Args:
        tracking_data: The updated tracking data
        output_file: Path to the output JSON file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tracking_data, f, indent=2)
        logger.info(f"Updated tracking data saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving tracking data to {output_file}: {e}")
        raise

def save_schema(schema: Dict, output_file: str, full_schema: bool = False) -> None:
    """
    Save the updated schema to a JSON file.
    
    Args:
        schema: The updated schema
        output_file: Path to the output JSON file
        full_schema: Whether to save the full schema or just the properties
    """
    try:
        if full_schema:
            # Save the full schema
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(schema, f, indent=2, ensure_ascii=False)
            logger.info(f"Full schema saved to {output_file}")
        else:
            # Extract only the OpenWebUIConfig properties to create a standalone output
            properties = schema["components"]["schemas"]["OpenWebUIConfig"]["properties"]
            
            # Create a properly formatted output
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(properties, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Schema properties saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving schema to {output_file}: {e}")
        raise

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate OpenAPI schema for environment variables')
    parser.add_argument('--tracking', '-t', default='variables_tracking.json', help='Path to the tracking JSON file (default: variables_tracking.json)')
    parser.add_argument('--markdown', '-m', default='env-configuration.md', help='Path to the Markdown file (default: env-configuration.md)')
    parser.add_argument('--schema', '-s', default='openwebui-config.json', help='Path to the existing schema JSON file (default: openwebui-config.json)')
    parser.add_argument('--output-schema', '-o', default='schema_properties.json', help='Path to the output properties JSON file (default: schema_properties.json)')
    parser.add_argument('--output-full-schema', '-f', default='full_schema.json', help='Path to the output full schema JSON file (default: full_schema.json)')
    parser.add_argument('--output-tracking', default=None, help='Path to the output tracking JSON file (default: same as tracking file)')
    parser.add_argument('--full-schema', action='store_true', help='Save the full schema instead of just the properties')
    args = parser.parse_args()
    
    try:
        tracking_data = load_tracking_data(args.tracking)
        md_lines = load_markdown(args.markdown)
        existing_schema = load_existing_schema(args.schema)
        
        updated_schema = update_schema(tracking_data, md_lines, existing_schema)
        
        # Save as properties or full schema based on flag
        save_schema(updated_schema, args.output_schema, args.full_schema)
        
        # Always save the full schema to the specified file
        save_schema(updated_schema, args.output_full_schema, True)
        
        if args.output_tracking:
            save_tracking_data(tracking_data, args.output_tracking)
        else:
            save_tracking_data(tracking_data, args.tracking)
        
        # Print summary
        print(f"Schema generation completed successfully!")
        print(f"Processed {tracking_data.get('processed_count', 0)}/{tracking_data['total_count']} variables")
        print(f"Added {tracking_data.get('added_count', 0)} new variables, updated {tracking_data.get('updated_count', 0)} existing variables")
        print(f"Properties saved to {args.output_schema}")
        print(f"Full schema saved to {args.output_full_schema}")
        
        # Calculate remaining variables
        remaining = tracking_data['total_count'] - tracking_data.get('processed_count', 0)
        if remaining > 0:
            print(f"Remaining variables to process: {remaining}")
        
    except Exception as e:
        logger.error(f"Error generating schema: {e}")
        raise

if __name__ == "__main__":
    main()
