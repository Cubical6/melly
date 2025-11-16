# JSON Validation in CI/CD Pipelines: Comprehensive Research & Recommendations

## Executive Summary

This document provides recommendations for validating JSON files in GitHub Actions CI/CD pipelines, based on analysis of current tools, GitHub Actions, and industry best practices.

**Bottom Line Recommendations:**
1. **For simple syntax validation**: Use `jq` (lightweight, pre-installed on most systems)
2. **For schema-based validation**: Use `check-jsonschema` CLI (comprehensive, fast, excellent GitHub integration)
3. **For GitHub Actions workflows specifically**: Use `cardinalby/schema-validation-action` (fastest, modern, .gitignore support)
4. **For complex validation logic**: Use Python's `jsonschema` package with custom validation scripts

---

## Part 1: Command-Line JSON Validators Comparison

### 1. jq - Swiss Army Knife for JSON
**Status**: Industry standard, pre-installed on most Linux systems

**Strengths**:
- Lightweight and universally available
- Can validate JSON syntax and structure with filters
- Extremely flexible for data transformation
- Excellent for pipeline operations

**Weaknesses**:
- Not purpose-built for schema validation
- Syntax can be complex for validation tasks
- Limited error reporting

**Basic Usage**:
```bash
# Validate JSON syntax only
jq empty < file.json && echo "Valid JSON" || echo "Invalid JSON"

# Validate and pretty-print
jq '.' file.json > /dev/null && echo "Valid" || echo "Invalid"

# Validate multiple files
for file in *.json; do
  jq empty < "$file" || echo "Invalid: $file"
done
```

**CI/CD Integration Cost**: Minimal (usually pre-installed)
**Use Case**: Quick syntax validation, not suitable for schema-based validation

---

### 2. jsonlint - Purpose-Built JSON Validator
**Status**: Dedicated JSON linting tool, Node.js-based

**Strengths**:
- Purpose-built for JSON validation
- Good error messages with line numbers
- Quick to set up
- Can be used globally or per-project

**Weaknesses**:
- Only validates JSON syntax, not schema compliance
- Requires Node.js installation
- Limited to syntax checking

**Installation & Usage**:
```bash
# Install globally
npm install -g jsonlint

# Validate single file
jsonlint file.json

# Validate with options
jsonlint --compact file.json

# Validate multiple files
jsonlint **/*.json

# With error output
jsonlint file.json 2>&1 || exit 1
```

**GitHub Actions Integration**:
```yaml
- name: Install jsonlint
  run: npm install -g jsonlint

- name: Validate JSON files
  run: jsonlint src/**/*.json
```

**CI/CD Integration Cost**: Low (npm-based)
**Use Case**: Basic JSON syntax validation across a codebase

---

### 3. check-jsonschema - CLI with Schema Validation
**Status**: Modern, actively maintained, excellent GitHub integration

**Repository**: https://github.com/python-jsonschema/check-jsonschema

**Strengths**:
- Built-in support for GitHub Workflows, Renovate, Azure Pipelines
- Validates against JSON Schema (Draft 4, 6, 7, 2019-09, 2020-12)
- Works as CLI and pre-commit hook
- Can reference remote schemas with automatic caching
- Excellent error messages with context
- Works with local or remote schema files
- Supports multiple file validation with glob patterns
- Part of python-jsonschema ecosystem (industry standard)

**Weaknesses**:
- Requires Python 3.7+
- Slightly slower than pure JavaScript validators for large datasets
- Must learn JSON Schema format

**Installation & Usage**:
```bash
# Install via pip
pip install check-jsonschema

# Install via pipx (recommended)
pipx install check-jsonschema

# Install via homebrew (macOS)
brew install check-jsonschema

# Validate single file against schema
check-jsonschema --schemafile schema.json instance.json

# Validate multiple files
check-jsonschema --schemafile schema.json *.json

# Using remote schema with caching
check-jsonschema \
  --schemafile https://json.schemastore.org/package.json \
  package.json

# Verbose output for debugging
check-jsonschema --schemafile schema.json instance.json --verbose

# Default schemas for common files
check-jsonschema --schemafile https://json.schemastore.org/.github/workflows/workflows.json .github/workflows/*.yml

# Using data from stdin
cat data.json | check-jsonschema --schemafile schema.json -
```

**GitHub Actions Integration**:
```yaml
name: Validate JSON Files

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install check-jsonschema
        run: pip install check-jsonschema
      
      - name: Validate JSON files
        run: |
          check-jsonschema \
            --schemafile knowledge-base/schemas/init.json \
            knowledge-base/systems/*/init.json
```

**Pre-commit Hook Integration**:
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/python-jsonschema/check-jsonschema
  rev: 0.35.0
  hooks:
    - id: check-github-workflows
      args: ["--verbose"]
    
    - id: check-jsonschema
      args: 
        - --schemafile=.schemas/config.json
      files: |
        (?x)^(
          config\.json|
          data/.*\.json
        )$
```

**CI/CD Integration Cost**: Low (Python-based, widely available)
**Use Case**: Comprehensive schema-based validation with excellent error reporting

---

### 4. ajv-cli - High-Performance Schema Validator
**Status**: Active, widely used in enterprise environments

**Repository**: https://github.com/ajv-validator/ajv-cli

**Strengths**:
- Fastest JSON Schema validator available
- Supports all JSON Schema drafts (3, 4, 6, 7, 2019-09, 2020-12)
- Can generate standalone validation code (for CI performance)
- Multiple error format options (JSON, line format, Code Climate)
- Excellent for large-scale validation tasks

**Weaknesses**:
- Requires Node.js
- Less user-friendly than check-jsonschema
- Error messages less descriptive than alternatives

**Installation & Usage**:
```bash
# Install globally
npm install -g ajv-cli ajv-formats

# Basic validation
ajv validate -s schema.json -d data.json

# Validate with error reporting
npx ajv validate -s schema.json -d data.json -c ajv-formats

# Multiple files (with loop)
for file in src/**/*.json; do
  npx ajv validate -s schema.json -d "$file" || exit 1
done

# Line format output (CI-friendly)
ajv validate -s schema.json -d data.json --output=line

# Code Climate format (GitLab compatible)
ajv validate -s schema.json -d data.json --output=codeClimate

# Test mode (assert results)
ajv test -s schema.json -d valid.json --valid
ajv test -s schema.json -d invalid.json --invalid
```

**GitHub Actions Integration**:
```yaml
- name: Install ajv-cli
  run: npm install -g ajv-cli ajv-formats

- name: Validate JSON files
  run: |
    for file in src/**/*.json; do
      npx ajv validate -s schema.json -d "$file" || exit 1
    done
```

**CI/CD Integration Cost**: Low (npm-based)
**Use Case**: High-performance validation for large datasets or when building standalone validators

---

## Part 2: GitHub Actions for JSON Validation

### Available Pre-Built Actions

#### 1. **schema-validation-action** (cardinalby)
**GitHub**: https://github.com/cardinalby/schema-validation-action
**Marketplace**: schema-validation-action

**Strengths**:
- Extremely fast (uses fdir for efficient directory crawling)
- Modern, actively maintained
- Supports .gitignore integration for file exclusion
- Can validate both JSON and YAML
- Multiple file support with glob patterns
- Built on reliable ajv validator
- Detailed error reporting

**Weaknesses**:
- Limited documentation
- Less customization than CLI tools

**Usage Example**:
```yaml
name: Validate Schemas

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate JSON against schema
        uses: cardinalby/schema-validation-action@v1
        with:
          # Required: path to the JSON schema
          schema: schemas/config.json
          
          # Required: files to validate (glob pattern)
          json: "config/**/*.json"
          
          # Optional: respect .gitignore
          ignoreGitignore: false
          
          # Optional: verbose output
          verbose: true
          
          # Optional: custom error messages
          customErrorMessages: |
            {
              "/properties/name/type": "Name must be a string",
              "/required": "Missing required field"
            }
```

**Configuration Tips**:
- Use glob patterns: `config/**/*.json` or `config/*.json`
- Exclude paths: Add to .gitignore with trailing slash for directories
- For JSON files only: Use `*.json`, `**/*.json`
- For YAML too: Omit file extension or use both `.json` and `.yaml`

---

#### 2. **Validate JSON Action** (OrRosenblatt)
**GitHub**: https://github.com/OrRosenblatt/validate-json-action
**Marketplace**: Validate JSON

**Strengths**:
- Simple, focused action
- Clear error reporting
- Well-documented with examples
- Uses fast ajv validator

**Weaknesses**:
- Less feature-rich than schema-validation-action
- Limited glob pattern support

**Usage Example**:
```yaml
- name: Validate JSON files
  uses: OrRosenblatt/validate-json-action@master
  env:
    SCHEMA: schemas/config.json
    JSONS: |
      config.json
      src/**/*.json
```

---

#### 3. **jsonschema_validator** (PnX-SI)
**GitHub**: https://github.com/PnX-SI/jsonschema_validator

**Strengths**:
- Supports multiple schemas with $ref resolution
- Good for complex schema hierarchies
- Uses ajv validator

**Weaknesses**:
- More complex setup required
- Fewer maintained

**Usage Example**:
```yaml
- name: Validate with jsonschema
  uses: PnX-SI/jsonschema_validator@v1.0.0
  with:
    data: data.json
    schemas: schemas/main.json
```

---

#### 4. **json-yaml-validate**
**GitHub**: https://github.com/marketplace/actions/json-yaml-validate

**Strengths**:
- Validates both JSON and YAML
- Can validate syntax only or against schema
- Supports external schema references

**Weaknesses**:
- Less documentation
- Fewer stars/community adoption

---

### Recommendation: Best GitHub Action

**Winner: `cardinalby/schema-validation-action`**

Why:
1. **Performance**: Extremely fast directory crawling
2. **Features**: Supports .gitignore, glob patterns, custom errors
3. **Maintenance**: Actively maintained
4. **Flexibility**: Works with both JSON and YAML
5. **Reliability**: Built on well-tested ajv validator

---

## Part 3: Python-Based Validation

### jsonschema Package

**Installation**:
```bash
pip install jsonschema check-jsonschema
```

**Direct Python Usage**:
```python
import json
from jsonschema import validate, ValidationError

# Load schema and instance
with open('schema.json') as f:
    schema = json.load(f)

with open('data.json') as f:
    instance = json.load(f)

# Validate
try:
    validate(instance=instance, schema=schema)
    print("Valid!")
except ValidationError as e:
    print(f"Validation error: {e.message}")
    exit(1)
```

**Command-Line Usage** (via check-jsonschema):
Already covered above under section "3. check-jsonschema"

**Advanced Python Validation Script**:
```python
#!/usr/bin/env python3
"""
Comprehensive JSON validation script for CI/CD pipelines.
Supports batch validation with detailed reporting.
"""

import json
import sys
import glob
from pathlib import Path
from jsonschema import Draft7Validator, ValidationError

def validate_files(schema_path, file_patterns, verbose=False):
    """Validate multiple JSON files against a schema."""
    
    # Load schema
    with open(schema_path) as f:
        schema = json.load(f)
    
    validator = Draft7Validator(schema)
    errors = []
    valid_count = 0
    
    # Find all matching files
    files_to_validate = []
    for pattern in file_patterns:
        files_to_validate.extend(glob.glob(pattern, recursive=True))
    
    if not files_to_validate:
        print(f"No files found matching patterns: {file_patterns}")
        return 1
    
    # Validate each file
    for file_path in files_to_validate:
        try:
            with open(file_path) as f:
                data = json.load(f)
            
            # Validate against schema
            if not validator.is_valid(data):
                errors.append({
                    'file': file_path,
                    'errors': [
                        {
                            'path': list(e.path),
                            'message': e.message,
                            'schema_path': list(e.schema_path)
                        }
                        for e in validator.iter_errors(data)
                    ]
                })
            else:
                valid_count += 1
                if verbose:
                    print(f"✓ {file_path}")
        
        except json.JSONDecodeError as e:
            errors.append({
                'file': file_path,
                'error': f"Invalid JSON: {e.msg}",
                'line': e.lineno,
                'column': e.colno
            })
        except Exception as e:
            errors.append({
                'file': file_path,
                'error': str(e)
            })
    
    # Report results
    if errors:
        print(f"\n❌ Validation failed: {len(errors)} file(s) with errors")
        for error in errors:
            print(f"\n  File: {error['file']}")
            if 'errors' in error:
                for err in error['errors']:
                    path = '.'.join(str(p) for p in err['path']) or 'root'
                    print(f"    - {path}: {err['message']}")
            else:
                print(f"    - {error.get('error', 'Unknown error')}")
        return 1
    else:
        print(f"✓ All {valid_count} file(s) are valid")
        return 0

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate JSON files against a schema'
    )
    parser.add_argument('schema', help='Path to JSON schema')
    parser.add_argument('files', nargs='+', help='Files/patterns to validate')
    parser.add_argument('-v', '--verbose', action='store_true')
    
    args = parser.parse_args()
    
    sys.exit(validate_files(args.schema, args.files, args.verbose))
```

**GitHub Actions with Python Script**:
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Install validation dependencies
  run: pip install jsonschema

- name: Validate JSON files
  run: python .github/scripts/validate-json.py \
    schemas/config.json \
    'config/**/*.json' \
    'data/**/*.json' \
    --verbose
```

---

## Part 4: Error Handling & Reporting Best Practices

### 1. Exit Codes Strategy

All validation tools should use proper exit codes:

```yaml
# Pattern: check && success || failure
validate-json.sh || {
  echo "❌ JSON validation failed"
  exit 1
}
```

**Exit Codes**:
- `0` - All validations passed
- `1` - Validation failed (JSON syntax or schema)
- `2` - Tool error (missing files, bad config)
- `3` - Configuration error (bad schema)

### 2. Error Output Format

**Human-readable format** (development):
```
File: config/app.json
  Line 15: Property "name" is required
  Line 23: "version" must be a string

File: config/db.json
  Line 8: "port" must be <= 65535
```

**Machine-readable format** (CI systems):
```
config/app.json:15:0 - Property "name" is required
config/app.json:23:0 - "version" must be a string
config/db.json:8:0 - "port" must be <= 65535
```

**JSON format** (programmatic processing):
```json
{
  "valid": false,
  "errors": [
    {
      "file": "config/app.json",
      "line": 15,
      "path": "properties.name",
      "message": "Property \"name\" is required"
    }
  ]
}
```

### 3. Comprehensive Error Handling Script

```bash
#!/bin/bash
set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCHEMA_FILE="${1:-schema.json}"
FILE_PATTERN="${2:-*.json}"
ERRORS=0
WARNINGS=0
VALIDATED=0

# Function to report error
report_error() {
  local file=$1
  local message=$2
  echo -e "${RED}✗ Error:${NC} $file"
  echo "  $message"
  ((ERRORS++))
}

# Function to report warning
report_warning() {
  local file=$1
  local message=$2
  echo -e "${YELLOW}⚠ Warning:${NC} $file"
  echo "  $message"
  ((WARNINGS++))
}

# Validate schema exists
if [[ ! -f "$SCHEMA_FILE" ]]; then
  echo -e "${RED}Error: Schema file not found: $SCHEMA_FILE${NC}"
  exit 2
fi

# Find and validate files
while IFS= read -r file; do
  # Skip if no files found
  [[ -z "$file" ]] && continue
  
  # Validate JSON syntax first
  if ! jq empty < "$file" 2>/dev/null; then
    report_error "$file" "Invalid JSON syntax"
    continue
  fi
  
  # Validate against schema
  if ! check-jsonschema --schemafile "$SCHEMA_FILE" "$file" 2>/dev/null; then
    report_error "$file" "Failed schema validation"
    continue
  fi
  
  # Check file size (optional warning)
  if [[ $(stat -f%z "$file" 2>/dev/null || stat -c%s "$file") -gt 5242880 ]]; then
    report_warning "$file" "Large file (>5MB) may impact performance"
  fi
  
  ((VALIDATED++))
  echo -e "${GREEN}✓ Valid:${NC} $file"
  
done < <(find . -name "$FILE_PATTERN" -not -path '*/node_modules/*' -not -path '*/.git/*')

# Summary
echo ""
echo "════════════════════════════════════════"
echo "Validation Summary"
echo "════════════════════════════════════════"
echo -e "Valid files: ${GREEN}$VALIDATED${NC}"
echo -e "Errors:      ${RED}$ERRORS${NC}"
echo -e "Warnings:    ${YELLOW}$WARNINGS${NC}"

# Exit with appropriate code
if [[ $ERRORS -gt 0 ]]; then
  exit 1
elif [[ $WARNINGS -gt 0 ]]; then
  exit 0  # Warnings don't fail CI
fi

exit 0
```

### 4. GitHub Actions with Error Summary

```yaml
name: JSON Validation with Error Summary

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install check-jsonschema
        run: pip install check-jsonschema
      
      - name: Validate JSON files
        id: validation
        run: |
          set +e  # Don't exit on error
          
          # Run validation and capture output
          OUTPUT=$(check-jsonschema \
            --schemafile schemas/config.json \
            'config/**/*.json' 2>&1)
          STATUS=$?
          
          # Store output for later use
          echo "output<<EOF" >> $GITHUB_OUTPUT
          echo "$OUTPUT" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
          
          exit $STATUS
      
      - name: Report Results
        if: always()
        run: |
          echo "## JSON Validation Results" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          
          if [ ${{ steps.validation.outcome }} == "success" ]; then
            echo "✅ All JSON files are valid" >> $GITHUB_STEP_SUMMARY
          else
            echo "❌ JSON validation failed" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "### Errors:" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo '```' >> $GITHUB_STEP_SUMMARY
            echo "${{ steps.validation.outputs.output }}" >> $GITHUB_STEP_SUMMARY
            echo '```' >> $GITHUB_STEP_SUMMARY
          fi
      
      - name: Comment on PR
        if: always() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const output = `${{ steps.validation.outputs.output }}`;
            const status = '${{ steps.validation.outcome }}';
            
            const comment = status === 'success'
              ? '✅ JSON validation passed'
              : `❌ JSON validation failed\n\n\`\`\`\n${output}\n\`\`\``;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

## Part 5: Integration Strategies & Implementation Guide

### Strategy 1: Simple Syntax Validation (Minimal Setup)

**Best for**: Quick checks, simple projects

```yaml
name: Validate JSON Syntax

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate JSON files
        run: |
          find . -name "*.json" -not -path "*/node_modules/*" | while read f; do
            jq empty < "$f" || (echo "Invalid: $f" && exit 1)
          done
```

**Pros**: No setup, immediate feedback
**Cons**: No schema validation

---

### Strategy 2: Schema-Based with Built-In Action (Recommended)

**Best for**: Most projects, good balance of features and simplicity

```yaml
name: Validate JSON Schemas

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate against schemas
        uses: cardinalby/schema-validation-action@v1
        with:
          schema: schemas/config.json
          json: 'config/**/*.json'
          verbose: true
```

**Pros**: Fast, feature-rich, minimal setup
**Cons**: Limited customization

---

### Strategy 3: Comprehensive CLI Validation (Maximum Control)

**Best for**: Complex validation needs, custom error handling

```yaml
name: Comprehensive JSON Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install validation tools
        run: |
          pip install check-jsonschema jsonschema
          npm install -g jsonlint
      
      - name: Run validation suite
        run: |
          echo "Step 1: Syntax validation..."
          jsonlint 'config/**/*.json'
          
          echo "Step 2: Schema validation..."
          check-jsonschema --schemafile schemas/config.json 'config/**/*.json'
          
          echo "Step 3: Custom validation..."
          python scripts/validate-json.py schemas/config.json 'config/**/*.json'
      
      - name: Report to PR
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ JSON validation failed. Check the logs for details.'
            })
```

---

## Part 6: JSON Schema Best Practices

### Creating Effective Schemas

**Basic Schema Template**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/schemas/config.json",
  
  "title": "Configuration Schema",
  "description": "Validates application configuration files",
  "type": "object",
  
  "required": ["name", "version"],
  
  "properties": {
    "name": {
      "type": "string",
      "description": "Application name",
      "minLength": 1,
      "maxLength": 100
    },
    
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version (e.g., 1.0.0)"
    },
    
    "port": {
      "type": "integer",
      "minimum": 1,
      "maximum": 65535,
      "default": 3000
    },
    
    "features": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    },
    
    "tags": {
      "type": "object",
      "additionalProperties": {
        "type": "string"
      }
    }
  },
  
  "additionalProperties": false
}
```

### Custom Error Messages

```json
{
  "type": "object",
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "errorMessage": {
        "format": "Please provide a valid email address"
      }
    }
  }
}
```

---

## Part 7: Complete Implementation Example

### Project Setup

```
melly/
├── .github/
│   └── workflows/
│       └── validate-json.yml
├── .schemas/
│   ├── init.json
│   ├── c1-systems.json
│   ├── c2-containers.json
│   └── c3-components.json
├── scripts/
│   └── validate-json.py
└── knowledge-base/
    └── systems/
        └── *.json
```

### Schema Files

**`.schemas/c1-systems.json`**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "C1 Systems",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["id", "name", "description"],
    "properties": {
      "id": {
        "type": "string",
        "pattern": "^[a-z0-9-]+$"
      },
      "name": {
        "type": "string",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "type": "string",
        "minLength": 10
      },
      "containers": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["id", "name"],
          "properties": {
            "id": { "type": "string" },
            "name": { "type": "string" }
          }
        }
      }
    },
    "additionalProperties": false
  }
}
```

### Validation Workflow

```yaml
name: Validate JSON Schemas

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
    name: JSON Schema Validation
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install validation tools
        run: |
          pip install check-jsonschema jsonschema
          npm install -g jsonlint
      
      - name: Validate JSON syntax
        id: syntax
        run: |
          echo "Running syntax validation..."
          jsonlint 'knowledge-base/**/*.json' || exit 1
      
      - name: Validate against schemas
        id: schema
        run: |
          echo "Validating C1 systems..."
          check-jsonschema \
            --schemafile .schemas/c1-systems.json \
            knowledge-base/systems/*/c1-systems.json || exit 1
          
          echo "Validating C2 containers..."
          check-jsonschema \
            --schemafile .schemas/c2-containers.json \
            knowledge-base/systems/*/c2-containers.json || exit 1
          
          echo "Validating C3 components..."
          check-jsonschema \
            --schemafile .schemas/c3-components.json \
            knowledge-base/systems/*/c3-components.json || exit 1
      
      - name: Custom validation
        id: custom
        run: |
          python scripts/validate-json.py \
            .schemas/c1-systems.json \
            knowledge-base/systems/*/c1-systems.json \
            --verbose
      
      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: validation-report.json
          retention-days: 30
      
      - name: Comment on PR
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ JSON validation failed. Please check the validation report in the artifacts.'
            })
      
      - name: Add success comment
        if: success() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '✅ All JSON files passed validation!'
            })
```

---

## Summary: Tool Comparison Matrix

| Tool | Type | Performance | Setup | Features | Best For |
|------|------|-------------|-------|----------|----------|
| **jq** | CLI | Very Fast | Minimal | Syntax only | Quick checks |
| **jsonlint** | CLI | Fast | npm | Syntax + lint | Basic validation |
| **check-jsonschema** | CLI | Moderate | pip | Schema + detailed errors | Production use |
| **ajv-cli** | CLI | Fastest | npm | Schema + formats | High performance |
| **jsonschema (Python)** | Library | Moderate | pip | Custom validation | Complex logic |
| **cardinalby/schema-validation** | Action | Very Fast | Zero | Schema + globbing | GitHub Actions |

---

## Final Recommendations for Melly Project

Based on your melly project requirements:

1. **Primary Tool**: `check-jsonschema` CLI
   - Validates JSON Schema for `init.json`, `c1-systems.json`, `c2-containers.json`, `c3-components.json`
   - Built-in support for local and remote schemas
   - Excellent error reporting for debugging

2. **GitHub Actions**:
   ```yaml
   - uses: cardinalby/schema-validation-action@v1
     with:
       schema: .schemas/c1-systems.json
       json: knowledge-base/systems/**/*.json
       verbose: true
   ```

3. **Error Handling**:
   - Validate JSON syntax first (jq)
   - Validate against schema (check-jsonschema)
   - Run custom validation scripts for business logic
   - Report errors with context and suggestions

4. **Integration Points**:
   - Validation runs on every push/PR
   - Blocks merges if schemas invalid
   - Posts validation summary to PR
   - Archives validation reports for audit trail

5. **Pre-commit Hook** (local):
   ```yaml
   - repo: https://github.com/python-jsonschema/check-jsonschema
     hooks:
       - id: check-jsonschema
         args: ['--schemafile=.schemas/c1-systems.json']
         files: '^knowledge-base/systems/.*\.json$'
   ```

