# c4model-observations

> C4 Model observation documentation methodology for architectural findings across system, container, and component levels.

## Overview

The `c4model-observations` skill provides methodology for identifying, categorizing, and documenting architectural observations across all C4 Model levels (C1 System Context, C2 Container, C3 Component).

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

The skill activates automatically when you mention observation-related keywords:

```
> Document the observations I found in the authentication system
> What observations should I note about this architecture?
> Help me categorize this security finding
```

See [SKILL.md](skills/c4model-observations/SKILL.md) for complete methodology.

---

## Skill Structure

```
skills/c4model-observations/
├── SKILL.md           # Main skill methodology
├── reference.md       # Comprehensive methodology details
├── examples.md        # 30+ real-world examples
└── categories.md      # Category quick reference
```

---

## Documentation

| File | Description |
|------|-------------|
| [SKILL.md](skills/c4model-observations/SKILL.md) | Main skill: structure, severity, categories, examples |
| [reference.md](skills/c4model-observations/reference.md) | Detailed methodology, anti-patterns, validation |
| [examples.md](skills/c4model-observations/examples.md) | 30+ examples across C1, C2, C3 levels |
| [categories.md](skills/c4model-observations/categories.md) | Category definitions and selection guide |

---

## Related Skills

- **c4model-c1** - C1 System Context methodology
- **c4model-c2** - C2 Container methodology
- **c4model-c3** - C3 Component methodology
- **c4model-relations** - Relationship documentation methodology

---

## Version

**Version:** 1.0.0
**Author:** Melly Team
**License:** MIT
