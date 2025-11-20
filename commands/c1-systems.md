---
description: Identify C1-level systems from repositories
argument-hint: [init-json-path]
allowed-tools: Task, Read, Bash
---

Analyze repositories and identify C1 systems using C4 methodology.

## Context

- Init file: ${1:-init.json}
- Status: !`test -f "${1:-init.json}" && echo "✅ exists" || echo "❌ missing"`
- Validation: validation/scripts/

## Workflow

Use the Task tool to launch the **c1-abstractor** agent with the following requirements:

**Input**:
- Read init.json (repository paths and metadata)
- Apply C4 Level 1 methodology via c4model-c1 skill

**Process**:
- Analyze each repository for system boundaries
- Identify systems, actors, and high-level relationships
- Create system folder structure via create-folders.sh script
- Generate observations with evidence (file:line references)
- Map system relations (dependencies, communication)

**Output**:
- c1-systems.json with structure:
  - metadata (timestamp, parent reference to init.json)
  - systems[] (id, name, type, purpose, repository_path)
  - observations[] (category, content, evidence)
  - relations[] (from, to, type, protocol)

After agent completes:
- Validate output: `bash validation/scripts/validate-c1-systems.py c1-systems.json`
- Report results: systems count, next step

**Next step**: /melly-c2-containers

See [docs/workflow-guide.md](../../docs/workflow-guide.md) for detailed usage examples.
