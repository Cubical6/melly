# Minimal Alignment Plan - Optie 1

> **Doel**: Harmoniseer field names tussen C4 en Library docs
> **Effort**: 2-3 uur
> **Breaking Changes**: Minimal (field renames only)

---

## Changes

### 1. Field Renames

**Observations:**
- `content` → `description`
- `type` → `category` (in observation context)
- Ensure `tags` is always array

**Before:**
```json
{
  "id": "obs-001",
  "type": "fact",
  "content": "Routes defined in routes/web.php",
  "tags": ["routing"]
}
```

**After:**
```json
{
  "id": "obs-001",
  "category": "fact",
  "description": "Routes defined in routes/web.php",
  "tags": ["routing"]
}
```

### 2. Files to Update

- ✅ `templates/lib-docs-template.json` - Update observation examples
- ✅ `templates/enhanced-markdown-template.md` - Update frontmatter
- ✅ `scripts/extract-metadata.py` - Change output field names
- ✅ `scripts/validate-lib-docs.py` - Validate new field names
- ✅ `skills/lib-doc-methodology/SKILL.md` - Update documentation

### 3. What Stays the Same

- ✅ Observation categories (fact, technique, best-practice, etc.)
- ✅ Relation types (requires, part_of, extends, etc.)
- ✅ No evidence arrays (can add later)
- ✅ No severity field (can add later)

### 4. Backward Compatibility

**None** - This is a breaking change.

Users must:
- Regenerate library documentation
- Update any custom validation scripts

---

## Implementation

Execute in sequence:
1. Update templates
2. Update extract-metadata.py
3. Update validate-lib-docs.py
4. Update skill docs
5. Test & commit

Total effort: ~2-3 hours
