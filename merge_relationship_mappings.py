#!/usr/bin/env python3
"""
Merge Relationship Mappings

This script merges relationship mappings from multiple JSON files (typically generated
by an LLM analyzing different sections of the OpenWebUI documentation) into a single
comprehensive mapping file.

Usage:
  python merge_relationship_mappings.py --input-dir mappings --output relationship_mappings.json
"""

import os
import json
import argparse
import logging
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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

def merge_mappings(mapping_files: List[str]) -> Dict:
    """
    Merge multiple relationship mapping files into a single mapping.
    
    Args:
        mapping_files: List of paths to mapping JSON files
        
    Returns:
        A dictionary with the merged mappings
    """
    # Initialize merged structure
    merged = {
        "provider_mappings": {},
        "boolean_selectors": {}
    }
    
    # Track sources of mappings for reporting
    sources = {}
    
    # Process each mapping file
    for file_path in mapping_files:
        try:
            mapping = load_json_file(file_path)
            file_name = os.path.basename(file_path)
            
            # Process provider mappings
            for selector, details in mapping.get("provider_mappings", {}).items():
                if selector in merged["provider_mappings"]:
                    logger.warning(f"Duplicate provider mapping for {selector} in {file_name}")
                    
                    # Merge enum values
                    existing_enums = set(merged["provider_mappings"][selector].get("enum_values", []))
                    new_enums = set(details.get("enum_values", []))
                    merged_enums = sorted(list(existing_enums.union(new_enums)))
                    merged["provider_mappings"][selector]["enum_values"] = merged_enums
                    
                    # Merge provider fields
                    for provider, fields in details.get("provider_fields", {}).items():
                        if provider in merged["provider_mappings"][selector]["provider_fields"]:
                            # Add any new fields
                            existing_fields = set(merged["provider_mappings"][selector]["provider_fields"][provider])
                            new_fields = set(fields)
                            merged_fields = sorted(list(existing_fields.union(new_fields)))
                            merged["provider_mappings"][selector]["provider_fields"][provider] = merged_fields
                        else:
                            # Add new provider
                            merged["provider_mappings"][selector]["provider_fields"][provider] = fields
                    
                    # Update sources
                    sources.setdefault(selector, []).append(file_name)
                else:
                    # Add new provider mapping
                    merged["provider_mappings"][selector] = details
                    sources[selector] = [file_name]
            
            # Process boolean selectors
            for selector, details in mapping.get("boolean_selectors", {}).items():
                if selector in merged["boolean_selectors"]:
                    logger.warning(f"Duplicate boolean selector for {selector} in {file_name}")
                    
                    # Merge provider fields (dependent variables)
                    existing_fields = set(merged["boolean_selectors"][selector].get("provider_fields", []))
                    new_fields = set(details.get("provider_fields", []))
                    merged_fields = sorted(list(existing_fields.union(new_fields)))
                    merged["boolean_selectors"][selector]["provider_fields"] = merged_fields
                    
                    # Update sources
                    sources.setdefault(selector, []).append(file_name)
                else:
                    # Add new boolean selector
                    merged["boolean_selectors"][selector] = details
                    sources[selector] = [file_name]
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
    
    # Sort all lists for consistency
    for selector, details in merged["provider_mappings"].items():
        if "enum_values" in details:
            details["enum_values"] = sorted(details["enum_values"])
        for provider, fields in details.get("provider_fields", {}).items():
            details["provider_fields"][provider] = sorted(fields)
    
    for selector, details in merged["boolean_selectors"].items():
        if "provider_fields" in details:
            details["provider_fields"] = sorted(details["provider_fields"])
    
    # Log merge results
    logger.info(f"Merged {len(mapping_files)} mapping files")
    logger.info(f"Resulting in {len(merged['provider_mappings'])} provider mappings and {len(merged['boolean_selectors'])} boolean selectors")
    
    # Add source tracking metadata
    merged["_metadata"] = {
        "sources": sources,
        "file_count": len(mapping_files)
    }
    
    return merged

def find_mapping_files(input_dir: str) -> List[str]:
    """
    Find all JSON files in the input directory.
    
    Args:
        input_dir: Path to the directory containing mapping files
        
    Returns:
        A list of paths to JSON files
    """
    json_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def main():
    parser = argparse.ArgumentParser(description='Merge relationship mappings from multiple JSON files')
    parser.add_argument('--input-dir', '-i', required=True, 
                        help='Directory containing relationship mapping JSON files')
    parser.add_argument('--output', '-o', default='relationship_mappings.json', 
                        help='Path to the output merged mappings JSON file')
    args = parser.parse_args()
    
    try:
        # Find all JSON files in the input directory
        mapping_files = find_mapping_files(args.input_dir)
        if not mapping_files:
            logger.error(f"No JSON files found in {args.input_dir}")
            return
        
        logger.info(f"Found {len(mapping_files)} JSON files to merge")
        
        # Merge the mappings
        merged = merge_mappings(mapping_files)
        
        # Save the merged mappings
        save_json_file(merged, args.output)
        
        # Print summary
        print(f"\nMerge complete!")
        print(f"- Merged {len(mapping_files)} mapping files")
        print(f"- Saved result to {args.output}")
        print(f"- Resulting in:")
        print(f"  * {len(merged['provider_mappings'])} provider mappings")
        print(f"  * {len(merged['boolean_selectors'])} boolean selectors")
        
        # Print list of provider mappings
        print("\nProvider Mappings:")
        for selector in sorted(merged["provider_mappings"].keys()):
            enum_count = len(merged["provider_mappings"][selector].get("enum_values", []))
            provider_count = len(merged["provider_mappings"][selector].get("provider_fields", {}))
            field_count = sum(len(fields) for fields in merged["provider_mappings"][selector].get("provider_fields", {}).values())
            print(f"  - {selector}: {enum_count} options, {provider_count} providers, {field_count} dependent fields")
        
        # Print list of boolean selectors
        print("\nBoolean Selectors:")
        for selector in sorted(merged["boolean_selectors"].keys()):
            field_count = len(merged["boolean_selectors"][selector].get("provider_fields", []))
            print(f"  - {selector}: {field_count} dependent fields")
        
    except Exception as e:
        logger.error(f"Error merging mappings: {e}")
        raise

if __name__ == "__main__":
    main()
