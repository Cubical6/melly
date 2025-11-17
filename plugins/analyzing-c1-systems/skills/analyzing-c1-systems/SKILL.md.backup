---
name: c4model-c1
description: C4 Model Level 1 (System Context) methodology for identifying systems, actors, and boundaries. Use when analyzing software architecture at the highest abstraction level, identifying what systems exist, who uses them, and how they relate. Keywords - system context, C1 level, system identification, system boundaries, actors, external systems, high-level architecture, system relationships, software systems, architecture analysis, system mapping, architectural context.
allowed-tools: Read, Grep, Glob, Bash
---

# C4 Model - Level 1: System Context Methodology

## Overview

You are an expert in the C4 Model's Level 1 (System Context) methodology. This skill provides comprehensive knowledge for identifying and documenting software systems at the highest level of architectural abstraction.

**Your Mission:** Help identify WHAT systems exist, WHO uses them, and HOW they relate - without diving into implementation details.

---

## C1 Level Definition

### What is System Context (C1)?

The System Context level shows the **big picture** - the systems and their environment:

- **Systems** - Self-contained software systems with clear boundaries
- **Actors** - People and external systems that interact with your systems
- **Relationships** - High-level communication between systems
- **Boundaries** - Scope, ownership, and network boundaries

### Abstraction Level

```
┌─────────────────────────────────────────────┐
│ C1: System Context                          │ ← YOU ARE HERE
│ "What systems exist?"                       │
├─────────────────────────────────────────────┤
│ C2: Container Level                         │
│ "What are the deployable units?"            │
├─────────────────────────────────────────────┤
│ C3: Component Level                         │
│ "What are the code modules?"                │
├─────────────────────────────────────────────┤
│ C4: Code Level                              │
│ "What are the classes/functions?"           │
└─────────────────────────────────────────────┘
```

**At C1, we focus on:**
- ✅ System boundaries and scope
- ✅ System purpose and responsibilities
- ✅ User roles and actors
- ✅ External integrations
- ✅ High-level communication patterns

**At C1, we do NOT focus on:**
- ❌ Implementation technologies (that's C2)
- ❌ Code structure (that's C3/C4)
- ❌ Detailed APIs (that's C2/C3)
- ❌ Internal components (that's C3)

---

## System Identification Methodology

### Step 1: Understand Repository Structure

Start by analyzing the repositories provided in `init.json`:

**Questions to ask:**
1. How many repositories exist?
2. What type is each repository (monorepo, single, microservice)?
3. What package manifests exist (package.json, composer.json, etc.)?
4. What is the directory structure?

**Repository-to-System Mapping:**
- **Single repository** → Usually 1 system (sometimes 2 if frontend + backend)
- **Monorepo** → Multiple systems in one repository
- **Microservices** → Each repository = 1 system
- **Library** → Not a system itself, but used by systems

### Step 2: Apply System Identification Rules

A **system** at C1 level is:

#### ✅ A System IS:

1. **Independently deployable**
   - Can be built and deployed separately
   - Has its own runtime environment
   - Example: "Web Application", "REST API Service"

2. **Self-contained with clear boundaries**
   - Has defined inputs and outputs
   - Clear scope of responsibility
   - Example: "Payment Processing System", "User Database"

3. **Has a distinct purpose**
   - Solves a specific business problem
   - Provides specific functionality
   - Example: "Order Management System", "Notification Service"

4. **External third-party services**
   - Services outside your control
   - Third-party integrations
   - Example: "Stripe Payment Gateway", "SendGrid Email Service"

5. **Major infrastructure components**
   - Databases, message queues, caches
   - Critical infrastructure pieces
   - Example: "PostgreSQL Database", "Redis Cache", "RabbitMQ Message Broker"

#### ❌ A System is NOT:

1. **Technology/framework names**
   - ❌ "React Frontend" → ✅ "Customer Web Application"
   - ❌ "Express Backend" → ✅ "E-Commerce API"
   - ❌ "Django App" → ✅ "Content Management System"

2. **Internal code modules** (these are C3 components)
   - ❌ "Authentication Module"
   - ❌ "Payment Controller"
   - ❌ "User Service Class"

3. **Over-granular responsibilities** (combine into one system)
   - ❌ "Login System" + "Registration System" → ✅ "User Management System"
   - ❌ "Product List System" + "Product Detail System" → ✅ "Product Catalog System"

4. **Vague names without clear purpose**
   - ❌ "Frontend"
   - ❌ "Backend"
   - ❌ "Service"

### Step 3: Analyze Package Manifests

Package manifests reveal system purpose:

**npm/package.json indicators:**
```javascript
{
  "name": "customer-portal",  // System name hint
  "dependencies": {
    "react": "^18.0.0",      // Frontend system
    "express": "^4.18.0"      // Backend system (if same repo)
  },
  "scripts": {
    "start": "react-scripts start",  // Entry point
    "build": "react-scripts build"   // Build process
  }
}
```

**Common patterns:**
- `react` / `vue` / `angular` → Web Application (frontend)
- `express` / `fastify` / `koa` → API Service (backend)
- `next` / `nuxt` → Full-stack Web Application
- `@nestjs/core` → Backend API Service
- `electron` → Desktop Application
- `react-native` → Mobile Application

### Step 4: Detect System Type

Classify each system by type:

**System Types:**

1. **web-application**
   - User-facing web interfaces
   - SPAs, server-rendered apps
   - Example: Customer portal, admin dashboard

2. **mobile-application**
   - iOS, Android apps
   - React Native, Flutter apps
   - Example: Shopping app, delivery app

3. **desktop-application**
   - Electron, native desktop apps
   - Example: IDE, desktop client

4. **api-service**
   - REST APIs, GraphQL APIs
   - Backend services
   - Example: E-commerce API, user API

5. **database**
   - Relational, NoSQL databases
   - Example: PostgreSQL, MongoDB

6. **message-broker**
   - Event streaming, message queues
   - Example: Kafka, RabbitMQ, Redis Pub/Sub

7. **cache**
   - In-memory caches
   - Example: Redis, Memcached

8. **cdn**
   - Content delivery networks
   - Example: CloudFront, Cloudflare

9. **external-service**
   - Third-party APIs and services
   - Example: Stripe, SendGrid, Twilio

10. **internal-service**
    - Background workers, cron jobs
    - Example: Worker service, batch processor

11. **data-store**
    - File storage, object storage
    - Example: S3, file server

### Step 5: Define System Boundaries

For each system, define three boundary dimensions:

#### 1. Scope Boundary

**Ownership and control:**

- **internal** - Your team owns and controls it
  - Example: "Customer Web Application" (you built it)

- **external** - Third-party, outside your control
  - Example: "Stripe Payment Gateway" (external service)

- **hybrid** - Mix of internal and external
  - Example: "API Gateway" (managed service but you configure it)

#### 2. Deployment Boundary

**Where the system runs:**

- **on-premise** - Your own infrastructure
- **cloud** - AWS, Azure, GCP
- **hybrid** - Mix of on-premise and cloud
- **saas** - Software as a Service (external)
- **unknown** - Cannot determine

#### 3. Network Boundary

**Who can access it:**

- **public** - Accessible from internet
  - Example: Customer web application

- **private** - Internal network only
  - Example: Internal admin API

- **dmz** - Demilitarized zone, limited external access
  - Example: API gateway

- **unknown** - Cannot determine

**Example boundaries:**
```json
{
  "id": "customer-portal",
  "name": "Customer Web Application",
  "boundaries": {
    "scope": "internal",      // We own it
    "deployment": "cloud",    // Hosted on AWS
    "network": "public"       // Public internet access
  }
}
```

---

## Actor Identification Methodology

### Types of Actors

Actors are people or systems that interact with your systems:

#### 1. User Actors (People)

**Questions to ask:**
- Who uses this system?
- What user roles exist?
- What are the personas?
- What permissions do they have?

**Common user actors:**
- **End User / Customer** - Primary users of customer-facing systems
- **Administrator** - System administrators, super users
- **Support Agent** - Customer support representatives
- **Developer** - Internal developers using APIs
- **Manager** - Business users viewing reports
- **Guest / Anonymous User** - Unauthenticated visitors

**How to identify:**
- Look for authentication/authorization code
- Check user role definitions in code
- Review database user/role tables
- Analyze permission systems

**Code indicators:**
```typescript
// User roles indicate actors
enum UserRole {
  CUSTOMER,      // → Customer actor
  ADMIN,         // → Administrator actor
  SUPPORT,       // → Support Agent actor
  GUEST          // → Anonymous User actor
}
```

#### 2. External System Actors

**Questions to ask:**
- What external services are integrated?
- What third-party APIs are called?
- What systems are outside our control?
- What services do we depend on?

**Common external system actors:**
- **Payment Providers** - Stripe, PayPal, Square
- **Email Services** - SendGrid, Mailgun, AWS SES
- **SMS Services** - Twilio, Nexmo
- **Authentication Providers** - Auth0, Okta, Firebase Auth
- **Analytics Services** - Google Analytics, Mixpanel
- **CDN Services** - CloudFront, Cloudflare
- **Cloud Storage** - AWS S3, Google Cloud Storage
- **Monitoring Services** - Datadog, New Relic, Sentry

**How to identify:**
- Search for API keys in config files (.env.example)
- Check package dependencies for SDK libraries
- Review environment variables
- Look for external API base URLs

**Example external actors:**
```bash
# .env.example reveals external actors:
STRIPE_API_KEY=sk_test_...        # → Stripe actor
SENDGRID_API_KEY=SG...            # → SendGrid actor
TWILIO_ACCOUNT_SID=AC...          # → Twilio actor
GOOGLE_ANALYTICS_ID=UA-...        # → Google Analytics actor
```

### Actor Documentation Format

```json
{
  "actors": [
    {
      "id": "customer",
      "name": "Customer",
      "type": "user",
      "description": "End user who browses products and makes purchases",
      "interacts_with": ["customer-web-app", "mobile-app"]
    },
    {
      "id": "stripe",
      "name": "Stripe Payment Gateway",
      "type": "external-actor",
      "description": "Third-party payment processing service",
      "interacts_with": ["payment-api"]
    }
  ]
}
```

---

## Relationship Identification

### Relationship Types

Document how systems communicate:

#### Common Relationship Types

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

### Relationship Direction

Specify the direction of communication:

- **outbound** - This system initiates communication to target
  - Example: "Web App calls API" (outbound from Web App)

- **inbound** - Target system initiates communication to this system
  - Example: "API receives requests from Web App" (inbound to API)

- **bidirectional** - Communication flows both ways
  - Example: WebSocket connection

**Prefer outbound/inbound over bidirectional** for clarity.

### Relationship Metadata

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

### How to Identify Relationships

**1. Search for API calls:**
```bash
# Look for HTTP client libraries
grep -r "axios\|fetch\|http.get" src/
grep -r "requests.get\|httpx" .
grep -r "Http::get\|Guzzle" .
```

**2. Check environment variables:**
```bash
# .env.example reveals external integrations
cat .env.example | grep -E "API_URL|BASE_URL|ENDPOINT"
```

**3. Review configuration files:**
```javascript
// config/api.js
const API_BASE_URL = 'https://api.example.com';  // → Relationship to API
const STRIPE_API = 'https://api.stripe.com';     // → Relationship to Stripe
```

**4. Analyze package dependencies:**
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

---

## Observation Guidelines

### Observation Categories for C1

When documenting systems, capture these observation categories:

#### 1. **architecture**
System-level architectural patterns and decisions

**Examples:**
- "Microservices architecture with API gateway"
- "Monolithic architecture with single database"
- "Event-driven architecture using message queue"
- "Serverless architecture on AWS Lambda"

#### 2. **integration**
External system integrations and communication patterns

**Examples:**
- "Integrates with Stripe for payment processing"
- "Uses SendGrid for email notifications"
- "Connects to Auth0 for authentication"
- "Publishes events to Kafka message broker"

#### 3. **boundaries**
System boundary definitions and scope

**Examples:**
- "Public-facing web application accessible from internet"
- "Internal admin panel restricted to VPN access"
- "API gateway serves as single entry point for all services"
- "Database isolated in private subnet with no internet access"

#### 4. **security**
Security posture, authentication, and authorization

**Examples:**
- "JWT-based authentication with 1-hour token expiry"
- "OAuth 2.0 integration with Auth0"
- "API keys stored in environment variables"
- "HTTPS enforced for all communications"
- "No CSRF protection implemented" (warning)

#### 5. **scalability**
Scalability patterns and constraints

**Examples:**
- "Horizontally scalable API with load balancer"
- "CDN used for static asset delivery"
- "Database read replicas for scaling reads"
- "Stateless API design enables easy scaling"

#### 6. **actors**
User types and external actors

**Examples:**
- "Three primary user roles: customer, admin, support"
- "Anonymous users can browse products without login"
- "External payment provider (Stripe) integrated"
- "Third-party analytics service (Google Analytics) tracking users"

#### 7. **deployment**
Deployment patterns, hosting, and infrastructure

**Examples:**
- "Deployed on AWS using ECS containers"
- "Hosted on Vercel with automatic deployments"
- "On-premise deployment in company data center"
- "Serverless deployment using AWS Lambda"

#### 8. **technology-stack**
Technologies, frameworks, and libraries used

**Examples:**
- "React 18 with TypeScript for type safety"
- "Node.js runtime with Express framework"
- "PostgreSQL database with Prisma ORM"
- "Redis cache for session storage"

### Observation Structure

```json
{
  "id": "obs-arch-microservices",
  "title": "Microservices architecture with API gateway",
  "category": "architecture",
  "severity": "info",
  "description": "System follows microservices architecture with multiple independent services coordinated through an API gateway that handles routing, authentication, and rate limiting",
  "evidence": [
    {
      "type": "pattern",
      "location": "infrastructure/",
      "snippet": "Multiple service directories: auth-service/, user-service/, order-service/"
    }
  ],
  "tags": ["microservices", "api-gateway", "distributed"]
}
```

### Observation Severity Levels

- **info** - Informational observation (neutral)
- **warning** - Potential issue requiring attention
- **critical** - Critical issue requiring immediate action

**Examples:**
- ℹ️ **info**: "Uses React 18 for frontend development"
- ⚠️ **warning**: "No rate limiting on API endpoints"
- 🔴 **critical**: "API keys hardcoded in source code"

---

## Common Architecture Patterns

### Pattern 1: Simple Web Application

**Scenario:** Small web app with frontend and backend

**Systems identified:**
1. **Web Frontend** (web-application)
   - User-facing SPA
   - Repository: `/frontend/`

2. **Backend API** (api-service)
   - REST API
   - Repository: `/backend/`

3. **PostgreSQL Database** (database)
   - Data persistence
   - External infrastructure

**Actors:**
- End User (uses Web Frontend)

**Relationships:**
- Web Frontend → Backend API (http-rest)
- Backend API → PostgreSQL Database (database-query)

---

### Pattern 2: Microservices Architecture

**Scenario:** Multiple services with API gateway

**Systems identified:**
1. **API Gateway** (api-service)
   - Request routing
   - Repository: `/gateway/`

2. **Auth Service** (api-service)
   - Authentication
   - Repository: `/auth-service/`

3. **User Service** (api-service)
   - User management
   - Repository: `/user-service/`

4. **Order Service** (api-service)
   - Order processing
   - Repository: `/order-service/`

5. **Message Queue** (message-broker)
   - Event bus
   - External (RabbitMQ/Kafka)

**Actors:**
- Mobile App (external system actor)
- Administrator (user actor)

**Relationships:**
- API Gateway → Auth Service (grpc)
- API Gateway → User Service (grpc)
- API Gateway → Order Service (grpc)
- Order Service → Message Queue (message-queue)

---

### Pattern 3: Event-Driven System

**Scenario:** Async processing with message queue

**Systems identified:**
1. **Web Application** (web-application)
   - User interface
   - Repository: `/webapp/`

2. **Backend API** (api-service)
   - API layer
   - Repository: `/api/`

3. **Message Queue** (message-broker)
   - Event streaming
   - External (Kafka)

4. **Worker Service** (internal-service)
   - Background processing
   - Repository: `/worker/`

5. **Notification Service** (internal-service)
   - Email/SMS sending
   - Repository: `/notifications/`

**External Actors:**
- SendGrid (email delivery)
- Twilio (SMS delivery)

**Relationships:**
- Web Application → Backend API (http-rest)
- Backend API → Message Queue (message-queue, publish)
- Worker Service → Message Queue (message-queue, subscribe)
- Notification Service → Message Queue (message-queue, subscribe)
- Notification Service → SendGrid (http-rest)
- Notification Service → Twilio (http-rest)

---

### Pattern 4: Mobile + Backend

**Scenario:** Mobile app with backend API

**Systems identified:**
1. **Mobile Application** (mobile-application)
   - iOS/Android app
   - Repository: `/mobile-app/`

2. **Backend API** (api-service)
   - REST API
   - Repository: `/backend/`

3. **PostgreSQL Database** (database)
   - Data store
   - External infrastructure

4. **Redis Cache** (cache)
   - Session/data cache
   - External infrastructure

5. **Auth0** (external-service)
   - Authentication provider
   - External SaaS

**Actors:**
- Mobile User (user actor)
- Auth0 (external system actor)

**Relationships:**
- Mobile Application → Backend API (http-rest)
- Mobile Application → Auth0 (authentication, OAuth)
- Backend API → PostgreSQL Database (database-query)
- Backend API → Redis Cache (database-query)
- Backend API → Auth0 (authentication, token validation)

---

## Integration with Melly Workflow

### When This Skill is Used

This skill is activated during:

1. **Phase 1: Initialization** (`/melly-init`)
   - Repository scanning
   - Technology detection

2. **Phase 2: C1 System Identification** (`/melly-c1-systems`)
   - Primary usage phase
   - System identification
   - Actor identification
   - Boundary detection
   - Relationship mapping

3. **Phase 5: Documentation** (`/melly-doc-c4model`)
   - Markdown generation
   - Observation documentation

### Input Expectations

This skill expects data from `init.json`:

```json
{
  "metadata": { ... },
  "repositories": [
    {
      "id": "frontend-spa",
      "name": "Frontend SPA",
      "path": "/repos/frontend-spa",
      "type": "single",
      "manifests": [ ... ],
      "structure": { ... },
      "technology": { ... }
    }
  ]
}
```

### Output Format

This skill helps generate `c1-systems.json`:

```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "generator": "melly-workflow",
    "generated_by": "c1-abstractor",
    "timestamp": "2025-11-15T20:10:00.000Z",
    "melly_version": "1.0.0",
    "parent_timestamp": "2025-11-15T20:00:00.000Z"
  },
  "systems": [
    {
      "id": "web-frontend",
      "name": "Web Frontend",
      "type": "web-application",
      "description": "Customer-facing e-commerce web application",
      "repositories": ["/repos/frontend-spa"],
      "boundaries": {
        "scope": "internal",
        "deployment": "cloud",
        "network": "public"
      },
      "responsibilities": [
        "Display product catalog",
        "Manage shopping cart",
        "Handle user authentication",
        "Process checkout workflow"
      ],
      "observations": [ ... ],
      "relations": [ ... ]
    }
  ],
  "actors": [ ... ],
  "summary": {
    "total_systems": 4,
    "total_actors": 3,
    "system_types": { ... }
  }
}
```

### Validation

Generated output must pass:

1. **Schema validation** - Correct JSON structure
2. **Timestamp ordering** - metadata.timestamp > parent_timestamp
3. **Referential integrity** - All relation targets exist
4. **Required fields** - All required fields present
5. **ID format** - Kebab-case pattern

Validation script:
```bash
python plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json
```

---

## Step-by-Step Workflow

### When Invoked by c1-abstractor Agent

Follow this systematic approach:

#### Step 1: Load Input Data
```bash
# Load init.json
cat init.json | jq '.repositories'
```

#### Step 2: Analyze Each Repository

For each repository:

1. **Identify primary purpose**
   - What does this repository do?
   - What is its main responsibility?

2. **Detect technology stack**
   - What frameworks/languages are used?
   - What does this tell us about system type?

3. **Check for external dependencies**
   - What third-party services are used?
   - What APIs are called?

4. **Map repository to system(s)**
   - Is this one system or multiple?
   - What is the system name?
   - What is the system type?

#### Step 3: Identify Actors

1. **Scan for user roles**
   ```bash
   grep -r "role\|Role\|USER_ROLE\|UserRole" src/
   ```

2. **Find external integrations**
   ```bash
   cat .env.example | grep -E "API_KEY|API_URL|WEBHOOK"
   ```

3. **Document each actor**
   - Name and type
   - What systems they interact with
   - Purpose/description

#### Step 4: Define Boundaries

For each system:

1. **Determine scope**
   - Internal (we own it) or external?

2. **Determine deployment**
   - Where does it run?
   - Cloud, on-premise, SaaS?

3. **Determine network**
   - Who can access it?
   - Public, private, DMZ?

#### Step 5: Map Relationships

For each system:

1. **Find API calls**
   ```bash
   grep -r "axios\|fetch\|http" src/
   ```

2. **Identify communication patterns**
   - HTTP REST?
   - GraphQL?
   - WebSocket?
   - Message queue?

3. **Document each relationship**
   - Source and target
   - Type and direction
   - Protocol details
   - Criticality

#### Step 6: Generate Observations

For each system, document:

1. **Architecture observations**
   - Patterns used
   - Design decisions

2. **Integration observations**
   - External dependencies
   - Communication patterns

3. **Security observations**
   - Authentication methods
   - Potential vulnerabilities

4. **Boundary observations**
   - Access controls
   - Network topology

#### Step 7: Validate Output

Before finalizing:

1. **Check system IDs**
   - All kebab-case
   - All unique

2. **Check relations**
   - All targets exist
   - Directions specified

3. **Check timestamps**
   - Child > parent

4. **Run validation script**
   ```bash
   python plugins/melly-validation/scripts/validate-c1-systems.py output.json
   ```

---

## Best Practices Summary

### ✅ DO:

1. **Start with repository boundaries**
   - Repositories often map to systems

2. **Focus on clear responsibilities**
   - Each system has one clear purpose

3. **Keep it high-level**
   - Avoid implementation details

4. **Document external dependencies**
   - Mark external systems clearly

5. **Use descriptive names**
   - "Customer Web Application" not "Frontend"

6. **Define all three boundary dimensions**
   - Scope, deployment, network

7. **Document relationships with direction**
   - Prefer outbound/inbound over bidirectional

8. **Provide evidence for observations**
   - Code snippets, config files, patterns

9. **Tag observations appropriately**
   - Use lowercase kebab-case tags

10. **Validate output before finalizing**
    - Run validation scripts

### ❌ DON'T:

1. **Don't use technology as system name**
   - ❌ "React App" → ✅ "Web Application"

2. **Don't over-granularize**
   - ❌ "Login System" + "Register System" → ✅ "Auth System"

3. **Don't identify components as systems**
   - Components are C3, not C1

4. **Don't use vague names**
   - ❌ "Backend" → ✅ "E-Commerce API"

5. **Don't mix abstraction levels**
   - Keep C1, C2, C3 separate

6. **Don't skip external actors**
   - Third-party services are critical

7. **Don't forget boundary definitions**
   - Always specify scope/deployment/network

8. **Don't use generic relationship types**
   - ❌ "http" → ✅ "http-rest" or "http-graphql"

9. **Don't ignore observations**
   - Document findings with evidence

10. **Don't skip validation**
    - Always validate generated JSON

---

## Troubleshooting

### Problem: Too Many Systems Identified

**Symptom:** 10+ systems for a small application

**Solution:** You're likely over-granularizing. Combine systems:
- Login + Registration + Profile → User Management System
- Multiple APIs doing similar things → One API System with multiple containers (C2)

### Problem: Can't Determine System Boundaries

**Symptom:** Unclear where one system ends and another begins

**Solution:** Ask:
- Can this be deployed independently?
- Does it have a clear single purpose?
- Is it in a separate repository?
- If unclear, it might be one system

### Problem: Technology Names in System IDs

**Symptom:** `react-frontend`, `express-backend`

**Solution:** Rename to business purpose:
- `react-frontend` → `customer-web-app`
- `express-backend` → `ecommerce-api`

### Problem: Missing External Actors

**Symptom:** No external-service type systems

**Solution:** Check:
- `.env.example` for API keys
- `package.json` dependencies for SDK libraries
- Code for external API calls
- Most apps use external services (payment, email, etc.)

### Problem: Relations Without Direction

**Symptom:** All relationships marked "bidirectional"

**Solution:** Think about who initiates:
- Frontend calls API → outbound from frontend
- API calls database → outbound from API
- Only use bidirectional for WebSocket, etc.

---

## Quick Reference

### System Type Checklist

- [ ] `web-application` - User-facing web UI
- [ ] `mobile-application` - iOS/Android app
- [ ] `desktop-application` - Desktop app
- [ ] `api-service` - Backend API
- [ ] `database` - Data store
- [ ] `message-broker` - Event streaming
- [ ] `cache` - In-memory cache
- [ ] `external-service` - Third-party service
- [ ] `internal-service` - Worker/background service

### Boundary Checklist

- [ ] Scope: `internal` / `external` / `hybrid`
- [ ] Deployment: `on-premise` / `cloud` / `saas` / `hybrid`
- [ ] Network: `public` / `private` / `dmz`

### Relationship Type Checklist

- [ ] `http-rest` - RESTful API
- [ ] `http-graphql` - GraphQL API
- [ ] `grpc` - gRPC RPC
- [ ] `websocket` - WebSocket
- [ ] `message-queue` - Async messaging
- [ ] `database-query` - Database access
- [ ] `authentication` - Auth flow

### Observation Category Checklist

- [ ] `architecture` - Patterns and decisions
- [ ] `integration` - External integrations
- [ ] `boundaries` - Scope and access
- [ ] `security` - Auth and vulnerabilities
- [ ] `scalability` - Scaling patterns
- [ ] `actors` - Users and external actors
- [ ] `deployment` - Hosting and infrastructure
- [ ] `technology-stack` - Technologies used

---

## Examples and Templates

See these files for complete examples:

- **Template**: `/plugins/melly-validation/templates/c1-systems-template.json`
- **Schema**: `/docs/json-schemas-design.md`
- **Methodology**: `/docs/c4model-methodology.md`
- **Workflow**: `/docs/workflow-guide.md`

---

## Summary

You now have comprehensive knowledge of C4 Model Level 1 (System Context) methodology. When invoked:

1. **Analyze repositories** from `init.json`
2. **Identify systems** using the rules above
3. **Identify actors** (users and external systems)
4. **Define boundaries** (scope, deployment, network)
5. **Map relationships** between systems
6. **Document observations** with evidence
7. **Generate `c1-systems.json`** following the schema
8. **Validate output** before finalizing

Remember: **C1 is about the big picture.** Focus on WHAT systems exist, WHO uses them, and HOW they relate - not the implementation details.

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-11-17
**Compatibility**: Melly 1.0.0+
