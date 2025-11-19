# C4model-C2 Skill Test Scenarios

Test scenarios for validating the c4model-c2 skill using RED-GREEN-REFACTOR methodology.

## Purpose

These scenarios test whether agents will:
1. Include version numbers from manifest files
2. Correctly distinguish C2 containers from C3 components
3. Not over-decompose into too many containers
4. Fill all required fields including for infrastructure containers

## How to Run Tests

### Baseline Test (RED phase)
Run scenarios WITHOUT the c4model-c2 skill loaded to see natural agent behavior.

### Compliance Test (GREEN phase)
Run scenarios WITH the c4model-c2 skill to verify it prevents violations.

### Refactor Phase
Document new rationalizations and update skill to close loopholes.

## Test Scenarios

1. **scenario-1-version-pressure.md** - Time pressure to skip versions
2. **scenario-2-over-decomposition.md** - Temptation to create too many containers
3. **scenario-3-infrastructure-fields.md** - Skipping required fields for databases
