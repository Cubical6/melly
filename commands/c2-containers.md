---
description: Identify C2-level containers (deployable units) from systems
argument-hint: [init-json-path]
allowed-tools: Task, Read, Bash
---

# Identify C2 Containers

Analyze systems and identify C2-level containers (deployable/runnable units) using C4 Model methodology.

## Context

- Init file: ${1:-init.json}
- C1 systems file: ${2:-c1-systems.json}
- Status: !`test -f ${1:-init.json} && test -f ${2:-c1-systems.json} && echo "✓ Files exist" || echo "✗ Missing files"`

## Prerequisites

Before running this command:
1. **Run /melly-init** first to generate init.json
2. **Run /melly-c1-systems** to generate c1-systems.json

## What This Command Does

1. **Validates prerequisites** - Checks init.json and c1-systems.json exist
2. **Launches c2-abstractor agent** - Applies C4 Level 2 methodology
3. **Identifies containers** - Deployable units (SPA, API, databases, caches, etc.)
4. **Detects technology stacks** - Languages, frameworks, libraries, versions
5. **Analyzes runtime environments** - Where and how containers run
6. **Maps communication** - How containers interact (REST, gRPC, database, etc.)
7. **Generates c2-containers.json** - Structured output with observations and relations
8. **Validates output** - Ensures schema compliance and referential integrity

## Workflow

Use the Task tool to launch the **c2-abstractor** agent with:
- Input: init.json, c1-systems.json
- Methodology: c4model-c2 skill (automatic activation)
- Output: c2-containers.json

After agent completes:
- Validate: `cat c2-containers.json | python ${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-c2-containers.py`
- Report results summary
- Suggest next step: `/melly-c3-components` or `/melly-doc-c4model`

## Next Steps

After successful completion:
- **Option 1**: Run `/melly-c3-components` to analyze component structure
- **Option 2**: Run `/melly-doc-c4model` to generate documentation
- **Option 3**: Manually inspect `c2-containers.json` for accuracy

## Troubleshooting

- **Missing init.json**: Run `/melly-init` first
- **Missing c1-systems.json**: Run `/melly-c1-systems` first
- **Validation fails**: Check error messages, fix issues in c2-containers.json
- **Timestamp errors**: Ensure c2 timestamp > c1 timestamp > init timestamp

## Documentation

For details on C4 Level 2 methodology:
- **Methodology**: See `plugins/c4model-c2/skills/c4model-c2/SKILL.md`
- **Schema**: See `${CLAUDE_PLUGIN_ROOT}/validation/templates/c2-containers-template.json`
- **Validation**: See `${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-c2-containers.py`
- **Workflow**: See `docs/c4model-methodology.md`

---

**C2 Level Focus**: Deployable units, technology stacks, runtime environments, communication patterns
