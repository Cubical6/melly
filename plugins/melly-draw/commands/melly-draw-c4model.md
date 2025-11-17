---
description: Generate C4 model diagrams (Mermaid + Obsidian canvas) from JSON files
argument-hint: [level]  # c1, c2, c3, or all
allowed-tools: Task, Read, Bash
---

Generate visual diagrams from C4 model JSON files.

## Context

Level: $1 (default: all)
Available levels: c1 (systems), c2 (containers), c3 (components), all

## Prerequisites

Check JSON files:
- init.json: !`test -f init.json && echo "✅ exists" || echo "❌ missing"`
- c1-systems.json: !`test -f c1-systems.json && echo "✅ exists" || echo "❌ missing"`
- c2-containers.json: !`test -f c2-containers.json && echo "✅ exists" || echo "❌ missing"`
- c3-components.json: !`test -f c3-components.json && echo "✅ exists" || echo "❌ missing"`

## Workflow

1. **Validate Input**
   - Level: ${1:-all}
   - If level specified, check corresponding JSON exists
   - If "all", check all JSON files exist

2. **Launch c4model-drawer Agent**
   - Use Task tool to invoke c4model-drawer agent
   - Pass level parameter: ${1:-all}
   - Agent will:
     - Parse JSON files
     - Generate Mermaid diagrams
     - Create Obsidian canvas files
     - Save to knowledge-base/systems/*/diagrams/

3. **Report Results**
   - List generated diagram files
   - Show statistics (entities, relations)
   - Display any errors or warnings

## Output

Generated files:
- Mermaid diagrams: `knowledge-base/systems/{system}/diagrams/c{1,2,3}-*.md`
- Canvas files: `knowledge-base/systems/{system}/diagrams/c{1,2,3}-*.canvas`

## Next Steps

After generation:
- Open diagrams in Obsidian for visualization
- Review system architecture visually
- Share diagrams with team
- Export to PNG/SVG if needed

## Examples

```bash
# Generate all diagrams
/melly-draw-c4model all

# Generate only C1 system context
/melly-draw-c4model c1

# Generate C2 containers
/melly-draw-c4model c2

# Generate C3 components
/melly-draw-c4model c3
```
