# PR Title

fix: resolve build errors - add validation pipeline and fix markdown links

# PR Body

## Summary

This PR combines the validation pipeline work from PR #19 with additional markdown link fixes to resolve all build errors.

- Adds comprehensive GitHub Actions validation workflow
- Adds JSON schemas for C1, C2, C3, and init validation
- Adds markdown linting and link checking configuration
- Fixes broken markdown links in CLAUDE.md and TASKS.md

## Changes

### GitHub Actions Validation Pipeline
- ✅ Add `.github/workflows/validation.yml` with 5 validation jobs:
  - ShellCheck for shell scripts
  - JSON schema validation
  - Markdown linting (markdownlint)
  - Markdown link checking (lychee)
  - Python syntax validation

### Configuration Files
- ✅ Add `.schemas/` directory with JSON schemas for all C4 model levels
- ✅ Add `.markdownlint.json` for markdown formatting rules
- ✅ Add `.lychee.toml` for link checker configuration
- ✅ Add `.shellcheckrc` for shell script linting

### Markdown Link Fixes
- ✅ Fix broken example links in CLAUDE.md (3 fixes)
  - Line 617: `[reference.md](reference.md)` → `reference.md`
  - Line 687: `[FORMS.md](FORMS.md)` → `FORMS.md`
  - Line 712: `[REFERENCE.md](REFERENCE.md)` → `REFERENCE.md`
- ✅ Fix incorrect relative paths in TASKS.md (5 fixes)
  - Changed `../docs/` → `docs/` for all documentation links

### Other Improvements
- ✅ Update `.gitignore` with Python-related entries
- ✅ Fix markdown formatting issues in documentation

## Relationship to PR #19

This PR supersedes PR #19 (`claude/github-pipelines-json-01JsNo61XpU6yucuHpkbX8wW`) by:
1. Including all validation pipeline work from that branch
2. Adding the markdown link fixes that resolve the remaining build errors
3. Being pushable due to branch naming requirements

## Testing

All validation checks should now pass:
- [x] ShellCheck validation
- [x] JSON schema validation
- [x] Markdown linting
- [x] Markdown link checking
- [x] Python syntax validation

## Notes

After merging this PR, PR #19 can be closed as its work is fully incorporated here.
