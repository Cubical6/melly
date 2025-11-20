# Observation Guide for C3 Components

This guide provides comprehensive methodology for documenting observations at the C3 level.

---

## Observation Categories for C3

### Observation Categories

When documenting components, capture these observation categories:

#### 1. **code-structure**
Code organization patterns and file structure

**Examples:**
- "Feature-based structure with users/, orders/, products/ directories"
- "Layered architecture with controllers/, services/, repositories/ separation"
- "Domain-driven design with domain/, application/, infrastructure/ layers"
- "Monolithic structure - all code in single src/ directory"

#### 2. **design-patterns**
Design patterns identified in code

**Examples:**
- "Singleton pattern for DatabaseConnection ensures single instance"
- "Repository pattern abstracts data access across all entities"
- "Factory pattern used for creating different user types"
- "Dependency injection via NestJS @Injectable decorators"
- "Observer pattern for event-driven order processing"

#### 3. **dependencies**
Component dependencies and coupling

**Examples:**
- "UserService depends on UserRepository, EmailService, and ValidationUtil"
- "High coupling between OrderService and PaymentService (7 method calls)"
- "Circular dependency detected: UserService ↔ OrderService"
- "Controllers depend only on Services (proper layering)"

#### 4. **complexity**
Code complexity metrics

**Examples:**
- "OrderService has cyclomatic complexity of 24 (high risk)"
- "UserController is 450 LOC (consider splitting)"
- "PaymentService has 12 public methods (large interface)"
- "Average complexity across services: 8 (acceptable)"

#### 5. **coupling**
Coupling and cohesion analysis

**Examples:**
- "Tight coupling: UserService directly instantiates EmailService (no DI)"
- "Loose coupling: All dependencies injected via constructor"
- "High afferent coupling: UserModel imported by 15 components"
- "Low cohesion: UtilityService has unrelated helper methods"

#### 6. **cohesion**
Component cohesion and single responsibility

**Examples:**
- "UserService has high cohesion - all methods relate to user management"
- "UtilityService has low cohesion - contains unrelated helpers"
- "OrderController violates SRP - handles both orders and payments"
- "Each repository focused on single entity (good cohesion)"

#### 7. **testing**
Test coverage and testability

**Examples:**
- "UserService has 95% test coverage with 24 unit tests"
- "PaymentGateway untestable - uses hardcoded external URLs"
- "All services use dependency injection for easy mocking"
- "Controllers have integration tests covering main flows"

#### 8. **documentation**
Code documentation quality

**Examples:**
- "All public methods have JSDoc comments"
- "UserService missing documentation for complex methods"
- "README.md in authentication/ explains module architecture"
- "Inline comments explain business logic in PaymentService"

### Observation Structure for C3

```json
{
  "id": "obs-repo-pattern-all-entities",
  "title": "Repository pattern used for all entity data access",
  "category": "design-patterns",
  "severity": "info",
  "pattern": "repository",
  "description": "All entities (User, Order, Product, Payment) have dedicated repository classes that abstract database operations using the Repository pattern. Repositories provide methods like findById, findAll, save, delete.",
  "evidence": [
    {
      "type": "pattern",
      "location": "src/users/UserRepository.ts",
      "snippet": "export class UserRepository { async findById(id: string): Promise<User> { ... } }"
    },
    {
      "type": "pattern",
      "location": "src/orders/OrderRepository.ts",
      "snippet": "export class OrderRepository { async findById(id: string): Promise<Order> { ... } }"
    }
  ],
  "impact": {
    "maintainability": "high",
    "testability": "high",
    "scalability": "medium"
  },
  "tags": ["repository-pattern", "data-access", "abstraction"]
}
```

### Observation Severity Levels

- **info** - Informational observation (neutral)
- **warning** - Potential issue requiring attention
- **critical** - Critical issue requiring immediate action

**Examples:**
- ℹ️ **info**: "Repository pattern used for data access abstraction"
- ⚠️ **warning**: "Circular dependency between UserService and OrderService"
- 🔴 **critical**: "No input validation in UserController endpoints"
