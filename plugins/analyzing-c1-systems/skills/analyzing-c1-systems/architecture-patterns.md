# Common Architecture Patterns

## Pattern 1: Simple Web Application

**Scenario:** Small web app with frontend and backend

**Systems identified:**
1. **Web Frontend** (web-application)
   - User-facing SPA
   - Repository: `/frontend/`

2. **Backend API** (api-service)
   - REST API
   - Repository: `/backend/`

3. **PostgreSQL Database** (database)
   - Data persistence
   - External infrastructure

**Actors:**
- End User (uses Web Frontend)

**Relationships:**
- Web Frontend → Backend API (http-rest)
- Backend API → PostgreSQL Database (database-query)

**Typical indicators:**
- Two repositories: frontend/ and backend/
- package.json with react/vue/angular in frontend
- package.json with express/fastify in backend
- Database connection string in .env

---

## Pattern 2: Microservices Architecture

**Scenario:** Multiple services with API gateway

**Systems identified:**
1. **API Gateway** (api-service)
   - Request routing
   - Repository: `/gateway/`

2. **Auth Service** (api-service)
   - Authentication
   - Repository: `/auth-service/`

3. **User Service** (api-service)
   - User management
   - Repository: `/user-service/`

4. **Order Service** (api-service)
   - Order processing
   - Repository: `/order-service/`

5. **Message Queue** (message-broker)
   - Event bus
   - External (RabbitMQ/Kafka)

**Actors:**
- Mobile App (external system actor)
- Administrator (user actor)

**Relationships:**
- API Gateway → Auth Service (grpc)
- API Gateway → User Service (grpc)
- API Gateway → Order Service (grpc)
- Order Service → Message Queue (message-queue)

**Typical indicators:**
- Multiple service repositories (auth-service/, user-service/, etc.)
- API gateway with routing configuration
- gRPC or REST between services
- Message queue dependency (rabbitmq, kafka)
- Service discovery (consul, etcd)

---

## Pattern 3: Event-Driven System

**Scenario:** Async processing with message queue

**Systems identified:**
1. **Web Application** (web-application)
   - User interface
   - Repository: `/webapp/`

2. **Backend API** (api-service)
   - API layer
   - Repository: `/api/`

3. **Message Queue** (message-broker)
   - Event streaming
   - External (Kafka)

4. **Worker Service** (internal-service)
   - Background processing
   - Repository: `/worker/`

5. **Notification Service** (internal-service)
   - Email/SMS sending
   - Repository: `/notifications/`

**External Actors:**
- SendGrid (email delivery)
- Twilio (SMS delivery)

**Relationships:**
- Web Application → Backend API (http-rest)
- Backend API → Message Queue (message-queue, publish)
- Worker Service → Message Queue (message-queue, subscribe)
- Notification Service → Message Queue (message-queue, subscribe)
- Notification Service → SendGrid (http-rest)
- Notification Service → Twilio (http-rest)

**Typical indicators:**
- Message queue dependency (kafka, rabbitmq, redis)
- Worker/consumer services subscribe to topics
- Async/background processing
- Event publishing in API code
- Email/SMS service integrations

---

## Pattern 4: Mobile + Backend

**Scenario:** Mobile app with backend API

**Systems identified:**
1. **Mobile Application** (mobile-application)
   - iOS/Android app
   - Repository: `/mobile-app/`

2. **Backend API** (api-service)
   - REST API
   - Repository: `/backend/`

3. **PostgreSQL Database** (database)
   - Data store
   - External infrastructure

4. **Redis Cache** (cache)
   - Session/data cache
   - External infrastructure

5. **Auth0** (external-service)
   - Authentication provider
   - External SaaS

**Actors:**
- Mobile User (user actor)
- Auth0 (external system actor)

**Relationships:**
- Mobile Application → Backend API (http-rest)
- Mobile Application → Auth0 (authentication, OAuth)
- Backend API → PostgreSQL Database (database-query)
- Backend API → Redis Cache (database-query)
- Backend API → Auth0 (authentication, token validation)

**Typical indicators:**
- React Native, Flutter, or native mobile code
- Backend API with mobile-specific endpoints
- OAuth/Auth0 integration
- Push notification service
- Redis for session/token caching
- Mobile-specific features (geolocation, camera, etc.)

---

## How to Identify Architecture Pattern

### Ask These Questions:

1. **How many repositories?**
   - 1-2 repos → Simple Web App or Mobile + Backend
   - 3-5 repos → Event-Driven System
   - 5+ repos → Microservices Architecture

2. **Is there an API gateway?**
   - Yes → Likely Microservices
   - No → Likely Simple Web App or Event-Driven

3. **Is there a message queue?**
   - Yes → Event-Driven System or Microservices
   - No → Simple Web App or Mobile + Backend

4. **Is there a mobile app?**
   - Yes → Mobile + Backend pattern
   - No → Other patterns

5. **How many services?**
   - 1-2 services → Simple Web App
   - 3-4 services → Event-Driven
   - 5+ services → Microservices

### Pattern Decision Tree

```
Start
  ↓
Mobile app exists?
  ├─ Yes → Pattern 4: Mobile + Backend
  └─ No  → Continue
      ↓
Message queue exists?
  ├─ Yes → Pattern 3: Event-Driven
  └─ No  → Continue
      ↓
API Gateway exists?
  ├─ Yes → Pattern 2: Microservices
  └─ No  → Pattern 1: Simple Web App
```

## Pattern-Specific Observations

### Simple Web Application

**Common observations:**
- Monolithic architecture
- Direct database access from API
- Session-based or JWT authentication
- Single deployment unit per tier (frontend, backend)

### Microservices Architecture

**Common observations:**
- Service-oriented architecture
- Service discovery and registration
- API gateway as single entry point
- Inter-service communication (gRPC, REST)
- Distributed data management

### Event-Driven System

**Common observations:**
- Asynchronous message passing
- Loose coupling between services
- Event sourcing or CQRS patterns
- Eventually consistent data
- Background job processing

### Mobile + Backend

**Common observations:**
- Mobile-first API design
- OAuth/token-based authentication
- Push notification support
- Offline-first considerations
- API versioning for mobile clients
