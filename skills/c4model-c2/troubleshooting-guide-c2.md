# Troubleshooting Guide - C2 Container Analysis

This document provides solutions to common problems encountered during C4 Model Level 2 (Container) analysis.

## Problem: Too Many Containers Identified

**Symptom:** 15+ containers for a simple web application

**Root Cause:** Confusing C3 components with C2 containers

**Solution:** Remember the deployment boundary:
- **Containers** are **deployable units** (can be deployed independently)
- **Components** are **code modules** within containers (cannot be deployed alone)
- If it can't be deployed independently, it's probably C3

**Decision Test:**
```
Can this be deployed separately?
├─ ✅ Yes → C2 Container
└─ ❌ No  → C3 Component
```

**Examples:**

| Item | Level | Reason |
|------|-------|--------|
| React SPA (builds to static files) | C2 Container | Deployed to CDN/web server |
| Auth module within React app | C3 Component | Part of SPA bundle |
| Express API server | C2 Container | Runs as separate process |
| Payment controller in Express | C3 Component | Code within API server |
| PostgreSQL database | C2 Container | Runs as separate process |
| User table in database | C3 Component | Schema within database |

**HARD LIMITS (Mandatory Validation):**

| Count | Classification | Action Required |
|-------|----------------|-----------------|
| 3-10 | ✅ Standard | Correct C2 abstraction level |
| 11-15 | ⚠️ Review Required | Each container MUST have explicit deployment boundary justification |
| 16-20 | ⚠️ Microservices | Document why this is microservices architecture, not over-granular |
| 20+ | 🛑 **STOP** | You are likely at C3 level. **Mandatory review of every container.** |

**RULE for 20+ Containers:**
- STOP analysis immediately
- Review EVERY identified "container" against the deployment boundary test
- Each item must answer YES to: "Can this be deployed independently?"
- If most answers are NO, you are at C3 level - consolidate to actual containers
- This is NOT guidance - this is a mandatory validation checkpoint

---

## Problem: Can't Determine Technology Stack

**Symptom:** No clear framework or language indicators

**Solution Steps:**

### Step 1: Check All Package Manifests

```bash
# Find all package files
find . -name "package.json" -o -name "requirements.txt" -o -name "pom.xml" -o -name "Cargo.toml"

# Examine dependencies
cat package.json | jq '.dependencies'
cat requirements.txt
```

### Step 2: Check Dockerfiles

```bash
# Find Dockerfiles
find . -name "Dockerfile*"

# Check base image
cat Dockerfile | grep "FROM"
```

**Common base images:**
- `FROM node:18` → Node.js 18
- `FROM python:3.11` → Python 3.11
- `FROM openjdk:17` → Java 17
- `FROM nginx:alpine` → Nginx web server

### Step 3: Count File Types

```bash
# Count source files by extension
find src -name "*.ts" | wc -l    # TypeScript
find src -name "*.js" | wc -l    # JavaScript
find src -name "*.py" | wc -l    # Python
find src -name "*.java" | wc -l  # Java
find src -name "*.go" | wc -l    # Go
find src -name "*.rs" | wc -l    # Rust
```

### Step 4: Check Build Configurations

```bash
# Check for framework config files
ls -la webpack.config.js tsconfig.json angular.json vue.config.js next.config.js

# Read framework configs
cat tsconfig.json | jq '.compilerOptions.jsx'  # React indicator
cat angular.json | jq '.projects'  # Angular indicator
```

### Step 5: Search for Framework Imports

```bash
# JavaScript/TypeScript frameworks
grep -r "from 'react'\|from 'vue'\|from '@angular" src/ | head -5

# Python frameworks
grep -r "from django\|from flask\|from fastapi" . | head -5

# Java frameworks
grep -r "import.*springframework" src/ | head -5
```

### Step 6: If Still Unclear - RESTRICTED USE ONLY

**"Unknown" is ONLY valid when ALL of these conditions are true:**
- ❌ NO manifest files exist (no package.json, requirements.txt, pom.xml, Cargo.toml, go.mod, Gemfile)
- ❌ NO Dockerfile exists OR Dockerfile does not specify version in FROM statement
- ❌ NO build configuration files found (tsconfig.json, angular.json, etc.)
- ❌ NO import statements reveal framework

**If ANY manifest file exists, you MUST extract the version. "Unknown" is NOT acceptable.**

When "Unknown" is legitimately required:
- Mark technology as **"Unknown"** temporarily
- Document **why** it's unclear with evidence of what you searched:
  ```json
  {
    "id": "obs-tech-unknown",
    "category": "technology",
    "severity": "critical",
    "description": "Unable to determine primary framework. Searched for all standard manifest files - none found.",
    "evidence": {
      "type": "command",
      "location": "find . -name 'package.json' -o -name 'requirements.txt' -o -name 'pom.xml' -o -name 'Cargo.toml' -o -name 'go.mod'",
      "snippet": "No results found"
    }
  }
  ```
- Ask user for clarification immediately
- This triggers a CRITICAL observation, not a warning

**RULE:** If you mark something as "Unknown" when manifest files exist, this is a VIOLATION of C2 methodology.

---

## Problem: Container vs System Confusion

**Symptom:** Unclear if something is C1 System or C2 Container

**Remember the Levels:**

| Level | Abstraction | Example |
|-------|-------------|---------|
| **C1 System** | High-level logical system with business purpose | "E-Commerce System" |
| **C2 Container** | Deployable/runnable unit within a system | "React SPA", "Express API", "PostgreSQL DB" |
| **C3 Component** | Code module within a container | "ProductList.tsx", "PaymentController.ts" |

**Decision Tree:**

```
Does it have a business purpose understood by non-technical stakeholders?
├─ ✅ Yes → Could be C1 System
│   └─ Does it consist of multiple deployable units?
│       ├─ ✅ Yes → C1 System
│       └─ ❌ No  → C2 Container (simple system with one container)
│
└─ ❌ No → Not C1 System
    └─ Can it be deployed independently?
        ├─ ✅ Yes → C2 Container
        └─ ❌ No  → C3 Component
```

**Real Examples:**

**Example 1: E-Commerce System**
- "E-Commerce System" → **C1 System** (business purpose: sell products online)
  - "Customer Web Portal" → **C2 Container** (React SPA)
  - "Product API Server" → **C2 Container** (Express API)
  - "Order Database" → **C2 Container** (PostgreSQL)
  - "Product Catalog Component" → **C3 Component** (code in React SPA)

**Example 2: Payment Processing System**
- "Payment Processing System" → **C1 System** (business purpose: process payments)
  - "Payment API Server" → **C2 Container** (NestJS API)
  - "Payment Database" → **C2 Container** (PostgreSQL)
  - "Stripe Integration Service" → **C2 Container** (Python worker)
  - "PaymentController" → **C3 Component** (code in NestJS API)

**Example 3: Monolith Application**
- "Customer Portal System" → **C1 System**
  - "Next.js Full-Stack Application" → **C2 Container** (single deployable unit)
    - Frontend pages → **C3 Components**
    - API routes → **C3 Components**
  - "PostgreSQL Database" → **C2 Container**

---

## Problem: Missing Required Fields in Validation

**Symptom:** Validation script fails with "Missing required field"

### Common Missing Fields:

#### 1. `system_id`

**Error:** `Missing required field: system_id`

**Solution:**
```bash
# Check c1-systems.json for valid system IDs
cat c1-systems.json | jq '.systems[].id'

# Use exact ID (case-sensitive)
# Example: "ecommerce-system" NOT "Ecommerce-System"
```

#### 2. `technology.primary_language`

**Error:** `Missing required field: technology.primary_language`

**Solution:**
- JavaScript, TypeScript, Python, Java, Go, Rust, etc.
- Required for all containers except pure infrastructure
- Use capitalized language name

**Example:**
```json
{
  "technology": {
    "primary_language": "TypeScript",
    "framework": "React 18.2.0"
  }
}
```

#### 3. `technology.framework`

**Error:** `Missing required field: technology.framework`

**Solution:**
- React, Express, Django, Spring Boot, FastAPI, etc.
- Required for all application containers
- Include version number

**Example:**
```json
{
  "technology": {
    "primary_language": "JavaScript",
    "framework": "Express.js 4.18.2"
  }
}
```

**Exception:** Infrastructure containers (databases, caches) may use "N/A":
```json
{
  "technology": {
    "primary_language": "N/A",
    "framework": "PostgreSQL 15.3"
  }
}
```

#### 4. `runtime.environment`

**Error:** `Missing required field: runtime.environment`

**Valid Values:**
- `browser` - Client-side web application
- `server` - Server-side application
- `mobile` - iOS/Android application
- `cloud` - Cloud-native/serverless
- `edge` - Edge computing
- `desktop` - Desktop application

**Example:**
```json
{
  "runtime": {
    "environment": "server",
    "platform": "Linux x64, Node.js 18.16.0"
  }
}
```

#### 5. `runtime.platform`

**Error:** `Missing required field: runtime.platform`

**Solution:**
Describe the exact platform where the container runs.

**Examples:**
```json
// Browser
"platform": "Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)"

// Server
"platform": "Linux x64, Node.js 18.16.0"
"platform": "Linux x64, Python 3.11.4"
"platform": "Linux x64, JVM 17"

// Mobile
"platform": "iOS 14+, Android 11+"

// Cloud
"platform": "AWS Lambda (Node.js 18 runtime)"
```

#### 6. `runtime.containerized`

**Error:** `Missing required field: runtime.containerized`

**Solution:**
- `true` - Runs in Docker/Kubernetes/container
- `false` - Runs directly on OS or in browser

**Examples:**
```json
// Containerized API
{
  "runtime": {
    "containerized": true,
    "container_technology": "Docker",
    "deployment_model": "Kubernetes with 3 replicas"
  }
}

// Browser SPA
{
  "runtime": {
    "containerized": false
  }
}
```

---

## Problem: Timestamp Validation Fails

**Symptom:** "Timestamp must be newer than parent timestamp"

**Root Cause:** c2-containers.json timestamp must be > c1-systems.json timestamp

**Solution:**

### Step 1: Check Current Timestamps

```bash
# Check C1 timestamp
cat c1-systems.json | jq '.metadata.timestamp'
# Example output: "2025-11-17T10:00:00.000Z"

# Check C2 timestamp
cat c2-containers.json | jq '.metadata.timestamp'
# Example output: "2025-11-17T09:00:00.000Z"  # WRONG! Earlier than C1
```

### Step 2: Regenerate with Current Timestamp

Ensure ISO 8601 format: `YYYY-MM-DDTHH:mm:ss.sssZ`

```bash
# Generate current timestamp
date -u +"%Y-%m-%dT%H:%M:%S.000Z"
# Example: 2025-11-17T20:20:00.000Z
```

### Step 3: Update c2-containers.json

```json
{
  "metadata": {
    "timestamp": "2025-11-17T20:20:00.000Z",
    "generated_by": "c2-abstractor",
    "parent": {
      "file": "c1-systems.json",
      "timestamp": "2025-11-17T10:00:00.000Z"
    }
  }
}
```

**Rule:** Always ensure C2 timestamp > C1 timestamp

---

## Problem: Communication Pattern Unclear

**Symptom:** Don't know which relation type to use

**Solution: Decision Tree:**

```
What protocol is used?
├─ HTTP
│   ├─ REST API → "http-rest"
│   ├─ GraphQL → "http-graphql"
│   └─ Generic → "http"
│
├─ gRPC → "grpc"
│
├─ WebSocket → "websocket"
│
├─ Database
│   ├─ Read only → "database-read"
│   ├─ Write only → "database-write"
│   └─ Both → "database-query"
│
├─ Cache
│   ├─ Read only → "cache-read"
│   ├─ Write only → "cache-write"
│   └─ Both → "cache-read-write"
│
├─ Message Queue
│   ├─ Publish → "message-publish"
│   └─ Subscribe → "message-subscribe"
│
└─ File Storage
    ├─ Read → "file-read"
    ├─ Write → "file-write"
    └─ Both → "file-read-write"
```

**Examples:**
- SPA calls API → `http-rest`
- API reads database → `database-query`
- API publishes to queue → `message-publish`
- Worker consumes queue → `message-subscribe`
- API caches responses → `cache-read-write`

---

## Problem: Monorepo vs Microservices Detection

**Symptom:** Unclear how many containers exist in a monorepo

**Solution:**

### Check for Multiple Package Files

```bash
# Find all package.json files (excluding node_modules)
find . -name "package.json" -not -path "*/node_modules/*"

# If multiple found, check structure
ls -la packages/ apps/ services/
```

### Check for Workspace Configuration

```bash
# Check for monorepo tools
cat package.json | jq '.workspaces'  # npm/yarn workspaces
cat lerna.json  # Lerna
cat nx.json  # Nx
cat pnpm-workspace.yaml  # pnpm
```

### Identify Deployable Units

**Rule:** Each independently deployable package = 1 container

**Example: Nx Monorepo**
```
monorepo/
├── apps/
│   ├── frontend/          → C2 Container (React SPA)
│   ├── api/               → C2 Container (NestJS API)
│   └── admin/             → C2 Container (Admin SPA)
├── libs/
│   ├── ui-components/     → C3 Component (shared library)
│   ├── data-access/       → C3 Component (shared library)
│   └── utils/             → C3 Component (shared library)
```

**Result:** 3 containers, 3 shared libraries (C3)

---

## Problem: Serverless Function Granularity

**Symptom:** Unclear if each Lambda function is a container

**Solution:**

### Option 1: Single Container (Recommended)

Treat all Lambda functions as **one container** if:
- Deployed together (single serverless.yml)
- Share same codebase
- Same runtime and dependencies

**Example:**
```yaml
# serverless.yml
functions:
  getUser: ...
  createUser: ...
  updateUser: ...
  deleteUser: ...
```

→ **One Container:** "User API Lambda Functions"

### Option 2: Multiple Containers

Only split into multiple containers if:
- Deployed independently (separate serverless.yml files)
- Different runtimes or dependencies
- Owned by different teams

**Example:**
```
services/
├── user-service/serverless.yml     → C2 Container
├── order-service/serverless.yml    → C2 Container
└── payment-service/serverless.yml  → C2 Container
```

**Rule:** Deployment boundary = container boundary

---

## Quick Reference Checklists

### Container Type Checklist

- [ ] `spa` - Single-page application (browser)
- [ ] `mobile-app` - iOS/Android application
- [ ] `desktop-app` - Desktop application
- [ ] `api` or `app-server` - Backend API server
- [ ] `web-server` - Web server, reverse proxy
- [ ] `database` - Relational or NoSQL database
- [ ] `cache` - In-memory cache (Redis, Memcached)
- [ ] `message-broker` - Message queue/event streaming
- [ ] `worker` - Background job processor
- [ ] `file-storage` - Object storage, file system

### Technology Detection Checklist

- [ ] **Primary Language** - JavaScript, TypeScript, Python, Java, etc.
- [ ] **Framework** - React, Express, Django, Spring Boot, etc.
- [ ] **Version** - Always include version numbers from manifests
- [ ] **Key Libraries** - List important dependencies with purpose

### Runtime Environment Checklist

- [ ] **Environment** - browser / server / mobile / cloud / edge
- [ ] **Platform** - OS, runtime version, supported browsers
- [ ] **Containerized** - true / false
- [ ] **Container Technology** - Docker, Kubernetes (if containerized)
- [ ] **Deployment Model** - Standalone, replicated, serverless

### Communication Checklist

- [ ] **Protocol** - HTTP, gRPC, WebSocket, database, message queue
- [ ] **Direction** - unidirectional / bidirectional
- [ ] **Authentication** - JWT, OAuth, API key, none
- [ ] **Format** - JSON, Protobuf, XML, binary

### Validation Checklist

- [ ] All required fields present (system_id, technology, runtime)
- [ ] Timestamp newer than c1-systems.json
- [ ] Valid container types used
- [ ] Communication patterns documented
- [ ] Observations categorized (8 categories)
- [ ] Evidence provided for observations

---

## FORBIDDEN Rationalizations (Automatic Validation Failures)

When under pressure, you may be tempted to skip C2 methodology rules. These rationalizations are **always wrong** and trigger **automatic validation failures**:

**RULE:** If your thinking matches ANY of these rationalizations, STOP immediately. You are about to violate C2 methodology. Do not proceed without addressing the actual requirement.

**Consequences:**
- Each rationalization triggers a CRITICAL severity observation
- Validation scripts will fail with explicit error messages
- Work containing these violations will be rejected

| Rationalization | Why It's Wrong |
|-----------------|----------------|
| "Versions can be refined later" | Creates technical debt, violates methodology. Do it right now. |
| "Reading package.json is line-by-line analysis" | Manifest files are metadata, not code. Version detection is standard C2. |
| "Version numbers get outdated anyway" | So does all documentation - not an excuse to skip standards. |
| "Generic names are honest about current state" | Generic names violate C2 standards. Period. |
| "Tech lead/senior approved it" | Authority doesn't override methodology. Push back professionally. |
| "Each module is important" | Important ≠ C2 container. Many important things are C3 components. |
| "Team needs granularity" | Then do C3 analysis. Don't pollute C2. |
| "Good enough for now" | Standards exist for consistency across all analysis. |
| "Being pragmatic not dogmatic" | Pragmatism ≠ violating definitions. The methodology IS pragmatic. |
| "We can add more detail later" | "Later" never comes. Do it correctly now. |
| "The spirit of the rule allows this" | Violating the letter IS violating the spirit. |
| "This case is different" | No it isn't. Apply the same standards uniformly. |

**If you catch yourself thinking any of these - STOP. Follow the methodology.**

---

## Still Having Issues?

### Enable Debug Mode

```bash
# Run validation with verbose output
python scripts/validate-c2-containers.py --verbose c2-containers.json

# Check for specific issues
python scripts/validate-c2-containers.py --check-timestamps c2-containers.json
```

### Common Debug Commands

```bash
# Validate JSON syntax
cat c2-containers.json | jq . > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Check required fields
cat c2-containers.json | jq '.containers[] | select(.technology.primary_language == null)'

# Verify timestamps
cat c2-containers.json | jq '.metadata.timestamp, .metadata.parent.timestamp'

# List all container IDs
cat c2-containers.json | jq '.containers[].id'
```

### Get Help

1. Review CLAUDE.md workflow guide
2. Check ${CLAUDE_PLUGIN_ROOT}/validation/templates/ for examples
3. Compare with c4model-c1 successful pattern
4. Ask user for clarification on unclear cases
