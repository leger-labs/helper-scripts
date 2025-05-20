#!/usr/bin/env python3
"""
Unified OpenWebUI Schema Generator

This script generates a comprehensive OpenAPI schema for OpenWebUI environment variables by:
1. Extracting schema properties from the documentation
2. Incorporating default templates from a JSON file
3. Adding relationship mappings from a JSON file
4. Comparing with a manual classification JSON to identify new variables

Usage:
  python unified_schema_generator.py \
    --input env-configuration-processed.md \
    --templates default_templates.json \
    --relationships relationship_mappings.json \
    --classifications final_leger_openwebui_var_classifications.json \
    --output openwebui-config-schema.json
"""

import re
import json
import os
import argparse
import logging
from typing import Dict, List, Optional, Tuple, Set, Any

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

def load_json_file(file_path: str) -> Dict:
    """
    Load a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The loaded JSON content as a dictionary
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {e}")
        raise

def save_json_file(data: Dict, output_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: The data to save
        output_path: Path to save the JSON file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved data to {output_path}")
    except Exception as e:
        logger.error(f"Error saving data to {output_path}: {e}")
        raise

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
    current_subcategory = None
    categories = {}
    variable_order = 1
    
    # Process each line
    for i, line in enumerate(lines):
        # Check for category (section) headers
        category_match = re.match(r"^##\s+(.+)$", line)
        if category_match:
            current_category = category_match.group(1).strip()
            current_subcategory = None
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
                current_subcategory = full_category
            continue
        
        # Check for variable headers
        var_match = re.match(VARIABLE_PATTERN, line)
        if var_match:
            var_name = var_match.group(1)
            if var_name not in variable_info:
                # Use subcategory if available, otherwise use main category
                effective_category = current_subcategory if current_subcategory else current_category
                
                variable_info[var_name] = {
                    "line_number": i,
                    "category": effective_category,
                    "order": variable_order
                }
                if effective_category:
                    categories[effective_category] = categories.get(effective_category, []) + [var_name]
                variable_order += 1
    
    # Report statistics
    logger.info(f"Found {len(variable_info)} variables across {len(categories)} categories")
    
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

    if var_name == "DEFAULT_USER_ROLE":
        enum_values = ["pending", "user", "admin"]
        options_description = "Options:\n  - `pending` - New users are pending until their accounts are manually activated by an admin.\n  - `user` - New users are automatically activated with regular user permissions.\n  - `admin` - New users are automatically activated with administrator permissions.\n"
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
    if var_name == "WEB_LOADER_ENGINE" and not any(v == "" for v in enum_values):
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
    
    # Special case for WEBUI_SESSION_COOKIE_SAME_SITE and WEBUI_AUTH_COOKIE_SAME_SITE
    if var_name in ["WEBUI_SESSION_COOKIE_SAME_SITE", "WEBUI_AUTH_COOKIE_SAME_SITE"] and not enum_values:
        enum_values = ["lax", "strict", "none"]
        options_description = "Options:\n"
        options_description += "  - `lax` - Sets the `SameSite` attribute to lax, allowing session cookies to be sent with requests initiated by third-party websites.\n"
        options_description += "  - `strict` - Sets the `SameSite` attribute to strict, blocking session cookies from being sent with requests initiated by third-party websites.\n"
        options_description += "  - `none` - Sets the `SameSite` attribute to none, allowing session cookies to be sent with requests initiated by third-party websites, but only over HTTPS.\n"
    
    # Special case for RAG_TEXT_SPLITTER
    if var_name == "RAG_TEXT_SPLITTER" and not enum_values:
        enum_values = ["character", "token"]
        options_description = "Options:\n"
        options_description += "  - `character` - Splits text by character count.\n"
        options_description += "  - `token` - Splits text by token count.\n"
    
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
    else:
        # Extract regular default value
        default_match = re.search(DEFAULT_PATTERN, section, re.MULTILINE)
        empty_default_match = re.search(DEFAULT_PATTERN_EMPTY, section, re.MULTILINE)
        
        if empty_default_match:
            details["default"] = ""
        elif default_match:
            default_value = default_match.group(1).strip()
            
            # Handle special cases
            if default_value == "None":
                details["default"] = None
            # Convert default value to the appropriate type
            elif details["type"] == "boolean":
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
            elif details["type"] == "array" and default_value == "[]":
                details["default"] = []
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
    if details.get("references_var"):
        prop["x-references-var"] = details["references_var"]
    
    # Add enum values if present
    if details.get("enum"):
        prop["enum"] = details["enum"]
    
    # Add sensitive flag if applicable
    if details["sensitive"]:
        prop["x-sensitive"] = True
    
    return prop

def apply_templates(schema_props: Dict, templates: Dict) -> Dict:
    """
    Apply default templates to schema properties.
    
    Args:
        schema_props: The schema properties
        templates: The default templates
        
    Returns:
        The updated schema properties
    """
    # Create a copy to avoid modifying the original
    schema = schema_props.copy()
    templates_applied = 0
    
    # Check each property for a reference to a template
    for var_name, prop in schema.items():
        if "x-references-var" in prop:
            template_name = prop["x-references-var"]
            if template_name in templates:
                # Add the template content to the property
                prop["x-default-template"] = templates[template_name]
                templates_applied += 1
                logger.info(f"Applied template {template_name} to {var_name}")
            else:
                logger.warning(f"Template {template_name} referenced by {var_name} not found")
    
    logger.info(f"Applied {templates_applied} default templates to schema properties")
    return schema

def apply_relationships(schema_props: Dict, relationships: Dict) -> Dict:
    """
    Apply relationship mappings to schema properties.
    
    Args:
        schema_props: The schema properties
        relationships: The relationship mappings
        
    Returns:
        The updated schema properties
    """
    # Create a copy to avoid modifying the original
    schema = schema_props.copy()
    relationships_applied = 0
    
    # Track which variables are processed
    processed_variables = set()
    
    # Apply provider mappings
    provider_mappings = relationships.get("provider_mappings", {})
    for selector_var, mapping in provider_mappings.items():
        if selector_var in schema:
            processed_variables.add(selector_var)
            
            # Add enum values if available
            if "enum_values" in mapping and "enum" not in schema[selector_var]:
                schema[selector_var]["enum"] = mapping["enum_values"]
            
            # Add x-provider-fields extension
            if "provider_fields" in mapping:
                schema[selector_var]["x-provider-fields"] = mapping["provider_fields"]
                
                # Add x-depends-on to all dependent fields
                for provider, fields in mapping["provider_fields"].items():
                    for field in fields:
                        if field in schema:
                            processed_variables.add(field)
                            schema[field]["x-depends-on"] = {selector_var: provider}
                            relationships_applied += 1
        else:
            logger.warning(f"Selector variable {selector_var} defined in relationships but not found in schema")
    
    # Apply boolean selectors
    boolean_selectors = relationships.get("boolean_selectors", {})
    for selector_var, mapping in boolean_selectors.items():
        if selector_var in schema:
            processed_variables.add(selector_var)
            
            # Add x-provider-fields extension
            if "provider_fields" in mapping:
                schema[selector_var]["x-provider-fields"] = mapping["provider_fields"]
                
                # Add x-depends-on to all dependent fields
                for field in mapping["provider_fields"]:
                    if field in schema:
                        processed_variables.add(field)
                        schema[field]["x-depends-on"] = {selector_var: mapping.get("value", True)}
                        relationships_applied += 1
        else:
            logger.warning(f"Boolean selector {selector_var} defined in relationships but not found in schema")
    
    logger.info(f"Applied {relationships_applied} relationships to schema properties")
    return schema

def compare_with_classifications(schema_props: Dict, classifications: Dict) -> Tuple[Dict, List[str]]:
    """
    Compare schema properties with manual classifications to identify new variables.
    
    Args:
        schema_props: The schema properties
        classifications: The manual classifications
        
    Returns:
        A tuple of (updated schema properties, list of new variables)
    """
    # Create a copy to avoid modifying the original
    schema = schema_props.copy()
    
    # Extract the variable classifications
    var_classifications = classifications.get("variable_classifications", {})
    
    # Find variables that are in the schema but not in the classifications
    new_variables = []
    for var_name in schema:
        if var_name not in var_classifications:
            new_variables.append(var_name)
            logger.info(f"New variable found: {var_name}")
    
    # Apply classifications to schema properties
    for var_name, prop in schema.items():
        if var_name in var_classifications:
            var_class = var_classifications[var_name]
            
            # Add visibility
            visibility = var_class.get("visibility")
            if visibility:
                prop["x-visibility"] = visibility
            
            # Add default handling
            default_handling = var_class.get("default_handling")
            if default_handling:
                prop["x-default-handling"] = default_handling
            
            # Add default value if not already set
            default_value = var_class.get("default_value")
            if default_value and "default" not in prop:
                # Convert the default value to the appropriate type
                if prop.get("type") == "boolean":
                    if default_value.lower() in ["true", "yes", "1"]:
                        prop["default"] = True
                    elif default_value.lower() in ["false", "no", "0"]:
                        prop["default"] = False
                    else:
                        prop["default"] = default_value
                elif prop.get("type") == "integer":
                    try:
                        prop["default"] = int(default_value)
                    except ValueError:
                        prop["default"] = default_value
                elif prop.get("type") == "number":
                    try:
                        prop["default"] = float(default_value)
                    except ValueError:
                        prop["default"] = default_value
                else:
                    prop["default"] = default_value
            
            # Add rationale if present
            rationale = var_class.get("rationale")
            if rationale:
                prop["x-rationale"] = rationale
    
    logger.info(f"Found {len(new_variables)} new variables that need manual classification")
    return schema, new_variables

def create_template_for_new_vars(new_vars: List[str], schema_props: Dict) -> Dict:
    """
    Create a template for new variables that need manual classification.
    
    Args:
        new_vars: List of new variable names
        schema_props: The schema properties
        
    Returns:
        A dictionary with templates for the new variables
    """
    template = {}
    for var_name in new_vars:
        if var_name in schema_props:
            prop = schema_props[var_name]
            
            # Extract default value
            default_value = prop.get("default", "")
            if default_value is None:
                default_value = ""
            elif isinstance(default_value, (bool, int, float)):
                default_value = str(default_value)
            
            # Create template entry
            template[var_name] = {
                "visibility": "exposed",  # Default to exposed, adjust as needed
                "default_handling": "preloaded",  # Default to preloaded, adjust as needed
                "default_value": default_value,
                "rationale": ""  # To be filled manually
            }
    
    return template

def append_new_vars_to_classifications(new_vars: List[str], schema_props: Dict, 
                                       classifications: Dict, output_path: str) -> None:
    """
    Append templates for new variables to the classifications file.
    
    Args:
        new_vars: List of new variable names
        schema_props: The schema properties
        classifications: The current classifications
        output_path: Path to save the updated classifications
    """
    if not new_vars:
        logger.info("No new variables to append to classifications")
        return
    
    # Create template for new variables
    new_vars_template = create_template_for_new_vars(new_vars, schema_props)
    
    # Create a copy of the classifications
    updated_classifications = classifications.copy()
    
    # Add new variables to the copy
    var_classifications = updated_classifications.get("variable_classifications", {})
    for var_name, template in new_vars_template.items():
        var_classifications[var_name] = template
    
    # Update the classifications
    updated_classifications["variable_classifications"] = var_classifications
    
    # Save the updated classifications
    save_json_file(updated_classifications, output_path)
    logger.info(f"Appended {len(new_vars)} new variables to classifications in {output_path}")

def create_full_schema(properties: Dict) -> Dict:
    """
    Create a full OpenAPI schema with the provided properties.
    
    Args:
        properties: The schema properties
        
    Returns:
        A complete OpenAPI schema
    """
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "OpenWebUI Configuration",
            "description": "Configuration schema for OpenWebUI environment variables",
            "version": "0.7.0"
        },
        "paths": {},
        "components": {
            "schemas": {
                "OpenWebUIConfig": {
                    "type": "object",
                    "properties": properties,
                    "required": []
                }
            }
        }
    }

def generate_schema(markdown_path: str, templates_path: str, 
                    relationships_path: str, classifications_path: str, 
                    output_path: str, append_new_vars: bool = True,
                    properties_only: bool = False) -> None:
    """
    Generate a complete OpenAPI schema for OpenWebUI environment variables.
    
    Args:
        markdown_path: Path to the Markdown documentation
        templates_path: Path to the default templates JSON file
        relationships_path: Path to the relationship mappings JSON file
        classifications_path: Path to the manual classifications JSON file
        output_path: Path to the output schema JSON file
        append_new_vars: Whether to append new variables to the classifications file
        properties_only: Whether to output only the properties section of the schema
    """
    # Step 1: Parse the Markdown documentation
    variable_info, markdown_lines = parse_markdown(markdown_path)
    
    # Step 2: Extract details for each variable
    schema_properties = {}
    for var_name, var_info in variable_info.items():
        try:
            # Skip DEFAULT_*_TEMPLATE variables (they're handled separately)
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
    
    # Step 3: Load external data
    templates = load_json_file(templates_path)
    relationships = load_json_file(relationships_path)
    classifications = load_json_file(classifications_path)
    
    # Step 4: Apply templates to schema properties
    schema = apply_templates(schema_properties, templates)
    
    # Step 5: Apply relationships to schema properties
    schema = apply_relationships(schema, relationships)
    
    # Step 6: Compare with classifications and identify new variables
    schema, new_variables = compare_with_classifications(schema, classifications)
    
    # Step 7: Append new variables to classifications if requested
    if append_new_vars and new_variables:
        new_classifications_path = f"{os.path.splitext(classifications_path)[0]}_with_new_vars.json"
        append_new_vars_to_classifications(new_variables, schema_properties, 
                                          classifications, new_classifications_path)
    
    # Step 8: Save the final schema
    if properties_only:
        save_json_file(schema, output_path)
        logger.info(f"Saved schema properties to {output_path}")
    else:
        full_schema = create_full_schema(schema)
        save_json_file(full_schema, output_path)
        logger.info(f"Saved full schema to {output_path}")
    
    # Report statistics
    print(f"\nSchema generation complete!")
    print(f"- Processed {len(schema)} variables")
    print(f"- Applied {sum(1 for p in schema.values() if 'x-default-template' in p)} default templates")
    print(f"- Applied {sum(1 for p in schema.values() if 'x-depends-on' in p)} dependency relationships")
    print(f"- Applied {sum(1 for p in schema.values() if 'x-visibility' in p)} manual classifications")
    
    if new_variables:
        print(f"\nFound {len(new_variables)} new variables that need manual classification:")
        for var_name in sorted(new_variables):
            print(f"  - {var_name}")
        if append_new_vars:
            print(f"\nTemplate for new variables saved to {new_classifications_path}")
            print(f"Please review and update the classification for these variables.")

def main():
    parser = argparse.ArgumentParser(description='Generate an OpenAPI schema for OpenWebUI environment variables')
    parser.add_argument('--input', '-i', default='prepared_docs/env-configuration-processed.md', 
                        help='Path to the input Markdown file')
    parser.add_argument('--templates', '-t', default='prepared_docs/default_templates.json', 
                        help='Path to the default templates JSON file')
    parser.add_argument('--relationships', '-r', default='relationship_mappings.json', 
                        help='Path to the relationship mappings JSON file')
    parser.add_argument('--classifications', '-c', default='final_leger_openwebui_var_classifications.json', 
                        help='Path to the manual classifications JSON file')
    parser.add_argument('--output', '-o', default='openwebui-config-schema.json', 
                        help='Path to the output schema JSON file')
    parser.add_argument('--no-append', action='store_true',
                        help='Do not append new variables to the classifications file')
    parser.add_argument('--properties-only', '-p', action='store_true',
                        help='Output only the properties section of the schema')
    args = parser.parse_args()
    
    try:
        generate_schema(
            markdown_path=args.input,
            templates_path=args.templates,
            relationships_path=args.relationships,
            classifications_path=args.classifications,
            output_path=args.output,
            append_new_vars=not args.no_append,
            properties_only=args.properties_only
        )
    except Exception as e:
        logger.error(f"Error generating schema: {e}")
        raise

if __name__ == "__main__":
    main()
