# Dependency Analysis

This guide provides comprehensive methodology for analyzing component dependencies at the C3 level.

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
while IFS= read -r -d '' file; do
  count=$(grep -c '^import' "$file" 2>/dev/null || echo 0)
  printf "%d %s\n" "$count" "$file"
done < <(find src -name "*.ts" -print0) | sort -rn | head -20

# Find components imported by many others (high afferent coupling)
grep -rE "from ['\"](\.\./)+[^'\"]+['\"]" src/ | cut -d: -f2 | cut -d"'" -d'"' -f2 | sort | uniq -c | sort -rn
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
