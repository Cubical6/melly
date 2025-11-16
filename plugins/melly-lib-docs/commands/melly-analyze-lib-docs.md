---
description: Analyze library documentation and extract metadata for semantic search
argument-hint: [library-name] [docs-path]
allowed-tools: Task, Read, Write, Bash, Glob, Grep
---

# Library Documentation Analysis

Analyze markdown-based library documentation and extract observations and relations for semantic search.

## Arguments

- `$1` - **Library name** (required): Name of the library (e.g., laravel, react, django)
- `$2` - **Documentation path** (optional): Path to library docs
  - Default: `knowledge-base/libraries/$1/`
  - Supports absolute or relative paths

## Workflow

### Phase 1: Validation

1. **Validate arguments**:
   - Library name is required
   - If no path provided, use default: `knowledge-base/libraries/$1/`
   - Verify documentation path exists
   - Check for markdown files in path

2. **Verify dependencies**:
   - basic-memory MCP server is available
   - Validation scripts exist in plugin

### Phase 2: Analysis

3. **Invoke lib-doc-analyzer agent**:
   
   Explicitly invoke the lib-doc-analyzer agent to perform the analysis:
   
   ```
   Use the lib-doc-analyzer agent to analyze the $1 library documentation.
   
   Agent context:
   - Library name: $1
   - Documentation path: $2 (or knowledge-base/libraries/$1/ if not specified)
   - Task: Analyze all markdown files and extract observations and relations
   - Skill: Use the lib-doc-methodology skill for guidance
   ```
   
   **Alternative invocation patterns:**
   
   ```
   Have the lib-doc-analyzer agent process the library documentation at $2.
   Extract metadata from $1 documentation using the lib-doc-analyzer agent.
   Ask lib-doc-analyzer to analyze library docs for $1 at $2.
   ```
   
   **What the agent will do:**
   - Automatically follow the 5-phase workflow defined in its system prompt
   - Use the lib-doc-methodology skill for extraction rules
   - Generate enhanced markdown files with frontmatter
   - Create lib-docs-$1.json metadata file
   - Run validation scripts to verify quality


4. **Agent performs 5-phase workflow**:
   - Discovery: Find all markdown files
   - Parsing: Extract structure (headings, code, links)
   - Analysis: Extract observations and relations
   - Generation: Create enhanced markdown files
   - Validation: Verify content preservation

### Phase 3: Validation

5. **Run validation scripts**:
   ```bash
   # Validate metadata JSON
   python3 plugins/melly-lib-docs/scripts/validate-lib-docs.py lib-docs-$1.json
   
   # Verify content preservation
   python3 plugins/melly-lib-docs/scripts/validate-content.py $2
   ```

6. **Check validation results**:
   - Exit code 0: Success
   - Exit code 1: Warnings (continue with caution)
   - Exit code 2: Blocking errors (stop workflow)

### Phase 4: Integration

7. **Store in basic-memory**:
   - Create knowledge entities for each enhanced markdown file
   - Include metadata (observations, relations) in entity
   - Generate permalinks for cross-referencing

8. **Generate metadata file**:
   - Create `lib-docs-$1.json` with complete metadata
   - Include library info, entities, relationships, statistics
   - Store in documentation path

### Phase 5: Reporting

9. **Generate summary report**:
   ```
   ✅ Library Documentation Analysis Complete
   
   Library: [Library Name Version]
   Path: [Documentation Path]
   ---
   📊 Statistics:
     Files processed: [count]
     Observations: [count]
     Relations: [count]
     Total chunks: [count]
     Avg chunk size: [words]
   
   📁 Output:
     Enhanced files: [path]/**/*.md
     Metadata: lib-docs-[name].json
     basic-memory entities: [count] created
   
   ✅ Validation:
     Content preservation: [passed/total] passed
     Metadata quality: Valid
   
   💡 Next Steps:
     1. Search: "What is [concept] in [library]?"
     2. Build context: "Show me [library] [topic] concepts"
     3. Navigate: Open enhanced markdown files in Obsidian
   ```

## Examples

```bash
# Analyze Laravel documentation (default path)
/melly-analyze-lib-docs laravel

# Analyze React documentation (default path)
/melly-analyze-lib-docs react

# Analyze Django with custom path
/melly-analyze-lib-docs django /path/to/django-docs

# Analyze Laravel 11.x with explicit path
/melly-analyze-lib-docs laravel-11 knowledge-base/libraries/laravel-11/
```

## Error Handling

### Missing library name:
```
❌ Error: Library name is required
Usage: /melly-analyze-lib-docs [library-name] [docs-path]
Example: /melly-analyze-lib-docs laravel
```

### Documentation path not found:
```
❌ Error: Documentation path not found
Path: knowledge-base/libraries/[name]/
Please ensure the documentation exists or provide a custom path.
```

### No markdown files found:
```
❌ Error: No markdown files found in documentation path
Path: [path]
Expected: At least one .md file in the directory
```

### Validation failure:
```
❌ Validation Error: Content preservation failed
File: [filename]
Issue: Enhanced content differs from original
Action: Review agent output and try again
```

### basic-memory unavailable:
```
⚠️  Warning: basic-memory MCP server not available
Analysis will continue, but entities won't be stored for semantic search.
Metadata will still be generated in lib-docs-[name].json
```

## Output Structure

### Enhanced Markdown Files
Each original markdown file is enhanced with:
- **Frontmatter**: Library metadata (name, version, url, file info)
- **Metadata Section**: Observations and relations extracted from content
- **Separator**: `---` to separate metadata from original content
- **Original Content**: 100% preserved, byte-for-byte identical

### Metadata JSON File
`lib-docs-[library-name].json` contains:
- **library**: Library information (name, version, url, stats)
- **entities**: Array of enhanced files with metadata
- **relationships**: Cross-file relations discovered
- **analyzed_at**: Timestamp of analysis

### basic-memory Entities
Each enhanced markdown file becomes a searchable entity:
- **Content**: Original markdown content
- **Metadata**: Observations and relations
- **Permalink**: Stable reference for cross-linking

## Best Practices

1. **Organize documentation**:
   - Use standard path: `knowledge-base/libraries/[name]/`
   - Keep original structure (don't flatten)
   - Preserve version information

2. **Incremental updates**:
   - Re-analyze when docs are updated
   - Metadata will be regenerated
   - basic-memory entities will be updated

3. **Quality validation**:
   - Always review validation output
   - Check content preservation results
   - Verify observations are extracted, not fabricated

4. **Semantic search**:
   - Use natural language queries
   - Reference concepts by name
   - Build context from multiple entities

5. **Integration with C4 model**:
   - Library docs inform C2 (Container) analysis
   - Technical decisions reference library capabilities
   - Architectural patterns link to library features

## Troubleshooting

### Agent doesn't activate
**Cause**: lib-doc-analyzer agent not found
**Solution**: Ensure agent exists in `plugins/melly-lib-docs/agents/`

### Skill not used
**Cause**: lib-doc-methodology skill not loaded
**Solution**: Check `plugins/melly-lib-docs/skills/lib-doc-methodology/SKILL.md` exists

### Validation scripts fail
**Cause**: Python dependencies missing
**Solution**: Install required packages (see plugin README.md)

### basic-memory errors
**Cause**: MCP server configuration issue
**Solution**: Verify basic-memory in `~/.claude/settings.json`

## Dependencies

- **Agent**: lib-doc-analyzer
- **Skill**: lib-doc-methodology
- **Scripts**: validate-lib-docs.py, validate-content.py
- **MCP Server**: basic-memory (optional but recommended)
- **Python**: 3.8+ with required packages

## Related Commands

- `/melly-init` - Initialize C4 model exploration
- `/melly-c2-containers` - Analyze C2 containers (uses library knowledge)
- `/melly-doc-c4model` - Generate C4 documentation (references library docs)

---

**Version**: 1.0.0
**Plugin**: melly-lib-docs
**Category**: knowledge-extraction
