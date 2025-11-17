---
name: c4model-observations
description: Use when documenting observations, architectural findings, or key discoveries across C4 Model levels (C1 System Context, C2 Container, C3 Component). Invoke when analyzing architecture, identifying patterns, documenting technical findings, security concerns, performance issues, or quality attributes. Essential for creating structured observations in c1-systems.json, c2-containers.json, and c3-components.json files. Use when users mention "observations", "findings", "document discoveries", "architectural notes", or "key observations".
---

# C4 Model - Observation Documentation Methodology

## Overview

This skill provides methodology for identifying, categorizing, and documenting architectural observations across all C4 Model levels (C1, C2, C3).

**Mission:** Document WHAT you observe about systems, containers, and components—factual findings that inform architectural understanding.

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

### C1 System Context (9 categories)
`architecture`, `integration`, `boundaries`, `security`, `scalability`, `actors`, `external-dependencies`, `deployment`, `data-flow`

See [categories.md](categories.md) for detailed definitions.

### C2 Container (12 categories)
`technology`, `runtime`, `communication`, `data-storage`, `authentication`, `deployment`, `scalability`, `performance`, `dependencies`, `configuration`, `monitoring`, `security`

See [categories.md](categories.md) for detailed definitions.

### C3 Component (13 categories)
`design-patterns`, `code-structure`, `dependencies`, `error-handling`, `testing`, `performance`, `security`, `code-quality`, `documentation`, `complexity`, `coupling`, `cohesion`, `maintainability`

See [categories.md](categories.md) for detailed definitions.

---

## Quick Example

**C1 System Context:**
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

## Integration

Observations are used by:
- **Abstractor agents** (c1/c2/c3) - Generate observations during analysis
- **c4model-writer** - Convert observations to markdown docs
- **Validation scripts** - Validate structure and content
- **basic-memory MCP** - Search and retrieve observations
