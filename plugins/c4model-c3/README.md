# C4 Model - Level 3: Component Skill

> A comprehensive methodology skill for identifying and documenting components, analyzing code structure, and detecting design patterns at the component level of software architecture.

## Overview

The **c4model-c3** skill provides Claude Code with expert knowledge of the C4 Model's Level 3 (Component) methodology. This skill enables accurate identification, analysis, and documentation of:

- **Components** - Logical building blocks within containers with well-defined responsibilities
- **Code Structure** - File organization, exports, and module boundaries
- **Design Patterns** - Singleton, Factory, Repository, Dependency Injection, and more
- **Dependencies** - Component-to-component relationships and coupling analysis
- **Metrics** - Lines of code, complexity, test coverage, and code quality

## What is C3 Component Level?

C3 (Component) is the third level of abstraction in the C4 Model, answering the question: **"What are the logical building blocks within each container?"**

At this level, we focus on:
- Groupings of related functionality (not individual classes)
- Component responsibilities and interfaces
- Design patterns and architectural styles
- Component dependencies and coupling
- Code organization within containers

**We do NOT focus on:**
- Individual classes/functions (that's C4)
- Deployment units (that's C2)
- System boundaries (that's C1)
- Infrastructure details (that's C2)

## When to Use This Skill

This skill is automatically activated when Claude detects keywords like:
- "component identification"
- "C3 level"
- "code structure"
- "design patterns"
- "component boundaries"
- "coupling analysis"
- "cohesion analysis"
- "component responsibilities"

### Melly Workflow Integration

In the Melly workflow, this skill is used by:
- **`c3-abstractor` agent** - During component identification phase
- **`/melly-c3-components` command** - When generating `c3-components.json`
- **`c4model-writer` agent** - When documenting component architecture

## Key Concepts

### Components

A **component** is a grouping of related functionality encapsulated behind a well-defined interface, consisting of one or more code modules/files.

**Component Types:**
- **Service** - Business logic and application services
- **Controller** - Request handlers and API endpoints
- **Repository** - Data access and persistence layer
- **Model** - Domain models and data structures
- **Utility** - Helper functions and shared utilities
- **Middleware** - Request/response processing pipeline
- **View** - UI components and presentation layer
- **Facade** - Simplified interface to complex subsystems
- **Factory** - Object creation and instantiation
- **Adapter** - Interface translation for external APIs

### Code Structure

**Organization Patterns:**
- **Feature-based** - Components organized by business feature
- **Layer-based** - Components organized by architectural layer (MVC)
- **Domain-driven** - Components organized by domain boundaries

**Structure Analysis:**
- Directory structure and file organization
- Export patterns (public API)
- Module boundaries
- Code metrics (LOC, complexity, dependencies)

### Design Patterns

**Detected Patterns:**
- **Singleton** - Single instance pattern
- **Factory** - Object creation pattern
- **Repository** - Data access abstraction
- **Dependency Injection** - IoC and constructor injection
- **Observer** - Event subscription pattern
- **Strategy** - Interchangeable algorithm pattern
- **Decorator** - Behavior enhancement pattern
- **Adapter** - Interface translation pattern

### Dependencies

**Dependency Types:**
- **uses** - General usage (loose coupling)
- **calls** - Direct method invocation (moderate coupling)
- **imports** - Module import (tight coupling)
- **implements** - Interface implementation (loose coupling)
- **inherits** - Inheritance (tight coupling)
- **composes** - Composition (tight coupling)
- **observes** - Event subscription (loose coupling)

**Coupling Analysis:**
- **Loose coupling** - Interface-based, event-driven (good)
- **Tight coupling** - Direct imports, composition (warning)
- **Circular dependencies** - A → B → A (critical issue)

## Common Architecture Patterns

### 1. MVC (Model-View-Controller)

```
Controllers Layer:
  ├── UserController
  ├── ProductController
  └── OrderController
Services Layer:
  ├── UserService
  ├── ProductService
  └── OrderService
Repository Layer:
  ├── UserRepository
  ├── ProductRepository
  └── OrderRepository
Models Layer:
  ├── User
  ├── Product
  └── Order
```

**Dependencies:** Controllers → Services → Repositories → Models

### 2. Layered Architecture (3-Tier)

```
Presentation Layer:
  └── API Controllers
Business Logic Layer:
  └── Services
Data Access Layer:
  └── Repositories
```

**Dependencies:** One-way flow from top to bottom

### 3. Hexagonal Architecture (Ports & Adapters)

```
Domain Core:
  ├── User (model)
  └── OrderAggregate (model)
Application Layer:
  ├── CreateUserUseCase
  └── ProcessOrderUseCase
Infrastructure (Adapters):
  ├── UserRepositoryAdapter
  ├── EmailServiceAdapter
  └── PaymentGatewayAdapter
Ports (Interfaces):
  ├── IUserRepository
  └── IPaymentGateway
```

**Dependencies:** Infrastructure → Application → Domain (dependency inversion)

### 4. CQRS (Command Query Responsibility Segregation)

```
Commands (Write):
  ├── CreateUserCommand
  ├── UpdateOrderCommand
  └── ProcessPaymentCommand
Queries (Read):
  ├── GetUserQuery
  ├── ListOrdersQuery
  └── SearchProductsQuery
Handlers:
  ├── UserCommandHandler
  └── UserQueryHandler
```

**Dependencies:** Handlers process commands/queries

## Component Identification Rules

### What IS a Component (C3 Level)?

✅ **YES** - These are components:
- Groupings of related classes/modules with single responsibility
- Layers in layered architecture (each controller/service is a component)
- Feature modules with all layers
- Reusable libraries or utilities
- Domain model clusters

✅ **Examples:**
- "User Authentication Service" (AuthService + TokenManager + SessionStore)
- "Product Controller" (handles product endpoints)
- "User Repository" (data access for users)
- "Validation Utilities" (input validation helpers)

### What is NOT a Component (C3 Level)?

❌ **NO** - These are NOT components:
- Individual classes/functions (those are C4 - Code level)
- Entire containers (those are C2 - Container level)
- Generic layer names without specificity
- Technology/framework names

❌ **Examples:**
- "validateEmail() function" ❌ → Part of "Validation Utilities Component"
- "UserModel class" ❌ → Part of "User Domain Model Component"
- "Backend API" ❌ → This is a C2 Container
- "Controllers" ❌ → Too broad, identify specific controllers

## Best Practices

### 1. Identify Components at Right Granularity

**Right Granularity:**
- ✅ "Authentication Service Component" (multiple related classes)
- ✅ "User Controller Component" (specific controller with routes)
- ✅ "Payment Utilities Component" (related helper functions)

**Wrong Granularity:**
- ❌ "validateToken() function" (too fine - this is C4)
- ❌ "Services Layer" (too coarse - identify specific services)

### 2. Respect Architectural Patterns

- Identify the pattern first (MVC, layered, hexagonal)
- Then identify components within that pattern
- Document pattern usage in observations

### 3. Analyze Coupling and Cohesion

**High Cohesion (Good):**
- All methods operate on related data
- Single responsibility principle followed

**Low Cohesion (Warning):**
- Component does too many unrelated things
- Mixed responsibilities

**Loose Coupling (Good):**
- Interface-based dependencies
- Event-driven communication

**Tight Coupling (Warning):**
- Direct imports everywhere
- Difficult to test in isolation

### 4. Detect Design Patterns

**Document patterns found:**
- ℹ️ "Well-structured use of Repository pattern"
- ⚠️ "Singleton pattern overused, making testing difficult"
- 🔴 "God Object anti-pattern detected (500+ LOC)"

### 5. Calculate Metrics

**Important Metrics:**
- **Lines of Code** - Component size
- **Cyclomatic Complexity** - Code complexity (CC < 10 ideal)
- **Dependencies** - Number of component dependencies
- **Test Coverage** - Percentage of code tested
- **Methods** - Number of public methods
- **Exports** - Public API surface

## Anti-Patterns to Avoid

### ❌ Over-Granular Components

**Wrong:**
```
- validateEmail Component (1 function)
- validatePhone Component (1 function)
- sanitizeInput Component (1 function)
```

**Right:**
```
- Validation Utilities Component (all validation functions)
```

### ❌ Generic Names

**Wrong:**
```
- Helper Component
- Utils Component
- Service Component
```

**Right:**
```
- Email Validation Utilities
- Date Formatting Service
- Payment Processing Service
```

### ❌ Mixing Levels

**Wrong:** Identifying classes as components
```
- AuthService class ❌ (This is C4)
```

**Right:** Identify the component
```
- Authentication Service Component (contains AuthService, TokenManager, etc.)
```

### ❌ Ignoring Patterns

**Wrong:**
- Not documenting design patterns
- Missing coupling analysis

**Right:**
- Document patterns (Singleton, Factory, DI)
- Analyze coupling strength
- Flag circular dependencies

## Integration with Melly

### Input

This skill expects:
- Repository paths from `init.json`
- System definitions from `c1-systems.json`
- Container definitions from `c2-containers.json`
- Code files and directory structure

### Output

This skill helps generate:
- `c3-components.json` with component definitions
- Component observations (patterns, coupling, complexity)
- Component relations (dependencies)
- Markdown documentation in `knowledge-base/systems/*/c3/`

### Validation

Generated output is validated by:
- `plugins/melly-validation/scripts/validate-c3-components.py`
- Schema compliance checks
- Referential integrity validation (component → container links)
- Timestamp ordering checks

## Example: Identifying Components in NestJS Backend

### Container Found:
```
Backend API (NestJS)
  Path: /repos/api-server/src/
```

### Components Identified:

1. **User Controller**
   - Type: `controller`
   - Files: `controllers/UserController.ts` (150 LOC)
   - Responsibilities: Handle user-related HTTP requests
   - Dependencies: Uses UserService
   - Pattern: Dependency Injection (via @Injectable)

2. **User Service**
   - Type: `service`
   - Files: `services/UserService.ts` (280 LOC)
   - Responsibilities: User business logic
   - Dependencies: Uses UserRepository, EmailService
   - Pattern: Service Layer pattern

3. **User Repository**
   - Type: `repository`
   - Files: `repositories/UserRepository.ts` (120 LOC)
   - Responsibilities: User data access
   - Dependencies: Uses TypeORM
   - Pattern: Repository pattern

4. **Authentication Service**
   - Type: `service`
   - Files: `auth/AuthService.ts`, `auth/TokenManager.ts` (350 LOC total)
   - Responsibilities: User authentication, token management
   - Dependencies: Uses UserRepository, JwtService
   - Pattern: Dependency Injection, Singleton (TokenManager)

5. **Validation Utilities**
   - Type: `utility`
   - Files: `utils/validation.ts` (85 LOC)
   - Responsibilities: Input validation helpers
   - Dependencies: Uses class-validator library
   - Pattern: Utility functions

### Observations Generated:

- ℹ️ **design-patterns**: "Consistent use of Dependency Injection via NestJS @Injectable decorators"
- ℹ️ **code-structure**: "Well-organized layer-based architecture (controllers/services/repositories)"
- ⚠️ **coupling**: "UserService has tight coupling to 5+ components"
- ℹ️ **testing**: "High test coverage (85%) across all services"

## Technology-Specific Examples

### NestJS (TypeScript)
Components: Controllers with @Controller(), Services with @Injectable(), Repositories, Guards, Interceptors

### Django (Python)
Components: Views (views.py), Models (models.py), Serializers, Managers, Utilities

### Spring Boot (Java)
Components: RestControllers (@RestController), Services (@Service), Repositories (@Repository), Entities

### React (TypeScript)
Components: UI Components, Custom Hooks, Context Providers, Utilities

## References

- [C4 Model Official Documentation](https://c4model.com/)
- [Melly C4 Methodology Guide](/docs/c4model-methodology.md)
- [Melly Workflow Guide](/docs/workflow-guide.md)
- [C3 Components JSON Template](/plugins/melly-validation/templates/c3-components-template.json)
- [Design Patterns Catalog](https://refactoring.guru/design-patterns)

## Support

For issues or questions:
- Check the Melly documentation in `/docs/`
- Review examples in `/knowledge-base/templates/`
- Consult the C4 Model methodology guide

---

**Version**: 1.0.0
**Plugin Type**: Skill
**Compatibility**: Melly 1.0.0+
**License**: MIT
