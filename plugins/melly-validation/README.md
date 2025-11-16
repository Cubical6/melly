# Melly Validation Plugin

Centralized validation scripts and templates for the Melly C4 model workflow.

## Architecture Decision

**Approach**: AI → JSON → Script → Markdown

This ensures **consistency** in documentation structure by using deterministic
scripts instead of AI-based markdown generation, preventing issues like:
- Duplicate sections
- Inconsistent ordering
- Random formatting variations

## Structure

- `scripts/` - Validation and generation scripts (10 scripts)
- `templates/` - JSON structure templates (4 templates)

## Scripts

### Validation Scripts (7)

**Exit Code Convention:**
- 0: Validation passed
- 1: Non-blocking warning
- 2: Blocking error

Scripts:
- `validate-init.py` - Validates init.json structure
- `validate-c1-systems.py` - Validates c1-systems.json
- `validate-c2-containers.py` - Validates c2-containers.json
- `validate-c3-components.py` - Validates c3-components.json
- `validate-markdown.py` - Validates generated markdown
- `create-folders.sh` - Creates system directory structure
- `check-timestamp.sh` - Validates timestamp ordering

### Generation Scripts (3)

Deterministic markdown generation from JSON:
- `generate-c1-markdown.py` - C1 System Context → Markdown
- `generate-c2-markdown.py` - C2 Containers → Markdown
- `generate-c3-markdown.py` - C3 Components → Markdown

**Features:**
- ALWAYS generates same structure (no duplicates)
- Observations grouped by category, sorted by severity
- Relations in consistent table format
- Technology stack sections (C2/C3)
- Code structure sections (C3)

## Templates

JSON structure templates (used by AI agents as reference):
- `init-template.json` - Repository exploration structure
- `c1-systems-template.json` - System context structure
- `c2-containers-template.json` - Container structure
- `c3-components-template.json` - Component structure

## Workflow

```
1. AI Agent → Generates/updates JSON file (e.g., c1-systems.json)
2. Validation Script → Validates JSON structure
3. Generation Script → Converts JSON to Markdown (deterministic)
4. Validation Script → Validates Markdown output
```

**Example:**
```bash
# AI generates JSON
/melly-c1-systems

# Validate JSON
python scripts/validate-c1-systems.py c1-systems.json

# Generate Markdown (consistent output)
python scripts/generate-c1-markdown.py c1-systems.json

# Validate Markdown
python scripts/validate-markdown.py knowledge-base/systems/*/c1/*.md
```
