# c4model-observations

> C4 Model observation documentation methodology for architectural findings across system, container, and component levels.

## Overview

The `c4model-observations` skill provides comprehensive methodology for identifying, categorizing, and documenting architectural observations across all C4 Model levels (C1 System Context, C2 Container, C3 Component).

**Use this skill when:**
- Documenting architectural findings
- Identifying patterns in code
- Noting security concerns
- Recording performance issues
- Documenting quality attributes
- Creating structured observations

---

## Installation

### Via Melly Marketplace

```bash
# Install from marketplace
/plugin add c4model-observations
```

### Manual Installation

```bash
# Clone or copy to your project
cp -r plugins/c4model-observations ~/.claude/plugins/

# Or for project-specific installation
cp -r plugins/c4model-observations /path/to/project/.claude/plugins/
```

---

## Quick Start

### Automatic Activation

The skill activates automatically when you mention observation-related keywords:

```
> Document the observations I found in the authentication system
> What observations should I note about this architecture?
> Help me categorize this security finding
```

### Manual Activation

You can explicitly invoke the skill:

```
> Use the c4model-observations skill to help me document this finding
```

---

## Skill Structure

```
skills/c4model-observations/
├── SKILL.md           # Main skill (158 lines)
├── reference.md       # Comprehensive methodology
├── examples.md        # 30+ real-world examples
└── categories.md      # Category quick reference
```

---

## Key Features

### Observation Structure

Every observation includes:

**Required Fields:**
- `id` - Unique identifier
- `category` - Category (level-specific)
- `severity` - Critical, warning, or info
- `title` - Short description
- `description` - Detailed finding

**Optional Fields:**
- `evidence` - Supporting evidence (file paths, code snippets)
- `tags` - Searchable keywords
- `impact` - What this means
- `recommendation` - Suggested action

### Severity Levels

- **Critical** - Security vulnerabilities, data loss risks, system unavailability
- **Warning** - Performance issues, code quality, anti-patterns
- **Info** - Positive patterns, technology stack, capabilities

### Evidence Types

- `file` - File paths and directory structure
- `code` - Code snippets
- `config` - Configuration values
- `pattern` - Architectural patterns
- `metric` - Quantitative measurements
- `dependency` - Package dependencies

---

## Categories by Level

### C1 System Context (9 categories)

`architecture`, `integration`, `boundaries`, `security`, `scalability`, `actors`, `external-dependencies`, `deployment`, `data-flow`

Focus on **system-level** architecture and external integrations.

### C2 Container (12 categories)

`technology`, `runtime`, `communication`, `data-storage`, `authentication`, `deployment`, `scalability`, `performance`, `dependencies`, `configuration`, `monitoring`, `security`

Focus on **deployable units** and runtime characteristics.

### C3 Component (13 categories)

`design-patterns`, `code-structure`, `dependencies`, `error-handling`, `testing`, `performance`, `security`, `code-quality`, `documentation`, `complexity`, `coupling`, `cohesion`, `maintainability`

Focus on **code-level** implementation and quality.

---

## Examples

### C1 System Context Example

```json
{
  "id": "obs-event-driven-arch",
  "category": "architecture",
  "severity": "info",
  "title": "Event-driven architecture with message queues",
  "description": "System uses RabbitMQ for async processing, enabling loose coupling.",
  "evidence": [
    {
      "type": "config",
      "location": "docker-compose.yml",
      "snippet": "rabbitmq:\n  image: rabbitmq:3-management"
    }
  ],
  "impact": "Enables horizontal scaling and resilience"
}
```

### C2 Container Example

```json
{
  "id": "obs-db-no-connection-pool",
  "category": "performance",
  "severity": "warning",
  "title": "Database connections not pooled",
  "description": "Backend creates new DB connections per request.",
  "evidence": [
    {
      "type": "code",
      "location": "src/db/connection.ts:12",
      "snippet": "return await mysql.createConnection(config);"
    }
  ],
  "impact": "High latency under load",
  "recommendation": "Implement connection pooling"
}
```

### C3 Component Example

```json
{
  "id": "obs-auth-jwt-localstorage",
  "category": "security",
  "severity": "critical",
  "title": "JWT tokens stored in localStorage",
  "description": "Auth component stores JWTs in localStorage, vulnerable to XSS.",
  "evidence": [
    {
      "type": "code",
      "location": "src/auth/authSlice.ts:45",
      "snippet": "localStorage.setItem('authToken', token);"
    }
  ],
  "impact": "XSS attacks can steal tokens",
  "recommendation": "Migrate to httpOnly cookies"
}
```

See [examples.md](skills/c4model-observations/examples.md) for 30+ complete examples.

---

## Documentation

### SKILL.md
Main skill documentation (158 lines):
- What is an observation
- Observation structure
- Severity levels
- Evidence types
- Categories by level
- Quick examples

### reference.md
Comprehensive methodology:
- Detailed category definitions
- Evidence collection guidelines
- Severity level best practices
- Anti-patterns to avoid
- Cross-level consistency
- Validation requirements

### examples.md
30+ real-world examples:
- 10 C1 System Context examples
- 10 C2 Container examples
- 10 C3 Component examples
- All categories represented
- Mix of severity levels

### categories.md
Quick category reference:
- Category definitions by level
- Usage guidelines
- Decision tree for category selection
- Common mistakes

---

## Integration

### Used By

**Agents:**
- `c1-abstractor` - Generates C1 observations
- `c2-abstractor` - Generates C2 observations
- `c3-abstractor` - Generates C3 observations
- `c4model-writer` - Converts observations to markdown

**Validation:**
- `validate-c1-systems.py`
- `validate-c2-containers.py`
- `validate-c3-components.py`

**Storage:**
- `c1-systems.json`
- `c2-containers.json`
- `c3-components.json`
- basic-memory MCP

---

## Best Practices

1. **Be specific** - Detailed descriptions with concrete evidence
2. **Choose correct severity** - Critical for security/data, warning for should-fix, info for neutral
3. **Provide evidence** - Always include file paths and code snippets
4. **Use proper categories** - Match category to C4 level (C1/C2/C3)
5. **Add impact and recommendations** - For warnings and critical issues
6. **Include tags** - Aid searchability and cross-referencing

---

## Validation

### Required Field Validation

- `id` matches pattern: `^obs-[a-z0-9-]+$`
- `category` is valid for the C4 level
- `severity` is `critical`, `warning`, or `info`
- `title` max 100 characters
- `description` min 10 characters

### Evidence Validation

- `type` is valid evidence type
- `location` is required
- `snippet` recommended
- `note` optional but helpful

### Recommendation Requirements

- **Critical** observations MUST include recommendation
- **Warning** observations SHOULD include recommendation
- **Info** observations MAY include recommendation

---

## Related Skills

- **[c4model-c1](../c4model-c1)** - C1 System Context methodology
- **[c4model-c2](../c4model-c2)** - C2 Container methodology
- **[c4model-c3](../c4model-c3)** - C3 Component methodology
- **[c4model-relations](../c4model-relations)** - Relation documentation methodology

---

## Version

**Version:** 1.0.0
**Author:** Melly Team
**License:** MIT

---

## Support

For issues, questions, or contributions:
- Check [reference.md](skills/c4model-observations/reference.md) for detailed methodology
- Review [examples.md](skills/c4model-observations/examples.md) for real-world examples
- See [categories.md](skills/c4model-observations/categories.md) for category guidance
