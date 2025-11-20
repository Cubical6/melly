# Pattern Detection

This guide provides comprehensive methodology for detecting design patterns and architectural patterns at the C3 level.

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
grep -rE "findById|findAll|save.*Promise" src/
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
grep -rE "@Injectable|@Inject" src/

# Spring
grep -rE "@Service|@Autowired|@Component" src/

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
grep -rE "\.emit|\.on|@OnEvent|subscribe|publish" src/
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
grep -rE "implements.*Strategy|Strategy.*interface" src/
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
grep -rE "^@\w+\(" src/
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
grep -rE "Command|Handler" src/
grep -rE "Query|Handler" src/
grep -rE "@CommandHandler|@QueryHandler" src/  # NestJS CQRS
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
grep -rE "Event|emit|publish|subscribe" src/
grep -rE "@OnEvent|@Subscribe" src/  # Framework decorators
```
