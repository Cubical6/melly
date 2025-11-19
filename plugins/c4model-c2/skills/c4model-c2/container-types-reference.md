# Container Types Reference

This document provides comprehensive reference for all C4 Model Level 2 (Container) types with detailed examples and runtime characteristics.

## Type 1: Single-Page Application (SPA)

**Type:** `spa`

**Description:** Client-side web application that runs entirely in the browser

**Technology Indicators:**
- React, Vue, Angular, Svelte
- Webpack, Vite, or similar bundler
- Build output to static files (HTML/CSS/JS)

**Runtime:**
- Environment: `browser`
- Platform: `Chrome, Firefox, Safari, Edge`
- Containerized: `false` (static files)

**Example:**
```json
{
  "id": "customer-portal-spa",
  "name": "Customer Portal SPA",
  "type": "spa",
  "technology": {
    "primary_language": "TypeScript",
    "framework": "React 18.2.0",
    "libraries": [
      {"name": "React Router", "version": "6.14.0", "purpose": "Client-side routing"},
      {"name": "Redux Toolkit", "version": "1.9.5", "purpose": "State management"},
      {"name": "Axios", "version": "1.4.0", "purpose": "HTTP client"}
    ]
  },
  "runtime": {
    "environment": "browser",
    "platform": "Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)",
    "containerized": false
  }
}
```

---

## Type 2: API Server / Application Server

**Type:** `app-server` or `api`

**Description:** Server-side application that exposes APIs or serves requests

**Technology Indicators:**
- Express, NestJS, Fastify (Node.js)
- Django, Flask, FastAPI (Python)
- Spring Boot, Quarkus (Java)
- Runs on server, listens on port

**Runtime:**
- Environment: `server`
- Platform: `Linux, Node.js 18, Python 3.11, JVM 17`
- Containerized: `true` (usually)

**Example:**
```json
{
  "id": "ecommerce-api",
  "name": "E-Commerce REST API",
  "type": "api",
  "technology": {
    "primary_language": "TypeScript",
    "framework": "NestJS 10.0.0",
    "libraries": [
      {"name": "Prisma", "version": "5.0.0", "purpose": "ORM"},
      {"name": "Passport", "version": "0.6.0", "purpose": "Authentication"},
      {"name": "class-validator", "version": "0.14.0", "purpose": "Validation"}
    ]
  },
  "runtime": {
    "environment": "server",
    "platform": "Linux x64, Node.js 18.16.0",
    "containerized": true,
    "container_technology": "Docker",
    "deployment_model": "Kubernetes (3 replicas)"
  }
}
```

---

## Type 3: Database

**Type:** `database`

**Description:** Data persistence layer (relational or NoSQL)

**Technology Indicators:**
- PostgreSQL, MySQL, MariaDB (relational)
- MongoDB, Cassandra, DynamoDB (NoSQL)
- Docker image or managed service

**Runtime:**
- Environment: `server` or `cloud`
- Platform: `Linux, Docker`
- Containerized: `true` (often)

**Example:**
```json
{
  "id": "main-database",
  "name": "Main PostgreSQL Database",
  "type": "database",
  "technology": {
    "primary_language": "SQL",
    "framework": "PostgreSQL 15.3",
    "libraries": []
  },
  "runtime": {
    "environment": "server",
    "platform": "Linux x64, Docker",
    "containerized": true,
    "container_technology": "Docker",
    "deployment_model": "Single instance with volume persistence"
  }
}
```

---

## Type 4: Cache

**Type:** `cache`

**Description:** In-memory data store for caching and session management

**Technology Indicators:**
- Redis, Memcached
- In-memory key-value store
- TTL-based expiration

**Runtime:**
- Environment: `server`
- Platform: `Linux`
- Containerized: `true` (usually)

**Example:**
```json
{
  "id": "session-cache",
  "name": "Redis Session Cache",
  "type": "cache",
  "technology": {
    "primary_language": "N/A",
    "framework": "Redis 7.0",
    "libraries": []
  },
  "runtime": {
    "environment": "server",
    "platform": "Linux x64",
    "containerized": true,
    "container_technology": "Docker"
  }
}
```

---

## Type 5: Message Broker

**Type:** `message-broker`

**Description:** Message queue or event streaming platform

**Technology Indicators:**
- RabbitMQ, Apache Kafka, AWS SQS, Redis Pub/Sub
- Async message passing
- Producers and consumers

**Runtime:**
- Environment: `server` or `cloud`
- Platform: `Linux, Docker, or managed cloud service`
- Containerized: `true` (usually)

**Example:**
```json
{
  "id": "event-broker",
  "name": "RabbitMQ Message Broker",
  "type": "message-broker",
  "technology": {
    "primary_language": "N/A",
    "framework": "RabbitMQ 3.12",
    "libraries": []
  },
  "runtime": {
    "environment": "server",
    "platform": "Linux x64",
    "containerized": true,
    "container_technology": "Kubernetes"
  }
}
```

---

## Type 6: Web Server / Reverse Proxy

**Type:** `web-server`

**Description:** HTTP server, reverse proxy, or load balancer

**Technology Indicators:**
- Nginx, Apache, Traefik
- Serves static files
- Reverse proxy to backend services

**Runtime:**
- Environment: `server`
- Platform: `Linux`
- Containerized: `true` (usually)

**Example:**
```json
{
  "id": "nginx-proxy",
  "name": "Nginx Reverse Proxy",
  "type": "web-server",
  "technology": {
    "primary_language": "N/A",
    "framework": "Nginx 1.25",
    "libraries": []
  },
  "runtime": {
    "environment": "server",
    "platform": "Linux x64",
    "containerized": true,
    "container_technology": "Kubernetes"
  }
}
```

---

## Type 7: Worker / Background Service

**Type:** `worker`

**Description:** Background job processor, cron jobs, queue consumers

**Technology Indicators:**
- Celery workers, Sidekiq, Bull queue
- Processes background tasks
- Often queue-based

**Runtime:**
- Environment: `server`
- Platform: `Linux, Python, Ruby, Node.js`
- Containerized: `true` (usually)

**Example:**
```json
{
  "id": "email-worker",
  "name": "Email Processing Worker",
  "type": "worker",
  "technology": {
    "primary_language": "Python",
    "framework": "Celery 5.3.0",
    "libraries": [
      {"name": "sendgrid", "version": "6.10.0", "purpose": "Email sending"}
    ]
  },
  "runtime": {
    "environment": "server",
    "platform": "Linux x64, Python 3.11",
    "containerized": true,
    "container_technology": "Kubernetes"
  }
}
```

---

## Type 8: Mobile Application

**Type:** `mobile-app`

**Description:** Native or hybrid mobile application

**Technology Indicators:**
- React Native, Flutter, Swift, Kotlin
- Runs on mobile devices
- Platform-specific build outputs

**Runtime:**
- Environment: `mobile`
- Platform: `iOS, Android`
- Containerized: `false`

**Example:**
```json
{
  "id": "shopping-mobile-app",
  "name": "Shopping Mobile App",
  "type": "mobile-app",
  "technology": {
    "primary_language": "TypeScript",
    "framework": "React Native 0.72.0",
    "libraries": [
      {"name": "React Navigation", "version": "6.1.0", "purpose": "Navigation"}
    ]
  },
  "runtime": {
    "environment": "mobile",
    "platform": "iOS 14+, Android 11+",
    "containerized": false
  }
}
```

---

## Type 9: Desktop Application

**Type:** `desktop-app`

**Description:** Desktop application for Windows, macOS, or Linux

**Technology Indicators:**
- Electron, Tauri, Qt
- Native desktop frameworks
- Installable applications

**Runtime:**
- Environment: `desktop`
- Platform: `Windows, macOS, Linux`
- Containerized: `false`

**Example:**
```json
{
  "id": "admin-desktop-app",
  "name": "Admin Desktop Application",
  "type": "desktop-app",
  "technology": {
    "primary_language": "TypeScript",
    "framework": "Electron 25.0.0",
    "libraries": []
  },
  "runtime": {
    "environment": "desktop",
    "platform": "Windows 10+, macOS 11+, Linux",
    "containerized": false
  }
}
```

---

## Type 10: File Storage

**Type:** `file-storage`

**Description:** Object storage, file system, or CDN

**Technology Indicators:**
- AWS S3, MinIO, Azure Blob Storage
- File upload/download
- Static asset storage

**Runtime:**
- Environment: `cloud` or `server`
- Platform: `Cloud provider or self-hosted`
- Containerized: `varies`

**Example:**
```json
{
  "id": "media-storage",
  "name": "S3 Media Storage",
  "type": "file-storage",
  "technology": {
    "primary_language": "N/A",
    "framework": "AWS S3",
    "libraries": []
  },
  "runtime": {
    "environment": "cloud",
    "platform": "AWS",
    "containerized": false
  }
}
```

---

## Type Selection Guide

### Decision Tree

1. **Runs in browser?** → SPA (Type 1)
2. **Exposes API/HTTP endpoints?** → API Server (Type 2)
3. **Stores persistent data?** → Database (Type 3)
4. **In-memory caching?** → Cache (Type 4)
5. **Async messaging?** → Message Broker (Type 5)
6. **Proxies/serves static files?** → Web Server (Type 6)
7. **Background jobs?** → Worker (Type 7)
8. **Mobile device?** → Mobile App (Type 8)
9. **Desktop application?** → Desktop App (Type 9)
10. **File/object storage?** → File Storage (Type 10)

### Common Combinations

**Typical Web App:**
- SPA (frontend)
- API Server (backend)
- Database (persistence)
- Cache (session/performance)

**Microservices:**
- Multiple API Servers (services)
- Message Broker (async communication)
- Multiple Databases (per-service)
- Web Server (gateway/proxy)

**Full-Stack Application:**
- API Server with SSR (Next.js/Nuxt)
- Database
- Cache
- File Storage (uploads)

**Enterprise System:**
- SPA (admin portal)
- Mobile App (customer app)
- Multiple API Servers (microservices)
- Worker (background jobs)
- Message Broker (events)
- Multiple Databases
- Cache
- File Storage

---

## Best Practices

1. **One container = one deployable unit** - Don't split unnecessarily
2. **Runtime matters** - Document where container actually runs
3. **Technology precision** - Include versions (React 18, not just React)
4. **Containerization awareness** - Note Docker/K8s deployment
5. **Communication patterns** - Document how containers interact
6. **Scaling characteristics** - Note replicas, stateful vs stateless
7. **Dependencies** - Capture required infrastructure containers

## Common Pitfalls

1. **Confusing container with system** - Container is ONE deployable unit within a system
2. **Too granular** - Don't break down below deployment boundary
3. **Missing infrastructure** - Don't forget databases, caches, brokers
4. **Generic types** - Be specific (FastAPI API, not "Python app")
5. **Ignoring deployment** - Runtime and deployment model matter
