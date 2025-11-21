# Laravel 12 Documentation Index

> **Library**: Laravel Framework
> **Version**: 12.x
> **Source**: https://github.com/laravel/docs (12.x branch)
> **Last Updated**: 2025-11-15
> **Total Files**: 100 documentation files

---

## 📚 Documentation Structure

### 1. Getting Started
Foundation concepts and initial setup for Laravel applications.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `installation.md` | Installation & Setup | Environment setup, Laravel installer, Herd, IDE support |
| `configuration.md` | Configuration | Environment config, directory config, maintenance mode |
| `structure.md` | Directory Structure | App structure, namespace conventions |
| `deployment.md` | Deployment | Server requirements, optimization, deployment strategies |
| `lifecycle.md` | Request Lifecycle | HTTP kernel, service providers, request/response flow |
| `releases.md` | Release Notes | Version changes, upgrade guides |
| `upgrade.md` | Upgrade Guide | Migration instructions between versions |

**Relations**:
- `installation.md` → references → `configuration.md`, `structure.md`
- `lifecycle.md` → explains → `providers.md`, `middleware.md`

---

### 2. Architecture Concepts
Core architectural patterns and dependency injection.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `container.md` | Service Container | Dependency injection, binding, resolution |
| `providers.md` | Service Providers | Registration, bootstrapping, deferred providers |
| `facades.md` | Facades | Static proxies, real-time facades |
| `contracts.md` | Contracts | Interfaces, loose coupling |

**Relations**:
- `container.md` → used_by → `providers.md`, `facades.md`
- `contracts.md` → implemented_by → Core Laravel services

---

### 3. The Basics
Fundamental features for web application development.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `routing.md` | Routing | Route definitions, parameters, named routes, groups |
| `middleware.md` | Middleware | Request filtering, middleware groups, parameters |
| `csrf.md` | CSRF Protection | Token generation, validation, X-CSRF-TOKEN |
| `controllers.md` | Controllers | Resource controllers, dependency injection, middleware |
| `requests.md` | HTTP Requests | Request input, files, cookies, request lifecycle |
| `responses.md` | HTTP Responses | Response types, headers, cookies, redirects |
| `views.md` | Views | View rendering, data passing, view composers |
| `blade.md` | Blade Templates | Templating syntax, directives, components, layouts |
| `urls.md` | URL Generation | Named routes, controller actions, signed URLs |
| `session.md` | Session | Session drivers, data storage, flash data |
| `validation.md` | Validation | Validation rules, form requests, custom validators |
| `errors.md` | Error Handling | Exception handling, HTTP exceptions, logging |
| `logging.md` | Logging | Log channels, levels, custom channels |

**Relations**:
- `routing.md` → connects_to → `middleware.md`, `controllers.md`
- `controllers.md` → uses → `requests.md`, `responses.md`, `validation.md`
- `views.md` → uses → `blade.md`
- `requests.md` → validated_by → `validation.md`

---

### 4. Digging Deeper
Advanced features and utilities.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `artisan.md` | Artisan Console | Commands, scheduling, custom commands |
| `broadcasting.md` | Broadcasting | Real-time events, WebSockets, channels |
| `cache.md` | Cache | Cache drivers, operations, cache tags |
| `collections.md` | Collections | Collection methods, higher-order messages |
| `context.md` | Context | Request context, context propagation |
| `concurrency.md` | Concurrency | Parallel processing, async operations |
| `events.md` | Events | Event listeners, subscribers, dispatching |
| `filesystem.md` | File Storage | Disks, cloud storage, file operations |
| `helpers.md` | Helper Functions | Array, string, path, misc helpers |
| `http-client.md` | HTTP Client | Guzzle wrapper, requests, testing |
| `localization.md` | Localization | Translation, pluralization, language files |
| `mail.md` | Mail | Mailables, markdown mail, attachments, queuing |
| `notifications.md` | Notifications | Notification channels, mail, database, broadcast |
| `packages.md` | Package Development | Package discovery, service providers, resources |
| `processes.md` | Processes | Process invocation, pools, testing |
| `prompts.md` | Prompts | CLI prompts, user input |
| `queues.md` | Queues | Job queues, workers, dispatching, failed jobs |
| `rate-limiting.md` | Rate Limiting | Throttling, limiters |
| `redirects.md` | Redirects | Redirect responses, with data |
| `scheduling.md` | Task Scheduling | Cron scheduling, task frequency, output |
| `strings.md` | Strings | String manipulation, Stringable API |

**Relations**:
- `artisan.md` → used_for → `scheduling.md`
- `events.md` → triggers → `listeners.md`, `notifications.md`
- `queues.md` → processes → `mail.md`, `notifications.md`, `broadcasting.md`
- `cache.md` → improves → Application performance
- `filesystem.md` → stores → User uploads, generated files

---

### 5. Security
Authentication, authorization, and security features.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `authentication.md` | Authentication | Guards, providers, user authentication |
| `authorization.md` | Authorization | Gates, policies, middleware |
| `verification.md` | Email Verification | Email verification routes, middleware |
| `passwords.md` | Password Reset | Reset links, token repository |
| `encryption.md` | Encryption | Encrypt/decrypt, APP_KEY |
| `hashing.md` | Hashing | Password hashing, bcrypt, argon |

**Relations**:
- `authentication.md` → works_with → `session.md`, `middleware.md`
- `authorization.md` → uses → `authentication.md`
- `passwords.md` → requires → `mail.md`, `notifications.md`
- `hashing.md` → secures → `passwords.md`

---

### 6. Database
Database operations and query building.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `database.md` | Database | Connections, queries, transactions |
| `queries.md` | Query Builder | Fluent queries, joins, aggregates |
| `pagination.md` | Pagination | Paginator, cursor pagination |
| `migrations.md` | Migrations | Schema builder, version control |
| `seeding.md` | Database Seeding | Seeders, factories, test data |
| `redis.md` | Redis | Redis connections, pub/sub |
| `mongodb.md` | MongoDB | MongoDB integration |

**Relations**:
- `database.md` → provides → `queries.md`, `migrations.md`
- `queries.md` → used_by → `eloquent.md`
- `migrations.md` → creates_tables_for → `eloquent.md`
- `seeding.md` → uses → `eloquent-factories.md`

---

### 7. Eloquent ORM
Object-relational mapping and model operations.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `eloquent.md` | Eloquent ORM | Models, CRUD operations, scopes |
| `eloquent-relationships.md` | Relationships | HasOne, HasMany, BelongsTo, ManyToMany |
| `eloquent-collections.md` | Eloquent Collections | Model collection methods |
| `eloquent-mutators.md` | Mutators & Casts | Accessors, mutators, attribute casting |
| `eloquent-resources.md` | API Resources | Resource transformations, pagination |
| `eloquent-serialization.md` | Serialization | JSON, arrays, hidden attributes |
| `eloquent-factories.md` | Model Factories | Factory definitions, states, relationships |

**Relations**:
- `eloquent.md` → extends → `queries.md`
- `eloquent-relationships.md` → defines → Model associations
- `eloquent-collections.md` → extends → `collections.md`
- `eloquent-factories.md` → used_by → `seeding.md`, `testing.md`

---

### 8. Testing
Testing tools and strategies.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `testing.md` | Testing | PHPUnit, test setup, assertions |
| `http-tests.md` | HTTP Tests | Feature tests, JSON APIs, file uploads |
| `console-tests.md` | Console Tests | Artisan command testing |
| `database-testing.md` | Database Testing | Migrations, factories, seeders in tests |
| `mocking.md` | Mocking | Facades, events, jobs, notifications |
| `dusk.md` | Browser Tests | Laravel Dusk, browser automation, pages |

**Relations**:
- `testing.md` → uses → `http-tests.md`, `console-tests.md`, `database-testing.md`
- `database-testing.md` → uses → `eloquent-factories.md`
- `mocking.md` → helps_test → `events.md`, `mail.md`, `notifications.md`
- `dusk.md` → tests → Frontend functionality

---

### 9. Official Packages
First-party Laravel packages and integrations.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `billing.md` | Laravel Cashier (Stripe) | Subscriptions, invoices, webhooks |
| `cashier-paddle.md` | Cashier Paddle | Paddle billing integration |
| `fortify.md` | Laravel Fortify | Backend authentication scaffolding |
| `horizon.md` | Laravel Horizon | Queue monitoring, metrics |
| `passport.md` | Laravel Passport | OAuth2 server, API authentication |
| `pennant.md` | Laravel Pennant | Feature flags |
| `precognition.md` | Laravel Precognition | Real-time validation |
| `pulse.md` | Laravel Pulse | Application monitoring |
| `sanctum.md` | Laravel Sanctum | API token authentication, SPA auth |
| `scout.md` | Laravel Scout | Full-text search, Algolia, Meilisearch |
| `socialite.md` | Laravel Socialite | OAuth providers (GitHub, Google, etc.) |
| `telescope.md` | Laravel Telescope | Debugging assistant, request inspection |

**Relations**:
- `billing.md`, `cashier-paddle.md` → handle → Subscription payments
- `passport.md`, `sanctum.md` → provide → API authentication
- `fortify.md` → implements → `authentication.md` backend
- `horizon.md` → monitors → `queues.md`
- `scout.md` → indexes → `eloquent.md` models
- `telescope.md` → debugs → All application layers

---

### 10. Development Tools
Local development and deployment tools.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `homestead.md` | Laravel Homestead | Vagrant box, local development |
| `valet.md` | Laravel Valet | macOS development environment |
| `sail.md` | Laravel Sail | Docker development environment |
| `octane.md` | Laravel Octane | Application server (Swoole, RoadRunner) |
| `pint.md` | Laravel Pint | Code style fixer |
| `envoy.md` | Laravel Envoy | Task runner, SSH deployment |
| `mix.md` | Laravel Mix | Asset compilation (legacy) |
| `vite.md` | Vite | Modern asset bundling |

**Relations**:
- `homestead.md`, `valet.md`, `sail.md` → provide → Local development
- `octane.md` → improves → Application performance
- `vite.md` → replaces → `mix.md` (for asset compilation)
- `pint.md` → enforces → Code style standards

---

### 11. Frontend & UI
Frontend integration and UI components.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `frontend.md` | Frontend | Asset compilation, JavaScript frameworks |
| `starter-kits.md` | Starter Kits | Breeze, Jetstream |
| `folio.md` | Laravel Folio | Page-based routing |
| `reverb.md` | Laravel Reverb | WebSocket server |

**Relations**:
- `frontend.md` → uses → `vite.md`
- `starter-kits.md` → includes → `authentication.md`, `blade.md`
- `folio.md` → simplifies → `routing.md`
- `reverb.md` → enables → `broadcasting.md`

---

### 12. Meta & Documentation
Project documentation and contribution guides.

| File | Topic | Key Concepts |
|------|-------|--------------|
| `readme.md` | README | Project overview |
| `documentation.md` | Documentation | Docs contribution guide |
| `contributions.md` | Contributions | Code contribution guidelines |
| `license.md` | License | MIT License |
| `mcp.md` | MCP Integration | Model Context Protocol |

---

## 🔍 Key Concepts by Topic

### Core Architecture
- **Dependency Injection**: `container.md`, `providers.md`
- **Service Resolution**: `container.md`, `facades.md`
- **Request Lifecycle**: `lifecycle.md`, `middleware.md`

### HTTP Layer
- **Routing**: `routing.md`, `urls.md`, `folio.md`
- **Controllers**: `controllers.md`, `middleware.md`
- **Request/Response**: `requests.md`, `responses.md`, `validation.md`
- **Views**: `views.md`, `blade.md`

### Database & ORM
- **Query Building**: `database.md`, `queries.md`
- **ORM**: `eloquent.md`, `eloquent-relationships.md`
- **Migrations**: `migrations.md`, `seeding.md`
- **Testing**: `database-testing.md`, `eloquent-factories.md`

### Asynchronous Operations
- **Queues**: `queues.md`, `horizon.md`
- **Events**: `events.md`, `broadcasting.md`
- **Scheduling**: `scheduling.md`
- **Concurrency**: `concurrency.md`

### Security
- **Authentication**: `authentication.md`, `fortify.md`, `passport.md`, `sanctum.md`
- **Authorization**: `authorization.md`
- **Encryption**: `encryption.md`, `hashing.md`

### API Development
- **API Resources**: `eloquent-resources.md`
- **Authentication**: `passport.md`, `sanctum.md`
- **HTTP Client**: `http-client.md`
- **Rate Limiting**: `rate-limiting.md`

### Testing
- **Unit/Feature**: `testing.md`, `http-tests.md`, `console-tests.md`
- **Browser**: `dusk.md`
- **Mocking**: `mocking.md`

### DevOps
- **Local Dev**: `homestead.md`, `valet.md`, `sail.md`
- **Deployment**: `deployment.md`, `envoy.md`
- **Performance**: `octane.md`, `cache.md`
- **Monitoring**: `telescope.md`, `horizon.md`, `pulse.md`

---

## 📊 Documentation Statistics

- **Total Files**: 100 markdown files
- **Categories**: 12 major categories
- **Average File Size**: ~30 KB
- **Code Examples**: Present in all files
- **Cross-References**: Extensive internal linking

---

## 🔗 Common Documentation Patterns

### Cross-References
Most documentation files reference related topics using the pattern:
```markdown
[topic name](/docs/{{version}}/filename)
```

### Code Examples
All files include practical code examples with syntax highlighting:
```php
// Typical Laravel code example
```

### Callouts
Documentation uses various callout types:
- `[!NOTE]` - Important information
- `[!WARNING]` - Warnings about potential issues
- `[!TIP]` - Helpful tips

### Section Anchors
All major sections include named anchors for direct linking:
```markdown
<a name="section-name"></a>
## Section Title
```

---

## 💡 Usage Recommendations

### For Learning
1. Start with: `installation.md`, `routing.md`, `views.md`, `blade.md`
2. Progress to: `eloquent.md`, `migrations.md`, `authentication.md`
3. Advanced: `queues.md`, `broadcasting.md`, `packages.md`

### For API Development
Essential reads: `routing.md`, `controllers.md`, `eloquent.md`, `eloquent-resources.md`, `sanctum.md` or `passport.md`

### For Full-Stack Development
Focus on: `routing.md`, `blade.md`, `eloquent.md`, `validation.md`, `authentication.md`, `vite.md`

### For DevOps
Important: `deployment.md`, `sail.md` or `homestead.md`, `octane.md`, `horizon.md`, `cache.md`

---

## 🔄 Semantic Relations

### Dependencies
```
installation.md → requires → PHP, Composer
eloquent.md → depends_on → database.md
broadcasting.md → requires → redis.md or pusher
horizon.md → requires → queues.md, redis.md
```

### Replacements
```
vite.md → replaces → mix.md
sanctum.md → simpler_alternative_to → passport.md
```

### Enhancements
```
eloquent-collections.md → extends → collections.md
octane.md → improves_performance_of → Application
cache.md → optimizes → Database queries, API calls
```

---

**Generated by**: Library Documentation Analyzer
**Date**: 2025-11-21
**Analyzer Version**: Manual analysis v1.0
