# melly-draw Plugin

> C4 Model Diagram Visualization

Generate Mermaid diagrams and Obsidian canvas files from C4 model JSON data.

## Overview

This plugin provides visualization capabilities for the Melly C4 workflow:
- **Agent**: `c4model-drawer` - Generates diagrams from JSON files
- **Command**: `/melly-draw-c4model` - User-facing command to create visualizations

## Features

✅ **Mermaid Diagram Generation**
- C1 System Context diagrams
- C2 Container diagrams
- C3 Component diagrams
- Proper styling and grouping
- Relation visualization

✅ **Obsidian Canvas**
- Interactive canvas files
- Spatial node positioning
- Visual edge connections
- Compatible with Obsidian

✅ **Incremental Processing**
- Generate specific levels (c1, c2, c3)
- Or generate all diagrams at once
- Organized output structure

## Installation

```bash
# Install via marketplace
/plugin add ./plugins/melly-draw
```

## Usage

### Generate All Diagrams

```bash
/melly-draw-c4model all
```

### Generate Specific Level

```bash
# System context only
/melly-draw-c4model c1

# Container diagrams
/melly-draw-c4model c2

# Component diagrams
/melly-draw-c4model c3
```

## Prerequisites

Required JSON files:
- `init.json` (from `/melly-init`)
- `c1-systems.json` (from `/melly-c1-systems`)
- `c2-containers.json` (from `/melly-c2-containers`)
- `c3-components.json` (from `/melly-c3-components`)

## Output Structure

```
knowledge-base/systems/
└── {system-name}/
    └── diagrams/
        ├── c1-system-context.md        # Mermaid diagram
        ├── c1-canvas.canvas            # Obsidian canvas
        ├── c2-containers.md            # Mermaid diagram
        ├── c2-canvas.canvas            # Obsidian canvas
        ├── c3-components.md            # Mermaid diagram
        └── c3-canvas.canvas            # Obsidian canvas
```

## Diagram Types

### C1 System Context

Shows high-level systems and their relationships:
- Systems as nodes
- External systems
- Communication patterns
- System boundaries

### C2 Containers

Shows deployable units within systems:
- Containers grouped by system
- Technology stack indicators
- Inter-container communication
- Deployment units

### C3 Components

Shows logical components within containers:
- Components grouped by container
- Dependencies between components
- Design patterns
- Code structure

## Viewing Diagrams

### Mermaid Diagrams

Mermaid markdown files (`.md`) can be viewed in:
- Obsidian (with Mermaid plugin)
- GitHub (native support)
- VS Code (with Mermaid extension)
- Any Mermaid-compatible viewer

### Obsidian Canvas

Canvas files (`.canvas`) are JSON-based and viewable in:
- Obsidian (native canvas support)
- Any JSON viewer (for raw data)

## Integration

Part of the Melly C4 workflow:

```
/melly-init              → Initialize repositories
/melly-c1-systems        → Identify systems
/melly-c2-containers     → Identify containers
/melly-c3-components     → Identify components
/melly-doc-c4model       → Generate documentation
/melly-draw-c4model      → Generate diagrams ⬅️ This plugin
```

## Version

**1.0.0** - Initial release

## License

MIT

## Author

Melly Team - melly.jwpd1@simplelogin.com
