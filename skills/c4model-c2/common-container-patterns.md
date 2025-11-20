# Common Container Patterns

This document provides reusable architecture patterns for C4 Model Level 2 (Container) analysis with detailed examples.

## Pattern 1: Simple SPA + API + Database

**Scenario:** Basic web application with frontend, backend, and database

**Containers identified:**

1. **Frontend SPA Container**
   - Type: `spa`
   - Technology: React 18 + TypeScript
   - Runtime: Browser
   - Communicates with API via HTTP REST

2. **Backend API Container**
   - Type: `api`
   - Technology: Express.js + Node.js 18
   - Runtime: Server (Node.js)
   - Communicates with database via PostgreSQL protocol

3. **PostgreSQL Database Container**
   - Type: `database`
   - Technology: PostgreSQL 15
   - Runtime: Server (Docker)
   - Stores application data

**Architecture:**
```
┌──────────────────┐
│  Browser         │
│  ┌────────────┐  │
│  │ React SPA  │  │
│  └──────┬─────┘  │
└─────────┼────────┘
          │ HTTP REST
          ▼
┌─────────────────┐
│  Server         │
│  ┌────────────┐ │
│  │ Express API│ │
│  └──────┬─────┘ │
└─────────┼───────┘
          │ SQL
          ▼
┌─────────────────┐
│  ┌────────────┐ │
│  │PostgreSQL  │ │
│  │ Database   │ │
│  └────────────┘ │
└─────────────────┘
```

**Detection Commands:**
```bash
# Detect pattern
find . -name "package.json" | grep -E "(frontend|client|web)"
find . -name "package.json" | grep -E "(backend|server|api)"
find . -name "docker-compose.yml" | xargs grep postgres

# Verify frontend
cat frontend/package.json | jq '.dependencies | keys | .[]' | grep -E "react|vue|angular"

# Verify backend
cat backend/package.json | jq '.dependencies | keys | .[]' | grep -E "express|fastify|nestjs"

# Verify database
docker-compose config | grep postgres
```

---

## Pattern 2: Microservices with API Gateway

**Scenario:** Multiple microservices behind API gateway

**Containers identified:**

1. **API Gateway Container**
   - Type: `web-server`
   - Technology: Nginx or Kong
   - Runtime: Server
   - Routes requests to services

2. **Auth Service Container**
   - Type: `api`
   - Technology: NestJS
   - Runtime: Server (Node.js in Docker)
   - Handles authentication

3. **User Service Container**
   - Type: `api`
   - Technology: Spring Boot
   - Runtime: Server (JVM in Docker)
   - Manages user data

4. **Order Service Container**
   - Type: `api`
   - Technology: FastAPI
   - Runtime: Server (Python in Docker)
   - Processes orders

5. **Message Broker Container**
   - Type: `message-broker`
   - Technology: RabbitMQ
   - Runtime: Server (Docker)
   - Event bus

6. **Per-Service Databases**
   - Each service has its own database container

**Architecture:**
```
┌──────────────┐
│ API Gateway  │
└──────┬───────┘
       │ HTTP
   ┌───┴────┬────────┐
   │        │        │
   ▼        ▼        ▼
┌─────┐ ┌──────┐ ┌───────┐
│Auth │ │User  │ │Order  │
│Svc  │ │Svc   │ │Svc    │
└──┬──┘ └──┬───┘ └───┬───┘
   │       │         │
   └───────┴────┬────┘
               │
               ▼
         ┌─────────┐
         │RabbitMQ │
         └─────────┘
```

**Detection Commands:**
```bash
# Detect microservices pattern
find . -type d -name "*-service" -o -name "*-api"
ls services/ | wc -l  # Count service directories

# Find API gateway
grep -r "nginx\|kong\|traefik" docker-compose.yml k8s/

# Find message broker
grep -r "rabbitmq\|kafka" docker-compose.yml k8s/

# Count services
find services/ -name "package.json" -o -name "pom.xml" -o -name "requirements.txt" | wc -l
```

---

## Pattern 3: Serverless Architecture

**Scenario:** Serverless functions with managed services

**Containers identified:**

1. **Frontend SPA Container**
   - Type: `spa`
   - Deployed to: CloudFront + S3
   - Technology: React
   - Runtime: Browser

2. **API Lambda Functions Container(s)**
   - Type: `api`
   - Multiple functions or single function
   - Technology: Node.js Lambda handlers
   - Runtime: AWS Lambda (serverless)

3. **DynamoDB Database**
   - Type: `database`
   - Technology: AWS DynamoDB
   - Runtime: AWS managed
   - Fully serverless

4. **S3 Storage Container**
   - Type: `file-storage`
   - Technology: AWS S3
   - Runtime: AWS managed
   - Stores uploaded files

**Architecture:**
```
┌─────────────┐
│ CloudFront  │
│ + S3        │
│ (SPA)       │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│ API Gateway │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────┐
│ Lambda      │──────▶ DynamoDB │
│ Functions   │      └──────────┘
└─────────────┘
       │
       ▼
┌─────────────┐
│ S3 Bucket   │
└─────────────┘
```

**Detection Commands:**
```bash
# Detect serverless pattern
find . -name "serverless.yml" -o -name "serverless.yaml"
find . -name "vercel.json" -o -name "netlify.toml"
find . -name "template.yaml" | xargs grep "AWS::Serverless"

# Find Lambda functions
grep -r "AWS::Serverless::Function\|handler:" serverless.yml

# Find DynamoDB tables
grep -r "DynamoDB\|AWS::DynamoDB" template.yaml

# Find S3 usage
grep -r "S3_BUCKET\|aws-sdk.*s3" .
```

---

## Pattern 4: Full-Stack Framework (Next.js/Nuxt)

**Scenario:** Single full-stack application with SSR

**Containers identified:**

1. **Next.js Application Container**
   - Type: `app-server` (full-stack)
   - Technology: Next.js 13
   - Runtime: Server (Node.js)
   - Serves both frontend and API routes
   - **Note:** This is ONE container, not separate frontend/backend

2. **Database Container**
   - Type: `database`
   - Technology: PostgreSQL
   - Runtime: Server (Docker)

3. **Redis Cache Container**
   - Type: `cache`
   - Technology: Redis
   - Runtime: Server (Docker)
   - Caches SSR pages

**Architecture:**
```
┌────────────────────┐
│  Next.js App       │
│  ┌──────────────┐  │
│  │ SSR + API    │  │
│  │ Routes       │  │
│  └──────┬───────┘  │
└─────────┼──────────┘
        ┌─┴──┐
        │    │
    ┌───▼──┐ └──▼─────┐
    │ DB   │  │ Redis │
    └──────┘  └───────┘
```

**Detection Commands:**
```bash
# Detect Next.js/Nuxt pattern
grep -r "\"next\":\|\"nuxt\":" package.json

# Check for API routes
find . -type d -name "api" -path "*/pages/api" -o -path "*/app/api"

# Check for SSR
grep -r "getServerSideProps\|getStaticProps" pages/ app/

# Verify single application
[ $(find . -name "package.json" -not -path "*/node_modules/*" | wc -l) -eq 1 ] && echo "Single app"
```

---

## Pattern 5: Mobile App + Backend

**Scenario:** Mobile application with supporting backend

**Containers identified:**

1. **Mobile Application Container**
   - Type: `mobile-app`
   - Technology: React Native
   - Runtime: iOS/Android
   - Communicates with API

2. **Backend API Container**
   - Type: `api`
   - Technology: Django REST Framework
   - Runtime: Server (Python)
   - Provides mobile API

3. **PostgreSQL Database Container**
   - Type: `database`
   - Technology: PostgreSQL
   - Runtime: Server

4. **Redis Cache Container**
   - Type: `cache`
   - Technology: Redis
   - Runtime: Server
   - API response caching

5. **Push Notification Service Container**
   - Type: `worker`
   - Technology: Custom Python service
   - Runtime: Server
   - Sends push notifications via FCM/APNS

**Architecture:**
```
┌─────────────────┐
│ Mobile Device   │
│ ┌─────────────┐ │
│ │React Native │ │
│ │    App      │ │
│ └──────┬──────┘ │
└────────┼────────┘
         │ HTTPS
         ▼
┌────────────────┐      ┌────────┐
│ Django API     │──────▶ Postgres│
└────────┬───────┘      └────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────┐  ┌────────┐
│Redis │  │Push    │
│Cache │  │Service │
└──────┘  └────────┘
```

**Detection Commands:**
```bash
# Detect mobile app
find . -name "package.json" | xargs grep "react-native\|@ionic\|flutter"
find . -name "Podfile" -o -name "build.gradle"

# Detect backend API
grep -r "djangorestframework\|flask\|fastapi" requirements.txt

# Find push notification service
grep -r "fcm\|apns\|firebase-admin" . | grep -v node_modules
```

---

## Pattern 6: Event-Driven with Workers

**Scenario:** Async processing with message queue and workers

**Containers identified:**

1. **Web Application Container**
   - Type: `spa`
   - Technology: Vue 3
   - Runtime: Browser

2. **Backend API Container**
   - Type: `api`
   - Technology: FastAPI
   - Runtime: Server (Python)
   - Publishes events to queue

3. **Message Queue Container**
   - Type: `message-broker`
   - Technology: Kafka
   - Runtime: Server (Docker)
   - Event streaming

4. **Email Worker Container**
   - Type: `worker`
   - Technology: Celery
   - Runtime: Server (Python)
   - Consumes email events

5. **Report Worker Container**
   - Type: `worker`
   - Technology: Celery
   - Runtime: Server (Python)
   - Generates reports

6. **Database Container**
   - Type: `database`
   - Technology: PostgreSQL
   - Runtime: Server

**Architecture:**
```
┌──────┐    ┌─────┐
│ Vue  │───▶│ API │
│ SPA  │    └──┬──┘
└──────┘       │
               │ publish
               ▼
         ┌──────────┐
         │  Kafka   │
         │  Queue   │
         └─────┬────┘
           ┌───┴───┐
      subscribe  subscribe
           │       │
      ┌────▼──┐ ┌─▼──────┐
      │Email  │ │Report  │
      │Worker │ │Worker  │
      └───────┘ └────────┘
```

**Detection Commands:**
```bash
# Detect event-driven pattern
grep -r "celery\|sidekiq\|bull\|bee-queue" requirements.txt package.json Gemfile

# Find message brokers
grep -r "kafka\|rabbitmq\|redis.*pub.*sub" docker-compose.yml

# Find worker definitions
find . -name "*worker*.py" -o -name "*job*.py"
grep -r "celery.*worker\|worker.*start" .
```

---

## Pattern Selection Guide

### When to Use Each Pattern

| Pattern | Best For | Complexity | Scalability |
|---------|----------|------------|-------------|
| Pattern 1: SPA + API + DB | Simple web apps, MVPs | Low | Medium |
| Pattern 2: Microservices | Large systems, independent teams | High | Very High |
| Pattern 3: Serverless | Variable load, cost optimization | Medium | Auto-scale |
| Pattern 4: Full-Stack Framework | Rapid development, SSR needs | Low-Medium | Medium |
| Pattern 5: Mobile + Backend | Mobile-first apps | Medium | High |
| Pattern 6: Event-Driven | Async processing, decoupling | Medium-High | Very High |

### Mixing Patterns

Real-world systems often combine patterns:

**Example: E-commerce Platform**
- Pattern 1: Customer web portal (SPA + API + DB)
- Pattern 5: Mobile shopping app (Mobile + Backend)
- Pattern 6: Order processing (Event-driven workers)
- Pattern 3: Static assets (Serverless CDN)

---

## Detection Best Practices

1. **Start with docker-compose.yml or K8s manifests** - Shows all containers
2. **Check package manifests** - package.json, requirements.txt, pom.xml
3. **Look for framework indicators** - next.config.js, serverless.yml
4. **Examine folder structure** - services/, apps/, packages/
5. **Review deployment configs** - Dockerfile, K8s deployments
6. **Check environment variables** - .env files reveal connections

## Common Variations

### Pattern 1 Variations
- Add Redis cache → Pattern 1 + Cache
- Add Nginx proxy → Pattern 1 + Reverse Proxy
- Add worker → Pattern 1 + Background Jobs

### Pattern 2 Variations
- Per-service databases → Database-per-Service
- Shared database → Shared-Database (anti-pattern)
- Service mesh → Add Istio/Linkerd sidecar containers

### Pattern 3 Variations
- Vercel deployment → Vercel Edge Functions
- Netlify deployment → Netlify Functions
- Azure → Azure Functions + Cosmos DB

### Pattern 4 Variations
- Monorepo → Multiple Next.js apps
- Standalone API → Next.js + Separate API
- Edge runtime → Vercel Edge Runtime

---

## Anti-Patterns to Avoid

1. **Shared Database Across Services**
   - Violates microservices principles
   - Creates tight coupling
   - Makes each service dependent

2. **Monolith in Disguise**
   - Multiple "microservices" that all call each other synchronously
   - Should be one container

3. **Over-Granular Containers**
   - Breaking down below deployment boundary
   - Example: Separating utility functions into "containers"

4. **Missing Infrastructure Containers**
   - Forgetting databases, caches, message brokers
   - Only documenting application containers

5. **Generic Container Types**
   - "Node.js App" instead of "Express API Server"
   - "Python Service" instead of "FastAPI API + Celery Worker"

---

## Next Steps

After identifying the pattern:

1. **Document each container** using container-types-reference.md
2. **Map communication** using communication-patterns.md
3. **Capture technology details** using technology-detection-patterns.md
4. **Add observations** per observation-categories-c2.md
5. **Validate** using melly-validation scripts
