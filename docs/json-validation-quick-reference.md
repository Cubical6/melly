# JSON Validation Quick Reference Guide

## One-Page Summary

### Recommended Stack for Melly

| Component | Tool | Command |
|-----------|------|---------|
| **CLI Validation** | `check-jsonschema` | `pip install check-jsonschema` |
| **GitHub Actions** | `cardinalby/schema-validation-action` | See workflow below |
| **Local Pre-commit** | `check-jsonschema` hooks | Add to `.pre-commit-config.yaml` |
| **Syntax Check** | `jq` | Pre-installed on most systems |

### Command Examples

```bash
# Install check-jsonschema
pip install check-jsonschema

# Validate single file
check-jsonschema --schemafile .schemas/c1-systems.json knowledge-base/systems/app/c1-systems.json

# Validate multiple files with glob
check-jsonschema --schemafile .schemas/c1-systems.json 'knowledge-base/systems/*/c1-systems.json'

# Validate with verbose output
check-jsonschema --schemafile .schemas/c1-systems.json knowledge-base/systems/app/c1-systems.json --verbose

# Quick syntax check
jq empty < knowledge-base/systems/app/c1-systems.json
```

### Minimal GitHub Actions Workflow

```yaml
name: Validate JSON

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate C1 Systems
        uses: cardinalby/schema-validation-action@v1
        with:
          schema: .schemas/c1-systems.json
          json: knowledge-base/systems/**/*.c1-systems.json
          verbose: true
```

### Minimal Pre-commit Config

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.35.0
    hooks:
      - id: check-jsonschema
        args: ['--schemafile=.schemas/c1-systems.json']
        files: 'c1-systems\.json$'
```

## Error Messages & Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid JSON` | Syntax error (missing quote, bracket) | Use `jq '.' file.json` to find it |
| `Property "x" is required` | Missing required field | Add the required property |
| `"field" must be a string` | Wrong data type | Change value to string (in quotes) |
| `"field" must match pattern` | String format invalid | Check regex pattern in schema |
| `Additional properties are not allowed` | Unknown property in JSON | Check schema for allowed properties |

## Performance

- Validation speed: ~500ms to 2s per schema
- Pre-commit hooks: ~100ms (only changed files)
- GitHub Actions: ~1-2s per workflow job

## Key Files to Create

```
.schemas/                          # Store JSON schemas
├── init.json
├── c1-systems.json
├── c2-containers.json
└── c3-components.json

.github/workflows/                 # GitHub Actions
└── validate-json.yml

.github/scripts/                   # Helper scripts
└── validate-json.py

plugins/melly-validation/          # Validation plugin
├── scripts/
│   ├── validate-json.py
│   ├── validate-c1-systems.sh
│   ├── validate-c2-containers.sh
│   └── validate-c3-components.sh
└── schemas/
    ├── init.json
    ├── c1-systems.json
    ├── c2-containers.json
    └── c3-components.json
```

## Implementation Order

1. **Create `.schemas/` directory** with JSON Schema files
2. **Write JSON validation schemas** (Draft 7 format)
3. **Add GitHub Actions workflow** (validate-json.yml)
4. **Create validation script** (validate-json.py)
5. **Set up pre-commit hooks** (.pre-commit-config.yaml)
6. **Test locally** with sample files
7. **Commit and push** to trigger CI validation
8. **Document in melly-validation plugin**

## Troubleshooting

### Validation Not Running

Check:
- [ ] Schema file exists and is valid JSON
- [ ] File patterns match your JSON file locations
- [ ] JSON files themselves are syntactically valid

### Validation Passes Locally But Fails in CI

Check:
- [ ] Same file is being validated (check paths)
- [ ] Schema file path is correct relative to repo root
- [ ] Python version is compatible (3.7+)

### Slow Validation

Optimization:
- Use glob patterns to exclude unnecessary files
- Run validation only on changed files (pre-commit)
- Cache remote schemas (automatic in check-jsonschema)

## Resources

- **Full Research**: See `/docs/json-validation-research.md`
- **Implementation Plan**: See `/docs/melly-json-validation-implementation.md`
- **JSON Schema Docs**: https://json-schema.org/
- **check-jsonschema**: https://check-jsonschema.readthedocs.io/
- **GitHub Actions**: https://github.com/marketplace/actions?query=json+validation

## Decision Matrix

Choose validation approach based on your needs:

### Simple & Fast (Recommended for Melly)
```
check-jsonschema (CLI) + cardinalby/schema-validation-action (GitHub Actions)
```
- Minimal setup
- Fast execution
- Excellent error messages
- Great GitHub integration

### Maximum Control
```
Python jsonschema + custom validation scripts
```
- Full programmatic control
- Complex validation logic
- Custom error handling

### Ultra-Fast CI
```
ajv-cli + GitHub Actions
```
- Fastest validator available
- Node.js-based
- Lower-level control

### Syntax Only
```
jq + minimal scripting
```
- Zero dependencies
- For basic JSON syntax checking
- Not schema-based

## Next Steps

1. Read `/docs/melly-json-validation-implementation.md` for step-by-step setup
2. Create `.schemas/` directory with your JSON schemas
3. Add validation GitHub Actions workflow
4. Test locally with `check-jsonschema`
5. Commit and verify CI validation works
6. Document in melly-validation plugin README

---
Last Updated: 2025-11-16
