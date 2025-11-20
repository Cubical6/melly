---
description: Identify C3-level components from containers
argument-hint: [c2-containers-json-path]
allowed-tools: Task, Read, Bash
---

Analyze containers and identify C3 components using C4 Model methodology.

## Context

- Input: $1 (default: c2-containers.json)
- Status: !`test -f ${1:-c2-containers.json} && echo "✓ exists" || echo "✗ missing"`
- Prerequisites: !`test -f init.json && test -f c1-systems.json && echo "✓ ready" || echo "✗ run /melly-init and /melly-c1-systems and /melly-c2-containers first"`

## Workflow

**1. Validate Prerequisites**

Check that init.json, c1-systems.json, and c2-containers.json exist.
If missing, inform user to run previous commands first.

**2. Launch c3-abstractor Agent**

Use Task tool to launch c3-abstractor agent:
- Input: c2-containers.json path (${1:-c2-containers.json})
- Agent will validate files, load c4model-c3 skill, analyze containers, identify components, and generate c3-components.json
- Applies C3 methodology automatically

**3. Validate and Report**

After agent completion:
```bash
python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json
```

Report:
- Components identified (count and breakdown by type/layer)
- Validation status
- Next step: /melly-doc-c4model

## Output

- **c3-components.json** - Components with observations, relations, metrics
- **Validation report** - Structure and dependency validation
