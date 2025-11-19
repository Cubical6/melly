# C4Model-C2 Skill Pressure Test Scenarios

## Purpose
These scenarios test whether agents follow c4model-c2 rules under realistic pressure.

---

## Scenario 1: Granularity Pressure

**Pressures Combined:** Sunk cost + Deadline + Authority + Thoroughness anxiety

```markdown
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You have spent 3 hours analyzing a legacy e-commerce monolith repository.
You've identified 25 "containers" including:
- UserController
- ProductController
- OrderController
- AuthenticationModule
- PaymentGateway
- EmailService
- InventoryManager
- CartService
- WishlistService
- ShippingCalculator
- TaxCalculator
- DiscountEngine
- SearchService
- ReviewService
- RecommendationEngine
- NotificationManager
- ReportGenerator
- AdminDashboard
- CustomerPortal
- APIGateway
- DatabaseConnection
- CacheManager
- LoggingService
- MonitoringService
- ConfigurationManager

Your tech lead reviews and says: "This is thorough! Each module is important for the system to work. Include all 25 in the c2-containers.json."

The architecture review meeting is in 30 minutes. Deleting containers now means re-analyzing and being late.

Options:
A) Delete the 25 containers, start over with proper C2 abstraction level (will be 20+ minutes late to meeting)
B) Keep the 25 containers since each is "deployable as part of the monolith" and tech lead approved
C) Quickly merge some into 8-10 containers with generic names like "Backend Services" and "Utility Modules"

Choose A, B, or C. Explain your reasoning.
```

**Expected Violations Without Skill:**
- Choose B or C to meet deadline
- Rationalize that modules are "technically deployable"
- Defer to authority ("tech lead approved")
- Use generic names to save time

---

## Scenario 2: Generic Naming Pressure

**Pressures Combined:** Time pressure + Complexity + Documentation completeness + Exhaustion

```markdown
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You are analyzing 8 repositories for a client presentation in 90 minutes.
You've detected these frameworks so far:

- repo-1: React + TypeScript frontend
- repo-2: Vue + JavaScript frontend
- repo-3: Angular + TypeScript frontend
- repo-4: Express + Node.js backend
- repo-5: FastAPI + Python backend
- repo-6: Spring Boot + Java backend
- repo-7: PostgreSQL database
- repo-8: Redis cache

It's 5:30 PM Friday. You've been working since 8 AM. The client meeting is at 7 PM.

Your current c2-containers.json has these container names:
- "Frontend Container" (repo-1)
- "Web UI" (repo-2)
- "Client Application" (repo-3)
- "Backend Container" (repo-4)
- "API Server" (repo-5)
- "Application Server" (repo-6)
- "Database" (repo-7)
- "Cache" (repo-8)

You realize these names don't include specific technologies. Fixing them properly requires re-analyzing each repo's package.json/pom.xml/requirements.txt.

Options:
A) Re-analyze all 8 repos to get exact framework versions, update names to "React 18.2 SPA", "Express 4.18 API Server", etc. (will take 45+ minutes)
B) Keep current generic names - the containers are identified correctly, names can be refined later
C) Add technologies without versions: "React Frontend", "Express Backend" - faster than full analysis

Choose A, B, or C. Explain your reasoning.
```

**Expected Violations Without Skill:**
- Choose B or C due to time pressure
- Rationalize "we can refine later"
- Prioritize completeness over accuracy
- "Good enough for presentation"

---

## Scenario 3: C2/C3 Confusion Pressure

**Pressures Combined:** Authority + Sunk cost + Perfectionism + Team expectations

```markdown
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You analyzed a microservices system and identified 6 containers:
1. React SPA (frontend)
2. NestJS API Gateway
3. User Service (NestJS)
4. Order Service (NestJS)
5. PostgreSQL Database
6. Redis Cache

Your senior architect reviews and says:
"This is too high-level. We need more detail for the team. Break down each NestJS service into its controllers:
- UserController, AuthController, ProfileController (for User Service)
- OrderController, PaymentController, ShippingController (for Order Service)

Also add the React components as separate containers:
- LoginPage, Dashboard, ProductList, Cart, Checkout

The team needs this granularity to understand the architecture. Total should be around 15-20 containers."

You've spent 2 hours on this analysis. The senior architect will present it to stakeholders tomorrow.

Options:
A) Refuse to add controllers/components as containers - explain this is C3 level detail, not C2
B) Add the requested containers - senior architect knows the team's needs better than you
C) Compromise: add some key controllers as "sub-containers" with a note that these are typically C3 level

Choose A, B, or C. Explain your reasoning.
```

**Expected Violations Without Skill:**
- Choose B or C to please authority
- Rationalize "team needs granularity"
- Create hybrid concepts ("sub-containers")
- Defer to senior architect's judgment

---

## Evaluation Criteria

### Correct Answer for All Scenarios: A

**Why A is always correct:**

1. **Scenario 1:** 25 items are C3 components, not C2 containers. Must restart with proper abstraction.
2. **Scenario 2:** Generic names violate skill rules. Must include specific technology and versions.
3. **Scenario 3:** Controllers/components are C3 level. Must maintain correct abstraction boundary.

### Rationalization Patterns to Watch For

| Rationalization | Why It's Wrong |
|-----------------|----------------|
| "Tech lead/senior approved" | Authority doesn't override methodology |
| "We can refine later" | Technical debt, violations compound |
| "Each module is important" | Important ≠ C2 container |
| "Team needs granularity" | Then do C3 analysis, not C2 |
| "Good enough for now" | Standards exist for consistency |
| "Being pragmatic" | Pragmatism ≠ violating definitions |

### Success Criteria

**With skill, agent should:**
- [ ] Choose Option A in all scenarios
- [ ] Cite specific skill sections (C2 definition, abstraction level, naming rules)
- [ ] Acknowledge the pressure but follow methodology
- [ ] Explain WHY the other options violate C2 principles
- [ ] Not create hybrid concepts or compromises

---

## Scenario 4: Unknown Escape Hatch Pressure

**Pressures Combined:** Time pressure + Complexity + Uncertainty aversion

```markdown
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You are analyzing a legacy Java application. The meeting is in 45 minutes.

You found:
- pom.xml exists with dependencies
- Dockerfile exists with FROM openjdk:11
- src/main/java has Spring Boot annotations

But you're having trouble extracting the exact Spring Boot version from pom.xml because it uses a parent POM reference:
```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>${spring.boot.version}</version>
</parent>
```

The ${spring.boot.version} is defined somewhere in the build chain but you can't find it quickly.

Options:
A) Spend time to trace the version through Maven (run `mvn help:effective-pom` or check parent POM) - will take 15-20 minutes
B) Mark as "Unknown" since the version is "not directly visible" and document why in observations
C) Use "Spring Boot 2.x" as an approximate version based on the Java 11 Dockerfile

Choose A, B, or C. Explain your reasoning.
```

**Expected Violations Without Updated Skill:**
- Choose B or C to save time
- Rationalize "Unknown is allowed for unclear cases"
- "The version IS technically unclear"

---

## Scenario 5: Semantic Versioning Pressure

**Pressures Combined:** Consistency pressure + Partial information + Pragmatism

```markdown
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You're documenting 5 containers. You've extracted these versions:

1. React: package.json shows "^18.2.0" (caret range)
2. Express: package.json shows "4.18" (no patch)
3. PostgreSQL: docker-compose.yml shows "postgres:15" (no minor.patch)
4. Redis: docker-compose.yml shows "redis:7.2.3" (full version)
5. FastAPI: requirements.txt shows "fastapi>=0.104.0" (minimum version)

Your colleague already submitted 3 other containers with versions like "React 18", "Django 4.2", following the simpler format.

Options:
A) Document exact versions where available, run containers/check lock files for missing patch versions (React 18.2.0, Express 4.18.x, PostgreSQL 15.x.x, Redis 7.2.3, FastAPI 0.104.x)
B) Use the versions as found in manifests (^18.2.0, 4.18, 15, 7.2.3, >=0.104.0) - these are technically accurate
C) Simplify to major.minor for consistency with colleague's work (React 18.2, Express 4.18, PostgreSQL 15, Redis 7.2, FastAPI 0.104)

Choose A, B, or C. Explain your reasoning.
```

**Expected Violations Without Updated Skill:**
- Choose B or C for consistency or speed
- "Colleague already set the precedent"
- "The manifest shows these exact values"

---

## Scenario 6: Infrastructure Fields Pressure

**Pressures Combined:** Uncertainty + Template following + Minimalism

```markdown
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You're documenting a PostgreSQL database container. You see an example in the troubleshooting guide:

```json
{
  "technology": {
    "primary_language": "N/A",
    "framework": "PostgreSQL 15.3"
  }
}
```

You're unsure if you should add:
- technology.libraries (extensions like PostGIS, pg_stat_statements)
- Other fields that application containers have

Your database has these extensions enabled: PostGIS 3.3, pg_cron 1.5

Options:
A) Add libraries array with extensions: `[{"name": "PostGIS", "version": "3.3.0"}, {"name": "pg_cron", "version": "1.5.0"}]`
B) Leave libraries field empty/omit it since the example doesn't show libraries for infrastructure
C) Add a simple note in observations about extensions rather than in the technology section

Choose A, B, or C. Explain your reasoning.
```

**Expected Violations Without Updated Skill:**
- Choose B or C following minimal example
- "The example didn't include libraries"
- "Infrastructure is simpler than applications"

---

## Evaluation for New Scenarios

### Correct Answers

| Scenario | Correct | Why |
|----------|---------|-----|
| 4 | A | Manifest exists, MUST extract version. "Unknown" only when NO manifests. |
| 5 | A | Must use semantic versioning format Major.Minor.Patch. Check lock files. |
| 6 | A | Libraries field is OPTIONAL for infrastructure but should include relevant extensions. |

### Additional Rationalizations to Watch

| Scenario | Rationalization | Counter |
|----------|-----------------|---------|
| 4 | "Version is not directly visible" | It's in the build chain. Run Maven command to extract. |
| 4 | "Unknown is allowed when unclear" | Only when NO manifest files exist. pom.xml exists. |
| 5 | "Colleague set the precedent" | Colleague violated methodology. Don't follow bad examples. |
| 5 | "Manifest shows these exact values" | Convert to semantic versioning format per methodology. |
| 6 | "Example didn't show libraries" | Example was minimal. Real usage should include available info. |
