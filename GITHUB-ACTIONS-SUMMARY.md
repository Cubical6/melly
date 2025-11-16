# GitHub Actions Validation Workflows - Design Proposal Summary

**Full Document**: See `github-actions-design-proposal.md` (1,685 lines)  
**Date**: 2025-11-16  
**Status**: Design & Recommendations Only (No Implementation)

---

## Quick Reference

### Key Recommendations

1. **Workflow Count**: Use **2-3 focused workflows** (NOT 1 monolithic, NOT 4+ separate)
   - Workflow 1: "Quick Validations" (runs on push, ~2 min)
   - Workflow 2: "Code Quality" (runs on PRs, ~8 min)
   - Workflow 3 (optional): "Security" (runs on schedule)

2. **Execution Strategy**:
   - Use **parallel job execution** (matrix or separate jobs)
   - Implement **path-based filtering** with `dorny/paths-filter@v3`
   - Use **`fail-fast: false`** for comprehensive reporting
   - Apply **`continue-on-error`** selectively for non-blocking checks

3. **Tool Selection** (by file type):

| File Type | Recommended Action | Marketplace | Why |
|-----------|---|---|---|
| JSON | `json-yaml-validate` | 100+ stars | Fast, simple, good UX |
| Shell | `reviewdog/action-shellcheck` | 500+ stars | PR annotations, good feedback |
| Markdown Lint | `DavidAnson/markdownlint-cli2-action` | 700+ stars | Most popular, configurable |
| Markdown Links | `markdown-link-check` | 500+ stars | Reliable, handles retries |
| Python (fast) | `astral-sh/ruff-action` | 500+ stars | Modern, very fast |
| Python (comprehensive) | Manual: `pylint`, `mypy` | N/A | Detailed analysis |
| Path Filtering | `dorny/paths-filter` | 1000+ stars | Only run relevant jobs |
| Caching | `actions/cache@v4` | Official | Reduce build time by 80% |

---

## Workflow Designs (Choose One)

### Option A: Simple (Small Projects, <50 files)

**Single job, all checks sequential**
- Pros: Simple, easy to understand
- Cons: No parallelization, slower
- Time: 5-10 minutes

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: JSON syntax
        run: find . -name "*.json" -exec python -m json.tool {} \;
      - name: Shell lint
        run: shellcheck **/*.sh
      - name: Markdown lint
        uses: DavidAnson/markdownlint-cli2-action@v14
      - name: Python syntax
        run: python -m py_compile $(find . -name "*.py")
```

### Option B: Recommended (Medium Projects)

**Parallel jobs with path filtering**
- Pros: Fast, selective execution, clear separation
- Cons: Slightly more complex
- Time: 2-3 minutes (parallel)

Features:
- `dorny/paths-filter` to detect changed files
- Separate jobs for each validation type
- Runs only relevant checks
- Comprehensive error reporting

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      json: ${{ steps.filter.outputs.json }}
      shell: ${{ steps.filter.outputs.shell }}
      # ... other outputs
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
            # ... more filters

  validate-json:
    needs: changes
    if: ${{ needs.changes.outputs.json == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: marketplace/json-yaml-validate@v1

  validate-shell:
    needs: changes
    if: ${{ needs.changes.outputs.shell == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: reviewdog/action-shellcheck@v1

  # ... other validation jobs run in parallel
```

### Option C: Advanced (Large Projects, Team Standardization)

**Multiple workflows with reusable components**
- Pros: Highly scalable, reusable components, clear responsibilities
- Cons: More files to maintain
- Time: 2-3 min (quick) + 8 min (quality)

Structure:
```
.github/workflows/
├── 1-quick-validations.yml    # Runs on push (~2 min)
├── 2-code-quality.yml         # Runs on PRs (~8 min)
├── 3-security-scan.yml        # Runs on schedule
└── _reusable-validations.yml  # Shared logic
```

---

## Performance Optimization Checklist

**Caching** (saves 30-60 seconds):
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: ${{ runner.os }}-pip-
```

**Path Filtering** (skips unnecessary runs):
```yaml
on:
  push:
    paths:
      - '**/*.{json,sh,md,py}'
      - '.github/workflows/**'
```

**Parallelization** (reduces total time):
```yaml
jobs:
  json: # runs in parallel
    runs-on: ubuntu-latest
    steps: # ...
  
  shell: # runs in parallel
    runs-on: ubuntu-latest
    steps: # ...
  
  python: # runs in parallel
    runs-on: ubuntu-latest
    steps: # ...
```

**Fail-Fast Strategy**:
```yaml
strategy:
  fail-fast: false  # Run all checks, report all issues
```

---

## Execution Time Targets

| Phase | Target | Tools Included |
|-------|--------|-----------------|
| Quick Validations (push) | < 2 min | JSON, Shell, Python (syntax only) |
| Code Quality (PR) | < 8 min | Markdown lint, Markdown links, Python linting, comprehensive checks |
| Security (schedule) | < 15 min | Dependency scanning, SAST tools |

**Without optimization**: 4-10 minutes  
**With optimization**: 2-3 minutes (parallel execution + caching)

---

## Configuration Files to Create

1. **.markdownlint.json** - Markdown style rules
   ```json
   {
     "extends": "markdownlint/style/relaxed",
     "line-length": { "line_length": 120, "code_blocks": false }
   }
   ```

2. **.markdown-link-check.json** - Link checking config
   ```json
   {
     "timeout": "20s",
     "retryOn429": true,
     "retryCount": 3
   }
   ```

3. **pyproject.toml** - Python tool config
   ```toml
   [tool.ruff]
   line-length = 120
   target-version = "py39"
   ```

4. **.shellcheckrc** or env var - ShellCheck config
   ```bash
   disable=SC1091,SC2086
   ```

---

## Implementation Roadmap

### Phase 1: Quick Setup (1-2 hours)
- [ ] Create `.github/workflows/quick-validations.yml`
- [ ] Add JSON validation (syntax)
- [ ] Add Shell validation (ShellCheck)
- [ ] Test locally with `act`

### Phase 2: Enhance (2-3 hours)
- [ ] Add Markdown validation (linting)
- [ ] Add Python validation (syntax + ruff)
- [ ] Implement pip caching
- [ ] Add path-based filtering

### Phase 3: Optimize (3-4 hours)
- [ ] Separate workflows (quick + quality)
- [ ] Add Python matrix (3.9, 3.11, 3.12)
- [ ] Implement `dorny/paths-filter`
- [ ] Add comprehensive reporting

### Phase 4: Team Standardization (ongoing)
- [ ] Document in CONTRIBUTING.md
- [ ] Share config files in repo
- [ ] Monitor metrics
- [ ] Iterate on validation rules

---

## GitHub Actions Updates (2025)

**Important**: GitHub Actions cache backend updated February 1, 2025
- Upgrade to `actions/cache@v4` or `v3` immediately
- v2 and earlier are deprecated
- New service provides better performance and reliability

---

## Decision Matrix: Which Design to Choose?

| Project Size | Complexity | Team Size | Recommended |
|---|---|---|---|
| Small (<50 files) | Simple (1-2 langs) | Solo | **Option A** |
| Medium (50-500 files) | Moderate (2-4 langs) | Small team | **Option B** ← Most common |
| Large (500+ files) | Complex (4+ langs) | Large team | **Option C** |
| Monorepo | High (many packages) | Many teams | **Option C** + reusables |

---

## Avoid These Pitfalls

❌ **Single monolithic workflow** - Hard to debug, difficult to maintain  
❌ **4+ separate workflows** - Redundant setups, hard to manage  
❌ **No path filtering** - Wastes time running irrelevant checks  
❌ **Sequential execution** - Slower builds  
❌ **No caching** - Wastes 30-60 seconds on dependency install  
❌ **`fail-fast: true` on code quality** - Developers miss other issues  
❌ **Using deprecated `actions/cache@v2`** - Performance issues, not supported  
❌ **No configuration files** - Rules are hard to find and modify  

---

## Related Resources

**Full Document**: `github-actions-design-proposal.md` (11 sections, 1,685 lines)

**Sections Included**:
1. Workflow Architecture Strategy (single vs multiple)
2. File Type Validation Strategies (JSON, Shell, Markdown, Python)
3. Workflow Execution Patterns (triggers, fail-fast, matrix)
4. Performance Optimization (caching, parallelization, timing)
5. Recommended Workflow Designs (3 options with full YAML)
6. Configuration File Best Practices
7. Monitoring and Reporting
8. Common Pitfalls & Solutions
9. Implementation Roadmap
10. Tool Selection Summary
11. Testing Workflows Locally with `act`

**Key Sections**:
- Section 5 has **complete YAML examples** for all three design options
- Section 4 details **caching strategies** with hash-based key design
- Section 2 covers **tool selection** with pros/cons for each
- Section 3 explains **fail-fast vs comprehensive reporting**
- Section 10 has **quick reference tables** for tool selection

---

## Next Steps

1. **Read** `github-actions-design-proposal.md` (full design document)
2. **Choose** a workflow design (A, B, or C) based on project size
3. **Create** `.github/workflows/` directory structure
4. **Implement** (when ready - document is design only, not implementation)
5. **Test** locally with `act` before pushing to GitHub

---

**This document contains research and recommendations only.**  
**No implementation has been performed.**  
**Ready for implementation when you decide to proceed.**

---

Generated: 2025-11-16  
Document: `github-actions-design-proposal.md`  
Summary: `GITHUB-ACTIONS-SUMMARY.md` (this file)
