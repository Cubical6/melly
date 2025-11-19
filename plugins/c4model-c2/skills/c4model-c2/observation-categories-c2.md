# Observation Categories for C2

This document provides comprehensive guidance on documenting observations for C4 Model Level 2 (Container) analysis.

## Observation Categories

When documenting containers, capture these observation categories:

### 1. technology

**Focus:** Technology stack, frameworks, libraries, and versions

**What to Document:**
- Primary programming language and version
- Framework name and version
- Major libraries and their purposes
- Build tools and bundlers
- Package managers

**Examples:**
- ✅ "Uses React 18.2.0 with TypeScript for type safety"
- ✅ "Built with NestJS 10.0 framework following modular architecture"
- ✅ "Python 3.11 with FastAPI for high-performance async API"
- ⚠️ "Outdated Express 3.x version (current is 4.x)" (warning)
- ⚠️ "Mixed JavaScript and TypeScript files (inconsistent)" (warning)

**Detection Commands:**
```bash
# JavaScript/TypeScript
cat package.json | jq '.dependencies'
cat package.json | jq '.devDependencies'

# Python
cat requirements.txt
pip list

# Java
cat pom.xml | grep "<dependency>"
gradle dependencies

# Check versions
node --version
python --version
java --version
```

---

### 2. runtime

**Focus:** Runtime environment, platform, and deployment model

**What to Document:**
- Runtime environment (browser, Node.js, Python, JVM, etc.)
- Platform details (OS, architecture, version)
- Containerization (Docker, Kubernetes)
- Deployment model (single instance, replicas, serverless)
- Resource constraints (CPU, memory)

**Examples:**
- ✅ "Runs in browser (Chrome 90+, Firefox 88+, Safari 14+)"
- ✅ "Node.js 18.16.0 runtime on Linux x64"
- ✅ "Containerized with Docker, deployed to Kubernetes with 3 replicas"
- ✅ "Serverless deployment on AWS Lambda with cold start ~500ms"
- ⚠️ "No resource limits configured in Kubernetes" (warning)

**Detection Commands:**
```bash
# Check Dockerfile
cat Dockerfile | grep "FROM"

# Check K8s deployment
kubectl get deployment <name> -o yaml | grep replicas

# Check docker-compose
cat docker-compose.yml | grep "image:\|build:"

# Check runtime config
cat .node-version
cat runtime.txt
```

---

### 3. communication

**Focus:** How the container communicates with other containers

**What to Document:**
- Communication protocols (HTTP, gRPC, WebSocket, etc.)
- API specifications (REST, GraphQL)
- Message brokers (RabbitMQ, Kafka)
- Synchronous vs asynchronous
- Authentication mechanisms

**Examples:**
- ✅ "Communicates with API via HTTP REST over HTTPS"
- ✅ "Publishes events to RabbitMQ message broker"
- ✅ "Uses gRPC for inter-service communication"
- ✅ "WebSocket connection for real-time updates"
- ⚠️ "HTTP communication not encrypted (uses http://)" (warning)

**Detection Commands:**
```bash
# Find HTTP clients
grep -r "axios\|fetch\|requests" src/

# Find gRPC
grep -r "grpc\|proto" src/ | head -5

# Find WebSocket
grep -r "socket.io\|ws\|websocket" src/

# Find message broker
grep -r "amqp\|kafka\|redis.*publish" src/
```

---

### 4. data-storage

**Focus:** Data persistence, caching, and storage patterns

**What to Document:**
- Database type and version (PostgreSQL, MongoDB, etc.)
- Connection pooling configuration
- Caching strategy (Redis, Memcached)
- File storage (S3, local filesystem)
- Stateful vs stateless

**Examples:**
- ✅ "PostgreSQL 15 database with connection pooling (max 20)"
- ✅ "Redis cache for session storage with 1-hour TTL"
- ✅ "Stores uploaded files in AWS S3 bucket"
- ✅ "No database connection (stateless API)"
- ⚠️ "Database connection pool not configured (potential bottleneck)" (warning)

**Detection Commands:**
```bash
# Find database connections
grep -r "DATABASE_URL\|DB_HOST" .env

# Find ORMs
grep -r "prisma\|typeorm\|sequelize\|sqlalchemy" .

# Find cache usage
grep -r "REDIS_URL\|redis.get\|redis.set" .

# Find file storage
grep -r "S3_BUCKET\|aws-sdk.*s3\|multer" .
```

---

### 5. authentication

**Focus:** Authentication and authorization mechanisms

**What to Document:**
- Authentication method (JWT, OAuth, API keys)
- Token expiry and refresh
- Authorization rules (RBAC, ABAC)
- Session management
- Security headers

**Examples:**
- ✅ "JWT Bearer token authentication with 15-minute expiry"
- ✅ "OAuth 2.0 integration with Auth0"
- ✅ "API key authentication via x-api-key header"
- ⚠️ "No authentication implemented" (warning)
- 🔴 "JWT tokens never expire (security risk)" (critical)

**Detection Commands:**
```bash
# Find authentication libraries
grep -r "passport\|jsonwebtoken\|auth0" package.json

# Find JWT usage
grep -r "jwt\|bearer\|token" src/ | grep -i auth

# Find OAuth
grep -r "oauth\|openid" .

# Check for API keys
grep -r "API_KEY\|X-API-KEY" .env
```

---

### 6. configuration

**Focus:** Configuration management and environment variables

**What to Document:**
- Configuration sources (.env, ConfigMap, Secrets)
- Environment-specific configs (dev, staging, prod)
- Secret management
- Configuration validation
- Default values

**Examples:**
- ✅ "Configuration via environment variables"
- ✅ "Uses .env files for local development"
- ✅ "ConfigMap and Secrets in Kubernetes"
- ⚠️ "Hardcoded configuration values in source code" (warning)
- 🔴 "Secrets committed to git repository" (critical)

**Detection Commands:**
```bash
# Find .env files
find . -name ".env*" -not -path "*/node_modules/*"

# Check for ConfigMap usage
grep -r "ConfigMap" k8s/

# Find hardcoded values
grep -r "http://\|https://\|mongodb://\|postgres://" src/ | grep -v ".env"

# Check for secret management
grep -r "vault\|doppler\|aws-secrets-manager" .
```

---

### 7. monitoring

**Focus:** Logging, monitoring, and observability

**What to Document:**
- Logging framework and destination
- Metrics collection (Prometheus, DataDog)
- Tracing (OpenTelemetry, Jaeger)
- Health checks and readiness probes
- Error tracking (Sentry, Rollbar)

**Examples:**
- ✅ "Application logs to stdout, collected by Fluentd"
- ✅ "Prometheus metrics exposed on /metrics endpoint"
- ✅ "OpenTelemetry tracing enabled"
- ⚠️ "No logging or monitoring configured" (warning)
- ⚠️ "Logs contain sensitive data (PII, credentials)" (warning)

**Detection Commands:**
```bash
# Find logging libraries
grep -r "winston\|pino\|bunyan\|logrus" package.json

# Find metrics
grep -r "prometheus\|statsd\|datadog" .

# Find tracing
grep -r "opentelemetry\|jaeger\|zipkin" .

# Check for health endpoints
grep -r "/health\|/ready\|/alive" src/
```

---

### 8. dependencies

**Focus:** External dependencies and third-party services

**What to Document:**
- Third-party API integrations (Stripe, SendGrid)
- External service dependencies
- SDK usage
- Vendor lock-in risks
- Availability dependencies

**Examples:**
- ✅ "Depends on Stripe API for payment processing"
- ✅ "Uses SendGrid for transactional email"
- ✅ "Integrates with Google Analytics for tracking"
- ⚠️ "Heavy dependency on external APIs (availability risk)" (warning)
- ⚠️ "No fallback for third-party service failures" (warning)

**Detection Commands:**
```bash
# Find third-party SDKs
grep -r "stripe\|twilio\|sendgrid\|mailgun" package.json

# Find external API calls
grep -r "https://api\." src/ .env

# Check for API keys
grep -r "STRIPE_KEY\|TWILIO_\|SENDGRID_" .env

# Find vendor-specific code
grep -r "aws-sdk\|google-cloud\|azure" .
```

---

## Observation Structure

### JSON Schema

```json
{
  "id": "obs-tech-react-18",
  "category": "technology",
  "severity": "info",
  "description": "React 18.2.0 with TypeScript 5.0 for type-safe component development",
  "evidence": {
    "type": "file",
    "location": "package.json",
    "snippet": "\"react\": \"^18.2.0\", \"typescript\": \"^5.0.0\""
  },
  "tags": ["react", "typescript", "frontend", "spa"],
  "discovered_at": "2025-01-15T10:30:00Z",
  "discovered_by": "c2-abstractor"
}
```

### Field Descriptions

- **id**: Unique identifier (format: `obs-<category>-<short-desc>`)
- **category**: One of the 8 categories above
- **severity**: `info`, `warning`, or `critical`
- **description**: Human-readable observation
- **evidence**: Proof of the observation
  - **type**: `file`, `command`, `inference`
  - **location**: File path, command, or reasoning
  - **snippet**: Code snippet, command output, or explanation
- **tags**: Searchable keywords
- **discovered_at**: ISO 8601 timestamp
- **discovered_by**: Tool or agent name

---

## Observation Severity Levels

### info (Informational)

**Purpose:** Neutral findings documenting the system as it is

**Examples:**
- ℹ️ "Uses Prisma ORM for database access"
- ℹ️ "React 18.2.0 with functional components and hooks"
- ℹ️ "Deployed with 3 replicas for high availability"

**When to Use:**
- Technology choices (neutral)
- Architecture patterns (no issues)
- Configuration details (standard)

### warning (Needs Attention)

**Purpose:** Potential issues that should be addressed but aren't blocking

**Examples:**
- ⚠️ "Redis cache has no password configured"
- ⚠️ "Outdated Express 3.x version (current is 4.x)"
- ⚠️ "No resource limits configured in Kubernetes"
- ⚠️ "Logs contain timestamps but no correlation IDs"

**When to Use:**
- Outdated dependencies
- Missing best practices
- Potential performance issues
- Missing recommended features

### critical (Immediate Action)

**Purpose:** Critical issues requiring immediate action (security, stability)

**Examples:**
- 🔴 "Database credentials hardcoded in source code"
- 🔴 "JWT tokens never expire (security risk)"
- 🔴 "API exposed without authentication"
- 🔴 "Secrets committed to git repository"

**When to Use:**
- Security vulnerabilities
- Data exposure risks
- Critical misconfigurations
- Blocking production issues

---

## Best Practices

### DO:

1. **Be specific** - Include versions, exact technologies
2. **Provide evidence** - Link to files, commands, or reasoning
3. **Use consistent format** - Follow the JSON schema
4. **Tag appropriately** - Use searchable, relevant tags
5. **Document warnings** - Call out anti-patterns and risks
6. **Cite sources** - Reference configuration files, code

### DON'T:

1. **Don't be vague** - "Uses React" → "Uses React 18.2.0"
2. **Don't skip evidence** - Always provide proof
3. **Don't over-categorize** - One observation = one category
4. **Don't ignore security** - Flag security issues as critical
5. **Don't duplicate** - Consolidate similar observations
6. **Don't guess** - Only document what you can verify

---

## Common Observation Patterns

### Pattern: Outdated Dependencies

```json
{
  "id": "obs-tech-outdated-express",
  "category": "technology",
  "severity": "warning",
  "description": "Express 3.x is significantly outdated (current stable: 4.x). Consider upgrading for security patches and new features.",
  "evidence": {
    "type": "file",
    "location": "package.json",
    "snippet": "\"express\": \"^3.21.2\""
  },
  "tags": ["express", "outdated", "dependency", "security"]
}
```

### Pattern: Missing Authentication

```json
{
  "id": "obs-auth-missing",
  "category": "authentication",
  "severity": "critical",
  "description": "API endpoints exposed without authentication. All routes are publicly accessible.",
  "evidence": {
    "type": "command",
    "location": "grep -r 'app.get\\|app.post' src/",
    "snippet": "No authentication middleware found in route definitions"
  },
  "tags": ["authentication", "security", "api", "critical"]
}
```

### Pattern: Performance Configuration

```json
{
  "id": "obs-runtime-no-limits",
  "category": "runtime",
  "severity": "warning",
  "description": "Kubernetes deployment has no CPU or memory limits configured, which may lead to resource contention.",
  "evidence": {
    "type": "file",
    "location": "k8s/deployment.yaml",
    "snippet": "No 'resources.limits' section found in container spec"
  },
  "tags": ["kubernetes", "resources", "performance", "deployment"]
}
```

### Pattern: Good Practice

```json
{
  "id": "obs-monitor-prometheus",
  "category": "monitoring",
  "severity": "info",
  "description": "Prometheus metrics endpoint exposed at /metrics with custom application metrics",
  "evidence": {
    "type": "file",
    "location": "src/metrics.ts",
    "snippet": "app.get('/metrics', (req, res) => { res.set('Content-Type', register.contentType); res.end(register.metrics()); });"
  },
  "tags": ["prometheus", "monitoring", "metrics", "observability"]
}
```

---

## Relationship to C1 Observations

C2 observations are **more detailed** than C1:

| Aspect | C1 (System) | C2 (Container) |
|--------|-------------|----------------|
| **Scope** | Entire system | Individual containers |
| **Technology** | High-level tech stack | Specific frameworks & versions |
| **Runtime** | General deployment | Exact runtime config |
| **Communication** | External dependencies | Inter-container protocols |

**Example:**
- **C1**: "E-Commerce System uses Node.js and React"
- **C2 (Frontend)**: "React 18.2.0 SPA with TypeScript 5.0, deployed to Vercel"
- **C2 (Backend)**: "NestJS 10.0 API on Node.js 18.16.0, containerized in Kubernetes with 3 replicas"

---

## Next Steps

After capturing observations:

1. **Validate** using melly-validation scripts
2. **Store** in basic-memory MCP knowledge base
3. **Reference** in container documentation
4. **Track** warnings and critical issues
5. **Update** as system evolves
