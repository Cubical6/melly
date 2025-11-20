# Component Identification Methodology

This guide provides comprehensive methodology for identifying components at the C3 (Component) level of the C4 Model.

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
find src -name "*.ts" -print0 | xargs -0 -r wc -l | sort -rn

# Components with > 200 LOC are significant
find src -name "*.ts" -print0 | xargs -0 -r wc -l | awk '$1 > 200 { print $2, $1 }'
```

**Guidelines:**
- **< 100 LOC**: Small component or helper
- **100-300 LOC**: Typical component
- **300-500 LOC**: Large component (consider splitting)
- **> 500 LOC**: Very large (definitely a component, likely needs refactoring)

#### Metric 2: Cyclomatic Complexity
```bash
# Use complexity tools
find src -name "*.ts" -print0 | xargs -0 -r npx ts-complexity

# High complexity (>10) indicates important component
```

#### Metric 3: Dependency Count
```bash
# Count imports per file
find src -name "*.ts" -print0 | xargs -0 -r grep -cH "^import" 2>/dev/null | sort -t: -k2 -rn

# Files with many imports are often important orchestrators (Services)
```

#### Metric 4: Export Count
```bash
# Count exports per file
find src -name "*.ts" -print0 | xargs -0 -r grep -cH "^export" 2>/dev/null | sort -t: -k2 -rn

# Files with many exports are often facades or utility modules
```
