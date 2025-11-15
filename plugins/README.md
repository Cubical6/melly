# Melly Marketplace Plugins

This directory contains Claude Code plugins that provide contextual retrieval and skill development capabilities for the Melly marketplace.

## Installed Plugins

### 1. Abstractor Agent

**Version:** 1.0.0
**License:** MIT
**Repository:** [Cubical6/melly](https://github.com/Cubical6/melly)

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
**Repository:** [Cubical6/melly](https://github.com/Cubical6/melly)

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
/plugin add /path/to/melly/plugins/abstractor-agent
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

All plugins in the Melly marketplace are licensed under the MIT License.

## Credits

- **Abstractor Agent** - Based on [Axiom System Archaeologist](https://github.com/Cubical6/skillpacks) by tachyon-beep
- **Skill Builder** - Based on [Skill Builder](https://github.com/Cubical6/skill-builder) by Ken Collins
