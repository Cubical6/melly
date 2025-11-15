# C4 Model Documentation

> An easy to learn, developer friendly approach to software architecture diagramming

## Overview

The C4 model is a hierarchical framework for visualizing software architecture through four levels of abstraction. Created by Simon Brown, it provides a structured approach to documenting software systems that is both accessible to developers and useful for communicating with stakeholders.

## What is C4?

**C4 stands for Context, Containers, Components, and Code** - the four levels of abstraction used to describe a software system.

The core philosophy is simple:

> "A software system is made up of one or more containers (applications and data stores), each of which contains one or more components, which in turn are implemented by one or more code elements"

## The Four Levels

```
┌─────────────────────────────────────────────┐
│  Level 1: System Context                    │  <- Highest abstraction
│  (How the system fits in the world)         │
├─────────────────────────────────────────────┤
│  Level 2: Container                         │
│  (Applications & data stores)               │
├─────────────────────────────────────────────┤
│  Level 3: Component                         │
│  (Functional units within containers)       │
├─────────────────────────────────────────────┤
│  Level 4: Code                              │  <- Lowest abstraction
│  (Classes, interfaces, objects, functions)  │
└─────────────────────────────────────────────┘
```

### 1. System Context

**The big picture** - Shows how your software system fits into the world around it.

- **Audience**: Everyone (technical and non-technical)
- **Shows**: The system, users, and external dependencies
- **Zoom level**: 🔍 Very high level

### 2. Container

**The high-level technology choices** - Shows the major structural building blocks.

- **Audience**: Technical people (developers, architects)
- **Shows**: Applications, data stores, microservices
- **Zoom level**: 🔍🔍 High level
- **Note**: "Container" ≠ Docker container (it means any executable/deployable unit)

### 3. Component

**Inside each container** - Shows the major logical components and their interactions.

- **Audience**: Developers and architects
- **Shows**: Components, their responsibilities, and relationships
- **Zoom level**: 🔍🔍🔍 Medium level

### 4. Code

**Implementation details** - Shows how components are implemented in code.

- **Audience**: Developers
- **Shows**: Classes, interfaces, objects, functions
- **Zoom level**: 🔍🔍🔍🔍 Low level
- **Note**: Often auto-generated from code or skipped (UML class diagrams)

## Key Principles

### Abstraction-First Approach

The C4 model is grounded in how software architects and developers actually think about and build systems. This makes it:

- ✅ Easy to learn
- ✅ Developer-friendly
- ✅ Straightforward to implement
- ✅ Accessible to non-technical stakeholders (at higher levels)

### You Don't Need All Four Levels

**Important**: Most teams only need **System Context and Container diagrams**.

Use the appropriate level of detail for your audience and purpose:
- Quick overview? → System Context
- Architecture decisions? → System Context + Container
- Implementation planning? → Add Component diagrams
- Detailed design? → Rarely need Code level

### Notation Independence

The C4 model is **not** tied to UML or any specific notation. You can use:
- Simple boxes and lines
- PlantUML
- Structurizr DSL
- Draw.io
- Mermaid
- Any diagramming tool you prefer

## Supplementary Diagrams

Beyond the core four levels, C4 includes:

### System Landscape Diagram

Shows the big picture of system landscapes within an organization.
- **Audience**: Technical and non-technical stakeholders
- **Shows**: Multiple software systems and how they relate

### Dynamic Diagram

Illustrates how elements collaborate at runtime.
- **Shows**: Sequence of interactions (like UML sequence diagrams)
- **Useful for**: Understanding complex workflows

### Deployment Diagram

Shows how containers map to infrastructure.
- **Shows**: Physical/virtual hardware, containers, deployment topology
- **Useful for**: Understanding production architecture

## When to Use C4

### ✅ Use C4 When:

- Documenting software architecture
- Onboarding new team members
- Communicating design decisions
- Planning system evolution
- Conducting architecture reviews
- Creating technical documentation
- **Reverse engineering existing systems**

### ❌ C4 is Not For:

- Detailed process flows (use BPMN)
- Data modeling (use ER diagrams)
- User journeys (use journey maps)
- Network topology (use network diagrams)

## Benefits

### For Developers

- **Common vocabulary**: Everyone understands "context", "container", "component"
- **Right level of detail**: Choose the zoom level that fits your needs
- **Easy to maintain**: Simple diagrams are easier to keep up to date
- **Tool agnostic**: Use whatever tool you're comfortable with

### For Organizations

- **Better communication**: Between technical and non-technical stakeholders
- **Improved onboarding**: New developers understand the system faster
- **Architecture documentation**: Living documentation that evolves with the system
- **Decision tracking**: Visual record of architectural decisions

## Getting Started

1. **Start with System Context** - Understand the system boundary and external dependencies
2. **Add Container diagram** - Identify major structural building blocks
3. **Component diagrams as needed** - For complex containers
4. **Skip Code diagrams** - Unless absolutely necessary (use IDE for this)

## Resources in This Documentation

- **[Abstractions](abstractions.md)** - Detailed explanation of the four abstraction levels
- **[Diagram Types](diagram-types.md)** - Complete guide to all C4 diagram types
- **[Reverse Engineering Guide](reverse-engineering-guide.md)** - How to apply C4 to understand existing systems

## External Resources

- **Official Website**: [c4model.com](https://c4model.com)
- **Creator**: Simon Brown
- **Book**: "Software Architecture for Developers"
- **License**: Creative Commons Attribution 4.0 International

## Philosophy

The C4 model embraces pragmatism over perfection:

> "The C4 model is a way to think about and communicate software architecture. It's not a formal notation or strict methodology - use what works for you."

The goal is **effective communication**, not perfect diagrams.

---

**Next Steps**:
- Read [Abstractions](abstractions.md) for deep dive into each level
- Check [Reverse Engineering Guide](reverse-engineering-guide.md) to apply C4 to existing projects
- Review [Diagram Types](diagram-types.md) for detailed diagramming guidance
