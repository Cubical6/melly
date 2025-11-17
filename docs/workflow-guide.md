# Melly Workflow Guide

> **Practical guide to using Melly's C4 model workflow for codebase analysis**

## Quick Start

### Prerequisites

Before using Melly, ensure you have:

1. **Claude Code** installed and configured
2. **basic-memory MCP server** installed and running
   - See [plugins/basic-memory](../plugins/basic-memory) for installation
   - Enable permalinks and sync in settings
3. **Melly marketplace** components installed
   ```bash
   cd /path/to/melly
   /plugin add ./plugins/abstractor-agent
   /plugin add ./plugins/skill-builder
   /plugin add ./plugins/basic-memory
   /plugin add ./plugins/melly-init          # ✅ Phase 1 implemented
   ```

### Implementation Status

- ✅ **Phase 1: Initialization** (`/melly-init`) - IMPLEMENTED (2025-11-17)
  - Command: `plugins/melly-init/commands/melly-init.md` (33 lines)
  - Agent: `plugins/melly-init/agents/c4model-explorer.md` (70 lines)
  - Status: Production-ready, follows Claude Code best practices
- 🔴 Phase 2: C1 Systems (`/melly-c1-systems`) - Not yet implemented
- 🔴 Phase 3: C2 Containers (`/melly-c2-containers`) - Not yet implemented
- 🔴 Phase 4: C3 Components (`/melly-c3-components`) - Not yet implemented
- 🔴 Phase 5: Documentation (`/melly-doc-c4model`) - Not yet implemented
- 🔴 Phase 6: Visualization (`/melly-draw-c4model`) - Not yet implemented

---

## Complete Workflow Example

### Scenario: Analyzing a Web Application

Let's walk through analyzing a typical web application with frontend and backend repositories.

#### Step 1: Initialize the Exploration

```bash
/melly-init
```

**What it does:**
- Prompts you for repository locations
- Scans all repositories in the specified path
- Identifies package manifests (package.json, composer.json, etc.)
- Generates `init.json` with metadata

**Example interaction:**
```
You: /melly-init

Claude: I'll help you initialize the C4 model exploration.
        Where are your code repositories located?

You: /home/user/projects/my-web-app

Claude: Scanning repositories in /home/user/projects/my-web-app...

        Found 2 repositories:
        1. my-web-app/frontend (React + TypeScript)
        2. my-web-app/backend (Node.js + Express)

        Generated init.json with repository metadata.
        ✓ Validated with validate-init.py
```

**Output:**
- `init.json` created in project root
- Repository structure mapped
- Ready for C1 analysis

---

#### Step 2: Identify Systems (C1)

```bash
/melly-c1-systems
```

**What it does:**
- Reads `init.json`
- Identifies high-level systems
- Creates folder structure in `knowledge-base/systems/`
- Generates `c1-systems.json`

**Example interaction:**
```
You: /melly-c1-systems

Claude: Analyzing repositories for C1 system identification...

        Identified 2 systems:
        1. Web Application (frontend repository)
           - React-based SPA
           - TypeScript implementation
           - Modern build tools (Vite)

        2. API Server (backend repository)
           - Express.js REST API
           - PostgreSQL database
           - JWT authentication

        Created system folders:
        - knowledge-base/systems/web-application/
        - knowledge-base/systems/api-server/

        Generated c1-systems.json with observations and relations.
        ✓ Validated with validate-c1-systems.py
```

**Output:**
- System folders created
- `c1-systems.json` with system details
- Observations and relations documented

---

#### Step 3: Identify Containers (C2)

```bash
/melly-c2-containers
```

**What it does:**
- Reads `c1-systems.json`
- Identifies containers within each system
- Detects technology stack
- Generates `c2-containers.json`

**Example interaction:**
```
You: /melly-c2-containers

Claude: Analyzing systems for C2 container identification...

        Web Application System:
        ├── Frontend SPA Container
        │   ├── Technology: React 18, TypeScript 5, Vite
        │   ├── Runtime: Browser
        │   └── Port: Development on 5173

        API Server System:
        ├── Backend API Container
        │   ├── Technology: Express.js, Node.js 20
        │   ├── Runtime: Server (Node.js)
        │   └── Port: 3000
        ├── PostgreSQL Database
        │   ├── Technology: PostgreSQL 15
        │   ├── Runtime: Server (Docker container)
        │   └── Port: 5432
        └── Redis Cache
            ├── Technology: Redis 7
            ├── Runtime: Server (Docker container)
            └── Port: 6379

        Generated c2-containers.json
        ✓ Validated with validate-c2-containers.py
```

**Output:**
- `c2-containers.json` with container details
- Technology stack documented
- Container relationships mapped

---

#### Step 4: Identify Components (C3)

```bash
/melly-c3-components
```

**What it does:**
- Reads `c2-containers.json`
- Identifies components within containers
- Analyzes code structure
- Generates `c3-components.json`

**Example interaction:**
```
You: /melly-c3-components

Claude: Analyzing containers for C3 component identification...

        Frontend SPA Container:
        ├── Authentication Component
        │   ├── Path: src/features/auth
        │   ├── Handles JWT tokens
        │   └── OAuth 2.0 integration
        ├── User Management Component
        │   ├── Path: src/features/users
        │   ├── CRUD operations
        │   └── Profile management
        └── Dashboard Component
            ├── Path: src/features/dashboard
            └── Data visualization

        Backend API Container:
        ├── Authentication Service
        │   ├── Path: src/services/auth
        │   ├── JWT generation
        │   └── Password hashing (bcrypt)
        ├── User Repository
        │   ├── Path: src/repositories/user
        │   └── Database access layer
        └── API Routes
            ├── Path: src/routes
            └── Express route handlers

        Generated c3-components.json
        ✓ Validated with validate-c3-components.py
```

**Output:**
- `c3-components.json` with component details
- Code structure documented
- Component dependencies mapped

---

#### Step 5: Generate Documentation

```bash
/melly-doc-c4model
```

**What it does:**
- Reads all JSON files (init, c1, c2, c3)
- Generates markdown documentation
- Stores in basic-memory knowledge base
- Creates organized documentation structure

**Example interaction:**
```
You: /melly-doc-c4model

Claude: Generating C4 model documentation...

        Processing C1 Systems:
        ✓ web-application.md
        ✓ api-server.md

        Processing C2 Containers:
        ✓ frontend-spa.md
        ✓ backend-api.md
        ✓ postgresql-database.md
        ✓ redis-cache.md

        Processing C3 Components:
        ✓ authentication-component.md
        ✓ user-management-component.md
        ✓ dashboard-component.md
        ✓ authentication-service.md
        ✓ user-repository.md
        ✓ api-routes.md

        All documentation stored in basic-memory knowledge base.
        ✓ Validated with validate-markdown.py
```

**Output:**
- Markdown files in `knowledge-base/systems/*/c1|c2|c3/`
- Documentation stored in basic-memory
- Searchable knowledge base created

---

#### Step 6: Visualize Architecture

```bash
/melly-draw-c4model
```

**What it does:**
- Reads all JSON files
- Generates Mermaid diagrams
- Creates Obsidian canvas files
- Visualizes architecture at all levels

**Example interaction:**
```
You: /melly-draw-c4model

Claude: Generating visual diagrams...

        C1 System Context Diagram:
        ✓ systems-overview.canvas

        C2 Container Diagrams:
        ✓ web-application-containers.canvas
        ✓ api-server-containers.canvas

        C3 Component Diagrams:
        ✓ frontend-spa-components.canvas
        ✓ backend-api-components.canvas

        All diagrams stored in basic-memory.
        Open in Obsidian to view visualizations.
```

**Output:**
- Mermaid diagrams generated
- Obsidian canvas files created
- Visual architecture documentation

---

## Incremental Updates

### When Code Changes

If your codebase changes, you can incrementally update the C4 model:

#### Update Workflow

1. **Re-run initialization** (if new repos added):
   ```bash
   /melly-init
   ```
   - Only new/changed repositories will be processed
   - Existing data merged with updates

2. **Re-run affected levels**:
   ```bash
   /melly-c1-systems    # If system structure changed
   /melly-c2-containers # If containers changed
   /melly-c3-components # If components changed
   ```
   - Timestamp validation ensures efficient reprocessing
   - Only changed entities are updated

3. **Regenerate documentation**:
   ```bash
   /melly-doc-c4model
   /melly-draw-c4model
   ```

### Example: Adding a New Service

```
You: I added a new authentication microservice to my backend.
     How do I update the C4 model?

Claude: Since you added a new service, we should update from C2 level:

        1. First, update the initialization:
           /melly-init

        2. Update C2 containers (new service will be detected):
           /melly-c2-containers

        3. Analyze the new service's components:
           /melly-c3-components

        4. Regenerate documentation:
           /melly-doc-c4model

        5. Update visualizations:
           /melly-draw-c4model

        This will integrate the new authentication service into your
        existing C4 model without regenerating everything.
```

---

## Advanced Usage

### Selective Visualization

Generate diagrams for specific levels:

```bash
/melly-draw-c4model c1    # Only system context
/melly-draw-c4model c2    # Only containers
/melly-draw-c4model c3    # Only components
```

### Custom Analysis

Ask Claude to analyze specific aspects:

```
You: What are the security concerns in my authentication flow?

Claude: [Activates c4model skills and searches knowledge base]

        Based on the C4 documentation, I found these security concerns:

        1. Frontend Authentication Component (C3):
           - Stores JWT tokens in localStorage (vulnerable to XSS)
           - Recommendation: Use httpOnly cookies instead

        2. Backend Authentication Service (C3):
           - Password hashing uses bcrypt (good!)
           - JWT tokens don't expire (security risk)
           - Recommendation: Add token expiration (e.g., 15 minutes)

        3. API Server Container (C2):
           - No rate limiting on auth endpoints
           - Recommendation: Implement rate limiting to prevent brute force

        Would you like me to create a task list to address these concerns?
```

### Knowledge Base Queries

Search the C4 documentation:

```
You: Show me all components that interact with the database

Claude: [Searches basic-memory knowledge base]

        Found 3 components with database interactions:

        1. User Repository (Backend API)
           - Location: src/repositories/user
           - Database: PostgreSQL
           - Relations: CRUD operations on users table

        2. Session Store (Backend API)
           - Location: src/services/session
           - Database: Redis
           - Relations: Session caching and expiration

        3. Analytics Collector (Backend API)
           - Location: src/services/analytics
           - Database: PostgreSQL
           - Relations: Writes to analytics table
```

---

## Troubleshooting

### Common Issues

#### 1. "init.json not found"

**Problem:** Trying to run `/melly-c1-systems` before `/melly-init`

**Solution:**
```bash
/melly-init  # Always run this first
```

#### 2. "Timestamp order violation"

**Problem:** JSON files are out of sync (older C2 than C1)

**Solution:**
```bash
# Rerun the workflow in order
/melly-c1-systems
/melly-c2-containers
/melly-c3-components
```

#### 3. "basic-memory MCP not available"

**Problem:** MCP server not running

**Solution:**
1. Check MCP server status in Claude Code settings
2. Restart basic-memory server
3. Verify connection with:
   ```
   You: Can you list my knowledge notes?
   ```

#### 4. "Validation failed"

**Problem:** Generated JSON doesn't match schema

**Solution:**
- Check error message from validation script
- Review the generated JSON file
- Report issue if validation is incorrect

---

## Best Practices

### 1. Start Fresh

For new projects, always start with `/melly-init` and work through the levels sequentially.

### 2. Document Observations

When Claude generates observations, review them for accuracy. You can manually edit JSON files if needed.

### 3. Keep Documentation in Sync

After code changes, update the C4 model promptly to keep documentation accurate.

### 4. Use Knowledge Base

Leverage basic-memory's search capabilities to find relevant documentation quickly.

### 5. Visualize Early

Generate visualizations frequently - they help validate your understanding of the architecture.

---

## Example Projects

### Monorepo Example

```
/home/user/projects/monorepo/
├── packages/
│   ├── frontend/
│   ├── backend/
│   ├── shared/
│   └── mobile/
```

**Workflow:**
```bash
/melly-init               # Point to /home/user/projects/monorepo
/melly-c1-systems        # Identifies 4 systems (frontend, backend, shared, mobile)
/melly-c2-containers     # Analyzes each package
/melly-c3-components     # Deep dive into components
/melly-doc-c4model       # Generate docs
/melly-draw-c4model         # Create diagrams
```

### Microservices Example

```
/home/user/projects/microservices/
├── auth-service/
├── user-service/
├── payment-service/
├── notification-service/
└── api-gateway/
```

**Workflow:**
```bash
/melly-init               # Point to /home/user/projects/microservices
/melly-c1-systems        # Each service is a system
/melly-c2-containers     # Service containers + databases
/melly-c3-components     # Service internals
/melly-doc-c4model       # Generate docs
/melly-draw-c4model         # Create architecture diagrams
```

---

## Integration with Other Tools

### Obsidian

1. Open `knowledge-base/` in Obsidian
2. Browse generated markdown files
3. View canvas diagrams
4. Use graph view to see relationships

### CI/CD

Add to your pipeline:

```yaml
# .github/workflows/c4-docs.yml
name: Update C4 Documentation

on:
  push:
    branches: [main]

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Update C4 Model
        run: |
          claude -p "/melly-init && /melly-c1-systems && /melly-c2-containers && /melly-c3-components && /melly-doc-c4model"
```

---

## Available Components

### Implemented Plugins

Melly currently provides the following production-ready components:

#### Core Plugins (3)

1. **abstractor-agent** ✅
   - Deep architectural analysis through subagent-driven exploration
   - Generates C4 diagrams and subsystem catalogs
   - Use: `/system-archaeologist`

2. **skill-builder** ✅
   - Meta-skill for creating and editing Claude Code skills
   - CLI tools and Python scripting patterns
   - Use: "Help me create a skill for [task]"

3. **basic-memory** ✅
   - Knowledge management via MCP server
   - Multi-project support with sync
   - Obsidian canvas integration

#### Validation & Templates (1)

1. **melly-validation** ✅
   - Centralized validation scripts (7 validators)
   - Markdown generators (3 generators)
   - JSON templates for all C4 levels
   - Total: 2,859 lines of production-ready code

#### C4 Methodology Skills (1/5)

1. **c4model-c1** ✅
   - **C1 (System Context) methodology skill**
   - Comprehensive guidance for system identification
   - System identification rules and criteria
   - Actor identification (users and external systems)
   - Boundary detection methodology
   - Relationship mapping (8 relationship types)
   - Observation guidelines (8 categories with evidence)
   - 4 complete architecture patterns (web, microservices, event-driven, mobile)
   - Complete workflow integration (init.json → c1-systems.json)
   - **Documentation**: 1,558 lines (400 README + 1,158 SKILL.md)
   - **Use**: Automatically activates when working with system identification

### In Development

The following workflow components are currently being developed:

- **c4model-c2** 🔴 - C2 Container methodology skill
- **c4model-c3** 🔴 - C3 Component methodology skill
- **c4model-observations** 🔴 - Observation documentation skill
- **c4model-relations** 🔴 - Relation documentation skill
- **melly-init** 🔴 - Initialization workflow command
- **melly-c1** 🔴 - C1 Systems workflow command
- **melly-c2** 🔴 - C2 Containers workflow command
- **melly-c3** 🔴 - C3 Components workflow command
- **melly-doc** 🔴 - Documentation generation command
- **melly-draw** 🔴 - Diagram visualization command

**Legend:** ✅ Completed | 🔴 In Development

---

## Next Steps

After completing the workflow:

1. **Review Documentation** - Verify accuracy of generated docs
2. **Share with Team** - Commit documentation to version control
3. **Keep Updated** - Re-run workflow when architecture changes
4. **Extend** - Add custom skills for project-specific analysis
5. **Contribute** - Share your improvements with the Melly community

---

## Resources

- [C4 Model Methodology](./c4model-methodology.md) - Deep dive into C4 approach
- [CLAUDE.md](../CLAUDE.md) - Implementation guide for extending Melly
- [TASKS.md](../TASKS.md) - Development roadmap

---

**Last Updated:** 2025-11-17
**Version:** 1.0.0
