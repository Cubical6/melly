# Relationship Identification

## Relationship Types

Document how systems communicate:

### Common Relationship Types

1. **http-rest** - RESTful HTTP API
   - Most common web API pattern
   - Example: Frontend calls backend REST API

2. **http-graphql** - GraphQL API
   - Query-based API pattern
   - Example: React app queries GraphQL server

3. **grpc** - gRPC remote procedure calls
   - High-performance RPC
   - Example: Microservice-to-microservice communication

4. **websocket** - WebSocket bidirectional communication
   - Real-time communication
   - Example: Chat application, live updates

5. **message-queue** - Asynchronous message queue
   - Decoupled async communication
   - Example: Publishing events to RabbitMQ

6. **database-query** - Database read/write operations
   - Direct database access
   - Example: API querying PostgreSQL

7. **file-transfer** - File upload/download
   - File operations
   - Example: Uploading files to S3

8. **authentication** - Authentication/authorization
   - Identity verification
   - Example: OAuth flow with Auth0

## Relationship Direction

Specify the direction of communication:

- **outbound** - This system initiates communication to target
  - Example: "Web App calls API" (outbound from Web App)

- **inbound** - Target system initiates communication to this system
  - Example: "API receives requests from Web App" (inbound to API)

- **bidirectional** - Communication flows both ways
  - Example: WebSocket connection

**Prefer outbound/inbound over bidirectional** for clarity.

## Relationship Metadata

Document additional context:

```json
{
  "target": "payment-api",
  "type": "http-rest",
  "direction": "outbound",
  "description": "Processes payments via REST API",
  "protocol": {
    "method": "POST",
    "endpoint": "/api/v1/payments",
    "format": "JSON",
    "authentication": "JWT Bearer Token"
  },
  "metadata": {
    "synchronous": true,
    "frequency": "medium",
    "critical": true
  },
  "tags": ["payment", "rest", "critical"]
}
```

## How to Identify Relationships

### 1. Search for API calls:

```bash
# Look for HTTP client libraries
grep -r "axios\|fetch\|http.get" src/
grep -r "requests.get\|httpx" .
grep -r "Http::get\|Guzzle" .
```

### 2. Check environment variables:

```bash
# .env.example reveals external integrations
cat .env.example | grep -E "API_URL|BASE_URL|ENDPOINT"
```

### 3. Review configuration files:

```javascript
// config/api.js
const API_BASE_URL = 'https://api.example.com';  // → Relationship to API
const STRIPE_API = 'https://api.stripe.com';     // → Relationship to Stripe
```

### 4. Analyze package dependencies:

```json
{
  "dependencies": {
    "axios": "^1.0.0",           // → HTTP client (likely REST API calls)
    "@sendgrid/mail": "^7.0.0",  // → SendGrid integration
    "stripe": "^10.0.0",         // → Stripe integration
    "socket.io-client": "^4.0.0" // → WebSocket communication
  }
}
```

## Technology-to-Relationship Mapping

| Package/Library | Relationship Type | Example |
|----------------|-------------------|---------|
| axios, fetch | http-rest | REST API calls |
| @apollo/client | http-graphql | GraphQL queries |
| @grpc/grpc-js | grpc | Microservice RPC |
| socket.io-client | websocket | Real-time communication |
| amqplib, kafka-node | message-queue | Async messaging |
| pg, mysql2, mongoose | database-query | Database access |
| @aws-sdk/client-s3 | file-transfer | S3 uploads/downloads |
| @auth0/auth0-spa-js | authentication | OAuth flow |

## Relationship Discovery Checklist

- [ ] Search for HTTP client imports
- [ ] Check .env.example for API endpoints
- [ ] Review package.json dependencies
- [ ] Analyze configuration files
- [ ] Look for WebSocket connections
- [ ] Find message queue publishers/subscribers
- [ ] Identify database connections
- [ ] Detect authentication flows
