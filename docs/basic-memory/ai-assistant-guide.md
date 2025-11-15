# AI Assistant Guide for Basic Memory - Melly Edition

## Overview

This guide teaches AI assistants how to use Basic Memory within the Melly Claude Code environment. Basic Memory is a local-first knowledge management system that creates semantic knowledge graphs from markdown files, enabling persistent, structured knowledge across Claude Code sessions.

**Melly Configuration**: This guide is tailored for the Melly basic-memory plugin, which is pre-configured with optimized defaults for Claude Code workflows.

## Quick Start

The Melly basic-memory plugin is pre-configured with:
- **Default Project**: `main` - automatically selected, no prompting required
- **Project Root**: `${CLAUDE_PROJECT_DIR}/knowledge-base` - all notes stored here
- **Kebab Filenames**: Enabled - note titles automatically converted to kebab-case
- **Sync**: Enabled - real-time file synchronization

**You can start using knowledge management immediately without any setup.**

## Core Architecture

Basic Memory operates on a simple flow:

```
User Markdown Files → File Sync → SQLite Index → MCP Server → Claude Code
```

The system is built on three principles:

1. **Local-First**: Knowledge stored as plain text markdown files in your project
2. **Semantic Knowledge Graph**: Built from entities, observations, and relations
3. **Persistent Context**: Knowledge survives conversations and sessions

## Knowledge Graph Elements

### Entities

Entities are individual markdown files representing concepts. Each entity has:
- **Frontmatter metadata**: Title, tags, timestamps
- **Observations**: Categorized facts about the entity
- **Relations**: Links to other entities

**File location**: All entities are stored in `${CLAUDE_PROJECT_DIR}/knowledge-base/main/`

**Example entity**:
```markdown
---
title: React Hooks
tags: [react, javascript, frontend]
created: 2025-01-15T10:30:00Z
updated: 2025-01-15T14:45:00Z
---

# React Hooks

- [fact] Introduced in React 16.8 #react #hooks
- [technique] useState manages component state #state-management
- [technique] useEffect handles side effects #lifecycle
- [best-practice] Custom hooks enable logic reuse #patterns

- relates_to [[React Components]]
- implements [[JavaScript Closures]]
- part_of [[React Ecosystem]]
```

### Observations

Observations are categorized facts using the syntax: `- [category] content #tags`

**Common categories**:
- `[fact]` - Verifiable information
- `[idea]` - Concepts or proposals
- `[decision]` - Choices made and rationale
- `[technique]` - Methods or approaches
- `[requirement]` - Needs or constraints
- `[question]` - Open questions
- `[insight]` - Realizations or discoveries
- `[problem]` - Issues or challenges
- `[solution]` - Resolutions or fixes
- `[best-practice]` - Recommended patterns

**Tags**: Use hashtags for cross-cutting concerns (e.g., `#security`, `#performance`, `#api`)

### Relations

Relations are directional links between entities using: `- relation_type [[Target Entity]]`

**Common relation types**:
- `relates_to` - General association
- `implements` - Concrete realization
- `requires` - Dependency
- `extends` - Inheritance or expansion
- `part_of` - Composition
- `contrasts_with` - Difference or opposition
- `caused_by` - Causation
- `leads_to` - Consequence
- `similar_to` - Resemblance

**Forward References**: You can reference entities before they exist. Relations automatically resolve when target entities are created.

## Working with Knowledge

### Creating Knowledge Notes

Since default project mode is enabled, you can create notes without specifying a project:

```
> "Save this conversation about React hooks to my knowledge base"
→ Creates: knowledge-base/main/react-hooks.md

> "Create a note about the authentication flow we discussed"
→ Creates: knowledge-base/main/authentication-flow.md
```

**Best practice structure**:
```markdown
---
title: Clear Descriptive Title
tags: [domain, concept, cross-cutting-concern]
---

# Title

## Context
Brief background or overview

## Key Points
- [category] Observation with #tags
- [category] Another observation #tags

## Related Concepts
- relation_type [[Other Entity]]
- relation_type [[Another Entity]]
```

### Reading Knowledge

Read notes by identifier:

```
> "Show me the note about React Hooks"
> "Read the authentication flow note"
```

Responses include:
- **Metadata**: Title, tags, timestamps
- **Content**: Paginated for large notes
- **Relations**: Connected entities

### Searching Knowledge

**Basic search** - Query across all notes:
```
> "What did I learn about error handling?"
> "Search for API design patterns"
```

**Advanced search** - Filter by tags and timeframe:
```
> "Show me notes tagged with 'security' from last week"
> "Find all notes about React from the past month"
```

**Search types**:
- **Semantic**: Natural language understanding
- **Tag-based**: Filter by frontmatter tags
- **Full-text**: Keyword matching

**Response structure**:
- Relevance scores
- Metadata preview
- Content snippets
- Entity identifiers for full access

### Building Context

Build context progressively around entities:

```
> "Show me everything related to the authentication flow"
> "Build context around React Hooks including related concepts"
```

**Depth control**: Context can be expanded to multiple levels of relations
**Timeframe filtering**: Focus on recent or historical knowledge

**Response includes**:
- The target entity
- Related entities at each depth level
- Observations from all entities
- Relation paths showing connections

### Recording Conversations

Capture discussions with user permission:

```
> "Save this conversation to my knowledge base"
> "Create a note about what we just discussed"
```

**Best practices**:
- Ask permission before recording
- Explain what will be saved
- Use descriptive titles
- Add relevant tags
- Create relations to existing knowledge

### Editing Notes

**Supported operations**:
- **Append**: Add content to end
- **Prepend**: Add content to beginning
- **Find-and-replace**: Update specific text
- **Replace sections**: Update markdown sections
- **Add observations**: Insert categorized facts
- **Add relations**: Create new links
- **Bulk updates**: Modify multiple notes

**Example**:
```
> "Add a note about hooks optimization to the React Hooks entity"
> "Update the authentication flow note with the new OAuth details"
```

### Organizing Knowledge

**File paths**: Notes are stored in `knowledge-base/main/` with kebab-case filenames
- "React Hooks" → `react-hooks.md`
- "API Design Patterns" → `api-design-patterns.md`

**Tags**: Use frontmatter tags for categorization and cross-cutting concerns

**Relations**: Create semantic connections between related concepts

## Default Project Workflow

Since `BASIC_MEMORY_DEFAULT_PROJECT_MODE=true`, all operations automatically use the `main` project:

1. **No project selection needed**: All commands work without specifying a project
2. **Consistent storage**: All notes in `knowledge-base/main/`
3. **Simplified workflow**: Focus on content, not project management

**If multi-project support is needed**, users can:
- Disable default project mode in `.mcp.json`
- Use explicit project names in commands
- Organize knowledge into separate collections (work, personal, research)

## Error Handling

Common issues and solutions:

**Entity not found**:
- Verify exact entity title (case-sensitive)
- Try searching first: "Search for notes about [topic]"
- Check if entity exists: "List all notes"

**Forward reference resolution**:
- Relations to non-existent entities are valid
- They automatically resolve when target is created
- No error thrown for forward references

**Empty search results**:
- Try broader search terms
- Check tag spelling
- Use semantic search instead of exact keywords

**Edit conflicts**:
- File changed outside Claude Code
- Solution: Re-read the entity, then retry edit

**Permission errors**:
- File system permissions issue
- Check `knowledge-base/main/` directory permissions

## Advanced Patterns

### Progressive Knowledge Building

Build knowledge incrementally across sessions:

1. **Session 1**: Create initial entity with basic observations
2. **Session 2**: Add relations to related entities
3. **Session 3**: Expand with new insights and techniques
4. **Session 4**: Consolidate and refine

### Knowledge Graph Traversal

Navigate the knowledge graph semantically:

```
> "Show me everything connected to React Hooks"
→ Traverses: React Hooks → React Components → Component Lifecycle → State Management

> "What requires authentication?"
→ Finds: All entities with 'requires [[Authentication]]' relation
```

### Temporal Analysis

Track knowledge evolution over time:

```
> "What have I learned about React in the past month?"
> "Show me recent insights about API design"
```

### Knowledge Validation

Periodically validate knowledge consistency:

- Check for orphaned entities (no relations)
- Identify duplicate or conflicting information
- Verify forward references are resolved
- Update outdated observations

### Automated Documentation

Generate documentation from knowledge graph:

1. Build context around key entities
2. Follow relation paths systematically
3. Organize by semantic structure
4. Export as comprehensive guide

### Knowledge Consolidation

Merge related notes when knowledge overlaps:

1. Identify similar entities via search
2. Compare observations and relations
3. Consolidate into primary entity
4. Redirect relations from deprecated entities

## Best Practices

### 1. Structure Knowledge Semantically

- Use clear, descriptive entity titles
- Choose specific categories for observations
- Create meaningful relation types
- Add relevant tags for cross-cutting concerns

### 2. Search Before Creating

Avoid duplicates:
```
> "Do I have any notes about React Hooks?"
→ If yes, update existing entity
→ If no, create new entity
```

### 3. Use Exact Entity Titles in Relations

Relations must match entity titles exactly:
- Good: `relates_to [[React Hooks]]`
- Bad: `relates_to [[react hooks]]` (case mismatch)
- Bad: `relates_to [[Hooks]]` (incomplete title)

### 4. Build Context Strategically

- Start with specific entities
- Expand depth as needed
- Filter by timeframe when relevant
- Use context to discover connections

### 5. Maintain Consistent Naming

- Follow established naming conventions
- Use kebab-case for filenames (automatic)
- Be consistent with entity titles
- Use standard relation types

### 6. Validate Regularly

Periodic validation ensures quality:
- Check for dead forward references
- Identify orphaned entities
- Update outdated information
- Merge duplicate knowledge

### 7. Update Incrementally

Build knowledge over time:
- Add observations as you learn
- Create relations as connections emerge
- Refine categories and tags
- Consolidate when patterns appear

### 8. Implement Tagging Strategy

Effective tagging enables discovery:
- **Domain tags**: `#react`, `#python`, `#security`
- **Type tags**: `#pattern`, `#tutorial`, `#reference`
- **Status tags**: `#draft`, `#complete`, `#review`
- **Priority tags**: `#important`, `#explore`, `#archive`

### 9. Treat Knowledge as Code

Knowledge should be:
- **Versioned**: Git tracks all changes
- **Reviewed**: Validate accuracy and relevance
- **Refactored**: Improve structure over time
- **Documented**: Include context and rationale

### 10. Respect User Permissions

Always:
- Ask before recording conversations
- Explain what will be saved
- Allow user to review before saving
- Honor user's knowledge ownership

## Integration with Claude Code

### File References

Reference knowledge base files in Claude Code:

```
> "Review the authentication flow at @knowledge-base/main/authentication-flow.md"
> "Compare @knowledge-base/main/api-v1.md with @knowledge-base/main/api-v2.md"
```

### Slash Commands

Create custom slash commands that leverage basic-memory:

```markdown
---
description: Search knowledge base for topic
argument-hint: [search-query]
---

Search the knowledge base for: $1

Use semantic search to find relevant notes, then:
1. List matching entities with identifiers
2. Show key observations from top results
3. Suggest related entities to explore
```

### Hooks Integration

Use hooks to automatically capture knowledge:

**PostToolUse hook example**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this code change should be documented in the knowledge base. If it represents a significant pattern, technique, or decision, suggest creating a knowledge note."
          }
        ]
      }
    ]
  }
}
```

### Agent Collaboration

Create agents that work with the knowledge base:

```markdown
---
name: knowledge-curator
description: Manages and organizes the knowledge base. Use when consolidating knowledge or validating consistency.
---

# Knowledge Curator

You are a knowledge management expert specializing in semantic knowledge graphs.

## Responsibilities

1. **Search for duplicates** before creating new entities
2. **Consolidate** related notes when appropriate
3. **Validate** forward references and relations
4. **Organize** with consistent tags and categories
5. **Suggest** connections between related concepts

## Workflow

When curating knowledge:
1. Search existing knowledge for the topic
2. Identify overlaps and gaps
3. Recommend consolidation or creation
4. Ensure consistent naming and structure
5. Validate all relations resolve correctly
```

## Configuration Reference

### Melly Plugin Settings

Location: `plugins/basic-memory/.mcp.json`

```json
{
  "basic-memory": {
    "command": "uvx",
    "args": ["basic-memory", "mcp"],
    "env": {
      "BASIC_MEMORY_DEFAULT_PROJECT_MODE": "true",
      "BASIC_MEMORY_PROJECT_ROOT": "${CLAUDE_PROJECT_DIR}/knowledge-base",
      "BASIC_MEMORY_KEBAB_FILENAMES": "true",
      "BASIC_MEMORY_DISABLE_PERMALINKS": "true",
      "BASIC_MEMORY_SYNC_CHANGES": "true"
    }
  }
}
```

### Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `BASIC_MEMORY_DEFAULT_PROJECT_MODE` | `true` | Auto-select default project (no prompting) |
| `BASIC_MEMORY_PROJECT_ROOT` | `${CLAUDE_PROJECT_DIR}/knowledge-base` | Root directory for all projects |
| `BASIC_MEMORY_KEBAB_FILENAMES` | `true` | Convert titles to kebab-case filenames |
| `BASIC_MEMORY_DISABLE_PERMALINKS` | `true` | Disable automatic permalink generation |
| `BASIC_MEMORY_SYNC_CHANGES` | `true` | Enable real-time file synchronization |

### Customizing Configuration

To override defaults, modify `plugins/basic-memory/.mcp.json` or set environment variables:

```bash
export BASIC_MEMORY_DEFAULT_PROJECT_MODE=false  # Enable multi-project selection
export BASIC_MEMORY_KEBAB_FILENAMES=false       # Use original filenames
claude
```

## Knowledge Base Structure

```
${CLAUDE_PROJECT_DIR}/
├── knowledge-base/              # Auto-created on first use
│   ├── main/                    # Default project
│   │   ├── react-hooks.md
│   │   ├── authentication-flow.md
│   │   ├── api-design-patterns.md
│   │   └── .basic-memory/       # Project metadata
│   │       ├── index.db         # SQLite index
│   │       └── config.json      # Project config
│   └── [other-projects]/        # If multi-project enabled
└── ...
```

## Troubleshooting

### MCP Server Not Starting

**Symptoms**: Basic-memory tools not available in Claude Code

**Solutions**:
1. Verify installation: `uvx basic-memory --version`
2. Check MCP status: `/mcp` in Claude Code
3. Restart Claude Code (required after plugin installation)
4. Check logs: `claude --debug`

### Tools Not Appearing

**Symptoms**: Claude doesn't have access to basic-memory functions

**Solutions**:
1. Restart Claude Code (always required after installing MCP plugins)
2. Verify plugin is enabled: `/plugin`
3. Check uvx is in PATH: `which uvx`

### Sync Issues

**Symptoms**: Changes not reflected in knowledge base

**Solutions**:
1. Verify `BASIC_MEMORY_SYNC_CHANGES=true` in `.mcp.json`
2. Check file permissions on `knowledge-base/` directory
3. Manually trigger sync in basic-memory CLI if needed

### Entity Not Found

**Symptoms**: Cannot find entity by title

**Solutions**:
1. Check exact title (case-sensitive)
2. Search instead: "Search for notes about [topic]"
3. Verify file exists: `ls knowledge-base/main/`
4. Check for filename mismatch (kebab-case conversion)

## Resources

### Documentation

- **Basic Memory Docs**: https://docs.basicmemory.com/
- **Getting Started**: https://docs.basicmemory.com/getting-started/
- **User Guide**: https://docs.basicmemory.com/user-guide
- **CLI Reference**: https://docs.basicmemory.com/guides/cli-reference
- **Knowledge Format**: https://docs.basicmemory.com/guides/knowledge-format

### Melly Integration

- **Plugin README**: `plugins/basic-memory/README.md`
- **MCP Configuration**: `plugins/basic-memory/.mcp.json`
- **Melly Marketplace**: `README.md`
- **Claude Code MCP Guide**: `docs/claude-code/mcp.md`

### Community

- **Basic Memory GitHub**: https://github.com/basicmachines-co/basic-memory
- **Melly GitHub**: https://github.com/Cubical6/melly
- **Basic Memory Discord**: https://basicmemory.com/discord

## Philosophy

Basic Memory is designed to help humans build **enduring knowledge they'll own forever**, not disposable agent memory. When working with the knowledge base:

1. **User owns the knowledge**: All files are plain markdown in their project
2. **Build for the long term**: Create quality, structured knowledge
3. **Respect user agency**: Always ask permission before recording
4. **Enable discovery**: Use semantic structure to surface connections
5. **Grow incrementally**: Knowledge graphs evolve over time

Your role as an AI assistant is to help users build, organize, and leverage their personal knowledge graph effectively.

---

**Version**: 1.0.0 (Melly Edition)
**Last Updated**: 2025-11-15
**Plugin**: basic-memory@melly v1.0.0
