# Implementation Plan: Section 6.1 - /melly-c1-systems Slash Command

## Analysis

### Requirements from TASKS.md Section 6.1
- **Create**: `.claude/commands/melly-c1-systems.md` (now in plugin: `plugins/melly-c1/commands/melly-c1-systems.md`)
- **Description**: Identify C1-level systems
- **Allowed tools**: Task, Read, Write, Bash
- **Command logic**:
  1. Run c4model-explorer for validation (check init.json exists)
  2. Invoke c1-abstractor per repository
  3. Validate c1-systems.json
  4. Commit results

### Best Practices from Section 0
- ✅ **Size**: 10-50 lines (target: ~35 lines)
- ✅ **Orchestration**: Use Task tool to invoke agents
- ✅ **No implementation**: Let agents do the work
- ✅ **Runtime context**: Use !`command` for status checks
- ✅ **Clear arguments**: Provide argument hints
- ✅ **Error handling**: Graceful failures
- ✅ **Documentation**: Link to docs, don't embed

### Dependencies
- **Section 5**: melly-init must be completed first (creates init.json)
- **Section 6.2**: c1-abstractor agent must be implemented
- **Section 3**: melly-validation plugin (validation scripts) ✅ COMPLETED
- **Section 4.1**: c4model-c1 skill ✅ COMPLETED

## Implementation Plan

### Phase 1: Create Slash Command (6.1)

**Location**: `plugins/melly-c1/commands/melly-c1-systems.md`

**Structure**:
```markdown
---
description: Identify C1-level systems from repositories
argument-hint: [init-json-path]
allowed-tools: Task, Read, Bash
---

Analyze repositories and identify C1 systems using C4 methodology.

## Context
- Init file: $1 (or init.json if not specified)
- Status: !`test -f ${1:-init.json} && echo "✅ exists" || echo "❌ missing"`
- Validation scripts: plugins/melly-validation/scripts/

## Workflow

1. **Validate prerequisites**:
   - Check init.json exists
   - Verify melly-validation plugin available

2. **Launch c1-abstractor agent** using Task tool:
   - Input: init.json (repository paths)
   - Skill: c4model-c1 (methodology)
   - Output: c1-systems.json

3. **Validate output**:
   - Run: `bash plugins/melly-validation/scripts/validate-c1-systems.py c1-systems.json`

4. **Report results**:
   - Systems identified: [count]
   - Next step: /melly-c2-containers

See [docs/workflow-guide.md](../../docs/workflow-guide.md) for details.
```

**Target**: 35-40 lines

---

### Phase 2: Create c1-abstractor Agent (6.2)

**Location**: `plugins/melly-c1/agents/c1-abstractor.md`

**Structure**:
```markdown
---
name: c1-abstractor
description: Identify C1 systems from repositories using C4 methodology. Use when analyzing system architecture at the highest level.
tools: Read, Grep, Write, Bash
model: sonnet
---

# C1 System Abstractor

You identify systems at C4 Level 1 (System Context).

## Workflow

1. **Load methodology**
   - Activate c4model-c1 skill for C1 identification rules
   - Understand system boundaries, actors, responsibilities

2. **Read init.json**
   - Extract repository paths
   - Get metadata (package manifests, directory structure)

3. **Analyze repositories**
   - For each repository path:
     - Scan directory structure
     - Identify deployment units
     - Detect system boundaries
     - Map external actors
   - Apply C1 methodology from c4model-c1 skill

4. **Create system folders**
   - Execute: `bash plugins/melly-validation/scripts/create-folders.sh [system-id]`
   - Verify folder structure created

5. **Generate c1-systems.json**
   - Structure:
     ```json
     {
       "metadata": {
         "generated_at": "ISO-8601-timestamp",
         "parent_reference": {
           "file": "init.json",
           "timestamp": "from-init.json"
         }
       },
       "systems": [
         {
           "id": "kebab-case-id",
           "name": "System Name",
           "type": "web-application|api|database|...",
           "purpose": "Brief description",
           "repository_path": "/absolute/path"
         }
       ],
       "observations": [
         {
           "category": "architecture-pattern|deployment|...",
           "content": "Finding description",
           "evidence": ["file:line", "manifest:field"]
         }
       ],
       "relations": [
         {
           "from": "system-id-1",
           "to": "system-id-2",
           "type": "depends-on|calls|...",
           "protocol": "http|grpc|..."
         }
       ]
     }
     ```

6. **Return summary**
   - Systems found: [count]
   - File: c1-systems.json
   - Validation: Ready for validate-c1-systems.py

## Success Criteria

- All repositories analyzed
- System folders created in knowledge-base/systems/
- c1-systems.json generated with valid structure
- Observations include evidence (file:line references)
- Relations map system dependencies
```

**Target**: 60-80 lines

---

### Phase 3: Testing Strategy

1. **Unit tests**:
   - Test command with valid init.json
   - Test command with missing init.json
   - Test agent with sample repository

2. **Integration tests**:
   - Full workflow: init.json → c1-systems.json
   - Validation: validate-c1-systems.py passes
   - Folder creation: knowledge-base/systems/ populated

3. **Error handling**:
   - Missing init.json → clear error message
   - Invalid init.json → validation failure
   - Missing validation script → graceful degradation

---

### Phase 4: Documentation Updates

1. **TASKS.md**:
   - Mark section 6.1 as complete
   - Mark section 6.2 as complete
   - Update status from 🔴 to ✅

2. **README.md** (if applicable):
   - Add /melly-c1-systems to command list
   - Update workflow diagram

3. **docs/workflow-guide.md**:
   - Add usage example for /melly-c1-systems
   - Include sample output

---

## Execution Plan

### Step 1: Create command file
- Create `plugins/melly-c1/commands/melly-c1-systems.md`
- Follow structure above
- Keep to 35-40 lines

### Step 2: Create agent file
- Create `plugins/melly-c1/agents/c1-abstractor.md`
- Follow structure above
- Keep to 60-80 lines

### Step 3: Update plugin.json (if needed)
- Verify plugin.json in melly-c1 directory
- Ensure commands and agents directories are referenced

### Step 4: Test implementation
- Create sample init.json for testing
- Run /melly-c1-systems command
- Verify c1-systems.json generated
- Run validation script

### Step 5: Update documentation
- Update TASKS.md (sections 6.1 and 6.2)
- Update other relevant docs

---

## Success Metrics

- ✅ Command under 50 lines
- ✅ Agent under 100 lines
- ✅ No external script dependencies (except validation)
- ✅ Clear, linear workflow
- ✅ Follows Claude Code best practices
- ✅ Integration with c4model-c1 skill
- ✅ Uses melly-validation plugin
- ✅ Validation passes

---

## Risk Mitigation

**Risk**: Missing dependencies (init.json, c4model-explorer)
- **Mitigation**: Add clear prerequisite checks in command
- **Mitigation**: Provide helpful error messages

**Risk**: Agent workflow too complex
- **Mitigation**: Keep to 6-step linear workflow
- **Mitigation**: Delegate methodology to c4model-c1 skill

**Risk**: Validation script not executable
- **Mitigation**: Check script permissions before execution
- **Mitigation**: Provide alternative validation method

---

## Timeline

- **Phase 1** (Command): 15 minutes
- **Phase 2** (Agent): 30 minutes
- **Phase 3** (Testing): 20 minutes
- **Phase 4** (Documentation): 15 minutes

**Total**: ~80 minutes

---

## Notes

- This implementation follows the **refactored best practices** from Section 0
- Uses **progressive disclosure**: command is simple, agent has details
- **No over-engineering**: straightforward, linear workflows
- **Reusable**: agent can be invoked directly or via command
- **Testable**: clear inputs/outputs, validation built-in
