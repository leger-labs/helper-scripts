#!/usr/bin/env python3
"""
Download and Prepare OpenWebUI Documentation

This script:
1. Downloads the latest OpenWebUI environment configuration documentation
2. Extracts DEFAULT_*_TEMPLATE variables to a separate JSON file
3. Splits the documentation into sections based on ## headers
4. Saves each section as a separate Markdown file

Usage:
  python download_and_prepare_docs.py --output-dir prepared_docs
"""

import re
import os
import json
import requests
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# URL of the OpenWebUI environment configuration documentation
DOCS_URL = "https://raw.githubusercontent.com/open-webui/docs/refs/heads/main/docs/getting-started/env-configuration.md"

def download_documentation() -> str:
    """
    Download the latest OpenWebUI documentation.
    
    Returns:
        The content of the environment configuration documentation
    """
    try:
        response = requests.get(DOCS_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except Exception as e:
        logger.error(f"Error downloading documentation: {e}")
        raise

def extract_templates(content: str) -> Tuple[str, Dict[str, str]]:
    """
    Extract DEFAULT_*_TEMPLATE variables and their content from the documentation.
    
    Args:
        content: The content of the documentation
        
    Returns:
        A tuple of (updated_content, templates_dict)
    """
    # Find all template definitions
    template_pattern = r"`(DEFAULT_[A-Z0-9_]+_TEMPLATE)`:\s*```\s*\n([\s\S]*?)\n```"
    template_matches = list(re.finditer(template_pattern, content))
    
    # Extract templates
    templates = {}
    for match in template_matches:
        var_name = match.group(1)
        template_content = match.group(2).strip()
        templates[var_name] = template_content
        logger.info(f"Extracted template for {var_name} ({len(template_content)} chars)")
    
    # Remove template definitions from the content
    updated_content = content
    for match in reversed(template_matches):  # Process in reverse to preserve positions
        start, end = match.span()
        updated_content = updated_content[:start] + updated_content[end:]
    
    return updated_content, templates

def split_into_sections(content: str) -> Dict[str, str]:
    """
    Split the documentation into sections based on ## headers.
    
    Args:
        content: The content of the documentation
        
    Returns:
        A dictionary mapping section titles to their content
    """
    # Find all level 2 headers (##)
    section_pattern = r"^##\s+(.+)$"
    section_matches = list(re.finditer(section_pattern, content, re.MULTILINE))
    
    sections = {}
    
    # Process each section
    for i, match in enumerate(section_matches):
        section_title = match.group(1).strip()
        start_pos = match.start()
        
        # Find the end of this section (start of next section or end of content)
        if i < len(section_matches) - 1:
            end_pos = section_matches[i + 1].start()
        else:
            end_pos = len(content)
        
        # Extract the section content
        section_content = content[start_pos:end_pos].strip()
        
        # Create a safe filename from the section title
        safe_title = re.sub(r'[^\w\s-]', '', section_title).strip().lower()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        
        sections[safe_title] = section_content
        logger.info(f"Extracted section: {section_title} ({len(section_content)} chars)")
    
    return sections

def save_templates(templates: Dict[str, str], output_dir: str) -> None:
    """
    Save the extracted templates to a JSON file.
    
    Args:
        templates: Dictionary mapping template names to content
        output_dir: Directory to save the output
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "default_templates.json")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(templates, f, indent=2)
        logger.info(f"Saved {len(templates)} templates to {output_path}")
    except Exception as e:
        logger.error(f"Error saving templates to {output_path}: {e}")
        raise

def save_sections(sections: Dict[str, str], output_dir: str) -> None:
    """
    Save each section as a separate Markdown file.
    
    Args:
        sections: Dictionary mapping section titles to content
        output_dir: Directory to save the output
    """
    sections_dir = os.path.join(output_dir, "sections")
    os.makedirs(sections_dir, exist_ok=True)
    
    for title, content in sections.items():
        output_path = os.path.join(sections_dir, f"{title}.md")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved section to {output_path}")
        except Exception as e:
            logger.error(f"Error saving section to {output_path}: {e}")
            raise

def save_full_content(content: str, output_dir: str) -> None:
    """
    Save the full (modified) content as a Markdown file.
    
    Args:
        content: The content to save
        output_dir: Directory to save the output
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "env-configuration-processed.md")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Saved processed content to {output_path}")
    except Exception as e:
        logger.error(f"Error saving content to {output_path}: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Download and prepare OpenWebUI documentation')
    parser.add_argument('--output-dir', '-o', default='prepared_docs', 
                        help='Directory to save the prepared files (default: prepared_docs)')
    args = parser.parse_args()
    
    try:
        # Download the documentation
        content = download_documentation()
        logger.info(f"Downloaded documentation ({len(content)} chars)")
        
        # Extract templates
        updated_content, templates = extract_templates(content)
        logger.info(f"Extracted {len(templates)} templates")
        
        # Split into sections
        sections = split_into_sections(updated_content)
        logger.info(f"Split documentation into {len(sections)} sections")
        
        # Save outputs
        save_templates(templates, args.output_dir)
        save_sections(sections, args.output_dir)
        save_full_content(updated_content, args.output_dir)
        
        print(f"\nDocumentation processing complete!")
        print(f"- Templates saved to {os.path.join(args.output_dir, 'default_templates.json')}")
        print(f"- Sections saved to {os.path.join(args.output_dir, 'sections')}")
        print(f"- Processed documentation saved to {os.path.join(args.output_dir, 'env-configuration-processed.md')}")
        print(f"\nNext steps:")
        print(f"1. Review the extracted sections in the '{os.path.join(args.output_dir, 'sections')}' directory")
        print(f"2. Use the LLM system prompt to generate relationship mappings for each section")
        print(f"3. Combine the mappings into a single JSON file")
        
    except Exception as e:
        logger.error(f"Error preparing documentation: {e}")
        raise

if __name__ == "__main__":
    main()
