# Observation Categories Reference

**Quick reference guide for observation categories across C1, C2, and C3 levels.**

---

## Table of Contents

1. [C1 System Context Categories](#c1-system-context-categories)
2. [C2 Container Categories](#c2-container-categories)
3. [C3 Component Categories](#c3-component-categories)
4. [Category Selection Guide](#category-selection-guide)

---

## C1 System Context Categories

**Focus:** System-level architecture, external integrations, and high-level concerns.

### architecture
**Use for:** Overall system patterns, architectural styles, strategic decisions
**Examples:**
- Event-driven architecture with message queues
- Microservices architecture with API gateway
- Monolithic layered architecture
- CQRS pattern implementation

---

### integration
**Use for:** How systems communicate and integrate with each other
**Examples:**
- REST API communication over HTTPS
- GraphQL gateway for unified access
- Event-driven integration via message queues
- Service mesh for inter-service communication

---

### boundaries
**Use for:** System scope, ownership, organizational limits
**Examples:**
- System boundary includes web app and API
- Frontend team owns UI, backend team owns API
- Deployment boundary per service
- Network boundary: public vs private subnets

---

### security
**Use for:** System-level security, authentication, authorization
**Examples:**
- OAuth2 authentication via Auth0
- JWT-based authentication
- No rate limiting on public endpoints
- TLS encryption for all communications

---

### scalability
**Use for:** System's ability to scale and handle growth
**Examples:**
- Horizontally scalable via Kubernetes
- Auto-scaling based on CPU metrics
- Database sharding for horizontal scaling
- Stateless design enables cloud scaling

---

### actors
**Use for:** User types, roles, external actors
**Examples:**
- Three user roles: Customer, Admin, Support
- External audit system queries via API
- Mobile app acts as user of REST API
- Third-party integrations as system actors

---

### external-dependencies
**Use for:** Third-party systems, critical external services
**Examples:**
- Stripe payment gateway (critical)
- SendGrid email service with AWS SES fallback
- Auth0 for authentication (no fallback)
- Snowflake data warehouse for analytics

---

### deployment
**Use for:** Infrastructure, hosting, deployment strategies
**Examples:**
- AWS ECS Fargate deployment
- Kubernetes with blue-green deployments
- Multi-region active-active setup
- Infrastructure as code with Terraform

---

### data-flow
**Use for:** How data moves between systems
**Examples:**
- User data flows: web → API → database
- Analytics pipeline: app → Kafka → warehouse
- Batch ETL nightly to data lake
- Real-time streaming to analytics platform

---

## C2 Container Categories

**Focus:** Deployable units, runtime characteristics, technology stack.

### technology
**Use for:** Tech stack, frameworks, libraries, languages
**Examples:**
- React 18 SPA with Redux Toolkit
- Node.js 18 with Express.js
- Python FastAPI with SQLAlchemy
- .NET 7 with Entity Framework Core

---

### runtime
**Use for:** Runtime environment and characteristics
**Examples:**
- Node.js event loop (single-threaded)
- JVM with 4GB heap configuration
- Python 3.11 with uvicorn ASGI server
- Requires 16 environment variables

---

### communication
**Use for:** Inter-container protocols and patterns
**Examples:**
- REST API with JSON payloads
- gRPC with Protobuf serialization
- WebSocket for real-time updates
- Message queue for async communication

---

### data-storage
**Use for:** Databases, caches, storage mechanisms
**Examples:**
- PostgreSQL 14 for relational data
- Redis for session and caching
- MongoDB for document storage
- S3 for file storage

---

### authentication
**Use for:** Container-level auth and authorization
**Examples:**
- JWT bearer token authentication
- Session cookies with Redis storage
- API key for service-to-service auth
- OAuth2 client credentials flow

---

### deployment
**Use for:** Containerization, orchestration, deployment
**Examples:**
- Docker container on Kubernetes
- Health check at /health endpoint
- Blue-green deployment via ArgoCD
- Auto-scaling 2-10 replicas

---

### scalability
**Use for:** Container scaling capabilities
**Examples:**
- Horizontal pod autoscaling based on CPU
- Stateless design enables replication
- Limited by database connection pool
- Scales independently of other services

---

### performance
**Use for:** Container performance characteristics
**Examples:**
- Average response time: 50ms
- Code splitting and lazy loading
- Caching strategy reduces DB load
- No query optimization with indexes

---

### dependencies
**Use for:** Container dependencies on others
**Examples:**
- Depends on API container and Redis
- Critical dependency on PostgreSQL
- Loose coupling via message queue
- No direct database dependencies

---

### configuration
**Use for:** Configuration management approaches
**Examples:**
- Environment variables for config
- Kubernetes ConfigMaps and Secrets
- Feature flags in LaunchDarkly
- Config validation on startup

---

### monitoring
**Use for:** Observability, logging, monitoring
**Examples:**
- Winston logger with JSON format
- Prometheus metrics at /metrics
- OpenTelemetry distributed tracing
- No structured logging implemented

---

### security
**Use for:** Container-level security implementation
**Examples:**
- Container runs as non-root user
- Security scanning with Trivy
- Secrets injected via Kubernetes
- HTTPS only, no HTTP allowed

---

## C3 Component Categories

**Focus:** Code-level implementation, patterns, quality.

### design-patterns
**Use for:** Design patterns in code
**Examples:**
- Repository pattern for data access
- Factory pattern for service creation
- Singleton pattern for configuration
- Observer pattern for event handling

---

### code-structure
**Use for:** Code organization and modularity
**Examples:**
- Feature-based directory structure
- Layered architecture: controllers/services/repositories
- Domain-driven design modules
- Clean separation of concerns

---

### dependencies
**Use for:** Component imports and coupling
**Examples:**
- Dependency injection via constructor
- Circular dependency between modules
- Interface-based dependencies
- Heavy reliance on utility modules

---

### error-handling
**Use for:** Error handling strategies
**Examples:**
- Try-catch blocks in async operations
- Global error handler middleware
- Custom error classes for domain errors
- No error handling in critical paths

---

### testing
**Use for:** Test coverage and quality
**Examples:**
- 95% unit test coverage with Jest
- Integration tests for API endpoints
- No tests for edge cases
- Tests use mocks appropriately

---

### performance
**Use for:** Algorithm efficiency, optimization
**Examples:**
- O(n²) algorithm for data processing
- Memoization for expensive calculations
- N+1 query problem in data loading
- Efficient caching of computed values

---

### security
**Use for:** Security implementation in code
**Examples:**
- SQL injection vulnerability
- JWT tokens in localStorage (XSS risk)
- Input validation with Joi
- Output encoding prevents XSS

---

### code-quality
**Use for:** Code quality metrics
**Examples:**
- High cyclomatic complexity (>20)
- Consistent naming conventions
- Significant code duplication
- Clean, readable code

---

### documentation
**Use for:** Code documentation quality
**Examples:**
- Comprehensive JSDoc/TSDoc
- README files for each module
- No documentation for complex logic
- Inline comments explain why, not what

---

### complexity
**Use for:** Code complexity measurements
**Examples:**
- Function cyclomatic complexity: 45
- Deep nesting (6 levels) in conditionals
- Functions average 150 lines
- Cognitive complexity manageable

---

### coupling
**Use for:** Interdependence between components
**Examples:**
- Tight coupling to ORM throughout
- Loose coupling via interfaces
- Direct database access in UI
- Service layer properly abstracted

---

### cohesion
**Use for:** How related component responsibilities are
**Examples:**
- High cohesion: single responsibility
- Low cohesion: mixed concerns
- Each module has clear focus
- Service handles auth, logging, config (bad)

---

### maintainability
**Use for:** How easy to maintain and modify
**Examples:**
- High maintainability with clean separation
- Technical debt: hardcoded values
- Difficult to modify due to coupling
- Well-structured, easy to understand

---

## Category Selection Guide

### Decision Tree

**Question 1: What C4 level are you documenting?**

- **C1 (System Context)** → Use C1 categories
- **C2 (Container)** → Use C2 categories
- **C3 (Component)** → Use C3 categories

---

**Question 2: What aspect are you observing?**

#### C1 Level

| Observation About | Use Category |
|-------------------|--------------|
| Overall architecture pattern | `architecture` |
| How systems communicate | `integration` |
| What's in/out of system | `boundaries` |
| System-level auth/security | `security` |
| Scaling approach | `scalability` |
| Who uses the system | `actors` |
| Third-party services | `external-dependencies` |
| Where/how deployed | `deployment` |
| How data moves | `data-flow` |

---

#### C2 Level

| Observation About | Use Category |
|-------------------|--------------|
| Languages, frameworks | `technology` |
| Runtime environment | `runtime` |
| Container communication | `communication` |
| Databases, storage | `data-storage` |
| Auth mechanisms | `authentication` |
| Containerization | `deployment` |
| Container scaling | `scalability` |
| Container performance | `performance` |
| Container dependencies | `dependencies` |
| Config management | `configuration` |
| Logging, metrics | `monitoring` |
| Container security | `security` |

---

#### C3 Level

| Observation About | Use Category |
|-------------------|--------------|
| Design patterns used | `design-patterns` |
| Code organization | `code-structure` |
| Imports, dependencies | `dependencies` |
| Error handling approach | `error-handling` |
| Tests, coverage | `testing` |
| Algorithms, optimization | `performance` |
| Security in code | `security` |
| Code quality metrics | `code-quality` |
| Documentation | `documentation` |
| Code complexity | `complexity` |
| Component coupling | `coupling` |
| Component cohesion | `cohesion` |
| How easy to maintain | `maintainability` |

---

## Common Mistakes

### Using Wrong Level Category

❌ **Wrong:**
```json
{
  "level": "C1",
  "category": "code-quality"  // C3 category!
}
```

✅ **Right:**
```json
{
  "level": "C1",
  "category": "architecture"  // C1 category
}
```

---

### Too Granular for Level

❌ **Wrong (C1):**
```json
{
  "category": "architecture",
  "title": "Repository pattern in UserService"  // Too detailed!
}
```

✅ **Right (C1):**
```json
{
  "category": "architecture",
  "title": "Microservices architecture with API gateway"
}
```

---

### Not Granular Enough

❌ **Wrong (C3):**
```json
{
  "category": "design-patterns",
  "title": "Microservices architecture"  // Too high-level!
}
```

✅ **Right (C3):**
```json
{
  "category": "design-patterns",
  "title": "Repository pattern for data access"
}
```

---

## Category Counts

- **C1 System Context**: 9 categories
- **C2 Container**: 12 categories
- **C3 Component**: 13 categories

**Total**: 34 categories across all levels

---

## Related Resources

- **[SKILL.md](SKILL.md)** - Main skill documentation
- **[reference.md](reference.md)** - Comprehensive methodology
- **[examples.md](examples.md)** - 30+ examples with categories
