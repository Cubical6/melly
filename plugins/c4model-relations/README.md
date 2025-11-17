# c4model-relations

> C4 Model relation documentation methodology for dependencies and communications across system, container, and component levels

## Overview

The `c4model-relations` skill provides comprehensive methodology for identifying, categorizing, and documenting relations (dependencies and communications) across all three C4 Model levels:

- **C1 System Context** - Communication between systems
- **C2 Container Level** - Communication between containers
- **C3 Component Level** - Dependencies between components

## Features

- ✅ **Comprehensive Type Definitions** - Complete relation type taxonomy for C1, C2, C3
- ✅ **Protocol Documentation** - Guidelines for documenting communication protocols
- ✅ **Direction and Coupling** - Clear guidance on direction (C1) and coupling (C3)
- ✅ **Rich Examples** - 45+ real-world examples across all levels
- ✅ **Validation Support** - Integration with Melly validation scripts
- ✅ **Progressive Disclosure** - SKILL.md (concise) → reference.md (detailed)

## Installation

### Via CLI

```bash
cd /path/to/your/project
/plugin add ./plugins/c4model-relations
```

### Manual Installation

Copy the plugin directory to your project:

```bash
cp -r plugins/c4model-relations /path/to/your/project/.claude-plugins/
```

## Usage

### Automatic Activation

Claude automatically activates this skill when you:

- Mention "relations", "dependencies", or "connections"
- Ask about "how systems communicate"
- Need to document "API calls" or "integrations"
- Work with "data flow" between components
- Use commands: `/melly-c1-systems`, `/melly-c2-containers`, `/melly-c3-components`

### Manual Activation

Ask Claude explicitly:

```
> Use the c4model-relations skill to help me document the communication between these systems
> How should I document the relation between the API and the database?
> What relation type should I use for a GraphQL API?
```

## Skill Structure

```
skills/c4model-relations/
├── SKILL.md           # Main skill (150 lines) - Quick reference
├── reference.md       # Detailed methodology and best practices
├── examples.md        # 45+ comprehensive examples
└── types.md          # Complete relation type definitions
```

### SKILL.md

**Content:**
- Overview of what relations are
- Relation structure (required/optional fields)
- Relation types by C4 level (C1, C2, C3)
- Direction and coupling concepts
- Protocol documentation guidelines
- Quick examples for each level
- Integration with Melly workflow

**When to use:** Quick reference, understanding basics

### reference.md

**Content:**
- Detailed relation type definitions
- Protocol documentation guidelines
- Direction vs coupling explanation
- Best practices per level (C1, C2, C3)
- Graph validity rules
- Common architectural patterns

**When to use:** Detailed methodology, best practices, validation rules

### examples.md

**Content:**
- 12+ C1 System Context examples
- 12+ C2 Container examples
- 15+ C3 Component examples
- Cross-level examples
- Each example includes complete metadata

**When to use:** Real-world reference, templates for your own relations

### types.md

**Content:**
- Complete C1 relation type definitions
- Complete C2 relation type definitions
- Complete C3 relation type definitions
- Type selection guidelines
- Usage patterns per level

**When to use:** Choosing the right relation type, understanding type differences

## Relation Types Overview

### C1 System Context Types

Communication protocols between systems:

- `http-rest` - RESTful HTTP APIs
- `http-graphql` - GraphQL APIs
- `grpc` - gRPC remote procedure calls
- `websocket` - WebSocket connections
- `message-queue` - Async messaging (AMQP, Kafka, SQS)
- `database-connection` - System to database access
- `authentication` - Auth flows (OAuth, SAML)
- `external-api` - Third-party integrations

**Key Fields:** `direction`, `protocol`

### C2 Container Types

Container-to-container communication:

- `http-rest`, `http-graphql` - API calls
- `database-read-write`, `database-query` - Database operations
- `cache-read-write`, `cache-read`, `cache-write` - Cache access
- `message-publish`, `message-subscribe` - Message queue patterns
- `file-read`, `file-write` - File storage operations
- `websocket` - Real-time communication

**Key Fields:** `protocol`, `isAsync`

### C3 Component Types

Code-level dependencies and patterns:

- `dependency`, `uses`, `calls` - General dependencies
- `inherits`, `implements`, `extends` - OOP patterns
- `composes`, `aggregates` - Composition patterns
- `injects`, `provides`, `consumes` - DI patterns
- `observes`, `notifies` - Event patterns
- `imports`, `delegates` - Module patterns

**Key Fields:** `coupling` (loose/tight)

## Quick Examples

### C1 Example

```json
{
  "id": "rel-webapp-to-api",
  "target": "backend-api",
  "type": "http-rest",
  "description": "Sends HTTP requests to fetch customer data",
  "protocol": "HTTP/REST",
  "direction": "outbound",
  "isAsync": true,
  "tags": ["api", "rest", "critical"]
}
```

### C2 Example

```json
{
  "id": "rel-api-to-postgres",
  "target": "postgres-db",
  "type": "database-read-write",
  "description": "Reads and writes application data using Sequelize ORM",
  "protocol": "PostgreSQL Wire Protocol",
  "isAsync": false,
  "tags": ["database", "postgres", "orm"]
}
```

### C3 Example

```json
{
  "id": "rel-controller-to-service",
  "target": "user-service",
  "type": "uses",
  "description": "Delegates business logic operations to UserService",
  "coupling": "loose",
  "tags": ["service-layer", "delegation"]
}
```

## Integration with Melly Workflow

### Workflow Phases

This skill is used during:

1. **C1 Analysis** (`/melly-c1-systems`) - Document system-to-system relations
2. **C2 Analysis** (`/melly-c2-containers`) - Document container-to-container relations
3. **C3 Analysis** (`/melly-c3-components`) - Document component-to-component relations
4. **Documentation** (`/melly-doc-c4model`) - Convert relations to markdown

### Output Files

Relations are stored in:
- `c1-systems.json` - Within each system's `relations` array
- `c2-containers.json` - Within each container's `relations` array
- `c3-components.json` - Within each component's `relations` array

### Validation

Validate relations using Melly validation scripts:

```bash
python plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json
python plugins/melly-validation/scripts/validate-c2-containers.py c2-containers.json
python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json
```

## Best Practices

### Writing Descriptions

✅ **DO:**
- Use active voice: "Sends HTTP requests to fetch user data"
- Start with verbs: Sends, Fetches, Reads, Writes, Depends on
- Be specific: What data? What purpose?
- Keep concise: 1-2 sentences max

❌ **DON'T:**
- Use passive voice: ❌ "Data is sent"
- Use vague terms: ❌ "Connection" or "Uses it"
- Skip purpose: ❌ "Talks to the API"

### Choosing Types

✅ **DO:**
- Use specific types: `http-rest` instead of `http`
- Match type to level: C1 types at C1, etc.
- Include protocol for network communication
- Specify direction for C1 (outbound/inbound/bidirectional)
- Assess coupling for C3 (loose/tight)

❌ **DON'T:**
- Use generic types when specific ones exist
- Mix abstraction levels
- Skip direction or coupling fields
- Create invalid target references

## Troubleshooting

### Skill Not Activating

**Problem:** Claude doesn't automatically use the skill

**Solution:**
- Check plugin is installed: `/plugins`
- Use explicit keywords: "relations", "dependencies", "how systems communicate"
- Invoke manually: "Use the c4model-relations skill..."

### Choosing Relation Type

**Problem:** Unsure which type to use

**Solution:**
- Check [types.md](./skills/c4model-relations/types.md) for complete definitions
- Review [examples.md](./skills/c4model-relations/examples.md) for similar cases
- Follow level-specific guidelines in [reference.md](./skills/c4model-relations/reference.md)

### Validation Errors

**Problem:** Relations fail validation

**Solution:**
- Ensure target entity exists
- Check type matches C4 level
- Verify direction (C1) or coupling (C3) is set
- Validate ID format: `^rel-[a-z0-9-]+$`
- Check description is active voice

## Related Skills

- **c4model-c1** - C1 System Context analysis methodology
- **c4model-c2** - C2 Container analysis methodology
- **c4model-c3** - C3 Component analysis methodology
- **c4model-observations** - Observation documentation methodology

## Contributing

Found an issue or have a suggestion? Please open an issue on GitHub:

https://github.com/Cubical6/melly/issues

## License

MIT

---

**Version:** 1.0.0
**Author:** Melly Team
**Last Updated:** 2025-11-17
