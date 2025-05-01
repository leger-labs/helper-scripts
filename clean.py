
import json

# Load the original JSON
with open('variables_tracking.json', 'r') as f:
    data = json.load(f)

# Extract just the variables dictionary
variables = data.get("variables", {})

# Create a simplified version with only 'order'
simplified = {
    key: {
        "order": value["order"]
    }
    for key, value in variables.items()
    if "order" in value
}

# Save the result to variables.json
with open('variables.json', 'w') as f:
    json.dump(simplified, f, indent=2)

print("Simplified variables written to variables.json")
