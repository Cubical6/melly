# Knowledge Base Directory

This directory serves as the template for basic-memory knowledge bases. When the basic-memory plugin is installed, it configures the MCP server to store all projects in a `knowledge-base` folder within your Claude Code project directory.

## Directory Structure

When you create projects in basic-memory, they will be organized like this:

```
${CLAUDE_PROJECT_DIR}/knowledge-base/
├── main/                    # Default project
│   ├── note-1.md
│   ├── note-2.md
│   └── .basic-memory/       # Project metadata
├── work/                    # Additional projects
│   └── ...
└── personal/
    └── ...
```

## Default Configuration

The MCP server is pre-configured with:

- **Default Project**: `main` - Automatically selected project
- **Default Project Mode**: `true` - No prompting for project selection
- **Project Root**: `${CLAUDE_PROJECT_DIR}/knowledge-base` - All projects stored here
- **Kebab Filenames**: `true` - Note filenames use kebab-case

## Usage

Create and search notes naturally:

```
> "Save this conversation about React hooks to my knowledge base"
> "Search my notes for API design patterns"
> "Create a note about microservices architecture"
```

Basic-memory will automatically:
1. Use the "main" project by default
2. Store notes in `${CLAUDE_PROJECT_DIR}/knowledge-base/main/`
3. Convert filenames to kebab-case (e.g., "My Note" → "my-note.md")

## Multi-Project Organization

To work with multiple projects:

```
> "Switch to my work project"
> "Create a note in my personal project about..."
> "Search all projects for deployment strategies"
```

## Learn More

- [Basic Memory Documentation](https://docs.basicmemory.com/)
- [User Guide](https://docs.basicmemory.com/user-guide/)
- [CLI Reference](https://docs.basicmemory.com/guides/cli-reference)
