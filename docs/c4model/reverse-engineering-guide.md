# Reverse Engineering with C4 Model

> How to apply C4 abstraction levels to understand and document existing systems

## Overview

Reverse engineering a software system means **working backwards from the implementation to understand the architecture**. The C4 model provides an excellent framework for this because it gives you a structured approach to extract and document architecture at different levels of abstraction.

This guide shows you how to apply each C4 level to reverse engineer existing projects.

---

## The Reverse Engineering Process

### Traditional Approach (Bottom-Up)

```
Code → Components → Containers → System Context
  ↑         ↑            ↑              ↑
Start    Build up    Continue      Final picture
here     from code    abstracting   of system
```

### C4 Approach (Top-Down then Bottom-Up)

**Better strategy**: Combine both approaches!

```
1. Quick System Context (top-down survey)
        ↓
2. Identify Containers (deployment + code structure)
        ↓
3. Analyze Components (code organization)
        ↓
4. Refine all levels with discoveries
```

This hybrid approach is more efficient and gives you context before diving into details.

---

## Level 1: Reverse Engineering System Context

### Goal

Understand **how the system fits into the world** - what it depends on and who depends on it.

### Investigation Techniques

#### 1. Talk to People (Best Starting Point)

**Who to interview**:
- Developers who work on the system
- DevOps/operations team
- Product managers
- End users

**Questions to ask**:
- Who uses this system?
- What other systems does it integrate with?
- What external services does it depend on?
- What authentication/authorization is used?
- What are the main user roles?

#### 2. Review Documentation

**Look for**:
- Architecture diagrams (even if outdated)
- README files
- Wiki pages
- API documentation
- Deployment guides
- Onboarding documentation

**Files to check**:
```bash
README.md
docs/
wiki/
ARCHITECTURE.md
.docs/
confluence/ (if exported)
```

#### 3. Analyze Configuration Files

**Configuration reveals dependencies**:

**Environment files**:
```bash
# Look for external service URLs
.env
.env.example
config/
application.yml
application.properties
settings.py
config.json
```

**Example discoveries from .env**:
```bash
# Database (external system)
DATABASE_URL=postgresql://...

# Payment gateway (external system)
STRIPE_API_KEY=...
PAYMENT_GATEWAY_URL=https://api.stripe.com

# Email service (external system)
SENDGRID_API_KEY=...
EMAIL_SERVICE_URL=...

# Authentication (external system or internal?)
AUTH0_DOMAIN=...
OAUTH_PROVIDER=...

# External APIs
GOOGLE_MAPS_API_KEY=...
AWS_S3_BUCKET=...
```

**Docker and deployment files**:
```bash
docker-compose.yml      # Shows services and dependencies
Dockerfile              # Shows base images and dependencies
kubernetes/*.yaml       # Shows deployed services
terraform/              # Shows infrastructure dependencies
```

#### 4. Network Analysis

**Monitor network traffic**:
```bash
# Check what the application connects to
netstat -an | grep ESTABLISHED
lsof -i -P -n

# Monitor HTTP requests (if web app)
# Use browser DevTools → Network tab
# or tcpdump, Wireshark
```

**API Gateway/Proxy logs**:
- Nginx access logs
- API Gateway logs
- Load balancer logs

#### 5. Code Analysis for External Dependencies

**Search for external service clients**:
```bash
# Search for HTTP clients
rg -i "http://" -g "*.{js,ts,py,java,go}"
rg -i "https://" -g "*.{js,ts,py,java,go}"

# Search for SDK imports
rg "import.*sdk" -g "*.{js,ts}"
rg "from.*client import" -g "*.py"

# Search for API clients
rg -i "client|api|gateway|service" -g "*.{js,ts,py,java,go}"
```

**Package dependencies**:
```bash
# JavaScript/TypeScript
cat package.json | jq '.dependencies'

# Python
cat requirements.txt
cat Pipfile

# Java
cat pom.xml
cat build.gradle

# Go
cat go.mod

# Ruby
cat Gemfile

# .NET
cat *.csproj
```

**Look for SDKs**:
- AWS SDK → Uses AWS services
- Stripe SDK → Payment processing
- Twilio SDK → SMS/communications
- SendGrid SDK → Email service
- etc.

### Documentation Template

Create a System Context diagram showing:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  [Person: End User]                             │
│         │                                       │
│         ↓ Uses                                  │
│  ┌──────────────────┐                           │
│  │  [Your System]   │──→ Sends email ──→ [SendGrid]
│  │   "Description"  │                           │
│  └──────────────────┘──→ Processes ───→ [Stripe]
│         │              payments                 │
│         ↓ Stores data                           │
│  [Database System]                              │
│         │                                       │
│  [Person: Admin]                                │
│         │                                       │
│         ↓ Manages                               │
│  [Your System]                                  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Document format**:
```markdown
# System Context: [System Name]

## System Purpose
Brief description of what the system does.

## Users/Actors
- **End User**: Description of end users
- **Admin**: Description of administrators
- **[Other roles]**: ...

## External Systems
- **[External System 1]**: What it provides, how it's used
- **[External System 2]**: What it provides, how it's used

## System Boundary
What is inside our control vs. external dependencies.
```

---

## Level 2: Reverse Engineering Containers

### Goal

Identify the **major structural building blocks** - applications, services, databases, and how they communicate.

### Investigation Techniques

#### 1. Deployment Analysis (Most Reliable)

**Look at how the system is deployed**:

**Docker Compose**:
```yaml
# docker-compose.yml reveals containers clearly
version: '3'
services:
  web:              # Container: Web Application
    build: ./web
    ports:
      - "80:80"

  api:              # Container: API Application
    build: ./api
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis

  db:               # Container: Database
    image: postgres:14

  redis:            # Container: Cache
    image: redis:alpine

  worker:           # Container: Background Worker
    build: ./worker
```

**Kubernetes**:
```bash
# List all deployments/services
kubectl get deployments
kubectl get services
kubectl get pods

# Examine deployment files
ls kubernetes/
cat kubernetes/deployment.yaml
```

**Cloud Platforms**:
```bash
# AWS
aws ecs list-services
aws lambda list-functions
aws rds describe-db-instances

# Azure
az webapp list
az functionapp list

# GCP
gcloud app services list
gcloud functions list
```

#### 2. Code Structure Analysis

**Repository structure often reveals containers**:

```
project/
├── frontend/          # Container: SPA (React/Vue/Angular)
├── backend/           # Container: API Server
├── mobile/            # Container: Mobile App
│   ├── ios/
│   └── android/
├── worker/            # Container: Background Worker
├── admin-dashboard/   # Container: Admin SPA
└── database/          # Container: Database (migrations)
    └── migrations/
```

**Monorepo structure**:
```
packages/
├── web-app/          # Container
├── api/              # Container
├── admin/            # Container
├── shared/           # Not a container (shared library)
└── mobile/           # Container
```

#### 3. Process Analysis

**Check what's running**:
```bash
# See running processes
ps aux | grep -i "node\|python\|java\|dotnet"

# Check listening ports
netstat -tulpn
lsof -i -P -n | grep LISTEN

# Docker containers
docker ps
docker-compose ps
```

**Example discoveries**:
```
Port 3000: Node.js API server      → Container: API Application
Port 80:   Nginx                   → Container: Web Server
Port 5432: PostgreSQL              → Container: Database
Port 6379: Redis                   → Container: Cache
Port 5672: RabbitMQ                → Container: Message Queue
```

#### 4. Technology Stack Discovery

**Each technology usually represents a container**:

**Build files**:
```bash
# JavaScript/TypeScript
package.json (in root or subdirs)

# Python
setup.py
requirements.txt
Pipfile

# Java
pom.xml
build.gradle

# .NET
*.csproj
*.sln

# Go
go.mod
```

**Runtime detection**:
```bash
# Find all package.json files (each might be a container)
find . -name "package.json" -not -path "*/node_modules/*"

# Find all requirements.txt
find . -name "requirements.txt"

# Find all go.mod files
find . -name "go.mod"
```

#### 5. Communication Pattern Analysis

**How containers communicate**:

**REST API calls**:
```bash
# Search for API endpoints
rg "fetch\(|axios\.|http\.|request\(" -g "*.{js,ts}"
rg "requests\.|urllib|httpx" -g "*.py"
```

**Message queues**:
```bash
# Search for message queue usage
rg "rabbitmq|kafka|sqs|pubsub" -i
rg "publish|subscribe|send_message" -i
```

**Database connections**:
```bash
# Search for database connections
rg "createConnection|mongoose|sequelize|typeorm" -g "*.{js,ts}"
rg "psycopg2|pymongo|sqlalchemy" -g "*.py"
```

**GraphQL**:
```bash
rg "graphql|apollo" -i
find . -name "*.graphql"
```

#### 6. Identify Technology for Each Container

**Web Applications**:
- Check `package.json` → React, Vue, Angular?
- Check `index.html` → SPA or server-rendered?
- Check frameworks: Next.js, Nuxt, Gatsby, etc.

**Backend Applications**:
- Node.js: Express, NestJS, Fastify
- Python: Django, Flask, FastAPI
- Java: Spring Boot, Quarkus
- .NET: ASP.NET Core
- Go: Gin, Echo, Chi
- Ruby: Rails, Sinatra

**Databases**:
- PostgreSQL, MySQL, MongoDB, Redis, etc.
- Check connection strings in config

**Mobile**:
- iOS: Swift, Objective-C
- Android: Kotlin, Java
- Cross-platform: React Native, Flutter

### Container Identification Checklist

For each container, document:

- ✅ **Name**: What to call it
- ✅ **Type**: Web app, API, database, worker, etc.
- ✅ **Technology**: Language, framework, version
- ✅ **Responsibility**: What it does
- ✅ **Communication**: What it talks to and how (REST, GraphQL, message queue, etc.)
- ✅ **Data**: What data it stores or accesses

### Documentation Template

```markdown
# Container Diagram: [System Name]

## Containers

### [Container 1 Name]
- **Type**: Web Application / API / Database / Worker / etc.
- **Technology**: React 18, TypeScript, hosted on Vercel
- **Responsibility**: Provides user interface for customers
- **Communicates with**:
  - API Application (HTTPS/REST)
  - Authentication Service (OAuth 2.0)

### [Container 2 Name]
- **Type**: API Application
- **Technology**: Node.js, Express, TypeScript
- **Responsibility**: Provides REST API for business logic
- **Communicates with**:
  - Database (PostgreSQL JDBC)
  - Redis Cache (Redis protocol)
  - Message Queue (RabbitMQ AMQP)

### [Container 3 Name]
- **Type**: Database
- **Technology**: PostgreSQL 14
- **Responsibility**: Stores user data, orders, products

## Communication Patterns

- **Frontend → API**: HTTPS/REST, JSON
- **API → Database**: PostgreSQL protocol
- **API → Cache**: Redis protocol
- **API → Queue**: AMQP (RabbitMQ)

## Deployment Notes

- Frontend: Deployed to Vercel CDN
- API: Deployed to AWS ECS (Docker containers)
- Database: AWS RDS PostgreSQL
- Cache: AWS ElastiCache Redis
```

---

## Level 3: Reverse Engineering Components

### Goal

Understand the **internal structure of each container** - how it's organized into logical components.

### Investigation Techniques

#### 1. Code Structure Analysis (Primary Method)

**Folder structure reveals components**:

**Example: Express.js API**:
```
api/
├── src/
│   ├── controllers/       # Component: API Controllers
│   │   ├── userController.ts
│   │   └── orderController.ts
│   ├── services/          # Component: Business Logic Services
│   │   ├── userService.ts
│   │   └── orderService.ts
│   ├── repositories/      # Component: Data Access
│   │   ├── userRepository.ts
│   │   └── orderRepository.ts
│   ├── middleware/        # Component: Middleware
│   │   └── auth.ts
│   └── models/            # Component: Domain Models
│       ├── User.ts
│       └── Order.ts
```

**Components identified**:
1. **API Controllers** - Handle HTTP requests, routing
2. **Services** - Business logic and orchestration
3. **Repositories** - Data access layer
4. **Middleware** - Authentication, logging, etc.
5. **Models** - Domain entities

**Example: React SPA**:
```
frontend/
├── src/
│   ├── components/        # Component: UI Components
│   │   ├── common/
│   │   └── features/
│   ├── pages/             # Component: Page Components
│   ├── services/          # Component: API Client Services
│   │   └── apiClient.ts
│   ├── store/             # Component: State Management
│   │   └── redux/
│   ├── hooks/             # Component: Custom Hooks
│   └── utils/             # Component: Utilities
```

**Components identified**:
1. **UI Components** - Reusable React components
2. **Pages** - Top-level page components
3. **API Client** - Backend communication
4. **State Management** - Redux/Context state
5. **Custom Hooks** - Reusable logic

#### 2. Architecture Pattern Detection

**Identify the pattern used**:

**Layered Architecture**:
```
presentation/   → Component: Presentation Layer
business/       → Component: Business Layer
data/           → Component: Data Layer
```

**Hexagonal/Ports & Adapters**:
```
domain/         → Component: Domain Logic
ports/          → Component: Ports (interfaces)
adapters/       → Component: Adapters (implementations)
```

**MVC/MVP/MVVM**:
```
models/         → Component: Models
views/          → Component: Views
controllers/    → Component: Controllers
```

**Clean Architecture**:
```
entities/       → Component: Entities
usecases/       → Component: Use Cases
interfaces/     → Component: Interface Adapters
frameworks/     → Component: Frameworks & Drivers
```

**Microservices Internal Structure**:
```
api/            → Component: API Layer
handlers/       → Component: Request Handlers
services/       → Component: Business Services
repositories/   → Component: Data Repositories
```

#### 3. Dependency Analysis

**Understand component relationships**:

**Import analysis**:
```bash
# What does this module import?
rg "^import.*from" src/services/userService.ts

# What imports this module?
rg "from.*userService" src/
```

**Dependency flow**:
```
Controllers → Services → Repositories → Database
    ↓            ↓            ↓
 (HTTP)     (Business)    (Data Access)
```

#### 4. Class/Module Analysis

**Identify major classes or modules**:

```bash
# Find all classes
rg "^class\s+\w+" -g "*.{ts,js}" --no-filename -r '$0'

# Find all exported functions/modules
rg "^export (class|function|const)" -g "*.{ts,js}"

# Find interfaces (contracts between components)
rg "^interface\s+\w+" -g "*.ts" -r '$0'
```

#### 5. Responsibility Identification

**For each folder/module, determine**:
- What does it do?
- What concerns does it handle?
- What layer is it in?

**Ask**:
- Is this a component or just implementation detail?
- Does it have a clear responsibility?
- Does it interact with other parts?

### Component Identification Rules

**A component should**:
- ✅ Have a clear, single responsibility
- ✅ Be a logical grouping (not just one class)
- ✅ Have well-defined interfaces/boundaries
- ✅ Interact with other components
- ✅ Be meaningful to developers

**Not a component**:
- ❌ Individual classes (too granular)
- ❌ Utility functions (supporting role)
- ❌ Configuration files
- ❌ Single files with no clear boundary

### Investigation Workflow

**For each container**:

1. **Map the folder structure**:
   ```bash
   tree -L 2 src/
   ```

2. **Identify architectural layers/patterns**:
   - Is it layered?
   - Is it feature-based?
   - Is it domain-driven?

3. **Group related code into components**:
   - What folders represent logical units?
   - What are the major responsibilities?

4. **Identify component boundaries**:
   - How do components communicate?
   - What are the interfaces?

5. **Document component interactions**:
   - Draw dependency graph
   - Identify circular dependencies (code smell!)

### Documentation Template

```markdown
# Component Diagram: [Container Name]

## Architecture Pattern
[e.g., Layered Architecture, Hexagonal, MVC, etc.]

## Components

### Component 1: [Name]
- **Responsibility**: What this component does
- **Technology**: Framework, libraries used
- **Location**: `src/path/to/component/`
- **Key Classes/Modules**: Main classes or modules
- **Dependencies**: What components it uses
- **Used By**: What components use this

### Component 2: [Name]
- **Responsibility**:
- **Technology**:
- **Location**:
- **Key Classes/Modules**:
- **Dependencies**:
- **Used By**:

## Component Interactions

```
[API Controllers]
      ↓ uses
[Business Services]
      ↓ uses
[Repositories]
      ↓ uses
[Database] (external)
```

## Notes
- Circular dependencies detected: [if any]
- Code smells: [if any]
- Recommended refactoring: [if any]
```

---

## Level 4: Reverse Engineering Code

### Goal

Understand the **implementation details** - classes, interfaces, methods.

### When to Do This

⚠️ **Rarely needed** for documentation purposes!

Use this level when:
- Learning a complex algorithm
- Understanding a specific design pattern
- Teaching others about implementation
- Regulatory/compliance documentation

### Investigation Techniques

#### 1. Use Your IDE

**Modern IDEs are better than manual diagrams**:
- Class hierarchy view
- Call hierarchy
- Dependency graphs
- UML generation plugins

**IntelliJ IDEA / VS Code / Eclipse**:
- Right-click → "Show Diagram"
- Navigate → "Type Hierarchy"
- Navigate → "Call Hierarchy"

#### 2. Auto-Generate Diagrams

**Tools**:
- **PlantUML**: Generate from code annotations
- **TypeDoc**: TypeScript documentation
- **Javadoc**: Java documentation
- **Doxygen**: Multi-language
- **PyReverse**: Python class diagrams

**Example with PlantUML**:
```bash
# Generate class diagram from Java
java -jar plantuml.jar -Djava.awt.headless=true -classpath src/

# From Python
pyreverse -o png mypackage
```

#### 3. Code Reading

**Read the code directly**:
```bash
# For small components, just read the code
cat src/services/UserService.ts
```

Most of the time, **reading the code is faster and more accurate** than creating diagrams.

### Documentation Template

**If you must document at code level**:

```markdown
# Code: [Component Name]

## Key Classes

### ClassName
- **Purpose**: What this class does
- **Implements**: Interfaces implemented
- **Extends**: Parent class
- **Dependencies**: Other classes it uses

**Key Methods**:
- `methodName(params): returnType` - Description

## Design Patterns
- Pattern used: [e.g., Factory, Singleton, Observer]
- Why it's used: [rationale]

## UML Diagram
[Insert auto-generated UML or link to IDE view]
```

**Better alternative**: Just link to the code!
```markdown
See implementation: `src/services/UserService.ts`
```

---

## Practical Reverse Engineering Workflows

### Workflow 1: Complete Unknown System

**You know nothing about the system.**

```
Day 1: System Context
├─ Talk to stakeholders (2 hours)
├─ Review any existing docs (1 hour)
├─ Analyze configuration files (1 hour)
└─ Create System Context diagram (1 hour)

Day 2-3: Container
├─ Analyze deployment (docker-compose, k8s) (2 hours)
├─ Analyze repository structure (2 hours)
├─ Check running processes (1 hour)
├─ Identify all containers (2 hours)
└─ Create Container diagram (2 hours)

Day 4-5: Components (for key containers)
├─ Analyze code structure (3 hours per container)
├─ Identify architectural patterns (2 hours)
├─ Map component relationships (2 hours)
└─ Create Component diagrams (2 hours per container)

Week 2: Refinement
├─ Validate with team
├─ Add missing details
└─ Document discoveries
```

### Workflow 2: Familiar Domain, New Codebase

**You understand the business domain but not this specific codebase.**

```
Step 1: Quick System Context (30 min)
└─ You probably already know the external systems

Step 2: Container Discovery (2 hours)
├─ Check deployment files
├─ Review repository structure
└─ Create Container diagram

Step 3: Component Analysis (1-2 days)
├─ Focus on containers that interest you
└─ Create selective Component diagrams

Step 4: Code Deep-Dive (as needed)
└─ Just read the code, don't diagram it
```

### Workflow 3: Legacy System Modernization

**You need to understand before rewriting/refactoring.**

```
Step 1: System Context (1 day)
└─ Understand all integrations (critical for migration)

Step 2: Container Identification (2 days)
└─ Identify what needs to be migrated/replaced

Step 3: Component Analysis (1 week)
├─ Understand internal structure deeply
└─ Identify coupling and dependencies

Step 4: Identify Seams (1 week)
└─ Where can we safely refactor or replace?

Step 5: Plan Migration
└─ Use diagrams to plan strangler pattern or big rewrite
```

### Workflow 4: Security Audit / Code Review

**You need to understand security implications.**

```
Step 1: System Context (1 hour)
└─ Identify attack surface and external integrations

Step 2: Container Discovery (2 hours)
└─ Identify all network boundaries

Step 3: Data Flow Analysis (1 day)
├─ Where does sensitive data flow?
├─ What components handle authentication?
└─ What components handle authorization?

Step 4: Code Review (as needed)
└─ Focus on security-critical components
```

---

## Tools for Reverse Engineering

### Diagram Tools

**Manual Diagramming**:
- **Draw.io** (diagrams.net) - Free, web-based
- **Lucidchart** - Commercial, polished
- **PlantUML** - Text-based, version-controllable
- **Mermaid** - Text-based, renders in Markdown
- **Excalidraw** - Hand-drawn style

**C4-Specific Tools**:
- **Structurizr** - Official C4 tool (DSL or web)
- **C4-PlantUML** - PlantUML macros for C4
- **IcePanel** - Visual C4 modeling

### Code Analysis Tools

**Static Analysis**:
- **SonarQube** - Code quality and architecture
- **Structure101** - Dependency analysis
- **NDepend** (.NET) - Architecture analysis
- **JDepend** (Java) - Package dependencies

**Dependency Visualization**:
- **Dependency Cruiser** (JavaScript)
- **Madge** (JavaScript)
- **Pydeps** (Python)
- **Go callgraph** (Go)

**Architecture Discovery**:
- **Sourcetrail** - Interactive code exploration
- **CodeScene** - Behavioral code analysis
- **Lattix** - Architecture and dependency management

### Dynamic Analysis

**Runtime Analysis**:
- **Jaeger** / **Zipkin** - Distributed tracing
- **Datadog** / **New Relic** - APM
- **Wireshark** / **tcpdump** - Network analysis

---

## Best Practices for Reverse Engineering

### Do ✅

1. **Start with people** - Talk to developers/architects first
2. **Top-down first** - Get System Context before diving into code
3. **Focus on value** - Don't document everything, focus on what's unclear
4. **Validate frequently** - Check your understanding with the team
5. **Use multiple sources** - Code + config + deployment + docs
6. **Document as you go** - Don't wait until you understand everything
7. **Keep it simple** - Simple diagrams are more useful than detailed ones
8. **Version control diagrams** - Check them into the repo
9. **Update as you learn** - Iterate on your diagrams
10. **Link to code** - Reference actual files and line numbers

### Don't ❌

1. **Don't diagram everything** - Only what adds value
2. **Don't guess** - If uncertain, mark as "TODO" or "Investigate"
3. **Don't work in isolation** - Collaborate with team
4. **Don't create stale docs** - Delete if you won't maintain
5. **Don't over-detail** - Keep appropriate abstraction level
6. **Don't mix levels** - Keep each diagram at one C4 level
7. **Don't skip validation** - Always verify your understanding
8. **Don't forget updates** - Architecture changes, update diagrams

---

## Reverse Engineering Checklist

### System Context ✓
- [ ] Identified all user types/personas
- [ ] Identified all external systems
- [ ] Identified all major integrations
- [ ] Documented authentication/authorization approach
- [ ] Created System Context diagram
- [ ] Validated with team

### Container ✓
- [ ] Analyzed deployment configuration
- [ ] Identified all runtime containers
- [ ] Identified technology stack for each
- [ ] Documented communication protocols
- [ ] Identified all data stores
- [ ] Created Container diagram
- [ ] Validated with team

### Component ✓
- [ ] Analyzed code structure for each container
- [ ] Identified architectural pattern
- [ ] Mapped major components
- [ ] Documented component responsibilities
- [ ] Identified component dependencies
- [ ] Created Component diagrams (selective)
- [ ] Validated with team

### Code (Optional) ✓
- [ ] Identified key classes/interfaces
- [ ] Understood design patterns used
- [ ] Generated or documented as needed
- [ ] Prefer linking to code over diagrams

---

## Example: Reverse Engineering an E-Commerce System

### Step 1: System Context Discovery

**Interviews**:
- Product manager: "Customers browse products, add to cart, checkout with Stripe"
- DevOps: "We integrate with SendGrid for emails, AWS S3 for images"
- Developer: "Auth is handled by Auth0"

**Config analysis** (`.env.example`):
```bash
DATABASE_URL=postgresql://...
STRIPE_API_KEY=...
SENDGRID_API_KEY=...
AUTH0_DOMAIN=...
S3_BUCKET_NAME=...
```

**System Context diagram**:
```
[Customer] → Uses → [E-Commerce System] → Processes payments → [Stripe]
                            ↓
                     Sends emails → [SendGrid]
                            ↓
                     Stores images → [AWS S3]
                            ↓
                     Authenticates → [Auth0]
[Admin] → Manages → [E-Commerce System]
```

### Step 2: Container Discovery

**docker-compose.yml**:
```yaml
services:
  frontend:        # React SPA
  api:             # Node.js Express API
  postgres:        # Database
  redis:           # Session cache
  worker:          # Background job processor
```

**Container diagram**:
```
[Single Page App]
  React, TypeScript
  "Customer-facing UI"
      ↓
   Uses (HTTPS/REST)
      ↓
[API Application]
  Node.js, Express
  "Business logic & API"
      ↓
   Reads/Writes (PostgreSQL)
      ↓
[PostgreSQL Database]
  "Stores products, orders, users"
      ↓
[Redis Cache]
  "Session storage"
      ↓
[Background Worker]
  Node.js, Bull
  "Processes async jobs"
```

### Step 3: Component Discovery (API Container)

**Code structure**:
```
api/src/
├── controllers/    # Component: API Controllers
├── services/       # Component: Business Services
├── repositories/   # Component: Data Access
├── jobs/           # Component: Background Jobs
├── middleware/     # Component: Middleware
└── models/         # Component: Domain Models
```

**Component diagram**:
```
[API Controllers]
      ↓
[Auth Middleware]
      ↓
[Business Services]
      ↓
[Repositories]
      ↓
[PostgreSQL] (external)

[Business Services]
      ↓
[Job Queue]
      ↓
[Background Worker] (external container)
```

### Result

**Documentation created**:
- `docs/architecture/system-context.md` + diagram
- `docs/architecture/container.md` + diagram
- `docs/architecture/api-components.md` + diagram
- `docs/architecture/frontend-components.md` + diagram

**Time invested**: ~3 days
**Value**: New developers onboard in hours instead of weeks

---

## Summary

Reverse engineering with C4 provides a **structured approach** to understanding existing systems:

### The Process

1. **System Context**: Talk to people, analyze config, identify dependencies
2. **Container**: Analyze deployment, code structure, identify technology
3. **Component**: Analyze code organization, identify patterns, map relationships
4. **Code**: Use IDE, rarely document manually

### Key Principles

- Start **top-down** (System Context) to get orientation
- Use **bottom-up** (code analysis) to discover details
- **Validate frequently** with the team
- **Document selectively** - only what adds value
- **Keep it simple** - simple diagrams are more useful

### Success Metrics

A successful reverse engineering effort should:
- ✅ Help new team members onboard faster
- ✅ Support architectural decision-making
- ✅ Identify technical debt and improvement opportunities
- ✅ Create shared understanding across the team
- ✅ Be maintainable (not too detailed)

**Remember**: The goal is understanding and communication, not perfect documentation!

---

**Next Steps**:
- Review [Diagram Types](diagram-types.md) for detailed diagramming guidance on creating each type
- Check [Abstractions](abstractions.md) for deeper understanding of each level
- Start with System Context for your own project
