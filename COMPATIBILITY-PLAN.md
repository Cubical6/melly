# melly-lib-docs Compatibility Plan voor PR #18

> **Doel**: Align melly-lib-docs plugin met nieuwe observations/relations structuur uit PR #18
> **Status**: 🔴 INCOMPATIBLE - Requires updates
> **Priority**: P0 - CRITICAL (blocking merge)

---

## 🔍 Gap Analysis

### Current Implementation (melly-lib-docs)

**Observations Format:**
```json
{
  "id": "obs-001",
  "type": "fact",              // ❌ WRONG FIELD
  "category": "routing",       // ❌ WRONG USAGE (this is library category)
  "content": "Description",    // ❌ MISSING title/description split
  // ❌ MISSING severity
  // ❌ MISSING evidence array
  "tags": ["tag1"]
}
```

**Relations Format:**
```json
{
  "id": "rel-001",
  "type": "requires",
  "target": "entity-id",
  "description": "Description"
  // ❌ MISSING protocol
  // ❌ MISSING direction (C1)
  // ❌ MISSING coupling (C3)
  // ❌ MISSING isAsync
}
```

**Markdown Format:**
```markdown
### Observations
- [fact] Routes defined in routes/web.php #routing
- [technique] Use Route::get() for GET requests #http

### Relations
- requires [[Controllers]]
- part_of [[Routing]]
```

---

### PR #18 Required Structure

**Observations Format:**
```json
{
  "id": "obs-jwt-storage",
  "category": "security",           // ✅ Observation category (not library)
  "severity": "critical",           // ✅ NEW REQUIRED
  "title": "JWT tokens in localStorage",  // ✅ NEW REQUIRED
  "description": "The application stores JWT tokens in localStorage...",  // ✅ Renamed from content
  "evidence": [                     // ✅ NEW REQUIRED (array)
    {
      "type": "file",              // file|code|config|pattern|metric|...
      "location": "src/auth.js:42"
    }
  ],
  "tags": ["security", "authentication"],  // ✅ Same
  "impact": "High security risk",   // ✅ NEW OPTIONAL
  "recommendation": "Use httpOnly cookies"  // ✅ NEW OPTIONAL
}
```

**Relations Format:**
```json
{
  "id": "rel-frontend-api",
  "source": "web-app",              // ✅ Optional (often implied)
  "target": "backend-api",          // ✅ Same
  "type": "http-rest",              // ✅ More specific types
  "description": "Sends HTTP requests to fetch data",  // ✅ Same
  "protocol": "HTTP/REST",          // ✅ NEW OPTIONAL
  "direction": "outbound",          // ✅ NEW (C1 only)
  "coupling": "loose",              // ✅ NEW (C3 only)
  "isAsync": false,                 // ✅ NEW OPTIONAL
  "tags": ["api", "rest"]           // ✅ Same
}
```

**New Observation Categories (from PR #18):**
- security, performance, documentation
- coupling, cohesion, code-structure
- error-handling, design-patterns
- deployment, users, external-dependencies
- data-flow, technology-stack

**New Relation Types:**
- **C1**: http-rest, http-graphql, websocket, event-stream, database-connection, rpc, soap, smtp, external-api
- **C2**: database-query, database-write, cache-read, cache-write, message-subscribe, cdn-fetch, stream
- **C3**: composition/composes, inheritance/inherits, dependency/depends-on, aggregation/aggregates

---

## 📋 Required Changes

### Phase 1: Update Type Definitions ⚡ CRITICAL

**Task 1.1**: Import types from PR #18
- Copy `types-observations.json` to `melly-lib-docs/templates/`
- Copy `types-relations.json` to `melly-lib-docs/templates/`
- Copy `types-notes.json` to `melly-lib-docs/templates/`

**Task 1.2**: Update observation categories in skill
- File: `skills/lib-doc-methodology/SKILL.md`
- Replace current categories with PR #18 categories
- Map library-specific categories to PR #18 categories:
  - `fact` → `technology-stack` or context-specific
  - `technique` → `code-structure` or `design-patterns`
  - `best-practice` → `performance` or `security`
  - `requirement` → `external-dependencies`
  - `problem` → `error-handling`
  - etc.

**Task 1.3**: Update relation types in skill
- Add C1/C2/C3 specific relation types
- Document direction/coupling usage
- Add protocol field guidance

---

### Phase 2: Update Scripts 🔧 HIGH

**Task 2.1**: Update `extract-metadata.py`
- Change observation extraction to new format:
  ```python
  {
    "id": f"obs-{slug}",
    "category": map_to_pr18_category(detected_type),  # NEW
    "severity": detect_severity(content),              # NEW
    "title": extract_title(content, max=100),          # NEW
    "description": extract_description(content),       # RENAMED
    "evidence": extract_evidence(parsed),              # NEW ARRAY
    "tags": extract_tags(content),
    "impact": extract_impact(content),                 # NEW OPTIONAL
    "recommendation": extract_recommendation(content)  # NEW OPTIONAL
  }
  ```

- Change relation extraction to new format:
  ```python
  {
    "id": f"rel-{slug}",
    "target": target_id,
    "type": map_to_specific_type(generic_type),  # More specific
    "description": description,
    "protocol": detect_protocol(context),        # NEW
    "direction": detect_direction(context),      # NEW C1
    "coupling": detect_coupling(context),        # NEW C3
    "isAsync": detect_async(context),            # NEW
    "tags": extract_tags(context)
  }
  ```

**Task 2.2**: Add severity detection function
```python
def detect_severity(content: str, category: str) -> str:
    """Detect severity from content and category"""
    if any(word in content.lower() for word in ['critical', 'security', 'vulnerable', 'exposed']):
        return 'critical'
    elif any(word in content.lower() for word in ['warning', 'caution', 'should', 'recommended']):
        return 'warning'
    else:
        return 'info'
```

**Task 2.3**: Add evidence extraction function
```python
def extract_evidence(parsed: Dict, observation_content: str) -> List[Dict]:
    """Extract evidence from code blocks and links near observation"""
    evidence = []

    # From code blocks
    for code_block in parsed['code_blocks']:
        evidence.append({
            "type": "code",
            "location": f"Code example in {parsed.get('current_heading', 'document')}"
        })

    # From file paths in content
    file_paths = re.findall(r'`([^`]+\.(js|py|php|java|rb|go|rs))`', observation_content)
    for path, _ in file_paths:
        evidence.append({
            "type": "file",
            "location": path
        })

    return evidence if evidence else [{"type": "pattern", "location": "Documentation pattern"}]
```

**Task 2.4**: Add category mapping function
```python
def map_to_pr18_category(library_type: str, content: str) -> str:
    """Map library-specific observation type to PR #18 categories"""

    # Keyword-based detection
    if any(word in content.lower() for word in ['security', 'vulnerable', 'attack', 'xss', 'sql injection', 'authentication', 'authorization']):
        return 'security'
    elif any(word in content.lower() for word in ['performance', 'slow', 'cache', 'optimize', 'latency', 'throughput']):
        return 'performance'
    elif any(word in content.lower() for word in ['coupling', 'dependent', 'tightly coupled']):
        return 'coupling'
    elif any(word in content.lower() for word in ['cohesion', 'single responsibility', 'focused']):
        return 'cohesion'
    elif any(word in content.lower() for word in ['error', 'exception', 'try-catch', 'handling']):
        return 'error-handling'
    elif any(word in content.lower() for word in ['pattern', 'singleton', 'factory', 'observer', 'strategy']):
        return 'design-patterns'
    elif any(word in content.lower() for word in ['deployment', 'production', 'environment', 'ci/cd']):
        return 'deployment'
    elif any(word in content.lower() for word in ['dependency', 'requires', 'package', 'library', 'npm', 'composer']):
        return 'external-dependencies'
    elif any(word in content.lower() for word in ['data flow', 'pipeline', 'transformation']):
        return 'data-flow'
    elif any(word in content.lower() for word in ['technology', 'framework', 'language', 'stack']):
        return 'technology-stack'

    # Fallback based on library type
    type_mapping = {
        'fact': 'technology-stack',
        'technique': 'code-structure',
        'best-practice': 'design-patterns',
        'requirement': 'external-dependencies',
        'example': 'code-structure',
        'problem': 'error-handling',
        'solution': 'design-patterns',
        'insight': 'design-patterns',
        'decision': 'design-patterns',
        'question': 'documentation'
    }

    return type_mapping.get(library_type, 'documentation')
```

**Task 2.5**: Update `validate-lib-docs.py`
- Add validation for new required fields (severity, title, description, evidence)
- Add validation for evidence array structure
- Add validation for PR #18 observation categories
- Add validation for PR #18 relation types
- Add validation for direction (C1 only)
- Add validation for coupling (C3 only, values: loose|tight)

---

### Phase 3: Update Templates 📄 HIGH

**Task 3.1**: Update `lib-docs-template.json`
- Replace observation examples with PR #18 format
- Replace relation examples with PR #18 format
- Add evidence arrays
- Add severity levels
- Add title/description split
- Add protocol/direction/coupling fields

**Task 3.2**: Update `enhanced-markdown-template.md`
- Update frontmatter to use "title" (not "name")
- Update observations section with new format:
  ```markdown
  ### Observations

  #### Security

  - **[critical]** JWT tokens in localStorage
    - **Description**: The application stores JWT tokens in localStorage, vulnerable to XSS
    - **Evidence**: `src/auth/storage.js:42` (code), `docs/security.md` (documentation)
    - **Impact**: High security risk
    - **Recommendation**: Use httpOnly cookies
    - **Tags**: #security #authentication #xss
  ```

- Update relations section with new format:
  ```markdown
  ### Relations

  - **requires** [[Eloquent ORM]]
    - **Protocol**: Database/ORM
    - **Direction**: Outbound
    - **Async**: No
    - **Description**: Uses Eloquent models for data access
    - **Tags**: #database #orm
  ```

---

### Phase 4: Update Agent Workflow 🤖 MEDIUM

**Task 4.1**: Update `lib-doc-analyzer.md` agent
- Update Phase 3 (Semantic Analysis) to generate new observation format
- Add severity detection step
- Add evidence extraction step
- Add title/description splitting step
- Update relation extraction with protocol/direction/coupling

**Task 4.2**: Update enhanced markdown generation
- Generate observations in new format
- Generate relations in new format
- Include all new fields in output

---

### Phase 5: Update Skill Documentation 📚 MEDIUM

**Task 5.1**: Update `lib-doc-methodology/SKILL.md`
- Replace observation categories section with PR #18 categories
- Add severity level guidance
- Add evidence type documentation
- Add title vs description guidelines
- Update relation types with C1/C2/C3 specifics
- Add direction/coupling documentation
- Update examples to use new format

---

### Phase 6: Update Slash Command 🎯 LOW

**Task 6.1**: Update `melly-analyze-lib-docs.md`
- Update output report to show new statistics:
  - Observations by severity (critical/warning/info)
  - Observations by category (security, performance, etc.)
  - Relations by type (http-rest, database-query, etc.)
- Update validation step to use new validators

---

## 🎯 Implementation Strategy

### Approach A: Sequential Updates (RECOMMENDED)
1. **Import types** (Phase 1) - Foundation
2. **Update scripts** (Phase 2) - Core logic
3. **Update templates** (Phase 3) - Examples
4. **Update agent** (Phase 4) - Workflow
5. **Update skill** (Phase 5) - Documentation
6. **Update command** (Phase 6) - UI

**Pros**: Safe, testable at each step
**Cons**: Takes longer

### Approach B: Parallel Updates
1. **Team 1**: Phases 1-2 (Types + Scripts)
2. **Team 2**: Phases 3-4 (Templates + Agent)
3. **Team 3**: Phases 5-6 (Skill + Command)

**Pros**: Faster completion
**Cons**: Risk of integration issues

---

## ✅ Validation Checklist

After all changes:

- [ ] All observation examples have: id, category, severity, title, description, evidence[]
- [ ] All relation examples have: id, target, type, description
- [ ] Evidence is always an array (not single object)
- [ ] Severity is one of: critical, warning, info
- [ ] Categories match PR #18 allowed values
- [ ] Relation types match PR #18 C1/C2/C3 types
- [ ] Direction only used for C1 relations
- [ ] Coupling only used for C3 relations (loose|tight only)
- [ ] Scripts generate new format correctly
- [ ] Templates validate against PR #18 schemas
- [ ] Skill documentation updated
- [ ] All tests pass

---

## 🚨 Breaking Changes

### For Users
- Old observation format no longer valid
- Must regenerate all existing library documentation
- Scripts output different JSON structure

### For Developers
- `extract-metadata.py` has new function signatures
- `validate-lib-docs.py` validates different schema
- Template structure changed

---

## 📊 Effort Estimation

| Phase | Tasks | Estimated Time | Priority |
|-------|-------|----------------|----------|
| Phase 1 | 3 tasks | 2 hours | P0 Critical |
| Phase 2 | 5 tasks | 8 hours | P0 Critical |
| Phase 3 | 2 tasks | 4 hours | P1 High |
| Phase 4 | 2 tasks | 3 hours | P1 High |
| Phase 5 | 1 task | 2 hours | P2 Medium |
| Phase 6 | 1 task | 1 hour | P3 Low |
| **TOTAL** | **14 tasks** | **~20 hours** | |

---

## 🎯 Recommended Parallel Execution Plan

**Agent Assignment:**

1. **Agent A** - Type Definitions & Category Mapping (Phases 1 + 2.4)
   - Import PR #18 types
   - Create category mapping logic
   - 3 hours

2. **Agent B** - Script Updates: Observations (Phase 2.1-2.3)
   - Update observation extraction
   - Add severity detection
   - Add evidence extraction
   - 4 hours

3. **Agent C** - Script Updates: Relations (Phase 2.1 + 2.5)
   - Update relation extraction
   - Add validation updates
   - 4 hours

4. **Agent D** - Templates & Documentation (Phases 3 + 5)
   - Update JSON templates
   - Update markdown template
   - Update skill documentation
   - 6 hours

5. **Agent E** - Agent & Command (Phases 4 + 6)
   - Update agent workflow
   - Update slash command
   - 4 hours

**Total parallel time: ~6 hours** (vs 20 hours sequential)

---

## 🚀 Next Steps

1. **User approval** - Confirm this plan
2. **Create feature branch** - `feature/pr18-compatibility`
3. **Execute phases** - Sequential or parallel
4. **Testing** - Validate with real library docs
5. **Merge PR #18** - After our updates complete
6. **Merge compatibility** - After PR #18 merged

---

**Created**: 2025-11-16
**Author**: Claude
**Status**: 🟡 AWAITING APPROVAL
