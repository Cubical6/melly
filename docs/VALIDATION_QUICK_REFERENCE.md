# Melly Validation Scripts - Quick Reference Card

## Script Status at a Glance

| Script | Status | Input | Output | Validates |
|--------|--------|-------|--------|-----------|
| **validate-init.py** | 🔴 STUB | init.json | Exit code | Repository structure |
| **validate-c1-systems.py** | 🔴 STUB | c1-systems.json | Exit code | System definitions |
| **validate-c2-containers.py** | 🔴 STUB | c2-containers.json | Exit code | Container definitions + refs |
| **validate-c3-components.py** | 🔴 STUB | c3-components.json | Exit code | Component definitions + refs |
| **validate-markdown.py** | 🔴 STUB | *.md files | Exit code | Markdown structure |
| **check-timestamp.sh** | 🔴 STUB | JSON dir | Exit code | Timestamp ordering |
| **create-folders.sh** | 🔴 STUB | JSON files | Dirs created | Directory creation |
| **generate-c1-markdown.py** | ✅ DONE | c1-systems.json | README.md | - |
| **generate-c2-markdown.py** | ✅ DONE | c2-containers.json | *.md | - |
| **generate-c3-markdown.py** | ✅ DONE | c3-components.json | *.md | - (TODO: fix system_id) |

## Exit Code Quick Reference

```
0 = Success ✓
1 = Warning ⚠️  (proceed with caution)
2 = Error ✗ (halt workflow)
```

## Usage Examples

### Run All Validations

```bash
cd /home/user/melly

# Validate all JSON files
python plugins/melly-validation/scripts/validate-init.py init.json
python plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json
python plugins/melly-validation/scripts/validate-c2-containers.py c2-containers.json
python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json

# Check timestamps
bash plugins/melly-validation/scripts/check-timestamp.sh .

# Create folder structure
bash plugins/melly-validation/scripts/create-folders.sh .

# Generate markdown
python plugins/melly-validation/scripts/generate-c1-markdown.py c1-systems.json
python plugins/melly-validation/scripts/generate-c2-markdown.py c2-containers.json
python plugins/melly-validation/scripts/generate-c3-markdown.py c3-components.json

# Validate markdown output
python plugins/melly-validation/scripts/validate-markdown.py 'knowledge-base/systems/**/*.md'
```

### Check Exit Code in Bash

```bash
python plugins/melly-validation/scripts/validate-init.py init.json
STATUS=$?

case $STATUS in
  0) echo "✓ Validation passed" ;;
  1) echo "⚠️  Validation warnings" ;;
  2) echo "✗ Validation failed" ;;
esac
```

## What Each Validator Should Check

### validate-init.py
- JSON format valid
- Schema matches init-template.json
- metadata.schema_version == "1.0.0"
- metadata.timestamp valid ISO 8601
- metadata.generator == "melly-workflow"
- repositories array exists

### validate-c1-systems.py
- JSON format valid
- Schema matches c1-systems-template.json
- metadata.schema_version == "1.0.0"
- metadata.timestamp >= parent timestamp
- systems array exists
- Each system has: id, name, type, boundaries, repositories
- Observations have: description, category, severity
- Relations have: target, type, direction

### validate-c2-containers.py
- JSON format valid
- Schema matches c2-containers-template.json
- metadata.schema_version == "1.0.0"
- metadata.timestamp >= parent timestamp
- containers array exists
- Each container has: id, name, system_id, type, responsibility
- All system_id values exist in c1-systems.json (CROSS-FILE CHECK)
- Technology fields present and valid
- Runtime fields present and valid

### validate-c3-components.py
- JSON format valid
- Schema matches c3-components-template.json
- metadata.schema_version == "1.0.0"
- metadata.timestamp >= parent timestamp
- components array exists
- Each component has: id, name, container_id, type, responsibility
- All container_id values exist in c2-containers.json (CROSS-FILE CHECK)
- Structure fields present (path, language)
- Code structure details valid

### check-timestamp.sh
- init.json timestamp exists
- c1-systems.json timestamp >= init.json
- c2-containers.json timestamp >= c1-systems.json
- c3-components.json timestamp >= c2-containers.json
- All timestamps valid ISO 8601
- No timestamps in future (reasonable bounds)

### validate-markdown.py
- File exists and is readable
- YAML frontmatter valid (id, title, level, type, generated)
- Required sections present: Overview, Observations, Relations, Metadata
- No duplicate sections
- Heading hierarchy correct
- Code blocks properly closed
- Table formatting valid
- No broken internal links

## Execution Dependency Order

```
1. validate-init.py (must pass before continuing)
      ↓
2. validate-c1-systems.py (must pass)
      ↓
3. check-timestamp.sh (must pass)
      ↓
4. validate-c2-containers.py (must pass)
      ↓
5. validate-c3-components.py (must pass)
      ↓
6. create-folders.sh (optional, creates structure)
      ↓
7. generate-c1/c2/c3-markdown.py (can run in parallel)
      ↓
8. validate-markdown.py (must pass)
```

## Blocking vs Non-Blocking

### BLOCKING (exit 2 halts workflow):
- Invalid JSON syntax
- Missing required fields
- Cross-file reference integrity violations
- Invalid timestamps
- Broken markdown structure

### NON-BLOCKING (exit 1 allows continuation):
- Missing optional fields
- Empty arrays (no systems/containers/components)
- Timestamp drift warnings
- Missing observations/relations

## Python Dependencies

```
jsonschema>=4.17.0
pyyaml>=6.0
python-dateutil>=2.8.0
```

Install:
```bash
pip install -r plugins/melly-validation/requirements.txt
```

## Shell Dependencies

- `jq` - JSON query tool (for bash scripts)
- `date` - Standard Unix tool
- `bash` 4.0+

## Template Structures

### init.json
```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "generator": "melly-workflow",
    "timestamp": "ISO_8601_DATE"
  },
  "repositories": []
}
```

### c1-systems.json
```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "timestamp": "ISO_8601_DATE",
    "parent": { "file": "init.json", "timestamp": "..." }
  },
  "systems": [
    {
      "id": "system-id",
      "name": "System Name",
      "type": "system|microservice|service",
      "boundaries": { "scope": "..." },
      "repositories": ["repo1", "repo2"],
      "observations": [
        {
          "description": "...",
          "category": "architecture|technology|...",
          "severity": "critical|warning|info"
        }
      ],
      "relations": [
        {
          "target": "...",
          "type": "depends_on|communicates_with|...",
          "direction": "inbound|outbound|bidirectional"
        }
      ]
    }
  ]
}
```

### c2-containers.json
```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "timestamp": "ISO_8601_DATE",
    "parent": { "file": "c1-systems.json", "timestamp": "..." }
  },
  "containers": [
    {
      "id": "container-id",
      "name": "Container Name",
      "system_id": "system-id",
      "type": "web-app|api|database|...",
      "responsibility": "...",
      "technology": {
        "primary_language": "javascript|python|java|...",
        "framework": "react|fastapi|spring|...",
        "libraries": [
          { "name": "lib", "version": "1.0.0", "purpose": "..." }
        ]
      },
      "runtime": {
        "environment": "production|staging|development",
        "platform": "nodejs|python3|jvm|...",
        "containerized": true,
        "container_technology": "docker|kubernetes|..."
      }
    }
  ]
}
```

### c3-components.json
```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "timestamp": "ISO_8601_DATE",
    "parent": { "file": "c2-containers.json", "timestamp": "..." }
  },
  "components": [
    {
      "id": "component-id",
      "name": "Component Name",
      "container_id": "container-id",
      "type": "module|package|class|service|...",
      "responsibility": "...",
      "structure": {
        "path": "src/components/auth",
        "language": "javascript",
        "files": [
          { "path": "index.ts", "lines": 150, "type": "typescript" }
        ],
        "exports": [
          { "name": "AuthService", "type": "class" }
        ]
      },
      "patterns": [
        { "name": "Strategy Pattern", "category": "behavioral", "description": "..." }
      ],
      "metrics": {
        "lines_of_code": 1500,
        "cyclomatic_complexity": 8,
        "test_coverage": 85
      }
    }
  ]
}
```

## Markdown Output Structure

Generated files follow this pattern:

```markdown
---
id: component-id
title: Component Title
level: c1|c2|c3
type: system|container|component
generated: auto
---

# Component Title

## Overview
[Type, scope, responsibility information]

## Technology Stack (C2/C3 only)
[Framework, language, libraries]

## Runtime Environment (C2 only)
[Platform, containerization]

## Code Structure (C3 only)
[Path, language, files, exports]

## Design Patterns (C3 only)
[Identified patterns]

## Metrics (C3 only)
[LOC, complexity, coverage]

## Observations
[Grouped by category, sorted by severity]

## Relations
[Markdown table format]

## Metadata
[Source, level, ID, relationships]
```

## Common Errors & Solutions

### Error: "File not found: init.json"
**Solution**: Run from melly root directory or provide absolute path

### Error: "Invalid JSON syntax"
**Solution**: Validate JSON with `jq . < file.json` or online JSON validator

### Error: "System 'foo' referenced but not found"
**Solution**: Add system to c1-systems.json or fix reference in c2-containers.json

### Error: "Timestamp out of order"
**Solution**: Ensure parent timestamps are earlier than child timestamps

### Error: "No systems found in JSON" (Exit 1)
**Solution**: This is a warning - c1-systems.json array is empty (may be OK initially)

## Performance Tips

- Cache Python dependencies: `pip install --target ./venv/`
- Parallelize generation scripts (C1, C2, C3 can run simultaneously)
- Use `continue-on-error: true` in CI for non-blocking validators
- Batch validate markdown: `validate-markdown.py 'knowledge-base/**/*.md'`

## Testing

```bash
# Test single validator
python plugins/melly-validation/scripts/validate-init.py test-data/init.json

# Test with real data
python plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json && echo "✓ Pass" || echo "✗ Fail"

# Run all in sequence
bash plugins/melly-validation/scripts/run-all-validations.sh
```

## Documentation Links

- Detailed Analysis: `/home/user/melly/docs/validation-analysis.md`
- CI/CD Design: `/home/user/melly/docs/ci-cd-design.md`
- Plugin README: `/home/user/melly/plugins/melly-validation/README.md`
- CLAUDE.md: `/home/user/melly/CLAUDE.md` (section 10)

---

**Last Updated**: 2025-11-16
**Status**: Ready for implementation
**Next Step**: Start with validate-init.py
