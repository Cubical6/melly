# C4 Model Methodology for Melly

> **A structured approach to reverse engineering and documenting software architecture**

## Overview

The C4 model is a lean, hierarchical approach to software architecture diagramming. Melly uses this methodology to progressively abstract code repositories from concrete implementation details to high-level system context.

## What is the C4 Model?

The C4 model stands for **Context, Containers, Components, and Code** - four levels of abstraction for visualizing software architecture:

```
C1: System Context    (Highest abstraction - What systems exist?)
    ↓
C2: Containers        (What are the deployable units?)
    ↓
C3: Components        (What are the logical building blocks?)
    ↓
C4: Code             (Lowest abstraction - Classes, functions, etc.)
```

## Melly's C4 Implementation

### C1: System Context Level

**Purpose**: Identify and document the high-level systems and their relationships.

**What we identify:**
- External systems the software interacts with
- Major subsystems within the codebase
- System boundaries
- User personas and actors

**Output:**
- `init.json` - Repository metadata and structure
- `c1-systems.json` - Systems identified with observations and relations
- Markdown documentation in `knowledge-base/systems/*/c1/`

**Example Systems:**
- Web Application
- REST API
- Database System
- Message Queue
- External Payment Gateway
- Authentication Service

**Key Questions:**
- What are the major systems in this architecture?
- How do they communicate?
- What are the system boundaries?
- Who are the users of each system?

---

### C2: Container Level

**Purpose**: Break down each system into deployable/runnable containers.

**What we identify:**
- Web servers (e.g., Nginx, Apache)
- Application servers (e.g., Node.js, Python Flask)
- Databases (e.g., PostgreSQL, MongoDB)
- File storage systems
- Message brokers
- Microservices

**Output:**
- `c2-containers.json` - Containers per system with technology stack
- Markdown documentation in `knowledge-base/systems/*/c2/`

**Example Containers:**
- Frontend SPA (React application running in browser)
- Backend API (Express.js application on Node.js)
- PostgreSQL Database
- Redis Cache
- Worker Queue (Celery workers)

**Key Questions:**
- What are the deployable units?
- What technology is each container built with?
- How do containers communicate (HTTP, gRPC, message queues)?
- Where does each container run (browser, server, cloud)?

---

### C3: Component Level

**Purpose**: Identify the logical components within each container.

**What we identify:**
- Major code modules/packages
- Controllers, services, repositories
- Domain models
- Shared libraries
- Plugin systems

**Output:**
- `c3-components.json` - Components per container with structure
- Markdown documentation in `knowledge-base/systems/*/c3/`

**Example Components:**
- Authentication Component
- User Management Component
- Payment Processing Component
- Notification Service
- Logging Framework

**Key Questions:**
- What are the major logical building blocks?
- What responsibilities does each component have?
- How do components depend on each other?
- What patterns are used (MVC, layered architecture, etc.)?

---

### C4: Code Level (Future)

**Purpose**: Document the actual code implementation details.

**What we identify:**
- Classes and interfaces
- Functions and methods
- Data structures
- Design patterns

**Status:** Not yet implemented in Melly v1.0

---

## Melly Workflow

### Phase 1: Initialization (`/melly-init`)

**Input:** Repository paths
**Process:**
1. Scan all repositories
2. Identify package manifests (package.json, composer.json, etc.)
3. Map directory structure
4. Generate `init.json`

**Output:** `init.json` with repository metadata

---

### Phase 2: C1 System Identification (`/melly-c1-systems`)

**Input:** `init.json`
**Process:**
1. Analyze repository structures
2. Identify systems based on:
   - Repository boundaries
   - Package manifests
   - Technology indicators
3. Create system folders in `knowledge-base/systems/`
4. Generate `c1-systems.json`

**Output:**
- System folders created
- `c1-systems.json` with observations and relations

---

### Phase 3: C2 Container Identification (`/melly-c2-containers`)

**Input:** `init.json`, `c1-systems.json`
**Process:**
1. For each system, identify containers:
   - Frontend applications
   - Backend services
   - Databases
   - Message queues
   - Cache systems
2. Detect technology stack
3. Generate `c2-containers.json`

**Output:** `c2-containers.json` with container details

---

### Phase 4: C3 Component Identification (`/melly-c3-components`)

**Input:** `init.json`, `c1-systems.json`, `c2-containers.json`
**Process:**
1. For each container, identify components:
   - Code modules
   - Services
   - Controllers
   - Repositories
2. Analyze code structure
3. Generate `c3-components.json`

**Output:** `c3-components.json` with component details

---

### Phase 5: Documentation Generation (`/melly-doc-c4model`)

**Input:** All JSON files (init, c1, c2, c3)
**Process:**
1. For each level (C1, C2, C3):
   - Load appropriate template
   - Generate markdown from JSON data
   - Populate observations section
   - Populate relations section
   - Store in basic-memory knowledge base

**Output:** Markdown files in `knowledge-base/systems/*/c1|c2|c3/`

---

### Phase 6: Visualization (`/melly-draw-c4model`)

**Input:** All JSON files
**Process:**
1. Parse observations and relations
2. Generate Mermaid diagrams for:
   - System context (C1)
   - Container diagrams (C2)
   - Component diagrams (C3)
3. Create Obsidian canvas files
4. Store via basic-memory MCP

**Output:** Visual diagrams in canvas format

---

## JSON Schema Structure

### init.json

```json
{
  "timestamp": "2025-11-15T20:00:00Z",
  "repositories": [
    {
      "path": "/path/to/repo",
      "name": "repo-name",
      "manifests": [
        {
          "type": "npm",
          "path": "package.json",
          "dependencies": {...}
        }
      ],
      "structure": {
        "src": [...],
        "tests": [...],
        "docs": [...]
      }
    }
  ]
}
```

### c1-systems.json

```json
{
  "timestamp": "2025-11-15T20:10:00Z",
  "systems": [
    {
      "id": "web-app",
      "name": "Web Application",
      "repositories": ["/path/to/frontend"],
      "observations": [
        "React-based single page application",
        "Uses TypeScript",
        "Communicates with REST API"
      ],
      "relations": [
        {
          "target": "api-server",
          "type": "http",
          "description": "Consumes REST API"
        }
      ]
    }
  ]
}
```

### c2-containers.json

```json
{
  "timestamp": "2025-11-15T20:20:00Z",
  "containers": [
    {
      "id": "frontend-spa",
      "name": "Frontend SPA",
      "system": "web-app",
      "technology": "React 18, TypeScript 5",
      "runtime": "Browser",
      "observations": [
        "Client-side routing with React Router",
        "State management with Redux Toolkit",
        "Material-UI component library"
      ],
      "relations": [
        {
          "target": "backend-api",
          "type": "http-rest",
          "description": "Fetches data via REST API"
        }
      ]
    }
  ]
}
```

### c3-components.json

```json
{
  "timestamp": "2025-11-15T20:30:00Z",
  "components": [
    {
      "id": "auth-component",
      "name": "Authentication Component",
      "container": "frontend-spa",
      "path": "src/features/auth",
      "observations": [
        "Handles JWT token management",
        "Integrates with OAuth 2.0",
        "Stores tokens in localStorage"
      ],
      "relations": [
        {
          "target": "user-component",
          "type": "dependency",
          "description": "Provides user authentication state"
        }
      ]
    }
  ]
}
```

---

## Observations and Relations

### Observations

**Purpose:** Document key findings about each entity (system, container, component)

**Format:** Array of strings, each describing a notable characteristic

**Examples:**
- "Uses event-driven architecture"
- "Implements CQRS pattern"
- "Heavy use of async/await patterns"
- "No error handling in critical paths"
- "Well-tested with 85% code coverage"

### Relations

**Purpose:** Document relationships and dependencies between entities

**Format:** Array of objects with target, type, and description

**Relation Types:**
- `http` / `http-rest` / `http-graphql`
- `grpc`
- `message-queue`
- `database-query`
- `dependency`
- `inheritance`
- `composition`

**Examples:**
```json
{
  "target": "payment-service",
  "type": "http-rest",
  "description": "Processes payments via REST API"
}
```

---

## Best Practices

### 1. Start High, Go Deep

Always start with C1 (system context) before moving to C2, C3. This ensures proper hierarchy and context.

### 2. Incremental Updates

Use timestamp checking to only reprocess changed repositories. This keeps the workflow efficient.

### 3. Observations Over Opinions

Document what you observe in the code, not what you think should be there.

### 4. Relations Matter

Carefully document relationships - they're critical for understanding architecture.

### 5. Validation First

Always validate JSON output before moving to the next phase. Invalid data compounds errors.

---

## Integration with basic-memory

All generated documentation is stored in the basic-memory MCP server:

1. **Create Notes:** Each markdown file becomes a knowledge note
2. **Search:** Full-text search across all C4 documentation
3. **Multi-Project:** Share C4 knowledge across projects
4. **Sync:** Keep documentation synchronized
5. **Permalinks:** Stable references to documentation

---

## References

- [C4 Model Official Site](https://c4model.com/)
- [Simon Brown's C4 Model](https://www.youtube.com/watch?v=x2-rSnhpw0g)
- [Structurizr](https://structurizr.com/)

---

**Last Updated:** 2025-11-15
**Version:** 1.0.0
