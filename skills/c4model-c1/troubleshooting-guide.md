# Troubleshooting Guide for C1 Analysis

## Problem: Too Many Systems Identified

**Symptom:** 10+ systems for a small application

**Root cause:** Over-granularization - treating components as systems

**Solution:** Combine systems that share:
- Same deployment unit
- Same repository
- Same business capability

**Examples:**
- Login + Registration + Profile → **User Management System**
- Product List + Product Detail + Product Search → **Product Catalog System**
- Multiple APIs doing similar things → **One API System** with multiple containers (C2)

**Questions to ask:**
- Can these be deployed independently?
- Do they have separate repositories?
- Do they solve different business problems?

If "no" to all three → combine into one system.

---

## Problem: Can't Determine System Boundaries

**Symptom:** Unclear where one system ends and another begins

**Root cause:** Mixed abstraction levels or unclear responsibilities

**Solution:** Ask the following questions in order:

1. **Can this be deployed independently?**
   - Yes → Likely separate systems
   - No → Likely one system

2. **Does it have a clear single purpose?**
   - Yes → Good system candidate
   - No → May need to split or combine

3. **Is it in a separate repository?**
   - Yes → Usually separate system
   - No → May be same system (unless monorepo)

4. **Does it have its own runtime?**
   - Yes → Separate system
   - No → Probably same system

**If still unclear:** Default to fewer systems. You can always split at C2 (Container) level.

**Example:**
```
Unclear: "Authentication" separate from "User Management"?

Ask:
- Independent deployment? No (both part of same API)
- Separate repos? No
- Own runtime? No

→ Combine into "User Management System"
```

---

## Problem: Technology Names in System IDs

**Symptom:** System IDs like `react-frontend`, `express-backend`, `django-app`

**Root cause:** Focusing on implementation instead of purpose

**Solution:** Rename to business purpose:

| ❌ Technology Name | ✅ Business Purpose |
|-------------------|---------------------|
| react-frontend | customer-web-app |
| express-backend | ecommerce-api |
| django-app | content-management-system |
| postgres-db | user-database |
| redis-cache | session-cache |

**Pattern:** Ask "What does this do for the business?" not "What tech is it built with?"

**Good naming formula:**
```
[Business Capability] + [System Type]

Examples:
- Order Processing + API = order-processing-api
- Customer Portal + Web App = customer-portal
- Product Catalog + Service = product-catalog-service
```

---

## Problem: Missing External Actors

**Symptom:** No `external-service` type systems, no external actors

**Root cause:** Not checking for third-party integrations

**Solution:** Systematically check for external services:

### 1. Check .env.example

```bash
cat .env.example | grep -E "API_KEY|API_URL|WEBHOOK|SECRET"
```

Look for:
- `STRIPE_API_KEY` → Stripe payment gateway
- `SENDGRID_API_KEY` → SendGrid email service
- `TWILIO_*` → Twilio SMS service
- `AUTH0_*` → Auth0 authentication
- `GOOGLE_ANALYTICS_ID` → Google Analytics

### 2. Check package.json dependencies

```bash
cat package.json | grep -E "stripe|sendgrid|twilio|auth0|analytics"
```

Look for SDK packages:
- `stripe` → Stripe integration
- `@sendgrid/mail` → SendGrid integration
- `twilio` → Twilio integration
- `@auth0/*` → Auth0 integration

### 3. Search code for API calls

```bash
grep -r "https://api\." src/
grep -r "external.*api\|third.?party" src/
```

### 4. Common external services:

**Almost every app uses:**
- Payment provider (Stripe, PayPal)
- Email service (SendGrid, Mailgun)
- Authentication (Auth0, Firebase)
- Analytics (Google Analytics, Mixpanel)
- Monitoring (Datadog, Sentry)
- Cloud storage (S3, GCS)

---

## Problem: Relations Without Direction

**Symptom:** All relationships marked "bidirectional"

**Root cause:** Not analyzing who initiates communication

**Solution:** Think about who calls whom:

### Decision Rules:

1. **Frontend → Backend** = outbound from frontend
   - Frontend makes HTTP requests
   - Backend responds
   - Direction: outbound (from frontend perspective)

2. **API → Database** = outbound from API
   - API initiates queries
   - Database responds
   - Direction: outbound (from API perspective)

3. **Service → Message Queue** = depends on action
   - Publishing event → outbound
   - Subscribing/consuming → inbound

4. **Only bidirectional when:**
   - WebSocket connections
   - True peer-to-peer communication
   - Both systems initiate equally

### Examples:

| Relationship | Direction | Reasoning |
|--------------|-----------|-----------|
| Web App → API | outbound | Web app calls API |
| API → Database | outbound | API queries database |
| Worker → Queue | inbound | Worker consumes from queue |
| API → Queue (publish) | outbound | API publishes to queue |
| Chat Client ↔ Chat Server | bidirectional | WebSocket, both send |

**Rule of thumb:** If one system "calls" another, it's outbound from caller.

---

## Problem: Components Identified as Systems

**Symptom:** System IDs like `authentication-module`, `payment-controller`, `user-service-class`

**Root cause:** Confusing C1 (System) with C3 (Component) level

**Solution:** Recognize component indicators:

### ❌ These are C3 Components (NOT C1 Systems):

- Authentication Module
- Payment Controller
- User Service Class
- Shopping Cart Manager
- Email Helper
- Validation Utilities

### ✅ These are C1 Systems:

- User Management System (contains auth module)
- E-commerce API (contains payment controller)
- Web Application (contains shopping cart)
- Email Service (contains email helpers)

### How to tell:

| If it's... | Then it's... |
|-----------|--------------|
| Part of codebase structure | C3 Component |
| In a `/src/` directory | C3 Component |
| A class, module, or package | C3 Component |
| Independently deployable | C1 System |
| Has own repository (in microservices) | C1 System |
| Has own runtime/process | C1 System |

**When in doubt:** If you can't deploy it separately, it's not a C1 system.

---

## Problem: Validation Fails

**Symptom:** `validate-c1-systems.py` reports errors

**Common validation errors and fixes:**

### 1. Invalid ID format

```
Error: System ID 'User Management' is not kebab-case
Fix: Change to 'user-management-system'
```

### 2. Missing timestamps

```
Error: metadata.timestamp is missing
Fix: Add current ISO timestamp to metadata
```

### 3. Broken relationships

```
Error: Relation target 'api-service' does not exist
Fix: Ensure all relation targets reference existing system IDs
```

### 4. Invalid system type

```
Error: Unknown system type 'backend'
Fix: Use valid types: web-application, api-service, database, etc.
```

### 5. Timestamp ordering

```
Error: Child timestamp <= parent timestamp
Fix: Ensure c1-systems.json timestamp > init.json timestamp
```

**Debugging validation:**

```bash
# Run validation with verbose output
python validation/scripts/validate-c1-systems.py c1-systems.json -v

# Check JSON syntax
cat c1-systems.json | jq .

# Validate schema
cat c1-systems.json | jq '.metadata.schema_version'
```

---

## Quick Troubleshooting Checklist

Before finalizing C1 analysis:

- [ ] System count reasonable (3-8 systems for small app, 8-15 for medium)
- [ ] All system IDs in kebab-case
- [ ] No technology names in system IDs
- [ ] All systems have clear business purpose
- [ ] External services identified (payment, email, auth, etc.)
- [ ] Actors documented (both users and external systems)
- [ ] Relationships have direction (outbound/inbound)
- [ ] All relation targets exist
- [ ] Boundaries defined (scope, deployment, network)
- [ ] Observations documented with evidence
- [ ] Timestamps valid (child > parent)
- [ ] Validation script passes

**If checklist fails:** Review this troubleshooting guide for specific issues.
