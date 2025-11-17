---
name: c4model-relations
description: Use when documenting relations, dependencies, and communications between systems, containers, or components in C4 Model architecture. Invoke during dependency mapping, integration analysis, or when users mention "relations", "dependencies", "connections", "how systems communicate", "API calls", "integrations", "data flow", or need to understand inter-system/component relationships. Essential for understanding architectural communication patterns across C1, C2, and C3 levels.
---

# C4 Model - Relations Documentation Methodology

## Overview

This skill provides methodology for identifying, categorizing, and documenting relations (dependencies and communications) across all three C4 Model levels.

**Mission:** Document HOW systems, containers, and components communicate—what flows between them, in which direction, and through which protocols.

---

## What is a Relation?

A **relation** represents communication, dependency, or data flow between two entities:

- **C1 Relations** - Communication between systems (e.g., Web App → API)
- **C2 Relations** - Communication between containers (e.g., SPA → Backend, API → Database)
- **C3 Relations** - Dependencies between components (e.g., Controller → Service)

---

## Relation Structure

### Required Fields

```json
{
  "id": "rel-frontend-to-api",           // Unique identifier
  "target": "backend-api",               // Target entity ID
  "type": "http-rest",                   // Relation type (level-specific)
  "description": "Sends HTTP requests to fetch user data"  // Active voice
}
```

### Optional Fields

- `protocol` - Communication protocol (C1, C2)
- `direction` - C1 only: outbound, inbound, bidirectional
- `coupling` - C3 only: loose or tight
- `isAsync` - Synchronous or asynchronous
- `tags` - Tags for categorization

**Note:** Source is implied by context (the entity containing this relation).

---

## Relation Types by C4 Level

### C1: System Context

**Common Types:** `http-rest`, `http-graphql`, `grpc`, `websocket`, `message-queue`, `database-connection`, `authentication`, `external-api`

**Key Fields:** `direction` (outbound/inbound/bidirectional), `protocol`

### C2: Container

**Common Types:** `http-rest`, `database-read-write`, `cache-read-write`, `message-publish`, `message-subscribe`

**Key Fields:** `protocol`, `isAsync`

### C3: Component

**Common Types:** `dependency`, `uses`, `calls`, `inherits`, `implements`, `injects`, `observes`, `notifies`

**Key Fields:** `coupling` (loose/tight)

**Complete type definitions** → [types.md](./types.md)

---

## Direction and Coupling

### Direction (C1 Only)

- **`outbound`** - Source initiates (Frontend calls API)
- **`inbound`** - Target initiates (Webhook from external)
- **`bidirectional`** - Both directions (WebSocket)

**Prefer outbound/inbound over bidirectional.**

### Coupling (C3 Only)

- **`loose`** - Minimal dependency, easily replaceable (DI, interfaces)
- **`tight`** - Strong dependency, hard to replace (inheritance, direct refs)

**Prefer loose coupling.**

---

## Writing Descriptions

### Rules

1. **Active voice** - Subject performs action
2. **Start with verb** - Sends, Fetches, Reads, Writes
3. **Be specific** - What data? What purpose?
4. **Keep concise** - 1-2 sentences max

### Examples

✅ "Sends HTTP requests to fetch user profile and order history"
✅ "Reads customer records from PostgreSQL for order processing"
✅ "Injects UserRepository via dependency injection"

❌ "Talks to the API" (too vague)
❌ "Data is sent" (passive voice)
❌ "Connection" (not descriptive)

---

## Quick Examples

### C1 Example

```json
{
  "id": "rel-webapp-to-api",
  "target": "backend-api",
  "type": "http-rest",
  "description": "Sends HTTP requests to fetch and update customer data",
  "protocol": "HTTP/REST",
  "direction": "outbound",
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
  "tags": ["database", "postgres"]
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
  "tags": ["service-layer"]
}
```

**45+ comprehensive examples** → [examples.md](./examples.md)

---

## Common Protocols

**HTTP:** `HTTP/REST`, `HTTP/GraphQL`, `HTTP/2 gRPC`
**Database:** `PostgreSQL Wire Protocol`, `MySQL Wire Protocol`
**Messaging:** `AMQP`, `Kafka Protocol`, `MQTT`
**Other:** `WebSocket`, `Redis Protocol (RESP)`, `OAuth 2.0`

---

## Integration with Melly Workflow

### When Used

- **C1 Analysis** (`/melly-c1-systems`) - System relations
- **C2 Analysis** (`/melly-c2-containers`) - Container relations
- **C3 Analysis** (`/melly-c3-components`) - Component relations
- **Documentation** (`/melly-doc-c4model`) - Markdown generation

### Output Location

- `c1-systems.json` - `systems[].relations[]`
- `c2-containers.json` - `containers[].relations[]`
- `c3-components.json` - `components[].relations[]`

### Validation

```bash
python plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json
python plugins/melly-validation/scripts/validate-c2-containers.py c2-containers.json
python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json
```

---

## Best Practices

### ✅ DO

- Use specific types (`http-rest` not `http`)
- Write active descriptions (start with verbs)
- Specify direction for C1 (prefer outbound/inbound)
- Include protocol for network communication
- Assess coupling for C3 (loose/tight)
- Validate targets (ensure entity exists)

### ❌ DON'T

- Use passive voice (❌ "Data is sent" → ✅ "Sends data")
- Use generic types (❌ `http` → ✅ `http-rest`)
- Skip direction (C1) or coupling (C3)
- Create invalid targets
- Mix abstraction levels

---

## Detailed Documentation

- **Relation Types** → [types.md](./types.md) - Complete type definitions
- **Detailed Reference** → [reference.md](./reference.md) - Methodology and best practices
- **Comprehensive Examples** → [examples.md](./examples.md) - 45+ real-world examples

---

## Summary

When documenting relations:

1. **Identify communication** - How do entities interact?
2. **Choose appropriate type** - Based on C4 level and mechanism
3. **Specify direction** - For C1 (outbound/inbound/bidirectional)
4. **Document protocol** - For network communication
5. **Assess coupling** - For C3 (loose/tight)
6. **Write clear descriptions** - Active voice, specific, concise
7. **Validate output** - Ensure referential integrity

**Focus on:** WHAT flows, in WHICH direction, through WHICH protocol.

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-11-17
**Compatibility**: Melly 1.0.0+
