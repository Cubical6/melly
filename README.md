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

1. **`/melly:init`** - Initialize C4 model exploration
   - Scan repository structure
   - Identify package manifests
   - Generate init.json

2. **`/melly:c1-systems`** - Identify C1 (System Context) level
   - Detect systems from repositories
   - Generate architectural documentation
   - Store in knowledge base via basic-memory

3. **`/melly:c2-containers`** - Identify C2 (Container) level
   - Detect containers within systems
   - Map technology stack
   - Generate container documentation

4. **`/melly:c3-components`** - Identify C3 (Component) level
   - Detect components within containers
   - Analyze code structure
   - Generate component documentation

5. **`/melly:doc-c4model`** - Generate comprehensive documentation
   - Create markdown files from JSON data
   - Populate observations and relations
   - Store in basic-memory knowledge base

6. **`/melly:draw-c4model`** - Draw C4 model diagrams
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
# Install Melly core plugin from marketplace
/plugin install melly@melly

# Optional: Install additional plugins
/plugin install abstractor-agent@melly  # Deep architectural analysis
/plugin install basic-memory@melly      # MCP knowledge base server
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
# Start C4 model workflow
/melly:init

# Analyze system context
/melly:c1-systems

# Use Abstractor Agent for deep architectural analysis (optional plugin)
/system-archaeologist
```

## 📖 Repository Structure

```
melly/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace definition (3 plugins)
├── commands/                 # Slash commands (consolidated)
│   ├── init.md              # /melly:init - Repository exploration
│   ├── c1-systems.md        # /melly:c1-systems - C1 analyzer
│   ├── c2-containers.md     # /melly:c2-containers - C2 analyzer
│   ├── c3-components.md     # /melly:c3-components - C3 analyzer
│   ├── doc-c4model.md       # /melly:doc-c4model - Documentation
│   └── draw-c4model.md      # /melly:draw-c4model - Diagrams
├── agents/                   # Agents for specialized tasks
│   ├── c1-writer/           # C1 documentation generator
│   ├── c2-writer/           # C2 documentation generator
│   ├── c3-writer/           # C3 documentation generator
│   └── c4model-writer/      # General C4 documentation writer
├── skills/                   # C4 methodology skills
│   ├── c4model-c1/          # C1 System Context methodology
│   ├── c4model-c2/          # C2 Container methodology
│   ├── c4model-c3/          # C3 Component methodology
│   ├── c4model-observations/ # Observation documentation
│   └── c4model-relations/   # Relation documentation
├── validation/               # Validation scripts and templates
│   ├── scripts/             # Validation scripts
│   └── templates/           # Documentation templates
├── plugins/                  # Optional marketplace plugins
│   ├── abstractor-agent/    # Optional: Deep architectural analysis
│   └── basic-memory/        # Optional: MCP knowledge base server
├── knowledge-base/           # C4 model knowledge base
│   ├── libraries/           # Framework documentation (e.g., Laravel)
│   ├── systems/             # Generated C4 docs (gitignored)
│   └── templates/           # Markdown templates
├── docs/                     # Comprehensive documentation
│   ├── claude-code/         # Claude Code reference docs
│   ├── c4model/             # C4 model methodology
│   ├── workflow-guide.md    # User workflow guide
│   └── ...
├── CLAUDE.md                 # Implementation guide
├── TASKS.md                  # Development tasks
└── README.md                 # This file
```

### Plugin Categories

**Total: 3 plugins available**

**Core Plugin (1):**
- **melly**: ✅ Complete C4 model workflow with consolidated commands, agents, skills, and validation
  - 6 slash commands (/melly:init, /melly:c1-systems, /melly:c2-containers, etc.)
  - 4 specialized agents (c1-writer, c2-writer, c3-writer, c4model-writer)
  - 5 C4 methodology skills (10,000+ lines of comprehensive guidance)
  - Validation scripts and templates (7 validators, 3 generators)

**Optional Plugins (2):**
- **abstractor-agent**: ✅ System archaeologist for deep codebase exploration
- **basic-memory**: ✅ Knowledge management via MCP server for storing C4 documentation

**Current Status**: All components are functional and follow Claude Code best practices with consolidated single-plugin architecture.

**Legend:** ✅ Implemented and Functional

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
