# GitHub Actions Workflow Design Proposal
## Multi-File Validation (JSON, Shell, Markdown, Python)

**Created**: 2025-11-16  
**Status**: Design Proposal (Research & Recommendations Only)  
**Scope**: Workflow architecture, tool selection, performance optimization

---

## Executive Summary

This document provides comprehensive recommendations for designing GitHub Actions workflows to validate four file types: JSON, Shell scripts, Markdown, and Python. The design prioritizes:
- **Fail-fast feedback** for rapid issue detection
- **Comprehensive reporting** for complete project validation
- **Performance optimization** through caching and selective execution
- **Maintainability** with clear structure and reusable components

**Key Recommendation**: Use a **hybrid approach** with 2-3 focused workflows rather than a single monolithic workflow, combined with path-based filtering to run only relevant validation.

---

## 1. Workflow Architecture Strategy

### 1.1 Single vs. Multiple Workflows

#### Recommendation: **2-3 Focused Workflows**

**NOT recommended**: Single monolithic workflow
- Harder to maintain
- Difficult to debug when multiple validation types fail
- Can't easily adjust which validations run on different events
- Difficult to selectively run portions of the workflow

**NOT recommended**: 4+ separate workflows (one per file type)
- Unnecessary complexity
- Repeated checkout and setup overhead
- Difficult to manage consistent caching across workflows

**RECOMMENDED**: 2-3 focused workflows

```
Workflow 1: "Quick Validations" (Fail-Fast)
├─ JSON syntax validation
├─ Shell script syntax validation
└─ Markdown link checking (quick)

Workflow 2: "Code Quality" (Comprehensive)
├─ Shell script linting (shellcheck)
├─ Markdown linting (markdownlint)
└─ Python linting & syntax

Workflow 3: Optional "Security & Advanced"
├─ Dependency security scanning
├─ License compliance
└─ Advanced Python type checking
```

**Rationale**:
- Quick Validations runs on every push (fast feedback)
- Code Quality runs on PRs only (comprehensive review)
- Security workflow runs on schedule + tagged releases
- Synchronized execution within each workflow
- Minimal code duplication via reusable workflows

### 1.2 Workflow Orchestration Pattern

**Use GitHub's native "Reusable Workflows" feature**:
- Define common patterns once (e.g., "validate-json", "validate-python")
- Reference them from multiple workflows
- DRY principle: Maintain validation logic in one place
- Team consistency: Same validation rules across repos

**Suggested structure**:

```
.github/
├── workflows/
│   ├── _templates/              # Reusable workflows
│   │   ├── validate-json.yml
│   │   ├── validate-shell.yml
│   │   ├── validate-markdown.yml
│   │   └── validate-python.yml
│   ├── quick-validations.yml    # Orchestrator (main workflow)
│   ├── code-quality.yml         # Orchestrator
│   └── security.yml             # Orchestrator (optional)
└── .gitignore                    # Don't commit cache artifacts
```

---

## 2. File Type Validation Strategies

### 2.1 JSON Files

#### Recommended Actions

| Action | Purpose | Pros | Cons |
|--------|---------|------|------|
| **json-yaml-validate** | Syntax + Schema | Fast, multiple file support, optional schemas | Limited features |
| **schema-validation-action** | Schema validation | Full JSON Schema support, flexible | Slower on large files |
| **Validate JSON** (ajv-based) | JSON Schema validation | RFC 7592 compliant | Schema-only, no basic syntax |

#### Recommended Tools & Actions

**For Syntax Validation Only**:
```yaml
- name: Validate JSON syntax
  uses: marketplace/json-yaml-validate@v1
  with:
    glob: '**/*.json'
    # Excludes
    exclude: 'node_modules/**,build/**'
```

**For Schema Validation** (if you have schemas):
```yaml
- name: Validate JSON against schema
  uses: PnX-SI/jsonschema_validator@v1
  with:
    ajv: true
    files: '**/*.json'
    schemas: 'schemas/*.json'
```

**For GitHub Actions Workflows specifically**:
```yaml
- name: Validate GitHub Actions YAML
  uses: mpalmer/action-validator@v1
```

#### Performance Considerations

- **Fast**: json-yaml-validate uses `fdir` for O(n) file crawling
- **Caching**: Not needed (no dependencies to cache)
- **Fail-fast**: Include early in workflow (runs in <10 seconds)

#### Path Filtering

```yaml
on:
  push:
    paths:
      - '**/*.json'
      - '!node_modules/**'
      - '!.git/**'
  pull_request:
    paths:
      - '**/*.json'
```

### 2.2 Shell Scripts

#### Recommended Actions

| Action | Purpose | Integration |
|--------|---------|-------------|
| **reviewdog/action-shellcheck** | ShellCheck with PRcomments | ✅ Best for PR feedback |
| **ludeeus/action-shellcheck** | Basic ShellCheck runner | Simple, pre-installed on runners |
| **azohra/shell-linter** | Auto-scan + configurable | Good for large codebases |
| **Differential ShellCheck** | Only changed files | Performance-optimized |

#### Recommended Configuration

**Basic Setup** (already on GitHub runners):
```bash
# ShellCheck is pre-installed on ubuntu-latest
shellcheck **/*.sh
```

**Recommended: Use reviewdog for better PR integration**
```yaml
- name: Run shellcheck with reviewdog
  uses: reviewdog/action-shellcheck@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    reporter: github-pr-review
    shellcheck_flags: '--severity=warning'
```

#### Severity Configuration

```bash
# ShellCheck severity levels
--severity=style   # Info-level (default: all)
--severity=info    # Informational
--severity=warning # Warning
--severity=error   # Error only

# Recommended: use 'warning' threshold
# Allows info-level issues but fails on real problems
```

#### Exclude Problematic Files

```yaml
steps:
  - name: Run shellcheck
    run: |
      shellcheck \
        --exclude=SC1091,SC2086 \  # Exclude specific error codes
        $(find . -name "*.sh" \
          -not -path "./node_modules/*" \
          -not -path "./.git/*")
```

#### Path Filtering

```yaml
on:
  push:
    paths:
      - '**/*.sh'
      - '.github/workflows/**'  # Shell commands in workflows
  pull_request:
    paths:
      - '**/*.sh'
```

#### Performance Considerations

- **Speed**: O(n) where n = number of files; typically <5 seconds
- **Caching**: Not applicable (no dependencies)
- **Fail-fast**: Include early in workflow
- **Large repos**: Use Differential ShellCheck to only check changed files

### 2.3 Markdown Files

#### Recommended Actions

| Tool | Purpose | Best For |
|------|---------|----------|
| **DavidAnson/markdownlint-cli2-action** | Linting | Style & format consistency |
| **markdown-link-check** | Link validation | Broken link detection |
| **igorshubovych/markdownlint-cli** | Alt: Linting | Lightweight alternative |

#### Recommended Configuration

**Approach 1: Markdown Linting Only** (Fast)
```yaml
- name: Lint markdown files
  uses: DavidAnson/markdownlint-cli2-action@v14
  with:
    globs: '**/*.md'
    config: '.markdownlint.json'
    fix: false  # Or 'true' to auto-fix
```

**Approach 2: With Link Checking** (Slower, but comprehensive)
```yaml
- name: Check markdown links
  uses: gaurav-nelson/github-action-markdown-link-check@v1
  with:
    use-quiet-mode: 'yes'
    use-verbose-mode: 'yes'
    config-file: '.markdown-link-check.json'
```

#### Configuration File Examples

**.markdownlint.json** (rule configuration):
```json
{
  "extends": "markdownlint/style/relaxed",
  "default": true,
  "indentation": { "indent": 2 },
  "line-length": { "line_length": 120, "code_blocks": false },
  "no-bare-urls": false,
  "no-hard-tabs": true,
  "code-fence-style": { "style": "backtick" }
}
```

**.markdown-link-check.json** (link check config):
```json
{
  "ignorePatterns": [
    {
      "pattern": "^http://localhost"
    },
    {
      "pattern": "^https://internal.company.com"
    }
  ],
  "timeout": "20s",
  "retryOn429": true,
  "retryCount": 3,
  "aliveStatusCodes": [200, 206]
}
```

#### Workflow Strategy

**Option A: Run both in Quick Validations** (takes ~30-40 seconds)
- Good for projects with <100 markdown files
- Provides comprehensive feedback

**Option B: Separate Link Checking** (recommended)
```yaml
# quick-validations.yml
- name: Lint markdown (fast)
  uses: DavidAnson/markdownlint-cli2-action@v14

# code-quality.yml (runs on PRs only)
- name: Check markdown links (slow)
  uses: gaurav-nelson/github-action-markdown-link-check@v1
```

#### Path Filtering

```yaml
on:
  push:
    paths:
      - '**/*.md'
      - '.markdownlint.json'
  pull_request:
    paths:
      - '**/*.md'
      - '.markdownlint.json'
```

#### Performance Considerations

- **Linting**: O(n) where n = file count; typically <10 seconds
- **Link checking**: O(m) where m = number of links; can be 30-60 seconds
  - Mitigated by: parallel checking, caching, timeout configuration
- **Recommendation**: Linting in Quick workflow, link checking in Code Quality

### 2.4 Python Scripts

#### Recommended Tools

| Tool | Purpose | Speed | Coverage |
|------|---------|-------|----------|
| **flake8** | Syntax + basic lint | Fast | Limited |
| **pylint** | Comprehensive linting | Medium | High |
| **ruff** | Modern, fast linter | Very Fast | Medium-High |
| **mypy** | Type checking | Medium | Type safety |
| **black** | Code formatting | Fast | Format only |

#### Recommended Configuration

**Basic Syntax Check** (Fail-Fast):
```yaml
- name: Check Python syntax
  run: |
    python -m py_compile $(find . -name "*.py" \
      -not -path "./venv/*" \
      -not -path "./.git/*")
```

**Comprehensive Linting** (Code Quality):
```yaml
- name: Lint with ruff (fast modern linter)
  uses: astral-sh/ruff-action@v1
  with:
    args: 'check --select=E9,F63,F7,F82'  # Syntax errors only
    version: '0.3.5'

- name: Type check with mypy
  run: |
    pip install mypy types-all
    mypy src/
  continue-on-error: true  # Type errors don't block
```

#### Marketplace Actions

**Best: Python Code Quality and Lint**
```yaml
- name: Python linting
  uses: py-actions/flake8@v2
  with:
    args: |
      --count \
      --select=E9,F63,F7,F82 \
      --show-source \
      --statistics
```

**Alternative: Ruff (faster, modern)**
```yaml
- name: Run Ruff
  uses: astral-sh/ruff-action@v1
```

#### Caching Strategy

**Recommended**: Cache pip dependencies
```yaml
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Install dependencies
  run: pip install flake8 mypy
```

#### Path Filtering

```yaml
on:
  push:
    paths:
      - '**/*.py'
      - 'requirements*.txt'
      - 'pyproject.toml'
  pull_request:
    paths:
      - '**/*.py'
      - 'requirements*.txt'
```

#### Import Validation

```yaml
- name: Check imports
  run: |
    python -m py_compile $(find . -name "*.py")
    # or
    pip install isort
    isort --check-only --diff .
```

#### Performance Considerations

- **Syntax check**: <2 seconds (fast)
- **Ruff linting**: <10 seconds (very fast)
- **Pylint**: 30-60 seconds (comprehensive but slower)
- **Mypy**: 20-40 seconds (type checking adds time)
- **Caching pip**: Saves 30-60 seconds on dependency installation

**Recommendation**: 
- Quick Validations: Python syntax only
- Code Quality: Ruff + optional mypy
- Save pylint for detailed reviews or as optional step

---

## 3. Workflow Execution Patterns

### 3.1 Trigger Conditions

#### Recommended Event Configuration

```yaml
name: Quick Validations

on:
  push:
    branches:
      - main
      - develop
    paths:
      - '**/*.{json,sh,md,py}'
      - '.github/workflows/**'
  pull_request:
    paths:
      - '**/*.{json,sh,md,py}'
  workflow_dispatch:  # Manual trigger support
```

#### Event Recommendations

| Event | Use Case | Recommendation |
|-------|----------|-----------------|
| **on: push** | Every commit | ✅ Use for Quick Validations |
| **on: pull_request** | PR reviews | ✅ Use for Code Quality + PR comments |
| **on: schedule** | Periodic checks | ✅ Use for slow tools (link checking, security) |
| **on: workflow_dispatch** | Manual runs | ✅ Always include for debugging |

#### Path-Based Filtering Strategy

**Workflow-level (triggers entire workflow)**:
```yaml
on:
  push:
    paths:
      - '**/*.json'
      - '**/*.sh'
      - '**/*.md'
      - '**/*.py'
      - '.github/workflows/**'
    paths-ignore:
      - 'docs/**'           # Don't trigger on doc-only changes
      - '.gitignore'
      - 'README.md'
```

**Job/Step-level (selective execution with dorny/paths-filter)**:
```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      json: ${{ steps.filter.outputs.json }}
      shell: ${{ steps.filter.outputs.shell }}
      markdown: ${{ steps.filter.outputs.markdown }}
      python: ${{ steps.filter.outputs.python }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            json:
              - '**/*.json'
            shell:
              - '**/*.sh'
            markdown:
              - '**/*.md'
            python:
              - '**/*.py'

  validate-json:
    needs: changes
    if: ${{ needs.changes.outputs.json == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate JSON
        run: # ...

  validate-shell:
    needs: changes
    if: ${{ needs.changes.outputs.shell == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check shell scripts
        run: # ...
```

**Benefits of dorny/paths-filter**:
- Skip entire jobs if files haven't changed
- Avoid unnecessary checkouts and setup
- Significant time savings on large repos
- Enables partial validation on focused PRs

### 3.2 Fail-Fast vs. Comprehensive Reporting

#### Scenario 1: Quick Validations (Fail-Fast)

```yaml
name: Quick Validations
on: push

jobs:
  syntax-check:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true  # Stop on first failure
      matrix:
        check: [json, shell]
    steps:
      - uses: actions/checkout@v4
      - name: Validate ${{ matrix.check }}
        run: # validation step
```

**Characteristics**:
- `fail-fast: true` (default) - cancels other jobs immediately
- Results in 2-5 minute feedback loops
- Good for syntax errors (must be fixed before proceeding)
- Priority: Speed over comprehensiveness

#### Scenario 2: Comprehensive Code Quality (Fail-Fast False)

```yaml
name: Code Quality
on: pull_request

jobs:
  validation:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false  # Continue all checks, fail overall if any failed
      matrix:
        check:
          - json
          - shell
          - markdown
          - python
    steps:
      - uses: actions/checkout@v4
      - name: Run ${{ matrix.check }} validation
        run: # validation step
```

**Characteristics**:
- `fail-fast: false` - runs all matrix combinations
- Returns comprehensive report (all issues at once)
- Better for code review (developers see all problems)
- Takes longer but provides complete picture

#### Scenario 3: Selective Continue-on-Error (Recommended Hybrid)

```yaml
name: Code Quality
on: pull_request

jobs:
  validation:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        include:
          # Required checks (must pass)
          - check: json
            required: true
          - check: shell
            required: true
          # Optional checks (warning only)
          - check: markdown-links
            required: false
          - check: python-types
            required: false
    
    steps:
      - uses: actions/checkout@v4
      - name: Run ${{ matrix.check }}
        id: validation
        run: |
          # validation logic
        continue-on-error: ${{ !matrix.required }}
      
      - name: Fail on required checks
        if: |
          failure() && 
          matrix.required == true
        run: exit 1
```

**Benefits**:
- Required checks block PRs
- Optional checks provide feedback without blocking
- Clear distinction in code
- Flexible thresholds

### 3.3 Matrix Strategy for Testing Versions

#### When to Use Matrix

**Use matrix when**:
- Testing against multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Testing against multiple OS platforms (Ubuntu, macOS, Windows)
- Testing with different dependency versions
- Running tests in parallel to reduce total execution time

**Avoid matrix for**:
- Simple syntax validation (no version dependencies)
- Single-language projects with no version variance
- Sequential validation that can't run in parallel

#### Recommended Matrix Configuration

**Single-dimension matrix** (language versions):
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m py_compile .
```

**Multi-dimension matrix** (OS × version):
```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python-version: ['3.9', '3.11']
    # Creates 3 × 2 = 6 jobs
```

**Matrix with include/exclude**:
```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    include:
      - python-version: '3.9'
        experimental: false
      - python-version: '3.12-dev'
        experimental: true
    exclude:
      # Skip specific combinations
      - python-version: '3.9'
        os: 'windows-latest'  # Python 3.9 on Windows skipped
```

#### Dynamic Matrix from Previous Steps

**Advanced pattern**: Detect changed files, run only relevant versions

```yaml
jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: set-matrix
        run: |
          # Check if Python 3.8 is explicitly required
          if grep -q "python_requires.*3.8" setup.py; then
            echo "matrix={'python-version':['3.8','3.9','3.10','3.11','3.12']}" >> $GITHUB_OUTPUT
          else
            echo "matrix={'python-version':['3.10','3.11','3.12']}" >> $GITHUB_OUTPUT
          fi

  validate:
    needs: detect-changes
    strategy:
      matrix: ${{ fromJson(needs.detect-changes.outputs.matrix) }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -c "import sys; print(sys.version)"
```

#### Matrix Recommendations for File Validation

| Validation Type | Matrix Use | Rationale |
|---|---|---|
| JSON syntax | ❌ No matrix | No version dependencies |
| Shell scripts | ⚠️ Optional | Only if bash 3, 4, 5 variants matter |
| Markdown | ❌ No matrix | Markdown spec is stable |
| Python syntax | ✅ Yes (optional) | Test multiple Python versions |
| Python linting | ✅ Yes | Linter behavior varies by version |

**Recommendation**: 
- Use matrix only for Python validation
- Test against minimum supported and latest versions
- Consider 3 versions: LTS + current + dev (e.g., 3.9, 3.11, 3.12)

---

## 4. Performance Optimization Strategies

### 4.1 Caching Implementation

#### Cache Strategy Hierarchy

```
1. Dependency Lock Files (high priority)
   ├─ package-lock.json (Node.js)
   ├─ requirements.txt (Python)
   └─ Cargo.lock (Rust)

2. Installed Dependencies (medium priority)
   ├─ ~/.cache/pip/ (Python)
   ├─ node_modules/ (Node.js)
   └─ ~/.cargo (Rust)

3. Build Artifacts (low priority)
   └─ Only cache if regeneration is expensive
```

#### Recommended Python Caching

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  id: cache
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
      
- name: Install dependencies
  if: steps.cache.outputs.cache-hit != 'true'
  run: |
    pip install flake8 mypy pylint
```

**Key Cache Parameters**:
- `path`: Directory to cache (must already exist)
- `key`: Unique cache key (hash of dependencies)
- `restore-keys`: Fallback keys if exact match not found
- `if: cache-hit`: Skip install if cache hit

#### Shell Script Caching (Usually Not Needed)

```yaml
# ShellCheck is pre-installed, no caching needed
# But if you install additional tools:

- name: Cache shellcheck
  uses: actions/cache@v3
  with:
    path: /usr/local/bin/shellcheck
    key: shellcheck-v0.9.0
```

#### Markdown/JSON Caching (Not Applicable)

No dependencies to cache. Linters run directly on source files.

#### Cache Management Best Practices

**Cache Size Limits**:
- GitHub free tier: 5 GB per repo
- Premium: 120 GB per repo
- Cleanup stale caches regularly

**Cache Key Design**:
```yaml
# Good: Hash-based (invalidates on dependency change)
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}

# Avoid: Time-based (accumulates stale caches)
key: ${{ runner.os }}-pip-${{ github.run_number }}

# Better: Include version info
key: ${{ runner.os }}-pip-v1-${{ hashFiles('requirements.txt') }}
#                       ^^^ increment for major cache invalidations
```

#### Recent Updates (2025)

GitHub Actions cache backend updated February 1, 2025:
- Upgrade to `actions/cache@v4` or `v3` immediately
- v2 and earlier are deprecated
- New cache service provides better performance and reliability

```yaml
- uses: actions/cache@v4  # or v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 4.2 Parallelization

#### Job-Level Parallelism (Matrix)

```yaml
jobs:
  validation:
    strategy:
      matrix:
        check: [json, shell, markdown, python]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Checking ${{ matrix.check }}"
```

**Effect**: Jobs run in parallel (4 jobs simultaneously), reduces total time from 4min to ~1min

#### Step-Level Parallelism (Within Single Job)

Limited, but can use background processes:

```yaml
- name: Run checks in parallel
  run: |
    (validate-json &)
    (validate-shell &)
    (validate-markdown &)
    (validate-python &)
    wait
    echo "All checks complete"
```

#### Recommended Parallelization Pattern

```yaml
name: Validations

on: [push, pull_request]

jobs:
  # Detect changes first
  changes:
    runs-on: ubuntu-latest
    outputs:
      json: ${{ steps.filter.outputs.json }}
      shell: ${{ steps.filter.outputs.shell }}
      markdown: ${{ steps.filter.outputs.markdown }}
      python: ${{ steps.filter.outputs.python }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            json:
              - '**/*.json'
            shell:
              - '**/*.sh'
            markdown:
              - '**/*.md'
            python:
              - '**/*.py'

  # Run all validations in parallel
  json:
    needs: changes
    if: ${{ needs.changes.outputs.json == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: json-validate

  shell:
    needs: changes
    if: ${{ needs.changes.outputs.shell == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: shellcheck **/*.sh

  markdown:
    needs: changes
    if: ${{ needs.changes.outputs.markdown == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: markdownlint **/*.md

  python:
    needs: changes
    if: ${{ needs.changes.outputs.python == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
      - run: pip install flake8 && flake8 .

  # Require all checks to pass
  result:
    needs: [json, shell, markdown, python]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - run: |
          if [[ "${{ needs.json.result }}" != "success" && 
                "${{ needs.json.result }}" != "skipped" ]]; then
            exit 1
          fi
          # Check all jobs similarly
```

### 4.3 Execution Time Targets

**Typical Execution Times** (without caching):

| Validation | Time | Notes |
|---|---|---|
| JSON syntax (100 files) | <1s | Very fast |
| Shell scripts (50 files) | 2-5s | Fast |
| Markdown lint (50 files) | 3-8s | Moderate |
| Markdown link check (50 files) | 20-40s | Slower, external network |
| Python syntax (100 files) | 1-2s | Fast |
| Python lint (ruff) | 5-10s | Fast |
| Python lint (pylint) | 30-60s | Slow, comprehensive |

**Target Execution Times**:
- Quick Validations: < 2 minutes
  - Exclude: Markdown link checking, comprehensive linting
  
- Code Quality: < 8 minutes
  - Includes: Markdown link checking, comprehensive Python analysis
  
- Full Security Scan: < 15 minutes
  - Includes: Dependency scanning, SAST tools

---

## 5. Recommended Workflow Designs

### 5.1 Design Option A: Simple Single Workflow (Small Projects)

**Best for**: Small projects, simple validation needs, <50 total files

```yaml
name: Validate

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # JSON
      - name: Validate JSON
        run: |
          find . -name "*.json" ! -path "./node_modules/*" \
            -exec python -m json.tool {} \;

      # Shell
      - name: Lint shell scripts
        run: shellcheck **/*.sh || true

      # Markdown
      - name: Lint markdown
        uses: DavidAnson/markdownlint-cli2-action@v14

      # Python
      - name: Check Python syntax
        run: |
          find . -name "*.py" ! -path "./venv/*" \
            -exec python -m py_compile {} \;
```

**Pros**: Simple, easy to understand, minimal overhead  
**Cons**: No parallelization, no comprehensive reporting

---

### 5.2 Design Option B: Recommended Multi-Job Workflow

**Best for**: Medium projects, comprehensive validation, team environments

```yaml
name: Quick Validations

on:
  push:
    branches: [main, develop]
    paths:
      - '**/*.{json,sh,md,py}'
      - '.github/workflows/**'
  pull_request:
    paths:
      - '**/*.{json,sh,md,py}'
  workflow_dispatch:

jobs:
  # Detect which files changed
  changes:
    runs-on: ubuntu-latest
    outputs:
      json: ${{ steps.filter.outputs.json }}
      shell: ${{ steps.filter.outputs.shell }}
      markdown: ${{ steps.filter.outputs.markdown }}
      python: ${{ steps.filter.outputs.python }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for diff
      
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            json:
              - '**/*.json'
              - '!node_modules/**'
            shell:
              - '**/*.sh'
              - '!node_modules/**'
            markdown:
              - '**/*.md'
              - '!node_modules/**'
            python:
              - '**/*.py'
              - '!venv/**'

  # Validate JSON (runs only if JSON files changed)
  validate-json:
    needs: changes
    if: ${{ needs.changes.outputs.json == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate JSON syntax and format
        uses: marketplace/json-yaml-validate@v1
        with:
          glob: '**/*.json'
          exclude: 'node_modules/**'

  # Validate shell scripts (runs only if shell files changed)
  validate-shell:
    needs: changes
    if: ${{ needs.changes.outputs.shell == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Lint shell scripts
        uses: reviewdog/action-shellcheck@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          reporter: github-pr-review
          shellcheck_flags: '--severity=warning'

  # Validate markdown (runs only if markdown files changed)
  validate-markdown:
    needs: changes
    if: ${{ needs.changes.outputs.markdown == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Lint markdown
        uses: DavidAnson/markdownlint-cli2-action@v14
        with:
          globs: '**/*.md'
          config: '.markdownlint.json'

  # Validate Python (runs only if Python files changed)
  validate-python:
    needs: changes
    if: ${{ needs.changes.outputs.python == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: ${{ runner.os }}-pip-
      
      - name: Install linters
        run: pip install flake8 ruff
      
      - name: Check Python syntax
        run: |
          python -m py_compile $(find . -name "*.py" \
            -not -path "./venv/*")
      
      - name: Run ruff
        run: ruff check . --select=E9,F63,F7,F82
        continue-on-error: true

  # Overall result check
  result:
    needs: [validate-json, validate-shell, validate-markdown, validate-python]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Check validation results
        run: |
          if [[ "${{ needs.validate-json.result }}" == "failure" ]] || \
             [[ "${{ needs.validate-shell.result }}" == "failure" ]] || \
             [[ "${{ needs.validate-markdown.result }}" == "failure" ]] || \
             [[ "${{ needs.validate-python.result }}" == "failure" ]]; then
            echo "❌ One or more validations failed"
            exit 1
          fi
          echo "✅ All validations passed"
```

**Execution Flow**:
1. All validation jobs run in parallel
2. Only relevant jobs execute (based on changed files)
3. Results aggregated in final `result` job
4. Estimated time: 2-3 minutes (parallel execution)

**Pros**:
- Parallel execution (fast)
- Selective execution (only runs relevant checks)
- Clear job separation
- Easy to debug individual failures

---

### 5.3 Design Option C: Advanced Multi-Workflow Architecture (Large Projects)

**Best for**: Large projects, complex validation needs, team standardization

**Structure**:
```
.github/
├── workflows/
│   ├── 1-quick-validations.yml    # Fast feedback (push events)
│   ├── 2-code-quality.yml         # Comprehensive (PR reviews)
│   ├── 3-security-scan.yml        # Advanced checks (schedule + PR)
│   └── _reusable-validations.yml  # Shared logic
└── configs/
    ├── .markdownlint.json
    ├── .shellcheckrc
    ├── .python-lint.toml
    └── .json-schemas/
```

**Workflow 1: Quick Validations** (Runs on every push)

```yaml
name: 1. Quick Validations

on:
  push:
    branches: [main, develop]
    paths:
      - '**/*.{json,sh,md,py}'
      - '.github/workflows/**'
  workflow_dispatch:

concurrency:
  group: quick-${{ github.ref }}
  cancel-in-progress: true  # Cancel previous runs on new push

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      json: ${{ steps.filter.outputs.json }}
      shell: ${{ steps.filter.outputs.shell }}
      python: ${{ steps.filter.outputs.python }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            json:
              - '**/*.json'
            shell:
              - '**/*.sh'
            python:
              - '**/*.py'

  json-syntax:
    needs: changes
    if: ${{ needs.changes.outputs.json == 'true' }}
    uses: ./.github/workflows/_reusable-validations.yml
    with:
      check-type: 'json'

  shell-syntax:
    needs: changes
    if: ${{ needs.changes.outputs.shell == 'true' }}
    uses: ./.github/workflows/_reusable-validations.yml
    with:
      check-type: 'shell'

  python-syntax:
    needs: changes
    if: ${{ needs.changes.outputs.python == 'true' }}
    uses: ./.github/workflows/_reusable-validations.yml
    with:
      check-type: 'python'
```

**Workflow 2: Code Quality** (Runs on PRs)

```yaml
name: 2. Code Quality Review

on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:

jobs:
  markdown-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DavidAnson/markdownlint-cli2-action@v14
        with:
          globs: '**/*.md'
          config: '.markdownlint.json'

  markdown-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
          config-file: '.markdown-link-check.json'
        continue-on-error: true  # Don't block on link errors

  python-comprehensive:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.11']
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      - name: Install tools
        run: pip install flake8 pylint mypy
      - name: Run comprehensive linting
        run: |
          pylint src/ || true
          mypy src/ || true
        continue-on-error: true
```

**Workflow 3: Security** (Scheduled + on PR)

```yaml
name: 3. Security Scanning

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday
  pull_request:
    paths:
      - 'requirements*.txt'
      - 'pyproject.toml'
  workflow_dispatch:

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: |
          pip install safety
          safety check --json
        continue-on-error: true
```

**Reusable Workflow** (`_reusable-validations.yml`):

```yaml
name: Validate

on:
  workflow_call:
    inputs:
      check-type:
        required: true
        type: string
        description: 'Type of check: json, shell, python'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: JSON validation
        if: ${{ inputs.check-type == 'json' }}
        run: |
          find . -name "*.json" ! -path "./node_modules/*" \
            -exec python -m json.tool {} \;
      
      - name: Shell validation
        if: ${{ inputs.check-type == 'shell' }}
        run: shellcheck $(find . -name "*.sh")
      
      - name: Python validation
        if: ${{ inputs.check-type == 'python' }}
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
        run: |
          find . -name "*.py" ! -path "./venv/*" \
            -exec python -m py_compile {} \;
```

**Pros**:
- Clear separation of concerns
- Reusable components
- Scalable for teams
- Fine-grained control
- Easy to add new checks

**Cons**:
- More files to maintain
- Slight added complexity

---

## 6. Configuration File Best Practices

### 6.1 JSON Configuration

**.github/validate-json.json**:
```json
{
  "validation": {
    "strict": true,
    "ignorePatterns": [
      "node_modules/**",
      "dist/**",
      ".git/**"
    ],
    "expectedPatterns": [
      "**/*.json"
    ]
  }
}
```

### 6.2 Markdown Linting

**.markdownlint.json**:
```json
{
  "extends": "markdownlint/style/relaxed",
  "default": true,
  "MD004": false,
  "MD024": false,
  "MD025": false,
  "MD034": false,
  "MD040": false,
  "indentation": {
    "indent": 2,
    "indent_code_blocks": true
  },
  "line-length": {
    "line_length": 120,
    "code_blocks": false
  },
  "no-hard-tabs": true
}
```

**.markdown-link-check.json**:
```json
{
  "ignorePatterns": [
    {
      "pattern": "^http://localhost"
    },
    {
      "pattern": "^https://internal\\.company\\.com"
    },
    {
      "pattern": "^https://docs\\.private\\.com"
    }
  ],
  "timeout": "20s",
  "retryOn429": true,
  "retryCount": 3,
  "aliveStatusCodes": [200, 206]
}
```

### 6.3 Shell Configuration

**.shellcheckrc** or environment variable:
```bash
# .shellcheckrc (read by shellcheck)
disable=SC1091,SC2086,SC2181
format=json
```

Or via workflow:
```yaml
env:
  SHELLCHECK_OPTS: '--severity=warning --exclude=SC1091,SC2086'
```

### 6.4 Python Configuration

**pyproject.toml** (modern Python tooling):
```toml
[tool.ruff]
line-length = 120
target-version = "py39"
select = ["E9", "F63", "F7", "F82"]

[tool.mypy]
python_version = "3.9"
strict = true
ignore_missing_imports = true

[tool.black]
line-length = 120
target-version = ['py39']
```

---

## 7. Monitoring and Reporting

### 7.1 PR Annotations

**Using reviewdog** (shows inline comments on PRs):

```yaml
- name: ShellCheck with reviewdog
  uses: reviewdog/action-shellcheck@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    reporter: github-pr-review
    level: warning
```

### 7.2 Summary Reports

**Create GitHub Actions job summary**:

```yaml
- name: Create validation summary
  if: always()
  run: |
    {
      echo "# Validation Results"
      echo ""
      echo "| Check | Status |"
      echo "|-------|--------|"
      echo "| JSON  | ✅ Passed |"
      echo "| Shell | ✅ Passed |"
      echo "| Markdown | ⚠️ 2 warnings |"
      echo "| Python | ✅ Passed |"
    } >> $GITHUB_STEP_SUMMARY
```

### 7.3 Notification Strategy

**Badge in README**:
```markdown
![Validations](https://github.com/org/repo/actions/workflows/validations.yml/badge.svg)
```

**Slack/Discord Notifications**:
```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 8. Common Pitfalls and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| **Workflow runs too slowly** | Sequential execution | Use matrix strategy, run jobs in parallel |
| **Excessive cache misses** | Wrong cache key | Hash dependency files: `hashFiles('requirements.txt')` |
| **Path filters not working** | Workflow trigger limitation | Use `dorny/paths-filter@v3` for job-level filtering |
| **Matrix jobs continue after failure** | `fail-fast: false` | Set to `true` for fast feedback, or use `continue-on-error` per step |
| **Shell scripts fail unexpectedly** | Missing shebang | Add `#!/bin/bash` to all scripts |
| **JSON validation too strict** | Schema mismatch | Review `.markdownlint.json` or schema configuration |
| **Link check timeouts** | External service slow | Increase timeout: `timeout: "30s"` |
| **Python import errors | Missing setup step | Install dependencies before validation |

---

## 9. Implementation Roadmap

### Phase 1: Quick Setup (1-2 hours)

- [ ] Create `.github/workflows/quick-validations.yml` (Design Option A or B)
- [ ] Add JSON validation
- [ ] Add shell validation
- [ ] Test locally with `act`

### Phase 2: Enhance (2-3 hours)

- [ ] Add markdown validation
- [ ] Add Python validation
- [ ] Implement caching
- [ ] Add path-based filtering

### Phase 3: Optimize (3-4 hours)

- [ ] Separate workflows (quick + quality)
- [ ] Add matrix for Python versions
- [ ] Implement reusable workflows
- [ ] Add comprehensive reporting

### Phase 4: Team Standardization (ongoing)

- [ ] Document in CONTRIBUTING.md
- [ ] Share configuration files
- [ ] Monitor metrics (pass rate, execution time)
- [ ] Iterate on rules

---

## 10. Tool Selection Summary

### Quick Reference Table

| File Type | Primary Tool | Alternative | Speed | Setup |
|-----------|---|---|---|---|
| **JSON** | json-yaml-validate | Manual python -m json.tool | <1s | Minimal |
| **Shell** | reviewdog/action-shellcheck | ludeeus/action-shellcheck | 2-5s | Minimal |
| **Markdown Lint** | DavidAnson/markdownlint-cli2 | actionshub/markdownlint | 3-8s | Config file |
| **Markdown Links** | markdown-link-check | Linkinator | 30-60s | Config file |
| **Python Syntax** | py_compile or ruff | flake8 | 1-10s | Minimal |
| **Python Lint** | ruff | pylint | 10-30s | Config or default |
| **Python Types** | mypy | pyright | 20-40s | Config file |

### GitHub Actions Marketplace Recommended List

| Use Case | Recommended Action | Marketplace URL | Stars |
|---|---|---|---|
| JSON validation | json-yaml-validate | github.com/marketplace/actions/json-yaml-validate | 100+ |
| Shell linting | reviewdog/action-shellcheck | github.com/marketplace/actions/reviewdog-action-shellcheck | 500+ |
| Markdown linting | DavidAnson/markdownlint-cli2-action | github.com/DavidAnson/markdownlint-cli2-action | 700+ |
| Link checking | markdown-link-check | github.com/marketplace/actions/markdown-link-check | 500+ |
| Python linting | astral-sh/ruff-action | github.com/astral-sh/ruff-action | 500+ |
| Path filtering | dorny/paths-filter | github.com/dorny/paths-filter | 1000+ |
| Caching | actions/cache | github.com/actions/cache | Official |

---

## 11. Testing Your Workflows Locally

### Using `act` (Local GitHub Actions Testing)

**Installation**:
```bash
brew install act  # macOS
# or see https://github.com/nektos/act for other platforms
```

**Test workflow locally**:
```bash
cd your-project
act push -j validate-json
act push -j validate-shell
```

**Benefits**:
- No need to push to test workflows
- Fast iteration
- Catch errors before committing

---

## Conclusion

### Key Recommendations Summary

1. **Workflow Structure**: Use 2-3 focused workflows instead of one monolithic workflow
2. **Path Filtering**: Implement `dorny/paths-filter` for selective job execution
3. **Parallelization**: Run validation jobs in parallel using matrix strategy
4. **Caching**: Cache Python dependencies using hash-based keys
5. **Fail Strategy**: Use `fail-fast: false` for comprehensive reporting
6. **Tool Selection**: Prefer marketplace actions with 500+ stars and active maintenance
7. **Configuration**: Store validation rules in config files (.markdownlint.json, etc.)
8. **Monitoring**: Use PR annotations for inline feedback, GitHub summaries for overview

### Next Steps (Design → Implementation)

This document provides the **design** for your validation workflows. When ready to implement:

1. Choose a Design Option (A, B, or C)
2. Select your configuration files
3. Create workflow YAML files
4. Test locally with `act`
5. Push and verify on GitHub
6. Document in CONTRIBUTING.md

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-16  
**Status**: Design Proposal (Ready for Implementation)
