# Communication Patterns

This document provides comprehensive patterns for inter-container communication in C4 Model Level 2 analysis.

## Synchronous Communication

### HTTP REST API

**Pattern:** Client makes HTTP request, waits for response

**Indicators:**
- axios, fetch, requests library
- REST endpoints (`/api/v1/users`)
- JSON request/response

**Relation Type:** `http-rest`

**Example:**
```json
{
  "target": "ecommerce-api",
  "type": "http-rest",
  "direction": "outbound",
  "description": "Fetches product catalog data via REST API",
  "protocol": {
    "method": "GET, POST",
    "endpoint": "/api/v1/products",
    "format": "JSON",
    "authentication": "JWT Bearer Token"
  }
}
```

**Detection Commands:**
```bash
# Find HTTP client libraries
grep -r "axios\|fetch\|requests\|http.client" src/

# Find API endpoint definitions
grep -r "@Get\|@Post\|@app.route\|router.get" src/

# Find REST API calls
grep -r "http://\|https://" .env config/
```

---

### HTTP GraphQL API

**Pattern:** Client sends GraphQL query, receives specific data

**Indicators:**
- Apollo Client, graphql-request
- Single `/graphql` endpoint
- Query language

**Relation Type:** `http-graphql`

**Example:**
```json
{
  "target": "graphql-api",
  "type": "http-graphql",
  "direction": "outbound",
  "description": "Queries user and order data via GraphQL",
  "protocol": {
    "endpoint": "/graphql",
    "format": "GraphQL",
    "authentication": "API Key header"
  }
}
```

**Detection Commands:**
```bash
# Find GraphQL client libraries
grep -r "@apollo/client\|graphql-request" package.json

# Find GraphQL schemas
find . -name "*.graphql" -o -name "schema.gql"

# Find GraphQL operations
grep -r "query\|mutation\|subscription" src/ | grep graphql
```

---

### gRPC

**Pattern:** Remote procedure call with Protocol Buffers

**Indicators:**
- @grpc/grpc-js, grpc-go
- .proto files
- Binary protocol

**Relation Type:** `grpc`

**Example:**
```json
{
  "target": "user-service",
  "type": "grpc",
  "direction": "outbound",
  "description": "Calls user authentication via gRPC",
  "protocol": {
    "service": "UserService",
    "methods": ["Authenticate", "GetProfile"]
  }
}
```

**Detection Commands:**
```bash
# Find gRPC libraries
grep -r "@grpc\|grpc-go\|grpc-java" package.json pom.xml

# Find proto files
find . -name "*.proto"

# Find gRPC service definitions
grep -r "service.*{" *.proto
```

---

## Asynchronous Communication

### Message Queue (Publish/Subscribe)

**Pattern:** Publisher sends message to queue, consumer processes later

**Indicators:**
- RabbitMQ, Kafka, AWS SQS
- amqplib, kafkajs
- Queue/topic names

**Relation Types:** `message-publish`, `message-subscribe`

**Example (Publisher):**
```json
{
  "target": "order-queue",
  "type": "message-publish",
  "direction": "outbound",
  "description": "Publishes order created events",
  "protocol": {
    "queue": "orders.created",
    "format": "JSON",
    "broker": "RabbitMQ"
  }
}
```

**Example (Consumer):**
```json
{
  "target": "order-queue",
  "type": "message-subscribe",
  "direction": "inbound",
  "description": "Consumes order created events for processing",
  "protocol": {
    "queue": "orders.created",
    "format": "JSON",
    "broker": "RabbitMQ"
  }
}
```

**Detection Commands:**
```bash
# Find message broker libraries
grep -r "amqplib\|kafkajs\|aws-sdk.*sqs" package.json

# Find queue/topic names
grep -r "queue\|topic\|exchange" config/ src/

# Find publish/subscribe operations
grep -r "publish\|subscribe\|sendMessage\|consume" src/
```

---

### Event Streaming (Kafka)

**Pattern:** Continuous stream of events, multiple consumers

**Indicators:**
- Apache Kafka
- kafkajs, confluent-kafka
- Topics and partitions

**Relation Types:** `event-publish`, `event-subscribe`

**Example:**
```json
{
  "target": "kafka-broker",
  "type": "event-publish",
  "direction": "outbound",
  "description": "Streams order events to Kafka topic",
  "protocol": {
    "topic": "orders.events",
    "partitions": 3,
    "format": "Avro",
    "broker": "Kafka"
  }
}
```

---

## Database Communication

### Database Connection

**Pattern:** Application connects to database, executes queries

**Indicators:**
- Connection strings in .env
- ORM libraries (Prisma, SQLAlchemy, Hibernate)
- Database drivers (pg, psycopg2, mysql2)

**Relation Type:** `database-query`

**Example:**
```json
{
  "target": "main-database",
  "type": "database-query",
  "direction": "outbound",
  "description": "Reads and writes user and order data",
  "protocol": {
    "driver": "PostgreSQL wire protocol",
    "connection_pool": "Max 20 connections",
    "orm": "Prisma"
  }
}
```

**Detection Commands:**
```bash
# Find database connection strings
grep -r "DATABASE_URL\|DB_HOST\|POSTGRES\|MYSQL" .env config/

# Find ORM libraries
grep -r "prisma\|typeorm\|sequelize\|sqlalchemy\|hibernate" package.json requirements.txt pom.xml

# Find database drivers
grep -r "pg\|psycopg2\|mysql2\|mongodb" package.json requirements.txt
```

---

## Cache Access

### Cache Read/Write

**Pattern:** Application reads/writes to in-memory cache

**Indicators:**
- redis, ioredis, node-cache
- Cache keys and TTL
- GET/SET operations

**Relation Type:** `cache-read-write`

**Example:**
```json
{
  "target": "session-cache",
  "type": "cache-read-write",
  "direction": "bidirectional",
  "description": "Stores and retrieves user session data",
  "protocol": {
    "driver": "Redis protocol",
    "operations": ["GET", "SET", "DEL", "EXPIRE"],
    "ttl": "1 hour"
  }
}
```

**Detection Commands:**
```bash
# Find cache libraries
grep -r "redis\|ioredis\|memcached\|node-cache" package.json

# Find cache configuration
grep -r "REDIS_URL\|REDIS_HOST\|CACHE_" .env config/

# Find cache operations
grep -r "\.get\|\.set\|\.del\|cache\." src/
```

---

## File Storage Access

### Object Storage

**Pattern:** Application uploads/downloads files to/from object storage

**Indicators:**
- AWS S3, MinIO, Azure Blob
- aws-sdk, @aws-sdk/client-s3
- Bucket names

**Relation Type:** `file-storage-access`

**Example:**
```json
{
  "target": "media-storage",
  "type": "file-storage-access",
  "direction": "bidirectional",
  "description": "Uploads user-generated images and retrieves media files",
  "protocol": {
    "service": "AWS S3",
    "bucket": "user-media-prod",
    "operations": ["PutObject", "GetObject", "DeleteObject"]
  }
}
```

**Detection Commands:**
```bash
# Find storage SDKs
grep -r "aws-sdk\|@aws-sdk\|minio\|azure-storage" package.json

# Find bucket/container names
grep -r "S3_BUCKET\|STORAGE_BUCKET\|AZURE_CONTAINER" .env config/

# Find storage operations
grep -r "putObject\|getObject\|upload\|download" src/
```

---

## External API Calls

### Third-Party API Integration

**Pattern:** Container calls external third-party service

**Indicators:**
- API keys in .env
- External domain URLs
- SDK libraries (Stripe, Twilio, SendGrid)

**Relation Type:** `external-api`

**Example:**
```json
{
  "target": "stripe-api",
  "type": "external-api",
  "direction": "outbound",
  "description": "Processes payments via Stripe API",
  "protocol": {
    "service": "Stripe API v1",
    "authentication": "API Key",
    "endpoints": ["POST /v1/charges", "GET /v1/customers"]
  }
}
```

**Detection Commands:**
```bash
# Find external API libraries
grep -r "stripe\|twilio\|sendgrid\|mailgun" package.json

# Find API keys
grep -r "API_KEY\|SECRET_KEY" .env | grep -v "DATABASE\|JWT"

# Find external domains
grep -r "https://api\." src/ config/
```

---

## WebSocket Communication

### Real-Time Bidirectional

**Pattern:** Persistent connection for real-time data exchange

**Indicators:**
- socket.io, ws, websocket
- WebSocket URLs (ws://, wss://)
- Real-time events

**Relation Type:** `websocket`

**Example:**
```json
{
  "target": "realtime-server",
  "type": "websocket",
  "direction": "bidirectional",
  "description": "Real-time chat and notifications",
  "protocol": {
    "library": "Socket.IO 4.x",
    "events": ["message", "notification", "status_update"],
    "format": "JSON"
  }
}
```

**Detection Commands:**
```bash
# Find WebSocket libraries
grep -r "socket.io\|ws\|websocket" package.json

# Find WebSocket connections
grep -r "ws://\|wss://\|io.connect\|new WebSocket" src/

# Find socket events
grep -r "socket.emit\|socket.on" src/
```

---

## Communication Pattern Summary

| Pattern | Sync/Async | Use Case | Typical Protocol |
|---------|-----------|----------|------------------|
| HTTP REST | Sync | CRUD operations | JSON over HTTP |
| GraphQL | Sync | Flexible data queries | GraphQL over HTTP |
| gRPC | Sync | Service-to-service | Protobuf over HTTP/2 |
| Message Queue | Async | Event-driven, decoupling | AMQP, SQS |
| Event Stream | Async | Real-time data pipelines | Kafka protocol |
| Database | Sync | Data persistence | SQL, MongoDB protocol |
| Cache | Sync | Fast data access | Redis protocol |
| Object Storage | Sync | File upload/download | S3 API |
| WebSocket | Bidirectional | Real-time updates | WS protocol |

---

## Direction Guidelines

**Outbound:** Container initiates communication to another container
- API calls from frontend to backend
- Database queries from API server
- Cache reads/writes from application

**Inbound:** Container receives communication from another container
- API server receives HTTP requests
- Worker consumes queue messages
- Database accepts queries

**Bidirectional:** Two-way communication
- WebSocket connections
- Cache read/write operations
- File storage upload/download

---

## Best Practices

1. **Be specific** - Document exact protocols, not just "HTTP"
2. **Include authentication** - JWT, API keys, OAuth
3. **Note data format** - JSON, Protobuf, Avro
4. **Document endpoints** - Actual URLs or queue names
5. **Capture direction** - Outbound, inbound, bidirectional
6. **Version protocols** - REST API v1, gRPC v2
7. **Performance characteristics** - Sync vs async, latency

## Common Pitfalls

1. **Missing intermediate containers** - Don't forget API gateways, proxies
2. **Assuming HTTP** - Could be gRPC, WebSocket, etc.
3. **Ignoring message brokers** - Async communication is indirect
4. **Generic descriptions** - "Talks to API" → "Calls REST API GET /api/users"
5. **Forgetting authentication** - Security mechanisms matter
