# C4 Model - Level 1: System Context Skill

> A comprehensive methodology skill for identifying and documenting systems, actors, and boundaries at the highest level of software architecture abstraction.

## Overview

The **c4model-c1** skill provides Claude Code with expert knowledge of the C4 Model's Level 1 (System Context) methodology. This skill enables accurate identification, analysis, and documentation of:

- **Systems** - Self-contained software systems with clear boundaries
- **Actors** - Users, personas, and external systems that interact with your systems
- **Boundaries** - System scope, ownership, and network boundaries
- **Relationships** - High-level interactions between systems and actors

## What is C1 System Context?

C1 (System Context) is the highest level of abstraction in the C4 Model, answering the question: **"What systems exist and how do they relate?"**

At this level, we focus on:
- The big picture of the software landscape
- System boundaries and responsibilities
- Who/what interacts with each system
- High-level communication patterns

**We do NOT focus on:**
- Implementation details (that's C2-C4)
- Internal components (that's C3)
- Specific technologies (that's C2)
- Code structure (that's C4)

## When to Use This Skill

This skill is automatically activated when Claude detects keywords like:
- "system context"
- "C1 level"
- "identify systems"
- "system boundaries"
- "actors"
- "external systems"
- "high-level architecture"
- "system relationships"

### Melly Workflow Integration

In the Melly workflow, this skill is used by:
- **`c4model-explorer` agent** - During repository scanning
- **`c1-abstractor` agent** - During system identification phase
- **`/melly-c1-systems` command** - When generating `c1-systems.json`

## Key Concepts

### Systems

A **system** is a self-contained deployable unit with:
- Clear purpose and responsibilities
- Defined boundaries
- Capability to be built/deployed independently
- One or more repositories

**Examples:**
- Web Application
- Mobile App
- REST API Service
- Database System
- Message Queue
- Payment Gateway (external)

### Actors

An **actor** is someone or something that interacts with your systems:

**People Actors:**
- End User
- Administrator
- Customer Service Agent
- Developer

**System Actors:**
- External Payment Provider
- Email Service
- Authentication Service
- Analytics Platform

### Boundaries

**System Boundaries** define:
- **Scope** - Internal (we control) vs External (third-party) vs Hybrid
- **Deployment** - On-premise, Cloud, SaaS, Hybrid
- **Network** - Public, Private, DMZ

### Relationships

**System Relationships** show:
- Communication protocols (HTTP, gRPC, message queues)
- Data flow direction
- Integration patterns
- Critical dependencies

## Common Architecture Patterns

### 1. Web Application Pattern

```
[User] --uses--> [Web Frontend] --calls--> [Backend API] --queries--> [Database]
                                     |
                                     +----> [External Payment Service]
```

**Systems:**
- Web Frontend (client-side SPA)
- Backend API (REST service)
- Database (data store)
- Payment Service (external)

### 2. Microservices Pattern

```
[Mobile App] --uses--> [API Gateway] --routes--> [Auth Service]
                                     +---------> [User Service]
                                     +---------> [Order Service]
                                     +---------> [Payment Service]
```

**Systems:**
- Mobile Application
- API Gateway
- Multiple Microservices
- Shared Database (per service)

### 3. Event-Driven Pattern

```
[Web App] --publishes--> [Message Queue] --consumes--> [Worker Service]
                                         +-----------> [Notification Service]
```

**Systems:**
- Web Application
- Message Queue (Kafka, RabbitMQ)
- Worker Services
- Notification Service

## System Identification Rules

### What IS a System (C1 Level)?

✅ **YES** - These are systems:
- Independently deployable applications
- External third-party services
- Major infrastructure components (databases, message brokers)
- Separate codebases with distinct responsibilities

✅ **Examples:**
- "Customer Portal" (web application)
- "Order API" (REST service)
- "PostgreSQL Database" (data store)
- "Stripe Payment Gateway" (external service)

### What is NOT a System (C1 Level)?

❌ **NO** - These are NOT systems (they're C2 Containers or C3 Components):
- Frontend frameworks (React, Vue) - these are **containers**
- Backend frameworks (Express, Django) - these are **containers**
- Individual modules/packages - these are **components**
- Code libraries - these are **components**

❌ **Examples:**
- "React Frontend" ❌ → Should be "Web Application" (system) with "React SPA" (container)
- "Express API" ❌ → Should be "Backend API" (system) with "Express Server" (container)
- "Auth Module" ❌ → Should be part of a system, identified at C3 level

## Actor Identification

### User Actors

**Questions to ask:**
- Who uses this system?
- What roles exist?
- What are the user personas?

**Examples:**
- "Customer" - End user making purchases
- "Administrator" - Internal user managing system
- "Support Agent" - Customer service representative

### External System Actors

**Questions to ask:**
- What external services do we integrate with?
- What third-party APIs are used?
- What systems are outside our control?

**Examples:**
- "Stripe Payment Gateway"
- "SendGrid Email Service"
- "Auth0 Identity Provider"
- "Google Analytics"

## Best Practices

### 1. Start with Repository Boundaries

Repositories often map to systems:
- One repository = likely one system
- Monorepo = multiple systems
- Microservices = multiple repositories = multiple systems

### 2. Focus on Responsibilities

Each system should have a clear purpose:
- ✅ "User Management System" - handles user accounts
- ✅ "Payment Processing System" - processes payments
- ❌ "Backend" - too vague, split into specific systems

### 3. Identify External Dependencies Early

External systems are crucial:
- Mark as `scope: external`
- Document integration points
- Note critical dependencies

### 4. Keep It High-Level

At C1, avoid implementation details:
- ✅ "Web Application communicates with API"
- ❌ "React app makes axios calls to Express server"

### 5. Document Boundaries Clearly

Be explicit about boundaries:
```json
{
  "boundaries": {
    "scope": "internal",
    "deployment": "cloud",
    "network": "public"
  }
}
```

## Anti-Patterns to Avoid

### ❌ Over-Granular Systems

**Wrong:**
```
- Login System
- Registration System
- Profile System
- Password Reset System
```

**Right:**
```
- User Management System (handles all user operations)
```

### ❌ Technology as System Name

**Wrong:**
```
- React Frontend
- Express Backend
- PostgreSQL
```

**Right:**
```
- Web Application (uses React)
- REST API Service (uses Express)
- User Database (PostgreSQL)
```

### ❌ Mixing Levels

**Wrong:** Identifying components as systems
```
- Authentication Module ❌ (This is C3)
- Payment Controller ❌ (This is C3)
```

**Right:** Identify the containing system
```
- Backend API System (contains Authentication Module)
```

### ❌ Vague System Names

**Wrong:**
```
- Frontend
- Backend
- Service
```

**Right:**
```
- Customer Portal Web Application
- Order Management API
- Notification Service
```

## Integration with Melly

### Input

This skill expects:
- Repository paths and metadata from `init.json`
- Package manifests (package.json, composer.json, etc.)
- Directory structure information
- Technology indicators

### Output

This skill helps generate:
- `c1-systems.json` with system definitions
- System observations (architecture, boundaries, actors)
- System relations (communication patterns)
- Markdown documentation in `knowledge-base/systems/*/c1/`

### Validation

Generated output is validated by:
- `plugins/melly-validation/scripts/validate-c1-systems.py`
- Schema compliance checks
- Referential integrity validation
- Timestamp ordering checks

## Example: Identifying Systems in E-Commerce Project

### Repositories Found:
```
/repos/frontend-spa/
/repos/api-server/
/repos/admin-dashboard/
/repos/worker-service/
```

### Systems Identified:

1. **Customer Web Application**
   - Type: `web-application`
   - Repository: `/repos/frontend-spa/`
   - Scope: Internal, Cloud, Public
   - Responsibilities: Product browsing, cart, checkout

2. **E-Commerce API**
   - Type: `api-service`
   - Repository: `/repos/api-server/`
   - Scope: Internal, Cloud, Private
   - Responsibilities: Business logic, data access, integrations

3. **Admin Dashboard**
   - Type: `web-application`
   - Repository: `/repos/admin-dashboard/`
   - Scope: Internal, Cloud, Private
   - Responsibilities: Order management, inventory, reports

4. **Background Worker Service**
   - Type: `internal-service`
   - Repository: `/repos/worker-service/`
   - Scope: Internal, Cloud, Private
   - Responsibilities: Async jobs, email sending, data processing

5. **Stripe Payment Gateway** (External)
   - Type: `external-service`
   - Repository: N/A
   - Scope: External, SaaS, Public
   - Responsibilities: Payment processing

### Actors Identified:

1. **Customer** (User)
   - Interacts with: Customer Web Application

2. **Administrator** (User)
   - Interacts with: Admin Dashboard

3. **Payment Provider** (External System)
   - Interacts with: E-Commerce API

## References

- [C4 Model Official Documentation](https://c4model.com/)
- [Melly C4 Methodology Guide](/docs/c4model-methodology.md)
- [Melly Workflow Guide](/docs/workflow-guide.md)
- [C1 Systems JSON Template](/plugins/melly-validation/templates/c1-systems-template.json)

## Support

For issues or questions:
- Check the Melly documentation in `/docs/`
- Review examples in `/knowledge-base/templates/`
- Consult the C4 Model methodology guide

---

**Version**: 1.0.0
**Plugin Type**: Skill
**Compatibility**: Melly 1.0.0+
**License**: MIT
