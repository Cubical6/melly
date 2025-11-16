# Library Documentation Validation Scripts

Python validation scripts for the `melly-lib-docs` plugin.

## Scripts Overview

| Script | Purpose | Exit Codes |
|--------|---------|------------|
| `parse-markdown.py` | Universal markdown structure parser | 0=success, 2=error |
| `extract-metadata.py` | Extract observations and relations | 0=success, 2=error |
| `validate-content.py` | Verify content preservation | 0=preserved, 1=warning, 2=error |
| `validate-lib-docs.py` | Validate metadata JSON structure | 0=valid, 1=warning, 2=error |

## Requirements

- Python 3.8+
- No external dependencies (uses stdlib only)

## 1. parse-markdown.py

**Purpose**: Extract structured information from markdown files.

**Usage**:
```bash
./parse-markdown.py <markdown-file> [-v]
```

**Example**:
```bash
./parse-markdown.py docs/laravel/eloquent.md -v
```

**Output**: Parsed structure with headings, code blocks, links, inline code, lists, and blockquotes.

**Key Functions**:
- `parse_markdown_structure(content: str) -> Dict`: Extract all markdown elements
- `parse_file(file_path: Path) -> Optional[Dict]`: Parse file and return structure

## 2. extract-metadata.py

**Purpose**: Extract observations and relations from markdown using universal patterns.

**Usage**:
```bash
./extract-metadata.py <markdown-file> <library-name> <entity-id> [-o output.json]
```

**Example**:
```bash
./extract-metadata.py docs/laravel/eloquent.md laravel laravel-eloquent -o metadata.json
```

**Output**: JSON with observations (version, dependencies, best practices, techniques, examples, warnings) and relations.

**Key Functions**:
- `extract_observations(parsed: Dict, library: str) -> List[Dict]`: Extract observations using regex patterns
- `extract_relations(parsed: Dict, entity_id: str) -> List[Dict]`: Extract relations from links and cross-references

**Observation Categories**:
- `version` - Version information (e.g., "Introduced in X", "Requires Y+")
- `dependency` - Dependencies (e.g., "Requires X", "Depends on Y")
- `best_practice` - Best practices and recommendations
- `technique` - How-to headings and techniques
- `example` - Code examples
- `warning` - Notes, warnings, cautions
- `note` - General notes from blockquotes

**Relation Types**:
- `references` - General references
- `references_section` - Internal anchor links
- `source_code` - GitHub/source code links
- `official_docs` - Official documentation links
- `related_docs` - Internal documentation links
- `external_reference` - External references
- `related` - From "See also" sections
- `mentions` - Text mentions

## 3. validate-content.py

**Purpose**: Verify that original markdown content is 100% preserved in enhanced files.

**Usage**:
```bash
./validate-content.py <original-file> <enhanced-file> [--strict] [-v]
```

**Example**:
```bash
./validate-content.py docs/original/eloquent.md knowledge-base/libraries/laravel/eloquent.md
```

**Output**: Validation result with diff if mismatch detected.

**Key Functions**:
- `validate_content_preservation(original_file: Path, enhanced_file: Path, strict: bool) -> Tuple[bool, str]`: Verify content preservation
- `extract_original_from_enhanced(enhanced_content: str) -> Optional[str]`: Extract original content from enhanced file
- `normalize_whitespace(text: str, strict: bool) -> str`: Normalize whitespace for comparison

**Exit Codes**:
- `0` - Content preserved correctly
- `1` - Warning (minor whitespace differences only)
- `2` - Error (content mismatch)

## 4. validate-lib-docs.py

**Purpose**: Validate the structure and content of `lib-docs-{library}.json` files.

**Usage**:
```bash
./validate-lib-docs.py <json-file> [-v]
```

**Example**:
```bash
./validate-lib-docs.py knowledge-base/libraries/laravel/lib-docs-laravel.json -v
```

**Output**: Validation results with errors and warnings.

**Key Functions**:
- `validate_metadata_json(json_file: Path) -> Tuple[int, List[str], List[str]]`: Validate complete structure

**Validations**:
- Required root fields: `library`, `version`, `source_url`, `entities`, `metadata`
- Required entity fields: `id`, `name`, `type`, `file_path`, `observations`, `tags`
- Required observation fields: `category`, `content`
- Required relation fields: `source`, `target`, `type`
- Entity IDs are unique
- Relations reference valid entities
- Observations have valid categories
- Tags are non-empty arrays
- File paths exist (warning if not found)

**Exit Codes**:
- `0` - Validation passed
- `1` - Warning (non-critical issues)
- `2` - Error (critical validation failure)

## Workflow Integration

### Complete Workflow Example

```bash
# 1. Parse markdown structure
./parse-markdown.py docs/laravel/eloquent.md -v > /tmp/parsed.txt

# 2. Extract metadata
./extract-metadata.py docs/laravel/eloquent.md laravel laravel-eloquent -o /tmp/metadata.json

# 3. Generate enhanced file (done by agent)
# ... agent creates knowledge-base/libraries/laravel/eloquent.md with frontmatter ...

# 4. Validate content preservation
./validate-content.py docs/laravel/eloquent.md knowledge-base/libraries/laravel/eloquent.md

# 5. Validate final metadata JSON (after agent generates lib-docs-laravel.json)
./validate-lib-docs.py knowledge-base/libraries/laravel/lib-docs-laravel.json -v
```

### Exit Code Convention

All scripts follow this convention:
- `0` - Success (validation passed)
- `1` - Warning (non-critical issues, processing can continue)
- `2` - Error (critical failure, processing should stop)

### Usage in Hooks

These scripts can be used in hooks for automated validation:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python plugins/melly-lib-docs/scripts/validate-content.py \"$ORIGINAL\" \"$ENHANCED\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Testing

Run tests with sample markdown:

```bash
# Create test file
cat > /tmp/test.md << 'EOF'
# Test Document

Introduced in Version 2.0, requires Package A.

## How to Use

```python
print("example code")
```

> Note: Important warning here.

Best practice: Always validate input.

## See Also
- [Related Doc](related.md)
