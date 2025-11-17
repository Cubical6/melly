# Technology Detection Patterns

This document provides comprehensive patterns for detecting technologies and frameworks in C4 Model Level 2 (Container) analysis.

## Pattern 1: npm/package.json Detection

### Frontend Frameworks

**React:**

```json
{
  "dependencies": {
    "react": "^18.2.0",           // → React 18 SPA
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.0" // → Client-side routing
  }
}
```
→ **Container:** React SPA, runs in browser

**Vue:**

```json
{
  "dependencies": {
    "vue": "^3.3.0",              // → Vue 3 SPA
    "@vue/runtime-core": "^3.3.0"
  }
}
```
→ **Container:** Vue SPA, runs in browser

**Angular:**

```json
{
  "dependencies": {
    "@angular/core": "^16.0.0",   // → Angular 16 SPA
    "@angular/platform-browser": "^16.0.0"
  }
}
```
→ **Container:** Angular SPA, runs in browser

### Backend Frameworks

**Express.js:**

```json
{
  "dependencies": {
    "express": "^4.18.2",         // → Express API Server
    "cors": "^2.8.5",
    "helmet": "^7.0.0"
  }
}
```
→ **Container:** Express.js API Server, runs on Node.js

**NestJS:**

```json
{
  "dependencies": {
    "@nestjs/core": "^10.0.0",    // → NestJS API Server
    "@nestjs/platform-express": "^10.0.0"
  }
}
```
→ **Container:** NestJS API Server, runs on Node.js

**Fastify:**

```json
{
  "dependencies": {
    "fastify": "^4.20.0",         // → Fastify API Server
    "@fastify/cors": "^8.3.0"
  }
}
```
→ **Container:** Fastify API Server, runs on Node.js

### Full-Stack Frameworks

**Next.js:**

```json
{
  "dependencies": {
    "next": "^13.4.0",            // → Next.js Full-Stack
    "react": "^18.2.0"
  }
}
```
→ **Container:** Next.js Application (SSR + API routes), runs on Node.js server

**Nuxt.js:**

```json
{
  "dependencies": {
    "nuxt": "^3.6.0",             // → Nuxt.js Full-Stack
    "vue": "^3.3.0"
  }
}
```
→ **Container:** Nuxt.js Application, runs on Node.js server

### Mobile Frameworks

**React Native:**

```json
{
  "dependencies": {
    "react-native": "^0.72.0"     // → React Native Mobile App
  }
}
```
→ **Container:** React Native Mobile Application, runs on iOS/Android

**Ionic:**

```json
{
  "dependencies": {
    "@ionic/react": "^7.0.0",     // → Ionic Mobile App
    "capacitor": "^5.0.0"
  }
}
```
→ **Container:** Ionic Mobile Application, runs on iOS/Android

### Desktop Frameworks

**Electron:**

```json
{
  "dependencies": {
    "electron": "^25.0.0"         // → Electron Desktop App
  }
}
```
→ **Container:** Electron Desktop Application, runs on Windows/macOS/Linux

---

## Pattern 2: Python Detection

### Web Frameworks

**Django:**

```txt
# requirements.txt
Django==4.2.0                   # → Django Web Application
djangorestframework==3.14.0     # → Also has REST API
psycopg2-binary==2.9.6          # → Uses PostgreSQL
```
→ **Container:** Django Web Application + API, runs on Python 3.x

**Flask:**

```txt
# requirements.txt
Flask==2.3.0                    # → Flask API Server
Flask-CORS==4.0.0
gunicorn==21.0.0                # → WSGI server for production
```
→ **Container:** Flask API Server, runs on Python 3.x with Gunicorn

**FastAPI:**

```txt
# requirements.txt
fastapi==0.100.0                # → FastAPI API Server
uvicorn[standard]==0.23.0       # → ASGI server
pydantic==2.0.0                 # → Data validation
```
→ **Container:** FastAPI API Server, runs on Python 3.x with Uvicorn

### Background Workers

**Celery:**

```txt
# requirements.txt
celery==5.3.0                   # → Celery Worker
redis==4.6.0                    # → Uses Redis as broker
```
→ **Container:** Celery Worker, runs on Python 3.x

---

## Pattern 3: Java Detection

### Maven (pom.xml)

**Spring Boot:**

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>3.1.0</version>
    </dependency>
</dependencies>
```
→ **Container:** Spring Boot API Server, runs on JVM 17+

### Gradle (build.gradle)

**Quarkus:**

```groovy
dependencies {
    implementation 'io.quarkus:quarkus-resteasy-reactive'
    implementation 'io.quarkus:quarkus-jdbc-postgresql'
}
```
→ **Container:** Quarkus API Server, runs on JVM or native

---

## Pattern 4: Docker Detection

### Dockerfile Examples

**Node.js API Server:**

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```
→ **Container:** Node.js API Server, containerized with Docker, runs on Node.js 18

**Python FastAPI Server:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```
→ **Container:** Python FastAPI Server, containerized with Docker, runs on Python 3.11

### docker-compose.yml

**Multi-Container Application:**

```yaml
services:
  api:
    build: ./api
    ports:
      - "3000:3000"
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
```
→ **Containers identified:**
1. API Server (custom built from ./api)
2. PostgreSQL Database (postgres:15-alpine)
3. Redis Cache (redis:7-alpine)

---

## Pattern 5: Kubernetes Detection

### Deployment YAML

**Frontend SPA with Nginx:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-spa
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: nginx
        image: nginx:1.25-alpine
        ports:
        - containerPort: 80
```
→ **Container:** Nginx Web Server, containerized with K8s, serves static SPA

**API Server:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  template:
    spec:
      containers:
      - name: api
        image: myapp/api:1.0
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```
→ **Container:** Custom API Server, containerized with K8s

---

## Pattern 6: Serverless Detection

### Serverless Framework (serverless.yml)

**AWS Lambda:**

```yaml
service: my-api
provider:
  name: aws
  runtime: nodejs18.x
functions:
  api:
    handler: handler.main
    events:
      - http:
          path: /api/{proxy+}
          method: ANY
```
→ **Container:** AWS Lambda Function, runs on Node.js 18, serverless

### Vercel (vercel.json)

**Next.js on Vercel:**

```json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ]
}
```
→ **Container:** Next.js Application, serverless deployment on Vercel

---

## Detection CLI Commands

### Find Package Manifests

```bash
# Find npm package.json files
find . -name "package.json" -not -path "*/node_modules/*"

# Find Python requirements files
find . -name "requirements.txt" -o -name "Pipfile" -o -name "pyproject.toml"

# Find Java build files
find . -name "pom.xml" -o -name "build.gradle"

# Find Docker files
find . -name "Dockerfile" -o -name "docker-compose.yml"

# Find Kubernetes manifests
find . -name "*.yaml" -path "*/k8s/*" -o -path "*/kubernetes/*"
```

### Analyze Dependencies

```bash
# Node.js: List dependencies
cat package.json | jq '.dependencies'

# Python: List installed packages
pip list

# Java Maven: Show dependency tree
mvn dependency:tree

# Docker: Show image info
docker inspect <image-name>
```

### Grep for Framework Indicators

```bash
# Search for web frameworks
grep -r "express\|fastify\|nestjs" package.json

# Search for frontend frameworks
grep -r "react\|vue\|angular" package.json

# Search for Python frameworks
grep -r "django\|flask\|fastapi" requirements.txt

# Search for container orchestration
grep -r "kubernetes\|docker-compose" .
```

---

## Best Practices

1. **Check multiple indicators** - Don't rely on a single file
2. **Verify versions** - Framework versions matter for capabilities
3. **Look for actual usage** - Dependency presence doesn't guarantee usage
4. **Consider build artifacts** - Check dist/, build/, target/ folders
5. **Examine runtime configs** - .env files, config/*.json
6. **Review deployment configs** - Dockerfile, K8s manifests, serverless.yml

## Common Pitfalls

1. **Monorepo confusion** - Multiple package.json files may exist
2. **Dev vs prod dependencies** - Only production deps matter for runtime
3. **Transitive dependencies** - Don't confuse direct vs indirect deps
4. **Deprecated patterns** - Some frameworks have legacy detection patterns
5. **Polyglot projects** - May have multiple technologies in different folders
