---
name: c4model-c3
description: Expert methodology for C4 Model Level 3 (Component) analysis - identifying code-level components, their responsibilities, dependencies, and design patterns within containers. Use when analyzing component architecture, mapping code structure, detecting design patterns, identifying component boundaries and responsibilities, analyzing coupling and cohesion, or documenting components after C2 container identification. Essential for c3-abstractor agent during component identification phase.
---

# C4 Model - Level 3: Component Methodology

## Overview

You are an expert in the C4 Model's Level 3 (Component) methodology. This skill provides comprehensive knowledge for identifying and documenting software components at the code-level architectural abstraction.

**Your Mission:** Help identify WHAT code components exist within containers, WHAT responsibilities they have, and HOW they interact - with focus on design patterns and code structure.

### C3 Level Definition

The Component level shows the **internal structure** of containers - the major code building blocks:

- **Components** - Code modules, classes, packages with clear responsibilities
- **Responsibilities** - What each component does (single responsibility)
- **Dependencies** - How components depend on each other
- **Patterns** - Design patterns and architectural patterns used
- **Boundaries** - Package boundaries, module boundaries, layer boundaries

**At C3, we focus on:** Component identification and naming, responsibilities (single responsibility), dependencies and coupling, design patterns and architectural patterns, code organization, layer boundaries, component interactions.

**At C3, we do NOT focus on:** Individual functions/methods (C4), line-by-line code (C4), variable names and implementation details (C4), deployment details (C2).

---

## Detailed References

For comprehensive guidance on specific aspects of C3 component analysis, see:

- **[Component Identification](./component-identification.md)** - Component types, detection rules, boundaries, file structure patterns, responsibility analysis
- **[Dependency Analysis](./dependency-analysis.md)** - Dependency types, coupling analysis, circular dependencies, metrics, direction validation
- **[Pattern Detection](./pattern-detection.md)** - Design patterns (Singleton, Factory, Repository, etc.) and architectural patterns (MVC, Hexagonal, CQRS, etc.)
- **[Observation Guide](./observation-guide.md)** - Observation categories, severity levels, structure, evidence collection, quality metrics
- **[Technology Examples](./technology-examples.md)** - NestJS, Django, Spring Boot, React implementation examples and patterns
- **[Component Template](./templates/c3-component-template.json)** - JSON template for c3-components.json output

These references are loaded progressively when needed for detailed analysis.

---

## Component Identification Summary

A **component** at C3 level is a cohesive code module with clear responsibility - such as a collection of related classes/functions, an architectural building block, or a distinct layer/subsystem. Components include Controllers (HTTP handlers), Services (business logic), Repositories (data access), Models (data structures), Middleware (request processing), Utilities (helpers), DTOs (data transfer objects), and Adapters (external integrations).

**Key principles:** Focus on significant modules (>200 LOC or architecturally important), one primary responsibility per component (Single Responsibility Principle), group related code together (packages, modules, directories), avoid listing every file.

For complete methodology, see [component-identification.md](./component-identification.md).

---

## Dependency Analysis Summary

Component dependencies reveal the architecture's coupling and maintainability. Analyze internal dependencies (within container), external dependencies (libraries, frameworks), and framework dependencies. Validate dependency direction follows proper layering (Controllers → Services → Repositories → Models).

**Key metrics:** Afferent Coupling (Ca), Efferent Coupling (Ce), Instability (I = Ce / (Ca + Ce)), Circular Dependencies.

For complete methodology, see [dependency-analysis.md](./dependency-analysis.md).

---

## Pattern Detection Summary

Design patterns indicate architectural decisions and code quality. Detect Singleton, Factory, Repository, Dependency Injection, Observer, Strategy, Decorator, and Adapter patterns. Architectural patterns include MVC, Layered Architecture, Hexagonal, CQRS, Microkernel, and Event-Driven.

For complete methodology, see [pattern-detection.md](./pattern-detection.md).

---

## Observation Categories

Document findings using these categories: code-structure, design-patterns, dependencies, complexity, coupling, cohesion, testing, documentation.

**Severity levels:** ℹ️ info (informational), ⚠️ warning (potential issue), 🔴 critical (critical issue).

For complete guide, see [observation-guide.md](./observation-guide.md).

---

## Integration with Melly Workflow

### When This Skill is Used

This skill is activated during **Phase 3: C3 Component Identification** (`/melly-c3-components`) for component identification, responsibility analysis, dependency mapping, and pattern detection. Also used in **Phase 5: Documentation** (`/melly-doc-c4model`) for markdown generation.

### Input Expectations

Expects data from `c2-containers.json` with container details including id, name, type, system_id, path, technology (runtime, framework, language), and structure (entry_point, source_directory, build_output).

### Output Format

Generates `c3-components.json` with metadata (schema_version, generator, timestamp, parent_timestamp), components array (id, name, type, container_id, path, description, responsibilities, layer, dependencies, observations, relations, metrics), and summary (total_components, by_type, by_layer).

### Validation

Generated output must pass: Schema validation, timestamp ordering (metadata.timestamp > parent_timestamp), referential integrity (all dependency targets exist), required fields, ID format (kebab-case), container reference validation.

Validation script:
```bash
python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json
```

---

## Step-by-Step Workflow

### Systematic Approach for c3-abstractor Agent

**Step 1: Load Input Data**
```bash
cat c2-containers.json | jq '.containers'
```

**Step 2: Analyze Each Container**
Navigate to container path, understand directory structure, identify organization pattern (feature-based, layer-based, domain-driven).

**Step 3: Identify Components**
Analyze files/directories, determine component type, extract responsibilities, identify dependencies.

**Step 4: Map Dependencies**
Find internal dependencies (within container), external dependencies (npm packages), document relationships.

**Step 5: Detect Patterns**
Search for design patterns (Singleton, Factory, Repository, Dependency Injection), identify architectural pattern.

**Step 6: Generate Observations**
Document code structure, design patterns, dependencies, complexity, and quality findings.

**Step 7: Calculate Metrics**
Count lines of code, cyclomatic complexity, dependency count, public methods count.

**Step 8: Validate Output**
Check component IDs (kebab-case, unique), container references, dependencies (all targets exist), timestamps (child > parent), run validation script.

---

## Best Practices

### ✅ DO:

1. **Identify significant components only** - Focus on major building blocks, avoid listing every file
2. **Use clear component names** - "User Service" not "userService.ts"
3. **Define single responsibility** - Each component has one clear purpose
4. **Document dependencies clearly** - Internal vs external, purpose of each
5. **Detect design patterns** - Singleton, Factory, Repository, etc.
6. **Analyze code structure** - Feature-based? Layer-based?
7. **Calculate metrics** - LOC, complexity, dependency count
8. **Check for layer violations** - Controllers should not call Repositories directly
9. **Identify circular dependencies** - Use tools, document as warnings
10. **Provide evidence in observations** - Code snippets, file paths, metrics

### ❌ DON'T:

1. **Don't list every file as a component** - Significant modules only
2. **Don't use file names as component names** - Focus on responsibility
3. **Don't ignore component responsibilities** - Always define purpose
4. **Don't skip dependency analysis** - Dependencies reveal architecture
5. **Don't overlook design patterns** - Patterns indicate architectural decisions
6. **Don't ignore metrics** - Metrics help identify refactoring needs
7. **Don't document test files as components** - Tests verify, aren't components
8. **Don't mix abstraction levels** - Keep C3 focused on components, not functions (C4)
9. **Don't skip validation** - Always validate generated JSON
10. **Don't ignore circular dependencies** - Flag and document

---

## Troubleshooting

**Too Many Components:** Focus on significant components - group small utilities, combine related files, use LOC threshold (>200 LOC).

**Can't Determine Type:** Analyze behavior - HTTP requests → Controller, business logic → Service, database access → Repository.

**Circular Dependencies:** Document as warning, suggest refactoring (extract shared logic, use events, remove circular reference).

**Missing Responsibilities:** Read public methods, check method names (create/update/delete), analyze dependencies, read comments.

**No Patterns Detected:** Look for dependency injection, repository pattern, factory pattern, singleton pattern - use grep commands.

**Can't Calculate Metrics:** Use simple LOC counting, count methods manually, count dependencies, document what you can measure.

---

## Quick Reference

### Component Types
controller, service, repository, model, middleware, utility, dto, adapter, factory, validator, facade, guard

### Layers
presentation (Controllers, Middleware, DTOs), business (Services, Domain Models, Validators), data (Repositories, Database Models), integration (Adapters, External Service Clients)

### Design Patterns
Singleton, Factory, Repository, Dependency Injection, Observer, Strategy, Decorator, Adapter

### Architectural Patterns
MVC, Layered (3-tier), Hexagonal (Ports & Adapters), CQRS, Microkernel, Event-Driven

### Observation Categories
code-structure, design-patterns, dependencies, complexity, coupling, cohesion, testing, documentation

### Metrics
Lines of Code (LOC), Cyclomatic Complexity, Number of Dependencies, Number of Public Methods, Afferent Coupling (Ca), Efferent Coupling (Ce), Instability (I = Ce / (Ca + Ce))

---

## Summary

You now have comprehensive knowledge of C4 Model Level 3 (Component) methodology. When invoked:

1. **Load input data** from `c2-containers.json`
2. **Analyze each container** to understand structure
3. **Identify components** using file structure and code analysis
4. **Classify components** by type (controller, service, repository, etc.)
5. **Define responsibilities** for each component
6. **Map dependencies** between components
7. **Detect patterns** (design patterns and architectural patterns)
8. **Generate observations** with evidence
9. **Calculate metrics** (LOC, complexity, dependencies)
10. **Validate output** before finalizing

Remember: **C3 is about code structure.** Focus on WHAT code components exist, WHAT they do, and HOW they interact - not the implementation details of individual functions (that's C4).

For detailed methodology on specific aspects, refer to the documentation files listed in the "Detailed References" section above.

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-11-17
**Compatibility**: Melly 1.0.0+
