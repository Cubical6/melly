# C4 Model Abstractions

> Understanding the four levels of abstraction in the C4 model

## The Abstraction Hierarchy

The C4 model uses a hierarchical structure where each level zooms into more detail:

```
System Context (Level 1)
    ↓ zoom in
Container (Level 2)
    ↓ zoom in
Component (Level 3)
    ↓ zoom in
Code (Level 4)
```

Each level serves a specific purpose and audience, allowing you to communicate at the appropriate level of detail.

---

## Level 1: System Context

### What Is It?

The **System Context** diagram shows the big picture - how your software system fits into the world around it.

**Think of it as**: A map showing your system and everything it interacts with.

### What Does It Show?

- **Your software system** (as a single box)
- **People** (users/actors/roles/personas)
- **External systems** (other software systems your system depends on or interacts with)
- **Relationships** (how they interact)

### What It Doesn't Show

- Internal details of your system
- Technology choices
- Implementation details

### Example Elements

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [Person: Customer]                                 │
│  "Uses the system to                                │
│   place orders"                                     │
│         │                                           │
│         ↓ Places orders using                       │
│  ┌──────────────┐                                   │
│  │  E-Commerce  │──→ Sends email ──→ [Email System] │
│  │   System     │                                   │
│  │ (Your system)│──→ Processes ───→ [Payment Gateway]│
│  └──────────────┘       payments                    │
│         ↑                                           │
│         │ Manages inventory                         │
│  [Person: Admin]                                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Audience

- ✅ **Everyone** - technical and non-technical stakeholders
- Business stakeholders
- Project managers
- Developers
- Architects
- New team members

### When to Create

- ✅ **Always** - This should be your starting point
- Beginning of a project
- When onboarding new team members
- When explaining the system to stakeholders
- Architecture review sessions

### Benefits

1. **Establishes scope**: What's inside vs outside your system
2. **Identifies dependencies**: What external systems you rely on
3. **Shows users**: Who interacts with the system
4. **Creates common understanding**: Everyone can understand this diagram

### Key Questions It Answers

- Who uses the system?
- What other systems does it interact with?
- What is the system boundary?
- What are the main external dependencies?

---

## Level 2: Container

### What Is It?

The **Container** diagram zooms into your software system and shows the high-level technology choices.

**Important**: "Container" here means **any separately runnable/deployable unit**, not just Docker containers!

### What Is a Container?

A container represents something that:
- Executes code or stores data
- Needs to be running for the system to work
- Is independently deployable

**Examples of containers**:
- ✅ Web application (e.g., Spring Boot app)
- ✅ Single-page application (e.g., React app)
- ✅ Mobile app (e.g., iOS app)
- ✅ Database (e.g., PostgreSQL)
- ✅ File system
- ✅ Microservice
- ✅ Serverless function
- ✅ Desktop application

### What Does It Show?

- **Containers** within your software system
- **Technology choices** for each container
- **Communication** between containers
- **Data stores**
- **Major structural building blocks**

### Example Elements

```
System: E-Commerce System
┌─────────────────────────────────────────────────┐
│                                                 │
│  [Web Application]                              │
│  Spring Boot, Java                              │
│  "Delivers static content                       │
│   and e-commerce SPA"                           │
│         │                                       │
│         ↓ Makes API calls [HTTPS/JSON]          │
│  [API Application]                              │
│  Spring Boot, Java                              │
│  "Provides e-commerce                           │
│   functionality via API"                        │
│         │                                       │
│         ↓ Reads/Writes [JDBC]                   │
│  [Database]                                     │
│  PostgreSQL                                     │
│  "Stores user accounts,                         │
│   products, orders"                             │
│                                                 │
│  [Single Page Application]                      │
│  React, JavaScript                              │
│  "Provides e-commerce                           │
│   functionality to customers"                   │
│         │                                       │
│         └────→ Makes API calls to ──→ [API Application]
│                                                 │
└─────────────────────────────────────────────────┘
```

### Audience

- ✅ **Technical people** primarily
- Software developers
- Software architects
- Operations/support staff
- Technical project managers

### When to Create

- ✅ **Very commonly** - Most teams create this
- After System Context
- When making technology decisions
- Planning deployment architecture
- Technical onboarding
- Architecture reviews

### Benefits

1. **Shows high-level technology choices**: What tech stack is used
2. **Identifies deployment units**: What needs to be deployed
3. **Illustrates communication paths**: How containers interact
4. **Maps to DevOps concerns**: CI/CD, monitoring, scaling

### Key Questions It Answers

- What are the major structural building blocks?
- What technology is used for each part?
- How do the parts communicate?
- What needs to be deployed separately?
- Where is data stored?

---

## Level 3: Component

### What Is It?

The **Component** diagram zooms into an individual container and shows its internal structure.

### What Is a Component?

A component is a grouping of related functionality with:
- A well-defined interface
- Clear responsibility
- Encapsulated implementation

**Examples of components**:
- ✅ Group of related classes/modules
- ✅ Service layer
- ✅ Repository layer
- ✅ Controller
- ✅ Business logic module
- ✅ Integration adapter

**Not components**:
- ❌ Individual classes (too low level)
- ❌ Functions (too low level)
- ❌ Separate containers (wrong level)

### What Does It Show?

- **Components** within a container
- **Component responsibilities**
- **Interactions** between components
- **Architectural patterns** (e.g., layering, hexagonal)
- **Technology/frameworks** used

### Example Elements

```
Container: API Application (Spring Boot)
┌─────────────────────────────────────────────────┐
│                                                 │
│  [OrderController]                              │
│  Spring MVC Rest Controller                     │
│  "Provides order management                     │
│   via REST API"                                 │
│         │                                       │
│         ↓ Uses                                  │
│  [OrderService]                                 │
│  Spring Bean                                    │
│  "Business logic for order                      │
│   processing and validation"                    │
│         │                                       │
│         ↓ Uses                                  │
│  [OrderRepository]                              │
│  Spring Data JPA Repository                     │
│  "Provides data access                          │
│   for orders"                                   │
│         │                                       │
│         ↓ Uses                                  │
│  [Database] (from Container diagram)            │
│                                                 │
│  [PaymentGatewayAdapter]                        │
│  Spring Component                               │
│  "Integrates with external                      │
│   payment provider"                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Audience

- ✅ **Developers and architects**
- Software developers on the team
- Software architects
- Technical leads

### When to Create

- ⚠️ **Selectively** - Not for every container
- For complex containers
- When planning major refactoring
- Explaining architecture to new developers
- Architecture reviews for specific areas
- When container is being developed by multiple teams

### When NOT to Create

- ❌ Simple containers (e.g., database)
- ❌ When codebase is self-explanatory
- ❌ Small microservices (might be over-engineering)

### Benefits

1. **Shows internal structure**: How container is organized
2. **Identifies separation of concerns**: Layering, boundaries
3. **Highlights design patterns**: MVC, hexagonal, etc.
4. **Guides implementation**: What components to build

### Key Questions It Answers

- How is this container structured internally?
- What are the major components?
- How do components interact?
- What patterns are we using?
- Where should new functionality go?

---

## Level 4: Code

### What Is It?

The **Code** diagram shows how a component is implemented using code elements.

**Reality check**: This level is often **skipped** because:
- IDEs can generate this automatically
- UML class diagrams serve this purpose
- It's too detailed to maintain manually
- Code is the source of truth

### What Does It Show?

- **Classes** and interfaces
- **Methods** and properties
- **Relationships** (inheritance, composition, dependencies)
- **Implementation details**

### Example Elements

```
Component: OrderService
┌─────────────────────────────────────────────────┐
│                                                 │
│  <<interface>>                                  │
│  IOrderService                                  │
│  + createOrder(order: Order): OrderResult       │
│  + getOrder(id: string): Order                  │
│  + cancelOrder(id: string): void                │
│         △                                       │
│         │ implements                            │
│  OrderServiceImpl                               │
│  - orderRepository: IOrderRepository            │
│  - paymentGateway: IPaymentGateway             │
│  - emailService: IEmailService                  │
│  + createOrder(order: Order): OrderResult       │
│  + getOrder(id: string): Order                  │
│  + cancelOrder(id: string): void                │
│  - validateOrder(order: Order): bool            │
│  - processPayment(order: Order): PaymentResult  │
│         │                                       │
│         ↓ uses                                  │
│  Order                                          │
│  + id: string                                   │
│  + customerId: string                           │
│  + items: OrderItem[]                           │
│  + total: number                                │
│  + status: OrderStatus                          │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Audience

- ✅ **Developers only**
- Individual developers
- Code reviewers

### When to Create

- ⚠️ **Rarely**
- Complex algorithms or patterns
- Architecture documentation requiring this detail
- When automatically generated from code
- Teaching/training scenarios

### When NOT to Create

- ❌ Most of the time!
- ❌ When IDEs can show this
- ❌ When code is self-documenting
- ❌ For maintenance (it gets outdated quickly)

### Benefits

1. **Very detailed view**: Shows exact implementation
2. **Can be auto-generated**: Tools can create from code
3. **Teaching tool**: Good for understanding patterns

### Limitations

1. **High maintenance**: Gets outdated quickly
2. **Limited audience**: Only developers
3. **Redundant**: Code itself is the documentation
4. **Time-consuming**: Takes time to create and maintain

### Key Questions It Answers

- What classes implement this component?
- How are they related (inheritance, composition)?
- What are the key methods?
- What design patterns are used?

---

## Abstraction Levels Comparison

| Aspect | Level 1: Context | Level 2: Container | Level 3: Component | Level 4: Code |
|--------|-----------------|-------------------|-------------------|---------------|
| **Zoom** | 🔍 Highest | 🔍🔍 High | 🔍🔍🔍 Medium | 🔍🔍🔍🔍 Lowest |
| **Scope** | System + environment | Inside system | Inside container | Inside component |
| **Elements** | System, people, external systems | Containers (apps, DBs) | Components (modules) | Classes, interfaces |
| **Technology** | Hidden | Shown (tech stack) | Shown (frameworks) | Shown (code details) |
| **Audience** | Everyone | Technical people | Developers/architects | Developers |
| **Frequency** | ✅ Always create | ✅ Usually create | ⚠️ Sometimes create | ❌ Rarely create |
| **Detail Level** | Very low | Low-medium | Medium-high | Very high |
| **Maintenance** | Easy | Easy | Moderate | Difficult |

---

## Choosing the Right Level

### Decision Tree

```
Do you need to show the system in its environment?
    ├─ Yes → System Context diagram
    └─ No ↓

Do you need to show high-level technology choices?
    ├─ Yes → Container diagram
    └─ No ↓

Do you need to show internal structure of a container?
    ├─ Yes → Component diagram
    └─ No ↓

Do you need to show implementation details?
    ├─ Yes → Code diagram (or just look at the code!)
    └─ No → You're done!
```

### Common Combinations

**Most projects**: Context + Container
- Sufficient for most teams
- Covers both big picture and technical architecture
- Easy to maintain

**Complex projects**: Context + Container + Component (for key containers)
- Shows internal structure where needed
- Balances detail with maintainability

**Rare cases**: All four levels
- Very complex systems
- Regulatory requirements
- Extensive documentation needs

---

## The Relationship Between Levels

### Hierarchical Containment

```
┌─ System Context ────────────────────────────────────┐
│                                                     │
│  [Your System]                                      │
│  ┌─ Container ────────────────────────────┐         │
│  │                                        │         │
│  │  [Web App] [API] [Database]            │         │
│  │     │                                  │         │
│  │     └─ Component ─────────────┐        │         │
│  │        │                      │        │         │
│  │        [Controller] [Service] │        │         │
│  │           │                   │        │         │
│  │           └─ Code ──────┐     │        │         │
│  │              │          │     │        │         │
│  │              [Classes]  │     │        │         │
│  │              └──────────┘     │        │         │
│  │              └────────────────┘        │         │
│  └─────────────────────────────────────────┘         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Zooming Metaphor

Think of it like Google Maps:
- **System Context**: Country/region level (see major cities and borders)
- **Container**: City level (see neighborhoods and major roads)
- **Component**: Neighborhood level (see individual streets)
- **Code**: Building level (see individual rooms and layout)

---

## Best Practices

### Do ✅

1. **Start with System Context** - Always begin at the highest level
2. **Create Container diagrams** - For nearly all systems
3. **Be selective with Component diagrams** - Only where they add value
4. **Skip Code diagrams** - Unless you have a specific reason
5. **Use consistent terminology** - Stick to "container", "component", etc.
6. **Keep diagrams simple** - Don't overcrowd with details
7. **Use titles** - Make it clear which level you're showing

### Don't ❌

1. **Don't mix levels** - Keep each diagram at one abstraction level
2. **Don't create all levels** - Only create what adds value
3. **Don't show too much detail** - Simplify, simplify, simplify
4. **Don't forget the audience** - Match detail to who will read it
5. **Don't let diagrams get stale** - Update or delete outdated diagrams
6. **Don't use C4 for everything** - It's for software architecture, not processes

---

## Examples for Different System Types

### Monolithic Web Application

- ✅ **System Context**: Shows web app, users, external APIs
- ✅ **Container**: Shows web server, database, maybe cache
- ⚠️ **Component**: Maybe for the application container
- ❌ **Code**: Probably skip

### Microservices Architecture

- ✅ **System Context**: Shows entire system, users, external systems
- ✅ **Container**: Shows all microservices, databases, message queues
- ⚠️ **Component**: For complex microservices only
- ❌ **Code**: Probably skip

### Mobile Application

- ✅ **System Context**: Shows mobile app, backend, external services
- ✅ **Container**: Shows mobile app, backend API, database
- ⚠️ **Component**: For complex apps with many features
- ❌ **Code**: Probably skip

---

## Summary

The C4 model's abstraction levels provide a **flexible framework** for communicating software architecture:

1. **System Context** (Level 1): The big picture - always create this
2. **Container** (Level 2): High-level technology - create for most systems
3. **Component** (Level 3): Internal structure - create selectively
4. **Code** (Level 4): Implementation details - rarely needed

**Golden Rule**: Create the minimum number of diagrams that effectively communicate your architecture.

Focus on **System Context** and **Container** diagrams for most needs. Add **Component** diagrams only where they provide clear value. Skip **Code** diagrams unless you have a compelling reason.

---

**Next**:
- See [Reverse Engineering Guide](reverse-engineering-guide.md) to learn how to apply these abstractions to understand existing systems
- Review [Diagram Types](diagram-types.md) for detailed guidance on creating each type of diagram
