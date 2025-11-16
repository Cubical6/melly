# CI/CD Design for Melly Validation Pipeline

## Dependency Graph

```
AI Agent Generation
    │
    └─→ init.json
         │
         └─→ [validate-init.py]
              │ (Exit 2 if invalid)
              ↓
         [✓ Passed]
         │
         └─→ c1-systems.json
              │
              ├─→ [validate-c1-systems.py]
              │    └─→ (Exit 2 if invalid/schema mismatch)
              │
              └─→ [check-timestamp.sh]
                   └─→ (Exit 2 if init timestamp > c1 timestamp)
                   
              [✓ Both Passed]
              │
              └─→ c2-containers.json
                   │
                   ├─→ [validate-c2-containers.py]
                   │    └─→ Check system_id references exist in c1
                   │    └─→ (Exit 2 if cross-file refs broken)
                   │
                   └─→ [check-timestamp.sh]
                        └─→ (Exit 2 if c1 timestamp > c2 timestamp)
                   
                   [✓ Both Passed]
                   │
                   └─→ c3-components.json
                        │
                        ├─→ [validate-c3-components.py]
                        │    └─→ Check container_id refs exist in c2
                        │    └─→ (Exit 2 if cross-file refs broken)
                        │
                        └─→ [check-timestamp.sh]
                             └─→ (Exit 2 if c2 timestamp > c3 timestamp)
                        
                        [✓ All Passed]
                        │
                        ├─→ [create-folders.sh]
                        │    └─→ Create directory structure
                        │
                        ├─→ [generate-c1-markdown.py]
                        │    └─→ Output: knowledge-base/systems/{id}/c1/
                        │
                        ├─→ [generate-c2-markdown.py]
                        │    └─→ Output: knowledge-base/systems/{id}/c2/
                        │
                        ├─→ [generate-c3-markdown.py]
                        │    └─→ Output: knowledge-base/systems/{id}/c3/
                        │
                        └─→ [validate-markdown.py]
                             └─→ (Exit 2 if markdown broken/incomplete)
```

## CI/CD Pipeline Flow

### Phase 1: JSON Validation (BLOCKING)

```
┌─────────────────────────────────────────────────────────────┐
│ Trigger: PR opened/updated, push to main                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: JSON VALIDATION (Run in sequence - must all pass)  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. python validate-init.py init.json                       │
│     ├─ Exit 0: Continue                                     │
│     ├─ Exit 1: Warn but continue                            │
│     └─ Exit 2: STOP - Block PR                              │
│                                                              │
│  2. python validate-c1-systems.py c1-systems.json           │
│     ├─ Exit 0: Continue                                     │
│     ├─ Exit 1: Warn but continue                            │
│     └─ Exit 2: STOP - Block PR                              │
│                                                              │
│  3. bash check-timestamp.sh .                               │
│     ├─ Exit 0: Continue                                     │
│     ├─ Exit 1: Warn but continue                            │
│     └─ Exit 2: STOP - Block PR                              │
│                                                              │
│  4. python validate-c2-containers.py c2-containers.json     │
│     ├─ Exit 0: Continue                                     │
│     ├─ Exit 1: Warn but continue                            │
│     └─ Exit 2: STOP - Block PR                              │
│                                                              │
│  5. python validate-c3-components.py c3-components.json     │
│     ├─ Exit 0: Continue                                     │
│     ├─ Exit 1: Warn but continue                            │
│     └─ Exit 2: STOP - Block PR                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
              [If any Exit 2: FAIL]  [If all Exit 0 or 1: PASS]
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: MARKDOWN GENERATION (Can run in parallel)          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┬──────────────────┬──────────────────┐ │
│  │ C1 Generation    │ C2 Generation    │ C3 Generation    │ │
│  ├──────────────────┼──────────────────┼──────────────────┤ │
│  │ create-folders   │ (same)           │ (same)           │ │
│  │ generate-c1      │ generate-c2      │ generate-c3      │ │
│  └──────────────────┴──────────────────┴──────────────────┘ │
│                           ↓                                  │
│                  [All generation done]                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: MARKDOWN VALIDATION (BLOCKING)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  python validate-markdown.py 'knowledge-base/systems/**/*.md'│
│  ├─ Exit 0: Continue                                        │
│  ├─ Exit 1: Warn but continue                               │
│  └─ Exit 2: STOP - Block PR                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                           ↓
              [If Exit 2: FAIL]  [If Exit 0 or 1: PASS]
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ FINAL DECISION                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  EXIT 0: ✓ PASS - All validations OK                        │
│          Can merge to main                                  │
│          Mark all checks as "passed"                        │
│                                                              │
│  EXIT 1: ⚠️  WARN - Has warnings but passed validation      │
│          Can merge but review warnings                      │
│          Mark checks as "passed with warnings"              │
│                                                              │
│  EXIT 2: ✗ FAIL - Blocking errors found                     │
│          Cannot merge                                       │
│          Show which validation failed                       │
│          Provide remediation steps                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Script Status Matrix

```
┌──────────────────────────┬──────────┬─────────┬─────────────────────────┐
│ Script                   │ Status   │ Blocks? │ Run After               │
├──────────────────────────┼──────────┼─────────┼─────────────────────────┤
│ validate-init.py         │ STUB     │ YES     │ Start                   │
│ validate-c1-systems.py   │ STUB     │ YES     │ validate-init.py        │
│ check-timestamp.sh       │ STUB     │ YES     │ validate-c1-systems.py  │
│ validate-c2-containers.py│ STUB     │ YES     │ check-timestamp.sh      │
│ validate-c3-components.py│ STUB     │ YES     │ validate-c2-containers │
│ create-folders.sh        │ STUB     │ NO      │ validate-c3-components  │
│ generate-c1-markdown.py  │ DONE ✓   │ NO      │ create-folders.sh       │
│ generate-c2-markdown.py  │ DONE ✓   │ NO      │ (parallel)              │
│ generate-c3-markdown.py  │ DONE ✓   │ NO      │ (parallel)              │
│ validate-markdown.py     │ STUB     │ YES     │ All generation scripts  │
└──────────────────────────┴──────────┴─────────┴─────────────────────────┘
```

## Error Handling Strategy

### When Validation Fails

```
ValidationError
    ↓
Log error details (which file, which field, what was expected)
    ↓
Output helpful message:
    - "System 'web-api' references 'frontend' container"
    - "But 'frontend' is not defined in c2-containers.json"
    ↓
Exit with code 2
    ↓
CI/CD catches exit code 2
    ↓
Mark build as FAILED
    ↓
Block merge
    ↓
Developer gets notification with error details
```

### When Validation Warns

```
ValidationWarning
    ↓
Log warning (e.g., "System 'legacy' has no observations")
    ↓
Exit with code 1
    ↓
CI/CD catches exit code 1
    ↓
Mark build as "PASSED WITH WARNINGS"
    ↓
Allow merge but show warning summary
    ↓
Developers can review warnings before merging
```

## Recommended GitHub Actions Workflow

```yaml
name: Validate Melly C4 Workflow

on:
  pull_request:
    paths:
      - '**/*.json'
      - '**/*.md'
      - 'plugins/melly-validation/**'
  push:
    branches: [main]
    paths:
      - '**/*.json'
      - '**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r plugins/melly-validation/requirements.txt
          # Ensure jq is available
          apt-get update && apt-get install -y jq
      
      - name: Validate init.json
        run: |
          python plugins/melly-validation/scripts/validate-init.py init.json
        continue-on-error: true
      
      - name: Validate c1-systems.json
        run: |
          python plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json
        continue-on-error: true
      
      - name: Check timestamps
        run: |
          bash plugins/melly-validation/scripts/check-timestamp.sh .
        continue-on-error: true
      
      - name: Validate c2-containers.json
        run: |
          python plugins/melly-validation/scripts/validate-c2-containers.py c2-containers.json
        continue-on-error: true
      
      - name: Validate c3-components.json
        run: |
          python plugins/melly-validation/scripts/validate-c3-components.py c3-components.json
        continue-on-error: true
      
      - name: Create documentation structure
        run: |
          bash plugins/melly-validation/scripts/create-folders.sh .
        continue-on-error: true
      
      - name: Generate C1 markdown
        run: |
          python plugins/melly-validation/scripts/generate-c1-markdown.py c1-systems.json
      
      - name: Generate C2 markdown
        run: |
          python plugins/melly-validation/scripts/generate-c2-markdown.py c2-containers.json
      
      - name: Generate C3 markdown
        run: |
          python plugins/melly-validation/scripts/generate-c3-markdown.py c3-components.json
      
      - name: Validate markdown
        run: |
          python plugins/melly-validation/scripts/validate-markdown.py 'knowledge-base/systems/**/*.md'
        continue-on-error: true
      
      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: validation-report.json
      
      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            // Parse validation results and comment on PR
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('validation-report.json', 'utf8'));
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report.summary
            });
```

## Implementation Timeline

### Week 1: Core Validators
- [ ] Implement validate-init.py
- [ ] Implement validate-c1-systems.py
- [ ] Implement check-timestamp.sh

### Week 2: Advanced Validators
- [ ] Implement validate-c2-containers.py (with cross-file checks)
- [ ] Implement validate-c3-components.py (with cross-file checks)

### Week 3: Utility & Polish
- [ ] Implement create-folders.sh
- [ ] Implement validate-markdown.py
- [ ] Fix generate-c3-markdown.py TODO (system_id mapping)
- [ ] Write comprehensive tests

### Week 4: CI/CD Integration
- [ ] Create GitHub Actions workflow
- [ ] Test with sample repositories
- [ ] Document for team
- [ ] Set up branch protection rules

