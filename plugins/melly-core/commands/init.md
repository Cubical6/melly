---
description: Initialize C4 model exploration by scanning repositories and generating init.json
argument-hint: [repository-path]
allowed-tools: Task, Read, Bash
---

Initialize C4 model workflow by exploring code repositories.

## Context

- Repository path: ${1:-.} (current directory if not specified)
- Existing init.json: !`test -f init.json && echo "exists (will be replaced)" || echo "not found (will be created)"`

## Workflow

Use the Task tool to launch the `explorer` agent with:
- **Input**: Repository path(s) from argument or prompt user
- **Task**: Scan repositories, analyze structure, generate init.json
- **Output**: init.json validated and ready for C1 analysis

After the explorer agent completes:
- Verify init.json exists and is valid
- Report summary (repositories found, manifests detected)
- Suggest next step: `/melly-c1-systems`

## Usage Examples

```bash
# Initialize from current directory
/melly-init

# Initialize from specific path
/melly-init /path/to/repositories

# Initialize with multiple paths (agent will prompt)
/melly-init
```

## See Also

- [C4 Methodology](../../../docs/c4model-methodology.md)
- [Workflow Guide](../../../docs/workflow-guide.md)
