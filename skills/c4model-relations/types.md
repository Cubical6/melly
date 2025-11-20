# C4 Model Relation Types - Complete Reference

## Overview

This document provides comprehensive definitions for all relation types across C1, C2, and C3 levels of the C4 Model.

**Usage:** Reference this document when choosing the appropriate relation type for your architecture documentation.

---

## Table of Contents

1. [C1 System Context Relation Types](#c1-system-context-relation-types)
2. [C2 Container Relation Types](#c2-container-relation-types)
3. [C3 Component Relation Types](#c3-component-relation-types)
4. [Type Selection Guidelines](#type-selection-guidelines)

---

## C1 System Context Relation Types

### Network Communication Types

#### http / https / http-rest
**Description:** HTTP/HTTPS communication, typically RESTful APIs
**When to use:** REST APIs, web requests, standard HTTP communication
**Protocols:** HTTP/1.1, HTTP/2, HTTP/3
**Direction:** Usually outbound (client calls server)
**Example:** Web application calls backend REST API for data

#### http-graphql
**Description:** GraphQL API communication over HTTP
**When to use:** GraphQL queries and mutations
**Protocols:** HTTP with GraphQL
**Direction:** Usually outbound (client queries server)
**Example:** Frontend queries GraphQL API for flexible data fetching

#### grpc
**Description:** gRPC remote procedure calls
**When to use:** High-performance RPC, microservice communication
**Protocols:** HTTP/2 with Protocol Buffers
**Direction:** Usually outbound (client calls service)
**Example:** Microservices communicate via gRPC for low latency

#### graphql
**Description:** GraphQL protocol (alternative to http-graphql)
**When to use:** When emphasizing GraphQL over HTTP transport
**Example:** Same as http-graphql

#### websocket
**Description:** Bidirectional real-time communication
**When to use:** Live updates, chat, real-time notifications
**Protocols:** WebSocket Protocol (RFC 6455)
**Direction:** Bidirectional
**Example:** Chat application maintains persistent WebSocket connection

#### rpc
**Description:** Generic remote procedure call
**When to use:** Custom RPC protocols, legacy RPC systems
**Example:** XML-RPC, JSON-RPC communication

#### soap
**Description:** SOAP web services
**When to use:** Enterprise integrations, legacy systems
**Protocols:** SOAP over HTTP
**Example:** Integration with enterprise ERP system

### Messaging Types

#### message-queue
**Description:** Asynchronous messaging via message broker
**When to use:** Event-driven architectures, async processing, decoupled systems
**Protocols:** AMQP, Kafka Protocol, SQS API
**Direction:** Outbound (publish) or Inbound (consume)
**Example:** Order service publishes events to RabbitMQ for async processing

#### event-stream
**Description:** Event streaming platforms
**When to use:** Real-time data pipelines, event sourcing, log aggregation
**Protocols:** Kafka, Amazon Kinesis, Azure Event Hubs
**Example:** Analytics system consumes clickstream events from Kafka

### Data Access Types

#### database-connection
**Description:** Direct database access at system level
**When to use:** System-to-database communication, primary database
**Protocols:** PostgreSQL, MySQL, MongoDB protocols
**Direction:** Outbound (system queries database)
**Example:** Application system connects to PostgreSQL database

#### database-query
**Description:** Read-only database access
**When to use:** Read replicas, reporting systems, analytics
**Protocols:** SQL protocols (SELECT only)
**Direction:** Outbound
**Example:** Analytics dashboard queries PostgreSQL read replica

### Integration Types

#### authentication
**Description:** Authentication and authorization flows
**When to use:** Login flows, SSO, OAuth integrations
**Protocols:** OAuth 2.0, SAML, OpenID Connect
**Direction:** Outbound (system authenticates with provider)
**Example:** Web application authenticates users via Auth0

#### external-api
**Description:** Third-party API integration
**When to use:** Payment gateways, SaaS services, external data providers
**Protocols:** REST, SOAP, GraphQL, proprietary
**Direction:** Outbound (your system calls external API)
**Example:** E-commerce system processes payments via Stripe API

### Other Types

#### file-transfer
**Description:** File transfer protocols
**When to use:** File uploads, downloads, FTP, SFTP
**Protocols:** FTP, SFTP, SCP, HTTP multipart
**Example:** Backup system transfers files to remote storage via SFTP

#### smtp
**Description:** Email protocol
**When to use:** Email sending
**Protocols:** SMTP
**Example:** System sends transactional emails via SMTP

---

## C2 Container Relation Types

### API Communication Types

#### http-rest
**Description:** RESTful HTTP API calls between containers
**When to use:** Frontend to backend, service-to-service REST communication
**Methods:** GET, POST, PUT, DELETE, PATCH
**Typical containers:** SPA → API, API → Microservice
**Example:** React SPA calls Express API endpoints

#### http-graphql
**Description:** GraphQL queries between containers
**When to use:** Frontend GraphQL queries, flexible data fetching
**Methods:** Query, Mutation, Subscription
**Typical containers:** Apollo Client → GraphQL Server
**Example:** Next.js app queries GraphQL API

#### grpc
**Description:** gRPC calls between containers
**When to use:** High-performance inter-service communication
**Typical containers:** Microservice → Microservice
**Example:** Order service calls Inventory service via gRPC

#### websocket
**Description:** Real-time bidirectional communication
**When to use:** Live updates, real-time collaboration, push notifications
**Typical containers:** Browser → WebSocket Server
**Example:** Chat client maintains WebSocket connection to server

### Database Access Types

#### database-query
**Description:** Read-only database operations
**When to use:** SELECT queries, read replicas, reporting
**Operations:** SELECT
**Typical containers:** API → Read Replica, Analytics → Database
**Example:** API container reads user data from PostgreSQL read replica

#### database-write
**Description:** Write-only database operations
**When to use:** INSERT, UPDATE, DELETE operations, write-specific workers
**Operations:** INSERT, UPDATE, DELETE
**Typical containers:** Worker → Database
**Example:** Log aggregator writes logs to database

#### database-read-write
**Description:** Full database access (read and write)
**When to use:** Primary API servers, application logic containers
**Operations:** SELECT, INSERT, UPDATE, DELETE
**Typical containers:** API → Primary Database
**Example:** Express API reads and writes to PostgreSQL primary

#### database-connection
**Description:** Generic database connection (use specific types above when possible)
**When to use:** When access pattern is unclear or mixed
**Example:** General database connectivity

### Cache Access Types

#### cache-read
**Description:** Read-only cache access
**When to use:** Cache lookups, GET operations
**Operations:** GET, EXISTS, TTL
**Typical containers:** API → Cache
**Example:** API reads session data from Redis

#### cache-write
**Description:** Write-only cache operations
**When to use:** Cache updates, background cache warmers
**Operations:** SET, SETEX, DEL
**Typical containers:** Worker → Cache
**Example:** Cache warmer updates frequently accessed data in Redis

#### cache-read-write
**Description:** Full cache access
**When to use:** Typical caching patterns, read-through/write-through
**Operations:** GET, SET, DEL, INCR, DECR
**Typical containers:** API → Redis
**Example:** API caches database query results in Redis

#### cache-access
**Description:** Generic cache access (use specific types above when possible)
**When to use:** When access pattern is unclear
**Example:** General cache connectivity

### Message Queue Types

#### message-publish
**Description:** Publishes messages to queue or topic
**When to use:** Event producers, async job creators
**Patterns:** Pub-sub, work queue
**Typical containers:** API → Queue, Service → Event Bus
**Example:** Order API publishes order-created events to RabbitMQ

#### message-subscribe / message-consumer
**Description:** Consumes messages from queue or topic
**When to use:** Event consumers, background workers
**Patterns:** Pub-sub, work queue
**Typical containers:** Worker → Queue
**Example:** Email worker consumes notification jobs from SQS
**Note:** `message-consumer` is an alias for `message-subscribe`

### Storage Types

#### file-read
**Description:** Reads files from storage system
**When to use:** File processing, data import, asset loading
**Typical containers:** Worker → S3, API → File Storage
**Example:** Image processor reads uploaded files from S3

#### file-write
**Description:** Writes files to storage system
**When to use:** File uploads, data export, log writing
**Typical containers:** API → S3, Worker → File Storage
**Example:** API uploads user profile images to S3

#### cdn-fetch
**Description:** Fetches static assets from CDN
**When to use:** Asset delivery, static resource loading
**Typical containers:** Browser → CDN
**Example:** Web app fetches CSS/JS/images from CloudFront

### Other Types

#### stream
**Description:** Streaming data transfer
**When to use:** Video/audio streaming, large file transfers
**Example:** Video player streams content from media server

---

## C3 Component Relation Types

### Dependency Types

#### dependency
**Description:** General dependency relationship
**When to use:** Component depends on another for functionality
**Coupling:** Varies (document as loose or tight)
**Typical usage:** Any component dependency
**Example:** Controller depends on Service for business logic

#### uses
**Description:** Uses another component's functionality
**When to use:** Component actively uses another's methods or features
**Coupling:** Loose to moderate
**Typical usage:** Service uses Repository, Controller uses Service
**Example:** UserController uses UserService for user operations

#### calls
**Description:** Directly invokes methods on another component
**When to use:** Direct method calls, function invocation
**Coupling:** Tight
**Typical usage:** Any direct method invocation
**Example:** Service calls specific repository methods

### Object-Oriented Types

#### inherits / extends
**Description:** Class inheritance (is-a relationship)
**When to use:** OOP inheritance hierarchies
**Coupling:** Tight
**Typical usage:** Class extends base class
**Example:** UserController extends BaseController
**Note:** Both `inherits` and `extends` are valid

#### implements / interface-implementation
**Description:** Implements an interface or contract
**When to use:** Interface implementation, polymorphism
**Coupling:** Loose
**Typical usage:** Class implements interface
**Example:** UserRepository implements IUserRepository
**Note:** Both `implements` and `interface-implementation` are valid

#### composes
**Description:** Composition relationship (has-a, strong)
**When to use:** Component contains another as integral part
**Coupling:** Tight
**Typical usage:** Object composition
**Example:** Order composes OrderItem instances

#### aggregates
**Description:** Aggregation relationship (has-a, weak)
**When to use:** Component references another but doesn't own it
**Coupling:** Moderate
**Typical usage:** Object aggregation
**Example:** ShoppingCart aggregates Product references

### Dependency Injection Types

#### injects
**Description:** Dependency injection
**When to use:** DI frameworks, constructor/setter injection
**Coupling:** Loose
**Typical usage:** Service receives dependencies via DI container
**Example:** UserService receives UserRepository via constructor injection

#### provides
**Description:** Provides data or functionality to consumers
**When to use:** Provider pattern, dependency providers
**Coupling:** Loose
**Typical usage:** DI providers, context providers
**Example:** AuthProvider provides authenticated user context

#### consumes
**Description:** Consumes data or functionality from provider
**When to use:** Consumer pattern, dependency consumers
**Coupling:** Loose
**Typical usage:** Component consumes from provider
**Example:** UserProfile consumes auth context from AuthProvider

### Event-Driven Types

#### observes / event-subscriber
**Description:** Observer pattern - listens to events
**When to use:** Event listeners, subscribers, reactive patterns
**Coupling:** Loose
**Typical usage:** Event-driven architectures
**Example:** Logger observes error events from ErrorHandler
**Note:** Both `observes` and `event-subscriber` are valid

#### notifies / event-publisher
**Description:** Publishes events or notifications
**When to use:** Event emitters, publishers, observable patterns
**Coupling:** Loose
**Typical usage:** Event-driven architectures
**Example:** OrderService notifies subscribers when order is placed
**Note:** Both `notifies` and `event-publisher` are valid

### Other Types

#### imports
**Description:** Direct ES6/CommonJS module import
**When to use:** JavaScript/TypeScript module imports
**Coupling:** Tight
**Typical usage:** Any module import
**Example:** Component imports utility functions

#### delegates
**Description:** Delegates operations to another component
**When to use:** Delegation pattern, facades
**Coupling:** Moderate
**Typical usage:** Facade pattern, delegation
**Example:** UserFacade delegates operations to multiple subsystems

---

## Type Selection Guidelines

### Choosing Between Similar Types

#### http vs http-rest vs http-graphql
- Use **`http-rest`** for RESTful APIs (preferred)
- Use **`http-graphql`** for GraphQL APIs (preferred)
- Use **`http`** only when protocol is unclear (avoid if possible)

#### database-connection vs database-query vs database-read-write
- Use **`database-query`** for read-only access (SELECT)
- Use **`database-write`** for write-only access (INSERT/UPDATE/DELETE)
- Use **`database-read-write`** for full access (most common)
- Use **`database-connection`** only as fallback

#### cache-access vs cache-read vs cache-write
- Use **`cache-read`** for read-only (GET operations)
- Use **`cache-write`** for write-only (SET operations)
- Use **`cache-read-write`** for both (most common)
- Use **`cache-access`** only as fallback

#### message-subscribe vs message-consumer
- Both are valid (aliases)
- Use **`message-subscribe`** for clarity (preferred)
- Use **`message-consumer`** if it reads better in your context

#### implements vs interface-implementation
- Both are valid
- Use **`implements`** for brevity (preferred)
- Use **`interface-implementation`** if you need to be explicit

#### observes vs event-subscriber
- Both are valid
- Use **`observes`** for brevity (preferred)
- Use **`event-subscriber`** if you need to be explicit

#### notifies vs event-publisher
- Both are valid
- Use **`notifies`** for brevity (preferred)
- Use **`event-publisher`** if you need to be explicit

### Level-Specific Guidelines

#### C1 System Context
**Focus:** Communication protocols between systems
**Prefer:** Specific types (`http-rest` over `http`)
**Always include:** `direction` and `protocol` fields

#### C2 Container
**Focus:** Container-to-container interactions
**Prefer:** Access-specific types (`database-read-write` over `database-connection`)
**Always include:** `protocol` and `isAsync` fields

#### C3 Component
**Focus:** Code-level dependencies and patterns
**Prefer:** Pattern-specific types (`injects` over `dependency`)
**Always include:** `coupling` field

---

## Examples by Level

### C1 Examples
```json
{ "type": "http-rest", "description": "Fetches data via REST API" }
{ "type": "grpc", "description": "High-performance RPC calls" }
{ "type": "message-queue", "description": "Publishes events to AMQP queue" }
{ "type": "authentication", "description": "Authenticates via OAuth 2.0" }
```

### C2 Examples
```json
{ "type": "http-rest", "description": "REST API calls from SPA to backend" }
{ "type": "database-read-write", "description": "Full database access via ORM" }
{ "type": "cache-read-write", "description": "Caches query results in Redis" }
{ "type": "message-publish", "description": "Publishes order events to queue" }
```

### C3 Examples
```json
{ "type": "uses", "description": "Uses service for business logic" }
{ "type": "injects", "description": "Injects repository via DI" }
{ "type": "implements", "description": "Implements repository interface" }
{ "type": "observes", "description": "Listens to order completion events" }
```

---

## Validation Rules

### All Levels
- Type must be from the appropriate level enum
- Description must be in active voice
- ID must match pattern: `^rel-[a-z0-9-]+$`

### C1 Specific
- Must include `direction` field
- Should include `protocol` for network communication

### C2 Specific
- Should include `protocol` for network communication
- Should include `isAsync` for messaging/async operations

### C3 Specific
- Must include `coupling` field
- Focus on code-level patterns

---

## References

- **Detailed Reference:** [reference.md](./reference.md)
- **Examples:** [examples.md](./examples.md)
- **Main Skill:** [SKILL.md](./SKILL.md)
- **Type Schema:** `/validation/templates/types-relations.json`

---

**Version:** 1.0.0
**Last Updated:** 2025-11-17
