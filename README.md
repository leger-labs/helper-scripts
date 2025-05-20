# Complete Workflow for OpenWebUI Schema Generation

## 1. `download_and_prepare_docs.py`

This script handles the initial preparation steps:

- Downloads the latest OpenWebUI environment configuration document from GitHub
- Extracts all DEFAULT_*_TEMPLATE variables to a separate JSON file
- Splits the documentation into sections based on ## headers
- Saves each section as a separate file for LLM analysis

**Usage:**
```bash
python download_and_prepare_docs.py --output-dir prepared_docs
```

**Output:**
- `prepared_docs/default_templates.json` - All extracted templates
- `prepared_docs/sections/*.md` - Individual section files
- `prepared_docs/env-configuration-processed.md` - Full document with templates removed

## 2. LLM-based Relationship Mapping

With the sections prepared, you'll use the high-quality system prompt to analyze each section with Claude:

1. Copy the section content from `prepared_docs/sections/`
2. Use the `relationship_mapping_system_prompt.md` with Claude
3. Save each output to a JSON file in a `mappings` directory

## 3. `merge_relationship_mappings.py`

After getting LLM-generated mappings for each section, this script combines them into a unified mapping:

- Merges provider mappings from all section analyses
- Merges boolean selectors from all section analyses
- Resolves any duplicate mappings intelligently
- Produces a single JSON file with all relationships

**Usage:**
```bash
python merge_relationship_mappings.py --input-dir mappings --output relationship_mappings.json
```

**Output:**
- `relationship_mappings.json` - Comprehensive relationship mapping

## 4. `unified_schema_generator.py`

This script generates the complete OpenAPI schema:

- Extracts basic schema properties from the documentation
- Incorporates the default templates
- Applies the relationship mappings
- Compares with your manual classification JSON
- Identifies any new variables that need classification
- Appends templates for new variables to the classification file

**Usage:**
```bash
python unified_schema_generator.py \
  --input prepared_docs/env-configuration-processed.md \
  --templates prepared_docs/default_templates.json \
  --relationships relationship_mappings.json \
  --classifications final_leger_openwebui_var_classifications.json \
  --output openwebui-config-schema.json
```

**Output:**
- `openwebui-config-schema.json` - The final OpenAPI schema
- `final_leger_openwebui_var_classifications_with_new_vars.json` - Updated classification file with new variables

## Complete Workflow

1. **Preparation**:
   ```bash
   python download_and_prepare_docs.py --output-dir prepared_docs
   ```

2. **Generate Relationships** (Manual LLM Step):
   - Use Claude to analyze each section in `prepared_docs/sections/`
   - Save outputs to `mappings/section1.json`, `mappings/section2.json`, etc.

3. **Merge Relationships**:
   ```bash
   python merge_relationship_mappings.py --input-dir mappings --output relationship_mappings.json
   ```

4. **Generate Schema**:
   ```bash
   python unified_schema_generator.py \
     --input prepared_docs/env-configuration-processed.md \
     --templates prepared_docs/default_templates.json \
     --relationships relationship_mappings.json \
     --classifications final_leger_openwebui_var_classifications.json \
     --output openwebui-config-schema.json
   ```

5. **Update Classifications** (Manual Step):
   - Review `final_leger_openwebui_var_classifications_with_new_vars.json`
   - Update annotations for new variables
   - Copy back to `final_leger_openwebui_var_classifications.json`

6. **Regenerate Final Schema**:
   ```bash
   python unified_schema_generator.py \
     --input prepared_docs/env-configuration-processed.md \
     --templates prepared_docs/default_templates.json \
     --relationships relationship_mappings.json \
     --classifications final_leger_openwebui_var_classifications.json \
     --output openwebui-config-schema.json
   ```

This approach provides the flexibility, modularity and maintainability you requested, while leveraging both automated extraction and LLM intelligence for the most accurate results.
