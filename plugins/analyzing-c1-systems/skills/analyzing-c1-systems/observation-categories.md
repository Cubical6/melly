# Observation Guidelines for C1 Level

## Observation Categories

When documenting systems, capture these observation categories:

### 1. architecture

System-level architectural patterns and decisions.

**Examples:**
- "Microservices architecture with API gateway"
- "Monolithic architecture with single database"
- "Event-driven architecture using message queue"
- "Serverless architecture on AWS Lambda"

### 2. integration

External system integrations and communication patterns.

**Examples:**
- "Integrates with Stripe for payment processing"
- "Uses SendGrid for email notifications"
- "Connects to Auth0 for authentication"
- "Publishes events to Kafka message broker"

### 3. boundaries

System boundary definitions and scope.

**Examples:**
- "Public-facing web application accessible from internet"
- "Internal admin panel restricted to VPN access"
- "API gateway serves as single entry point for all services"
- "Database isolated in private subnet with no internet access"

### 4. security

Security posture, authentication, and authorization.

**Examples:**
- "JWT-based authentication with 1-hour token expiry"
- "OAuth 2.0 integration with Auth0"
- "API keys stored in environment variables"
- "HTTPS enforced for all communications"
- "No CSRF protection implemented" (warning)

### 5. scalability

Scalability patterns and constraints.

**Examples:**
- "Horizontally scalable API with load balancer"
- "CDN used for static asset delivery"
- "Database read replicas for scaling reads"
- "Stateless API design enables easy scaling"

### 6. actors

User types and external actors.

**Examples:**
- "Three primary user roles: customer, admin, support"
- "Anonymous users can browse products without login"
- "External payment provider (Stripe) integrated"
- "Third-party analytics service (Google Analytics) tracking users"

### 7. deployment

Deployment patterns, hosting, and infrastructure.

**Examples:**
- "Deployed on AWS using ECS containers"
- "Hosted on Vercel with automatic deployments"
- "On-premise deployment in company data center"
- "Serverless deployment using AWS Lambda"

### 8. technology-stack

Technologies, frameworks, and libraries used.

**Examples:**
- "React 18 with TypeScript for type safety"
- "Node.js runtime with Express framework"
- "PostgreSQL database with Prisma ORM"
- "Redis cache for session storage"

## Observation Structure

```json
{
  "id": "obs-arch-microservices",
  "title": "Microservices architecture with API gateway",
  "category": "architecture",
  "severity": "info",
  "description": "System follows microservices architecture with multiple independent services coordinated through an API gateway that handles routing, authentication, and rate limiting",
  "evidence": [
    {
      "type": "pattern",
      "location": "infrastructure/",
      "snippet": "Multiple service directories: auth-service/, user-service/, order-service/"
    }
  ],
  "tags": ["microservices", "api-gateway", "distributed"]
}
```

## Observation Severity Levels

- **info** - Informational observation (neutral)
- **warning** - Potential issue requiring attention
- **critical** - Critical issue requiring immediate action

**Examples:**
- ℹ️ **info**: "Uses React 18 for frontend development"
- ⚠️ **warning**: "No rate limiting on API endpoints"
- 🔴 **critical**: "API keys hardcoded in source code"

## Best Practices for Observations

### DO:

1. **Provide evidence** - Include code snippets, file paths, or configuration examples
2. **Be specific** - "JWT auth with 1-hour expiry" not "uses JWT"
3. **Tag appropriately** - Use lowercase kebab-case tags
4. **Set correct severity** - Critical for security issues, info for informational
5. **Link observations** - Reference related systems or actors

### DON'T:

1. **Don't be vague** - "Uses authentication" → "JWT-based auth with Auth0"
2. **Don't skip evidence** - Always include proof
3. **Don't mix categories** - One observation = one category
4. **Don't ignore warnings** - Document potential issues
5. **Don't duplicate** - Similar observations should be combined

## Observation Discovery Commands

**Find architectural patterns:**
```bash
ls -la  # Check directory structure
grep -r "microservice\|monolith\|serverless" .
```

**Find integrations:**
```bash
cat .env.example | grep -E "API_KEY|WEBHOOK"
grep -r "stripe\|sendgrid\|twilio" package.json
```

**Find security configurations:**
```bash
grep -r "jwt\|JWT\|oauth\|OAuth" src/
grep -r "bcrypt\|crypto\|hash" src/
cat .env.example | grep -E "SECRET|KEY|TOKEN"
```

**Find scalability indicators:**
```bash
grep -r "load.?balanc\|cluster\|replica" .
grep -r "cache\|Cache\|redis\|Redis" .
```

**Find deployment info:**
```bash
cat Dockerfile package.json docker-compose.yml
ls -la .github/workflows/ .gitlab-ci.yml
grep -r "aws\|AWS\|azure\|gcp" .
```
