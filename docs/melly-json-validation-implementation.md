# Melly Project: JSON Validation Implementation Plan

## Quick Summary for Melly

Your project needs to validate multiple JSON files in the Melly validation plugin:
- `init.json` (initial configuration)
- `c1-systems.json` (system definitions)
- `c2-containers.json` (container definitions)
- `c3-components.json` (component definitions)

## Recommended Approach

### 1. Primary Tool: `check-jsonschema` (CLI)

**Why**:
- Purpose-built for schema validation
- Excellent error reporting with context
- Python-based (matches your environment)
- Works as CLI and pre-commit hook
- Can use local or remote schemas
- Part of industry-standard jsonschema ecosystem

**Installation**:
```bash
pip install check-jsonschema
```

### 2. GitHub Actions: `cardinalby/schema-validation-action`

**Why**:
- Fastest option for GitHub Actions (uses fdir)
- Minimal setup
- Supports glob patterns perfectly
- Built-in .gitignore support
- Better performance than custom actions

## Implementation Steps

### Step 1: Create JSON Schemas

Create `.schemas/` directory with validation schemas:

```bash
mkdir -p .schemas
```

**Example: `.schemas/c1-systems.json`**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "C1 Systems Schema",
  "description": "Validates C1 system definitions",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "name", "description"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^[a-z0-9-]+$",
        "description": "System ID (lowercase alphanumeric with hyphens)"
      },
      "name": {
        "type": "string",
        "minLength": 1,
        "maxLength": 200,
        "description": "System name"
      },
      "description": {
        "type": "string",
        "minLength": 10,
        "description": "System description (min 10 characters)"
      },
      "containers": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["id", "name", "type"],
          "properties": {
            "id": { "type": "string" },
            "name": { "type": "string" },
            "type": { 
              "type": "string",
              "enum": ["web", "api", "database", "cache", "worker"]
            }
          }
        }
      }
    },
    "additionalProperties": false
  }
}
```

### Step 2: Create Validation Script

**`.github/scripts/validate-json.py`**:
```python
#!/usr/bin/env python3
"""
Melly JSON validation script.
Validates knowledge base JSON files against schemas.
"""

import json
import sys
import glob
from pathlib import Path
from jsonschema import Draft7Validator, ValidationError

def validate_file(schema_path, data_path):
    """Validate a single file against a schema."""
    try:
        with open(schema_path) as f:
            schema = json.load(f)
        with open(data_path) as f:
            data = json.load(f)
        
        validator = Draft7Validator(schema)
        
        if not validator.is_valid(data):
            errors = list(validator.iter_errors(data))
            return False, errors
        return True, None
    
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except Exception as e:
        return False, [str(e)]

def main():
    schema_path = sys.argv[1]
    file_patterns = sys.argv[2:]
    
    # Find all matching files
    files_to_validate = []
    for pattern in file_patterns:
        files_to_validate.extend(glob.glob(pattern, recursive=True))
    
    if not files_to_validate:
        print(f"No files found matching patterns: {file_patterns}")
        return 1
    
    all_valid = True
    
    for file_path in files_to_validate:
        valid, errors = validate_file(schema_path, file_path)
        
        if valid:
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            if isinstance(errors, list) and errors:
                for error in errors:
                    if hasattr(error, 'message'):
                        path = '.'.join(str(p) for p in error.path) or 'root'
                        print(f"    {path}: {error.message}")
                    else:
                        print(f"    {error}")
            all_valid = False
    
    return 0 if all_valid else 1

if __name__ == '__main__':
    sys.exit(main())
```

### Step 3: GitHub Actions Workflow

**`.github/workflows/validate-json.yml`**:
```yaml
name: Validate JSON Files

on:
  push:
    branches: [main, develop]
    paths:
      - 'knowledge-base/**/*.json'
      - '.schemas/**'
      - '.github/workflows/validate-json.yml'
  
  pull_request:
    branches: [main, develop]
    paths:
      - 'knowledge-base/**/*.json'
      - '.schemas/**'

jobs:
  validate:
    name: JSON Validation
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Validate C1 Systems
        uses: cardinalby/schema-validation-action@v1
        with:
          schema: .schemas/c1-systems.json
          json: 'knowledge-base/systems/**/c1-systems.json'
          verbose: true
      
      - name: Validate C2 Containers
        uses: cardinalby/schema-validation-action@v1
        with:
          schema: .schemas/c2-containers.json
          json: 'knowledge-base/systems/**/c2-containers.json'
          verbose: true
      
      - name: Validate C3 Components
        uses: cardinalby/schema-validation-action@v1
        with:
          schema: .schemas/c3-components.json
          json: 'knowledge-base/systems/**/c3-components.json'
          verbose: true
      
      - name: Report Results
        if: always()
        run: |
          echo "## JSON Validation Results" >> $GITHUB_STEP_SUMMARY
          if [ "${{ job.status }}" == "success" ]; then
            echo "✅ All JSON files passed validation" >> $GITHUB_STEP_SUMMARY
          else
            echo "❌ JSON validation failed - see logs above" >> $GITHUB_STEP_SUMMARY
          fi
```

### Step 4: Pre-commit Hook (Local)

**`.pre-commit-config.yaml`**:
```yaml
repos:
  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.35.0
    hooks:
      - id: check-jsonschema
        name: Validate C1 Systems
        args:
          - --schemafile=.schemas/c1-systems.json
        files: '^knowledge-base/systems/.*/c1-systems\.json$'
      
      - id: check-jsonschema
        name: Validate C2 Containers
        args:
          - --schemafile=.schemas/c2-containers.json
        files: '^knowledge-base/systems/.*/c2-containers\.json$'
      
      - id: check-jsonschema
        name: Validate C3 Components
        args:
          - --schemafile=.schemas/c3-components.json
        files: '^knowledge-base/systems/.*/c3-components\.json$'
```

### Step 5: Local Testing

```bash
# Install check-jsonschema
pip install check-jsonschema

# Test validation manually
check-jsonschema \
  --schemafile .schemas/c1-systems.json \
  knowledge-base/systems/*/c1-systems.json \
  --verbose

# Or use Python script
python .github/scripts/validate-json.py \
  .schemas/c1-systems.json \
  'knowledge-base/systems/*/c1-systems.json'
```

## Error Handling Strategy

### When Validation Fails

1. **Syntax Errors**: JSON is malformed (missing quotes, braces, etc.)
   - Fix with `jq '.' file.json` to see the error

2. **Schema Errors**: JSON is valid but doesn't match schema
   - Check required fields are present
   - Verify field types match (string vs number, etc.)
   - Check patterns for string validation
   - Verify array/enum values

### Debugging

```bash
# Pretty-print JSON to find syntax errors
jq '.' knowledge-base/systems/my-system/c1-systems.json

# Validate against schema with verbose output
check-jsonschema \
  --schemafile .schemas/c1-systems.json \
  knowledge-base/systems/my-system/c1-systems.json \
  --verbose

# Test schema validity itself
jq empty < .schemas/c1-systems.json
```

## Integration with Validation Plugin

The melly-validation plugin should:

1. **Store schemas** in `.schemas/` directory
2. **Include validation script** in `plugins/melly-validation/scripts/`
3. **Document schemas** with examples
4. **Support incremental validation** (check only changed files)
5. **Report errors clearly** (file, line, field, message)

### Plugin Structure

```
plugins/melly-validation/
├── scripts/
│   ├── validate-json.py          # Main validation script
│   ├── validate-init.sh          # Check init.json
│   ├── validate-c1-systems.sh    # Check c1-systems.json
│   ├── validate-c2-containers.sh # Check c2-containers.json
│   └── validate-c3-components.sh # Check c3-components.json
├── schemas/
│   ├── init.json
│   ├── c1-systems.json
│   ├── c2-containers.json
│   └── c3-components.json
└── README.md
```

## Performance Considerations

- `cardinalby/schema-validation-action`: ~1-2 seconds for typical repos
- `check-jsonschema`: ~500ms-1s for similar validation
- Pre-commit hooks: Instant (only runs on changed files)

## Comparison: What to Choose

| Scenario | Tool | Why |
|----------|------|-----|
| **Local development** | `check-jsonschema` CLI + pre-commit | Fast feedback, blocks bad commits |
| **CI/CD pipeline** | `cardinalby/schema-validation-action` | Minimal setup, fast, reliable |
| **Custom validation** | Python script | Full control, custom logic |
| **Quick syntax check** | `jq` | Lightweight, no setup |

## Actionable Checklist

- [ ] Create `.schemas/` directory with JSON Schema files
- [ ] Write `.github/workflows/validate-json.yml`
- [ ] Create `.github/scripts/validate-json.py`
- [ ] Add to `.pre-commit-config.yaml`
- [ ] Test locally with sample JSON files
- [ ] Test in GitHub Actions with PR
- [ ] Add documentation to melly-validation plugin
- [ ] Update TASKS.md with validation approach
- [ ] Set up branch protection rules to require validation

## Resources

- **check-jsonschema docs**: https://check-jsonschema.readthedocs.io/
- **cardinalby/schema-validation-action**: https://github.com/cardinalby/schema-validation-action
- **JSON Schema Guide**: https://json-schema.org/understanding-json-schema/
- **jsonschema (Python)**: https://python-jsonschema.readthedocs.io/

