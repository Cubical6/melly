# Melly Marketplace Plugins

This directory contains Claude Code plugins that provide contextual retrieval and skill development capabilities for the Melly marketplace.

## Installed Plugins

### 1. Axiom System Archaeologist

**Version:** 1.0.2
**License:** CC-BY-SA-4.0
**Repository:** [Cubical6/skillpacks](https://github.com/Cubical6/skillpacks)

Deep architectural analysis of existing codebases through autonomous subagent-driven exploration. Produces comprehensive documentation, C4 diagrams, and subsystem catalogs.

**Key Features:**
- Automatic generation of C4 diagrams (Context, Container, Component levels)
- Subsystem catalogs with dependency tracking
- Professional architectural documentation for stakeholders
- Validation checks for quality assurance
- Coordinated exploration through autonomous subagents

**Usage:**
```bash
/system-archaeologist
```

### 2. Skill Builder

**Version:** 1.0.0
**License:** MIT
**Repository:** [Cubical6/skill-builder](https://github.com/Cubical6/skill-builder)

Meta-skill for creating, editing, and converting Claude Code skills. Includes CLI tools (gh, aws, pip), Python scripting patterns, and progressive disclosure best practices.

**Key Features:**
- Create new skills from scratch with production-ready patterns
- Improve and refactor existing skills
- Convert sub-agents to skill format
- CLI-first approach with modern Python patterns
- Progressive disclosure architecture

**Usage:**
Ask natural questions like:
- "Help me create a skill for deploying AWS Lambda functions"
- "Improve the description for my data-processing skill"
- "Convert my code-reviewer sub-agent to a skill"

## Plugin Structure

Each plugin follows this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── skills/                  # Skills directory
│   └── skill-name/
│       ├── SKILL.md         # Main skill definition
│       └── ...              # Supporting files
└── commands/                # Optional: slash commands
    └── command.md
```

## Installation

These plugins are automatically available as part of the Melly marketplace. For manual installation:

```bash
# Install via Claude Code plugin system
/plugin add /path/to/melly/plugins/axiom-system-archaeologist
/plugin add /path/to/melly/plugins/skill-builder
```

## Development

To add a new plugin to the Melly marketplace:

1. Create a new directory in `plugins/`
2. Add a `.claude-plugin/plugin.json` with metadata
3. Implement skills in `skills/` directory
4. Update `/home/user/melly/.claude-plugin/marketplace.json`
5. Test the plugin locally
6. Commit and push to the repository

## Licenses

- **axiom-system-archaeologist**: CC-BY-SA-4.0
- **skill-builder**: MIT

See individual plugin directories for full license texts.
