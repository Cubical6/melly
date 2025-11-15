# Basic Memory Plugin

> Knowledge management system for Claude Code - create, search, and sync knowledge notes across projects

## Overview

Basic Memory is an open-source knowledge management system that integrates with Claude Code via the Model Context Protocol (MCP). This plugin automatically configures the basic-memory MCP server, enabling powerful knowledge management capabilities directly within your Claude Code workflows.

## Features

- **Multi-project support**: Organize knowledge into separate collections (work, personal, research)
- **Real-time sync**: Automatic synchronization across devices
- **Knowledge note creation**: Generate structured notes with tags and relationships
- **Search capabilities**: Query your knowledge base including frontmatter tags
- **Special prompts**: "Continue Conversation," "Recent Activity," and "Search" triggers
- **Direct references**: Use `memory://` URLs with permalinks for precise context
- **Import conversations**: Support for importing Claude and ChatGPT histories

## Prerequisites

Before using this plugin, you need to install basic-memory on your system:

### Installation

**Single-Step (Recommended):**
```bash
curl -LsSf https://basicmemory.com/install/latest.sh | sh
```

**Universal Installation:**
```bash
uv tool install basic-memory
```

**macOS via Homebrew:**
```bash
brew tap basicmachines-co/basic-memory
brew install basic-memory
```

## Plugin Installation

This plugin is available through the Melly marketplace:

```bash
# Add Melly marketplace if not already added
/plugin marketplace add Cubical6/melly

# Install basic-memory plugin
/plugin install basic-memory@melly
```

After installation, restart Claude Code to activate the MCP server.

## Usage

Once the plugin is installed and Claude Code is restarted, you can use basic-memory features naturally:

### Create Knowledge Notes

```
> "Save this conversation about React hooks to my knowledge base"
> "Create a note about the authentication flow we just discussed"
```

### Search Your Knowledge

```
> "What did I learn about error handling last week?"
> "Search my notes for information about API design"
```

### Multi-Project Organization

```
> "Switch to my personal knowledge project"
> "Show me notes tagged with 'architecture' in the work project"
```

### Continue Conversations

```
> "Continue our conversation about microservices"
```

### Direct References

```
> "Review the note at memory://abc123"
```

## Configuration

The MCP server is automatically configured when this plugin is installed. The configuration uses:

- **Transport**: stdio
- **Command**: `uvx basic-memory mcp`
- **No authentication required**: Local-first knowledge management

## Documentation

For complete basic-memory documentation:

- **Getting Started**: https://docs.basicmemory.com/getting-started/
- **User Guide**: https://docs.basicmemory.com/user-guide
- **CLI Reference**: https://docs.basicmemory.com/guides/cli-reference
- **Cloud Setup**: https://docs.basicmemory.com/guides/cloud
- **Obsidian Integration**: https://docs.basicmemory.com/integrations/obsidian
- **Knowledge Format**: https://docs.basicmemory.com/guides/knowledge-format

## Troubleshooting

### MCP Server Not Starting

If the basic-memory MCP server doesn't start:

1. **Verify installation**: Run `uvx basic-memory --version`
2. **Check MCP status**: Use `/mcp` command in Claude Code
3. **Restart Claude Code**: MCP servers require restart after plugin installation
4. **Check logs**: Run Claude Code with `--debug` flag

### Tools Not Available

If basic-memory tools don't appear:

1. **Restart required**: Always restart Claude Code after installing plugins with MCP servers
2. **Check plugin status**: Use `/plugin` to verify the plugin is enabled
3. **Verify uvx**: Ensure `uvx` is in your PATH

## Version

**Version**: 1.0.0
**License**: MIT
**Repository**: https://github.com/Cubical6/melly

## Credits

- **Basic Memory**: Created by [Basic Machines Co.](https://basicmemory.com)
- **Plugin Integration**: Melly Team

## See Also

- [Model Context Protocol (MCP) Documentation](/docs/claude-code/mcp.md)
- [Plugin Development Guide](/docs/claude-code/plugins.md)
- [Melly Marketplace](/README.md)
