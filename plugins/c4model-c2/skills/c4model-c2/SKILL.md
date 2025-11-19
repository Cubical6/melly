---
name: c4model-c2
description: Use when identifying deployable units within C1-identified systems, detecting technology stacks with versions, or documenting container communication patterns - provides C4 Model Level 2 methodology for container identification, type classification (spa, api, database, cache, worker, etc.), and runtime environment analysis
---

# C4 Model - Level 2: Container Methodology

## Navigation

**Core Methodology:**
- **[Methodology](./methodology.md)** - Step-by-step container identification process
- **[Output Format](./output-format.md)** - JSON schema and validation commands

**Reference Materials:**
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

**Common Questions This Skill Answers:**
- "What deployable units exist in this system?"
- "What frameworks/technologies are used?"
- "How does the frontend communicate with the backend?"
- "Is this application containerized/dockerized?"
- "What database does this system use?"

**Error Symptoms That Indicate C2 Issues:**
- "missing technology.framework" - Container definition incomplete
- "version not specified" - Forgot to extract from manifest
- "container not found" - Reference to undefined container
- "too many containers" - Over-decomposed at C3 level
- "validation failed: primary_language" - Missing required field

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

> **Full methodology details:** See [Methodology](./methodology.md) for complete step-by-step process.

### Is This a Container? Decision Tree

```
                    ┌─────────────────────┐
                    │ Can it be deployed  │
                    │   independently?    │
                    └─────────┬───────────┘
                              │
                    ┌─────────┴─────────┐
                   YES                  NO
                    │                    │
        ┌───────────┴────────┐     ┌─────┴─────┐
        │ Does it run code   │     │  NOT a    │
        │  or store data?    │     │ Container │
        └─────────┬──────────┘     │ (maybe C3)│
                  │                └───────────┘
        ┌─────────┴─────────┐
       YES                  NO
        │                    │
  ┌─────┴──────┐       ┌─────┴─────┐
  │ Has own    │       │  NOT a    │
  │ tech stack │       │ Container │
  │ w/version? │       └───────────┘
  └─────┬──────┘
        │
  ┌─────┴─────────┐
 YES              NO
  │                │
┌─┴──────────┐  ┌──┴───────────┐
│ CONTAINER! │  │ Add version  │
│ Document   │  │ from manifest│
│ in C2      │  │ then continue│
└────────────┘  └──────────────┘
```

### Quick Summary

**5 Steps:**
1. **Understand System Decomposition** - Review c1-systems.json
2. **Apply Container Identification Rules** - IS vs is NOT
3. **Analyze Repository Structure** - Find deployment indicators
4. **Detect Technology Stack** - Language, framework, versions
5. **Identify Runtime Environment** - browser/server/mobile/cloud

### Critical Rules

**A Container IS:**
- Deployable independently
- Executes code OR stores data
- Has distinct technology stack with versions
- Has runtime environment
- Communicates via defined protocols

**A Container is NOT:**
- Code modules (that's C3)
- Config files or dev tools
- Generic names without versions ("React SPA" → "React 18.2.0 SPA")

**MANDATORY:** Extract versions from manifest files (package.json, requirements.txt, pom.xml, etc.). This is NOT optional.

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

> **See [Output Format](./output-format.md) for complete JSON schema and validation commands.**

Generate `c2-containers.json` with container definitions including id, name, type, system_id, technology (with versions), runtime, relations, and observations.

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

### Common Rationalizations (Red Flags)

If you catch yourself thinking these, STOP - you're about to make a mistake:

| Rationalization | Reality |
|-----------------|---------|
| "This module deserves its own container" | Modules within an app are C3 Components, not C2 Containers. Can it be deployed separately? |
| "I'll add the version later" | Versions are MANDATORY. Read package.json/requirements.txt NOW. No version = invalid container. |
| "The exact version doesn't matter" | It does. "React 18" ≠ "React 18.2.0". Extract full semantic version from manifest. |
| "Generic versions (18.x) show appropriate uncertainty" | WRONG. "18.x" is not a version - it's an excuse. Extract exact version from manifest. |
| "Architecture matters more than versions" | Both matter equally. C2 requires technology stack WITH versions. No shortcuts. |
| "Version precision is not the decision point" | WRONG. Version precision IS required for valid C2 documentation. It's not optional. |
| "This is obviously a container" | Verify deployment boundary. If it can't be deployed independently, it's not a container. |
| "I'll group these APIs into separate containers" | One API server with multiple endpoints = one container. Don't over-decompose. |
| "Reading package.json is too detailed for C2" | WRONG. Technology detection from manifests IS C2. Line-by-line code analysis is C3. |
| "Infrastructure doesn't need technology fields" | ALL containers need ALL fields. Use "N/A" for primary_language on databases/caches. |
| "I can skip the runtime environment" | Runtime is essential. browser/server/mobile/cloud determines how container operates. |

**All of these mean: Go back, verify your work, follow the methodology.**

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
- [ ] `name` - Descriptive container name with technology and version
- [ ] `type` - One of 10 container types
- [ ] `system_id` - Reference to C1 system
- [ ] `technology.primary_language` - JavaScript, Python, etc. (or "N/A" for infrastructure)
- [ ] `technology.framework` - React 18.2.0, Express 4.18.2, etc. (with full version)
- [ ] `runtime.environment` - browser, server, mobile, cloud
- [ ] `runtime.platform` - Exact platform details
- [ ] `runtime.containerized` - true/false
- [ ] `relations[]` - Communication with other containers

### Required Fields Matrix by Container Type

**APPLICATION CONTAINERS** (spa, mobile-app, desktop-app, api, app-server, worker):

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| `technology.primary_language` | **REQUIRED** | Actual language | "TypeScript", "Python", "Java" |
| `technology.framework` | **REQUIRED** | Name + Full Version | "React 18.2.0", "FastAPI 0.104.1" |
| `technology.libraries` | **REQUIRED** | Array with versions | `[{"name": "Redux", "version": "4.2.1"}]` |

**INFRASTRUCTURE CONTAINERS** (database, cache, message-broker, web-server, file-storage):

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| `technology.primary_language` | **REQUIRED** | Always "N/A" | "N/A" |
| `technology.framework` | **REQUIRED** | Tool + Full Version | "PostgreSQL 15.4", "Redis 7.2.3" |
| `technology.libraries` | OPTIONAL | Usually empty | `[]` |

**RULE:** ALL containers MUST have ALL technology fields filled. Use "N/A" for infrastructure containers' primary_language, but NEVER leave fields empty or undefined.

**Version Format:** Always use semantic versioning: `<Major>.<Minor>.<Patch>`
- ✅ "React 18.2.0"
- ✅ "PostgreSQL 15.4.0"
- ❌ "React 18" (missing minor.patch)
- ❌ "Express" (missing version entirely)

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
