# Observations and Relations JSON Schema Specification

**Purpose**: Define precise structure for observations and relations sections in c1-systems.json, c2-containers.json, and c3-components.json

**Version**: 1.0.0
**Date**: 2025-11-15

---

## Table of Contents

1. [Overview](#overview)
2. [Observations Schema](#observations-schema)
3. [Relations Schema](#relations-schema)
4. [C1 Level Examples](#c1-level-examples)
5. [C2 Level Examples](#c2-level-examples)
6. [C3 Level Examples](#c3-level-examples)
7. [Validation Rules](#validation-rules)
8. [Markdown Conversion](#markdown-conversion)

---

## Overview

### Design Principles

1. **Structured over Unstructured**: Observations are objects, not strings
2. **Consistent Schema**: Same structure across C1, C2, C3 levels
3. **Categorization**: Group observations by type for better organization
4. **Prioritization**: Support severity levels for filtering
5. **Graph Validity**: Relations must reference valid entity IDs
6. **Extensibility**: Allow additional metadata without breaking schema

### Common Schema Pattern

Both observations and relations follow this pattern across all C4 levels:

```json
{
  "observations": {
    "type": "array",
    "items": "observation-object"
  },
  "relations": {
    "type": "array",
    "items": "relation-object"
  }
}
```

---

## Observations Schema

### What Constitutes an Observation?

An observation is a **factual finding** about an entity (system/container/component) that:
- Describes architectural characteristics
- Identifies technical details
- Notes quality attributes
- Highlights security concerns
- Documents performance patterns
- Records design decisions

### Data Structure

**Type**: Array of observation objects

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "category", "description"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for this observation (e.g., 'obs-001')"
    },
    "category": {
      "type": "string",
      "enum": [
        "architectural",
        "technical",
        "quality",
        "security",
        "performance",
        "scalability",
        "maintainability",
        "integration",
        "deployment",
        "data",
        "testing",
        "documentation"
      ],
      "description": "Primary category of the observation"
    },
    "severity": {
      "type": "string",
      "enum": ["info", "warning", "critical"],
      "default": "info",
      "description": "Importance level of this observation"
    },
    "description": {
      "type": "string",
      "description": "Detailed description of the observation",
      "minLength": 10
    },
    "evidence": {
      "type": "object",
      "description": "Supporting evidence for the observation",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["file", "code", "config", "metric", "pattern"],
          "description": "Type of evidence"
        },
        "location": {
          "type": "string",
          "description": "Path or location of evidence (e.g., 'src/config/database.js')"
        },
        "snippet": {
          "type": "string",
          "description": "Code snippet or configuration excerpt"
        }
      }
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Additional tags for searchability"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When this observation was recorded (ISO 8601)"
    }
  }
}
```

### Required Fields

- `id` - Unique identifier for the observation
- `category` - Classification of the observation
- `description` - What was observed

### Optional Fields

- `severity` - Importance level (defaults to "info")
- `evidence` - Supporting proof
- `tags` - Additional metadata
- `timestamp` - When observed

### Observation Categories

| Category | C1 Usage | C2 Usage | C3 Usage |
|----------|----------|----------|----------|
| **architectural** | System boundaries, patterns | Container architecture, deployment | Component patterns, structure |
| **technical** | Technology choices | Specific tech stack | Implementation details |
| **quality** | System-level quality | Container quality attributes | Code quality metrics |
| **security** | Authentication/authorization | Container security, TLS | Security implementation |
| **performance** | System scalability | Container performance | Algorithm efficiency |
| **integration** | External integrations | Inter-container communication | Inter-component coupling |
| **deployment** | Infrastructure | Container deployment | Component packaging |
| **data** | Data boundaries | Data storage | Data structures |
| **testing** | Test strategy | Container test coverage | Unit test coverage |
| **documentation** | System docs | Container docs | Code documentation |

---

## Relations Schema

### What Constitutes a Relation?

A relation is a **directional connection** between entities that:
- Describes dependencies
- Documents communication patterns
- Maps data flow
- Identifies integration points
- Shows inheritance/composition

### Data Structure

**Type**: Array of relation objects

**Schema**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "source", "target", "type", "description"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for this relation (e.g., 'rel-001')"
    },
    "source": {
      "type": "string",
      "description": "ID of the source entity (can be implicit from parent context)"
    },
    "target": {
      "type": "string",
      "description": "ID of the target entity (must be valid entity ID)"
    },
    "type": {
      "type": "string",
      "enum": [
        "http-rest",
        "http-graphql",
        "http-soap",
        "grpc",
        "websocket",
        "message-queue",
        "event-stream",
        "database-query",
        "database-write",
        "file-io",
        "dependency",
        "inheritance",
        "composition",
        "aggregation",
        "uses",
        "calls",
        "contains"
      ],
      "description": "Type of relationship"
    },
    "direction": {
      "type": "string",
      "enum": ["unidirectional", "bidirectional"],
      "default": "unidirectional",
      "description": "Direction of the relationship"
    },
    "description": {
      "type": "string",
      "description": "Human-readable description of the relationship",
      "minLength": 10
    },
    "protocol": {
      "type": "object",
      "description": "Protocol-specific details",
      "properties": {
        "method": {
          "type": "string",
          "description": "HTTP method, RPC method, etc."
        },
        "endpoint": {
          "type": "string",
          "description": "API endpoint, queue name, etc."
        },
        "format": {
          "type": "string",
          "description": "Data format (JSON, XML, Protobuf, etc.)"
        },
        "authentication": {
          "type": "string",
          "description": "Authentication method (JWT, OAuth, API Key, etc.)"
        }
      }
    },
    "metadata": {
      "type": "object",
      "description": "Additional metadata",
      "properties": {
        "synchronous": {
          "type": "boolean",
          "description": "Whether the communication is synchronous"
        },
        "frequency": {
          "type": "string",
          "description": "How often this relation is used (high, medium, low)"
        },
        "critical": {
          "type": "boolean",
          "description": "Whether this is a critical dependency"
        }
      }
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Additional tags for searchability"
    }
  }
}
```

### Required Fields

- `id` - Unique identifier for the relation
- `source` - Source entity ID
- `target` - Target entity ID
- `type` - Relationship type
- `description` - What the relationship represents

### Optional Fields

- `direction` - Defaults to unidirectional
- `protocol` - Protocol-specific details
- `metadata` - Additional context
- `tags` - Searchability

### Relation Types by Level

| Type | C1 Usage | C2 Usage | C3 Usage |
|------|----------|----------|----------|
| **http-rest** | System-to-system HTTP | Container REST API calls | Component HTTP clients |
| **http-graphql** | System GraphQL API | Container GraphQL endpoints | Component resolvers |
| **grpc** | System RPC | Container gRPC services | Component RPC calls |
| **websocket** | System real-time | Container WebSocket servers | Component WebSocket handlers |
| **message-queue** | System async messaging | Container queue consumers | Component message handlers |
| **event-stream** | System event-driven | Container event publishers | Component event listeners |
| **database-query** | System data access | Container DB connections | Component query builders |
| **dependency** | System dependencies | Container dependencies | Component imports |
| **uses** | System uses another | Container uses service | Component uses utility |
| **calls** | System invokes | Container RPC | Component function calls |
| **contains** | System contains subsystem | Container contains components | Component contains classes |

---

## C1 Level Examples

### Example: c1-systems.json

```json
{
  "version": "1.0.0",
  "timestamp": "2025-11-15T20:10:00Z",
  "parent": {
    "file": "init.json",
    "timestamp": "2025-11-15T20:00:00Z"
  },
  "metadata": {
    "generator": "c1-abstractor",
    "user": "melly-user",
    "project": "ecommerce-platform"
  },
  "systems": [
    {
      "id": "web-frontend",
      "name": "Web Frontend",
      "description": "Customer-facing e-commerce web application",
      "repositories": ["/repos/frontend-spa"],
      "observations": [
        {
          "id": "obs-c1-001",
          "category": "architectural",
          "severity": "info",
          "description": "Single Page Application (SPA) architecture using React framework",
          "evidence": {
            "type": "file",
            "location": "package.json",
            "snippet": "\"react\": \"^18.2.0\""
          },
          "tags": ["react", "spa", "frontend"],
          "timestamp": "2025-11-15T20:10:15Z"
        },
        {
          "id": "obs-c1-002",
          "category": "security",
          "severity": "warning",
          "description": "Authentication handled client-side with JWT tokens stored in localStorage",
          "evidence": {
            "type": "code",
            "location": "src/auth/AuthService.ts",
            "snippet": "localStorage.setItem('token', jwt)"
          },
          "tags": ["authentication", "jwt", "security"],
          "timestamp": "2025-11-15T20:10:20Z"
        },
        {
          "id": "obs-c1-003",
          "category": "integration",
          "severity": "info",
          "description": "Communicates with backend REST API over HTTPS",
          "evidence": {
            "type": "config",
            "location": ".env.example",
            "snippet": "REACT_APP_API_URL=https://api.example.com"
          },
          "tags": ["rest-api", "https", "integration"],
          "timestamp": "2025-11-15T20:10:25Z"
        },
        {
          "id": "obs-c1-004",
          "category": "performance",
          "severity": "info",
          "description": "Uses code splitting and lazy loading for optimal bundle size",
          "evidence": {
            "type": "pattern",
            "location": "src/App.tsx",
            "snippet": "const Dashboard = lazy(() => import('./pages/Dashboard'))"
          },
          "tags": ["performance", "code-splitting", "optimization"],
          "timestamp": "2025-11-15T20:10:30Z"
        }
      ],
      "relations": [
        {
          "id": "rel-c1-001",
          "source": "web-frontend",
          "target": "api-backend",
          "type": "http-rest",
          "direction": "unidirectional",
          "description": "Fetches product catalog, user data, and order information via REST API",
          "protocol": {
            "method": "GET, POST, PUT, DELETE",
            "endpoint": "/api/v1/*",
            "format": "JSON",
            "authentication": "JWT Bearer Token"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": true
          },
          "tags": ["rest", "json", "api"]
        },
        {
          "id": "rel-c1-002",
          "source": "web-frontend",
          "target": "payment-gateway",
          "type": "http-rest",
          "direction": "unidirectional",
          "description": "Processes payments through external payment gateway (Stripe)",
          "protocol": {
            "method": "POST",
            "endpoint": "https://api.stripe.com/v1/charges",
            "format": "JSON",
            "authentication": "API Key"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "medium",
            "critical": true
          },
          "tags": ["payment", "stripe", "external"]
        },
        {
          "id": "rel-c1-003",
          "source": "web-frontend",
          "target": "cdn",
          "type": "http-rest",
          "direction": "unidirectional",
          "description": "Loads static assets (images, fonts) from CDN",
          "protocol": {
            "method": "GET",
            "endpoint": "https://cdn.example.com/assets/*",
            "format": "Binary",
            "authentication": "None"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": false
          },
          "tags": ["cdn", "static-assets", "performance"]
        }
      ]
    },
    {
      "id": "api-backend",
      "name": "API Backend",
      "description": "RESTful API server for business logic and data access",
      "repositories": ["/repos/backend-api"],
      "observations": [
        {
          "id": "obs-c1-005",
          "category": "architectural",
          "severity": "info",
          "description": "Layered architecture with controllers, services, and repositories",
          "evidence": {
            "type": "pattern",
            "location": "src/",
            "snippet": "controllers/, services/, repositories/"
          },
          "tags": ["layered-architecture", "mvc", "backend"],
          "timestamp": "2025-11-15T20:11:00Z"
        },
        {
          "id": "obs-c1-006",
          "category": "technical",
          "severity": "info",
          "description": "Built with Node.js and Express.js framework",
          "evidence": {
            "type": "file",
            "location": "package.json",
            "snippet": "\"express\": \"^4.18.2\""
          },
          "tags": ["nodejs", "express", "javascript"],
          "timestamp": "2025-11-15T20:11:05Z"
        },
        {
          "id": "obs-c1-007",
          "category": "security",
          "severity": "critical",
          "description": "No rate limiting implemented on API endpoints",
          "evidence": {
            "type": "file",
            "location": "src/middleware/",
            "snippet": "Missing rate limiter middleware"
          },
          "tags": ["security", "rate-limiting", "vulnerability"],
          "timestamp": "2025-11-15T20:11:10Z"
        }
      ],
      "relations": [
        {
          "id": "rel-c1-004",
          "source": "api-backend",
          "target": "postgres-db",
          "type": "database-query",
          "direction": "bidirectional",
          "description": "Reads and writes application data to PostgreSQL database",
          "protocol": {
            "method": "SQL",
            "endpoint": "postgresql://localhost:5432/ecommerce",
            "format": "Binary Protocol",
            "authentication": "Username/Password"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": true
          },
          "tags": ["database", "postgresql", "data-access"]
        },
        {
          "id": "rel-c1-005",
          "source": "api-backend",
          "target": "redis-cache",
          "type": "database-query",
          "direction": "bidirectional",
          "description": "Caches frequently accessed data in Redis for performance",
          "protocol": {
            "method": "Redis Protocol",
            "endpoint": "redis://localhost:6379",
            "format": "Redis Serialization Protocol",
            "authentication": "Password"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": false
          },
          "tags": ["cache", "redis", "performance"]
        },
        {
          "id": "rel-c1-006",
          "source": "api-backend",
          "target": "email-service",
          "type": "http-rest",
          "direction": "unidirectional",
          "description": "Sends transactional emails via external email service (SendGrid)",
          "protocol": {
            "method": "POST",
            "endpoint": "https://api.sendgrid.com/v3/mail/send",
            "format": "JSON",
            "authentication": "API Key"
          },
          "metadata": {
            "synchronous": false,
            "frequency": "medium",
            "critical": false
          },
          "tags": ["email", "sendgrid", "notifications"]
        }
      ]
    }
  ]
}
```

### C1 Observations Characteristics

- **Focus**: System-level architecture and external integrations
- **Categories**: Architectural patterns, technology choices, security posture
- **Granularity**: High-level, strategic observations
- **Evidence**: Package manifests, config files, architectural patterns

### C1 Relations Characteristics

- **Focus**: Inter-system communication and external dependencies
- **Types**: HTTP, database connections, external APIs
- **Details**: Protocol, authentication, criticality
- **Scope**: Cross-system boundaries

---

## C2 Level Examples

### Example: c2-containers.json

```json
{
  "version": "1.0.0",
  "timestamp": "2025-11-15T20:20:00Z",
  "parent": {
    "file": "c1-systems.json",
    "timestamp": "2025-11-15T20:10:00Z"
  },
  "metadata": {
    "generator": "c2-abstractor",
    "user": "melly-user",
    "project": "ecommerce-platform"
  },
  "containers": [
    {
      "id": "frontend-spa",
      "name": "React SPA",
      "description": "Single Page Application built with React and TypeScript",
      "system": "web-frontend",
      "technology": "React 18.2, TypeScript 5.0, Vite 4.0",
      "runtime": "Browser",
      "observations": [
        {
          "id": "obs-c2-001",
          "category": "technical",
          "severity": "info",
          "description": "Uses Vite as build tool for fast development and optimized production builds",
          "evidence": {
            "type": "file",
            "location": "vite.config.ts",
            "snippet": "export default defineConfig({ plugins: [react()] })"
          },
          "tags": ["vite", "build-tool", "bundler"],
          "timestamp": "2025-11-15T20:20:10Z"
        },
        {
          "id": "obs-c2-002",
          "category": "architectural",
          "severity": "info",
          "description": "State management using Redux Toolkit with RTK Query for API calls",
          "evidence": {
            "type": "file",
            "location": "src/store/index.ts",
            "snippet": "configureStore({ reducer: { api: apiSlice.reducer } })"
          },
          "tags": ["redux", "state-management", "rtk-query"],
          "timestamp": "2025-11-15T20:20:15Z"
        },
        {
          "id": "obs-c2-003",
          "category": "quality",
          "severity": "warning",
          "description": "Test coverage at 45% - below recommended 80% threshold",
          "evidence": {
            "type": "metric",
            "location": "coverage/index.html",
            "snippet": "Total coverage: 45.2%"
          },
          "tags": ["testing", "coverage", "quality"],
          "timestamp": "2025-11-15T20:20:20Z"
        },
        {
          "id": "obs-c2-004",
          "category": "maintainability",
          "severity": "info",
          "description": "Consistent use of TypeScript strict mode for type safety",
          "evidence": {
            "type": "config",
            "location": "tsconfig.json",
            "snippet": "\"strict\": true"
          },
          "tags": ["typescript", "type-safety", "maintainability"],
          "timestamp": "2025-11-15T20:20:25Z"
        }
      ],
      "relations": [
        {
          "id": "rel-c2-001",
          "source": "frontend-spa",
          "target": "express-api",
          "type": "http-rest",
          "direction": "unidirectional",
          "description": "All API requests routed through RTK Query service layer",
          "protocol": {
            "method": "GET, POST, PUT, DELETE",
            "endpoint": "/api/v1/*",
            "format": "JSON",
            "authentication": "JWT Bearer Token in Authorization header"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": true
          },
          "tags": ["rest-api", "rtk-query"]
        }
      ]
    },
    {
      "id": "express-api",
      "name": "Express API Server",
      "description": "Node.js REST API server handling business logic",
      "system": "api-backend",
      "technology": "Node.js 18, Express.js 4.18, TypeScript 5.0",
      "runtime": "Node.js Server",
      "observations": [
        {
          "id": "obs-c2-005",
          "category": "architectural",
          "severity": "info",
          "description": "RESTful API design following OpenAPI 3.0 specification",
          "evidence": {
            "type": "file",
            "location": "docs/openapi.yaml",
            "snippet": "openapi: 3.0.0"
          },
          "tags": ["rest", "openapi", "api-design"],
          "timestamp": "2025-11-15T20:20:30Z"
        },
        {
          "id": "obs-c2-006",
          "category": "security",
          "severity": "info",
          "description": "JWT authentication with RS256 signature algorithm",
          "evidence": {
            "type": "code",
            "location": "src/middleware/auth.ts",
            "snippet": "jwt.verify(token, publicKey, { algorithms: ['RS256'] })"
          },
          "tags": ["jwt", "authentication", "security"],
          "timestamp": "2025-11-15T20:20:35Z"
        },
        {
          "id": "obs-c2-007",
          "category": "performance",
          "severity": "warning",
          "description": "No connection pooling configured for database connections",
          "evidence": {
            "type": "code",
            "location": "src/database/connection.ts",
            "snippet": "new Client() created per request"
          },
          "tags": ["database", "performance", "connection-pooling"],
          "timestamp": "2025-11-15T20:20:40Z"
        },
        {
          "id": "obs-c2-008",
          "category": "scalability",
          "severity": "critical",
          "description": "In-memory session storage prevents horizontal scaling",
          "evidence": {
            "type": "code",
            "location": "src/middleware/session.ts",
            "snippet": "session({ store: new MemoryStore() })"
          },
          "tags": ["sessions", "scalability", "memory"],
          "timestamp": "2025-11-15T20:20:45Z"
        }
      ],
      "relations": [
        {
          "id": "rel-c2-002",
          "source": "express-api",
          "target": "postgres-container",
          "type": "database-query",
          "direction": "bidirectional",
          "description": "Uses Sequelize ORM for database operations",
          "protocol": {
            "method": "SQL via Sequelize ORM",
            "endpoint": "postgresql://postgres:5432/ecommerce",
            "format": "Binary Protocol",
            "authentication": "Username/Password"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": true
          },
          "tags": ["sequelize", "orm", "postgresql"]
        },
        {
          "id": "rel-c2-003",
          "source": "express-api",
          "target": "redis-container",
          "type": "database-query",
          "direction": "bidirectional",
          "description": "Redis client for caching and session storage",
          "protocol": {
            "method": "Redis Commands",
            "endpoint": "redis://redis:6379",
            "format": "RESP",
            "authentication": "Password"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": false
          },
          "tags": ["redis", "cache", "sessions"]
        }
      ]
    },
    {
      "id": "postgres-container",
      "name": "PostgreSQL Database",
      "description": "Primary relational database for application data",
      "system": "api-backend",
      "technology": "PostgreSQL 15.2",
      "runtime": "Database Server",
      "observations": [
        {
          "id": "obs-c2-009",
          "category": "data",
          "severity": "info",
          "description": "Database schema includes 15 tables with proper foreign key constraints",
          "evidence": {
            "type": "file",
            "location": "migrations/",
            "snippet": "15 migration files found"
          },
          "tags": ["schema", "migrations", "database"],
          "timestamp": "2025-11-15T20:21:00Z"
        },
        {
          "id": "obs-c2-010",
          "category": "performance",
          "severity": "warning",
          "description": "No indexing strategy on frequently queried columns",
          "evidence": {
            "type": "metric",
            "location": "pg_stat_user_tables",
            "snippet": "Sequential scans > 10,000 on users table"
          },
          "tags": ["indexing", "performance", "optimization"],
          "timestamp": "2025-11-15T20:21:05Z"
        }
      ],
      "relations": []
    },
    {
      "id": "redis-container",
      "name": "Redis Cache",
      "description": "In-memory cache for performance optimization",
      "system": "api-backend",
      "technology": "Redis 7.0",
      "runtime": "Cache Server",
      "observations": [
        {
          "id": "obs-c2-011",
          "category": "performance",
          "severity": "info",
          "description": "Configured with LRU eviction policy for memory management",
          "evidence": {
            "type": "config",
            "location": "redis.conf",
            "snippet": "maxmemory-policy allkeys-lru"
          },
          "tags": ["cache", "eviction", "lru"],
          "timestamp": "2025-11-15T20:21:10Z"
        }
      ],
      "relations": []
    }
  ]
}
```

### C2 Observations Characteristics

- **Focus**: Container-specific implementation and deployment details
- **Categories**: Technology stack, runtime configuration, resource management
- **Granularity**: Medium-level, tactical observations
- **Evidence**: Config files, deployment manifests, runtime metrics

### C2 Relations Characteristics

- **Focus**: Inter-container communication within a system
- **Types**: Database connections, cache access, message queues
- **Details**: ORM/client libraries, connection strings, protocols
- **Scope**: Within system boundaries

---

## C3 Level Examples

### Example: c3-components.json

```json
{
  "version": "1.0.0",
  "timestamp": "2025-11-15T20:30:00Z",
  "parent": {
    "file": "c2-containers.json",
    "timestamp": "2025-11-15T20:20:00Z"
  },
  "metadata": {
    "generator": "c3-abstractor",
    "user": "melly-user",
    "project": "ecommerce-platform"
  },
  "components": [
    {
      "id": "auth-component",
      "name": "Authentication Component",
      "description": "Handles user authentication and authorization",
      "container": "express-api",
      "path": "src/components/auth",
      "observations": [
        {
          "id": "obs-c3-001",
          "category": "architectural",
          "severity": "info",
          "description": "Implements Passport.js strategy pattern for authentication",
          "evidence": {
            "type": "code",
            "location": "src/components/auth/strategies/jwt.strategy.ts",
            "snippet": "export class JwtStrategy extends PassportStrategy(Strategy) {}"
          },
          "tags": ["passport", "strategy-pattern", "authentication"],
          "timestamp": "2025-11-15T20:30:10Z"
        },
        {
          "id": "obs-c3-002",
          "category": "security",
          "severity": "info",
          "description": "Password hashing using bcrypt with 12 rounds",
          "evidence": {
            "type": "code",
            "location": "src/components/auth/password.service.ts",
            "snippet": "bcrypt.hash(password, 12)"
          },
          "tags": ["bcrypt", "password-hashing", "security"],
          "timestamp": "2025-11-15T20:30:15Z"
        },
        {
          "id": "obs-c3-003",
          "category": "quality",
          "severity": "info",
          "description": "Comprehensive unit tests with 95% coverage for this component",
          "evidence": {
            "type": "metric",
            "location": "coverage/components/auth/",
            "snippet": "Statements: 95.3%, Branches: 92.1%"
          },
          "tags": ["testing", "unit-tests", "coverage"],
          "timestamp": "2025-11-15T20:30:20Z"
        },
        {
          "id": "obs-c3-004",
          "category": "maintainability",
          "severity": "warning",
          "description": "AuthService class has high cyclomatic complexity (25)",
          "evidence": {
            "type": "metric",
            "location": "src/components/auth/auth.service.ts",
            "snippet": "Cyclomatic complexity: 25 (threshold: 10)"
          },
          "tags": ["complexity", "refactoring", "code-quality"],
          "timestamp": "2025-11-15T20:30:25Z"
        }
      ],
      "relations": [
        {
          "id": "rel-c3-001",
          "source": "auth-component",
          "target": "user-component",
          "type": "dependency",
          "direction": "unidirectional",
          "description": "Imports UserService to fetch user data during authentication",
          "protocol": {
            "method": "Direct import",
            "endpoint": "src/components/user/user.service",
            "format": "TypeScript class",
            "authentication": "N/A"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": true
          },
          "tags": ["dependency", "service-layer"]
        },
        {
          "id": "rel-c3-002",
          "source": "auth-component",
          "target": "token-component",
          "type": "calls",
          "direction": "bidirectional",
          "description": "Uses TokenService to generate and validate JWT tokens",
          "protocol": {
            "method": "Method calls",
            "endpoint": "TokenService.generate(), TokenService.validate()",
            "format": "Function calls",
            "authentication": "N/A"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": true
          },
          "tags": ["jwt", "token-management"]
        }
      ]
    },
    {
      "id": "user-component",
      "name": "User Management Component",
      "description": "Manages user CRUD operations and profile data",
      "container": "express-api",
      "path": "src/components/user",
      "observations": [
        {
          "id": "obs-c3-005",
          "category": "architectural",
          "severity": "info",
          "description": "Follows Repository pattern for data access abstraction",
          "evidence": {
            "type": "pattern",
            "location": "src/components/user/",
            "snippet": "user.repository.ts, user.service.ts, user.controller.ts"
          },
          "tags": ["repository-pattern", "layered-architecture"],
          "timestamp": "2025-11-15T20:30:30Z"
        },
        {
          "id": "obs-c3-006",
          "category": "data",
          "severity": "info",
          "description": "User entity includes 15 fields with proper validation decorators",
          "evidence": {
            "type": "code",
            "location": "src/components/user/user.entity.ts",
            "snippet": "@IsEmail() email: string; @MinLength(8) password: string;"
          },
          "tags": ["entity", "validation", "class-validator"],
          "timestamp": "2025-11-15T20:30:35Z"
        },
        {
          "id": "obs-c3-007",
          "category": "performance",
          "severity": "warning",
          "description": "N+1 query problem in getUsersWithOrders method",
          "evidence": {
            "type": "code",
            "location": "src/components/user/user.repository.ts",
            "snippet": "users.map(user => getOrders(user.id))"
          },
          "tags": ["n+1", "query-optimization", "performance"],
          "timestamp": "2025-11-15T20:30:40Z"
        }
      ],
      "relations": [
        {
          "id": "rel-c3-003",
          "source": "user-component",
          "target": "order-component",
          "type": "calls",
          "direction": "unidirectional",
          "description": "Fetches user order history from OrderService",
          "protocol": {
            "method": "Method call",
            "endpoint": "OrderService.getOrdersByUserId()",
            "format": "Function call",
            "authentication": "N/A"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "medium",
            "critical": false
          },
          "tags": ["service-call", "cross-component"]
        }
      ]
    },
    {
      "id": "order-component",
      "name": "Order Management Component",
      "description": "Handles order creation, updates, and fulfillment",
      "container": "express-api",
      "path": "src/components/order",
      "observations": [
        {
          "id": "obs-c3-008",
          "category": "architectural",
          "severity": "info",
          "description": "Implements State pattern for order status management",
          "evidence": {
            "type": "pattern",
            "location": "src/components/order/states/",
            "snippet": "PendingState, ProcessingState, CompletedState classes"
          },
          "tags": ["state-pattern", "design-pattern"],
          "timestamp": "2025-11-15T20:30:45Z"
        },
        {
          "id": "obs-c3-009",
          "category": "integration",
          "severity": "info",
          "description": "Integrates with external payment gateway via PaymentClient",
          "evidence": {
            "type": "code",
            "location": "src/components/order/payment.client.ts",
            "snippet": "axios.post('https://api.stripe.com/v1/charges')"
          },
          "tags": ["payment", "external-api", "stripe"],
          "timestamp": "2025-11-15T20:30:50Z"
        },
        {
          "id": "obs-c3-010",
          "category": "testing",
          "severity": "warning",
          "description": "Missing integration tests for payment workflow",
          "evidence": {
            "type": "file",
            "location": "src/components/order/__tests__/",
            "snippet": "Only unit tests found, no integration tests"
          },
          "tags": ["testing", "integration-tests", "coverage"],
          "timestamp": "2025-11-15T20:30:55Z"
        }
      ],
      "relations": [
        {
          "id": "rel-c3-004",
          "source": "order-component",
          "target": "product-component",
          "type": "dependency",
          "direction": "unidirectional",
          "description": "Imports ProductService to validate product availability",
          "protocol": {
            "method": "Direct import",
            "endpoint": "src/components/product/product.service",
            "format": "TypeScript class",
            "authentication": "N/A"
          },
          "metadata": {
            "synchronous": true,
            "frequency": "high",
            "critical": true
          },
          "tags": ["validation", "product-check"]
        },
        {
          "id": "rel-c3-005",
          "source": "order-component",
          "target": "notification-component",
          "type": "calls",
          "direction": "unidirectional",
          "description": "Triggers email notifications on order status changes",
          "protocol": {
            "method": "Method call",
            "endpoint": "NotificationService.sendOrderConfirmation()",
            "format": "Function call",
            "authentication": "N/A"
          },
          "metadata": {
            "synchronous": false,
            "frequency": "medium",
            "critical": false
          },
          "tags": ["notifications", "async"]
        }
      ]
    },
    {
      "id": "product-component",
      "name": "Product Catalog Component",
      "description": "Manages product listings, inventory, and search",
      "container": "express-api",
      "path": "src/components/product",
      "observations": [
        {
          "id": "obs-c3-011",
          "category": "performance",
          "severity": "info",
          "description": "Implements full-text search using PostgreSQL tsvector",
          "evidence": {
            "type": "code",
            "location": "src/components/product/product.repository.ts",
            "snippet": "to_tsvector('english', name || ' ' || description)"
          },
          "tags": ["search", "full-text-search", "postgresql"],
          "timestamp": "2025-11-15T20:31:00Z"
        },
        {
          "id": "obs-c3-012",
          "category": "scalability",
          "severity": "info",
          "description": "Product images stored in S3 with CloudFront CDN distribution",
          "evidence": {
            "type": "code",
            "location": "src/components/product/image.service.ts",
            "snippet": "s3.putObject({ Bucket: 'products', Key: imageKey })"
          },
          "tags": ["s3", "cdn", "cloudfront", "images"],
          "timestamp": "2025-11-15T20:31:05Z"
        }
      ],
      "relations": []
    },
    {
      "id": "notification-component",
      "name": "Notification Component",
      "description": "Handles email and push notifications",
      "container": "express-api",
      "path": "src/components/notification",
      "observations": [
        {
          "id": "obs-c3-013",
          "category": "integration",
          "severity": "info",
          "description": "Uses SendGrid API for transactional emails",
          "evidence": {
            "type": "code",
            "location": "src/components/notification/email.service.ts",
            "snippet": "sgMail.send({ to, from, subject, html })"
          },
          "tags": ["sendgrid", "email", "notifications"],
          "timestamp": "2025-11-15T20:31:10Z"
        },
        {
          "id": "obs-c3-014",
          "category": "architectural",
          "severity": "info",
          "description": "Implements Template Method pattern for notification types",
          "evidence": {
            "type": "pattern",
            "location": "src/components/notification/templates/",
            "snippet": "AbstractNotificationTemplate, EmailTemplate, PushTemplate"
          },
          "tags": ["template-method", "design-pattern"],
          "timestamp": "2025-11-15T20:31:15Z"
        }
      ],
      "relations": []
    },
    {
      "id": "token-component",
      "name": "Token Management Component",
      "description": "JWT token generation and validation",
      "container": "express-api",
      "path": "src/components/token",
      "observations": [
        {
          "id": "obs-c3-015",
          "category": "security",
          "severity": "info",
          "description": "Implements token rotation with refresh tokens",
          "evidence": {
            "type": "code",
            "location": "src/components/token/token.service.ts",
            "snippet": "generateAccessToken(), generateRefreshToken(), rotateTokens()"
          },
          "tags": ["jwt", "token-rotation", "security"],
          "timestamp": "2025-11-15T20:31:20Z"
        },
        {
          "id": "obs-c3-016",
          "category": "security",
          "severity": "critical",
          "description": "Refresh tokens stored in database without encryption",
          "evidence": {
            "type": "code",
            "location": "src/components/token/token.repository.ts",
            "snippet": "INSERT INTO refresh_tokens (token, user_id) VALUES (?, ?)"
          },
          "tags": ["security", "encryption", "vulnerability"],
          "timestamp": "2025-11-15T20:31:25Z"
        }
      ],
      "relations": []
    }
  ]
}
```

### C3 Observations Characteristics

- **Focus**: Component-level implementation details and code quality
- **Categories**: Design patterns, code metrics, testing, dependencies
- **Granularity**: Low-level, operational observations
- **Evidence**: Code snippets, test coverage, complexity metrics

### C3 Relations Characteristics

- **Focus**: Inter-component dependencies and function calls
- **Types**: Direct imports, method calls, composition, inheritance
- **Details**: Import paths, function signatures, call patterns
- **Scope**: Within container boundaries

---

## Validation Rules

### Observations Validation

1. **Required Fields**:
   - `id` must be unique within the JSON file
   - `category` must be from enum list
   - `description` must be minimum 10 characters

2. **ID Format**:
   - C1: `obs-c1-NNN` (e.g., `obs-c1-001`)
   - C2: `obs-c2-NNN` (e.g., `obs-c2-015`)
   - C3: `obs-c3-NNN` (e.g., `obs-c3-042`)

3. **Category Validation**:
   - Must be one of the predefined categories
   - Should align with C4 level (architectural at C1, technical at C2, code-level at C3)

4. **Severity Validation**:
   - Must be "info", "warning", or "critical"
   - Critical severity requires justification in description

5. **Evidence Validation**:
   - If provided, `type` must be from enum
   - `location` should be valid file path (relative to repository root)
   - `snippet` should be non-empty if provided

6. **Timestamp Validation**:
   - Must be ISO 8601 format
   - Should be after parent JSON file timestamp
   - Should be before current time

### Relations Validation

1. **Required Fields**:
   - `id` must be unique within the JSON file
   - `source` must reference a valid entity ID in parent context
   - `target` must reference a valid entity ID (can be in same or different JSON)
   - `type` must be from enum list
   - `description` must be minimum 10 characters

2. **ID Format**:
   - C1: `rel-c1-NNN` (e.g., `rel-c1-001`)
   - C2: `rel-c2-NNN` (e.g., `rel-c2-015`)
   - C3: `rel-c3-NNN` (e.g., `rel-c3-042`)

3. **Reference Validation** (Graph Validity):
   - `target` must be a valid entity ID
   - For C1: target can be any system ID
   - For C2: target should be container ID (can reference external systems)
   - For C3: target should be component ID (can reference external components)
   - No self-references (source != target)
   - No dangling references

4. **Type Validation**:
   - Must be one of the predefined relation types
   - Should align with C4 level and context
   - C1: Prefer system-level types (http-rest, grpc, message-queue)
   - C2: Prefer container-level types (database-query, websocket)
   - C3: Prefer code-level types (dependency, calls, inheritance)

5. **Direction Validation**:
   - Must be "unidirectional" or "bidirectional"
   - Bidirectional relations should have reciprocal relation in target entity

6. **Protocol Validation**:
   - If `type` is HTTP-based, protocol should include method and endpoint
   - If `type` is database, protocol should include connection details
   - Authentication should be specified for external relations

### Cross-File Validation

1. **Timestamp Ordering**:
   - c1-systems.json timestamp > init.json timestamp
   - c2-containers.json timestamp > c1-systems.json timestamp
   - c3-components.json timestamp > c2-containers.json timestamp

2. **Parent Reference Validation**:
   - C2 containers must reference valid C1 system IDs
   - C3 components must reference valid C2 container IDs

3. **Relation Target Validation**:
   - All relation targets must resolve to valid entities
   - Can reference entities in same or previous levels
   - External entities (not in JSON files) should be clearly marked

### Validation Script Usage

```bash
# Validate observations and relations in c1-systems.json
python ${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-c1-systems.py knowledge-base/c1-systems.json

# Validate observations and relations in c2-containers.json
python ${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-c2-containers.py knowledge-base/c2-containers.json

# Validate observations and relations in c3-components.json
python ${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-c3-components.py knowledge-base/c3-components.json
```

**Exit Codes**:
- `0` - All observations and relations valid
- `1` - Non-blocking warnings (e.g., missing optional fields)
- `2` - Blocking errors (e.g., invalid references, missing required fields)

---

## Markdown Conversion

### How c4model-writer Parses Observations

The `c4model-writer` agent converts observations from JSON to markdown using this process:

1. **Load JSON file** (c1-systems.json, c2-containers.json, or c3-components.json)
2. **For each entity** (system/container/component):
   - Read observations array
   - Group by category
   - Sort by severity (critical → warning → info)
3. **Generate markdown sections**:
   - Create "## Observations" heading
   - For each category with observations:
     - Create "### [Category]" subheading
     - For each observation:
       - Create bullet point with description
       - Add severity badge if warning/critical
       - Include evidence as nested code block if present
       - Add tags as inline badges

**Example Markdown Output**:

```markdown
## Observations

### Architectural

- Single Page Application (SPA) architecture using React framework
  ```typescript
  // Evidence: package.json
  "react": "^18.2.0"
  ```
  Tags: `react` `spa` `frontend`

### Security

- ⚠️ **WARNING**: Authentication handled client-side with JWT tokens stored in localStorage
  ```typescript
  // Evidence: src/auth/AuthService.ts
  localStorage.setItem('token', jwt)
  ```
  Tags: `authentication` `jwt` `security`

### Performance

- Uses code splitting and lazy loading for optimal bundle size
  ```typescript
  // Evidence: src/App.tsx
  const Dashboard = lazy(() => import('./pages/Dashboard'))
  ```
  Tags: `performance` `code-splitting` `optimization`
```

### How c4model-writer Parses Relations

The `c4model-writer` agent converts relations from JSON to markdown using this process:

1. **Load JSON file**
2. **For each entity**:
   - Read relations array
   - Sort by type, then by target
3. **Generate markdown table**:
   - Create "## Relations" heading
   - Create table with columns: Target | Type | Description | Details
   - For each relation:
     - Add row with target ID/name
     - Add relation type as badge
     - Add description
     - Add protocol details if present

**Example Markdown Output**:

```markdown
## Relations

| Target | Type | Description | Details |
|--------|------|-------------|---------|
| api-backend | `http-rest` | Fetches product catalog, user data, and order information via REST API | **Method**: GET, POST, PUT, DELETE<br>**Endpoint**: `/api/v1/*`<br>**Format**: JSON<br>**Auth**: JWT Bearer Token<br>**Critical**: Yes |
| payment-gateway | `http-rest` | Processes payments through external payment gateway (Stripe) | **Method**: POST<br>**Endpoint**: `https://api.stripe.com/v1/charges`<br>**Format**: JSON<br>**Auth**: API Key<br>**Critical**: Yes |
| cdn | `http-rest` | Loads static assets (images, fonts) from CDN | **Method**: GET<br>**Endpoint**: `https://cdn.example.com/assets/*`<br>**Format**: Binary<br>**Auth**: None |
```

### Markdown Template Mapping

The markdown template (e.g., `c1-markdown-template.md`) defines HOW to structure the markdown:

```yaml
sections:
  - heading: "Observations"
    format: "grouped-by-category"  # Group observations by category
    severity-badges: true           # Show severity as badges
    include-evidence: true          # Include evidence as code blocks
    include-tags: true              # Show tags as inline badges
    
  - heading: "Relations"
    format: "table"                 # Render as markdown table
    columns:                        # Table columns
      - "Target"
      - "Type"
      - "Description"
      - "Details"
    include-protocol: true          # Include protocol details
    include-metadata: true          # Include metadata (critical, frequency)
```

### basic-memory MCP Integration

The `c4model-writer` agent stores documentation in basic-memory MCP:

1. **Create Knowledge Note**:
   - Note ID: `{system-id}-c1`, `{container-id}-c2`, `{component-id}-c3`
   - Title: Entity name
   - Content: Generated markdown
   - Tags: Extract from observations and relations

2. **Store Observations as Searchable Data**:
   - Each observation becomes a searchable fact in basic-memory
   - Tags enable filtering (e.g., "show all security observations")

3. **Store Relations as Graph**:
   - Relations stored as edges in knowledge graph
   - Enable queries like "show all dependencies of component X"

4. **Enable Cross-Linking**:
   - Relations generate markdown links between notes
   - Click target ID to navigate to target documentation

**Example MCP Storage**:

```typescript
// Store system documentation in basic-memory
await basicMemory.createNote({
  id: "web-frontend-c1",
  title: "Web Frontend System",
  content: generatedMarkdown,
  tags: ["react", "spa", "frontend", "security", "authentication"],
  metadata: {
    level: "c1",
    entityId: "web-frontend",
    observationCount: 4,
    relationCount: 3
  }
});

// Store relations as graph edges
for (const relation of relations) {
  await basicMemory.createRelation({
    source: "web-frontend-c1",
    target: `${relation.target}-c1`,
    type: relation.type,
    metadata: relation.protocol
  });
}
```

---

## Summary

### Key Design Decisions

1. **Structured Observations**: Objects instead of strings for better categorization
2. **Comprehensive Relations**: Include protocol details and metadata
3. **Consistent Schema**: Same structure across C1, C2, C3
4. **Graph Validity**: Strict validation of relation targets
5. **Evidence Support**: Link observations to code/config sources
6. **Severity Levels**: Prioritize critical findings
7. **Markdown-Ready**: Structure optimized for documentation generation

### Implementation Checklist

- [ ] Update JSON schemas with observations/relations structures
- [ ] Update validation scripts to check new fields
- [ ] Update c4model-writer to parse new observation format
- [ ] Update c4model-writer to generate enhanced markdown
- [ ] Update markdown templates with new sections
- [ ] Test with sample data at all C4 levels
- [ ] Document schema in plugin README files

### Validation Responsibilities

| Script | Validates |
|--------|-----------|
| `validate-c1-systems.py` | C1 observations format, C1 relations graph validity |
| `validate-c2-containers.py` | C2 observations format, C2 relations graph validity, parent references |
| `validate-c3-components.py` | C3 observations format, C3 relations graph validity, parent references |
| `validate-markdown.py` | Markdown structure, observations rendering, relations tables |

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Status**: Schema Design Complete - Ready for Implementation
