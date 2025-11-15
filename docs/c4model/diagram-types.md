# C4 Diagram Types Reference

> Complete guide to all C4 diagram types with notation and examples

## Overview

The C4 model includes **7 diagram types**:

**Core diagrams** (hierarchical):
1. System Context
2. Container
3. Component
4. Code

**Supplementary diagrams** (cross-cutting):
5. System Landscape
6. Dynamic
7. Deployment

This guide covers each type in detail.

---

## Core Diagrams

### 1. System Context Diagram

#### Purpose
Shows how your software system fits into the world - the big picture.

#### Audience
- ✅ Everyone (technical and non-technical)
- Business stakeholders
- Project managers
- Developers
- Architects

#### Scope
- **Focus**: Single software system
- **Shows**: System boundary and external dependencies
- **Abstraction**: Very high level

#### Elements

| Element | Notation | Description |
|---------|----------|-------------|
| **Software System** (yours) | `[System Name]` | The system you're documenting |
| **Person** | `[Person: Role]` | A human user (role or persona) |
| **External System** | `[External System Name]` | Another software system |
| **Relationship** | `→` with label | How elements interact |

#### Example

```
┌────────────────────────────────────────────────┐
│                                                │
│  [Person: Customer]                            │
│  "A customer of the                            │
│   online store"                                │
│         │                                      │
│         ↓ Views products, places orders        │
│         │ [HTTPS]                              │
│  ┌──────────────────┐                          │
│  │  E-Commerce      │                          │
│  │  System          │──→ Sends emails [SMTP]  │
│  │                  │    [Email System]        │
│  │ "Allows customers│                          │
│  │  to browse and   │──→ Processes payments   │
│  │  purchase        │    [HTTPS]              │
│  │  products"       │    [Payment Gateway]    │
│  └──────────────────┘                          │
│         ↑                                      │
│         │ Manages products                     │
│         │ [HTTPS]                              │
│  [Person: Admin]                               │
│  "Manages the store"                           │
│                                                │
└────────────────────────────────────────────────┘
```

#### Best Practices

**Do** ✅:
- Show all external dependencies
- Include all user types/personas
- Label relationships clearly
- Use business language (avoid technical jargon)
- Keep it simple (one page)

**Don't** ❌:
- Show internal structure (that's Container level)
- Include too many details
- Use technical protocols (unless important for context)
- Show multiple systems (use System Landscape instead)

#### When to Create
- ✅ **Always** - This should be your first diagram
- Start of every project
- Onboarding new team members
- Explaining to stakeholders

---

### 2. Container Diagram

#### Purpose
Shows the high-level technology choices and how containers communicate.

#### Audience
- ✅ Technical people primarily
- Software developers
- Software architects
- DevOps/operations
- Technical project managers

#### Scope
- **Focus**: Single software system (zoom into System Context)
- **Shows**: Major structural building blocks
- **Abstraction**: High level

#### Elements

| Element | Notation | Description |
|---------|----------|-------------|
| **Container** | `[Container Name]`<br>`Technology` | Separately runnable/deployable unit |
| **Person** | `[Person: Role]` | Carried over from System Context |
| **External System** | `[External System]` | Carried over from System Context |
| **Relationship** | `→` with label & protocol | How containers communicate |

#### What Is a Container?

A container represents something that:
- Executes code or stores data
- Must be running for system to work
- Is independently deployable

**Examples**: Web app, API, SPA, mobile app, database, microservice, serverless function

**NOT Docker containers** - the term predates Docker!

#### Example

```
System: E-Commerce System
┌────────────────────────────────────────────────┐
│                                                │
│  [Person: Customer]                            │
│         │                                      │
│         ↓ Uses [HTTPS]                         │
│  ┌─────────────────┐                           │
│  │ Single Page App │                           │
│  │                 │                           │
│  │ React,          │                           │
│  │ TypeScript      │                           │
│  │                 │                           │
│  │ "Provides UI"   │                           │
│  └─────────────────┘                           │
│         │                                      │
│         ↓ Makes API calls [HTTPS/JSON]         │
│  ┌─────────────────┐                           │
│  │ API Application │──→ Sends email [SMTP]    │
│  │                 │    [Email System]         │
│  │ Node.js,        │                           │
│  │ Express         │──→ Processes payments     │
│  │                 │    [HTTPS]                │
│  │ "Business logic"│    [Payment Gateway]      │
│  └─────────────────┘                           │
│         │                                      │
│         ↓ Reads/Writes [PostgreSQL Protocol]   │
│  ┌─────────────────┐                           │
│  │ Database        │                           │
│  │                 │                           │
│  │ PostgreSQL 14   │                           │
│  │                 │                           │
│  │ "Stores user    │                           │
│  │  data, orders"  │                           │
│  └─────────────────┘                           │
│                                                │
└────────────────────────────────────────────────┘
```

#### Best Practices

**Do** ✅:
- Show technology choices (language, framework, database)
- Include protocol/format (HTTPS, JDBC, message queue)
- Group by system boundary
- Show data stores as containers
- Use consistent naming

**Don't** ❌:
- Show internal structure of containers (that's Component level)
- Include too many containers (group/simplify if needed)
- Mix abstraction levels
- Show infrastructure (use Deployment diagram)

#### When to Create
- ✅ **Very common** - Most projects should have this
- After System Context
- When planning architecture
- Making technology decisions
- DevOps planning

---

### 3. Component Diagram

#### Purpose
Shows the internal structure of a container - major components and their interactions.

#### Audience
- ✅ Developers and architects
- Development team
- Technical leads
- Code reviewers

#### Scope
- **Focus**: Single container (zoom into Container)
- **Shows**: Logical components and responsibilities
- **Abstraction**: Medium level

#### Elements

| Element | Notation | Description |
|---------|----------|-------------|
| **Component** | `[Component Name]`<br>`Technology/Type` | Grouping of related functionality |
| **Container** | `[Container Name]` | Other containers it talks to |
| **Relationship** | `→` with label | How components interact |

#### What Is a Component?

A component is a grouping of related functionality:
- Clear responsibility
- Well-defined interface
- Implementation encapsulated

**Examples**: Controller, service layer, repository, adapter, module

**NOT**: Individual classes, functions (too low level)

#### Example

```
Container: API Application (Node.js, Express)
┌────────────────────────────────────────────────┐
│                                                │
│  [OrderController]                             │
│  Express Router                                │
│  "Handles order HTTP requests"                 │
│         │                                      │
│         ↓ Uses                                 │
│  [OrderService]                                │
│  Service Class                                 │
│  "Order business logic"                        │
│         │                                      │
│         ├──→ Uses                              │
│         │   [OrderRepository]                  │
│         │   Data Access Layer                  │
│         │   "Persists orders"                  │
│         │        │                             │
│         │        ↓ Reads/Writes                │
│         │   [Database]                         │
│         │   (Container)                        │
│         │                                      │
│         └──→ Uses                              │
│             [PaymentAdapter]                   │
│             Integration Component              │
│             "Payment gateway client"           │
│                  │                             │
│                  ↓ Calls                       │
│             [Payment Gateway]                  │
│             (External System)                  │
│                                                │
│  [AuthMiddleware]                              │
│  Express Middleware                            │
│  "Handles authentication"                      │
│         │                                      │
│         ↓ Uses                                 │
│  [Auth Service]                                │
│  (External System)                             │
│                                                │
└────────────────────────────────────────────────┘
```

#### Best Practices

**Do** ✅:
- Show architectural layers (presentation, business, data)
- Group by responsibility
- Show key interfaces
- Indicate technology/framework for components
- Keep component count manageable (5-15)

**Don't** ❌:
- Show every class (too detailed)
- Mix with code-level details
- Create for simple containers
- Include utility classes

#### When to Create
- ⚠️ **Selectively** - Not for every container
- Complex containers
- Planning refactoring
- Explaining architecture to team
- Multiple teams working on same container

---

### 4. Code Diagram

#### Purpose
Shows implementation details - classes, interfaces, methods.

#### Audience
- ✅ Developers only
- Individual developers
- Code reviewers

#### Scope
- **Focus**: Single component (zoom into Component)
- **Shows**: Code elements and relationships
- **Abstraction**: Very low level

#### Elements

Standard UML class diagram elements:
- Classes
- Interfaces
- Methods
- Properties
- Relationships (inheritance, composition, dependency)

#### Example

```
Component: OrderService
┌────────────────────────────────────────────────┐
│                                                │
│  <<interface>>                                 │
│  IOrderService                                 │
│  + createOrder(order: Order): Promise<Order>   │
│  + getOrder(id: string): Promise<Order>        │
│  + cancelOrder(id: string): Promise<void>      │
│         △                                      │
│         │ implements                           │
│         │                                      │
│  OrderServiceImpl                              │
│  - orderRepo: IOrderRepository                 │
│  - paymentGateway: IPaymentGateway             │
│  - logger: ILogger                             │
│  + createOrder(order: Order): Promise<Order>   │
│  + getOrder(id: string): Promise<Order>        │
│  + cancelOrder(id: string): Promise<void>      │
│  - validateOrder(order: Order): boolean        │
│  - calculateTotal(items: Item[]): number       │
│         │                                      │
│         ↓ uses                                 │
│  Order                                         │
│  + id: string                                  │
│  + customerId: string                          │
│  + items: OrderItem[]                          │
│  + total: Money                                │
│  + status: OrderStatus                         │
│  + createdAt: Date                             │
│                                                │
│  OrderStatus                                   │
│  <<enumeration>>                               │
│  PENDING                                       │
│  CONFIRMED                                     │
│  SHIPPED                                       │
│  DELIVERED                                     │
│  CANCELLED                                     │
│                                                │
└────────────────────────────────────────────────┘
```

#### Best Practices

**Do** ✅:
- Use IDE to generate (don't draw manually)
- Focus on design patterns if documenting
- Keep it focused (one or two classes)
- Use for teaching/understanding algorithms

**Don't** ❌:
- Create for everything (wasteful)
- Try to keep up to date manually (will get stale)
- Include every method/property (too detailed)
- Use instead of reading code

#### When to Create
- ❌ **Rarely** - Most teams skip this level
- Auto-generated from code
- Teaching design patterns
- Regulatory documentation requirements
- Complex algorithms that need explanation

---

## Supplementary Diagrams

### 5. System Landscape Diagram

#### Purpose
Shows the organizational landscape - multiple systems and how they relate.

#### Audience
- ✅ Technical and business stakeholders
- Enterprise architects
- Business analysts
- Product managers

#### Scope
- **Focus**: Multiple software systems
- **Shows**: Big picture of IT landscape
- **Abstraction**: Very high level (even higher than System Context)

#### Elements

Same as System Context, but showing multiple systems:
- People
- Software systems (multiple!)
- Relationships

#### Example

```
Organization: Retail Company
┌────────────────────────────────────────────────┐
│                                                │
│  [Person: Customer]                            │
│         │                                      │
│         ↓ Uses                                 │
│  ┌─────────────────┐                           │
│  │ E-Commerce      │──→ Queries inventory      │
│  │ System          │    [Inventory System]     │
│  │                 │                           │
│  │ "Online store"  │──→ Creates orders         │
│  └─────────────────┘    [Order Management]    │
│         │                    │                 │
│         │                    ↓ Tracks          │
│         │               [Shipping System]      │
│         │                                      │
│         └──→ Authenticates                     │
│             [Identity Provider]                │
│                  ↑                             │
│                  │ Also used by                │
│  [Person: Employee]                            │
│         │                                      │
│         ↓ Uses                                 │
│  ┌─────────────────┐                           │
│  │ Warehouse       │──→ Updates                │
│  │ Management      │    [Inventory System]     │
│  │ System          │                           │
│  └─────────────────┘──→ Notifies               │
│                        [Shipping System]       │
│                                                │
│  [CRM System] ←── Syncs customer data ──┐      │
│                                         │      │
│                                  [E-Commerce]  │
│                                                │
└────────────────────────────────────────────────┘
```

#### When to Create
- Showing entire IT landscape
- Enterprise architecture documentation
- Understanding system dependencies
- Planning system integration

---

### 6. Dynamic Diagram

#### Purpose
Shows how elements collaborate at runtime for a specific scenario.

#### Audience
- ✅ Technical people
- Developers
- Architects
- Business analysts (for process understanding)

#### Scope
- **Can apply to**: Any C4 level (Context, Container, Component)
- **Shows**: Sequence of interactions
- **Abstraction**: Varies (match the level of static diagram)

#### Notation Styles

**Style 1: Collaboration (numbered steps)**
```
1. Customer → E-Commerce: Place order
2. E-Commerce → Payment Gateway: Process payment
3. Payment Gateway → E-Commerce: Payment confirmed
4. E-Commerce → Email System: Send confirmation
5. E-Commerce → Customer: Order confirmed
```

**Style 2: Sequence (UML-like)**
```
Customer    E-Commerce    Payment    Email
   │            │           │          │
   │─1. Order──→│           │          │
   │            │─2. Pay───→│          │
   │            │←3. OK─────│          │
   │            │─4. Send──────────────→│
   │←5. Confirm─│           │          │
```

#### Example (Container Level)

```
Use Case: Customer places order

┌────────────────────────────────────────────────┐
│                                                │
│  1. Customer submits order                     │
│     [Customer] → [SPA]                         │
│                                                │
│  2. SPA calls create order API                 │
│     [SPA] → [API] POST /orders                 │
│                                                │
│  3. API validates and saves order              │
│     [API] → [Database] INSERT order            │
│                                                │
│  4. API processes payment                      │
│     [API] → [Payment Gateway] POST /charge     │
│                                                │
│  5. Payment confirmed                          │
│     [Payment Gateway] → [API] 200 OK           │
│                                                │
│  6. API sends confirmation email               │
│     [API] → [Email System] POST /send          │
│                                                │
│  7. API returns success to SPA                 │
│     [API] → [SPA] 201 Created                  │
│                                                │
│  8. SPA shows confirmation to customer         │
│     [SPA] → [Customer] "Order confirmed"       │
│                                                │
└────────────────────────────────────────────────┘
```

#### When to Create
- Complex interactions need explanation
- Understanding workflows
- Planning API sequences
- Debugging distributed systems

---

### 7. Deployment Diagram

#### Purpose
Shows how containers map to infrastructure - the physical/virtual environment.

#### Audience
- ✅ Technical people
- DevOps/Operations
- Infrastructure engineers
- Developers (for deployment understanding)

#### Scope
- **Focus**: Deployment architecture
- **Shows**: Infrastructure, deployment units, networking
- **Abstraction**: Physical/virtual infrastructure

#### Elements

| Element | Notation | Description |
|---------|----------|-------------|
| **Deployment Node** | `[Node Name]` | Physical/virtual infrastructure |
| **Container** | `[Container]` | Deployed containers (from Container diagram) |
| **Relationships** | `→` | Network connections, protocols |

#### Deployment Node Types

- Physical hardware
- Virtual machines
- Containers (Docker)
- Kubernetes pods/clusters
- Cloud services (S3, Lambda, etc.)
- CDN
- Load balancers

#### Example

```
Production Environment
┌────────────────────────────────────────────────┐
│                                                │
│  [CDN: Cloudflare]                             │
│  ┌─────────────────┐                           │
│  │ Static Assets   │                           │
│  └─────────────────┘                           │
│         ↓ Routes                               │
│  [AWS: us-east-1]                              │
│    │                                           │
│    ├─ [EC2: Load Balancer]                     │
│    │    │                                      │
│    │    ├─→ [ECS Cluster]                      │
│    │    │    ┌─────────────────┐               │
│    │    │    │ [Container]     │               │
│    │    │    │ API Application │               │
│    │    │    │ (3 instances)   │               │
│    │    │    └─────────────────┘               │
│    │    │         ↓ Connects                   │
│    │    │    [RDS]                             │
│    │    │    ┌─────────────────┐               │
│    │    │    │ PostgreSQL      │               │
│    │    │    │ (Primary +      │               │
│    │    │    │  Read Replica)  │               │
│    │    │    └─────────────────┘               │
│    │    │                                      │
│    │    └─→ [S3 Bucket]                        │
│    │         "Static files, uploads"           │
│    │                                           │
│    └─ [ElastiCache]                            │
│        ┌─────────────────┐                     │
│        │ Redis           │                     │
│        │ (Session cache) │                     │
│        └─────────────────┘                     │
│                                                │
│  [Vercel]                                      │
│  ┌─────────────────┐                           │
│  │ Single Page App │                           │
│  │ (React)         │                           │
│  │ - Edge deployed │                           │
│  └─────────────────┘                           │
│                                                │
└────────────────────────────────────────────────┘
```

#### Best Practices

**Do** ✅:
- Show deployment topology
- Include scaling information (replicas, etc.)
- Show network zones (DMZ, private subnet)
- Indicate protocols and ports
- Show failover/redundancy

**Don't** ❌:
- Show too much infrastructure detail
- Mix with container-level concerns
- Include every configuration detail

#### When to Create
- DevOps planning
- Infrastructure documentation
- Security reviews
- Disaster recovery planning
- Cloud migration planning

---

## Choosing the Right Diagram Type

### Decision Matrix

| Need to show... | Use this diagram |
|----------------|------------------|
| How system fits in the world | System Context |
| Multiple systems in organization | System Landscape |
| Technology choices and structure | Container |
| Internal structure of container | Component |
| Implementation details | Code (or just read code!) |
| Runtime behavior/workflow | Dynamic |
| Infrastructure and deployment | Deployment |

### Common Combinations

**Typical project**:
- ✅ System Context
- ✅ Container
- ⚠️ Component (1-2 diagrams for key containers)
- ⚠️ Dynamic (1-2 for complex flows)

**Microservices**:
- ✅ System Landscape (show all services)
- ✅ System Context (per service)
- ✅ Container (per service - usually simple)
- ✅ Dynamic (for cross-service workflows)
- ✅ Deployment

**Legacy modernization**:
- ✅ System Context (current state)
- ✅ Container (current state)
- ✅ Component (areas to refactor)
- ✅ System Context (future state)
- ✅ Container (future state)

---

## Summary

The C4 model provides **7 diagram types** for different purposes:

**Core (hierarchical)**:
1. **System Context** - Always create
2. **Container** - Usually create
3. **Component** - Selectively create
4. **Code** - Rarely create

**Supplementary (cross-cutting)**:
5. **System Landscape** - For enterprise view
6. **Dynamic** - For runtime behavior
7. **Deployment** - For infrastructure

**Golden rule**: Create only the diagrams that add value. Most teams need **Context + Container + selective Component/Dynamic diagrams**.

---

**Next**: Apply these concepts using the [Reverse Engineering Guide](reverse-engineering-guide.md) to document your own systems.
