# Observation Documentation Reference

**Complete guide for documenting architectural observations across C1, C2, and C3 levels.**

---

## Table of Contents

1. [Category Definitions](#category-definitions)
2. [Evidence Collection Guidelines](#evidence-collection-guidelines)
3. [Severity Level Best Practices](#severity-level-best-practices)
4. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
5. [Cross-Level Consistency](#cross-level-consistency)
6. [Validation Requirements](#validation-requirements)

---

## Category Definitions

### C1 System Context Categories

#### architecture
**Definition:** Overall system architecture patterns, styles, and strategic decisions.

**What to document:**
- Architectural styles (monolith, microservices, event-driven, layered)
- System decomposition approach
- Major architectural patterns (CQRS, event sourcing, etc.)
- High-level structural decisions

**Examples:**
- "Event-driven architecture with message queues"
- "Microservices architecture with API gateway"
- "Monolithic layered architecture"

---

#### integration
**Definition:** How systems integrate and communicate with each other.

**What to document:**
- Integration patterns (REST, GraphQL, gRPC, messaging)
- API contracts and interfaces
- Data exchange formats
- Synchronous vs asynchronous communication

**Examples:**
- "Systems communicate via REST APIs over HTTPS"
- "Event-driven integration using RabbitMQ"
- "GraphQL gateway for unified API access"

---

#### boundaries
**Definition:** System scope, ownership boundaries, and organizational limits.

**What to document:**
- What's inside vs outside the system
- Team ownership boundaries
- Deployment boundaries
- Network boundaries (public/private/DMZ)

**Examples:**
- "System boundary includes web app and API, excludes database"
- "Frontend team owns UI system, backend team owns API system"

---

#### security
**Definition:** System-level security concerns, authentication, and authorization.

**What to document:**
- Authentication mechanisms (OAuth, JWT, SAML)
- Authorization approaches (RBAC, ABAC)
- Security vulnerabilities
- Data protection strategies

**Examples:**
- "JWT-based authentication with OAuth2"
- "No rate limiting on public API endpoints"
- "TLS encryption for all inter-system communication"

---

#### scalability
**Definition:** System's ability to scale and handle growth.

**What to document:**
- Horizontal vs vertical scaling approaches
- Scaling limitations
- Load balancing strategies
- Stateless vs stateful design

**Examples:**
- "Horizontally scalable via container orchestration"
- "Vertical scaling limited by database constraints"
- "Stateless design enables cloud auto-scaling"

---

#### actors
**Definition:** User types and external actors interacting with the system.

**What to document:**
- User personas and roles
- External systems acting as users
- Actor permissions and capabilities

**Examples:**
- "Three user types: Customer, Admin, Support Agent"
- "External audit system queries via API"

---

#### external-dependencies
**Definition:** Third-party systems, services, and critical external dependencies.

**What to document:**
- SaaS services and APIs
- Third-party integrations
- Dependency criticality
- Fallback mechanisms

**Examples:**
- "Critical dependency on Stripe payment gateway"
- "SendGrid for email, with fallback to AWS SES"
- "No fallback for authentication via Auth0"

---

#### deployment
**Definition:** Infrastructure, hosting, and deployment approaches.

**What to document:**
- Cloud vs on-premise
- Deployment strategies (blue-green, canary)
- Infrastructure as code
- Container orchestration

**Examples:**
- "Deployed on AWS using Kubernetes"
- "Blue-green deployment strategy with Terraform"
- "On-premise deployment with Docker Swarm"

---

#### data-flow
**Definition:** How data moves between systems and external actors.

**What to document:**
- Data flow directions
- Data transformations
- Data formats
- Real-time vs batch processing

**Examples:**
- "User data flows from web app to API to database"
- "Analytics data streamed to data warehouse via Kafka"

---

### C2 Container Categories

#### technology
**Definition:** Technology stack, frameworks, libraries, and languages.

**What to document:**
- Programming languages
- Frameworks and libraries
- Runtime environments
- Major dependencies

**Examples:**
- "React 18 SPA with Redux Toolkit"
- "Node.js 18 with Express.js framework"
- "Python 3.11 with FastAPI"

---

#### runtime
**Definition:** Runtime characteristics, environment, and execution context.

**What to document:**
- Runtime environment (Node.js, JVM, .NET)
- Process model (single-threaded, multi-threaded)
- Memory and resource requirements
- Environment variables

**Examples:**
- "Single-threaded Node.js event loop"
- "JVM with 4GB heap size"
- "Requires 16 environment variables"

---

#### communication
**Definition:** Inter-container communication protocols and patterns.

**What to document:**
- Communication protocols (HTTP, gRPC, WebSocket)
- API styles (REST, GraphQL)
- Message formats (JSON, Protobuf)
- Communication patterns (request/response, pub/sub)

**Examples:**
- "REST API with JSON payloads"
- "gRPC with Protobuf serialization"
- "WebSocket for real-time updates"

---

#### data-storage
**Definition:** Databases, caches, and storage mechanisms.

**What to document:**
- Database types (relational, NoSQL, graph)
- Caching strategies
- Storage technologies
- Data persistence approaches

**Examples:**
- "PostgreSQL 14 for relational data"
- "Redis for session caching"
- "MongoDB for document storage"

---

#### authentication
**Definition:** Container-level authentication and authorization.

**What to document:**
- Authentication mechanisms
- Token management
- Session handling
- Authorization strategies

**Examples:**
- "JWT bearer token authentication"
- "Session cookies with Redis storage"
- "API key authentication for service-to-service"

---

#### deployment
**Definition:** Container deployment strategies and configurations.

**What to document:**
- Containerization (Docker, etc.)
- Orchestration (Kubernetes, Docker Swarm)
- Deployment pipelines
- Health checks and readiness probes

**Examples:**
- "Docker container deployed on Kubernetes"
- "Health check endpoint at /health"
- "Blue-green deployment via ArgoCD"

---

#### scalability
**Definition:** Container-level scaling capabilities.

**What to document:**
- Horizontal pod autoscaling
- Replica counts
- Resource limits
- Scaling triggers

**Examples:**
- "Auto-scales 2-10 pods based on CPU"
- "Stateless design enables horizontal scaling"
- "Limited by database connection pool size"

---

#### performance
**Definition:** Container performance characteristics and optimizations.

**What to document:**
- Response times
- Throughput capacity
- Resource utilization
- Performance optimizations

**Examples:**
- "Average response time: 50ms"
- "Code splitting and lazy loading implemented"
- "Database queries not optimized with indexes"

---

#### dependencies
**Definition:** Container dependencies on other containers or services.

**What to document:**
- Direct dependencies
- Dependency versions
- Dependency criticality
- Coupling strength

**Examples:**
- "Depends on API container and Redis cache"
- "Critical dependency on database"
- "Loose coupling via message queue"

---

#### configuration
**Definition:** Configuration management approaches.

**What to document:**
- Configuration sources (env vars, config files, config servers)
- Secret management
- Feature flags
- Configuration validation

**Examples:**
- "Configuration via environment variables"
- "Secrets stored in Kubernetes secrets"
- "Feature flags managed in LaunchDarkly"

---

#### monitoring
**Definition:** Observability, logging, and monitoring.

**What to document:**
- Logging frameworks and formats
- Metrics collection
- Tracing and APM
- Alerting

**Examples:**
- "Winston logger with JSON format"
- "Prometheus metrics exposed at /metrics"
- "No distributed tracing implemented"

---

### C3 Component Categories

#### design-patterns
**Definition:** Design patterns and architectural patterns in code.

**What to document:**
- Creational patterns (Factory, Singleton, Builder)
- Structural patterns (Adapter, Decorator, Facade)
- Behavioral patterns (Observer, Strategy, Command)
- Domain patterns (Repository, Service, Entity)

**Examples:**
- "Repository pattern for data access"
- "Factory pattern for creating services"
- "Observer pattern for event handling"

---

#### code-structure
**Definition:** Code organization, modularity, and file structure.

**What to document:**
- Directory structure
- Module organization
- File naming conventions
- Code grouping strategies

**Examples:**
- "Feature-based directory structure"
- "Layered architecture: controllers/services/repositories"
- "Modules organized by domain"

---

#### dependencies
**Definition:** Component-level imports and dependencies.

**What to document:**
- Import patterns
- Circular dependencies
- Dependency injection
- Module coupling

**Examples:**
- "Dependency injection via constructor"
- "Circular dependency between User and Order modules"
- "Heavy reliance on utility modules"

---

#### error-handling
**Definition:** Error handling strategies and patterns.

**What to document:**
- Try-catch usage
- Error propagation
- Error logging
- Custom error types

**Examples:**
- "No error handling in async operations"
- "Custom error classes for domain errors"
- "Global error handler middleware"

---

#### testing
**Definition:** Test coverage, quality, and strategies.

**What to document:**
- Unit test coverage
- Integration tests
- Test frameworks
- Test quality

**Examples:**
- "85% unit test coverage with Jest"
- "No integration tests"
- "Tests use actual database instead of mocks"

---

#### performance
**Definition:** Algorithm efficiency and code-level optimizations.

**What to document:**
- Algorithm complexity
- Performance bottlenecks
- Optimization techniques
- Resource usage

**Examples:**
- "O(n²) algorithm for data processing"
- "Memoization used for expensive calculations"
- "No caching of computed values"

---

#### security
**Definition:** Security implementation details in code.

**What to document:**
- Input validation
- Output encoding
- Secret handling
- Vulnerability patterns

**Examples:**
- "SQL injection vulnerability in query builder"
- "JWT tokens stored in localStorage"
- "Input validation using Joi schema"

---

#### code-quality
**Definition:** Code quality metrics and standards.

**What to document:**
- Code complexity
- Code duplication
- Naming conventions
- Code style

**Examples:**
- "High cyclomatic complexity (>20)"
- "Consistent naming conventions followed"
- "Significant code duplication in controllers"

---

#### documentation
**Definition:** Code documentation quality and coverage.

**What to document:**
- JSDoc/TSDoc comments
- README files
- API documentation
- Inline comments

**Examples:**
- "Comprehensive JSDoc for all public APIs"
- "No documentation for complex algorithms"
- "README outdated, doesn't match implementation"

---

#### complexity
**Definition:** Code complexity measurements.

**What to document:**
- Cyclomatic complexity
- Cognitive complexity
- Function length
- Nesting depth

**Examples:**
- "Function with cyclomatic complexity of 45"
- "Deep nesting (6 levels) in conditional logic"
- "Functions average 150 lines (too long)"

---

#### coupling
**Definition:** Degree of interdependence between components.

**What to document:**
- Tight vs loose coupling
- Coupling to external libraries
- Coupling to infrastructure
- Circular dependencies

**Examples:**
- "Tight coupling to ORM throughout codebase"
- "Components loosely coupled via interfaces"
- "Direct database access in UI components"

---

#### cohesion
**Definition:** How closely related component responsibilities are.

**What to document:**
- Single Responsibility Principle adherence
- Component focus
- Mixed concerns

**Examples:**
- "High cohesion: each service has single responsibility"
- "Low cohesion: AuthService handles auth, logging, and config"

---

#### maintainability
**Definition:** How easy it is to maintain and modify the code.

**What to document:**
- Code readability
- Modification complexity
- Technical debt
- Refactoring needs

**Examples:**
- "High maintainability with clear separation of concerns"
- "Technical debt: hardcoded values throughout"
- "Difficult to modify due to tight coupling"

---

## Evidence Collection Guidelines

### Best Practices

1. **Always provide file paths**
   - Use relative paths from repository root
   - Include line numbers for code snippets: `src/auth.ts:45-52`
   - For directories, use trailing slash: `src/controllers/`

2. **Keep snippets concise**
   - 1-10 lines maximum
   - Focus on the relevant part
   - Use `...` to indicate omitted code

3. **Match evidence type to content**
   - `file` - For file/directory existence: `package.json`, `src/config/`
   - `code` - For actual code snippets
   - `config` - For configuration values: `.env`, `docker-compose.yml`
   - `pattern` - For architectural patterns without specific file
   - `metric` - For quantitative measurements
   - `dependency` - For package dependencies from manifests

4. **Add context with notes**
   - Explain what the evidence shows
   - Clarify non-obvious connections
   - Provide additional context

### Evidence Examples

**Good file evidence:**
```json
{
  "type": "file",
  "location": "src/repositories/UserRepository.ts",
  "note": "Repository pattern implementation"
}
```

**Good code evidence:**
```json
{
  "type": "code",
  "location": "src/auth/AuthService.ts:45-47",
  "snippet": "localStorage.setItem('token', jwt);\nconst decoded = jwtDecode(jwt);\nreturn decoded;",
  "note": "JWT stored in localStorage, vulnerable to XSS"
}
```

**Good config evidence:**
```json
{
  "type": "config",
  "location": "docker-compose.yml:15-18",
  "snippet": "redis:\n  image: redis:7-alpine\n  ports:\n    - '6379:6379'",
  "note": "Redis configured for caching"
}
```

**Good pattern evidence:**
```json
{
  "type": "pattern",
  "location": "src/services/",
  "note": "Service layer pattern with dependency injection throughout codebase"
}
```

---

## Severity Level Best Practices

### Critical Severity

**Use for:**
- **Security vulnerabilities**: XSS, SQL injection, exposed secrets, insecure authentication
- **Data loss risks**: No backups, data deletion without confirmation
- **System unavailability**: Single points of failure, no failover
- **Critical bugs**: Core functionality broken, data corruption

**Checklist:**
- ✅ Does this pose immediate risk to security, data, or availability?
- ✅ Could this result in data breach or data loss?
- ✅ Would this cause system downtime or service outage?
- ✅ Is immediate action required?

**Example:**
```json
{
  "severity": "critical",
  "title": "SQL injection vulnerability in user query",
  "description": "User input directly concatenated into SQL query without sanitization.",
  "impact": "Attackers can execute arbitrary SQL commands, access/modify all data",
  "recommendation": "Use parameterized queries immediately"
}
```

---

### Warning Severity

**Use for:**
- **Performance issues**: N+1 queries, inefficient algorithms, resource leaks
- **Code quality**: High complexity, duplication, poor naming
- **Missing best practices**: No error handling, no tests, deprecated dependencies
- **Architectural concerns**: Anti-patterns, tight coupling, violations of SOLID

**Checklist:**
- ✅ Should this be fixed but isn't immediately critical?
- ✅ Does this impact performance, maintainability, or scalability?
- ✅ Is this a violation of best practices?
- ✅ Could this become critical if left unaddressed?

**Example:**
```json
{
  "severity": "warning",
  "title": "Database connections not pooled",
  "description": "New database connection created for each request.",
  "impact": "High latency and connection exhaustion under load",
  "recommendation": "Implement connection pooling"
}
```

---

### Info Severity

**Use for:**
- **Design patterns**: Documented architectural patterns
- **Technology stack**: Frameworks and libraries in use
- **Good practices**: Well-implemented features
- **Architectural decisions**: Strategic technical choices
- **System capabilities**: Features and functionality

**Checklist:**
- ✅ Is this neutral or positive information?
- ✅ Does this document "what is" without judgment?
- ✅ Is this useful for understanding the system?
- ✅ Is no action required?

**Example:**
```json
{
  "severity": "info",
  "title": "Event-driven architecture with RabbitMQ",
  "description": "System uses message queues for async processing between services.",
  "impact": "Enables loose coupling and horizontal scaling"
}
```

---

## Anti-Patterns to Avoid

### 1. Opinion Instead of Fact

❌ **Bad:**
```json
{
  "description": "The authentication approach is poorly designed and should be refactored."
}
```

✅ **Good:**
```json
{
  "description": "JWT tokens stored in localStorage are vulnerable to XSS attacks.",
  "recommendation": "Migrate to httpOnly cookies"
}
```

---

### 2. Vague Observations

❌ **Bad:**
```json
{
  "title": "Performance issues",
  "description": "The system is slow."
}
```

✅ **Good:**
```json
{
  "title": "N+1 query problem in user dashboard",
  "description": "Dashboard loads user posts in a loop, executing one query per post instead of batching.",
  "evidence": [{"type": "code", "location": "src/dashboard.ts:78"}]
}
```

---

### 3. Missing Evidence

❌ **Bad:**
```json
{
  "title": "Uses event-driven architecture",
  "description": "The system has an event-driven design."
}
```

✅ **Good:**
```json
{
  "title": "Event-driven architecture with RabbitMQ",
  "description": "System uses RabbitMQ message broker for async event processing.",
  "evidence": [
    {"type": "config", "location": "docker-compose.yml", "snippet": "rabbitmq:..."},
    {"type": "dependency", "location": "package.json", "snippet": "\"amqplib\": \"^0.10.3\""}
  ]
}
```

---

### 4. Wrong Severity

❌ **Bad:**
```json
{
  "severity": "critical",
  "title": "Using older version of React",
  "description": "React 17 instead of React 18"
}
```

✅ **Good:**
```json
{
  "severity": "warning",
  "title": "React version outdated",
  "description": "Using React 17.0.2, missing React 18 performance improvements",
  "recommendation": "Upgrade to React 18 for concurrent features"
}
```

---

### 5. Wrong Category Level

❌ **Bad (C1 level):**
```json
{
  "category": "code-quality",
  "title": "High cyclomatic complexity in AuthService"
}
```

✅ **Good (C1 level):**
```json
{
  "category": "architecture",
  "title": "Microservices architecture with API gateway"
}
```

*Code quality is a C3 category; architecture is appropriate for C1*

---

## Cross-Level Consistency

### Observation Granularity

**C1 observations** should be high-level:
- System-wide patterns
- External integrations
- System boundaries
- Actor interactions

**C2 observations** should be mid-level:
- Container technologies
- Inter-container communication
- Container deployment
- Container-level performance

**C3 observations** should be detailed:
- Code patterns
- Component structure
- Implementation details
- Code quality metrics

### Avoid Duplication Across Levels

If the same observation applies to multiple levels, document it at the **highest appropriate level** and reference it at lower levels.

**Example:**
- C1: "System uses PostgreSQL for data persistence"
- C2: "API container connects to PostgreSQL database"
- C3: Don't repeat—focus on component-specific details like query patterns

---

## Validation Requirements

### Required Field Validation

1. **ID format**: Must match `^obs-[a-z0-9-]+$`
   - ✅ `obs-event-driven-arch`
   - ❌ `OBS-001`, `observation1`

2. **Category**: Must be valid for the C4 level
   - C1: 9 categories (architecture, integration, boundaries, ...)
   - C2: 12 categories (technology, runtime, communication, ...)
   - C3: 13 categories (design-patterns, code-structure, dependencies, ...)

3. **Severity**: Must be `critical`, `warning`, or `info`

4. **Title**: Max 100 characters, descriptive

5. **Description**: Min 10 characters, detailed

### Evidence Validation

1. **Type**: Must be valid evidence type
2. **Location**: Required, should be a valid path
3. **Snippet**: Optional but recommended
4. **Note**: Optional but helpful for context

### Recommendation Validation

- **Critical** observations MUST include `recommendation`
- **Warning** observations SHOULD include `recommendation`
- **Info** observations MAY include `recommendation`

---

## Additional Resources

- **[examples.md](examples.md)** - 30+ complete examples
- **[categories.md](categories.md)** - Category quick reference
- **Validation scripts** - `${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-*.py`
- **Type definitions** - `${CLAUDE_PLUGIN_ROOT}/validation/templates/types-observations.json`
