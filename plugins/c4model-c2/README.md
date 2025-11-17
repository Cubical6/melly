# C4 Model - Level 2: Container Methodology Skill

**Version**: 1.0.0
**Plugin Type**: Skill
**Dependencies**: c4model-c1

---

## Overview

The **c4model-c2** skill plugin provides comprehensive methodology for identifying and documenting containers (deployable/runnable units) at the C4 Model's Level 2 (Container) abstraction.

### What is C2 Container Level?

The Container level breaks down each system into its deployable and runnable units:

- **Web Servers** - Nginx, Apache, IIS
- **Application Servers** - Node.js apps, Spring Boot services, Django applications
- **Databases** - PostgreSQL, MongoDB, Redis
- **Message Brokers** - RabbitMQ, Kafka, SQS
- **Client Applications** - SPAs, mobile apps, desktop apps

> **⚠️ Important Terminology**: In C4 Model, "container" means any deployable/runnable unit (web server, mobile app, database, API server, etc.). It does **NOT** mean Docker container specifically. Docker is just one possible containerization technology. A "container" at C2 level can be a SPA running in a browser, a Lambda function, a mobile app, or any other independently deployable unit—regardless of whether Docker is used.

**Key Focus Areas:**
- ✅ Identify deployable/runnable units within each system
- ✅ Detect technology stacks and frameworks
- ✅ Analyze runtime environments and platforms
- ✅ Map communication patterns between containers
- ✅ Document deployment models and containerization

---

## Installation

### Via Claude Code Plugin Manager

```bash
# Install the plugin
/plugin add ./plugins/c4model-c2

# Verify installation
/plugins
```

### Manual Installation

```bash
# Project-level installation
mkdir -p .claude/skills
cp -r plugins/c4model-c2/skills/c4model-c2 .claude/skills/

# User-level installation (available across all projects)
mkdir -p ~/.claude/skills
cp -r plugins/c4model-c2/skills/c4model-c2 ~/.claude/skills/
```

### Dependencies

This skill requires:
- **c4model-c1** skill (must be installed first)
- **init.json** (from `/melly-init`)
- **c1-systems.json** (from `/melly-c1-systems`)

Install dependencies:
```bash
/plugin add ./plugins/c4model-c1
```

---

## Quick Start

### 1. Ensure Prerequisites

Before using this skill, make sure you have:

```bash
# Run initialization
/melly-init

# Generate C1 systems
/melly-c1-systems
```

This creates:
- `knowledge-base/init.json`
- `knowledge-base/c1-systems.json`

### 2. Invoke C2 Container Analysis

The skill is automatically activated when you run:

```bash
/melly-c2-containers
```

Or explicitly mention container analysis:

```
> Analyze the containers in the customer-web-app system
> What deployable units exist in the backend-api system?
> Identify the technology stack for each container
```

### 3. Understanding the Output

The skill helps generate `c2-containers.json`:

```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "generator": "melly-workflow",
    "generated_by": "c2-abstractor",
    "timestamp": "2025-11-17T20:20:00.000Z",
    "melly_version": "1.0.0",
    "parent_timestamp": "2025-11-17T20:10:00.000Z"
  },
  "containers": [
    {
      "id": "frontend-spa",
      "name": "Frontend Single-Page Application",
      "system_id": "customer-web-app",
      "type": "spa",
      "responsibility": "Provides interactive web interface for customers",
      "technology": {
        "primary_language": "TypeScript",
        "framework": "React 18.2.0",
        "libraries": [
          {
            "name": "React Router",
            "version": "6.14.0",
            "purpose": "Client-side routing"
          }
        ]
      },
      "runtime": {
        "environment": "browser",
        "platform": "Chrome, Firefox, Safari",
        "containerized": false
      },
      "observations": [...],
      "relations": [...]
    }
  ]
}
```

---

## Integration with Melly Workflow

### Workflow Position

The c4model-c2 skill is used in **Phase 3** of the Melly workflow:

```
Phase 1: /melly-init           → init.json
Phase 2: /melly-c1-systems     → c1-systems.json
Phase 3: /melly-c2-containers  → c2-containers.json  ← YOU ARE HERE
Phase 4: /melly-c3-components  → c3-components.json
Phase 5: /melly-doc-c4model    → Markdown docs
Phase 6: /melly-draw-c4model   → Visual diagrams
```

### Input Requirements

The skill expects:

**1. init.json** - Repository metadata
- Package manifests (package.json, composer.json, etc.)
- Directory structure
- Technology indicators

**2. c1-systems.json** - Systems identified at C1 level
- System IDs
- System types
- Repository associations

### Output Format

The skill helps generate `c2-containers.json` with:

- **Container identification** - All deployable/runnable units
- **Technology detection** - Languages, frameworks, libraries
- **Runtime analysis** - Environments, platforms, containerization
- **Observations** - Technology choices, patterns, issues
- **Relations** - Communication between containers

### Validation

All output must pass validation:

```bash
cat c2-containers.json | python plugins/melly-validation/scripts/validate-c2-containers.py
```

**Validation checks:**
- ✅ Schema structure correctness
- ✅ Timestamp ordering (c2 > c1 > init)
- ✅ Referential integrity (system_id references exist in c1-systems.json)
- ✅ Required fields present
- ✅ ID format (kebab-case)
- ✅ Technology and runtime fields complete

---

## What This Skill Teaches

### Container Identification Rules

**A container IS:**
- ✅ Independently deployable unit (can be deployed separately)
- ✅ Has its own runtime environment (browser, JVM, Node.js, etc.)
- ✅ Runs on a specific platform (server, cloud, browser)
- ✅ Has clear technology stack
- ✅ Communicates with other containers via defined protocols

**A container is NOT:**
- ❌ A code module within an application (that's C3 Component)
- ❌ A function or class (that's C4 Code level)
- ❌ A configuration file or static asset
- ❌ A vague "frontend" or "backend" (be specific!)

### Technology Detection Patterns

The skill teaches how to detect technologies from:

**npm/package.json:**
- `"react"` → React SPA container
- `"express"` → Express.js API server container
- `"next"` → Next.js full-stack container

**Python/requirements.txt:**
- `Django` → Django web application container
- `Flask` → Flask API server container
- `celery` → Celery worker container

**Docker/Kubernetes:**
- `Dockerfile` → Containerized deployment
- `docker-compose.yml` → Multi-container setup
- `kubernetes/*.yaml` → K8s orchestration

### Container Types

The skill covers 10+ container types:

1. **web-server** - Nginx, Apache, IIS
2. **app-server** - Express, Spring Boot, Django
3. **spa** - React, Vue, Angular (runs in browser)
4. **mobile-app** - React Native, Flutter
5. **desktop-app** - Electron, Tauri
6. **api** - REST API, GraphQL API servers
7. **database** - PostgreSQL, MongoDB, MySQL
8. **cache** - Redis, Memcached
9. **message-broker** - RabbitMQ, Kafka, SQS
10. **worker** - Background job processors

### Communication Patterns

The skill teaches identification of:

**Synchronous:**
- HTTP REST APIs
- HTTP GraphQL APIs
- gRPC calls

**Asynchronous:**
- Message queue publish/subscribe
- Event streaming
- Webhooks

**Database:**
- Direct database connections
- Read/write operations
- Connection pooling

---

## Examples

### Example 1: Simple Web Application

**Input: Single repository with React + Express**

```json
// Repository structure from init.json:
{
  "id": "webapp-repo",
  "manifests": [
    {
      "type": "npm",
      "path": "package.json",
      "data": {
        "dependencies": {
          "react": "^18.0.0",
          "express": "^4.18.0"
        }
      }
    }
  ]
}
```

**Output: 2 containers identified**

1. **Frontend SPA Container**
   - Type: `spa`
   - Technology: React 18
   - Runtime: Browser

2. **Backend API Container**
   - Type: `app-server`
   - Technology: Express 4
   - Runtime: Node.js server

### Example 2: Microservices Architecture

**Input: Multiple service repositories**

```json
// From c1-systems.json:
{
  "systems": [
    {"id": "auth-service", "repositories": ["/services/auth"]},
    {"id": "user-service", "repositories": ["/services/user"]},
    {"id": "order-service", "repositories": ["/services/order"]}
  ]
}
```

**Output: Multiple containers per system**

Each service system has:
- API container (Node.js/Express or Java/Spring)
- Database container (PostgreSQL)
- Cache container (Redis) - if applicable

### Example 3: Mobile Application

**Input: React Native mobile app**

```json
// From init.json:
{
  "id": "mobile-app",
  "manifests": [
    {
      "type": "npm",
      "data": {
        "dependencies": {
          "react-native": "^0.72.0"
        }
      }
    }
  ]
}
```

**Output: Mobile app container**

```json
{
  "id": "shopping-mobile-app",
  "type": "mobile-app",
  "technology": {
    "primary_language": "TypeScript",
    "framework": "React Native 0.72.0"
  },
  "runtime": {
    "environment": "mobile",
    "platform": "iOS 15+, Android 11+",
    "containerized": false
  }
}
```

---

## Best Practices

### DO ✅

1. **Be specific about technology versions**
   - ✅ "React 18.2.0" not "React"
   - ✅ "Node.js 18.16.0" not "Node"

2. **Identify all deployable units**
   - Don't forget databases, caches, message brokers
   - External services still count

3. **Document runtime environments clearly**
   - Browser? Server? Cloud? Mobile?
   - Containerized or not?

4. **Map communication patterns**
   - How do containers talk to each other?
   - Synchronous or asynchronous?

5. **Detect technology from evidence**
   - Check package manifests
   - Inspect Dockerfiles
   - Analyze configuration files

### DON'T ❌

1. **Don't confuse containers with components**
   - ❌ "Auth Component" is C3, not C2
   - ✅ "Auth Service API" is a container

2. **Don't use vague names**
   - ❌ "Frontend Container"
   - ✅ "Customer Portal SPA"

3. **Don't skip technology details**
   - Always specify language, framework, version
   - Runtime environment is required

4. **Don't ignore infrastructure containers**
   - Databases are containers too
   - Message brokers are containers

5. **Don't forget relationships**
   - Containers don't exist in isolation
   - Document all connections

---

## Troubleshooting

### Problem: Too Many Containers

**Symptom:** 20+ containers for a small system

**Solution:** You might be identifying C3 components as containers. Remember:
- Containers are **deployable units**
- If it can't be deployed separately, it's probably a component (C3)
- Combine related containers if they always deploy together

### Problem: Can't Determine Technology Stack

**Symptom:** No clear technology indicators

**Solution:**
1. Check all manifest files (package.json, requirements.txt, etc.)
2. Look for Dockerfiles (FROM statements reveal base images)
3. Inspect configuration files (webpack.config.js, tsconfig.json)
4. Check README.md for technology mentions
5. If still unclear, mark as "unknown" and document why

### Problem: Container vs Component Confusion

**Symptom:** Unsure if something is C2 or C3

**Ask these questions:**
- Can it be deployed independently? → C2 Container
- Does it have its own runtime? → C2 Container
- Is it just a code module? → C3 Component
- Is it a folder with TypeScript files? → Probably C3 Component

**Examples:**
- React SPA that builds to static files → C2 Container
- Auth module within the React app → C3 Component
- Express API server → C2 Container
- Payment controller within Express → C3 Component

### Problem: Validation Fails

**Symptom:** `validate-c2-containers.py` returns exit code 2

**Common issues:**

1. **Missing system_id reference**
   ```
   Container 'api-server': System not found: backend
   ```
   Fix: Use exact system ID from c1-systems.json

2. **Timestamp ordering violation**
   ```
   Timestamp must be newer than parent timestamp
   ```
   Fix: Ensure c2 timestamp > c1 timestamp

3. **Missing required fields**
   ```
   Container 'frontend': Missing required field 'technology.framework'
   ```
   Fix: Provide all required technology and runtime fields

### Problem: No Containers Found

**Symptom:** Empty containers array

**Solution:**
- Every system should have at least one container
- Check if system has deployable code
- Look for package manifests indicating runnables
- Consider infrastructure containers (database, cache)

---

## Related Documentation

- **C4 Model Methodology**: `docs/c4model-methodology.md`
- **JSON Schema Design**: `docs/json-schemas-design.md`
- **Validation Requirements**: Validation script documentation
- **Melly Workflow Guide**: `docs/workflow-guide.md`

---

## Support and Contribution

### Getting Help

If you encounter issues:

1. Check this README troubleshooting section
2. Review the SKILL.md for detailed methodology
3. Validate your output: `validate-c2-containers.py`
4. Check Melly documentation: `CLAUDE.md`

### Contributing

To improve this skill plugin:

1. Follow the C4 Model specification
2. Maintain consistency with c4model-c1 structure
3. Add concrete examples
4. Test with real repositories
5. Update validation scripts accordingly

---

## Changelog

### Version 1.0.0 (2025-11-17)

- ✅ Initial release
- ✅ Complete C2 Container methodology
- ✅ Technology detection patterns (20+ frameworks)
- ✅ Container type taxonomy (10+ types)
- ✅ Communication pattern identification
- ✅ Runtime environment analysis
- ✅ Integration with Melly workflow
- ✅ Comprehensive examples and troubleshooting
- ✅ Validation support

---

## License

This plugin is part of the Melly project. See the main repository LICENSE file for details.

---

**Plugin Version**: 1.0.0
**Last Updated**: 2025-11-17
**Compatibility**: Melly 1.0.0+
**Skill Type**: Methodology
