import json
import sys
import os
from typing import Dict, Set, List, Any
import argparse

def load_json_file(file_path: str) -> Dict:
    """Load a JSON file and return its contents."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        sys.exit(1)

def save_json_file(data: Dict, file_path: str) -> None:
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        sys.exit(1)

def extract_variables_from_classifications(classifications: Dict) -> Set[str]:
    """Extract variable names from the classifications file."""
    return set(classifications.keys())

def extract_variables_from_openapi(openapi_spec: Dict) -> Set[str]:
    """Extract variable names from the OpenAPI spec."""
    try:
        properties = openapi_spec["components"]["schemas"]["OpenWebUIConfig"]["properties"]
        return set(properties.keys())
    except KeyError:
        print("Error: OpenAPI spec doesn't have the expected structure")
        sys.exit(1)

def find_new_variables(openapi_vars: Set[str], classification_vars: Set[str]) -> List[str]:
    """Find variables in the OpenAPI spec that aren't in the classifications."""
    return sorted(list(openapi_vars - classification_vars))

def find_removed_variables(openapi_vars: Set[str], classification_vars: Set[str]) -> List[str]:
    """Find variables in the classifications that aren't in the OpenAPI spec."""
    return sorted(list(classification_vars - openapi_vars))

def get_variable_details(openapi_spec: Dict, var_name: str) -> Dict[str, Any]:
    """Get details for a specific variable from the OpenAPI spec."""
    try:
        return openapi_spec["components"]["schemas"]["OpenWebUIConfig"]["properties"][var_name]
    except KeyError:
        return {}

def create_template_for_new_vars(new_vars: List[str], openapi_spec: Dict) -> Dict:
    """Create a template for new variables."""
    template = {}
    for var in new_vars:
        details = get_variable_details(openapi_spec, var)
        default_value = details.get("default", "")
        template[var] = {
            "visibility": "exposed",  # Default to exposed, adjust as needed
            "default_handling": "preloaded",  # Default to preloaded, adjust as needed
            "default_value": str(default_value) if default_value is not None else "",
            "rationale": ""  # To be filled manually
        }
    return template

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Compare OpenAPI spec and classifications files')
    parser.add_argument('--classifications', default='final_leger_openwebui_var_classifications.json', 
                        help='Path to the classifications JSON file')
    parser.add_argument('--openapi', default='test_output.json', 
                        help='Path to the OpenAPI spec JSON file')
    parser.add_argument('--output', default='new_variables_template.json', 
                        help='Path to save the new variables template')
    parser.add_argument('--report', default='comparison_report.txt', 
                        help='Path to save the comparison report')
    args = parser.parse_args()
    
    # Load the JSON files
    classifications = load_json_file(args.classifications)
    openapi_spec = load_json_file(args.openapi)
    
    # Extract variable names
    classification_vars = extract_variables_from_classifications(classifications["variable_classifications"])
    openapi_vars = extract_variables_from_openapi(openapi_spec)
    
    # Find new and removed variables
    new_vars = find_new_variables(openapi_vars, classification_vars)
    removed_vars = find_removed_variables(openapi_vars, classification_vars)
    
    # Generate report
    with open(args.report, 'w') as report_file:
        report_file.write(f"Found {len(new_vars)} new variables that need manual annotation:\n")
        for i, var in enumerate(new_vars, 1):
            details = get_variable_details(openapi_spec, var)
            description = details.get("description", "No description available")
            default = details.get("default", "No default value")
            report_file.write(f"{i}. {var}\n")
            report_file.write(f"   Description: {description}\n")
            report_file.write(f"   Default value: {default}\n\n")
        
        if removed_vars:
            report_file.write(f"\nFound {len(removed_vars)} variables in classifications that aren't in the OpenAPI spec:\n")
            for var in removed_vars:
                report_file.write(f"- {var}\n")
        else:
            report_file.write("\nNo variables found in classifications that aren't in the OpenAPI spec.\n")
    
    # Print summary to console
    print(f"Found {len(new_vars)} new variables that need manual annotation.")
    if removed_vars:
        print(f"Found {len(removed_vars)} variables in classifications that aren't in the OpenAPI spec.")
    print(f"Detailed report saved to {args.report}")
    
    # Generate and save template for new variables
    if new_vars:
        template = create_template_for_new_vars(new_vars, openapi_spec)
        save_json_file(template, args.output)
        print(f"New variables template saved to {args.output}")

if __name__ == "__main__":
    main()
