# Container Identification Methodology

Detailed step-by-step process for identifying C2 containers within systems.

## Step 1: Understand System Decomposition

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

## Step 2: Apply Container Identification Rules

### A Container IS:

1. **Deployable independently** - Has own build/deployment process and artifact
2. **Executes code OR stores data** - Runs application logic or persists data
3. **Has distinct technology stack** - Built with specific language/framework
4. **Has runtime environment** - Runs in specific environment (browser, server, mobile, cloud)
5. **Communicates via defined protocols** - HTTP, database connections, message queues
6. **Infrastructure component** - Databases, caches, message brokers required for system operation

### A Container is NOT:

1. **Code modules within an application** (these are C3 components)
   - "Authentication Module" in React app → C3 Component
   - "Express API Application" → C2 Container

2. **Configuration files or static assets** - package.json, CSS files, images

3. **Development tools** - Webpack, Babel, ESLint, Jest test runner

4. **Generic names without technology and version**
   - "Frontend Container" → "React 18.2 SPA Container"
   - "Backend Container" → "Express 4.18 API Server Container"
   - "React SPA" (missing version) → "React 18.2 SPA"

5. **Names without versions** (versions MUST come from manifest files)
   - "React SPA" → "React 18.2.0 SPA"
   - "Express API Server" → "Express 4.18.2 API Server"

   **RULE (Mandatory):** You MUST extract versions from manifest files:
   - package.json (JavaScript/TypeScript)
   - requirements.txt / pyproject.toml (Python)
   - pom.xml / build.gradle (Java)
   - Cargo.toml (Rust)
   - go.mod (Go)

   This is NOT optional. Reading manifests is NOT "line-by-line code analysis" - it's standard C2 technology detection.

   **Failure to include versions from manifests = VIOLATION of C2 methodology = Critical validation error.**

6. **Over-granular decomposition**
   - "Login API" + "Register API" → "User Management API"

> **See [Troubleshooting Guide](./troubleshooting-guide-c2.md#problem-too-many-containers-identified) for detailed guidance.**

## Step 3: Analyze Repository Structure

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

## Step 4: Detect Technology Stack

For each container, identify:

### Primary Language
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

### Framework/Platform
React, Vue, Angular (frontend) | Express, NestJS, FastAPI, Django, Spring Boot (backend)

**Detection methods:**
- Check dependencies in package manifests
- Look for framework-specific files (`angular.json`, `vue.config.js`)
- Analyze import statements

> **See [Technology Detection Patterns](./technology-detection-patterns.md) for complete detection guide.**

## Step 5: Identify Runtime Environment

For each container, determine:

### Environment
- **browser** - Runs in web browser (SPAs)
- **server** - Runs on server (APIs, web servers)
- **mobile** - Runs on mobile device (iOS/Android)
- **cloud** - Runs in cloud (Lambda, Cloud Functions)
- **edge** - Runs at edge (Cloudflare Workers)

### Platform
- Browser: Chrome, Firefox, Safari, Edge
- Server: Linux, Node.js 18, Python 3.11, JVM 17
- Mobile: iOS 14+, Android 11+

### Containerization
- **Containerized:** true/false
- **Container Technology:** Docker, Kubernetes, ECS
- **Container Image:** `node:18-alpine`, `python:3.11-slim`
