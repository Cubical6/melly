# Observation Examples

**30+ real-world examples across C1, C2, and C3 levels.**

---

## Table of Contents

1. [C1 System Context Examples](#c1-system-context-examples)
2. [C2 Container Examples](#c2-container-examples)
3. [C3 Component Examples](#c3-component-examples)

---

## C1 System Context Examples

### Example 1: Event-Driven Architecture

```json
{
  "id": "obs-event-driven-arch",
  "category": "architecture",
  "severity": "info",
  "title": "Event-driven architecture with message queues",
  "description": "The system uses event-driven architecture with RabbitMQ message queues for asynchronous processing between services. This enables loose coupling and improved scalability.",
  "evidence": [
    {
      "type": "config",
      "location": "docker-compose.yml",
      "snippet": "rabbitmq:\n  image: rabbitmq:3-management\n  ports:\n    - '5672:5672'\n    - '15672:15672'",
      "note": "RabbitMQ configured as message broker"
    },
    {
      "type": "dependency",
      "location": "backend/package.json",
      "snippet": "\"amqplib\": \"^0.10.3\"",
      "note": "AMQP library for queue integration"
    }
  ],
  "tags": ["architecture", "messaging", "async", "rabbitmq"],
  "impact": "Enables horizontal scaling and system resilience. Services can process events asynchronously without blocking."
}
```

---

### Example 2: Third-Party Payment Dependency

```json
{
  "id": "obs-third-party-payment",
  "category": "external-dependencies",
  "severity": "warning",
  "title": "Critical dependency on third-party payment gateway",
  "description": "System has a hard dependency on Stripe payment gateway with no fallback mechanism. Stripe outages directly impact payment processing capability.",
  "evidence": [
    {
      "type": "code",
      "location": "src/services/payment.ts:23",
      "snippet": "const stripe = new Stripe(process.env.STRIPE_KEY);",
      "note": "Direct Stripe integration with no abstraction layer"
    },
    {
      "type": "file",
      "location": "src/services/payment.ts",
      "note": "Single payment provider implementation, no interface"
    }
  ],
  "tags": ["external-dependency", "payments", "stripe", "resilience"],
  "impact": "System unavailable for payments during Stripe outages. No ability to switch payment providers.",
  "recommendation": "Implement payment gateway abstraction layer to support multiple providers (Stripe, PayPal, Square) with failover capability."
}
```

---

### Example 3: Microservices Architecture

```json
{
  "id": "obs-microservices-pattern",
  "category": "architecture",
  "severity": "info",
  "title": "Microservices architecture with API gateway",
  "description": "System follows microservices architecture pattern with Kong API gateway routing requests to independent services (user-service, product-service, order-service).",
  "evidence": [
    {
      "type": "config",
      "location": "kong/kong.yml",
      "snippet": "services:\n  - name: user-service\n    url: http://user-api:3000\n  - name: product-service\n    url: http://product-api:3001",
      "note": "Kong gateway configuration"
    },
    {
      "type": "pattern",
      "location": "repos/",
      "note": "Separate repositories for each service: user-service/, product-service/, order-service/"
    }
  ],
  "tags": ["architecture", "microservices", "api-gateway", "kong"],
  "impact": "Enables independent deployment and scaling of services. Increases operational complexity."
}
```

---

### Example 4: Public API Without Rate Limiting

```json
{
  "id": "obs-no-rate-limiting",
  "category": "security",
  "severity": "critical",
  "title": "Public API lacks rate limiting",
  "description": "REST API is publicly accessible without rate limiting, making it vulnerable to denial-of-service attacks and API abuse.",
  "evidence": [
    {
      "type": "file",
      "location": "src/middleware/",
      "note": "No rate limiting middleware found"
    },
    {
      "type": "config",
      "location": "package.json",
      "note": "No rate limiting library installed (express-rate-limit, rate-limiter-flexible)"
    }
  ],
  "tags": ["security", "rate-limiting", "dos", "api"],
  "impact": "System vulnerable to denial-of-service attacks, API abuse, and resource exhaustion.",
  "recommendation": "Implement rate limiting using express-rate-limit or API gateway rate limiting policies."
}
```

---

### Example 5: OAuth2 Authentication

```json
{
  "id": "obs-oauth2-integration",
  "category": "integration",
  "severity": "info",
  "title": "OAuth2 authentication via Auth0",
  "description": "System integrates with Auth0 for OAuth2 authentication, supporting social login (Google, Facebook, GitHub) and enterprise SSO.",
  "evidence": [
    {
      "type": "config",
      "location": ".env.example",
      "snippet": "AUTH0_DOMAIN=example.auth0.com\nAUTH0_CLIENT_ID=xxx\nAUTH0_CALLBACK_URL=https://app.example.com/callback"
    },
    {
      "type": "dependency",
      "location": "frontend/package.json",
      "snippet": "\"@auth0/auth0-react\": \"^2.0.1\""
    }
  ],
  "tags": ["authentication", "oauth2", "auth0", "sso"],
  "impact": "Enables enterprise SSO and social login. Reduces authentication implementation complexity."
}
```

---

### Example 6: Multi-Tenant Architecture

```json
{
  "id": "obs-multi-tenant-saas",
  "category": "architecture",
  "severity": "info",
  "title": "Multi-tenant SaaS architecture with tenant isolation",
  "description": "System implements multi-tenant architecture with database-per-tenant isolation strategy. Each customer organization has a dedicated PostgreSQL schema.",
  "evidence": [
    {
      "type": "code",
      "location": "src/db/tenant.ts:34-38",
      "snippet": "const schema = `tenant_${tenantId}`;\nawait db.raw(`SET search_path TO ${schema}`);\nreturn db;",
      "note": "Schema-based tenant isolation"
    },
    {
      "type": "pattern",
      "location": "src/middleware/tenant-context.ts",
      "note": "Middleware extracts tenant from subdomain and sets context"
    }
  ],
  "tags": ["architecture", "multi-tenant", "saas", "isolation"],
  "impact": "Strong tenant data isolation. Schema-per-tenant approach may limit scalability with thousands of tenants."
}
```

---

### Example 7: Cloud-Native Deployment

```json
{
  "id": "obs-cloud-native-aws",
  "category": "deployment",
  "severity": "info",
  "title": "Cloud-native deployment on AWS with auto-scaling",
  "description": "System deployed on AWS using ECS Fargate for container orchestration with auto-scaling based on CPU and memory metrics.",
  "evidence": [
    {
      "type": "config",
      "location": "infrastructure/terraform/ecs.tf",
      "snippet": "resource \"aws_appautoscaling_target\" \"ecs_target\" {\n  max_capacity = 10\n  min_capacity = 2\n  resource_id = aws_ecs_service.main.id\n}",
      "note": "Terraform configuration for ECS auto-scaling"
    },
    {
      "type": "file",
      "location": "infrastructure/terraform/",
      "note": "Infrastructure as code using Terraform"
    }
  ],
  "tags": ["deployment", "aws", "ecs", "auto-scaling", "cloud-native"],
  "impact": "Enables automatic scaling based on demand. Reduces infrastructure management overhead."
}
```

---

### Example 8: Data Lake Integration

```json
{
  "id": "obs-data-lake-snowflake",
  "category": "data-flow",
  "severity": "info",
  "title": "Batch data export to Snowflake data lake",
  "description": "System exports operational data to Snowflake data lake nightly for analytics and reporting. ETL pipeline implemented using Apache Airflow.",
  "evidence": [
    {
      "type": "file",
      "location": "airflow/dags/export-to-snowflake.py",
      "note": "Airflow DAG for nightly data export"
    },
    {
      "type": "config",
      "location": "airflow/config/connections.yml",
      "snippet": "snowflake_conn:\n  conn_type: snowflake\n  account: xy12345\n  database: analytics_db"
    }
  ],
  "tags": ["data-flow", "etl", "snowflake", "analytics", "airflow"],
  "impact": "Enables advanced analytics and reporting without impacting operational database performance."
}
```

---

### Example 9: Service Mesh Implementation

```json
{
  "id": "obs-istio-service-mesh",
  "category": "integration",
  "severity": "info",
  "title": "Istio service mesh for service-to-service communication",
  "description": "Microservices communicate through Istio service mesh providing mTLS encryption, traffic management, and observability.",
  "evidence": [
    {
      "type": "config",
      "location": "k8s/istio/virtual-service.yml",
      "snippet": "apiVersion: networking.istio.io/v1beta1\nkind: VirtualService\nmetadata:\n  name: user-service"
    },
    {
      "type": "pattern",
      "location": "k8s/",
      "note": "Istio sidecar proxies injected into all service pods"
    }
  ],
  "tags": ["integration", "service-mesh", "istio", "mtls", "microservices"],
  "impact": "Provides mTLS encryption, circuit breaking, and distributed tracing without application code changes."
}
```

---

### Example 10: Geographic Distribution

```json
{
  "id": "obs-multi-region-active-active",
  "category": "scalability",
  "severity": "info",
  "title": "Multi-region active-active deployment for global users",
  "description": "System deployed in active-active configuration across US-East, US-West, and EU-Central regions with Route53 latency-based routing.",
  "evidence": [
    {
      "type": "config",
      "location": "infrastructure/terraform/route53.tf",
      "snippet": "routing_policy = \"latency\"\nset_identifier = \"us-east-1\""
    },
    {
      "type": "pattern",
      "location": "infrastructure/",
      "note": "Three Terraform workspaces: us-east, us-west, eu-central"
    }
  ],
  "tags": ["scalability", "multi-region", "global", "high-availability"],
  "impact": "Reduces latency for global users. Provides regional failover capability. Increases infrastructure cost and complexity."
}
```

---

## C2 Container Examples

### Example 11: React SPA with State Management

```json
{
  "id": "obs-spa-state-mgmt",
  "category": "technology",
  "severity": "info",
  "title": "Redux Toolkit for state management in React SPA",
  "description": "Frontend SPA uses Redux Toolkit for global state management, following best practices with feature-based slices and RTK Query for API calls.",
  "evidence": [
    {
      "type": "dependency",
      "location": "frontend/package.json",
      "snippet": "\"@reduxjs/toolkit\": \"^1.9.5\",\n\"react-redux\": \"^8.1.1\""
    },
    {
      "type": "file",
      "location": "frontend/src/store/",
      "note": "Well-organized store structure with feature slices: authSlice, userSlice, productSlice"
    },
    {
      "type": "code",
      "location": "frontend/src/store/index.ts",
      "snippet": "import { configureStore } from '@reduxjs/toolkit';\nimport authReducer from './authSlice';"
    }
  ],
  "tags": ["state-management", "redux", "frontend", "react"],
  "impact": "Provides predictable state updates, improved debugging with Redux DevTools, and type-safe API calls."
}
```

---

### Example 12: Database Connection Pool Missing

```json
{
  "id": "obs-db-no-connection-pool",
  "category": "performance",
  "severity": "warning",
  "title": "Database connections not pooled",
  "description": "Backend API creates new database connections for each request instead of using connection pooling, leading to performance degradation under load.",
  "evidence": [
    {
      "type": "code",
      "location": "src/db/connection.ts:12-15",
      "snippet": "export async function getConnection() {\n  return await mysql.createConnection(config);\n}",
      "note": "New connection created for every query"
    },
    {
      "type": "code",
      "location": "src/routes/users.ts:23",
      "snippet": "const conn = await getConnection();\nconst users = await conn.query('SELECT * FROM users');",
      "note": "Pattern repeated throughout codebase"
    }
  ],
  "tags": ["performance", "database", "connection-pool", "scalability"],
  "impact": "High latency for database queries. Connection exhaustion under concurrent load. Potential database server overload.",
  "recommendation": "Implement connection pooling using mysql2/pool with min 5, max 20 connections."
}
```

---

### Example 13: Container Health Checks

```json
{
  "id": "obs-health-check-implemented",
  "category": "deployment",
  "severity": "info",
  "title": "Comprehensive health check endpoints",
  "description": "Container implements /health (liveness) and /ready (readiness) endpoints with dependency checks for database, cache, and message queue.",
  "evidence": [
    {
      "type": "code",
      "location": "src/routes/health.ts:10-25",
      "snippet": "app.get('/health', async (req, res) => {\n  const dbOk = await checkDatabase();\n  const redisOk = await checkRedis();\n  const queueOk = await checkQueue();\n  res.status(dbOk && redisOk && queueOk ? 200 : 503).json({...});\n});"
    },
    {
      "type": "config",
      "location": "k8s/deployment.yml:45-52",
      "snippet": "livenessProbe:\n  httpGet:\n    path: /health\n    port: 3000\nreadinessProbe:\n  httpGet:\n    path: /ready\n    port: 3000"
    }
  ],
  "tags": ["deployment", "health-check", "kubernetes", "reliability"],
  "impact": "Kubernetes can detect and restart unhealthy containers. Prevents routing traffic to containers not ready to serve requests."
}
```

---

### Example 14: WebSocket Real-Time Communication

```json
{
  "id": "obs-websocket-notifications",
  "category": "communication",
  "severity": "info",
  "title": "WebSocket server for real-time notifications",
  "description": "Container implements WebSocket server using Socket.io for real-time push notifications to connected clients.",
  "evidence": [
    {
      "type": "dependency",
      "location": "backend/package.json",
      "snippet": "\"socket.io\": \"^4.6.1\""
    },
    {
      "type": "code",
      "location": "src/websocket/server.ts:15-20",
      "snippet": "const io = new Server(httpServer, {\n  cors: { origin: process.env.CORS_ORIGIN },\n  transports: ['websocket', 'polling']\n});"
    }
  ],
  "tags": ["communication", "websocket", "real-time", "socket.io"],
  "impact": "Enables instant notifications without polling. Maintains persistent connections, increasing server memory usage."
}
```

---

### Example 15: Docker Multi-Stage Build

```json
{
  "id": "obs-docker-multi-stage",
  "category": "deployment",
  "severity": "info",
  "title": "Multi-stage Docker build for optimized image size",
  "description": "Container uses multi-stage Dockerfile separating build and runtime stages, reducing final image size from 1.2GB to 180MB.",
  "evidence": [
    {
      "type": "config",
      "location": "Dockerfile:1-15",
      "snippet": "# Build stage\nFROM node:18-alpine AS builder\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\nCOPY . .\nRUN npm run build\n\n# Runtime stage\nFROM node:18-alpine\nWORKDIR /app\nCOPY --from=builder /app/dist ./dist\nCOPY package*.json ./\nRUN npm ci --production"
    }
  ],
  "tags": ["deployment", "docker", "optimization", "image-size"],
  "impact": "Reduces image size by 84%, faster deployments, lower storage costs, smaller attack surface."
}
```

---

### Example 16: Redis Session Storage

```json
{
  "id": "obs-redis-sessions",
  "category": "data-storage",
  "severity": "info",
  "title": "Redis for session storage with TTL",
  "description": "Container stores user sessions in Redis with 24-hour TTL, enabling horizontal scaling and fast session lookups.",
  "evidence": [
    {
      "type": "code",
      "location": "src/config/session.ts:8-14",
      "snippet": "app.use(session({\n  store: new RedisStore({ client: redisClient }),\n  secret: process.env.SESSION_SECRET,\n  resave: false,\n  saveUninitialized: false,\n  cookie: { maxAge: 24 * 60 * 60 * 1000 }\n}));"
    },
    {
      "type": "dependency",
      "location": "package.json",
      "snippet": "\"connect-redis\": \"^7.1.0\",\n\"redis\": \"^4.6.5\""
    }
  ],
  "tags": ["data-storage", "redis", "sessions", "caching"],
  "impact": "Enables stateless application design. Session data survives container restarts. Fast session access (~1ms)."
}
```

---

### Example 17: Environment Variable Overload

```json
{
  "id": "obs-env-var-overload",
  "category": "configuration",
  "severity": "warning",
  "title": "Excessive environment variables (42 required)",
  "description": "Container requires 42 environment variables to start, making configuration error-prone and deployment complex.",
  "evidence": [
    {
      "type": "file",
      "location": ".env.example",
      "note": "42 environment variables listed"
    },
    {
      "type": "code",
      "location": "src/config/index.ts:5-50",
      "snippet": "export const config = {\n  dbHost: required('DB_HOST'),\n  dbPort: required('DB_PORT'),\n  // ... 40 more",
      "note": "Long list of required config values"
    }
  ],
  "tags": ["configuration", "environment-variables", "complexity"],
  "impact": "High configuration complexity. Prone to misconfiguration errors. Difficult onboarding for new developers.",
  "recommendation": "Consolidate configuration using a config server (e.g., Spring Cloud Config) or use sensible defaults with override capability."
}
```

---

### Example 18: No Distributed Tracing

```json
{
  "id": "obs-no-distributed-tracing",
  "category": "monitoring",
  "severity": "warning",
  "title": "Missing distributed tracing in microservices",
  "description": "Container has logging but no distributed tracing instrumentation, making it difficult to debug cross-service request flows.",
  "evidence": [
    {
      "type": "file",
      "location": "package.json",
      "note": "No OpenTelemetry, Jaeger, or Zipkin dependencies"
    },
    {
      "type": "pattern",
      "location": "src/middleware/",
      "note": "No trace context propagation middleware"
    }
  ],
  "tags": ["monitoring", "distributed-tracing", "observability", "microservices"],
  "impact": "Difficult to trace requests across service boundaries. Hard to identify performance bottlenecks in multi-service flows.",
  "recommendation": "Implement OpenTelemetry instrumentation with Jaeger or Tempo backend for distributed tracing."
}
```

---

### Example 19: gRPC Inter-Service Communication

```json
{
  "id": "obs-grpc-communication",
  "category": "communication",
  "severity": "info",
  "title": "gRPC for high-performance inter-service communication",
  "description": "Container uses gRPC with Protocol Buffers for efficient inter-service communication, providing better performance than REST for internal APIs.",
  "evidence": [
    {
      "type": "dependency",
      "location": "package.json",
      "snippet": "\"@grpc/grpc-js\": \"^1.8.14\",\n\"@grpc/proto-loader\": \"^0.7.6\""
    },
    {
      "type": "file",
      "location": "proto/user-service.proto",
      "snippet": "service UserService {\n  rpc GetUser (GetUserRequest) returns (User);\n  rpc ListUsers (ListUsersRequest) returns (UserList);\n}",
      "note": "Protocol Buffer service definition"
    }
  ],
  "tags": ["communication", "grpc", "protobuf", "performance"],
  "impact": "Lower latency and bandwidth usage vs REST. Type-safe service contracts. Requires gRPC-compatible clients."
}
```

---

### Example 20: JWT Authentication with Refresh Tokens

```json
{
  "id": "obs-jwt-refresh-tokens",
  "category": "authentication",
  "severity": "info",
  "title": "JWT authentication with refresh token rotation",
  "description": "Container implements JWT access tokens (15min TTL) with refresh tokens (7 days) stored in httpOnly cookies, following OAuth2 best practices.",
  "evidence": [
    {
      "type": "code",
      "location": "src/auth/jwt.ts:45-52",
      "snippet": "const accessToken = jwt.sign(payload, secret, { expiresIn: '15m' });\nconst refreshToken = jwt.sign({ userId }, refreshSecret, { expiresIn: '7d' });\nres.cookie('refreshToken', refreshToken, { httpOnly: true, secure: true });",
      "note": "Token generation with appropriate TTLs"
    }
  ],
  "tags": ["authentication", "jwt", "refresh-tokens", "security"],
  "impact": "Balances security (short-lived access tokens) with UX (long refresh window). Refresh tokens in httpOnly cookies prevent XSS theft."
}
```

---

## C3 Component Examples

### Example 21: JWT in localStorage (Security Issue)

```json
{
  "id": "obs-auth-jwt-localstorage",
  "category": "security",
  "severity": "critical",
  "title": "JWT tokens stored in localStorage",
  "description": "Authentication component stores JWT tokens in browser localStorage, making them accessible to JavaScript and vulnerable to XSS attacks. Tokens should be stored in httpOnly cookies.",
  "evidence": [
    {
      "type": "code",
      "location": "src/features/auth/authSlice.ts:45",
      "snippet": "localStorage.setItem('authToken', action.payload.token);",
      "note": "Token persisted in localStorage"
    },
    {
      "type": "code",
      "location": "src/features/auth/authSlice.ts:52",
      "snippet": "const token = localStorage.getItem('authToken');\nif (token) { setAuthHeader(token); }",
      "note": "Token retrieved from localStorage on app init"
    }
  ],
  "tags": ["security", "authentication", "xss", "jwt"],
  "impact": "High security risk - Any XSS vulnerability can lead to token theft and account takeover. Tokens persist across browser sessions.",
  "recommendation": "Migrate to httpOnly cookies for token storage. Tokens will be automatically included in requests and inaccessible to JavaScript."
}
```

---

### Example 22: Repository Pattern Implementation

```json
{
  "id": "obs-repository-pattern",
  "category": "design-patterns",
  "severity": "info",
  "title": "Repository pattern for data access layer",
  "description": "UserService component implements the repository pattern to abstract database operations, improving testability and separation of concerns.",
  "evidence": [
    {
      "type": "file",
      "location": "src/repositories/UserRepository.ts",
      "note": "Dedicated repository class implementing IUserRepository interface"
    },
    {
      "type": "code",
      "location": "src/services/UserService.ts:23",
      "snippet": "constructor(private userRepo: IUserRepository) {}",
      "note": "Dependency injection of repository interface, not concrete implementation"
    },
    {
      "type": "code",
      "location": "src/repositories/UserRepository.ts:15-20",
      "snippet": "async findById(id: string): Promise<User | null> {\n  const row = await this.db('users').where({ id }).first();\n  return row ? this.mapToEntity(row) : null;\n}",
      "note": "Repository handles ORM queries and entity mapping"
    }
  ],
  "tags": ["design-pattern", "repository", "data-access", "separation-of-concerns"],
  "impact": "Improved testability through dependency injection. Clean separation between business logic and data access. Easier to swap database implementations."
}
```

---

### Example 23: Missing Error Handling

```json
{
  "id": "obs-no-error-handling",
  "category": "error-handling",
  "severity": "warning",
  "title": "Missing error handling in async operations",
  "description": "PaymentService component performs async Stripe operations without proper error handling, risking unhandled promise rejections and application crashes.",
  "evidence": [
    {
      "type": "code",
      "location": "src/features/payment/PaymentService.ts:78-82",
      "snippet": "async processPayment(amount: number) {\n  const charge = await stripe.charges.create({ amount });\n  await this.recordPayment(charge.id);\n  return charge.id;\n}",
      "note": "No try-catch block or .catch() handler"
    },
    {
      "type": "code",
      "location": "src/features/payment/PaymentService.ts:95-98",
      "snippet": "async refundPayment(chargeId: string) {\n  const refund = await stripe.refunds.create({ charge: chargeId });\n  return refund;\n}",
      "note": "Same pattern - no error handling"
    }
  ],
  "tags": ["error-handling", "async", "reliability", "payment"],
  "impact": "Application crashes or silent failures when Stripe API errors occur. No user feedback on payment failures. Potential data inconsistency.",
  "recommendation": "Add try-catch blocks to all async operations. Handle specific error types (network, API errors, validation). Log errors and return user-friendly messages."
}
```

---

### Example 24: High Cyclomatic Complexity

```json
{
  "id": "obs-high-complexity-validation",
  "category": "complexity",
  "severity": "warning",
  "title": "High cyclomatic complexity in validation function",
  "description": "FormValidator.validate() function has cyclomatic complexity of 45, making it difficult to understand, test, and maintain.",
  "evidence": [
    {
      "type": "metric",
      "location": "src/utils/FormValidator.ts:validate",
      "snippet": "Cyclomatic complexity: 45",
      "note": "Measured with ESLint complexity rule"
    },
    {
      "type": "code",
      "location": "src/utils/FormValidator.ts:25-180",
      "snippet": "function validate(form: Form): ValidationResult {\n  if (form.email) {\n    if (!isEmail(form.email)) {\n      if (form.email.includes('@')) {\n        // 150+ lines of nested conditions...",
      "note": "Deep nesting (7 levels) with many branches"
    }
  ],
  "tags": ["complexity", "code-quality", "maintainability", "testing"],
  "impact": "Difficult to understand control flow. Hard to achieve full test coverage. High risk of bugs when modifying. New developers struggle to maintain.",
  "recommendation": "Refactor into smaller functions, each validating one field. Extract common validation logic. Consider using validation library like Joi or Yup."
}
```

---

### Example 25: Comprehensive Unit Tests

```json
{
  "id": "obs-good-test-coverage",
  "category": "testing",
  "severity": "info",
  "title": "High unit test coverage with quality tests",
  "description": "AuthService component has 95% unit test coverage with well-structured tests covering happy paths, edge cases, and error scenarios.",
  "evidence": [
    {
      "type": "metric",
      "location": "coverage/auth/AuthService.ts.html",
      "snippet": "Lines: 95.2% (120/126)\nBranches: 92.5% (37/40)",
      "note": "Jest coverage report"
    },
    {
      "type": "file",
      "location": "src/features/auth/__tests__/AuthService.test.ts",
      "note": "12 test cases covering login, logout, token refresh, error scenarios"
    },
    {
      "type": "code",
      "location": "src/features/auth/__tests__/AuthService.test.ts:45-52",
      "snippet": "describe('login', () => {\n  it('should return tokens on valid credentials', async () => {...});\n  it('should throw on invalid credentials', async () => {...});\n  it('should lock account after 5 failed attempts', async () => {...});\n});"
    }
  ],
  "tags": ["testing", "unit-tests", "coverage", "quality"],
  "impact": "High confidence in component behavior. Early bug detection. Safe refactoring. Good documentation through tests."
}
```

---

### Example 26: N+1 Query Problem

```json
{
  "id": "obs-n-plus-one-queries",
  "category": "performance",
  "severity": "warning",
  "title": "N+1 query problem in dashboard data loading",
  "description": "DashboardController loads user posts in a loop, executing one query per post (N+1 problem). For a user with 100 posts, this results in 101 database queries.",
  "evidence": [
    {
      "type": "code",
      "location": "src/controllers/DashboardController.ts:78-82",
      "snippet": "const posts = await Post.find({ userId });\nfor (const post of posts) {\n  post.comments = await Comment.find({ postId: post.id }); // N queries\n  post.likes = await Like.count({ postId: post.id });      // N queries\n}",
      "note": "Separate query for each post's comments and likes"
    }
  ],
  "tags": ["performance", "database", "n+1", "orm"],
  "impact": "Dashboard load time scales linearly with number of posts. 100 posts = 201 queries = ~2 seconds. Severe performance degradation with large datasets.",
  "recommendation": "Use eager loading or JOIN queries to load related data in single query. Example: Post.find({ userId }).populate('comments likes')"
}
```

---

### Example 27: Tight Coupling to ORM

```json
{
  "id": "obs-tight-orm-coupling",
  "category": "coupling",
  "severity": "warning",
  "title": "Business logic tightly coupled to Sequelize ORM",
  "description": "Service layer components directly use Sequelize models and queries throughout, making it difficult to test or switch ORMs.",
  "evidence": [
    {
      "type": "code",
      "location": "src/services/OrderService.ts:34-38",
      "snippet": "async createOrder(data: OrderData) {\n  const order = await Order.create(data);\n  const items = await OrderItem.bulkCreate(order.id, data.items);\n  return order;\n}",
      "note": "Direct Sequelize model usage in service"
    },
    {
      "type": "pattern",
      "location": "src/services/",
      "note": "All 15 service files directly import and use Sequelize models"
    }
  ],
  "tags": ["coupling", "orm", "architecture", "testability"],
  "impact": "Difficult to unit test services (requires database). Hard to switch ORM. Business logic mixed with data access concerns.",
  "recommendation": "Introduce repository layer to abstract ORM. Services depend on repository interfaces, not concrete ORM implementations."
}
```

---

### Example 28: Factory Pattern for Service Creation

```json
{
  "id": "obs-factory-pattern-services",
  "category": "design-patterns",
  "severity": "info",
  "title": "Factory pattern for creating service instances",
  "description": "ServiceFactory component uses factory pattern to create service instances with appropriate dependencies, improving modularity and testability.",
  "evidence": [
    {
      "type": "code",
      "location": "src/factories/ServiceFactory.ts:12-25",
      "snippet": "class ServiceFactory {\n  createUserService(): UserService {\n    const repo = new UserRepository(this.db);\n    const cache = new RedisCache(this.redis);\n    const notifier = new EmailNotifier(this.mailer);\n    return new UserService(repo, cache, notifier);\n  }\n}",
      "note": "Factory encapsulates complex service construction"
    }
  ],
  "tags": ["design-pattern", "factory", "dependency-injection", "modularity"],
  "impact": "Centralized service creation logic. Easy to swap implementations. Supports testing with mock dependencies."
}
```

---

### Example 29: Missing Input Validation

```json
{
  "id": "obs-no-input-validation",
  "category": "security",
  "severity": "critical",
  "title": "No input validation in API controllers",
  "description": "UserController accepts user input without validation, allowing malformed data to reach the database and potentially causing SQL injection or data corruption.",
  "evidence": [
    {
      "type": "code",
      "location": "src/controllers/UserController.ts:23-27",
      "snippet": "async createUser(req: Request, res: Response) {\n  const user = await userService.create(req.body);\n  res.json(user);\n}",
      "note": "req.body used directly without validation"
    },
    {
      "type": "pattern",
      "location": "src/controllers/",
      "note": "No validation middleware (joi, class-validator, zod) found in any controller"
    }
  ],
  "tags": ["security", "validation", "input-validation", "api"],
  "impact": "Critical security vulnerability. Risk of SQL injection, NoSQL injection, data corruption. Invalid data can crash application.",
  "recommendation": "Implement input validation using Joi, class-validator, or Zod. Validate all inputs at controller level before processing."
}
```

---

### Example 30: Code Documentation with TSDoc

```json
{
  "id": "obs-tsdoc-documentation",
  "category": "documentation",
  "severity": "info",
  "title": "Comprehensive TSDoc documentation for public APIs",
  "description": "All public methods and classes in the API layer have comprehensive TSDoc comments including descriptions, parameter types, return values, and usage examples.",
  "evidence": [
    {
      "type": "code",
      "location": "src/api/UserAPI.ts:15-24",
      "snippet": "/**\n * Creates a new user account.\n * @param userData - User registration data\n * @param userData.email - User email (must be unique)\n * @param userData.password - Password (min 8 characters)\n * @returns Newly created user object (password excluded)\n * @throws {ValidationError} If email already exists\n * @example\n * const user = await userAPI.createUser({ email: 'test@example.com', password: 'secret123' });\n */\nasync createUser(userData: UserRegistrationData): Promise<User>"
    }
  ],
  "tags": ["documentation", "tsdoc", "api", "code-quality"],
  "impact": "Excellent developer experience. IntelliSense shows detailed information. Easier onboarding for new developers. Reduced need for external documentation."
}
```

---

## Summary

This examples document provides 30 real-world observation examples:

- **C1 System Context**: 10 examples covering architecture, integration, security, scalability, deployment
- **C2 Container**: 10 examples covering technology, performance, communication, monitoring, authentication
- **C3 Component**: 10 examples covering design patterns, security, testing, complexity, code quality

Each example demonstrates:
- Proper structure with all required fields
- Concrete evidence with file paths and code snippets
- Appropriate severity levels
- Clear impact and recommendations
- Relevant tags for searchability

Use these examples as templates when documenting your own architectural observations.
