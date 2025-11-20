# c4model-writer Agent Workflow Specification

**Version**: 1.0.0
**Date**: 2025-11-15
**Agent**: `c4model-writer`
**Purpose**: Convert JSON files to markdown documentation using basic-memory MCP

---

## Overview

The `c4model-writer` agent converts JSON files (c1-systems.json, c2-containers.json, c3-components.json) into structured markdown documentation using basic-memory MCP for persistent storage. It supports incremental updates, parallel processing, and maintains data integrity throughout the conversion process.

---

## Table of Contents

1. [Agent Workflow Steps](#1-agent-workflow-steps)
2. [JSON to Markdown Conversion](#2-json-to-markdown-conversion)
3. [basic-memory MCP Integration](#3-basic-memory-mcp-integration)
4. [Incremental Update Strategy](#4-incremental-update-strategy)
5. [Template Usage](#5-template-usage)
6. [Error Handling](#6-error-handling)
7. [Complete Examples](#7-complete-examples)

---

## 1. Agent Workflow Steps

### Phase 1: Initialization and Validation

```
1. Accept invocation parameters
   ├─ level: "c1" | "c2" | "c3" | "all"
   ├─ force_regenerate: boolean (default: false)
   └─ output_path: path (default: knowledge-base/systems/)

2. Validate prerequisites
   ├─ Check JSON files exist
   ├─ Validate timestamp ordering (c1 → c2 → c3)
   ├─ Run validation scripts
   └─ Verify basic-memory MCP available

3. Load templates
   ├─ Read c1-markdown-template.md
   ├─ Read c2-markdown-template.md
   └─ Read c3-markdown-template.md
```

### Phase 2: Change Detection (Incremental Updates)

```
4. Detect changed entities
   ├─ Load previous metadata (.melly-doc-metadata.json)
   ├─ Compare JSON timestamps
   ├─ Calculate entity checksums
   └─ Build change map:
      {
        "new": [...],
        "modified": [...],
        "unchanged": [...]
      }

5. Filter entities to process
   ├─ If force_regenerate=true → process all
   ├─ Otherwise → process only new + modified
   └─ Log processing plan
```

### Phase 3: Parallel Markdown Generation

```
6. Process entities in parallel
   ├─ For c1, c2, c3 simultaneously:
   │  ├─ Load JSON data
   │  ├─ Filter entities to process
   │  └─ For each entity in parallel:
   │     ├─ Generate markdown content
   │     ├─ Validate markdown structure
   │     └─ Queue for MCP storage
   └─ Wait for all levels to complete

7. Generate markdown per entity
   ├─ Select template based on level
   ├─ Build frontmatter
   ├─ Generate overview section
   ├─ Transform observations
   ├─ Transform relations
   ├─ Add metadata sections
   └─ Return complete markdown string
```

### Phase 4: basic-memory MCP Storage

```
8. Store markdown via MCP
   ├─ Create/update notes for each entity
   ├─ Organize by level (c1/, c2/, c3/)
   ├─ Set appropriate filenames (kebab-case)
   ├─ Handle MCP errors gracefully
   └─ Confirm successful storage

9. Update generation metadata
   ├─ Record timestamps per entity
   ├─ Store checksums for change detection
   ├─ Save to .melly-doc-metadata.json
   └─ Commit metadata file
```

### Phase 5: Validation and Reporting

```
10. Validate generated markdown
    ├─ Run validate-markdown.py on all files
    ├─ Check frontmatter completeness
    ├─ Verify section structure
    └─ Validate internal links

11. Generate summary report
    ├─ Count: new, modified, unchanged, errors
    ├─ List all generated file paths
    ├─ Report validation issues
    └─ Log completion status
```

---

## 2. JSON to Markdown Conversion

### 2.1 Frontmatter Mapping

| JSON Field | Markdown Frontmatter | Notes |
|------------|---------------------|-------|
| `id` | `id` | Unique identifier |
| `name` | `title` | Display name |
| Level | `level` | "c1" \| "c2" \| "c3" |
| `timestamp` | `last_updated` | ISO 8601 format |
| Generated date | `generated_at` | Current timestamp |
| Checksum | `source_checksum` | For change detection |
| **C1 Specific** | | |
| `repositories` | `repositories` | Array of repo paths |
| **C2 Specific** | | |
| `system` | `parent_system` | Parent system ID |
| `technology` | `technology_stack` | Tech description |
| **C3 Specific** | | |
| `container` | `parent_container` | Parent container ID |
| `path` | `source_path` | Code location |

### 2.2 Section Mapping

#### Overview Section
```markdown
## Overview

{entity.name} is a {level_description}.

**Type**: {entity_type}
**Purpose**: {derived from first observation or description}
```

#### Observations Section

See **[observations-relations-schema.md](./observations-relations-schema.md)** for complete details.

```markdown
## Observations

### {Category}

- {description}
  ```{language}
  // Evidence: {location}
  {snippet}
  ```
  Tags: `{tag1}` `{tag2}`
```

**Conversion Logic:**
1. Group observations by category
2. Sort by severity (critical → warning → info)
3. Generate heading per category
4. Add severity badge for warning/critical
5. Include evidence as code block
6. Add tags as inline badges

#### Relations Section

```markdown
## Relations

| Target | Type | Description | Details |
|--------|------|-------------|---------|
| [[{target}]] | `{type}` | {description} | **Method**: {method}<br>**Auth**: {auth} |
```

**Conversion Logic:**
1. Sort by type, then by target
2. Create table with columns
3. Add wikilink for target (enables navigation)
4. Add protocol details as formatted text

### 2.3 Complete Mapping Example

**Input JSON (c1-systems.json)**:
```json
{
  "systems": [
    {
      "id": "web-app",
      "name": "Web Application",
      "repositories": ["/path/to/frontend"],
      "observations": [
        {
          "id": "obs-001",
          "category": "architectural",
          "severity": "info",
          "description": "React-based SPA",
          "evidence": {
            "type": "file",
            "location": "package.json",
            "snippet": "\"react\": \"^18.2.0\""
          },
          "tags": ["react", "spa"]
        }
      ],
      "relations": [
        {
          "id": "rel-001",
          "source": "web-app",
          "target": "api-server",
          "type": "http-rest",
          "description": "Consumes REST API",
          "protocol": {
            "method": "GET, POST",
            "endpoint": "/api/v1/*",
            "authentication": "JWT"
          }
        }
      ]
    }
  ]
}
```

**Output Markdown**:
```markdown
---
id: web-app
title: Web Application
level: c1
last_updated: 2025-11-15T20:10:00Z
generated_at: 2025-11-15T21:00:00Z
source_checksum: abc123def456
repositories:
  - /path/to/frontend
tags:
  - system
  - c1
  - react
  - spa
---

# Web Application

## Overview

Web Application is a C1 System Context level entity.

**Type**: System

## Observations

### Architectural

- React-based SPA
  ```json
  // Evidence: package.json
  "react": "^18.2.0"
  ```
  Tags: `react` `spa`

## Relations

| Target | Type | Description | Details |
|--------|------|-------------|---------|
| [[api-server]] | `http-rest` | Consumes REST API | **Method**: GET, POST<br>**Endpoint**: `/api/v1/*`<br>**Auth**: JWT |

## Metadata

**Source**: c1-systems.json
**Generated**: 2025-11-15T21:00:00Z
```

---

## 3. basic-memory MCP Integration

### 3.1 Required MCP Operations

#### Create/Update Notes

```typescript
// Store entity markdown via basic-memory MCP
function store_entity_markdown(level, entity, markdown_content) {
  const system_folder = get_system_folder(entity);
  const note_path = `${level}/${entity.id}`;

  const result = basic_memory_create_note({
    project: "main",
    title: entity.name,
    content: markdown_content,
    path: note_path,
    tags: [level, "c4model", "auto-generated"]
  });

  return result;
}
```

#### Note Organization

```
knowledge-base/
├── main/                    # Default basic-memory project
│   ├── system-1/
│   │   ├── c1/
│   │   │   └── system-1.md
│   │   ├── c2/
│   │   │   ├── container-1.md
│   │   │   └── container-2.md
│   │   └── c3/
│   │       ├── component-1.md
│   │       └── component-2.md
│   └── system-2/
│       └── ...
└── .basic-memory/
    └── project.json
```

### 3.2 MCP Error Handling

```python
def safe_mcp_operation(operation, *args, **kwargs):
    """Wrapper for MCP operations with error handling"""

    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            result = operation(*args, **kwargs)
            return {"success": True, "data": result}

        except MCPConnectionError as e:
            if attempt < max_retries - 1:
                wait(retry_delay * (attempt + 1))
                continue
            return {"success": False, "error": "MCP connection failed"}

        except MCPAuthError as e:
            return {"success": False, "error": "MCP authentication failed"}

    return {"success": False, "error": "Max retries exceeded"}
```

---

## 4. Incremental Update Strategy

### 4.1 Change Detection Algorithm

```python
def detect_entity_changes(json_data, previous_metadata):
    """
    Detect which entities changed since last generation

    Returns:
        {
            "new": [...],
            "modified": [...],
            "unchanged": [...]
        }
    """

    changes = {"new": [], "modified": [], "unchanged": []}

    current_entities = get_entities_from_json(json_data)

    for entity in current_entities:
        entity_id = entity['id']
        current_checksum = calculate_entity_checksum(entity)

        if entity_id not in previous_metadata:
            changes["new"].append(entity)
            continue

        previous_checksum = previous_metadata[entity_id].get('checksum')

        if current_checksum != previous_checksum:
            changes["modified"].append(entity)
        else:
            changes["unchanged"].append(entity)

    return changes


def calculate_entity_checksum(entity):
    """Calculate SHA-256 checksum for change detection"""
    import hashlib
    import json

    stable_json = json.dumps(entity, sort_keys=True)
    checksum = hashlib.sha256(stable_json.encode()).hexdigest()

    return checksum
```

### 4.2 Metadata Storage Format

**File**: `.melly-doc-metadata.json`

```json
{
  "last_generation": "2025-11-15T21:00:00Z",
  "version": "1.0",
  "entities": {
    "c1": {
      "web-app": {
        "checksum": "abc123def456",
        "last_updated": "2025-11-15T20:10:00Z",
        "markdown_path": "knowledge-base/main/web-app/c1/web-application.md",
        "generated_at": "2025-11-15T21:00:00Z"
      }
    },
    "c2": {
      "frontend-spa": {
        "checksum": "xyz789ghi012",
        "last_updated": "2025-11-15T20:20:00Z",
        "markdown_path": "knowledge-base/main/web-app/c2/frontend-spa.md",
        "generated_at": "2025-11-15T21:00:00Z"
      }
    }
  },
  "json_timestamps": {
    "init": "2025-11-15T20:00:00Z",
    "c1": "2025-11-15T20:10:00Z",
    "c2": "2025-11-15T20:20:00Z",
    "c3": "2025-11-15T20:30:00Z"
  }
}
```

### 4.3 Preserving Manual Edits

```python
def merge_manual_edits(generated_markdown, existing_markdown):
    """
    Preserve manually added sections when updating

    Strategy:
    1. Parse both into sections
    2. Identify manual sections (not in template)
    3. Merge generated + manual sections
    4. Preserve manual edits in overlapping sections
    """

    generated_sections = parse_markdown_sections(generated_markdown)
    existing_sections = parse_markdown_sections(existing_markdown)

    standard_sections = get_template_section_names()
    manual_sections = {
        name: content
        for name, content in existing_sections.items()
        if name not in standard_sections
    }

    merged = {}
    merged.update(generated_sections)
    merged.update(manual_sections)

    return reconstruct_markdown(merged)
```

---

## 5. Template Usage

### 5.1 Template Structure

Templates define the structure of generated documentation:

**File**: `${CLAUDE_PLUGIN_ROOT}/validation/templates/c1-markdown-template.md`

```markdown
---
id: {{entity.id}}
title: {{entity.name}}
level: c1
last_updated: {{json.timestamp}}
generated_at: {{generation.timestamp}}
source_checksum: {{entity.checksum}}
repositories: {{entity.repositories}}
tags: [system, c1, auto-generated]
---

# {{entity.name}}

## Overview

{{entity.name}} is a C1 System Context level entity.

**Type**: System
**Purpose**: {{entity.observations[0] || "System purpose"}}

## Observations

{{#each entity.observations}}
- {{this.description}}
  {{#if this.evidence}}
  ```{{this.evidence.type}}
  // Evidence: {{this.evidence.location}}
  {{this.evidence.snippet}}
  ```
  {{/if}}
  Tags: {{#each this.tags}}`{{this}}`{{/each}}
{{/each}}

## Relations

| Target | Type | Description | Details |
|--------|------|-------------|---------|
{{#each entity.relations}}
| [[{{this.target}}]] | `{{this.type}}` | {{this.description}} | {{render_protocol this.protocol}} |
{{/each}}

## Metadata

**Source**: c1-systems.json
**Generated**: {{generation.timestamp}}
```

### 5.2 Placeholder Variables

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{entity.id}}` | Entity ID | "web-app" |
| `{{entity.name}}` | Display name | "Web Application" |
| `{{entity.observations}}` | Array of observations | [...] |
| `{{json.timestamp}}` | Source JSON timestamp | "2025-11-15T20:10:00Z" |
| `{{generation.timestamp}}` | Current time | "2025-11-15T21:00:00Z" |
| `{{entity.checksum}}` | SHA-256 checksum | "abc123..." |

### 5.3 Template Processing

```python
def apply_template(template_content, entity_data, metadata):
    """Process template with entity data"""

    context = {
        "entity": entity_data,
        "json": {"timestamp": get_json_timestamp(entity_data)},
        "generation": {"timestamp": metadata['generated_at']}
    }

    result = template_content

    # Replace simple placeholders
    for key, value in flatten_context(context).items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value))

    # Process loops ({{#each X}})
    result = process_loops(result, context)

    # Process conditionals ({{#if X}})
    result = process_conditionals(result, context)

    return result
```

---

## 6. Error Handling

### 6.1 Error Categories

#### 1. Input Validation Errors (Blocking)

```python
def validate_inputs(level, json_files):
    """Validate all inputs before processing"""

    errors = []

    # Check files exist
    for json_file in json_files:
        if not file_exists(json_file):
            errors.append(f"Missing: {json_file}")

    # Run validation scripts
    validation_results = run_validation_scripts(level)
    for result in validation_results:
        if result['exit_code'] == 2:
            errors.append(f"Validation failed: {result['stderr']}")

    # Check timestamp ordering
    if not verify_timestamp_order(json_files):
        errors.append("Timestamp order invalid")

    if errors:
        raise ValidationError("\n".join(errors))
```

#### 2. MCP Connection Errors (Retryable)

```python
def handle_mcp_error(error, entity, retry_count=0):
    """Handle MCP errors with retry logic"""

    max_retries = 3

    if retry_count >= max_retries:
        return {
            "success": False,
            "entity_id": entity['id'],
            "error": "MCP storage failed",
            "action": "skip"
        }

    # Exponential backoff
    wait_time = 2 ** retry_count
    sleep(wait_time)

    return retry_mcp_storage(entity, retry_count + 1)
```

#### 3. Template Processing Errors (Recoverable)

```python
def handle_template_error(error, entity):
    """Handle template errors with fallback"""

    try:
        # Try minimal markdown fallback
        fallback_markdown = generate_minimal_markdown(entity)
        return {
            "success": True,
            "markdown": fallback_markdown,
            "warning": "Used fallback template"
        }
    except Exception as e:
        return {
            "success": False,
            "entity_id": entity['id'],
            "error": f"Template error: {error}"
        }
```

### 6.2 Error Recovery Workflow

```
1. Validation Error (Exit 2)
   └─> Stop processing, return error report

2. MCP Connection Error
   ├─> Retry 3x with exponential backoff
   ├─> If fail → skip entity, log error
   └─> Continue with remaining entities

3. Template Processing Error
   ├─> Try fallback: minimal markdown
   ├─> If success → log warning, proceed
   └─> If fail → skip entity, log error

4. Partial Failure Handling
   ├─> Continue processing other entities
   ├─> Collect all errors/warnings
   └─> Generate summary report
```

---

## 7. Complete Examples

### Example 1: Incremental Update Detection

**Previous Metadata**:
```json
{
  "entities": {
    "c1": {
      "payment-system": {
        "checksum": "abc123",
        "last_updated": "2025-11-15T20:10:00Z"
      },
      "order-system": {
        "checksum": "def456",
        "last_updated": "2025-11-15T20:10:00Z"
      }
    }
  }
}
```

**Current c1-systems.json**:
- `payment-system`: observations added (checksum changed → "xyz789")
- `order-system`: no changes (checksum same → "def456")
- `inventory-system`: NEW system

**Change Detection Result**:
```json
{
  "new": ["inventory-system"],
  "modified": ["payment-system"],
  "unchanged": ["order-system"]
}
```

**Processing Plan**:
```
Processing 2 entities (1 new, 1 modified)
Skipping 1 unchanged entity

Entities to process:
  ✓ payment-system (modified)
  ✓ inventory-system (new)

Entities to skip:
  - order-system (unchanged)
```

### Example 2: Summary Report

```
Summary Report
--------------

Entities Processed:
  - Total: 12
  - Skipped (unchanged): 5

Storage Results:
  - Successful: 11
  - Failed: 1 (auth-component: MCP timeout)

Validation:
  - Errors: 0
  - Warnings: 2 (missing observations)

Generated Files:
  ✓ knowledge-base/main/payment-system/c1/payment-system.md
  ✓ knowledge-base/main/payment-system/c2/api-server.md
  ✓ knowledge-base/main/payment-system/c3/payment-controller.md
  ✗ knowledge-base/main/auth-system/c3/auth-component.md (MCP timeout)
```

---

## Conclusion

This workflow specification provides:

✅ **Sequential Processing** - 5 clear phases with validation
✅ **Comprehensive Mapping** - JSON-to-Markdown conversion
✅ **MCP Integration** - basic-memory storage with error handling
✅ **Incremental Updates** - Checksum-based change detection
✅ **Template System** - Flexible markdown generation
✅ **Robust Error Handling** - Recovery procedures
✅ **Concrete Examples** - Real-world usage

---

**Document Version**: 1.0.0
**Date**: 2025-11-15
**Status**: Workflow Design Complete - Ready for Implementation
