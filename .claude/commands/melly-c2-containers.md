---
description: Identify C2-level containers from systems
argument-hint: [init-json-path]
allowed-tools: Task, Read, Bash
---

Analyze C1 systems and identify C2 containers (technology boundaries).

## Context

- Init file: $1 (or init.json if not specified)
- Init status: !`test -f ${1:-init.json} && echo "✅ exists" || echo "❌ missing"`
- C1 systems: !`test -f c1-systems.json && echo "✅ exists" || echo "❌ missing - run /melly-c1-systems first"`

## Prerequisites

This command requires:
1. `init.json` - Run `/melly-init` first if missing
2. `c1-systems.json` - Run `/melly-c1-systems` first if missing

## Workflow

Use the Task tool to launch c2-abstractor agent to:
1. Read init.json and c1-systems.json
2. Validate timestamp ordering (c1 > init)
3. Apply C2 methodology (via c4model-c2 skill)
4. Identify containers per system (technology boundaries)
5. Generate c2-containers.json

After agent completes:
- Validate: `bash plugins/melly-validation/scripts/validate-c2-containers.py c2-containers.json`
- Report results: systems analyzed, containers found, validation status
- Suggest next step: `/melly-c3-components`

## Error Handling

If validation fails:
- Review error messages from validate-c2-containers.py
- Check c2-containers.json structure
- Verify all system references are valid
- Re-run command after fixes

See [docs/workflow-guide.md](../../docs/workflow-guide.md) for detailed usage.
