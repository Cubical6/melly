---
name: c4model-relations
description: Use when documenting relations, dependencies, and communications between systems, containers, or components in C4 Model architecture. Invoke during dependency mapping, integration analysis, or when users mention "relations", "dependencies", "connections", "how systems communicate", "API calls", "integrations", "data flow", or need to understand inter-system/component relationships.
---

# C4 Model - Relations Documentation

## Overview

Document HOW systems, containers, and components communicate—what flows between them, in which direction, and through which protocols.

**Core Principle:** Relations describe communication and dependencies. Use level-appropriate types with active voice descriptions.

## When to Use

- Documenting system-to-system communication (C1)
- Mapping container interactions (C2)
- Describing component dependencies (C3)
- Integration analysis and dependency mapping

## When NOT to Use

- Documenting static properties → use c4model-observations
- Describing internal implementation details
- Non-architectural documentation

---

## Quick Reference

| Level | Key Fields | Common Types | Focus |
|-------|------------|--------------|-------|
| C1 | `direction`, `protocol` | http-rest, message-queue, authentication | Protocols between systems |
| C2 | `protocol`, `isAsync` | database-read-write, cache-read | Container interactions |
| C3 | `coupling` | uses, injects, implements, observes | Code-level dependencies |

**IMPORTANT:** `direction` is C1 ONLY. Never use `direction` for C2 or C3 relations.

**Type specificity:** Match type to actual operation:
- `cache-read` for read-only, `cache-write` for write-only, `cache-read-write` for both
- `database-query` for read-only, `database-read-write` for both

**Complete type definitions** → [types.md](./types.md)

---

## Relation Structure

```json
{
  "id": "rel-frontend-to-api",
  "target": "backend-api",
  "type": "http-rest",
  "description": "Sends HTTP requests to fetch user data"
}
```

**Required:** `id`, `target`, `type`, `description`
**Optional:** `protocol`, `direction` (C1), `coupling` (C3), `isAsync`, `tags`

---

## Direction and Coupling

**Direction (C1 only):**
- `outbound` - Source initiates (Frontend → API)
- `inbound` - Target initiates (Webhook → Your system)
- `bidirectional` - Both ways (WebSocket)

**Coupling (C3 only):**
- `loose` - Easily replaceable (DI, interfaces)
- `tight` - Hard to replace (inheritance, direct refs)

---

## Writing Descriptions

✅ Active voice, start with verb, be specific:
- "Sends HTTP requests to fetch user profile"
- "Reads customer records from PostgreSQL"
- "Injects UserRepository via DI"

❌ Avoid:
- "Data is sent" (passive)
- "Connection" (vague)
- "Talks to the API" (unspecific)

---

## Examples

**C1:** `{ "type": "http-rest", "direction": "outbound", "protocol": "HTTP/REST" }`
**C2:** `{ "type": "database-read-write", "protocol": "PostgreSQL Wire Protocol" }`
**C3:** `{ "type": "uses", "coupling": "loose" }`

**45+ examples** → [examples.md](./examples.md)

---

## Common Mistakes

1. **Wrong level types** - Use C1 types at C1, C3 types at C3
2. **Using direction for C2/C3** - `direction` is C1 ONLY, never use for containers or components
3. **Wrong access type** - Use `cache-read` for read-only, not `cache-read-write`
4. **Missing direction/coupling** - Required for C1/C3 respectively
5. **Passive voice** - Always use active voice descriptions
6. **Generic types** - Use `http-rest` not `http`
7. **Invalid targets** - Ensure target entity exists

---

## Integration

**Commands:** `/melly-c1-systems`, `/melly-c2-containers`, `/melly-c3-components`

**Output:** `systems[].relations[]`, `containers[].relations[]`, `components[].relations[]`

**Validation:** `python validation/scripts/validate-c{1,2,3}-*.py`

---

## Detailed Documentation

- [types.md](./types.md) - Complete type definitions
- [reference.md](./reference.md) - Methodology and best practices
- [examples.md](./examples.md) - 45+ real-world examples
