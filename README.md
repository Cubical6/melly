# Melly

> A marketplace of Claude Code components for contextual knowledge retrieval

Melly is a marketplace of production-ready Claude Code components that enable intelligent contextual retrieval from knowledge bases. It provides a collection of plugins, skills, agents, and workflows that extend Claude Code with powerful capabilities for codebase analysis, skill development, and documentation generation.

## 🎯 What is Melly?

Melly serves as a central hub for Claude Code components optimized for contextual retrieval and knowledge management. Whether you need to analyze large codebases, develop new skills, or generate comprehensive architectural documentation - Melly provides the tools and components you need.

## 📦 Available Plugins

### Abstractor Agent

Deep architectural analysis of existing codebases through autonomous subagent-driven exploration.

**Key Features:**
- C4 diagrams (Context, Container, Component levels)
- Subsystem catalogs with dependency tracking
- Architectural documentation for stakeholders
- Validation checks for quality assurance

**Repository:** [Cubical6/melly](https://github.com/Cubical6/melly)
**License:** MIT

### Skill Builder

Meta-skill for creating, editing, and converting Claude Code skills.

**Key Features:**
- Create new skills with production-ready patterns
- Improve and refactor existing skills
- Convert sub-agents to skill format
- CLI-first approach with Python patterns

**Repository:** [Cubical6/melly](https://github.com/Cubical6/melly)
**License:** MIT

## 🚀 Installation

```bash
# Clone the Melly repository
git clone https://github.com/Cubical6/melly.git
cd melly

# Install plugins via Claude Code
/plugin add ./plugins/abstractor-agent
/plugin add ./plugins/skill-builder
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **CLAUDE.md** - Implementation guide for agents, skills, commands, and hooks
- **docs/sub-agents.md** - Complete agent guide
- **docs/skills.md** - Skill authoring best practices
- **docs/slash-commands.md** - Command reference
- **docs/hooks.md** - Hook system documentation
- And more...

## 🛠️ Usage

After installation, components are automatically available:

```bash
# Use Abstractor Agent
/system-archaeologist

# Ask Skill Builder for help
"Help me create a skill for AWS Lambda deployment"
```

## 📖 Repository Structure

```
melly/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace definition
├── plugins/                  # Marketplace plugins
│   ├── abstractor-agent/
│   └── skill-builder/
├── docs/                     # Comprehensive documentation
│   ├── sub-agents.md
│   ├── skills.md
│   ├── slash-commands.md
│   └── ...
├── CLAUDE.md                 # Implementation guide
└── README.md                 # This file
```

## 🤝 Contributing

Melly is a community-driven marketplace. Contributions are welcome!

1. Fork the repository
2. Add your plugin to `plugins/`
3. Update `marketplace.json`
4. Create a pull request

## 📄 License

See individual plugin licenses in their respective directories.

## 🔗 Links

- [Melly Marketplace](https://github.com/Cubical6/melly)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)

## 📜 Credits

- **Abstractor Agent** - Based on [Axiom System Archaeologist](https://github.com/Cubical6/skillpacks) by tachyon-beep
- **Skill Builder** - Based on [Skill Builder](https://github.com/Cubical6/skill-builder) by Ken Collins
