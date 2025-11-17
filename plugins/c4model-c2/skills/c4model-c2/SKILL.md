---
name: c4model-c2
description: C4 Model Level 2 (Container) methodology for identifying deployable units, technology stacks, and runtime environments. Use when analyzing software architecture at the container abstraction level, identifying what deployable/runnable units exist, what technologies they use, and how they communicate. Keywords - container level, C2 level, container identification, deployable units, technology stack, runtime environment, application server, web server, database container, technology detection, framework analysis, deployment model, containerization, docker, kubernetes, microservices containers, spa container, api server, message broker, cache container, infrastructure as code.
---

# C4 Model - Level 2: Container Methodology

## Navigation

- **[Technology Detection Patterns](./technology-detection-patterns.md)** - Comprehensive guide to detecting frameworks, languages, and tooling
- **[Container Types Reference](./container-types-reference.md)** - Complete reference for all 10 container types with examples
- **[Communication Patterns](./communication-patterns.md)** - How containers communicate (HTTP, gRPC, queues, databases)
- **[Common Container Patterns](./common-container-patterns.md)** - Reusable architecture patterns (SPA+API+DB, microservices, serverless)
- **[Observation Categories](./observation-categories-c2.md)** - 8 observation categories with examples
- **[Troubleshooting Guide](./troubleshooting-guide-c2.md)** - Solutions to common problems

---

## Overview

You are an expert in the C4 Model's Level 2 (Container) methodology. This skill provides comprehensive knowledge for identifying and documenting containers (deployable/runnable units) at the second level of architectural abstraction.

**Your Mission:** Help identify WHAT deployable units exist within each system, WHAT technologies they use, and HOW they communicate - focusing on the building blocks that get deployed to production.

**C2 Container Level Definition:**
A container represents an application or data store that executes code or stores data. It's something that needs to be running for the overall system to work. Think: web servers, application servers, standalone applications, databases, file systems, message brokers.

**Relationship to Other Levels:**
- **C1 (System Context)** - Identified high-level systems → Now we decompose each system into containers
- **C2 (Container) - YOU ARE HERE** - Identify deployable/runnable units within each system
- **C3 (Component)** - Will identify code modules within each container (next level)

---

## C2 Level Definition

### What is a Container (C2)?

A **container** at C2 level is a deployable/runnable unit:

- **Deployable Unit** - Can be deployed independently (even if part of a larger system)
- **Runs Code or Stores Data** - Executes application logic or persists information
- **Has Technology Stack** - Built with specific languages, frameworks, libraries
- **Has Runtime Environment** - Runs in browser, server, cloud, mobile device
- **Communicates via Protocols** - HTTP, gRPC, database connections, message queues

**Important:** Container in C4 Model ≠ Docker container
- C4 "container" = deployable/runnable unit (broader concept)
- Docker container is one possible deployment technology

### Abstraction Level

```
┌─────────────────────────────────────────────┐
│ C1: System Context                          │
│ "What systems exist?"                       │
├─────────────────────────────────────────────┤
│ C2: Container Level                         │ ← YOU ARE HERE
│ "What are the deployable units?"            │
├─────────────────────────────────────────────┤
│ C3: Component Level                         │
│ "What are the code modules?"                │
├─────────────────────────────────────────────┤
│ C4: Code Level                              │
│ "What are the classes/functions?"           │
└─────────────────────────────────────────────┘
```

**At C2, we focus on:**
- ✅ Deployable/runnable units (what gets deployed)
- ✅ Technology stack (languages, frameworks, versions)
- ✅ Runtime environment (browser, server, cloud, mobile)
- ✅ Communication protocols (HTTP, gRPC, database, messaging)
- ✅ Deployment model (containerized, serverless, standalone)

**At C2, we do NOT focus on:**
- ❌ Code structure (that's C3 Component level)
- ❌ Classes and functions (that's C4 Code level)
- ❌ System boundaries (that was C1 System level)
- ❌ Line-by-line code analysis

---

## Container Identification Methodology

### Step 1: Understand System Decomposition

Start by reviewing the systems identified at C1 level in `c1-systems.json`:

**Questions to ask:**
1. What systems were identified at C1?
2. What repositories belong to each system?
3. What is the system type (web-application, api-service, etc.)?
4. What technologies were mentioned in system observations?

**System-to-Container Mapping Examples:**

**Simple Web Application System →**
- Frontend SPA container (React/Vue/Angular in browser)
- Backend API container (Express/Django/Spring on server)
- Database container (PostgreSQL/MongoDB)
- Cache container (Redis) - optional

**Microservice System →**
- API Server container (main service logic)
- Database container (service-specific database)
- Worker container (background processing) - optional
- Message broker container (RabbitMQ/Kafka) - if async

**Mobile App System →**
- Mobile Application container (React Native/Flutter on mobile)
- Backend API container (supporting backend)
- Database container
- Push notification service container - optional

> **See [Common Container Patterns](./common-container-patterns.md) for 6 reusable architecture patterns.**

### Step 2: Apply Container Identification Rules

#### ✅ A Container IS:

1. **Deployable independently** - Has own build/deployment process and artifact
2. **Executes code OR stores data** - Runs application logic or persists data
3. **Has distinct technology stack** - Built with specific language/framework
4. **Has runtime environment** - Runs in specific environment (browser, server, mobile, cloud)
5. **Communicates via defined protocols** - HTTP, database connections, message queues
6. **Infrastructure component** - Databases, caches, message brokers required for system operation

#### ❌ A Container is NOT:

1. **Code modules within an application** (these are C3 components)
   - ❌ "Authentication Module" in React app → C3 Component
   - ✅ "Express API Application" → C2 Container

2. **Configuration files or static assets** - package.json, CSS files, images

3. **Development tools** - Webpack, Babel, ESLint, Jest test runner

4. **Generic names without technology**
   - ❌ "Frontend Container" → ✅ "React SPA Container"
   - ❌ "Backend Container" → ✅ "Express API Server Container"

5. **Over-granular decomposition**
   - ❌ "Login API" + "Register API" → ✅ "User Management API"

> **See [Troubleshooting Guide](./troubleshooting-guide-c2.md#problem-too-many-containers-identified) for detailed guidance.**

### Step 3: Analyze Repository Structure

For each system, examine its repositories to identify containers:

**Look for deployment indicators:**

```bash
# Check for containerization
find . -name "Dockerfile" -o -name "docker-compose.yml"

# Check for build outputs
ls -la dist/ build/ target/ out/

# Check for deployment configs
ls -la .kubernetes/ .aws/ .azure/ vercel.json netlify.toml
```

**Common patterns:**

- **Frontend SPA:** `public/index.html`, `src/App.tsx`, `package.json` with React/Vue/Angular
- **Backend API:** `src/server.js`, `app.py`, `Main.java` with Express/Django/Spring
- **Database:** `docker-compose.yml` defining database service, migration files
- **Worker:** Queue consumer code, `worker.js`, `worker.py`

### Step 4: Detect Technology Stack

For each container, identify:

#### Primary Language
JavaScript, TypeScript, Python, Java, Go, Ruby, PHP, C#, Rust

**Detection methods:**
```bash
# Check package manifests
cat package.json | jq '.dependencies'
cat requirements.txt
cat pom.xml

# Count file extensions
find src -name "*.ts" | wc -l
find src -name "*.py" | wc -l

# Check Dockerfile
cat Dockerfile | grep "FROM"
```

#### Framework/Platform
React, Vue, Angular (frontend) | Express, NestJS, FastAPI, Django, Spring Boot (backend)

**Detection methods:**
- Check dependencies in package manifests
- Look for framework-specific files (`angular.json`, `vue.config.js`)
- Analyze import statements

> **See [Technology Detection Patterns](./technology-detection-patterns.md) for complete detection guide.**

### Step 5: Identify Runtime Environment

For each container, determine:

#### Environment
- **browser** - Runs in web browser (SPAs)
- **server** - Runs on server (APIs, web servers)
- **mobile** - Runs on mobile device (iOS/Android)
- **cloud** - Runs in cloud (Lambda, Cloud Functions)
- **edge** - Runs at edge (Cloudflare Workers)

#### Platform
- Browser: Chrome, Firefox, Safari, Edge
- Server: Linux, Node.js 18, Python 3.11, JVM 17
- Mobile: iOS 14+, Android 11+

#### Containerization
- **Containerized:** true/false
- **Container Technology:** Docker, Kubernetes, ECS
- **Container Image:** `node:18-alpine`, `python:3.11-slim`

---

## Container Types Quick Reference

**10 Container Types:**

1. **spa** - Single-Page Application (browser)
2. **mobile-app** - iOS/Android application
3. **desktop-app** - Desktop application
4. **api** / **app-server** - Backend API server
5. **web-server** - Web server, reverse proxy
6. **database** - Relational or NoSQL database
7. **cache** - In-memory cache (Redis, Memcached)
8. **message-broker** - Message queue/event streaming
9. **worker** - Background job processor
10. **file-storage** - Object storage, file system

> **See [Container Types Reference](./container-types-reference.md) for detailed examples of all 10 types.**

---

## Communication Pattern Identification

### Identify Relationships Between Containers

Document how containers communicate using these patterns:

**Synchronous:**
- **http-rest** - RESTful HTTP API
- **http-graphql** - GraphQL API
- **grpc** - gRPC remote procedure calls
- **websocket** - WebSocket bidirectional communication

**Asynchronous:**
- **message-publish** - Publish to queue/topic
- **message-subscribe** - Subscribe to queue/topic

**Data Access:**
- **database-query** - Database read/write
- **cache-read-write** - Cache read and write
- **file-storage-access** - File upload/download

> **See [Communication Patterns](./communication-patterns.md) for complete patterns guide.**

### Detection Commands

```bash
# Find HTTP clients
grep -r "axios\|fetch\|requests" src/

# Find database connections
grep -r "DATABASE_URL\|DB_HOST" .env

# Find message brokers
grep -r "amqplib\|kafkajs\|redis.*publish" src/
```

---

## Observation Categories

When documenting containers, capture these 8 observation categories:

1. **technology** - Technology stack, frameworks, libraries, versions
2. **runtime** - Runtime environment, platform, deployment model
3. **communication** - How container communicates with others
4. **data-storage** - Data persistence, caching, storage patterns
5. **authentication** - Authentication and authorization mechanisms
6. **configuration** - Configuration management, environment variables
7. **monitoring** - Logging, monitoring, observability
8. **dependencies** - External dependencies, third-party services

**Severity Levels:**
- **info** - Informational observation (neutral)
- **warning** - Potential issue requiring attention
- **critical** - Critical issue requiring immediate action

> **See [Observation Categories](./observation-categories-c2.md) for detailed guidelines and examples.**

---

## Workflow Integration

### When This Skill is Used

This skill is activated during:

1. **Phase 3: C2 Container Identification** (`/melly-c2-containers`)
   - Primary usage phase
   - Container identification per system
   - Technology stack detection

2. **Manual Container Analysis**
   - User asks "what containers exist?"
   - User asks "what is the technology stack?"
   - User mentions keywords: "deployable units", "runtime environment", "containerization"

### Input Requirements

**Required Files:**
- `c1-systems.json` - Must exist with identified systems
- Repository access - Must be able to read system repositories

**Required Information:**
- System ID to analyze
- Repository paths
- System type and technologies (from C1)

### Output Format

**Generate `c2-containers.json` with:**

```json
{
  "metadata": {
    "version": "1.0.0",
    "timestamp": "2025-11-17T20:20:00.000Z",
    "generated_by": "c2-abstractor",
    "parent": {
      "file": "c1-systems.json",
      "timestamp": "2025-11-17T10:00:00.000Z"
    }
  },
  "containers": [
    {
      "id": "ecommerce-spa",
      "name": "E-Commerce Customer Portal",
      "type": "spa",
      "system_id": "ecommerce-system",
      "technology": {
        "primary_language": "TypeScript",
        "framework": "React 18.2.0",
        "libraries": [
          {"name": "React Router", "version": "6.14.0", "purpose": "Client-side routing"},
          {"name": "Redux Toolkit", "version": "1.9.5", "purpose": "State management"}
        ]
      },
      "runtime": {
        "environment": "browser",
        "platform": "Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)",
        "containerized": false
      },
      "relations": [
        {
          "target": "ecommerce-api",
          "type": "http-rest",
          "direction": "outbound",
          "description": "Fetches product data and submits orders"
        }
      ],
      "observations": [],
      "metadata": {
        "repository": "frontend/",
        "discovered_at": "2025-11-17T20:15:00.000Z"
      }
    }
  ]
}
```

### Validation

After generating `c2-containers.json`:

```bash
# Validate JSON structure
python plugins/melly-validation/scripts/validate-c2-containers.py c2-containers.json

# Verify timestamps
python plugins/melly-validation/scripts/check-timestamp.sh c2-containers.json c1-systems.json
```

---

## Best Practices

### DO:

1. **Start with C1 understanding** - Review c1-systems.json first
2. **Focus on deployment boundary** - What can be deployed separately?
3. **Be specific with technology** - Include versions (React 18, not just React)
4. **Document runtime precisely** - Exact platform and containerization details
5. **Capture all communication** - Document how containers interact
6. **Use proper container types** - Choose from 10 defined types
7. **Provide evidence** - Link observations to files/commands
8. **Validate early** - Run validation scripts frequently

### DON'T:

1. **Don't confuse C2 with C3** - Components are code modules, not containers
2. **Don't be too granular** - 20+ containers likely means you're at C3 level
3. **Don't use generic names** - "Frontend" → "React SPA"
4. **Don't skip infrastructure** - Document databases, caches, brokers
5. **Don't guess** - Only document what you can verify
6. **Don't ignore validation** - Always validate before proceeding

---

## Quick Reference Checklist

### Container Identification Checklist

- [ ] Review C1 systems from c1-systems.json
- [ ] Identify deployable units per system
- [ ] Verify deployment boundary (can it be deployed separately?)
- [ ] Detect primary language and framework
- [ ] Identify runtime environment and platform
- [ ] Document communication patterns
- [ ] Capture observations (8 categories)
- [ ] Validate with melly-validation scripts

### Required Fields Checklist

- [ ] `id` - Unique container identifier
- [ ] `name` - Descriptive container name
- [ ] `type` - One of 10 container types
- [ ] `system_id` - Reference to C1 system
- [ ] `technology.primary_language` - JavaScript, Python, etc.
- [ ] `technology.framework` - React, Express, Django, etc.
- [ ] `runtime.environment` - browser, server, mobile, cloud
- [ ] `runtime.platform` - Exact platform details
- [ ] `runtime.containerized` - true/false
- [ ] `relations[]` - Communication with other containers

---

## Summary

**C2 Container Level focuses on:**

1. **WHAT deployable units exist** - Identify containers within each system
2. **WHAT technologies are used** - Detect languages, frameworks, versions
3. **WHERE containers run** - Identify runtime environments and platforms
4. **HOW containers communicate** - Document protocols and patterns

**Key Outputs:**
- `c2-containers.json` - Complete container inventory
- Observations per container (8 categories)
- Communication patterns documented
- Technology stack validated

**Next Steps:**
After completing C2 analysis:
1. Validate with `validate-c2-containers.py`
2. Review observations for warnings/critical issues
3. Proceed to C3 (Component) level analysis
4. Generate documentation with `/melly-doc-c4model`

**For detailed guidance, see the supporting documentation:**
- [Technology Detection Patterns](./technology-detection-patterns.md)
- [Container Types Reference](./container-types-reference.md)
- [Communication Patterns](./communication-patterns.md)
- [Common Container Patterns](./common-container-patterns.md)
- [Observation Categories](./observation-categories-c2.md)
- [Troubleshooting Guide](./troubleshooting-guide-c2.md)
