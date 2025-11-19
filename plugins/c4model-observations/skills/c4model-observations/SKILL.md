---
name: c4model-observations
description: Use when documenting observations, architectural findings, or discoveries across C4 Model levels (C1, C2, C3). Triggers include "observations", "findings", "document architecture", "security concerns", "performance issues", "quality attributes". Creates structured observations for c1-systems.json, c2-containers.json, and c3-components.json files with evidence, severity levels, and recommendations.
---

# C4 Model - Observation Documentation Methodology

## Overview

This skill provides methodology for identifying, categorizing, and documenting architectural observations across all C4 Model levels (C1, C2, C3).

**Mission:** Document WHAT you observe about systems, containers, and components—factual findings that inform architectural understanding.

---

## When to Use

- Documenting architectural findings during code analysis
- Categorizing security, performance, or quality issues
- Creating structured observations for C4 model documentation
- Recording evidence with file paths and code snippets

## When NOT to Use

- Writing C4 diagrams themselves (use c4model-c1/c2/c3)
- Documenting relationships between entities (use c4model-relations)
- General code documentation without architectural significance

---

## What is an Observation?

An **observation** is a factual finding about an entity that describes:

- Architectural characteristics, patterns, and decisions
- Technical details, technologies, frameworks
- Quality attributes like performance, scalability, maintainability
- Security concerns and vulnerabilities
- Design decisions and their rationale
- Performance patterns and bottlenecks

**Observations are facts, not opinions.** Document what you see in the code, configuration, and architecture.

---

## Observation Structure

### Required Fields

```json
{
  "id": "obs-unique-identifier",
  "category": "architecture|technology|security|...",
  "severity": "critical|warning|info",
  "title": "Short descriptive title (max 100 chars)",
  "description": "Detailed description of what was observed"
}
```

### Optional Fields (Recommended)

```json
{
  "evidence": [
    {
      "type": "file|code|config|pattern|metric|dependency",
      "location": "path/to/file.js:45-52",
      "snippet": "code excerpt or config value",
      "note": "additional context"
    }
  ],
  "tags": ["searchable", "keywords"],
  "impact": "What this means for the system",
  "recommendation": "Suggested action (for warnings/critical)"
}
```

---

## Severity Levels

**Critical** - Immediate attention required:
- Security vulnerabilities, data loss risks, system unavailability

**Warning** - Should be addressed:
- Performance bottlenecks, code quality issues, anti-patterns

**Info** - Informational or positive findings:
- Design patterns, technology stack, good practices

---

## Evidence Types

| Type | Usage | Example |
|------|-------|---------|
| `file` | File paths, directory structure | `package.json` |
| `code` | Code snippets | `localStorage.setItem('token', jwt)` |
| `config` | Configuration values | `DATABASE_URL=...` |
| `pattern` | Architectural patterns | `Repository pattern` |
| `metric` | Measurements | `Complexity: 45` |
| `dependency` | Package dependencies | `"express": "^4.18.0"` |

---

## Categories by Level

| Level | Categories |
|-------|------------|
| **C1** | `architecture`, `integration`, `boundaries`, `security`, `scalability`, `actors`, `external-dependencies`, `deployment`, `data-flow` |
| **C2** | `technology`, `runtime`, `communication`, `data-storage`, `authentication`, `deployment`, `scalability`, `performance`, `dependencies`, `configuration`, `monitoring`, `security` |
| **C3** | `design-patterns`, `code-structure`, `dependencies`, `error-handling`, `testing`, `performance`, `security`, `code-quality`, `documentation`, `complexity`, `coupling`, `cohesion`, `maintainability` |

See [categories.md](categories.md) for detailed definitions.

---

## Quick Examples

**C3 Component (Critical):**
```json
{
  "id": "obs-jwt-localstorage",
  "category": "security",
  "severity": "critical",
  "title": "JWT tokens stored in localStorage",
  "description": "Tokens in localStorage are vulnerable to XSS attacks.",
  "evidence": [
    {"type": "code", "location": "src/auth/storage.ts:45", "snippet": "localStorage.setItem('token', jwt)"}
  ],
  "recommendation": "Use httpOnly cookies for token storage"
}
```

**C2 Container (Warning):**
```json
{
  "id": "obs-no-connection-pool",
  "category": "performance",
  "severity": "warning",
  "title": "Database connections not pooled",
  "description": "New connection created for each request, causing overhead.",
  "evidence": [
    {"type": "code", "location": "src/db/connection.ts:12", "snippet": "new Client(config)"}
  ],
  "recommendation": "Implement connection pooling with pg-pool"
}
```

**C1 System Context (Info):**
```json
{
  "id": "obs-event-driven-arch",
  "category": "architecture",
  "severity": "info",
  "title": "Event-driven architecture with message queues",
  "description": "System uses RabbitMQ for async processing, enabling loose coupling.",
  "evidence": [
    {"type": "config", "location": "docker-compose.yml", "snippet": "rabbitmq:..."}
  ],
  "impact": "Enables horizontal scaling and resilience"
}
```

See [examples.md](examples.md) for 30+ complete examples across all levels.

---

## Best Practices

1. **Be specific** - Detailed descriptions with concrete evidence
2. **Choose correct severity** - Critical for security/data issues, warning for should-fix, info for neutral
3. **Provide evidence** - Always include file paths and code snippets
4. **Use proper categories** - Match category to C4 level (C1/C2/C3)
5. **Add impact and recommendations** - For warnings and critical issues
6. **Include tags** - Aid searchability and cross-referencing

---

## Detailed Reference

For comprehensive methodology:

- **[reference.md](reference.md)** - Category definitions, evidence guidelines, best practices
- **[examples.md](examples.md)** - 30+ examples across C1, C2, C3 levels
- **[categories.md](categories.md)** - Complete category reference by level

---

## Common Mistakes

1. **Opinion instead of fact** - Document observations, not judgments ("poorly designed" vs "tight coupling between modules")
2. **Vague descriptions** - Be specific with file paths and evidence
3. **Wrong severity** - Critical for security/data loss, warning for should-fix, info for neutral findings
4. **Wrong category level** - Use C1 categories at C1 level, C3 at C3 level

---

## Integration

Observations are used by:
- **Abstractor agents** (c1/c2/c3) - Generate observations during analysis
- **c4model-writer** - Convert observations to markdown docs
- **Validation scripts** - Validate structure and content
- **basic-memory MCP** - Search and retrieve observations

---

## Related Skills

- **c4model-c1** - C1 System Context methodology
- **c4model-c2** - C2 Container methodology
- **c4model-c3** - C3 Component methodology
- **c4model-relations** - Relationship documentation methodology
