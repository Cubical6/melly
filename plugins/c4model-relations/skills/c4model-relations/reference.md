# C4 Model Relations - Detailed Reference

## Table of Contents

1. [Relation Type Definitions](#relation-type-definitions)
2. [Protocol Documentation Guidelines](#protocol-documentation-guidelines)
3. [Direction vs Coupling](#direction-vs-coupling)
4. [Best Practices per Level](#best-practices-per-level)
5. [Graph Validity Rules](#graph-validity-rules)
6. [Common Patterns](#common-patterns)

---

## Relation Type Definitions

### C1 System Context Relation Types

#### http / http-rest
**Description:** HTTP/HTTPS communication, typically RESTful APIs
**Usage:** REST APIs, web requests
**Protocols:** HTTP/1.1, HTTP/2, HTTP/3
**Example:** Web application calls backend REST API

#### http-graphql
**Description:** GraphQL API communication over HTTP
**Usage:** GraphQL queries and mutations
**Protocols:** HTTP with GraphQL
**Example:** Frontend queries GraphQL API for flexible data fetching

#### grpc
**Description:** gRPC remote procedure calls
**Usage:** High-performance RPC between services
**Protocols:** HTTP/2 with gRPC
**Example:** Microservices communicate via gRPC for low latency

#### websocket
**Description:** Bidirectional real-time communication
**Usage:** Live updates, chat, notifications
**Protocols:** WebSocket Protocol
**Example:** Chat application maintains persistent connection

#### message-queue
**Description:** Asynchronous messaging via message broker
**Usage:** Event-driven architectures, async processing
**Protocols:** AMQP, Kafka, SQS, RabbitMQ
**Example:** Order service publishes events to queue for async processing

#### event-stream
**Description:** Event streaming platforms
**Usage:** Real-time data pipelines, event sourcing
**Protocols:** Kafka, Kinesis
**Example:** Analytics system consumes clickstream events

#### database-connection
**Description:** Direct database access at system level
**Usage:** System-to-database communication
**Protocols:** PostgreSQL, MySQL, MongoDB
**Example:** Application system connects to database system

#### database-query
**Description:** Read-only database access
**Usage:** Read replicas, reporting systems
**Protocols:** SQL protocols
**Example:** Analytics dashboard queries read replica

#### authentication
**Description:** Authentication and authorization flows
**Usage:** Login, SSO, OAuth flows
**Protocols:** OAuth 2.0, SAML, OIDC
**Example:** Application authenticates users via Auth0

#### external-api
**Description:** Third-party API integration
**Usage:** Payment gateways, SaaS services, external data
**Protocols:** REST, SOAP, GraphQL
**Example:** E-commerce system processes payments via Stripe API

---

### C2 Container Relation Types

#### http-rest
**Description:** RESTful HTTP API calls between containers
**Usage:** Frontend to backend, service-to-service
**Methods:** GET, POST, PUT, DELETE, PATCH
**Example:** React SPA calls Express API

#### http-graphql
**Description:** GraphQL queries between containers
**Usage:** Frontend GraphQL queries to backend
**Methods:** Query, Mutation, Subscription
**Example:** Apollo Client queries GraphQL server

#### grpc
**Description:** gRPC calls between containers
**Usage:** High-performance inter-service communication
**Example:** Backend microservices communicate via gRPC

#### websocket
**Description:** Real-time bidirectional communication
**Usage:** Live updates, real-time collaboration
**Example:** WebSocket server pushes updates to browser clients

#### database-query
**Description:** Read-only database operations
**Usage:** SELECT queries, read replicas
**Operations:** SELECT
**Example:** API container reads from PostgreSQL read replica

#### database-write
**Description:** Write-only database operations
**Usage:** INSERT, UPDATE, DELETE operations
**Operations:** INSERT, UPDATE, DELETE
**Example:** Worker container writes logs to database

#### database-read-write
**Description:** Full database access (read and write)
**Usage:** API servers, application containers
**Operations:** SELECT, INSERT, UPDATE, DELETE
**Example:** Express API reads and writes to PostgreSQL

#### cache-read
**Description:** Read-only cache access
**Usage:** Cache lookups, GET operations
**Operations:** GET, EXISTS
**Example:** API reads session data from Redis

#### cache-write
**Description:** Write-only cache operations
**Usage:** Cache updates, SET operations
**Operations:** SET, DEL
**Example:** Worker updates cache entries

#### cache-read-write
**Description:** Full cache access
**Usage:** Typical caching patterns
**Operations:** GET, SET, DEL
**Example:** API caches query results in Redis

#### message-publish
**Description:** Publishes messages to queue/topic
**Usage:** Event producers, async job creators
**Patterns:** Pub-sub, work queue
**Example:** API publishes order events to RabbitMQ

#### message-subscribe
**Description:** Consumes messages from queue/topic
**Usage:** Event consumers, background workers
**Patterns:** Pub-sub, work queue
**Example:** Worker consumes email notification jobs

#### file-read
**Description:** Reads files from storage
**Usage:** File processing, data import
**Example:** Worker reads CSV files from S3

#### file-write
**Description:** Writes files to storage
**Usage:** File generation, data export
**Example:** API uploads images to S3

#### cdn-fetch
**Description:** Fetches static assets from CDN
**Usage:** Images, scripts, stylesheets
**Example:** Browser fetches assets from CloudFront

---

### C3 Component Relation Types

#### dependency
**Description:** General dependency relationship
**Usage:** Component depends on another for functionality
**Coupling:** Varies
**Example:** Controller depends on Service

#### uses
**Description:** Uses another component's functionality
**Usage:** Service uses repository, controller uses service
**Coupling:** Loose to moderate
**Example:** UserController uses UserService

#### calls
**Description:** Invokes methods on another component
**Usage:** Direct method calls, function invocation
**Coupling:** Tight
**Example:** Service calls repository methods

#### inherits
**Description:** Class inheritance (extends)
**Usage:** OOP inheritance hierarchies
**Coupling:** Tight
**Example:** UserController extends BaseController

#### implements
**Description:** Implements an interface or contract
**Usage:** Interface implementation, polymorphism
**Coupling:** Loose
**Example:** UserRepository implements IUserRepository

#### composes
**Description:** Composition relationship (has-a)
**Usage:** Component contains another as part
**Coupling:** Tight
**Example:** Order composes OrderItem instances

#### aggregates
**Description:** Aggregation relationship (has-a, weaker)
**Usage:** Component references another
**Coupling:** Moderate
**Example:** Shopping cart aggregates products

#### imports
**Description:** Direct ES6/CommonJS import
**Usage:** Module imports
**Coupling:** Tight
**Example:** Component imports utility functions

#### injects
**Description:** Dependency injection
**Usage:** DI frameworks, constructor injection
**Coupling:** Loose
**Example:** Service receives repository via DI

#### observes
**Description:** Observer pattern - listens to events
**Usage:** Event listeners, subscribers
**Coupling:** Loose
**Example:** Logger observes error events

#### notifies
**Description:** Publishes events or notifications
**Usage:** Event emitters, publishers
**Coupling:** Loose
**Example:** Order service notifies payment service

#### delegates
**Description:** Delegates operations to another component
**Usage:** Delegation pattern
**Coupling:** Moderate
**Example:** Facade delegates to subsystems

#### extends
**Description:** Extends functionality (inheritance or mixins)
**Usage:** Class inheritance, prototype extension
**Coupling:** Tight
**Example:** CustomValidator extends Validator

#### provides
**Description:** Provides data or functionality to others
**Usage:** Provider pattern, context providers
**Coupling:** Loose
**Example:** AuthProvider provides user context

#### consumes
**Description:** Consumes data or functionality from provider
**Usage:** Consumer pattern, context consumers
**Coupling:** Loose
**Example:** Component consumes auth context

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
- **Validation Scripts:** `/plugins/melly-validation/scripts/`
- **Schema Documentation:** `/docs/observations-relations-schema.md`

---

**Version:** 1.0.0
**Last Updated:** 2025-11-17
