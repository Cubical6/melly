# Melly C2 Container Plugin

> C4 Model Level 2: Container identification and analysis

## Overview

This plugin implements the C2 (Container) level of the C4 Model workflow for the Melly marketplace. It identifies and documents deployable/runnable units (containers) within systems.

## Components

### 1. c2-abstractor Agent

**Location**: `agents/c2-abstractor.md`

**Purpose**: Analyzes repositories to identify C2-level containers (deployable units like SPAs, APIs, databases, caches, message brokers).

**Key Features**:
- Simple linear workflow (not multi-phase)
- Uses c4model-c2 skill for methodology
- Built-in tools only (Read, Grep, Glob, Bash, Write)
- Validates prerequisites before processing
- Generates structured c2-containers.json output

**Workflow**:
1. Validate prerequisites (init.json, c1-systems.json)
2. Load C4 Level 2 methodology via c4model-c2 skill
3. Analyze each system to identify containers
4. Detect technology stacks and runtime environments
5. Map communication patterns between containers
6. Generate c2-containers.json with observations and relations
7. Validate output using validation scripts
8. Report results

### 2. /melly-c2-containers Command

**Location**: `commands/melly-c2-containers.md`

**Purpose**: User-facing slash command that orchestrates the C2 container identification workflow.

**Key Features**:
- Orchestration only (delegates to c2-abstractor agent)
- Under 50 lines of core logic
- Clear prerequisite validation
- Links to detailed documentation

**Usage**:
```bash
/melly-c2-containers
```

**Prerequisites**:
- `init.json` must exist (run `/melly-init` first)
- `c1-systems.json` must exist (run `/melly-c1-systems` first)

## Output Format

### c2-containers.json Structure

```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "timestamp": "2025-11-17T23:00:00.000Z",
    "parent": {
      "file": "c1-systems.json",
      "timestamp": "2025-11-17T22:00:00.000Z"
    }
  },
  "containers": [
    {
      "id": "container-id",
      "name": "Container Name",
      "type": "spa|api|database|cache|message-broker|web-server|worker|file-storage",
      "system_id": "parent-system-id",
      "responsibility": "What this container does",
      "technology": {
        "primary_language": "TypeScript|Python|Java|...",
        "framework": "React 18.2.0|FastAPI 0.104|...",
        "libraries": [...]
      },
      "runtime": {
        "environment": "browser|server|cloud|mobile",
        "platform": "Platform description",
        "containerized": true|false,
        "container_technology": "Docker|Kubernetes|..."
      },
      "observations": [...],
      "relations": [...]
    }
  ]
}
```

## Container Types

- **SPA** - Single-Page Applications (browser)
- **API** - API servers (Node.js, Python, Java)
- **Database** - Database systems (PostgreSQL, MongoDB)
- **Cache** - Caching systems (Redis, Memcached)
- **Message Broker** - Message queues (RabbitMQ, Kafka)
- **Web Server** - Web servers, reverse proxies (Nginx, Apache)
- **Worker** - Background job processors
- **File Storage** - Object storage, file systems

## Validation

Output is validated using:
```bash
cat c2-containers.json | python plugins/melly-validation/scripts/validate-c2-containers.py
```

**Exit codes**:
- `0` - Validation passed
- `1` - Passed with warnings
- `2` - Failed with errors (blocking)

## Integration

### With Other Phases

1. **Requires**: `/melly-init` (init.json) and `/melly-c1-systems` (c1-systems.json)
2. **Provides**: c2-containers.json for `/melly-c3-components` and `/melly-doc-c4model`

### With Skills

Uses **c4model-c2 skill** for methodology:
- Container identification rules
- Technology detection patterns
- Runtime environment analysis
- Communication pattern analysis

## Best Practices

### Following Claude Code Best Practices

This implementation follows the simplified patterns outlined in TASKS.md Section 0:

✅ **Simplicity**:
- Agent: Simple linear workflow (6 steps), not multi-phase
- Command: Orchestration only, under 50 lines
- No over-engineering

✅ **Progressive Disclosure**:
- Agent uses c4model-c2 skill for detailed methodology
- Command links to comprehensive documentation
- Simple main files, detailed docs referenced

✅ **Natural Delegation**:
- Command delegates to agent via Task tool
- Agent uses skill for methodology (automatic activation)
- Validation as separate post-step (not embedded)

✅ **Built-in Tools**:
- Read, Grep, Glob, Bash, Write (no external scripts in workflow)
- Validation scripts used separately, not during agent execution

## Development Status

**Status**: ✅ COMPLETED (2025-11-17)

**Core Implementation**: Complete
- [x] c2-abstractor agent
- [x] /melly-c2-containers command
- [x] Validation integration
- [x] Documentation

**Future Enhancements**:
- [ ] Incremental processing (detect changes, process only modified systems)
- [ ] Parallel execution (run per repository concurrently)

## References

- **Methodology**: `plugins/c4model-c2/skills/c4model-c2/SKILL.md` (2,318 lines)
- **Schema**: `plugins/melly-validation/templates/c2-containers-template.json`
- **Validation**: `plugins/melly-validation/scripts/validate-c2-containers.py`
- **C4 Model Guide**: `docs/c4model-methodology.md`
- **TASKS.md**: Section 7 (Phase 3: C2 Containers)

## Installation

This plugin is part of the melly marketplace. It's automatically included when you install Melly.

## License

MIT License - See repository root for details

---

**Plugin Version**: 1.0.0
**Melly Version**: 1.0.0+
**Last Updated**: 2025-11-17
