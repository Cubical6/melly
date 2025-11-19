# melly-c3 Plugin

C4 Model Level 3 (Component) identification plugin for Melly workflow.

## Overview

This plugin provides tools for identifying and documenting software components at the C3 (Component) level of the C4 model. It analyzes containers to identify code-level components, their responsibilities, dependencies, and design patterns.

## Components

### Agent: c3-abstractor

**Location:** `agents/c3-abstractor.md`

**Purpose:** Analyzes containers and identifies C3 components using C4 Model methodology.

**Features:**
- Validates prerequisite files (init.json, c1-systems.json, c2-containers.json)
- Checks timestamp ordering for data consistency
- Loads c4model-c3 skill for methodology
- Identifies component types (controller, service, repository, model, etc.)
- Analyzes component dependencies and coupling
- Detects design patterns (Singleton, Factory, Repository, DI)
- Calculates component metrics (LOC, complexity, dependencies)
- Generates c3-components.json with observations and relations
- Validates output structure

**Usage:** Automatically invoked by `/melly-c3-components` command.

### Command: /melly-c3-components

**Location:** `commands/melly-c3-components.md`

**Purpose:** User-facing command to orchestrate C3 component identification.

**Syntax:**
```bash
/melly-c3-components [c2-containers-json-path]
```

**Features:**
- Validates prerequisites (init.json, c1-systems.json, c2-containers.json)
- Launches c3-abstractor agent via Task tool
- Validates output with melly-validation scripts
- Reports component statistics and next steps

**Output:**
- `c3-components.json` - Components with metadata, observations, relations

## Dependencies

### Required Plugins

- **c4model-c3** - C3 methodology skill (component identification rules, patterns)
- **melly-validation** - Validation scripts (validate-c3-components.py, check-timestamp.sh)

### Required Files

- `init.json` - From `/melly-init`
- `c1-systems.json` - From `/melly-c1-systems`
- `c2-containers.json` - From `/melly-c2-containers`

## Workflow Integration

This plugin is part of the Melly C4 workflow:

```
/melly-init
    ↓
/melly-c1-systems
    ↓
/melly-c2-containers
    ↓
/melly-c3-components  ← This plugin
    ↓
/melly-doc-c4model
    ↓
/melly-draw-c4model
```

## Output Format

The agent generates `c3-components.json` with:

```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "generator": "c3-abstractor",
    "timestamp": "ISO 8601 timestamp",
    "parent_file": "c2-containers.json",
    "parent_timestamp": "parent timestamp"
  },
  "components": [
    {
      "id": "kebab-case-id",
      "name": "Component Name",
      "type": "controller|service|repository|model|middleware|utility|dto|adapter",
      "container_id": "parent-container-id",
      "path": "relative/path/to/component",
      "description": "Component purpose",
      "responsibilities": ["Primary responsibility"],
      "layer": "presentation|business|data|integration",
      "dependencies": [
        {"target": "component-id", "type": "uses|calls|depends-on"}
      ],
      "observations": [
        {"category": "code-structure|design-patterns|dependencies|complexity", "content": "finding", "severity": "info|warning|critical", "evidence": "file:line"}
      ],
      "relations": [
        {"target": "external-system", "type": "http|database|file", "description": "interaction"}
      ],
      "metrics": {
        "loc": 0,
        "complexity": 0,
        "dependencies_count": 0,
        "public_methods": 0
      }
    }
  ],
  "summary": {
    "total_components": 0,
    "by_type": {},
    "by_layer": {}
  }
}
```

## Best Practices

### Component Identification

- **Focus on significant components** - Components >200 LOC or architecturally important
- **Single responsibility** - Each component has one clear purpose
- **Clear naming** - Use descriptive names ("User Service" not "userService.ts")
- **Layer separation** - Validate proper layering (presentation → business → data)

### Design Pattern Detection

- Singleton, Factory, Repository patterns
- Dependency Injection
- Observer, Strategy, Decorator, Adapter patterns
- Architectural patterns (MVC, Layered, Hexagonal, CQRS)

### Observations

- **Code structure** - Organization, file structure, modularity
- **Design patterns** - Patterns detected with evidence
- **Dependencies** - Internal and external dependencies
- **Complexity** - High complexity areas, refactoring needs
- **Coupling** - Tight coupling warnings
- **Quality** - Documentation, testing, error handling

### Validation

All generated JSON must pass validation:
```bash
python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json
```

Validates:
- Schema structure
- Timestamp ordering (c3 > c2 > c1 > init)
- Referential integrity (all dependency targets exist)
- Required fields
- ID format (kebab-case)
- Container reference validation

## Version

- **Version:** 1.0.0
- **Last Updated:** 2025-11-17
- **Compatibility:** Melly 1.0.0+

## License

MIT License - See repository root for details.
