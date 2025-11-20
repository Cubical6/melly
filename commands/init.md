---
description: Initialize C4 model exploration - scan repositories and generate init.json
argument-hint: [repository-path]
allowed-tools: Task, Read, Write, Bash
---

Initialize C4 model exploration by scanning repositories and generating init.json.

## Context

- Repository path: ${1:-.} (current directory if not specified)
- Repository exists: !`test -d "${1:-.}" && echo "yes" || echo "no"`
- Existing init.json: !`test -f init.json && echo "found ($(stat -c%y init.json | cut -d' ' -f1))" || echo "none"`

## Workflow

Use the Task tool to launch the c4model-explorer agent with:
- Repository root path: ${1:-.}
- Output file: init.json

The agent will:
1. Scan all repositories in the specified location
2. Identify package manifests and technology stacks
3. Generate init.json with metadata and structure

After agent completes:
- Validate output: `python3 ${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-init.py < init.json`
- Review init.json for accuracy
- Suggest next step: /melly-c1-systems

## Notes

See [docs/workflow-guide.md](../../../docs/workflow-guide.md) for detailed usage examples.
