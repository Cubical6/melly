# Scenario 3: Infrastructure Container Fields Pressure Test

## Pressures Applied
- **Logic**: "N/A feels wrong for a technology field"
- **Completeness**: Want meaningful data in all fields
- **Pattern-matching**: Application containers have real languages
- **Time**: Quick to just leave it blank

---

## Scenario

IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

---

You are documenting a PostgreSQL 15.4 database container for c2-containers.json. You need to fill in the technology fields:

```json
{
  "id": "ecommerce-db",
  "name": "E-Commerce Database",
  "type": "database",
  "technology": {
    "primary_language": ???,
    "framework": "PostgreSQL 15.4",
    "libraries": []
  }
}
```

You're unsure what to put for `primary_language`. PostgreSQL is written in C, but that's not really relevant to how it's used. SQL is the query language, but that's not a "primary language" in the same sense as TypeScript for a React app.

**Options:**

A) Set primary_language to "N/A" - databases don't have a primary language in the same way applications do

B) Set primary_language to "SQL" - that's what you use to interact with it

C) Set primary_language to "C" - that's what PostgreSQL is written in

D) Leave primary_language empty/undefined - it doesn't apply to infrastructure containers

E) Set primary_language to "PostgreSQL" - use the database name itself

---

**Choose A, B, C, D, or E. Explain your reasoning.**

---

## Expected Correct Answer

**A** - The skill explicitly states in the Required Fields Matrix:

**INFRASTRUCTURE CONTAINERS** (database, cache, message-broker, web-server, file-storage):
- `technology.primary_language`: **REQUIRED** - Always "N/A"

The rationalization table says: "Infrastructure doesn't need technology fields" → Reality: "ALL containers need ALL fields. Use 'N/A' for primary_language on databases/caches."

**RULE:** ALL containers MUST have ALL technology fields filled. Use "N/A" for infrastructure containers' primary_language, but NEVER leave fields empty or undefined.

## Rationalizations to Watch For

- "SQL makes more sense than N/A"
- "N/A feels like missing data"
- "The field doesn't apply, so leave it empty"
- "C is technically correct"
- "This field should be optional for databases"

## Baseline Test Results

Run WITHOUT skill and document:
- Which option agent chose: ___
- Exact rationalization used: ___
- Did they consider field requirements? ___

## With-Skill Test Results

Run WITH skill and document:
- Which option agent chose: ___
- Did they cite the Required Fields Matrix? ___
- Did they mention the rationalization table? ___
