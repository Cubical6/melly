---
description: Generate C4 model markdown documentation from JSON files
argument-hint: [level]
allowed-tools: Task, Read, Bash
---

Generate structured markdown documentation from C4 model JSON files.

## Context

- Level: $1 (or "all" if not specified)
- JSON files status: !`test -f init.json && test -f c1-systems.json && test -f c2-containers.json && test -f c3-components.json && echo "✓ All present" || echo "✗ Missing files"`
- Last generation: !`test -f .melly-doc-metadata.json && jq -r '.last_generation' .melly-doc-metadata.json || echo "Never"`

## Workflow

Use the Task tool to launch the c4model-writer agent to:
1. Validate all required JSON files exist
2. Apply C4 markdown templates
3. Generate documentation via basic-memory MCP
4. Run validation on generated files

**Agent invocation:**
```
Level: ${1:-all}
Force regenerate: false (incremental updates enabled)
Output: knowledge-base/systems/
```

## After Completion

The agent will report:
- Entities processed (new/modified/unchanged)
- Generated file paths
- Validation results

**Validation:**
```bash
# Validate generated markdown (if needed)
bash ${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-markdown.py knowledge-base/systems/**/*.md
```

**Next steps:**
- Review generated documentation in knowledge-base/
- Run `/melly-draw-c4model` to create visualizations
- Commit documentation to repository

For detailed usage, see [docs/workflow-guide.md](../../../docs/workflow-guide.md)
