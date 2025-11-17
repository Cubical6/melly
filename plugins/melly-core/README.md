# Melly Core Plugin

> Core workflow components for C4 model-based code reverse engineering

## Overview

The `melly-core` plugin provides the essential agents and commands for the Melly C4 model workflow. This plugin consolidates the core reverse engineering functionality following Claude Code best practices.

## Components

### Agents

#### `explorer`
- **Purpose**: Scan code repositories and generate `init.json`
- **Usage**: Automatically activated when analyzing repositories
- **Output**: `init.json` with repository metadata, manifests, and structure

### Commands

#### `/melly-init`
- **Purpose**: Initialize C4 model exploration for a project
- **Arguments**: `[repository-path]` (optional, prompts if not provided)
- **Output**: `init.json` file validated and ready for C1 analysis

## Installation

```bash
# From Melly repository root
claude plugin add ./plugins/melly-core
```

## Dependencies

- **melly-validation**: Validation scripts and templates
- Python 3.8+ (for validation scripts)

## Workflow

1. Run `/melly-init` to scan repositories
2. Explorer agent analyzes structure and generates `init.json`
3. Validation ensures data quality
4. Ready for C1 system analysis

## Architecture

This plugin follows the **consolidated plugin structure** from Melly's refactoring effort:
- Simple, focused agents (30-60 lines)
- Clear, concise commands (10-30 lines)
- Progressive disclosure (link to docs)
- Use built-in tools (minimize external scripts)

## Version

**1.0.0** - Initial release (2025-11-17)

## License

MIT
