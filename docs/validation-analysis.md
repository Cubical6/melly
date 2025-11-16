# Melly Validation Scripts Analysis

## Executive Summary

The melly-validation plugin contains **10 scripts** (7 validation/utility + 3 generation):
- **3 scripts are FULLY IMPLEMENTED** with complete logic (markdown generation)
- **7 scripts are PLACEHOLDER STUBS** awaiting implementation (validation + utility)
- **Dependencies**: jsonschema, pyyaml, python-dateutil
- **Exit code convention**: 0 (success), 1 (warning), 2 (blocking error)

---

## 1. VALIDATION SCRIPTS (7 total - ALL STUBS)

### 1.1 validate-init.py
**Status**: STUB - NOT IMPLEMENTED
**Purpose**: Validate `init.json` structure from repository exploration phase
**Expected Input**: `init.json` file path
**Expected Output**: Exit code indicating validation result
**Error Handling**: None yet
**Exit Codes**:
- 0: Valid init.json
- 1: Non-blocking warnings (e.g., missing optional fields)
- 2: Invalid JSON structure

**Should Validate**:
- [ ] JSON structure conforms to init-template.json
- [ ] `metadata.schema_version` exists and is "1.0.0"
- [ ] `metadata.timestamp` is valid ISO 8601
- [ ] `metadata.generator` is "melly-workflow"
- [ ] `repositories` array exists (can be empty)
- [ ] All repository entries have required fields

**Dependencies**:
- Standard library (json, sys)
- jsonschema (for schema validation)

---

### 1.2 validate-c1-systems.py
**Status**: STUB - NOT IMPLEMENTED
**Purpose**: Validate `c1-systems.json` structure from C1 analysis phase
**Expected Input**: `c1-systems.json` file path
**Expected Output**: Exit code indicating validation result
**Error Handling**: None yet
**Exit Codes**:
- 0: Valid c1-systems.json
- 1: Non-blocking warnings
- 2: Invalid structure

**Should Validate**:
- [ ] JSON structure matches c1-systems-template.json
- [ ] `metadata.schema_version` is "1.0.0"
- [ ] `metadata.timestamp` exists and is later than parent (init.json)
- [ ] `systems` array exists (can be empty)
- [ ] Each system has: `id`, `name`, `type`, `boundaries`, `repositories`
- [ ] Observations (if present) have: `description`, `category`, `severity`
- [ ] Relations (if present) have: `target`, `type`, `direction`

**Dependencies**:
- Standard library (json, sys)
- jsonschema
- python-dateutil (for timestamp comparison)

---

### 1.3 validate-c2-containers.py
**Status**: STUB - NOT IMPLEMENTED
**Purpose**: Validate `c2-containers.json` structure from C2 analysis phase
**Expected Input**: `c2-containers.json` file path
**Expected Output**: Exit code indicating validation result
**Error Handling**: None yet
**Exit Codes**:
- 0: Valid c2-containers.json
- 1: Non-blocking warnings
- 2: Invalid structure

**Should Validate**:
- [ ] JSON structure matches c2-containers-template.json
- [ ] `metadata.schema_version` is "1.0.0"
- [ ] `metadata.timestamp` is later than parent (c1-systems.json)
- [ ] `containers` array exists (can be empty)
- [ ] Each container has: `id`, `name`, `system_id`, `type`, `responsibility`
- [ ] Technology stack fields: `primary_language`, `framework`, `libraries[]`
- [ ] Runtime fields: `environment`, `platform`, `containerized`, `container_technology`
- [ ] All container `system_id` values exist in c1-systems.json

**Dependencies**:
- Standard library (json, sys)
- jsonschema
- python-dateutil (for timestamp validation)

---

### 1.4 validate-c3-components.py
**Status**: STUB - NOT IMPLEMENTED
**Purpose**: Validate `c3-components.json` structure from C3 analysis phase
**Expected Input**: `c3-components.json` file path
**Expected Output**: Exit code indicating validation result
**Error Handling**: None yet
**Exit Codes**:
- 0: Valid c3-components.json
- 1: Non-blocking warnings
- 2: Invalid structure

**Should Validate**:
- [ ] JSON structure matches c3-components-template.json
- [ ] `metadata.schema_version` is "1.0.0"
- [ ] `metadata.timestamp` is later than parent (c2-containers.json)
- [ ] `components` array exists (can be empty)
- [ ] Each component has: `id`, `name`, `container_id`, `type`, `responsibility`
- [ ] Code structure fields: `path`, `language`, `files[]`, `exports[]`
- [ ] Design patterns fields (if present): `name`, `category`, `description`
- [ ] Metrics fields (if present): `lines_of_code`, `cyclomatic_complexity`, `test_coverage`
- [ ] All component `container_id` values exist in c2-containers.json

**Dependencies**:
- Standard library (json, sys)
- jsonschema
- python-dateutil

---

### 1.5 validate-markdown.py
**Status**: STUB - NOT IMPLEMENTED
**Purpose**: Validate generated markdown files for correctness and completeness
**Expected Input**: One or more markdown file paths (glob pattern support)
**Expected Output**: Exit code indicating validation result
**Error Handling**: None yet
**Exit Codes**:
- 0: All markdown files valid
- 1: Non-blocking issues (e.g., missing optional sections)
- 2: Critical markdown issues

**Should Validate**:
- [ ] Markdown file exists and is readable
- [ ] YAML frontmatter is valid (id, title, level, type, generated)
- [ ] Required sections present: Overview, Observations, Relations, Metadata
- [ ] No duplicate sections
- [ ] Heading hierarchy is correct (## sections under #)
- [ ] Code blocks are properly closed
- [ ] Links are valid (no broken references)
- [ ] Table formatting is correct (proper markdown table syntax)

**Dependencies**:
- Standard library (json, sys, pathlib)
- pyyaml (for frontmatter parsing)

---

### 1.6 check-timestamp.sh
**Status**: STUB - NOT IMPLEMENTED
**Purpose**: Validate timestamp ordering across JSON workflow files
**Expected Input**: Path to directory containing JSON files or explicit file paths
**Expected Output**: Exit code indicating timestamp validity
**Error Handling**: None yet
**Exit Codes**:
- 0: Timestamps valid and in order
- 1: Warnings about timestamp drift
- 2: Invalid timestamp ordering (blocking)

**Should Validate**:
- [ ] init.json timestamp exists
- [ ] c1-systems.json timestamp >= init.json timestamp
- [ ] c2-containers.json timestamp >= c1-systems.json timestamp
- [ ] c3-components.json timestamp >= c2-containers.json timestamp
- [ ] Timestamps are valid ISO 8601 format
- [ ] Time gaps are reasonable (not too large, not negative)

**Dependencies**:
- Bash builtins
- Standard Unix tools: date, jq

---

### 1.7 create-folders.sh
**Status**: STUB - NOT IMPLEMENTED
**Purpose**: Create directory structure for generated documentation
**Expected Input**: JSON file path or directory name
**Expected Output**: Directory structure created
**Error Handling**: None yet
**Exit Codes**:
- 0: Directories created successfully
- 1: Warnings (e.g., directories already exist)
- 2: Error (unable to create directories)

**Should Create**:
- [ ] `knowledge-base/systems/` (root)
- [ ] `knowledge-base/systems/{system-id}/` for each system in c1-systems.json
- [ ] `knowledge-base/systems/{system-id}/c1/` for C1 documentation
- [ ] `knowledge-base/systems/{system-id}/c2/` for C2 documentation
- [ ] `knowledge-base/systems/{system-id}/c3/` for C3 documentation

**Dependencies**:
- Bash builtins
- Standard Unix tools: mkdir, jq

---

## 2. GENERATION SCRIPTS (3 total - ALL IMPLEMENTED)

### 2.1 generate-c1-markdown.py ✓ COMPLETE
**Status**: FULLY IMPLEMENTED
**Purpose**: Generate C1 (System Context) markdown from c1-systems.json
**Input**: `c1-systems.json` file path
**Output**: Markdown files in `knowledge-base/systems/{system-id}/c1/README.md`

**Exit Codes**:
- 0: Success - all C1 systems converted
- 1: Warning - no systems in JSON (still exits 0)
- 2: Blocking error - file not found or invalid JSON

**Features Implemented**:
- ✓ YAML frontmatter generation (always same structure)
- ✓ Overview section with type, scope, repositories
- ✓ Observations section (grouped by category, sorted by severity)
- ✓ Relations section (markdown table format)
- ✓ Metadata section with source info
- ✓ Evidence snippets with language type
- ✓ Severity icons (🔴 critical, ⚠️ warning, ℹ️ info)
- ✓ Directory creation (parents=True)
- ✓ Proper error handling for missing files

**Code Quality**:
- Well-structured with separate functions for each section
- Clear docstrings
- Proper error messages
- Handles missing/empty data gracefully

**Dependencies**:
- Standard library: json, sys, pathlib, typing

---

### 2.2 generate-c2-markdown.py ✓ COMPLETE
**Status**: FULLY IMPLEMENTED
**Purpose**: Generate C2 (Container) markdown from c2-containers.json
**Input**: `c2-containers.json` file path
**Output**: Markdown files in `knowledge-base/systems/{system-id}/c2/{container-id}.md`

**Exit Codes**:
- 0: Success - all containers converted
- 1: Warning - no containers in JSON (still exits 0)
- 2: Blocking error - file not found or invalid JSON

**Features Implemented**:
- ✓ YAML frontmatter (id, title, level, type, system, generated)
- ✓ Overview with type, system, responsibility
- ✓ Technology Stack section:
  - Primary language, framework
  - Libraries table (Name, Version, Purpose)
- ✓ Runtime Environment section:
  - Environment, platform, containerization
  - Container technology (if containerized)
- ✓ Observations section (grouped by category)
- ✓ Relations section (markdown table format)
- ✓ Metadata section
- ✓ Evidence links and tags
- ✓ Directory creation per system

**Code Quality**:
- Clean function separation
- Consistent with C1 generator style
- Robust error handling
- Proper markdown table formatting

**Dependencies**:
- Standard library: json, sys, pathlib, typing

---

### 2.3 generate-c3-markdown.py ✓ COMPLETE
**Status**: FULLY IMPLEMENTED
**Purpose**: Generate C3 (Component) markdown from c3-components.json
**Input**: `c3-components.json` file path
**Output**: Markdown files in `knowledge-base/systems/{system-id}/c3/{component-id}.md`

**Exit Codes**:
- 0: Success - all components converted
- 1: Warning - no components in JSON (still exits 0)
- 2: Blocking error - file not found or invalid JSON

**Features Implemented**:
- ✓ YAML frontmatter (id, title, level, type, container)
- ✓ Overview with type, container, responsibility
- ✓ Code Structure section:
  - Path, language
  - Files list (path, lines, type)
  - Exports list (name, type)
- ✓ Design Patterns section (if present):
  - Pattern name, category, description
- ✓ Metrics section (if present):
  - Lines of code, cyclomatic complexity, test coverage
- ✓ Observations section (grouped by category)
- ✓ Relations section with coupling info:
  - Target, type, coupling level, description
- ✓ Metadata section
- ✓ Tags support

**Known Issues**:
- ⚠️ Line 263: TODO comment about system_id mapping
  - Uses hardcoded "unknown-system" as placeholder
  - Needs to read c2-containers.json to map container_id → system_id
  - Should be fixed before production use

**Code Quality**:
- Well-organized sections
- Consistent style with C1 and C2
- Clear data structure handling
- Proper error handling

**Dependencies**:
- Standard library: json, sys, pathlib, typing

---

## 3. DEPENDENCY ANALYSIS

### Python Dependencies (requirements.txt)
```
jsonschema>=4.17.0      # For JSON schema validation
pyyaml>=6.0             # For YAML parsing (frontmatter)
python-dateutil>=2.8.0  # For timestamp parsing and comparison
```

### Current Usage
- **Implemented scripts**: Only use standard library (json, sys, pathlib, typing)
- **Stub scripts**: Will need: jsonschema, pyyaml, python-dateutil
- **Shell scripts**: Use only Bash builtins + jq, date, mkdir

### Missing Dependencies
- **jq**: Not listed in requirements but assumed for JSON parsing in shell scripts
  - Should add to documentation or create requirements-dev.txt
  - Check if pre-installed in CI/CD environment

---

## 4. EXIT CODE CONVENTIONS

### Standardized Convention (from README.md)
```
0: Validation passed / Operation successful
1: Non-blocking warning (proceeds but with caution)
2: Blocking error (halts workflow)
```

### Current Implementation
- **Generation scripts**: Follow convention correctly
  - Exit 0 on success (even if no items to process)
  - Exit 2 on file/JSON errors
  - Exit 1 on warnings (no systems/containers/components)

- **Stub scripts**: No implementation yet
  - Must follow same pattern
  - Should document which checks are critical (exit 2) vs. warnings (exit 1)

---

## 5. VALIDATION COVERAGE ANALYSIS

### Currently Covered (via generation)
- ✓ JSON file exists and is readable
- ✓ JSON is valid syntax
- ✓ Basic structure exists (systems/containers/components arrays)
- ✓ Required fields in data items (id, name)

### NOT YET COVERED (gaps)
- ❌ JSON schema validation against templates
- ❌ Timestamp ordering and validity
- ❌ Cross-file references (e.g., system_id in containers must exist in systems)
- ❌ Markdown structure and content validation
- ❌ Missing required observations/relations
- ❌ Data consistency (e.g., no orphaned containers)
- ❌ Directory structure creation
- ❌ File naming conventions

### Severity Levels for Validation
**Critical (exit 2)**:
- Invalid JSON syntax
- Missing required fields
- Invalid timestamp format
- Cross-file reference integrity
- Unknown system_id/container_id

**Warning (exit 1)**:
- Missing optional fields
- Timestamp drift (e.g., too far in future)
- Missing observations
- Inconsistent naming conventions

---

## 6. CI/CD INTEGRATION DESIGN

### Recommended Workflow

```
1. Code Changes → PR
   ↓
2. Trigger Validation Pipeline:
   a) Run validation scripts:
      - validate-init.py init.json
      - validate-c1-systems.py c1-systems.json
      - validate-c2-containers.py c2-containers.json
      - validate-c3-components.py c3-components.json
   b) Check timestamps:
      - check-timestamp.sh .
   c) Validate markdown (if regenerating):
      - generate-c1-markdown.py c1-systems.json
      - generate-c2-markdown.py c2-containers.json
      - generate-c3-markdown.py c3-components.json
      - validate-markdown.py knowledge-base/systems/**/*.md
   ↓
3. Exit Code Decision:
   - Exit 0: Pass, merge allowed
   - Exit 1: Warning, merge with caution
   - Exit 2: Blocking error, PR blocked
   ↓
4. Optional: Generate reports/artifacts
```

### GitHub Actions Integration

**Minimal (.github/workflows/validate.yml)**:
```yaml
on: [pull_request, push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r plugins/melly-validation/requirements.txt
      
      - name: Validate JSON files
        run: |
          python plugins/melly-validation/scripts/validate-init.py init.json || true
          python plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json || true
          python plugins/melly-validation/scripts/validate-c2-containers.py c2-containers.json || true
          python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json || true
      
      - name: Check timestamps
        run: bash plugins/melly-validation/scripts/check-timestamp.sh .
      
      - name: Generate and validate markdown
        run: |
          python plugins/melly-validation/scripts/generate-c1-markdown.py c1-systems.json
          python plugins/melly-validation/scripts/generate-c2-markdown.py c2-containers.json
          python plugins/melly-validation/scripts/generate-c3-markdown.py c3-components.json
          python plugins/melly-validation/scripts/validate-markdown.py 'knowledge-base/systems/**/*.md'
```

### Environment Requirements
- Python 3.10+
- jq (for JSON parsing in shell scripts)
- Bash 4.0+
- Standard Unix tools: date, mkdir

---

## 7. IMPLEMENTATION ROADMAP

### Phase 1: Validation Scripts (Priority)
1. **validate-init.py** → Simplest, required for all workflows
2. **check-timestamp.sh** → Critical for workflow integrity
3. **validate-c1-systems.py** → Most important C level validator
4. **validate-c2-containers.py** → Cross-file reference validation
5. **validate-c3-components.py** → Most complex validation
6. **validate-markdown.py** → Ensure output quality

### Phase 2: Utility Scripts
1. **create-folders.sh** → Directory structure management
2. Fix **generate-c3-markdown.py** → Resolve TODO (system_id mapping)

### Testing Strategy
- Unit tests for each validation function
- Integration tests with sample JSON files
- CI/CD pipeline testing
- Error case coverage (missing files, invalid JSON, etc.)

---

## 8. QUICK REFERENCE TABLE

| Script | Status | Priority | Input | Output | Exit 0 | Exit 2 |
|--------|--------|----------|-------|--------|--------|--------|
| validate-init.py | STUB | HIGH | init.json | Valid? | Yes | Invalid JSON/Schema |
| validate-c1-systems.py | STUB | HIGH | c1-systems.json | Valid? | Yes | Invalid structure |
| validate-c2-containers.py | STUB | HIGH | c2-containers.json | Valid? | Yes | Bad references |
| validate-c3-components.py | STUB | HIGH | c3-components.json | Valid? | Yes | Missing container_id |
| validate-markdown.py | STUB | MEDIUM | *.md files | Valid? | Yes | Broken structure |
| check-timestamp.sh | STUB | HIGH | JSON dir | Ordered? | Yes | Out of order |
| create-folders.sh | STUB | MEDIUM | JSON files | Dirs created | Yes | Can't create dirs |
| generate-c1-markdown.py | ✓ DONE | LOW | c1-systems.json | README.md | Yes | File/JSON error |
| generate-c2-markdown.py | ✓ DONE | LOW | c2-containers.json | *.md | Yes | File/JSON error |
| generate-c3-markdown.py | ✓ DONE | LOW | c3-components.json | *.md | Yes | File/JSON error |

---

## 9. RECOMMENDATIONS FOR CI/CD DESIGN

### 1. Execution Order (Critical)
```
validate-init.py
  ↓ (only if ✓)
validate-c1-systems.py
  ↓ (only if ✓)
check-timestamp.sh
  ↓
validate-c2-containers.py
  ↓
validate-c3-components.py
  ↓
create-folders.sh
  ↓
generate-c1-markdown.py
generate-c2-markdown.py
generate-c3-markdown.py
  ↓
validate-markdown.py
```

### 2. Allow for Partial Failures
- Validation warnings (exit 1) should not block
- Markdown generation is optional on PR (full on merge to main)
- Log all warnings for developer review

### 3. Reporting
- Generate summary report of validation results
- List any warnings with severity levels
- Provide clear remediation steps
- Archive markdown output as artifact

### 4. Caching Strategy
- Cache Python dependencies (venv or pip cache)
- Cache generated markdown (with hash validation)
- Cache validation results (with dependency tracking)

---

## SUMMARY

**Status**: 3/10 scripts implemented, 7/10 stubs
- **Blockers**: None - generation scripts work, validation framework exists
- **Quick Wins**: Implement validation scripts (reusable JSON schema approach)
- **Known Issues**: generate-c3-markdown.py TODO (system_id mapping)
- **CI/CD Readiness**: Generation scripts ready, validation framework needs completion

