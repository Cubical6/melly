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

1. **`/melly-init`** - Initialize C4 model exploration
   - Scan repository structure
   - Identify package manifests
   - Generate init.json

2. **`/melly-c1-systems`** - Identify C1 (System Context) level
   - Detect systems from repositories
   - Generate architectural documentation
   - Store in knowledge base via basic-memory

3. **`/melly-c2-containers`** ✅ - Identify C2 (Container) level
   - Detect containers within systems
   - Map technology stack
   - Generate container documentation
   - **Status**: Implemented (43 lines, follows best practices)

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
# Use Abstractor Agent for deep architectural analysis
/system-archaeologist

# Start C4 model workflow
/melly-init
```

## 📖 Repository Structure

```
melly/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace definition (16 plugins)
├── plugins/                  # Marketplace plugins
│   ├── abstractor-agent/    # Core: Deep architectural analysis
│   ├── basic-memory/        # Core: MCP knowledge base server
│   ├── melly-validation/    # Validation: Scripts and templates
│   ├── melly-core/          # New: Consolidated core (refactoring)
│   │
│   ├── C4 Workflow (6):     # Complete workflow plugins
│   ├── melly-init/          # /melly-init - Repository exploration
│   ├── melly-c1/            # /melly-c1-systems - C1 analyzer
│   ├── melly-c2/            # /melly-c2-containers - C2 analyzer
│   ├── melly-c3/            # /melly-c3-components - C3 analyzer
│   ├── melly-doc/           # /melly-doc-c4model - Documentation
│   ├── melly-draw/          # /melly-draw-c4model - Diagrams
│   │
│   ├── C4 Skills (5):       # Methodology skills
│   ├── c4model-c1/          # C1 System Context methodology
│   ├── c4model-c2/          # C2 Container methodology
│   ├── c4model-c3/          # C3 Component methodology
│   ├── c4model-observations/  # Observation documentation
│   ├── c4model-relations/   # Relation documentation
│   │
│   ├── c1-abstractor/       # Standalone: Simplified C1 analyzer
│   └── melly-writer-lib/    # Library: Documentation writer utilities
│
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

**Total: 16 plugins implemented**

**Core Infrastructure (2):**
- **abstractor-agent**: ✅ System archaeologist for codebase exploration
- **basic-memory**: ✅ Knowledge management via MCP server

**C4 Workflow Plugins (6) - All Functional:**
- **melly-init**: ✅ Repository exploration and initialization
- **melly-c1**: ✅ C1 System Context analysis
- **melly-c2**: ✅ C2 Container analysis
- **melly-c3**: ✅ C3 Component analysis
- **melly-doc**: ✅ Documentation generation
- **melly-draw**: ✅ Diagram visualization

**C4 Methodology Skills (5):**
- **c4model-c1**: ✅ C1 System Context methodology (1,558 lines)
- **c4model-c2**: ✅ C2 Container methodology (2,318 lines, 20+ tech patterns)
- **c4model-c3**: ✅ C3 Component methodology (2,109 lines, 12 component types)
- **c4model-observations**: ✅ Observation documentation (2,455 lines, 34 categories)
- **c4model-relations**: ✅ Relation documentation (2,619 lines, 48 relation types)

**Validation & Quality (1):**
- **melly-validation**: ✅ Scripts & templates (7 validators, 3 generators, 2,859 lines)

**Refactoring & Utilities (3):**
- **melly-core**: ✅ Consolidated core plugin (new architecture)
- **c1-abstractor**: ✅ Standalone simplified C1 analyzer
- **melly-writer-lib**: ✅ Library documentation writer utilities

**Current Status**: All components are functional. Architectural refactoring in progress to consolidate plugins and follow Claude Code best practices.

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
