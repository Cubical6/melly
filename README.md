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

### Basic Memory (MCP Server)

Knowledge management system via MCP for storing and retrieving C4 model documentation.

**Key Features:**
- Create and search knowledge notes
- Multi-project support with sync
- Obsidian canvas integration for visualizations
- Permalink support for stable references

**Repository:** [Cubical6/melly](https://github.com/Cubical6/melly)
**License:** MIT

## 🔄 Melly C4 Model Workflow

Melly provides a complete workflow for reverse engineering codebases using the C4 model methodology:

### Workflow Commands

1. **`/melly-init`** - Initialize C4 model exploration
   - Scan repository structure
   - Identify package manifests
   - Generate init.json

2. **`/melly-c1-systems`** - Identify C1 (System Context) level
   - Detect systems from repositories
   - Generate architectural documentation
   - Store in knowledge base via basic-memory

3. **`/melly-c2-containers`** - Identify C2 (Container) level
   - Detect containers within systems
   - Map technology stack
   - Generate container documentation

4. **`/melly-c3-components`** - Identify C3 (Component) level
   - Detect components within containers
   - Analyze code structure
   - Generate component documentation

5. **`/melly-doc-c4model`** - Generate comprehensive documentation
   - Create markdown files from JSON data
   - Populate observations and relations
   - Store in basic-memory knowledge base

6. **`/melly-draw-c4model`** - Draw C4 model diagrams
   - Create Mermaid diagrams
   - Generate Obsidian canvas files
   - Visualize system architecture

### Knowledge Base Structure

All generated documentation is stored in `knowledge-base/`:
- `systems/` - C4 model documentation (gitignored, auto-generated)
- `libraries/` - Tool and package documentation
- `templates/` - Markdown templates for documentation

## 🚀 Installation

### Prerequisites

Melly requires the following MCP servers for full functionality:

#### Required
- **basic-memory**: Knowledge base storage and retrieval for C4 model documentation
  - Installation: See [plugins/basic-memory](./plugins/basic-memory)
  - Configuration: Enable permalinks and sync in your Claude Code settings

#### Optional
- **context7**: Enhanced contextual information retrieval
  - Installation: Coming soon

### Install Melly

```bash
# Clone the Melly repository
git clone https://github.com/Cubical6/melly.git
cd melly

# Install plugins via Claude Code
/plugin add ./plugins/abstractor-agent
/plugin add ./plugins/skill-builder
/plugin add ./plugins/basic-memory
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **CLAUDE.md** - Implementation guide for agents, skills, commands, and hooks
- **docs/claude-code/sub-agents.md** - Complete agent guide
- **docs/claude-code/skills.md** - Skill authoring best practices
- **docs/claude-code/slash-commands.md** - Command reference
- **docs/claude-code/hooks.md** - Hook system documentation
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
│   └── marketplace.json      # Marketplace definition (18 workflow plugins)
├── plugins/                  # Marketplace plugins
│   ├── abstractor-agent/    # Existing: Deep architectural analysis
│   ├── skill-builder/       # Existing: Meta-skill for skill development
│   ├── basic-memory/        # Existing: MCP knowledge base server
│   │
│   ├── Agents (6):          # C4 workflow agents
│   ├── c4model-explorer/    # Repository exploration and init.json
│   ├── c1-abstractor/       # C1 System Context analyzer
│   ├── c2-abstractor/       # C2 Container analyzer
│   ├── c3-abstractor/       # C3 Component analyzer
│   ├── c4model-writer/      # Documentation generator
│   ├── c4model-drawer/      # C4 diagram drawer
│   │
│   ├── Commands (6):        # C4 workflow slash commands
│   ├── melly-init/          # /melly-init
│   ├── melly-c1-systems/    # /melly-c1-systems
│   ├── melly-c2-containers/ # /melly-c2-containers
│   ├── melly-c3-components/ # /melly-c3-components
│   ├── melly-doc-c4model/   # /melly-doc-c4model
│   ├── melly-draw-c4model/  # /melly-draw-c4model
│   │
│   ├── Skills (5):          # C4 methodology skills
│   ├── c4model-c1/          # C1 System Context methodology
│   ├── c4model-c2/          # C2 Container methodology
│   ├── c4model-c3/          # C3 Component methodology
│   ├── c4model-observations/  # Observation documentation
│   ├── c4model-relations/   # Relation documentation
│   │
│   └── Validation (1):      # Quality assurance
│       └── melly-validation/  # Scripts and templates
├── knowledge-base/           # C4 model knowledge base
│   ├── libraries/           # Tool and package docs
│   ├── systems/             # Generated C4 docs (gitignored)
│   └── templates/           # Markdown templates
├── docs/                     # Comprehensive documentation
│   ├── claude-code/         # Claude Code documentation
│   │   ├── sub-agents.md
│   │   ├── skills.md
│   │   ├── slash-commands.md
│   │   └── ...
│   ├── c4model-methodology.md  # C4 approach guide
│   └── workflow-guide.md    # Melly workflow usage
├── CLAUDE.md                 # Implementation guide
├── TASKS.md                  # Development tasks
└── README.md                 # This file
```

### Plugin Categories

**Total: 5 plugins** (3 existing + 1 validation + 1 skill) | **In Development: 11 workflow plugins**

**Implemented Plugins (5):**
- **abstractor-agent**: ✅ System archaeologist for codebase exploration
- **skill-builder**: ✅ Create and manage skills
- **basic-memory**: ✅ Knowledge management via MCP
- **melly-validation**: ✅ Centralized validation scripts & templates (7 validators, 3 generators)
- **c4model-c1**: ✅ C1 System Context methodology skill (1,558 lines of documentation)

**Workflow Plugins (In Development):**
- **melly-init**: 🔴 Explorer agent, init command
- **melly-c1**: 🔴 C1 abstractor agent, c1-systems command
- **melly-c2**: 🔴 C2 abstractor agent, c2-containers command, C2 methodology skill
- **melly-c3**: 🔴 C3 abstractor agent, c3-components command, C3 methodology skill
- **melly-doc**: 🔴 Writer agent, doc-c4model command, observations/relations skills
- **melly-draw**: 🔴 Drawer agent, draw-c4model command

**Skills (In Development):**
- **c4model-c2**: 🔴 C2 Container methodology skill
- **c4model-c3**: 🔴 C3 Component methodology skill
- **c4model-observations**: 🔴 Observation documentation skill
- **c4model-relations**: 🔴 Relation documentation skill

**Legend:** ✅ Completed | 🔴 In Development

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
