---
name: c4model-c3
description: C4 Model Level 3 (Component) methodology for identifying code-level components, their responsibilities, dependencies, and design patterns. Use when analyzing software architecture at the component abstraction level, identifying code modules, classes, functions, and their interactions within containers. Keywords - component level, C3 level, component identification, code structure, design patterns, component boundaries, component responsibilities, dependency analysis, code modules, architectural components, software components, code organization, component relationships, coupling analysis, cohesion analysis.
allowed-tools: Read, Grep, Glob, Bash
---

# C4 Model - Level 3: Component Methodology

## Overview

You are an expert in the C4 Model's Level 3 (Component) methodology. This skill provides comprehensive knowledge for identifying and documenting software components at the code-level architectural abstraction.

**Your Mission:** Help identify WHAT code components exist within containers, WHAT responsibilities they have, and HOW they interact - with focus on design patterns and code structure.

---

## C3 Level Definition

### What is Component Level (C3)?

The Component level shows the **internal structure** of containers - the major code building blocks:

- **Components** - Code modules, classes, packages with clear responsibilities
- **Responsibilities** - What each component does (single responsibility)
- **Dependencies** - How components depend on each other
- **Patterns** - Design patterns and architectural patterns used
- **Boundaries** - Package boundaries, module boundaries, layer boundaries

### Abstraction Level

```
┌─────────────────────────────────────────────┐
│ C1: System Context                          │
│ "What systems exist?"                       │
├─────────────────────────────────────────────┤
│ C2: Container Level                         │
│ "What are the deployable units?"            │
├─────────────────────────────────────────────┤
│ C3: Component Level                         │ ← YOU ARE HERE
│ "What are the code modules?"                │
├─────────────────────────────────────────────┤
│ C4: Code Level                              │
│ "What are the classes/functions?"           │
└─────────────────────────────────────────────┘
```

**At C3, we focus on:**
- ✅ Component identification and naming
- ✅ Component responsibilities (single responsibility)
- ✅ Component dependencies and coupling
- ✅ Design patterns and architectural patterns
- ✅ Code organization and structure
- ✅ Layer boundaries and module boundaries
- ✅ Component interactions and relationships

**At C3, we do NOT focus on:**
- ❌ Individual functions/methods (that's C4)
- ❌ Line-by-line code (that's C4)
- ❌ Variable names and implementation details (that's C4)
- ❌ Deployment details (that's C2)

---

## Component Identification Methodology

### Step 1: Understand Container Structure

Start by analyzing the containers from `c2-containers.json`:

**Questions to ask:**
1. What containers exist in this system?
2. What is the technology stack for each container?
3. What is the directory structure?
4. What is the entry point?

**Container-to-Component Mapping:**
- **Backend API** → Controllers, Services, Repositories, Models
- **Web Frontend** → Pages, Components, Services, State Management
- **Mobile App** → Screens, ViewModels, Services, Repositories
- **Worker Service** → Jobs, Handlers, Processors, Queues
- **Library** → Modules, Utilities, Helpers

### Step 2: Apply Component Identification Rules

A **component** at C3 level is:

#### ✅ A Component IS:

1. **A cohesive code module with clear responsibility**
   - Has one primary purpose (Single Responsibility Principle)
   - Encapsulates related functionality
   - Example: `UserAuthenticationService`, `OrderRepository`, `PaymentController`

2. **A collection of related classes/functions**
   - Groups related code together
   - Organized in a package, module, or directory
   - Example: `authentication/` module with auth-related classes

3. **An architectural building block**
   - Represents a significant piece of functionality
   - Has well-defined interface/API
   - Example: `EmailNotificationService`, `DatabaseConnection`

4. **A layer or subsystem**
   - Distinct architectural layer
   - Clear boundary from other layers
   - Example: `data-access-layer/`, `business-logic-layer/`

#### ❌ A Component is NOT:

1. **Individual functions** (too granular - that's C4)
   - ❌ `validateEmail()` function
   - ❌ `calculateTotal()` function
   - ✅ `ValidationService` (collection of validation functions)

2. **Single classes unless architecturally significant**
   - ❌ `EmailValidator` class (too small)
   - ✅ `AuthenticationService` class (significant)
   - Rule: If class > 200 LOC or has major role, it's a component

3. **Configuration files**
   - ❌ `config.json`
   - ❌ `.env`
   - These are not components, but configuration

4. **Test files**
   - ❌ `UserService.test.ts`
   - Tests verify components but aren't components themselves

### Step 3: Analyze File Structure

Use file system structure to identify components:

**Common patterns:**

#### Pattern 1: Directory-based Components (Recommended)
```
src/
├── authentication/           # → Component: Authentication
│   ├── AuthService.ts
│   ├── AuthController.ts
│   ├── TokenManager.ts
│   └── index.ts
├── users/                    # → Component: User Management
│   ├── UserService.ts
│   ├── UserRepository.ts
│   ├── User.model.ts
│   └── index.ts
└── payments/                 # → Component: Payment Processing
    ├── PaymentService.ts
    ├── PaymentGateway.ts
    └── index.ts
```

#### Pattern 2: Layered Components
```
src/
├── controllers/              # → Component Layer: Controllers
│   ├── UserController.ts
│   ├── OrderController.ts
│   └── ProductController.ts
├── services/                 # → Component Layer: Services
│   ├── UserService.ts
│   ├── OrderService.ts
│   └── ProductService.ts
└── repositories/             # → Component Layer: Repositories
    ├── UserRepository.ts
    ├── OrderRepository.ts
    └── ProductRepository.ts
```

#### Pattern 3: Feature-based Components
```
src/
├── features/
│   ├── user-management/      # → Component: User Management
│   │   ├── components/
│   │   ├── services/
│   │   └── models/
│   ├── order-management/     # → Component: Order Management
│   │   ├── components/
│   │   ├── services/
│   │   └── models/
```

**Detection commands:**
```bash
# Find directories with code files
find src -type d -not -path "*/node_modules/*" -not -path "*/.git/*"

# List files by directory
ls -la src/*/

# Count files per directory
find src -type f \( -name "*.ts" -o -name "*.js" \) | xargs dirname | sort | uniq -c
```

### Step 4: Detect Component Types

Classify each component by type:

**Component Types:**

1. **controller** - HTTP request handlers
   - Handles incoming requests
   - Routes to services
   - Returns responses
   - Example: `UserController`, `OrderController`

2. **service** - Business logic
   - Core business logic
   - Orchestrates operations
   - Encapsulates domain logic
   - Example: `UserService`, `PaymentService`

3. **repository** - Data access
   - Database operations
   - Data persistence
   - Query abstraction
   - Example: `UserRepository`, `OrderRepository`

4. **model** - Data models
   - Entity definitions
   - Data structures
   - Domain objects
   - Example: `User`, `Order`, `Product`

5. **middleware** - Request/response processing
   - Authentication middleware
   - Logging middleware
   - Validation middleware
   - Example: `AuthMiddleware`, `LoggingMiddleware`

6. **utility** - Helper functions
   - Shared utilities
   - Common helpers
   - Cross-cutting concerns
   - Example: `DateUtils`, `StringUtils`

7. **dto** - Data transfer objects
   - Request/response schemas
   - API contracts
   - Validation schemas
   - Example: `CreateUserDto`, `LoginResponseDto`

8. **adapter** - External integrations
   - Third-party API clients
   - External service wrappers
   - Protocol adapters
   - Example: `StripeAdapter`, `SendGridAdapter`

9. **factory** - Object creation
   - Complex object construction
   - Dependency creation
   - Example: `UserFactory`, `OrderFactory`

10. **validator** - Validation logic
    - Input validation
    - Business rule validation
    - Example: `EmailValidator`, `OrderValidator`

11. **facade** - Simplified interfaces
    - Simplifies complex subsystems
    - Provides unified interface
    - Example: `PaymentFacade`, `NotificationFacade`

12. **guard** - Authorization/authentication
    - Access control
    - Route protection
    - Example: `AuthGuard`, `RoleGuard`

### Step 5: Define Component Boundaries

For each component, define:

#### 1. Package/Module Boundary
- What package or module does it belong to?
- What is the namespace?
- What is the import path?

**Example:**
```typescript
// Component: Authentication Service
// Package: @app/authentication
// Module: src/authentication/AuthService.ts
// Import: import { AuthService } from '@app/authentication';
```

#### 2. Layer Boundary
- What architectural layer?
- Presentation, Business Logic, Data Access?

**Example:**
```
Presentation Layer:    Controllers, Middleware, DTOs
Business Logic Layer:  Services, Domain Models, Validators
Data Access Layer:     Repositories, Database Models, Adapters
```

#### 3. Responsibility Boundary
- What is the single responsibility?
- What does it do?
- What does it NOT do?

**Example:**
```json
{
  "id": "user-service",
  "name": "User Service",
  "responsibility": "Manages user lifecycle operations including registration, profile updates, and account deletion",
  "does": [
    "Validate user input",
    "Create new users",
    "Update user profiles",
    "Delete user accounts"
  ],
  "does_not": [
    "Handle HTTP requests (Controller's job)",
    "Access database directly (Repository's job)",
    "Send emails (Email Service's job)"
  ]
}
```

### Step 6: Identify Component Responsibilities

For each component, determine its responsibilities:

**Questions to ask:**
1. What is the primary purpose?
2. What operations does it perform?
3. What data does it manage?
4. What services does it provide?
5. What dependencies does it have?

**Analysis techniques:**

#### Technique 1: Analyze Public Methods
```typescript
// UserService.ts
export class UserService {
  // Public interface reveals responsibilities:
  async createUser(data: CreateUserDto): Promise<User>
  async updateUser(id: string, data: UpdateUserDto): Promise<User>
  async deleteUser(id: string): Promise<void>
  async getUserById(id: string): Promise<User>
  async getUserByEmail(email: string): Promise<User>
}

// Responsibilities:
// - User creation
// - User updates
// - User deletion
// - User retrieval by ID
// - User retrieval by email
```

#### Technique 2: Analyze Dependencies
```typescript
// PaymentService.ts depends on:
import { PaymentGateway } from './PaymentGateway';
import { OrderRepository } from '../orders/OrderRepository';
import { EmailService } from '../notifications/EmailService';

// Responsibilities indicated by dependencies:
// - Processes payments (PaymentGateway)
// - Updates order status (OrderRepository)
// - Sends payment confirmations (EmailService)
```

#### Technique 3: Analyze File Content
```bash
# Count methods in a class (using extended regex)
grep -E '^\s+(public|private|protected|async)\s+\w+\s*\(' UserService.ts

# Find key operations
grep -E '(create|update|delete|get|find|save)' UserService.ts
```

---

## Code Structure Analysis

### Directory Structure Patterns

#### Pattern 1: Feature-based Structure
```
src/
├── users/
│   ├── user.controller.ts     # Component: User Controller
│   ├── user.service.ts        # Component: User Service
│   ├── user.repository.ts     # Component: User Repository
│   ├── user.model.ts          # Component: User Model
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   └── update-user.dto.ts
│   └── index.ts
```

**Advantages:**
- Clear feature boundaries
- Easy to locate related code
- Good for domain-driven design

**Component detection:**
```bash
# List all feature directories
ls -d src/*/

# Count components per feature
find src \( -name "*.service.ts" -o -name "*.controller.ts" -o -name "*.repository.ts" \) | xargs dirname | sort | uniq -c
```

#### Pattern 2: Layer-based Structure
```
src/
├── controllers/
│   ├── user.controller.ts
│   ├── order.controller.ts
│   └── product.controller.ts
├── services/
│   ├── user.service.ts
│   ├── order.service.ts
│   └── product.service.ts
├── repositories/
│   ├── user.repository.ts
│   ├── order.repository.ts
│   └── product.repository.ts
└── models/
    ├── user.model.ts
    ├── order.model.ts
    └── product.model.ts
```

**Advantages:**
- Clear layer separation
- Easy to enforce layer rules
- Good for traditional MVC

**Component detection:**
```bash
# Count components per layer
wc -l controllers/*.ts services/*.ts repositories/*.ts
```

#### Pattern 3: Domain-Driven Design (DDD)
```
src/
├── domain/
│   ├── user/
│   │   ├── User.entity.ts         # Component: User Entity
│   │   ├── UserRepository.ts      # Component: User Repository
│   │   └── UserService.ts         # Component: User Domain Service
│   └── order/
│       ├── Order.entity.ts
│       ├── OrderRepository.ts
│       └── OrderService.ts
├── application/
│   ├── user/
│   │   ├── CreateUserUseCase.ts   # Component: Create User Use Case
│   │   ├── UpdateUserUseCase.ts   # Component: Update User Use Case
│   └── order/
│       ├── PlaceOrderUseCase.ts
│       └── CancelOrderUseCase.ts
└── infrastructure/
    ├── database/
    │   ├── UserRepositoryImpl.ts  # Component: User Repository Implementation
    │   └── OrderRepositoryImpl.ts
    └── http/
        ├── UserController.ts      # Component: User Controller
        └── OrderController.ts
```

**Advantages:**
- Clear domain boundaries
- Separation of concerns
- Testable use cases

### Export Pattern Analysis

Analyze how components expose their APIs:

#### Pattern 1: Named Exports
```typescript
// authentication/index.ts
export { AuthService } from './AuthService';
export { AuthController } from './AuthController';
export { TokenManager } from './TokenManager';
export * from './dto';

// Component: Authentication Module
// Public API: AuthService, AuthController, TokenManager, DTOs
```

#### Pattern 2: Default Exports
```typescript
// UserService.ts
export default class UserService { ... }

// Component: User Service
// Import: import UserService from './UserService';
```

#### Pattern 3: Facade Exports
```typescript
// payment/index.ts
import { PaymentService } from './PaymentService';
import { PaymentGateway } from './PaymentGateway';
import { PaymentValidator } from './PaymentValidator';

// Facade pattern - single entry point
export class PaymentFacade {
  constructor(
    private service: PaymentService,
    private gateway: PaymentGateway,
    private validator: PaymentValidator
  ) {}

  // Simplified API
  async processPayment(data: PaymentDto): Promise<PaymentResult> { ... }
}

// Component: Payment Facade
// Hides internal complexity
```

### Code Metrics Analysis

Use metrics to identify significant components:

#### Metric 1: Lines of Code (LOC)
```bash
# Count lines per file
find src -name "*.ts" -print0 | xargs -0 wc -l | sort -rn

# Components with > 200 LOC are significant
find src -name "*.ts" -print0 | xargs -0 wc -l | awk '$1 > 200 { print $2, $1 }'
```

**Guidelines:**
- **< 100 LOC**: Small component or helper
- **100-300 LOC**: Typical component
- **300-500 LOC**: Large component (consider splitting)
- **> 500 LOC**: Very large (definitely a component, likely needs refactoring)

#### Metric 2: Cyclomatic Complexity
```bash
# Use complexity tools
find src -name "*.ts" -print0 | xargs -0 npx ts-complexity

# High complexity (>10) indicates important component
```

#### Metric 3: Dependency Count
```bash
# Count imports per file
find src -name "*.ts" -print0 | xargs -0 grep -c "^import" 2>/dev/null

# Files with many imports are often important orchestrators (Services)
```

#### Metric 4: Export Count
```bash
# Count exports per file
find src -name "*.ts" -print0 | xargs -0 grep -c "^export" 2>/dev/null

# Files with many exports are often facades or utility modules
```

---

## Dependency Analysis

### Dependency Types

#### 1. Internal Dependencies (Within Container)
```typescript
// UserService.ts
import { UserRepository } from './UserRepository';     // Same feature
import { EmailService } from '../email/EmailService';  // Different feature
import { ValidationUtil } from '../utils/validation';  // Utility

// Dependencies:
// - UserRepository (direct dependency)
// - EmailService (cross-feature dependency)
// - ValidationUtil (utility dependency)
```

#### 2. External Dependencies (Outside Container)
```typescript
// PaymentService.ts
import Stripe from 'stripe';                    // External library
import { Logger } from '@nestjs/common';        // Framework
import axios from 'axios';                      // HTTP client

// External dependencies:
// - Stripe SDK
// - NestJS framework
// - Axios library
```

#### 3. Framework Dependencies
```typescript
// UserController.ts
import { Controller, Get, Post, Body } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

// Framework dependencies:
// - NestJS decorators
// - Swagger decorators
```

### Dependency Direction

Analyze the flow of dependencies:

**Recommended flow (Dependency Inversion):**
```
Controllers → Services → Repositories → Models
     ↓            ↓            ↓
  (HTTP)      (Business)    (Data)
```

**Anti-pattern (Skip layers):**
```
Controllers → Repositories  ❌  (skips business logic layer)
```

**Example: Good Dependency Direction**
```typescript
// Good: Controller depends on Service
@Controller('users')
export class UserController {
  constructor(private userService: UserService) {}

  @Post()
  createUser(@Body() dto: CreateUserDto) {
    return this.userService.createUser(dto);
  }
}

// Good: Service depends on Repository
export class UserService {
  constructor(private userRepo: UserRepository) {}

  async createUser(dto: CreateUserDto) {
    // Business logic here
    return this.userRepo.save(user);
  }
}

// Good: Repository depends on Model
export class UserRepository {
  async save(user: User) {
    // Data access here
  }
}
```

### Coupling Analysis

**Types of coupling:**

#### 1. Tight Coupling (Bad)
```typescript
// Bad: Direct instantiation
export class UserService {
  private emailService = new EmailService();  // ❌ Tightly coupled

  async createUser(data: CreateUserDto) {
    const user = await this.saveUser(data);
    this.emailService.sendWelcome(user);  // Can't mock in tests
  }
}
```

#### 2. Loose Coupling (Good)
```typescript
// Good: Dependency injection
export class UserService {
  constructor(private emailService: EmailService) {}  // ✅ Loosely coupled

  async createUser(data: CreateUserDto) {
    const user = await this.saveUser(data);
    this.emailService.sendWelcome(user);  // Easy to mock
  }
}
```

**Coupling metrics:**
- **Afferent Coupling (Ca)**: Number of components that depend on this component
- **Efferent Coupling (Ce)**: Number of components this component depends on
- **Instability (I)**: Ce / (Ca + Ce)
  - I = 0: Very stable (many dependents, no dependencies)
  - I = 1: Very unstable (no dependents, many dependencies)

**Detection:**
```bash
# Find components with many imports (high efferent coupling)
find src -name "*.ts" -print0 | while IFS= read -r -d '' file; do
  count=$(grep -c '^import' "$file" || echo 0)
  printf "%d %s\n" "$count" "$file"
done | sort -rn | head -20

# Find components imported by many others (high afferent coupling)
grep -r "from '\.\./\.\./.*'" src/ | cut -d"'" -f2 | sort | uniq -c | sort -rn
```

### Circular Dependency Detection

**Anti-pattern: Circular dependencies**
```
UserService → OrderService → UserService  ❌
```

**Detection:**
```bash
# Use madge for Node.js projects
npx madge --circular src/

# Use dependency-cruiser
npx depcruise --validate .dependency-cruiser.js src/
```

**Solution:**
- Extract shared logic to third component
- Use events instead of direct calls
- Refactor to remove circular reference

---

## Pattern Detection

### Design Patterns

#### Pattern 1: Singleton Pattern

**Description:** Ensures a class has only one instance

**Detection:**
```typescript
// Singleton pattern indicators
export class DatabaseConnection {
  private static instance: DatabaseConnection;

  private constructor() {}  // Private constructor

  static getInstance(): DatabaseConnection {
    if (!this.instance) {
      this.instance = new DatabaseConnection();
    }
    return this.instance;
  }
}
```

**Grep detection:**
```bash
grep -r "private static.*instance" src/
grep -r "private constructor" src/
grep -r "getInstance()" src/
```

**Observation:**
```json
{
  "id": "obs-singleton-database",
  "title": "Singleton pattern for database connection",
  "category": "design-patterns",
  "severity": "info",
  "pattern": "singleton",
  "description": "DatabaseConnection uses Singleton pattern to ensure single instance across application"
}
```

#### Pattern 2: Factory Pattern

**Description:** Creates objects without specifying exact class

**Detection:**
```typescript
// Factory pattern indicators
export class UserFactory {
  static createUser(type: string, data: any): User {
    switch (type) {
      case 'admin':
        return new AdminUser(data);
      case 'customer':
        return new CustomerUser(data);
      default:
        return new GuestUser(data);
    }
  }
}
```

**Grep detection:**
```bash
grep -r "Factory" src/
grep -r "static create" src/
```

#### Pattern 3: Repository Pattern

**Description:** Abstracts data access logic

**Detection:**
```typescript
// Repository pattern indicators
export class UserRepository {
  async findById(id: string): Promise<User> { ... }
  async findAll(): Promise<User[]> { ... }
  async save(user: User): Promise<User> { ... }
  async delete(id: string): Promise<void> { ... }
}
```

**Grep detection:**
```bash
grep -r "Repository" src/
grep -r "findById\|findAll\|save.*Promise" src/
```

#### Pattern 4: Dependency Injection

**Description:** Dependencies provided externally

**Detection in NestJS:**
```typescript
@Injectable()
export class UserService {
  constructor(
    @Inject(UserRepository) private userRepo: UserRepository,
    @Inject(EmailService) private emailService: EmailService
  ) {}
}
```

**Detection in Spring (Java):**
```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;
}
```

**Grep detection:**
```bash
# NestJS
grep -r "@Injectable\|@Inject" src/

# Spring
grep -r "@Service\|@Autowired\|@Component" src/

# Constructor injection
grep -r "constructor(" src/ | grep "private"
```

#### Pattern 5: Observer Pattern (Event-Driven)

**Description:** Publish-subscribe mechanism

**Detection:**
```typescript
// Observer pattern indicators
export class OrderService {
  async createOrder(data: CreateOrderDto) {
    const order = await this.orderRepo.save(data);

    // Emit event
    this.eventEmitter.emit('order.created', order);

    return order;
  }
}

// Observers
export class EmailService {
  @OnEvent('order.created')
  handleOrderCreated(order: Order) {
    this.sendOrderConfirmation(order);
  }
}
```

**Grep detection:**
```bash
grep -r "\.emit\|\.on\|@OnEvent\|subscribe\|publish" src/
```

#### Pattern 6: Strategy Pattern

**Description:** Select algorithm at runtime

**Detection:**
```typescript
// Strategy pattern
interface PaymentStrategy {
  pay(amount: number): Promise<PaymentResult>;
}

class CreditCardPayment implements PaymentStrategy {
  async pay(amount: number) { ... }
}

class PayPalPayment implements PaymentStrategy {
  async pay(amount: number) { ... }
}

class PaymentContext {
  constructor(private strategy: PaymentStrategy) {}

  async executePayment(amount: number) {
    return this.strategy.pay(amount);
  }
}
```

**Grep detection:**
```bash
grep -r "implements.*Strategy\|Strategy.*interface" src/
```

#### Pattern 7: Decorator Pattern

**Description:** Add behavior dynamically

**Detection in TypeScript:**
```typescript
// Decorator pattern (using TypeScript decorators)
@Controller('users')
@UseGuards(AuthGuard)          // Decorator
@UseInterceptors(LoggingInterceptor)  // Decorator
export class UserController {
  @Get()
  @Roles('admin')              // Decorator
  findAll() { ... }
}
```

**Grep detection:**
```bash
grep -r "^@\w\+(" src/
```

#### Pattern 8: Adapter Pattern

**Description:** Converts interface to another interface

**Detection:**
```typescript
// Adapter pattern
export class StripeAdapter {
  constructor(private stripeClient: Stripe) {}

  // Adapt Stripe API to internal interface
  async processPayment(payment: PaymentDto): Promise<PaymentResult> {
    const stripePayment = this.convertToStripeFormat(payment);
    const result = await this.stripeClient.charges.create(stripePayment);
    return this.convertFromStripeFormat(result);
  }
}
```

**Grep detection:**
```bash
grep -r "Adapter" src/
grep -r "convert.*Format" src/
```

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

---

## Common Architecture Patterns

### Pattern 1: MVC (Model-View-Controller)

**Description:** Separates concerns into Model, View, Controller

**Component structure:**
```
src/
├── models/                  # Models (Data)
│   ├── User.ts
│   ├── Order.ts
│   └── Product.ts
├── views/                   # Views (Presentation) - if server-rendered
│   ├── user-list.ejs
│   └── order-detail.ejs
└── controllers/             # Controllers (Logic)
    ├── UserController.ts
    ├── OrderController.ts
    └── ProductController.ts
```

**Components identified:**
- **Controllers**: UserController, OrderController, ProductController
- **Models**: User, Order, Product
- **Views**: (if applicable)

**Observation:**
```json
{
  "id": "obs-mvc-pattern",
  "title": "MVC pattern with controllers and models",
  "category": "architectural-pattern",
  "pattern": "mvc",
  "description": "Application follows MVC pattern with clear separation between controllers (request handling) and models (data representation)"
}
```

---

### Pattern 2: Layered Architecture (3-Tier)

**Description:** Separates into Presentation, Business Logic, Data Access layers

**Component structure:**
```
src/
├── presentation/            # Presentation Layer
│   ├── controllers/
│   │   ├── UserController.ts
│   │   └── OrderController.ts
│   └── middleware/
│       ├── AuthMiddleware.ts
│       └── ValidationMiddleware.ts
├── business/                # Business Logic Layer
│   ├── services/
│   │   ├── UserService.ts
│   │   └── OrderService.ts
│   └── validators/
│       ├── UserValidator.ts
│       └── OrderValidator.ts
└── data/                    # Data Access Layer
    ├── repositories/
    │   ├── UserRepository.ts
    │   └── OrderRepository.ts
    └── models/
        ├── User.model.ts
        └── Order.model.ts
```

**Layer rules:**
- Presentation → Business Logic → Data Access (one direction only)
- No skipping layers (Controller can't call Repository directly)

**Components identified:**
- **Presentation**: UserController, OrderController, AuthMiddleware
- **Business Logic**: UserService, OrderService, UserValidator
- **Data Access**: UserRepository, OrderRepository, User Model, Order Model

**Detection:**
```bash
# Check for layer violations
grep -r "Repository" src/controllers/  # ❌ Controller calling Repository directly

# Verify proper layering
grep -r "Service" src/controllers/     # ✅ Controller calling Service
grep -r "Repository" src/services/     # ✅ Service calling Repository
```

---

### Pattern 3: Hexagonal Architecture (Ports & Adapters)

**Description:** Core business logic isolated from external concerns

**Component structure:**
```
src/
├── domain/                  # Core Domain (Business Logic)
│   ├── user/
│   │   ├── User.entity.ts
│   │   ├── UserService.ts
│   │   └── ports/
│   │       ├── UserRepository.port.ts      # Interface
│   │       └── EmailService.port.ts         # Interface
│   └── order/
│       ├── Order.entity.ts
│       └── OrderService.ts
├── application/             # Application Services (Use Cases)
│   ├── CreateUserUseCase.ts
│   ├── PlaceOrderUseCase.ts
│   └── ProcessPaymentUseCase.ts
└── infrastructure/          # Infrastructure (Adapters)
    ├── database/
    │   └── UserRepositoryImpl.ts           # Implementation
    ├── email/
    │   └── EmailServiceImpl.ts             # Implementation
    └── http/
        ├── UserController.ts               # HTTP Adapter
        └── OrderController.ts              # HTTP Adapter
```

**Key concepts:**
- **Ports**: Interfaces defined by domain (UserRepository.port.ts)
- **Adapters**: Implementations in infrastructure (UserRepositoryImpl.ts)
- **Dependency Inversion**: Domain defines interfaces, infrastructure implements

**Components identified:**
- **Domain**: User, Order, UserService, OrderService
- **Ports**: UserRepository (interface), EmailService (interface)
- **Adapters**: UserRepositoryImpl, EmailServiceImpl, UserController
- **Use Cases**: CreateUserUseCase, PlaceOrderUseCase

**Observation:**
```json
{
  "id": "obs-hexagonal-arch",
  "title": "Hexagonal architecture with ports and adapters",
  "category": "architectural-pattern",
  "pattern": "hexagonal",
  "description": "Application uses hexagonal architecture. Domain defines port interfaces (UserRepository.port.ts), infrastructure provides adapter implementations (UserRepositoryImpl.ts). Business logic isolated from external dependencies."
}
```

---

### Pattern 4: CQRS (Command Query Responsibility Segregation)

**Description:** Separate read and write operations

**Component structure:**
```
src/
├── commands/                # Write side (Commands)
│   ├── CreateUserCommand.ts
│   ├── UpdateUserCommand.ts
│   └── handlers/
│       ├── CreateUserHandler.ts
│       └── UpdateUserHandler.ts
├── queries/                 # Read side (Queries)
│   ├── GetUserQuery.ts
│   ├── ListUsersQuery.ts
│   └── handlers/
│       ├── GetUserHandler.ts
│       └── ListUsersHandler.ts
└── models/
    ├── write/               # Write models
    │   └── User.entity.ts
    └── read/                # Read models (often denormalized)
        └── UserView.ts
```

**Key concepts:**
- **Commands**: Change state (CreateUser, UpdateUser)
- **Queries**: Read state (GetUser, ListUsers)
- **Separate models**: Write model vs Read model

**Components identified:**
- **Commands**: CreateUserCommand, UpdateUserCommand
- **Command Handlers**: CreateUserHandler, UpdateUserHandler
- **Queries**: GetUserQuery, ListUsersQuery
- **Query Handlers**: GetUserHandler, ListUsersHandler
- **Write Models**: User (entity)
- **Read Models**: UserView

**Detection:**
```bash
grep -r "Command\|Handler" src/
grep -r "Query\|Handler" src/
grep -r "@CommandHandler\|@QueryHandler" src/  # NestJS CQRS
```

---

### Pattern 5: Microkernel (Plugin Architecture)

**Description:** Core system with pluggable modules

**Component structure:**
```
src/
├── core/                    # Core System
│   ├── Application.ts
│   ├── PluginManager.ts
│   └── interfaces/
│       └── Plugin.interface.ts
└── plugins/                 # Plugins
    ├── authentication/
    │   ├── AuthPlugin.ts
    │   └── AuthService.ts
    ├── logging/
    │   ├── LoggingPlugin.ts
    │   └── Logger.ts
    └── cache/
        ├── CachePlugin.ts
        └── CacheService.ts
```

**Key concepts:**
- **Core**: Minimal core system
- **Plugins**: Optional modules that extend core
- **Plugin Interface**: Contract for plugins

**Components identified:**
- **Core**: Application, PluginManager
- **Plugins**: AuthPlugin, LoggingPlugin, CachePlugin
- **Plugin Interface**: Plugin.interface.ts

---

### Pattern 6: Event-Driven Architecture

**Description:** Components communicate via events

**Component structure:**
```
src/
├── events/                  # Event Definitions
│   ├── UserCreatedEvent.ts
│   ├── OrderPlacedEvent.ts
│   └── PaymentProcessedEvent.ts
├── publishers/              # Event Publishers
│   ├── UserEventPublisher.ts
│   └── OrderEventPublisher.ts
└── subscribers/             # Event Subscribers
    ├── EmailSubscriber.ts
    ├── AnalyticsSubscriber.ts
    └── NotificationSubscriber.ts
```

**Component flow:**
```
UserService → publishes UserCreatedEvent
                  ↓
    [Event Bus / Message Queue]
                  ↓
EmailSubscriber receives event → sends welcome email
AnalyticsSubscriber receives event → tracks user registration
```

**Components identified:**
- **Event Publishers**: UserEventPublisher, OrderEventPublisher
- **Event Subscribers**: EmailSubscriber, AnalyticsSubscriber, NotificationSubscriber
- **Events**: UserCreatedEvent, OrderPlacedEvent, PaymentProcessedEvent
- **Event Bus**: EventEmitter, Message Queue

**Detection:**
```bash
grep -r "Event\|emit\|publish\|subscribe" src/
grep -r "@OnEvent\|@Subscribe" src/  # Framework decorators
```

---

## Integration with Melly Workflow

### When This Skill is Used

This skill is activated during:

1. **Phase 3: C3 Component Identification** (`/melly-c3-components`)
   - Primary usage phase
   - Component identification within containers
   - Responsibility analysis
   - Dependency mapping
   - Pattern detection

2. **Phase 5: Documentation** (`/melly-doc-c4model`)
   - Markdown generation
   - Component documentation
   - Observation documentation

### Input Expectations

This skill expects data from `c2-containers.json`:

```json
{
  "metadata": { ... },
  "containers": [
    {
      "id": "backend-api",
      "name": "Backend API",
      "type": "api-service",
      "system_id": "ecommerce-system",
      "path": "/repos/backend",
      "technology": {
        "runtime": "Node.js",
        "framework": "NestJS",
        "language": "TypeScript"
      },
      "structure": {
        "entry_point": "src/main.ts",
        "source_directory": "src/",
        "build_output": "dist/"
      }
    }
  ]
}
```

### Output Format

This skill helps generate `c3-components.json`:

```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "generator": "melly-workflow",
    "generated_by": "c3-abstractor",
    "timestamp": "2025-11-17T10:30:00.000Z",
    "melly_version": "1.0.0",
    "parent_timestamp": "2025-11-17T10:20:00.000Z"
  },
  "components": [
    {
      "id": "user-controller",
      "name": "User Controller",
      "type": "controller",
      "container_id": "backend-api",
      "path": "src/users/user.controller.ts",
      "description": "Handles HTTP requests for user management operations",
      "responsibilities": [
        "Validate incoming HTTP requests",
        "Route requests to UserService",
        "Transform service responses to HTTP responses",
        "Handle authentication and authorization"
      ],
      "layer": "presentation",
      "dependencies": [
        {
          "target": "user-service",
          "type": "internal",
          "purpose": "Delegates business logic to UserService"
        }
      ],
      "observations": [ ... ],
      "relations": [ ... ],
      "metrics": {
        "lines_of_code": 150,
        "cyclomatic_complexity": 6,
        "public_methods": 5,
        "dependencies_count": 2
      }
    }
  ],
  "summary": {
    "total_components": 24,
    "by_type": {
      "controller": 4,
      "service": 6,
      "repository": 4,
      "model": 5,
      "middleware": 3,
      "utility": 2
    },
    "by_layer": {
      "presentation": 7,
      "business": 10,
      "data": 7
    }
  }
}
```

### Validation

Generated output must pass:

1. **Schema validation** - Correct JSON structure
2. **Timestamp ordering** - metadata.timestamp > parent_timestamp
3. **Referential integrity** - All dependency targets exist
4. **Required fields** - All required fields present
5. **ID format** - Kebab-case pattern
6. **Container reference** - All container_id values exist in c2-containers.json

Validation script:
```bash
python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json
```

---

## Step-by-Step Workflow

### When Invoked by c3-abstractor Agent

Follow this systematic approach:

#### Step 1: Load Input Data
```bash
# Load c2-containers.json
cat c2-containers.json | jq '.containers'
```

#### Step 2: Analyze Each Container

For each container:

1. **Navigate to container path**
   ```bash
   cd /repos/backend
   ls -la src/
   ```

2. **Understand directory structure**
   ```bash
   tree src/ -L 3 -I 'node_modules|test|*.spec.ts'
   ```

3. **Identify component organization pattern**
   - Feature-based?
   - Layer-based?
   - Domain-driven?

#### Step 3: Identify Components

For each potential component:

1. **Analyze file/directory**
   ```bash
   # Read component file
   cat src/users/user.service.ts

   # Count lines
   wc -l src/users/user.service.ts

   # Find public methods
   grep -E "^\s+(public|async)\s+\w+\s*\(" src/users/user.service.ts
   ```

2. **Determine component type**
   - Controller, Service, Repository, Model, etc.

3. **Extract responsibilities**
   - What does it do?
   - What methods does it expose?

4. **Identify dependencies**
   ```bash
   grep "^import" src/users/user.service.ts
   ```

#### Step 4: Map Component Dependencies

For each component:

1. **Find internal dependencies**
   ```bash
   # Dependencies within same container
   grep "from '\.\./.*'" src/users/user.service.ts
   ```

2. **Find external dependencies**
   ```bash
   # Dependencies from npm packages
   grep "from '[^.].*'" src/users/user.service.ts
   ```

3. **Document dependency relationships**
   - What does it depend on?
   - Why does it depend on it?
   - What type of dependency?

#### Step 5: Detect Patterns

1. **Search for design patterns**
   ```bash
   # Singleton
   grep -r "private static.*instance\|getInstance()" src/

   # Factory
   grep -r "Factory\|static create" src/

   # Repository
   grep -r "Repository.*findById\|findAll" src/

   # Dependency Injection
   grep -r "@Injectable\|@Inject\|constructor.*private" src/
   ```

2. **Identify architectural pattern**
   - MVC? Layered? Hexagonal? CQRS?

#### Step 6: Generate Observations

For each component:

1. **Code structure observations**
   - How is code organized?
   - Is structure clear?

2. **Design pattern observations**
   - What patterns are used?
   - Why are they used?

3. **Dependency observations**
   - High coupling?
   - Circular dependencies?

4. **Complexity observations**
   - High cyclomatic complexity?
   - Large files?

5. **Quality observations**
   - Test coverage?
   - Documentation?

#### Step 7: Calculate Metrics

For each component:

```bash
# Lines of code
wc -l src/users/user.service.ts

# Cyclomatic complexity (requires tool)
npx ts-complexity src/users/user.service.ts

# Dependency count
grep -c "^import" src/users/user.service.ts

# Public methods count
grep -cE '^\s+(public|async)' src/users/user.service.ts
```

#### Step 8: Validate Output

Before finalizing:

1. **Check component IDs**
   - All kebab-case
   - All unique

2. **Check container references**
   - All container_id values exist in c2-containers.json

3. **Check dependencies**
   - All target components exist

4. **Check timestamps**
   - Child > parent

5. **Run validation script**
   ```bash
   python plugins/melly-validation/scripts/validate-c3-components.py output.json
   ```

---

## Best Practices Summary

### ✅ DO:

1. **Identify significant components only**
   - Focus on major building blocks
   - Avoid listing every single file

2. **Use clear component names**
   - "User Service" not "userService.ts"
   - Focus on responsibility, not filename

3. **Define single responsibility**
   - Each component should have one clear purpose

4. **Document dependencies clearly**
   - Internal vs external
   - Purpose of each dependency

5. **Detect design patterns**
   - Singleton, Factory, Repository, etc.
   - Document pattern usage

6. **Analyze code structure**
   - Feature-based? Layer-based?
   - Document organization pattern

7. **Calculate metrics**
   - LOC, complexity, dependency count
   - Use metrics to identify significant components

8. **Check for layer violations**
   - Controllers should not call Repositories directly
   - Respect layer boundaries

9. **Identify circular dependencies**
   - Use tools to detect cycles
   - Document and flag as warnings

10. **Provide evidence in observations**
    - Code snippets
    - File paths
    - Metrics

### ❌ DON'T:

1. **Don't list every file as a component**
   - ❌ Every utility function
   - ✅ Significant modules only

2. **Don't use file names as component names**
   - ❌ "user.service.ts"
   - ✅ "User Service"

3. **Don't ignore component responsibilities**
   - Always define what component does

4. **Don't skip dependency analysis**
   - Dependencies reveal architecture

5. **Don't overlook design patterns**
   - Patterns indicate architectural decisions

6. **Don't ignore metrics**
   - Metrics help identify refactoring needs

7. **Don't document test files as components**
   - Tests verify components, aren't components

8. **Don't mix abstraction levels**
   - Keep C3 focused on components, not individual functions (C4)

9. **Don't skip validation**
   - Always validate generated JSON

10. **Don't ignore circular dependencies**
    - Flag and document circular dependencies

---

## Troubleshooting

### Problem: Too Many Components Identified

**Symptom:** 100+ components for a small API

**Solution:** You're being too granular. Focus on significant components:
- Group small utilities into single "Utility" component
- Combine related files into component modules
- Use LOC threshold (>200 LOC = component)

### Problem: Can't Determine Component Type

**Symptom:** Unclear if file is controller, service, or something else

**Solution:** Analyze the code:
- Does it handle HTTP requests? → Controller
- Does it contain business logic? → Service
- Does it access database? → Repository
- Look for naming conventions (UserController, UserService)

### Problem: Circular Dependencies Detected

**Symptom:** UserService → OrderService → UserService

**Solution:**
- Document as warning observation
- Suggest refactoring:
  - Extract shared logic to third component
  - Use events instead of direct calls
  - Refactor to remove circular reference

### Problem: Missing Responsibilities

**Symptom:** Can't determine what component does

**Solution:** Analyze:
- Read public methods
- Check method names (create, update, delete → CRUD operations)
- Look at dependencies (what it uses reveals what it does)
- Read class/file comments

### Problem: No Design Patterns Detected

**Symptom:** Can't find any patterns

**Solution:** Look for:
- Dependency injection (constructor parameters)
- Repository pattern (findById, findAll, save methods)
- Factory pattern (create methods)
- Singleton pattern (getInstance)
- Use grep commands from Pattern Detection section

### Problem: Can't Calculate Metrics

**Symptom:** No tools available for complexity analysis

**Solution:**
- Use simple LOC counting: `wc -l file.ts`
- Count methods manually: `grep -cE '^\s+(public|async)' file.ts`
- Count dependencies: `grep -c "^import" file.ts`
- Document what you can measure

---

## Quick Reference

### Component Type Checklist

- [ ] `controller` - HTTP request handlers
- [ ] `service` - Business logic
- [ ] `repository` - Data access
- [ ] `model` - Data models/entities
- [ ] `middleware` - Request/response processing
- [ ] `utility` - Helper functions
- [ ] `dto` - Data transfer objects
- [ ] `adapter` - External integrations
- [ ] `factory` - Object creation
- [ ] `validator` - Validation logic
- [ ] `facade` - Simplified interfaces
- [ ] `guard` - Authorization/authentication

### Layer Checklist

- [ ] `presentation` - Controllers, Middleware, DTOs
- [ ] `business` - Services, Domain Models, Validators
- [ ] `data` - Repositories, Database Models
- [ ] `integration` - Adapters, External Service Clients

### Design Pattern Checklist

- [ ] Singleton - Single instance
- [ ] Factory - Object creation
- [ ] Repository - Data access abstraction
- [ ] Dependency Injection - External dependencies
- [ ] Observer - Event-driven
- [ ] Strategy - Algorithm selection
- [ ] Decorator - Dynamic behavior
- [ ] Adapter - Interface conversion

### Architectural Pattern Checklist

- [ ] MVC - Model-View-Controller
- [ ] Layered - 3-tier architecture
- [ ] Hexagonal - Ports & Adapters
- [ ] CQRS - Command Query Responsibility Segregation
- [ ] Microkernel - Plugin architecture
- [ ] Event-Driven - Event-based communication

### Observation Category Checklist

- [ ] `code-structure` - Organization patterns
- [ ] `design-patterns` - Patterns identified
- [ ] `dependencies` - Component dependencies
- [ ] `complexity` - Code metrics
- [ ] `coupling` - Coupling analysis
- [ ] `cohesion` - Cohesion analysis
- [ ] `testing` - Test coverage
- [ ] `documentation` - Documentation quality

### Metrics Checklist

- [ ] Lines of Code (LOC)
- [ ] Cyclomatic Complexity
- [ ] Number of Dependencies
- [ ] Number of Public Methods
- [ ] Afferent Coupling (Ca)
- [ ] Efferent Coupling (Ce)
- [ ] Instability (I = Ce / (Ca + Ce))

---

## Examples and Templates

See these files for complete examples:

- **Template**: `/plugins/melly-validation/templates/c3-components-template.json`
- **Schema**: `/docs/json-schemas-design.md`
- **Methodology**: `/docs/c4model-methodology.md`
- **Workflow**: `/docs/workflow-guide.md`

---

## Technology-Specific Examples

### NestJS Example

**Component identification in NestJS backend:**

```typescript
// src/users/user.controller.ts
@Controller('users')
export class UserController {           // Component: User Controller (controller)
  constructor(private userService: UserService) {}

  @Post()
  create(@Body() dto: CreateUserDto) {
    return this.userService.create(dto);
  }
}

// src/users/user.service.ts
@Injectable()
export class UserService {              // Component: User Service (service)
  constructor(private userRepo: UserRepository) {}

  async create(dto: CreateUserDto) {
    return this.userRepo.save(dto);
  }
}

// src/users/user.repository.ts
@Injectable()
export class UserRepository {           // Component: User Repository (repository)
  constructor(@InjectRepository(User) private repo: Repository<User>) {}

  async save(data: CreateUserDto) {
    return this.repo.save(data);
  }
}
```

**Components:**
1. **User Controller** (controller) - Handles HTTP requests
2. **User Service** (service) - Business logic
3. **User Repository** (repository) - Data access

**Patterns:**
- Dependency Injection (@Injectable, constructor injection)
- Repository Pattern (UserRepository)
- Layered Architecture (Controller → Service → Repository)

---

### Django Example (Python)

**Component identification in Django backend:**

```python
# users/views.py
class UserViewSet(viewsets.ModelViewSet):     # Component: User ViewSet (controller)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = UserService.create_user(serializer.validated_data)
            return Response(UserSerializer(user).data)

# users/services.py
class UserService:                            # Component: User Service (service)
    @staticmethod
    def create_user(data):
        # Business logic
        user = User.objects.create(**data)
        EmailService.send_welcome(user)
        return user

# users/models.py
class User(models.Model):                     # Component: User Model (model)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
```

**Components:**
1. **User ViewSet** (controller) - Handles HTTP requests
2. **User Service** (service) - Business logic
3. **User Model** (model) - Data model

---

### Spring Boot Example (Java)

**Component identification in Spring Boot backend:**

```java
// UserController.java
@RestController
@RequestMapping("/users")
public class UserController {                 // Component: User Controller (controller)
    @Autowired
    private UserService userService;

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody CreateUserDto dto) {
        User user = userService.createUser(dto);
        return ResponseEntity.ok(user);
    }
}

// UserService.java
@Service
public class UserService {                    // Component: User Service (service)
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;

    public User createUser(CreateUserDto dto) {
        User user = new User(dto);
        userRepository.save(user);
        emailService.sendWelcome(user);
        return user;
    }
}

// UserRepository.java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {  // Component: User Repository (repository)
    Optional<User> findByEmail(String email);
}
```

**Components:**
1. **User Controller** (controller) - HTTP request handling
2. **User Service** (service) - Business logic
3. **User Repository** (repository) - Data access

**Patterns:**
- Dependency Injection (@Autowired)
- Repository Pattern (Spring Data JPA)
- Layered Architecture

---

### React Example (Frontend)

**Component identification in React frontend:**

```typescript
// src/features/users/UserList.tsx
export function UserList() {                  // Component: User List (page/screen)
  const { users, loading } = useUsers();

  return (
    <div>
      {users.map(user => <UserCard key={user.id} user={user} />)}
    </div>
  );
}

// src/features/users/hooks/useUsers.ts
export function useUsers() {                  // Component: User Hook (state management)
  const [users, setUsers] = useState([]);

  useEffect(() => {
    UserService.fetchUsers().then(setUsers);
  }, []);

  return { users, loading };
}

// src/services/UserService.ts
export class UserService {                    // Component: User Service (service)
  static async fetchUsers() {
    const response = await api.get('/users');
    return response.data;
  }

  static async createUser(data: CreateUserDto) {
    const response = await api.post('/users', data);
    return response.data;
  }
}
```

**Components:**
1. **User List** (page) - UI component
2. **useUsers Hook** (state-management) - State management
3. **User Service** (service) - API client

---

## Summary

You now have comprehensive knowledge of C4 Model Level 3 (Component) methodology. When invoked:

1. **Load input data** from `c2-containers.json`
2. **Analyze each container** to understand structure
3. **Identify components** using file structure and code analysis
4. **Classify components** by type (controller, service, repository, etc.)
5. **Define responsibilities** for each component
6. **Map dependencies** between components
7. **Detect patterns** (design patterns and architectural patterns)
8. **Generate observations** with evidence
9. **Calculate metrics** (LOC, complexity, dependencies)
10. **Validate output** before finalizing

Remember: **C3 is about code structure.** Focus on WHAT code components exist, WHAT they do, and HOW they interact - not the implementation details of individual functions (that's C4).

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-11-17
**Compatibility**: Melly 1.0.0+
