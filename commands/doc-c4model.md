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
1. Detect basic-memory project root (auto-selects from ~/.basic-memory/config.json or uses fallback)
2. Validate all required JSON files exist
3. Apply C4 markdown templates
4. Generate documentation to detected project location
5. Run validation on generated files

**Agent invocation:**
```
Level: ${1:-all}
Force regenerate: false (incremental updates enabled)
Output: Auto-detected project root (see agent output for location)
```

**Project Detection:**
- Single project: Auto-selected automatically
- Multiple projects: Uses default_project from config or BASIC_MEMORY_PROJECT_ROOT env var
- No config: Falls back to ./knowledge-base in current directory

## After Completion

The agent will report:
- Project name and root path used
- Entities processed (new/modified/unchanged)
- Generated file paths
- Validation results

**Validation:**
```bash
# Validate generated markdown (if needed)
# Use the project root path reported by the agent
bash plugins/melly-validation/scripts/validate-markdown.py {project-root}/systems/**/*.md
```

**Basic-Memory Indexing (Optional):**
If you want generated files indexed in basic-memory for semantic search:
```bash
# One-time sync
basic-memory sync

# Or continuous watching (recommended)
basic-memory sync --watch
```

**Next steps:**
- Review generated documentation in the reported project root
- Optionally sync with basic-memory for searchable knowledge
- Run `/melly-draw-c4model` to create visualizations
- Commit documentation to repository

For detailed usage, see [docs/workflow-guide.md](../../../docs/workflow-guide.md)
