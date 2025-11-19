# C4 Model Relations - Comprehensive Examples

## Overview

This document provides comprehensive examples of relations across all three C4 Model levels, covering all major relation types.

**Usage:** Reference these examples when documenting your own architecture relations.

---

## Table of Contents

1. [C1 System Context Examples](#c1-system-context-examples)
2. [C2 Container Examples](#c2-container-examples)
3. [C3 Component Examples](#c3-component-examples)
4. [Cross-Level Examples](#cross-level-examples)

---

## C1 System Context Examples

### Example 1: REST API Communication

```json
{
  "id": "rel-webapp-to-api",
  "target": "backend-api",
  "type": "http-rest",
  "description": "Sends HTTP requests to fetch and update customer data",
  "protocol": "HTTP/REST",
  "direction": "outbound",
  "isAsync": true,
  "tags": ["api", "rest", "critical"]
}
```

**Context:** Web application calls backend API for all data operations
**Direction:** Outbound (web app initiates requests)
**Protocol:** RESTful HTTP

---

### Example 2: External Payment Gateway

```json
{
  "id": "rel-api-to-payment",
  "target": "stripe-payment-gateway",
  "type": "external-api",
  "description": "Processes payments via Stripe API for customer transactions",
  "protocol": "HTTPS/REST",
  "direction": "bidirectional",
  "isAsync": true,
  "tags": ["payment", "external", "stripe", "critical"]
}
```

**Context:** E-commerce system integrates with Stripe for payments
**Direction:** Bidirectional (API calls Stripe, Stripe sends webhooks)
**Protocol:** HTTPS with REST and webhook callbacks

---

### Example 3: Message Queue Processing

```json
{
  "id": "rel-worker-to-queue",
  "target": "rabbitmq",
  "type": "message-queue",
  "description": "Consumes background job messages for email notifications and data processing",
  "protocol": "AMQP",
  "direction": "inbound",
  "isAsync": true,
  "tags": ["async", "queue", "rabbitmq", "worker"]
}
```

**Context:** Worker service consumes messages from queue
**Direction:** Inbound (queue pushes messages to worker)
**Protocol:** AMQP (RabbitMQ)

---

### Example 4: OAuth Authentication

```json
{
  "id": "rel-app-to-auth",
  "target": "auth0",
  "type": "authentication",
  "description": "Authenticates users via OAuth 2.0 with social login support",
  "protocol": "OAuth 2.0",
  "direction": "outbound",
  "isAsync": false,
  "tags": ["auth", "oauth", "security", "auth0"]
}
```

**Context:** Application uses Auth0 for user authentication
**Direction:** Outbound (app redirects to Auth0)
**Protocol:** OAuth 2.0

---

### Example 5: GraphQL API

```json
{
  "id": "rel-mobile-to-graphql",
  "target": "graphql-api",
  "type": "http-graphql",
  "description": "Queries GraphQL API for flexible data fetching with nested relations",
  "protocol": "HTTP/GraphQL",
  "direction": "outbound",
  "isAsync": true,
  "tags": ["graphql", "api", "mobile"]
}
```

**Context:** Mobile app uses GraphQL for efficient data queries
**Direction:** Outbound (mobile queries API)
**Protocol:** GraphQL over HTTP

---

### Example 6: WebSocket Real-Time Communication

```json
{
  "id": "rel-chat-to-websocket",
  "target": "websocket-server",
  "type": "websocket",
  "description": "Maintains persistent WebSocket connection for real-time chat messages",
  "protocol": "WebSocket (RFC 6455)",
  "direction": "bidirectional",
  "isAsync": true,
  "tags": ["websocket", "realtime", "chat"]
}
```

**Context:** Chat application uses WebSocket for real-time messaging
**Direction:** Bidirectional (messages flow both ways)
**Protocol:** WebSocket

---

### Example 7: gRPC Microservices

```json
{
  "id": "rel-gateway-to-services",
  "target": "microservices-cluster",
  "type": "grpc",
  "description": "Communicates with microservices via gRPC for high-performance RPC calls",
  "protocol": "HTTP/2 gRPC",
  "direction": "outbound",
  "isAsync": false,
  "tags": ["grpc", "microservices", "rpc"]
}
```

**Context:** API gateway calls microservices via gRPC
**Direction:** Outbound (gateway calls services)
**Protocol:** gRPC over HTTP/2

---

### Example 8: Event Stream Processing

```json
{
  "id": "rel-analytics-to-kafka",
  "target": "kafka-cluster",
  "type": "event-stream",
  "description": "Consumes real-time clickstream events for analytics processing",
  "protocol": "Kafka Protocol",
  "direction": "inbound",
  "isAsync": true,
  "tags": ["kafka", "streaming", "analytics"]
}
```

**Context:** Analytics system processes events from Kafka
**Direction:** Inbound (Kafka streams events to analytics)
**Protocol:** Kafka streaming protocol

---

### Example 9: Database Connection

```json
{
  "id": "rel-app-to-database",
  "target": "postgres-cluster",
  "type": "database-connection",
  "description": "Connects to PostgreSQL cluster for persistent data storage",
  "protocol": "PostgreSQL Wire Protocol",
  "direction": "outbound",
  "isAsync": false,
  "tags": ["database", "postgres", "storage"]
}
```

**Context:** Application system connects to database system
**Direction:** Outbound (app queries database)
**Protocol:** PostgreSQL protocol

---

### Example 10: Email Service Integration

```json
{
  "id": "rel-notif-to-sendgrid",
  "target": "sendgrid",
  "type": "external-api",
  "description": "Sends transactional emails via SendGrid API",
  "protocol": "HTTPS/REST",
  "direction": "outbound",
  "isAsync": true,
  "tags": ["email", "sendgrid", "notifications"]
}
```

**Context:** Notification system sends emails via SendGrid
**Direction:** Outbound (system calls SendGrid API)
**Protocol:** HTTPS REST API

---

### Example 11: File Transfer

```json
{
  "id": "rel-backup-to-s3",
  "target": "aws-s3",
  "type": "file-transfer",
  "description": "Transfers backup files to S3 for long-term storage",
  "protocol": "HTTPS S3 API",
  "direction": "outbound",
  "isAsync": true,
  "tags": ["backup", "s3", "storage"]
}
```

**Context:** Backup system uploads files to S3
**Direction:** Outbound (backup pushes to S3)
**Protocol:** S3 API over HTTPS

---

### Example 12: Read Replica Access

```json
{
  "id": "rel-reporting-to-replica",
  "target": "postgres-read-replica",
  "type": "database-query",
  "description": "Queries read replica for reporting without impacting primary database",
  "protocol": "PostgreSQL Wire Protocol",
  "direction": "outbound",
  "isAsync": false,
  "tags": ["database", "reporting", "read-replica"]
}
```

**Context:** Reporting system queries read-only replica
**Direction:** Outbound (reporting queries replica)
**Protocol:** PostgreSQL (read-only)

---

## C2 Container Examples

### Example 1: SPA to API

```json
{
  "id": "rel-spa-to-api",
  "target": "express-api",
  "type": "http-rest",
  "description": "Fetches user data and submits forms via REST API endpoints",
  "protocol": "HTTP/REST",
  "isAsync": true,
  "tags": ["rest", "ajax", "fetch", "spa"]
}
```

**Context:** React SPA calls Express backend
**Container Flow:** Browser (SPA) → Server (API)
**Operations:** GET, POST, PUT, DELETE

---

### Example 2: API to PostgreSQL

```json
{
  "id": "rel-api-to-postgres",
  "target": "postgres-container",
  "type": "database-read-write",
  "description": "Reads and writes application data using Sequelize ORM",
  "protocol": "PostgreSQL Wire Protocol",
  "isAsync": false,
  "tags": ["database", "postgres", "sql", "sequelize"]
}
```

**Context:** Express API accesses PostgreSQL database
**Container Flow:** API Server → Database Container
**Operations:** Full CRUD via ORM

---

### Example 3: API to Redis Cache

```json
{
  "id": "rel-api-to-redis",
  "target": "redis-container",
  "type": "cache-read-write",
  "description": "Caches frequently accessed data to improve response times",
  "protocol": "Redis Protocol (RESP)",
  "isAsync": false,
  "tags": ["cache", "redis", "performance"]
}
```

**Context:** API caches query results in Redis
**Container Flow:** API Server → Cache Container
**Operations:** GET, SET, DEL

---

### Example 4: Worker to Message Queue

```json
{
  "id": "rel-worker-to-queue",
  "target": "rabbitmq-container",
  "type": "message-subscribe",
  "description": "Consumes email notification jobs from RabbitMQ queue",
  "protocol": "AMQP",
  "isAsync": true,
  "tags": ["queue", "worker", "email", "rabbitmq"]
}
```

**Context:** Worker consumes messages from RabbitMQ
**Container Flow:** Worker Container ← Message Queue Container
**Pattern:** Consumer (pull model)

---

### Example 5: API to Message Queue

```json
{
  "id": "rel-api-to-queue",
  "target": "rabbitmq-container",
  "type": "message-publish",
  "description": "Publishes order completion events for async processing",
  "protocol": "AMQP",
  "isAsync": true,
  "tags": ["queue", "publisher", "async"]
}
```

**Context:** API publishes events to queue
**Container Flow:** API Server → Message Queue Container
**Pattern:** Publisher (push model)

---

### Example 6: Frontend to GraphQL

```json
{
  "id": "rel-frontend-to-graphql",
  "target": "graphql-server",
  "type": "http-graphql",
  "description": "Queries GraphQL API with Apollo Client for nested data fetching",
  "protocol": "HTTP/GraphQL",
  "isAsync": true,
  "tags": ["graphql", "apollo", "queries"]
}
```

**Context:** Next.js frontend uses GraphQL API
**Container Flow:** Frontend Container → GraphQL Server Container
**Operations:** Query, Mutation

---

### Example 7: API to S3 Storage

```json
{
  "id": "rel-api-to-s3",
  "target": "aws-s3",
  "type": "file-write",
  "description": "Uploads user-generated images to S3 bucket",
  "protocol": "HTTPS S3 API",
  "isAsync": true,
  "tags": ["s3", "upload", "images"]
}
```

**Context:** API uploads files to S3
**Container Flow:** API Server → S3 Storage
**Operations:** PutObject, DeleteObject

---

### Example 8: Worker Reading Files

```json
{
  "id": "rel-worker-to-s3",
  "target": "aws-s3",
  "type": "file-read",
  "description": "Reads CSV files from S3 for batch processing",
  "protocol": "HTTPS S3 API",
  "isAsync": true,
  "tags": ["s3", "batch", "csv"]
}
```

**Context:** Background worker processes files from S3
**Container Flow:** Worker Container → S3 Storage
**Operations:** GetObject, ListObjects

---

### Example 9: Browser to CDN

```json
{
  "id": "rel-browser-to-cdn",
  "target": "cloudfront-cdn",
  "type": "cdn-fetch",
  "description": "Fetches static assets (JS, CSS, images) from CDN",
  "protocol": "HTTPS",
  "isAsync": true,
  "tags": ["cdn", "static", "assets"]
}
```

**Context:** Browser loads assets from CloudFront
**Container Flow:** Browser → CDN
**Operations:** GET (cached assets)

---

### Example 10: WebSocket Server

```json
{
  "id": "rel-client-to-websocket",
  "target": "websocket-server",
  "type": "websocket",
  "description": "Maintains WebSocket connection for real-time notifications",
  "protocol": "WebSocket Protocol",
  "isAsync": true,
  "tags": ["websocket", "realtime", "notifications"]
}
```

**Context:** Web client connects to WebSocket server
**Container Flow:** Browser ↔ WebSocket Server (bidirectional)
**Operations:** Send, Receive messages

---

### Example 11: Service to MySQL

```json
{
  "id": "rel-service-to-mysql",
  "target": "mysql-container",
  "type": "database-connection",
  "description": "Connects to MySQL database for general data operations",
  "protocol": "MySQL Wire Protocol",
  "isAsync": false,
  "tags": ["database", "mysql", "generic"]
}
```

**Context:** Service container accesses MySQL
**Container Flow:** Service Container → MySQL Container
**Operations:** Mixed read/write

---

### Example 12: Auth Service to Session Cache

```json
{
  "id": "rel-auth-to-cache",
  "target": "redis-container",
  "type": "cache-access",
  "description": "Accesses session cache for user authentication state",
  "protocol": "Redis Protocol",
  "isAsync": false,
  "tags": ["cache", "session", "auth"]
}
```

**Context:** Auth service stores sessions in Redis
**Container Flow:** Auth Container → Redis Container
**Operations:** Session management

---

## C3 Component Examples

### Example 1: Controller Uses Service

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

**Context:** Layered architecture pattern
**Component Flow:** UserController → UserService
**Pattern:** Service layer delegation

---

### Example 2: Service Injects Repository

```json
{
  "id": "rel-service-to-repo",
  "target": "user-repository",
  "type": "injects",
  "description": "Injects UserRepository via dependency injection for data access",
  "coupling": "loose",
  "tags": ["di", "repository-pattern"]
}
```

**Context:** Dependency injection pattern
**Component Flow:** UserService ← UserRepository (injected)
**Pattern:** Constructor injection

---

### Example 3: Auth Provides Context

```json
{
  "id": "rel-auth-to-user",
  "target": "user-component",
  "type": "provides",
  "description": "Provides authenticated user information to consuming components",
  "coupling": "loose",
  "tags": ["auth", "context", "provider"]
}
```

**Context:** React context provider pattern
**Component Flow:** AuthProvider → Consumers
**Pattern:** Provider/Consumer

---

### Example 4: Validator Extends Base

```json
{
  "id": "rel-validator-extends-base",
  "target": "base-validator",
  "type": "inherits",
  "description": "Extends base validation logic with custom rules",
  "coupling": "tight",
  "tags": ["inheritance", "validation"]
}
```

**Context:** OOP inheritance hierarchy
**Component Flow:** CustomValidator extends BaseValidator
**Pattern:** Classical inheritance

---

### Example 5: Payment Observes Order Events

```json
{
  "id": "rel-payment-observes-order",
  "target": "order-component",
  "type": "observes",
  "description": "Listens to order completion events to trigger payment processing",
  "coupling": "loose",
  "tags": ["event", "observer-pattern", "payment"]
}
```

**Context:** Observer/subscriber pattern
**Component Flow:** PaymentService ← OrderService (events)
**Pattern:** Event-driven

---

### Example 6: Order Notifies Subscribers

```json
{
  "id": "rel-order-notifies-payment",
  "target": "payment-component",
  "type": "notifies",
  "description": "Emits order completion events to registered subscribers",
  "coupling": "loose",
  "tags": ["event", "publisher", "orders"]
}
```

**Context:** Publisher pattern
**Component Flow:** OrderService → Subscribers
**Pattern:** Event emitter

---

### Example 7: Service Implements Interface

```json
{
  "id": "rel-service-implements-interface",
  "target": "repository-interface",
  "type": "implements",
  "description": "Implements IUserRepository contract for data access abstraction",
  "coupling": "loose",
  "tags": ["interface", "contract", "di"]
}
```

**Context:** Interface-based programming
**Component Flow:** UserRepository implements IUserRepository
**Pattern:** Dependency inversion

---

### Example 8: Logger Subscribes to Errors

```json
{
  "id": "rel-logger-subscribes-errors",
  "target": "error-handler",
  "type": "event-subscriber",
  "description": "Subscribes to error events for centralized logging",
  "coupling": "loose",
  "tags": ["event", "logging", "observer"]
}
```

**Context:** Error handling with observers
**Component Flow:** Logger ← ErrorHandler (events)
**Pattern:** Event subscription

---

### Example 9: Controller Calls Service Methods

```json
{
  "id": "rel-controller-calls-service",
  "target": "order-service",
  "type": "calls",
  "description": "Invokes createOrder and getOrderById methods directly",
  "coupling": "tight",
  "tags": ["method-call", "direct-call"]
}
```

**Context:** Direct method invocation
**Component Flow:** OrderController → OrderService.createOrder()
**Pattern:** Direct coupling

---

### Example 10: Component Composes Others

```json
{
  "id": "rel-order-composes-items",
  "target": "order-item",
  "type": "composes",
  "description": "Composes OrderItem instances as integral parts of Order",
  "coupling": "tight",
  "tags": ["composition", "has-a"]
}
```

**Context:** Object composition
**Component Flow:** Order has OrderItem[]
**Pattern:** Composition (strong has-a)

---

### Example 11: Component Aggregates References

```json
{
  "id": "rel-cart-aggregates-products",
  "target": "product",
  "type": "aggregates",
  "description": "Aggregates Product references without owning them",
  "coupling": "moderate",
  "tags": ["aggregation", "reference"]
}
```

**Context:** Object aggregation
**Component Flow:** ShoppingCart has Product[] (references)
**Pattern:** Aggregation (weak has-a)

---

### Example 12: Component Imports Utilities

```json
{
  "id": "rel-service-imports-utils",
  "target": "date-utils",
  "type": "imports",
  "description": "Imports date formatting utilities via ES6 import",
  "coupling": "tight",
  "tags": ["import", "utilities"]
}
```

**Context:** Module imports
**Component Flow:** OrderService imports { formatDate } from './utils'
**Pattern:** ES6 modules

---

### Example 13: Facade Delegates to Subsystems

```json
{
  "id": "rel-facade-delegates",
  "target": "subsystems",
  "type": "delegates",
  "description": "Delegates complex operations to multiple subsystems",
  "coupling": "moderate",
  "tags": ["facade", "delegation"]
}
```

**Context:** Facade pattern
**Component Flow:** OrderFacade → [PaymentService, InventoryService, ShippingService]
**Pattern:** Facade

---

### Example 14: Component Extends Functionality

```json
{
  "id": "rel-advanced-extends-basic",
  "target": "basic-search",
  "type": "extends",
  "description": "Extends basic search with advanced filtering and sorting",
  "coupling": "tight",
  "tags": ["inheritance", "extension"]
}
```

**Context:** Feature extension via inheritance
**Component Flow:** AdvancedSearch extends BasicSearch
**Pattern:** Extension

---

### Example 15: Consumer Uses Context

```json
{
  "id": "rel-profile-consumes-auth",
  "target": "auth-context",
  "type": "consumes",
  "description": "Consumes authenticated user data from AuthContext",
  "coupling": "loose",
  "tags": ["context", "react", "consumer"]
}
```

**Context:** React context consumer
**Component Flow:** UserProfile consumes AuthContext
**Pattern:** Context API

---

## Cross-Level Examples

### Example: Full Stack Feature

**C1 Level:**
```json
{
  "source": "mobile-app",
  "target": "backend-api",
  "type": "http-rest",
  "direction": "outbound"
}
```

**C2 Level:**
```json
{
  "source": "react-native-app",
  "target": "express-api",
  "type": "http-rest"
},
{
  "source": "express-api",
  "target": "postgres-db",
  "type": "database-read-write"
}
```

**C3 Level:**
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

---

## Summary

These examples demonstrate:

- **C1 Relations:** System-to-system communication patterns
- **C2 Relations:** Container-to-container interactions
- **C3 Relations:** Component-level dependencies and design patterns

Each example includes:
- Unique ID
- Target entity
- Relation type
- Clear description
- Appropriate metadata (direction, protocol, coupling)
- Tags for categorization

Use these as templates for documenting your own architecture relations.

---

**Version:** 1.0.0
**Last Updated:** 2025-11-17
