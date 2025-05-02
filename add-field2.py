
import json
import re
import sys

# Ensure you specify the input files in the command line
if len(sys.argv) < 3:
    print("Usage: python add-field.py <variables-json> <classification-json>")
    sys.exit(1)

# Get the input files from command line arguments
variables_json_file = sys.argv[1]  # variables.json (with order)
classification_json_file = sys.argv[2]  # Classification JSON

# Step 1: Read the existing variables.json
with open(variables_json_file, "r", encoding="utf-8") as f:
    variables_data = json.load(f)

# Step 2: Read the prefilled classification JSON
with open(classification_json_file, "r", encoding="utf-8") as f:
    classification_data = json.load(f)

# Step 3: Merge variables_data and classification_data to add the x_leger_default field
for var_name, var_info in variables_data.items():
    if var_name in classification_data['variable_classifications']:
        # Adding x_leger_default to the classification data
        classification_data['variable_classifications'][var_name]["x_leger_default"] = ""

# Write the merged data to a final classification file
final_classification_file = "final_classification.json"
with open(final_classification_file, "w", encoding="utf-8") as f:
    json.dump(classification_data, f, indent=2)

print(f"Updated classifications written to '{final_classification_file}'")

# Read the original HTML (class.html or any file passed as argument)
html_file = "class.html"
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

# Step 4: Add a new column header for "x-leger-default"
html = re.sub(
    r'(<th[^>]*>[^<]*</th>)',  # Find a <th> (will insert after the first match)
    r'\1\n<th style="width: 10%;">x-leger-default</th>',
    html,
    count=1  # Only insert once
)

# Step 5: Add x-leger-default column in row generation
html = re.sub(
    r'(//.*other columns.*\n)',
    r'''\1
    // x-leger-default cell
    const xLegerDefaultCell = document.createElement('td');
    const xLegerDefaultInput = document.createElement('input');
    xLegerDefaultInput.type = 'text';
    xLegerDefaultInput.className = 'x-leger-default-input';
    xLegerDefaultInput.dataset.var = varName;
    xLegerDefaultInput.value = classification['variable_classifications'][varName].x_leger_default || '';
    xLegerDefaultCell.appendChild(xLegerDefaultInput);
    row.appendChild(xLegerDefaultCell);\n''',
    html
)

# Step 6: Add event listener for x-leger-default input
html = re.sub(
    r'(//.*event listener for the x-leger-default input.*\n)?(</script>)',
    r'''
// Add an event listener for the x-leger-default input
document.querySelectorAll('.x-leger-default-input').forEach(input => {
    input.addEventListener('change', function() {
        const varName = this.dataset.var;
        classification['variable_classifications'][varName].x_leger_default = this.value;
    });
});
\2''',
    html
)

# Step 7: Add x-leger-default to exportClassifications function
html = re.sub(
    r'("rationale": classification\[varName\]\.rationale,?)',
    r'\1\n            "x-leger-default": classification["variable_classifications"][varName].x_leger_default,',
    html
)

# Save the modified HTML to a new file
output_html_file = "updated_class.html"
with open(output_html_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated HTML written to '{output_html_file}'")
