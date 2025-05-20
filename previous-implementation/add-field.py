
import re
import sys

# Ensure you specify the input file in the command line (class.html)
if len(sys.argv) < 2:
    print("Usage: python add-field.py <input-html-file>")
    sys.exit(1)

# Get the input file from the command line argument
input_file = sys.argv[1]

# Read the original HTML (class.html or any file passed as argument)
with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

# Step 1: Add a new column header for "x-leger-default"
html = re.sub(
    r'(<th[^>]*>[^<]*</th>)',  # Find a <th> (will insert after the first match)
    r'\1\n<th style="width: 10%;">x-leger-default</th>',
    html,
    count=1  # Only insert once
)

# Step 2: Add x-leger-default column in row generation
html = re.sub(
    r'(//.*other columns.*\n)',
    r'''\1
    // x-leger-default cell
    const xLegerDefaultCell = document.createElement('td');
    const xLegerDefaultInput = document.createElement('input');
    xLegerDefaultInput.type = 'text';
    xLegerDefaultInput.className = 'x-leger-default-input';
    xLegerDefaultInput.dataset.var = varName;
    xLegerDefaultInput.value = classification[varName].x_leger_default || '';
    xLegerDefaultCell.appendChild(xLegerDefaultInput);
    row.appendChild(xLegerDefaultCell);\n''',
    html
)

# Step 3: Add x_leger_default to classification initialization
html = re.sub(
    r'("rationale":\s*""\s*)',
    r'\1,\n        "x_leger_default": ""',
    html
)

# Step 4: Add event listener for x-leger-default input
html = re.sub(
    r'(//.*event listener for the x-leger-default input.*\n)?(</script>)',
    r'''
// Add an event listener for the x-leger-default input
document.querySelectorAll('.x-leger-default-input').forEach(input => {
    input.addEventListener('change', function() {
        const varName = this.dataset.var;
        classification[varName].x_leger_default = this.value;
    });
});
\2''',
    html
)

# Step 5: Add x-leger-default to exportClassifications function
html = re.sub(
    r'("rationale": classification\[varName\]\.rationale,?)',
    r'\1\n            "x-leger-default": classification[varName].x_leger_default,',
    html
)

# Save the modified HTML to a new file
output_file = "updated_class.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated HTML written to '{output_file}'")
