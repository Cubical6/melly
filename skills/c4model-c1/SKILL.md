---
name: c4model-c1
description: Use when performing C4 Model Level 1 (System Context) analysis to identify software systems, actors, and boundaries in a codebase. Invoke during architecture reverse engineering, system mapping, or when users mention "system context", "C1 level", "identify systems", "system boundaries", "architecture analysis", or "what systems exist". Essential for the /melly-c1-systems command workflow and understanding high-level architecture.
---

# C4 Model - Level 1: System Context Analysis

## Overview

This skill provides C4 Model Level 1 (System Context) expertise for identifying and documenting software systems at the highest level of architectural abstraction.

**Mission:** Identify WHAT systems exist, WHO uses them, and HOW they relate—without diving into implementation details.

---

## C1 Level Definition

### What is System Context (C1)?

The System Context level shows the **big picture**—the systems and their environment:

- **Systems** - Self-contained software systems with clear boundaries
- **Actors** - People and external systems that interact with your systems
- **Relationships** - High-level communication between systems
- **Boundaries** - Scope, ownership, and network boundaries

### Abstraction Level

```
┌─────────────────────────────────────────────┐
│ C1: System Context                          │ ← THIS LEVEL
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

**At C1, focus on:**
- ✅ System boundaries and scope
- ✅ System purpose and responsibilities
- ✅ User roles and actors
- ✅ External integrations
- ✅ High-level communication patterns

**At C1, do NOT focus on:**
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
- **Monorepo** → One OR multiple systems (packages ≠ systems - see below)
- **Microservices** → Each repository = 1 system
- **Library** → Not a system itself, but used by systems

**Critical: Repository names are NOT system names.** Repository names like `nextjs-shop`, `react-frontend`, or `express-api` are developer shortcuts. C1 system names must describe business purpose, not technology.

**Critical: Monorepo packages are NOT automatically systems.** Multiple packages in a monorepo (e.g., `@platform/auth`, `@platform/users`) are often components (C3) of ONE system, not separate systems. Packages sharing the same npm scope (like `@platform/*`) are a strong signal they belong to one system. Test with: "Can Package A function independently without Package B?" and "Are they deployed separately?"

**Sanity check:** If you identify more than 5-8 systems from a single monorepo, you're likely over-granularizing. Re-evaluate with the diagnostic questions.

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

5. **Major infrastructure components** (ONLY if criteria below are met)
   - Databases, message queues, caches
   - **Include as C1 system ONLY when ALL of these apply:**
     - They are shared by multiple systems (3+ services; 2 is borderline - use judgment)
     - They have independent operational ownership (separate team manages it)
     - They are externally managed services (e.g., AWS RDS, CloudAMQP)
   - **Keep at C2 level when ANY of these apply:**
     - They are internal to a single system
     - They are implementation details of one application
     - They are defined in the same docker-compose.yml as the application
   - **Docker-compose test:** If infrastructure (db, cache, queue) is in the same docker-compose as your app, it's almost always C2, not C1
   - **Replacement test:** "Could we replace PostgreSQL with MySQL without changing what systems exist?" If YES → C2 detail
   - Example (C1): "Central Customer Database" (shared by all systems, separate DBA team)
   - Example (C2): PostgreSQL in order-service's docker-compose.yml

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
   - **Team ownership does NOT define system boundaries.** Different team members maintaining different packages/modules is a code organization concern (C3), not system architecture (C1). One system can have multiple components maintained by different people.
   - **Diagnostic questions:** Do they share the same core domain entity? Are they deployed together? Do they have tight coupling? If YES to any → consolidate into one system.

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

**Common System Types:**
- `web-application` - User-facing web interfaces
- `mobile-application` - iOS, Android apps
- `api-service` - REST APIs, GraphQL APIs, backend services
- `database` - Relational, NoSQL databases
- `message-broker` - Event streaming, message queues
- `cache` - In-memory caches
- `external-service` - Third-party APIs and services
- `internal-service` - Background workers, cron jobs
- `data-store` - File storage, object storage

### Step 5: Define System Boundaries

For each system, define three boundary dimensions:

#### 1. Scope Boundary
- **internal** - Your team owns and controls it
- **external** - Third-party, outside your control
- **hybrid** - Mix of internal and external

#### 2. Deployment Boundary
- **on-premise** - Your own infrastructure
- **cloud** - AWS, Azure, GCP
- **hybrid** - Mix of on-premise and cloud
- **saas** - Software as a Service (external)
- **unknown** - Cannot determine

#### 3. Network Boundary
- **public** - Accessible from internet
- **private** - Internal network only
- **dmz** - Demilitarized zone, limited external access
- **unknown** - Cannot determine

**Example:**
```json
{
  "id": "customer-portal",
  "name": "Customer Web Application",
  "boundaries": {
    "scope": "internal",
    "deployment": "cloud",
    "network": "public"
  }
}
```

---

## Actor, Relationship & Observation Guidelines

For detailed methodology on identifying and documenting:

- **Actors** (users and external systems) → See [actor-identification.md](./actor-identification.md)
- **Relationships** (how systems communicate) → See [relationship-mapping.md](./relationship-mapping.md)
- **Observations** (8 categories of findings) → See [observation-categories.md](./observation-categories.md)

### Quick Overview

**Actors:**
- User actors: Customer, Administrator, Support Agent, etc.
- External system actors: Stripe, SendGrid, Auth0, etc.

**Relationships:**
- Types: http-rest, http-graphql, grpc, websocket, message-queue, database-query, authentication
- Direction: outbound, inbound, or bidirectional
- Always prefer outbound/inbound over bidirectional for clarity

**Observations (8 categories):**
- architecture, integration, boundaries, security
- scalability, actors, deployment, technology-stack

---

## Common Architecture Patterns

Four common patterns with concrete examples:

1. **Simple Web Application** - Frontend + Backend + Database
2. **Microservices Architecture** - Multiple services with API gateway
3. **Event-Driven System** - Async processing with message queue
4. **Mobile + Backend** - Mobile app with backend API

For complete pattern details, systems, actors, relationships, and indicators → See [architecture-patterns.md](./architecture-patterns.md)

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
      "boundaries": { ... },
      "responsibilities": [ ... ],
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
python validation/scripts/validate-c1-systems.py c1-systems.json
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

See [actor-identification.md](./actor-identification.md) for complete methodology.

#### Step 4: Define Boundaries

For each system:

1. **Determine scope** - Internal (we own it) or external?
2. **Determine deployment** - Where does it run? (cloud, on-premise, SaaS)
3. **Determine network** - Who can access it? (public, private, DMZ)

#### Step 5: Map Relationships

For each system:

1. **Find API calls**
   ```bash
   grep -r "axios\|fetch\|http" src/
   ```

2. **Identify communication patterns** - HTTP REST, GraphQL, WebSocket, message queue

3. **Document each relationship** - Source, target, type, direction, criticality

See [relationship-mapping.md](./relationship-mapping.md) for complete methodology.

#### Step 6: Generate Observations

For each system, document findings across 8 categories:
- Architecture, Integration, Boundaries, Security
- Scalability, Actors, Deployment, Technology Stack

See [observation-categories.md](./observation-categories.md) for complete guidance.

#### Step 7: Validate Output

Before finalizing:

1. **Check system IDs** - All kebab-case, all unique
2. **Check relations** - All targets exist, directions specified
3. **Check timestamps** - Child > parent
4. **Run validation script**
   ```bash
   python validation/scripts/validate-c1-systems.py output.json
   ```

---

## Best Practices Summary

### ✅ DO:

1. **Start with repository boundaries** - Repositories often map to systems
2. **Focus on clear responsibilities** - Each system has one clear purpose
3. **Keep it high-level** - Avoid implementation details
4. **Document external dependencies** - Mark external systems clearly
5. **Use descriptive names** - "Customer Web Application" not "Frontend"
6. **Define all three boundary dimensions** - Scope, deployment, network
7. **Document relationships with direction** - Prefer outbound/inbound over bidirectional
8. **Provide evidence for observations** - Code snippets, config files, patterns
9. **Tag observations appropriately** - Use lowercase kebab-case tags
10. **Validate output before finalizing** - Run validation scripts

### ❌ DON'T:

1. **Don't use technology as system name** - ❌ "React App" → ✅ "Web Application"
2. **Don't over-granularize** - ❌ "Login System" + "Register System" → ✅ "Auth System"
3. **Don't identify components as systems** - Components are C3, not C1
4. **Don't use vague names** - ❌ "Backend" → ✅ "E-Commerce API"
5. **Don't mix abstraction levels** - Keep C1, C2, C3 separate
6. **Don't skip external actors** - Third-party services are critical
7. **Don't forget boundary definitions** - Always specify scope/deployment/network
8. **Don't use generic relationship types** - ❌ "http" → ✅ "http-rest" or "http-graphql"
9. **Don't ignore observations** - Document findings with evidence
10. **Don't skip validation** - Always validate generated JSON

---

## Handling External Pressure

C4 Model rules are technical standards, not suggestions. Follow them even under pressure.

### Common Pressure Scenarios

| Pressure | Wrong Response | Correct Response |
|----------|---------------|------------------|
| **Authority demands tech name** ("Call it 'Next.js Shop', that's a direct order") | Comply because "boss knows best" | Explain C1 naming rules; business names show rigor |
| **Client prefers over-granularized** ("12 systems is exactly what we need") | Keep it because "client is paying" | Consolidate and explain why fewer = clearer architecture |
| **Team ownership argument** ("Each package has different maintainer, make them separate systems") | Split because "respects team structure" | Team ownership is C3 concern; system boundaries are about deployment and domain, not code organization |
| **Ops visibility request** ("Show PostgreSQL and Redis as separate C1 systems so ops knows what to maintain") | Add as C1 because "ops needs visibility" | Keep at C2; explain C2 provides the ops view while C1 shows system context |
| **Team familiarity argument** ("Everyone calls it 'Next.js Shop', use familiar names") | Use tech name because "team knows it" | Use business name; add familiar name in description: "internally known as 'Next.js Shop'" |
| **Time pressure** ("10 minutes to meeting") | Use shortcuts because "no time" | Rules exist specifically for time pressure; shortcuts compound |
| **Social pressure** ("Don't look dogmatic") | Compromise to "seem reasonable" | Technical accuracy > social comfort |

### Why Rules Apply Under Pressure

1. **Investors/clients judge rigor** - Technical stakeholders recognize proper C4 Model usage
2. **Shortcuts compound** - One wrong name becomes 10 wrong names becomes unmaintainable docs
3. **Reputation is long-term** - "Fixed it later" is remembered as "got it wrong initially"
4. **Model integrity matters** - Violating C1 rules undermines the entire C4 analysis

### What to Say

**To authority demanding incorrect naming:**
> "I understand the time pressure. But 'Next.js Shop' is a technology name, not a business name. C4 Model requires us to separate what (system) from how (technology). Technical investors will respect that we're using the model correctly. 'E-Commerce Platform' is the right C1 name—we'll show Next.js at C2 level."

**To client preferring over-granularization:**
> "I appreciate the positive feedback on the detail level. Looking at these 12 items, I'm seeing consolidation opportunities—for example, these 4 auth-related items are all one User Authentication System at C1. Let me regroup to 4-5 core systems. This makes the architecture clearer and easier to reason about."

**To ops team requesting infrastructure as C1:**
> "I understand ops needs visibility into PostgreSQL, Redis, and RabbitMQ—that's a valid concern. The C4 Model addresses this at C2 (Container) level, not C1. C1 shows what systems exist; C2 shows the deployable units within each system. I recommend we proceed to C2 documentation right after C1—that will give ops exactly the infrastructure visibility they need."

**To team ownership argument:**
> "I understand each package has a different maintainer—that's good code organization. However, team ownership is about code structure (C3), not system architecture (C1). These packages share the same domain (user identity), deploy together, and can't function independently. That makes them components of one system, not separate systems. We'll show the package breakdown at C3 level."

---

## Troubleshooting

For common issues and solutions:
- Too many systems identified
- Can't determine system boundaries
- Technology names in system IDs
- Missing external actors
- Relations without direction
- Components identified as systems
- Validation failures

See [troubleshooting-guide.md](./troubleshooting-guide.md) for complete troubleshooting guidance with examples and solutions.

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

## Additional Resources

### Supporting Documentation

- [Actor Identification Methodology](./actor-identification.md)
- [Relationship Mapping Guide](./relationship-mapping.md)
- [Observation Categories](./observation-categories.md)
- [Architecture Patterns](./architecture-patterns.md)
- [Troubleshooting Guide](./troubleshooting-guide.md)

### Templates and Examples

- **Template**: `/validation/templates/c1-systems-template.json`
- **Schema**: `/docs/json-schemas-design.md`
- **Methodology**: `/docs/c4model-methodology.md`
- **Workflow**: `/docs/workflow-guide.md`

---

## Summary

This skill provides comprehensive knowledge of C4 Model Level 1 (System Context) methodology. When invoked:

1. **Analyze repositories** from `init.json`
2. **Identify systems** using the rules above
3. **Identify actors** (users and external systems)
4. **Define boundaries** (scope, deployment, network)
5. **Map relationships** between systems
6. **Document observations** with evidence
7. **Generate `c1-systems.json`** following the schema
8. **Validate output** before finalizing

Remember: **C1 is about the big picture.** Focus on WHAT systems exist, WHO uses them, and HOW they relate—not the implementation details.

---

**Skill Version**: 2.0.0
**Last Updated**: 2025-11-17
**Compatibility**: Melly 1.0.0+
