# C4 Model Relations - Detailed Reference

## Table of Contents

1. [Protocol Documentation Guidelines](#protocol-documentation-guidelines)
2. [Direction vs Coupling](#direction-vs-coupling)
3. [Best Practices per Level](#best-practices-per-level)
4. [Graph Validity Rules](#graph-validity-rules)
5. [Common Patterns](#common-patterns)

---

## Relation Type Definitions

For complete type definitions for all C4 levels, see [types.md](./types.md).

---

## Protocol Documentation Guidelines

### When to Document Protocol

**Always include protocol for:**
- C1 system-to-system communication
- C2 container-to-container communication
- External integrations
- Any network communication

**Optional for:**
- C3 code-level dependencies (unless calling external APIs)
- In-process method calls

### Protocol Format

Use standard protocol names:

**Good:**
- `HTTP/REST`
- `HTTP/2 gRPC`
- `PostgreSQL Wire Protocol`
- `AMQP`
- `OAuth 2.0`

**Bad:**
- `rest` (too vague)
- `http` (specify REST, GraphQL, etc.)
- `database` (specify PostgreSQL, MySQL, etc.)

### Protocol Details to Include

For **HTTP-based protocols:**
- HTTP version (HTTP/1.1, HTTP/2)
- API style (REST, GraphQL, RPC)
- Authentication method
- Content type (JSON, XML, etc.)

For **Database protocols:**
- Database type (PostgreSQL, MySQL, MongoDB)
- Connection method (wire protocol, ORM)
- Authentication method

For **Messaging protocols:**
- Broker type (RabbitMQ, Kafka, SQS)
- Protocol (AMQP, Kafka Protocol)
- Pattern (pub-sub, work queue)

---

## Direction vs Coupling

### Direction (C1 Level)

**Purpose:** Describes the flow of communication between systems

#### outbound
**Definition:** Source system initiates communication
**Example:** Frontend makes HTTP requests to API
**Use when:** Source actively calls, queries, or requests from target

#### inbound
**Definition:** Target system initiates communication
**Example:** External webhook calls your API
**Use when:** Target pushes data, calls back, or triggers source

#### bidirectional
**Definition:** Communication flows both ways
**Example:** WebSocket connection with messages in both directions
**Use when:** True two-way communication (avoid overusing)

**Best Practice:** Prefer outbound/inbound over bidirectional for clarity. Create two separate relations if needed.

### Coupling (C3 Level)

**Purpose:** Describes strength of dependency between components

#### loose
**Definition:** Minimal dependency, easily replaceable
**Characteristics:**
- Components interact through interfaces or abstractions
- Easy to test (can use mocks)
- Easy to swap implementations
- Changes in one component don't force changes in another

**Examples:**
- Dependency injection
- Interface-based dependencies
- Event-driven communication
- Plugin architectures

#### tight
**Definition:** Strong dependency, hard to replace
**Characteristics:**
- Direct class references
- Hard to test without real implementation
- Hard to swap implementations
- Changes cascade between components

**Examples:**
- Direct class instantiation
- Class inheritance
- Static method calls
- Global state dependencies

**Best Practice:** Prefer loose coupling. Document tight coupling as potential refactoring opportunity.

---

## Best Practices per Level

### C1 System Context Best Practices

1. **Focus on protocols**
   - Always specify communication protocol
   - Include authentication method for external relations
   - Document sync vs async nature

2. **Specify direction**
   - Use outbound for active calls (API requests, queries)
   - Use inbound for passive receives (webhooks, callbacks)
   - Avoid bidirectional unless truly necessary

3. **Document external integrations**
   - Mark external services clearly
   - Include vendor name (Stripe, SendGrid, etc.)
   - Note criticality for business operations

4. **Group similar relations**
   - One relation for "Frontend → API" covering all endpoints
   - Don't create separate relations for each API endpoint

### C2 Container Best Practices

1. **Be specific about API style**
   - Use `http-rest` not just `http`
   - Use `http-graphql` for GraphQL
   - Distinguish between REST and RPC

2. **Differentiate read vs write**
   - Use `database-query` for read-only
   - Use `database-write` for write-only
   - Use `database-read-write` for both

3. **Document cache patterns**
   - Specify cache operations (read, write, both)
   - Include eviction strategy if relevant
   - Note cache hit/miss criticality

4. **Show message patterns**
   - Use `message-publish` for producers
   - Use `message-subscribe` for consumers
   - Document topic/queue names in description

### C3 Component Best Practices

1. **Assess coupling**
   - Always include coupling field
   - Prefer loose coupling
   - Document tight coupling as technical debt

2. **Document design patterns**
   - Use `injects` for DI
   - Use `observes`/`notifies` for Observer pattern
   - Use `implements` for Strategy/Interface patterns

3. **Show dependency direction**
   - High-level → low-level (Controller → Service → Repository)
   - Abstract → concrete (Interface ← Implementation)
   - Stable → volatile

4. **Highlight circular dependencies**
   - Flag as warning in observations
   - Consider refactoring
   - Document workaround if intentional

---

## Graph Validity Rules

### Referential Integrity

**Rule:** All relation targets must reference valid entity IDs

**Validation:**
```python
# Pseudo-code
for relation in entity.relations:
    if relation.target not in valid_entity_ids:
        raise ValidationError(f"Invalid target: {relation.target}")
```

**Examples:**

✅ Valid:
```json
{
  "id": "rel-api-to-db",
  "target": "postgres-db",  // postgres-db exists in containers list
  "type": "database-read-write"
}
```

❌ Invalid:
```json
{
  "id": "rel-api-to-db",
  "target": "mysql-db",  // mysql-db doesn't exist
  "type": "database-read-write"
}
```

### No Self-References

**Rule:** Source cannot equal target

✅ Valid:
```json
{ "source": "api-service", "target": "database" }
```

❌ Invalid:
```json
{ "source": "api-service", "target": "api-service" }
```

### Cross-Level References

**Rule:** Relations can reference entities at same or different levels

**C1 → C1:** System to system ✅
**C2 → C2:** Container to container within same system ✅
**C2 → C1:** Container to external system ✅
**C3 → C3:** Component to component within same container ✅
**C3 → C2:** Component to external container ✅

### Bidirectional Relations

**Rule:** If bidirectional, both entities should document the relation

**Best Practice:** Prefer two unidirectional relations over one bidirectional

✅ Preferred:
```json
// In entity A
{ "target": "B", "type": "http-rest", "direction": "outbound" }
// In entity B
{ "target": "A", "type": "websocket", "direction": "inbound" }
```

❌ Less clear:
```json
// In entity A
{ "target": "B", "type": "http-rest", "direction": "bidirectional" }
// No corresponding relation in B
```

### Dangling References

**Rule:** All targets should eventually resolve to a documented entity

**Exceptions:**
- External systems not in your control
- Mark these clearly in description
- Use `external-api` or similar type

---

## Common Patterns

### Frontend-Backend Pattern

**C1 Level:**
```json
{
  "source": "web-application",
  "target": "backend-api",
  "type": "http-rest",
  "direction": "outbound",
  "protocol": "HTTP/REST"
}
```

**C2 Level:**
```json
{
  "source": "react-spa",
  "target": "express-api",
  "type": "http-rest",
  "protocol": "HTTP/REST",
  "isAsync": true
}
```

### API-Database Pattern

**C2 Level:**
```json
{
  "source": "express-api",
  "target": "postgres-db",
  "type": "database-read-write",
  "protocol": "PostgreSQL Wire Protocol",
  "isAsync": false
}
```

### Event-Driven Pattern

**C1 Level:**
```json
{
  "source": "order-service",
  "target": "message-queue",
  "type": "message-queue",
  "direction": "outbound",
  "protocol": "AMQP",
  "isAsync": true
}
```

**C2 Level:**
```json
{
  "source": "order-container",
  "target": "rabbitmq",
  "type": "message-publish",
  "protocol": "AMQP"
},
{
  "source": "notification-worker",
  "target": "rabbitmq",
  "type": "message-subscribe",
  "protocol": "AMQP"
}
```

### Layered Architecture Pattern (C3)

```json
{
  "source": "user-controller",
  "target": "user-service",
  "type": "uses",
  "coupling": "loose"
},
{
  "source": "user-service",
  "target": "user-repository",
  "type": "injects",
  "coupling": "loose"
}
```

### Observer Pattern (C3)

```json
{
  "source": "order-service",
  "target": "order-events",
  "type": "notifies",
  "coupling": "loose"
},
{
  "source": "payment-service",
  "target": "order-events",
  "type": "observes",
  "coupling": "loose"
}
```

---

## Validation Checklist

Before finalizing relations documentation:

- [ ] All relation IDs are unique
- [ ] All targets reference valid entity IDs
- [ ] No self-references (source ≠ target)
- [ ] Direction specified for C1 relations
- [ ] Coupling specified for C3 relations
- [ ] Protocol documented for network communication
- [ ] Descriptions in active voice
- [ ] Types match C4 level (C1 types at C1, etc.)
- [ ] isAsync set appropriately
- [ ] Tags use lowercase kebab-case
- [ ] Critical relations tagged appropriately

---

## References

- **Type Definitions:** [types.md](./types.md)
- **Examples:** [examples.md](./examples.md)
- **Main Skill:** [SKILL.md](./SKILL.md)
- **Validation Scripts:** `${CLAUDE_PLUGIN_ROOT}/validation/scripts/`
- **Schema Documentation:** `/docs/observations-relations-schema.md`

---

**Version:** 1.0.0
**Last Updated:** 2025-11-17
