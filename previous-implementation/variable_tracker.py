#!/usr/bin/env python3
"""
Variable Tracker - Scans Markdown documentation to identify environment variables.

This script parses a Markdown file containing documentation about environment variables,
extracts variable names, and creates a tracking dictionary with metadata for each variable.
The result is output as a JSON file for further processing.
"""

import re
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Regular expressions for identifying environment variables
VAR_PATTERN = r"^#### `([A-Z][A-Z0-9_]+)`$"
TYPE_PATTERN = r"^- Type: `([^`]+)`"
DEFAULT_PATTERN = r"^- Default: `?([^`\n]+)`?"
DEFAULT_PATTERN_EMPTY = r"^- Default: Empty string \('\'\), since `None` is set as default\."
PERSISTENCE_PATTERN = r"^- Persistence: This environment variable is a `PersistentConfig` variable\."
DESCRIPTION_PATTERN = r"^- Description: (.+)$"
ENUM_PATTERN = r"^  - `([^`]*)`(.*?)(?=\n  -|\n\n|\n-|$)"

def extract_category(line: str) -> Optional[str]:
    """
    Extract the category name from a heading line.
    
    Args:
        line: The line to check for a heading
        
    Returns:
        The category name if the line is a heading, None otherwise
    """
    # Match ## headings (level 2 headings)
    match = re.match(r"^## (.+)$", line)
    if match:
        return match.group(1).strip()
    return None

def is_variable_header(line: str) -> Optional[str]:
    """
    Check if a line contains a variable definition header.
    
    Args:
        line: The line to check
        
    Returns:
        The variable name if the line is a variable header, None otherwise
    """
    match = re.match(VAR_PATTERN, line)
    if match:
        return match.group(1)
    return None

def parse_markdown(file_path: str) -> Dict:
    """
    Parse the Markdown file and extract environment variables with their metadata.
    
    Args:
        file_path: Path to the Markdown file
        
    Returns:
        A dictionary with variable tracking information
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise
    
    lines = content.split('\n')
    tracked_vars = {}
    comment_blocks = []
    current_category = None
    current_comment_block = []
    in_comment_block = False
    current_order = 1
    
    # First pass: get all the variable names, categories, and extract comment blocks
    for i, line in enumerate(lines):
        # Check for comment blocks (:::info, :::note, etc.)
        if line.strip().startswith(':::'):
            if not in_comment_block:
                in_comment_block = True
                current_comment_block = [line]
            else:
                current_comment_block.append(line)
                in_comment_block = False
                comment_blocks.append('\n'.join(current_comment_block))
                current_comment_block = []
        elif in_comment_block:
            current_comment_block.append(line)
            
        # Check for category headings
        category = extract_category(line)
        if category:
            current_category = category
            continue
        
        # Check for variable headers (skip DEFAULT_*_TEMPLATE variables)
        var_name = is_variable_header(line)
        if var_name and not (var_name.startswith("DEFAULT_") and var_name.endswith("_TEMPLATE")):
            if var_name in tracked_vars:
                logger.warning(f"Duplicate variable found: {var_name}")
                continue
                
            tracked_vars[var_name] = {
                "order": current_order,
                "category": current_category,
                "processed": "no",
                "line_number": i + 1  # 1-based line number
            }
            current_order += 1
    
    # Save comment blocks to a separate file
    if comment_blocks:
        try:
            with open('comments.md', 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(comment_blocks))
            logger.info(f"Comment blocks saved to comments.md")
        except Exception as e:
            logger.error(f"Error saving comment blocks: {e}")
    
    return {
        "variables": tracked_vars,
        "total_count": len(tracked_vars),
        "categories": {cat: len([v for v in tracked_vars.values() if v["category"] == cat]) 
                     for cat in set(v["category"] for v in tracked_vars.values())}
    }

def save_tracking_data(tracking_data: Dict, output_file: str) -> None:
    """
    Save the tracking data to a JSON file.
    
    Args:
        tracking_data: The dictionary with tracking information
        output_file: Path to the output JSON file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tracking_data, f, indent=2)
        logger.info(f"Tracking data saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving tracking data to {output_file}: {e}")
        raise

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Track environment variables in Markdown documentation')
    parser.add_argument('--input', '-i', default='env-configuration.md', help='Path to the input Markdown file (default: env-configuration.md)')
    parser.add_argument('--output', '-o', default='variables_tracking.json', help='Path to the output JSON file (default: variables_tracking.json)')
    args = parser.parse_args()
    
    try:
        tracking_data = parse_markdown(args.input)
        save_tracking_data(tracking_data, args.output)
        
        # Print summary
        print(f"Variable tracking completed successfully!")
        print(f"Found {tracking_data['total_count']} environment variables across {len(tracking_data['categories'])} categories")
        top_categories = sorted(tracking_data['categories'].items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"Top categories: " + ", ".join([f"{cat} ({count})" for cat, count in top_categories]))
    except Exception as e:
        logger.error(f"Error processing Markdown file: {e}")
        raise

if __name__ == "__main__":
    main()
