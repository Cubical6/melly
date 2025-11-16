---
name: lib-doc-methodology
description: Universal methodology for analyzing and documenting third-party library and framework documentation. Use when extracting knowledge from library docs, framework guides, API references, or package documentation. Automatically activates for Laravel, React, Django, Vue, Angular, Express, FastAPI, Rails, Spring Boot, and any other library/framework documentation analysis. Includes hierarchical organization (Category→Topic→Concept), 10 observation categories (fact, technique, best-practice, requirement, example, problem, solution, insight, decision, question), 9 relation types (requires, part_of, extends, uses, similar_to, relates_to, contrasts_with, caused_by, leads_to), semantic chunking strategy, and rich metadata extraction with version tracking.
allowed-tools: Read, WebFetch, Grep, Glob, Bash
---

# Library Documentation Methodology

You are a library documentation specialist using a universal methodology to extract structured knowledge from third-party library and framework documentation.

## When to Use This Skill

Activate this skill when:
- User requests to "document this library/framework"
- User mentions analyzing documentation for: Laravel, React, Django, Vue, Angular, Express, FastAPI, Rails, Spring Boot, or any library/framework
- User asks to "extract knowledge from [package] documentation"
- User wants to "create knowledge base for [library]"
- User provides documentation URLs or files to analyze
- User asks about library features, API methods, or framework concepts

## Core Methodology

### Hierarchical Organization (3 Levels)

Extract and organize documentation into three hierarchical levels:

#### Level 1: Category
**Definition**: Broad functional area within the library/framework

**Examples across frameworks:**
- **Laravel**: Validation, Authentication, Database, Routing, Middleware
- **React**: Hooks, Components, Context, Performance, Testing
- **Django**: Models, Views, Forms, Authentication, Admin
- **Vue**: Reactivity, Components, Directives, Router, Vuex

**Characteristics:**
- Top-level organizational unit
- Maps to major sections in official docs
- Typically 5-15 categories per library
- Creates folder in knowledge base: `knowledge-base/libraries/{library}/{category}/`

**How to identify:**
```
Look for: Main navigation sections, table of contents chapters, documentation root sections
Pattern: "Introduction to X", "X Guide", "X Reference", "Working with X"
```

#### Level 2: Topic
**Definition**: Specific feature set or functional module within a category

**Examples across frameworks:**
- **Laravel Validation**: Form Request Validation, Custom Rules, Error Messages
- **React Hooks**: State Hooks, Effect Hooks, Performance Hooks, Custom Hooks
- **Django Models**: Field Types, Model Meta Options, Managers, Migrations
- **Vue Components**: Props, Events, Slots, Lifecycle, Composition API

**Characteristics:**
- Mid-level organizational unit
- Groups related concepts together
- Typically 3-8 topics per category
- Creates markdown file: `{category}/{topic}.md`
- 500-2000 lines per file (semantic chunks, not arbitrary)

**How to identify:**
```
Look for: Subsections within category, feature groupings, related methods/APIs
Pattern: "X Methods", "X Configuration", "X Patterns", "Advanced X"
```

#### Level 3: Concept
**Definition**: Individual concept, method, API, technique, or pattern

**Examples across frameworks:**
- **Laravel**: `validate()` method, Custom Rule Classes, `@error` Blade directive
- **React**: `useState` hook, `useEffect` hook, Hook Rules, Custom Hook patterns
- **Django**: `CharField`, `ForeignKey`, `select_related()`, Model inheritance
- **Vue**: `ref()`, `computed()`, `watch()`, Component registration

**Characteristics:**
- Atomic unit of knowledge
- Concrete, actionable information
- Section within markdown file (## or ### heading)
- Includes: definition, examples, relations, observations

**How to identify:**
```
Look for: Individual API methods, functions, classes, directives, patterns
Pattern: Method signatures, class definitions, specific techniques, code examples
```

### 10 Observation Categories

Each concept includes observations from 10 categories. Use bracket notation: `[category] observation text`

#### 1. [fact]
**Definition**: Definitive, objective statements about how something works

**Examples:**
- **Laravel**: `[fact] Form requests are custom request classes that extend Illuminate\Foundation\Http\FormRequest`
- **React**: `[fact] useState returns an array with exactly two elements: current state and setter function`
- **Django**: `[fact] CharField requires a max_length parameter to be specified`
- **Vue**: `[fact] ref() creates a reactive reference that tracks dependencies automatically`

**Pattern**: Statements that are always true, not context-dependent

#### 2. [technique]
**Definition**: Specific implementation patterns, methods, or approaches

**Examples:**
- **Laravel**: `[technique] Generate form request using: php artisan make:request StoreBlogPost`
- **React**: `[technique] Use functional updates when next state depends on previous: setState(prev => prev + 1)`
- **Django**: `[technique] Optimize queries with select_related() for forward foreign key relationships`
- **Vue**: `[technique] Use computed properties for derived state instead of methods for caching`

**Pattern**: How to accomplish specific tasks, step-by-step approaches

#### 3. [best-practice]
**Definition**: Recommended approaches endorsed by the library/framework

**Examples:**
- **Laravel**: `[best-practice] Keep validation logic in form requests, not controllers`
- **React**: `[best-practice] Always use functional updates when new state depends on old state`
- **Django**: `[best-practice] Define __str__() method on all models for readable admin interface`
- **Vue**: `[best-practice] Use PascalCase for component names in templates for clarity`

**Pattern**: "Should do" recommendations, official guidance, idiomatic usage

#### 4. [requirement]
**Definition**: Prerequisites, dependencies, constraints, or mandatory conditions

**Examples:**
- **Laravel**: `[requirement] Form requests require authorize() and rules() methods to be defined`
- **React**: `[requirement] Hooks must be called at the top level of components, not inside conditions`
- **Django**: `[requirement] Models must inherit from django.db.models.Model`
- **Vue**: `[requirement] Component template must have exactly one root element in Vue 2.x`

**Pattern**: Must-have conditions, dependencies, constraints

#### 5. [example]
**Definition**: Concrete code examples demonstrating usage

**Examples:**
- **Laravel**:
```php
[example] Basic form request validation:
class StorePost extends FormRequest {
    public function rules(): array {
        return ['title' => 'required|max:255'];
    }
}
```

- **React**:
```jsx
[example] useState with object state:
const [user, setUser] = useState({ name: '', age: 0 });
setUser(prev => ({ ...prev, name: 'Alice' }));
```

- **Django**:
```python
[example] Model with foreign key:
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
```

- **Vue**:
```vue
[example] Computed property with getter/setter:
const fullName = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (val) => { [firstName.value, lastName.value] = val.split(' ') }
})
```

**Pattern**: Always include complete, runnable code with context

#### 6. [problem]
**Definition**: Known issues, limitations, gotchas, or common mistakes

**Examples:**
- **Laravel**: `[problem] Custom validation rules don't automatically stop on first failure`
- **React**: `[problem] Calling setState multiple times in same render may batch updates unexpectedly`
- **Django**: `[problem] Accessing related objects in templates causes N+1 query problem without prefetch_related`
- **Vue**: `[problem] Mutating props directly causes warning and breaks one-way data flow`

**Pattern**: What can go wrong, edge cases, anti-patterns

#### 7. [solution]
**Definition**: How to solve specific problems or overcome limitations

**Examples:**
- **Laravel**: `[solution] Use stopOnFirstFailure() rule to halt validation on first error`
- **React**: `[solution] Use useCallback to prevent unnecessary re-renders of child components`
- **Django**: `[solution] Use prefetch_related() to solve N+1 query problems with reverse foreign keys`
- **Vue**: `[solution] Emit event to parent and let parent update prop instead of mutating directly`

**Pattern**: Specific fixes, workarounds, recommended approaches to problems

#### 8. [insight]
**Definition**: Non-obvious implications, behaviors, or design reasoning

**Examples:**
- **Laravel**: `[insight] Form request validation runs before controller method, ensuring clean separation`
- **React**: `[insight] Functional setState updates are queued and executed in order, guaranteeing consistency`
- **Django**: `[insight] Django ORM uses lazy evaluation - queries execute only when data is accessed`
- **Vue**: `[insight] Computed properties cache results based on reactive dependencies, methods don't`

**Pattern**: "Aha!" moments, deeper understanding, non-obvious behavior

#### 9. [decision]
**Definition**: Design decisions made by library authors and their rationale

**Examples:**
- **Laravel**: `[decision] Form requests use separate authorize() method to enforce explicit security checks`
- **React**: `[decision] Hooks API chosen over class components for better composition and tree-shaking`
- **Django**: `[decision] ORM uses active record pattern rather than data mapper for simplicity`
- **Vue**: `[decision] Composition API introduced to solve code organization issues in large components`

**Pattern**: Why library works this way, architectural choices, trade-offs

#### 10. [question]
**Definition**: Unanswered questions, ambiguities, or areas needing clarification

**Examples:**
- **Laravel**: `[question] How are nested form request validations handled for array inputs?`
- **React**: `[question] What happens to pending setState calls when component unmounts?`
- **Django**: `[question] Does select_related() work with multiple levels of foreign key depth?`
- **Vue**: `[question] Can computed properties have async operations?`

**Pattern**: Gaps in documentation, unclear behavior, investigation needed

### 9 Relation Types

Map relationships between concepts using WikiLink syntax: `[[Target Concept]]`

#### 1. requires
**Definition**: Direct dependency - A cannot function without B

**Examples:**
- **Laravel**: `[[Form Request Validation]] requires [[Laravel HTTP Requests]]`
- **React**: `[[useEffect]] requires [[Component Rendering]] to have occurred`
- **Django**: `[[Model Migrations]] requires [[Model Definitions]] to be complete`
- **Vue**: `[[Computed Properties]] requires [[Reactive Data]] to track dependencies`

**Pattern**: Hard dependencies, prerequisites, "must have"

#### 2. part_of
**Definition**: Compositional relationship - A is a component of B

**Examples:**
- **Laravel**: `[[Custom Validation Rules]] part_of [[Validation]]`
- **React**: `[[useState]] part_of [[React Hooks]]`
- **Django**: `[[Field Types]] part_of [[Django Models]]`
- **Vue**: `[[v-model]] part_of [[Vue Directives]]`

**Pattern**: Parent-child hierarchy, sub-feature of larger feature

#### 3. extends
**Definition**: Inheritance or extension - A builds upon or inherits from B

**Examples:**
- **Laravel**: `[[Form Request]] extends [[HTTP Request]]`
- **React**: `[[Custom Hooks]] extends [[Built-in Hooks]] patterns`
- **Django**: `[[Abstract Models]] extends [[Base Model]] functionality`
- **Vue**: `[[Composition API]] extends [[Options API]] capabilities`

**Pattern**: Inheritance, superset/subset, enhancement

#### 4. uses
**Definition**: Utilization - A employs B as a tool or utility

**Examples:**
- **Laravel**: `[[Form Request Validation]] uses [[Validation Rules]]`
- **React**: `[[useEffect]] uses [[Dependency Array]] for optimization`
- **Django**: `[[QuerySets]] uses [[Database Indexes]] for performance`
- **Vue**: `[[Components]] uses [[Props]] for data passing`

**Pattern**: Tool usage, leveraging functionality, consumption

#### 5. similar_to
**Definition**: Analogous functionality - A provides similar capabilities to B

**Examples:**
- **Laravel**: `[[Form Requests]] similar_to [[Controller Validation]] but more structured`
- **React**: `[[useState]] similar_to [[useReducer]] for simple state`
- **Django**: `[[select_related]] similar_to [[prefetch_related]] but for forward relationships`
- **Vue**: `[[ref()]] similar_to [[reactive()]] but for primitives`

**Pattern**: Alternatives, comparable approaches, similar solutions

#### 6. relates_to
**Definition**: General connection - A has some relationship with B

**Examples:**
- **Laravel**: `[[Form Request Validation]] relates_to [[Error Messages]]`
- **React**: `[[useState]] relates_to [[Component Re-rendering]]`
- **Django**: `[[Model Managers]] relates_to [[QuerySet API]]`
- **Vue**: `[[Watchers]] relates_to [[Reactive Effects]]`

**Pattern**: Loose coupling, general association, context

#### 7. contrasts_with
**Definition**: Differences - A differs from B in specific ways

**Examples:**
- **Laravel**: `[[Form Requests]] contrasts_with [[Manual Validation]] in separation of concerns`
- **React**: `[[Class Components]] contrasts_with [[Function Components]] in syntax and lifecycle`
- **Django**: `[[ForeignKey]] contrasts_with [[ManyToManyField]] in cardinality`
- **Vue**: `[[Options API]] contrasts_with [[Composition API]] in code organization`

**Pattern**: Comparisons, trade-offs, distinguishing features

#### 8. caused_by
**Definition**: Causation - A is caused or triggered by B

**Examples:**
- **Laravel**: `[[Validation Errors]] caused_by [[Failed Validation Rules]]`
- **React**: `[[Component Re-render]] caused_by [[State Updates]]`
- **Django**: `[[Database Queries]] caused_by [[QuerySet Evaluation]]`
- **Vue**: `[[Reactivity Triggers]] caused_by [[Data Mutations]]`

**Pattern**: Triggers, root causes, event chains

#### 9. leads_to
**Definition**: Consequence - A results in or enables B

**Examples:**
- **Laravel**: `[[Passing Validation]] leads_to [[Controller Method Execution]]`
- **React**: `[[setState Call]] leads_to [[Component Re-render]]`
- **Django**: `[[Model Save]] leads_to [[Database Write]]`
- **Vue**: `[[Data Mutation]] leads_to [[DOM Update]]`

**Pattern**: Outcomes, effects, consequences

### Universal Markdown Patterns

Identify and extract these common patterns across all library documentation:

#### 1. Version Information
**Pattern variants:**
```markdown
<!-- Official version syntax -->
Version: 11.x, 18.2.0, 4.3.1

<!-- Version blocks -->
> **Version note**: Available since v3.0

<!-- Compatibility notes -->
Compatible with: PHP 8.1+, Node 18+

<!-- Deprecation warnings -->
⚠️ Deprecated in v5, use X instead
```

**Extract as:**
```yaml
version: "11.x"
minimum_version: "11.0.0"
deprecated_version: null
compatibility: ["PHP 8.1+"]
```

#### 2. Dependencies
**Pattern variants:**
```markdown
<!-- Explicit dependencies -->
Requires: Laravel 10.x, PHP 8.1+

<!-- Installation commands -->
npm install react react-dom
pip install django==4.2

<!-- Peer dependencies -->
Peer dependencies: vue@^3.0.0

<!-- Optional dependencies -->
Optional: @types/react for TypeScript
```

**Extract as:**
```yaml
dependencies:
  required: ["laravel: ^10.0", "php: ^8.1"]
  optional: ["typescript: ^5.0"]
  peer: []
```

#### 3. Best Practices Sections
**Pattern variants:**
```markdown
## Best Practices
## Recommendations
## Tips and Tricks
## Do's and Don'ts
## Common Pitfalls

<!-- Callout boxes -->
💡 Tip: Always validate user input
⚠️ Warning: Never mutate state directly
✅ Do: Use functional updates
❌ Don't: Access state synchronously after setState
```

**Extract as:**
```markdown
[best-practice] Always validate user input
[problem] Mutating state directly causes bugs
[best-practice] Use functional updates for state
[problem] Accessing state synchronously after setState may have stale values
```

#### 4. Code Examples
**Pattern variants:**
````markdown
<!-- Inline examples -->
```php
// Example code here
```

<!-- Titled examples -->
### Example: Basic Usage
```js
// Code
```

<!-- Annotated examples -->
```python
# Step 1: Import
from django.db import models

# Step 2: Define model
class User(models.Model):
    pass
```

<!-- Multiple language examples -->
#### JavaScript
```js
// JS version
```

#### TypeScript
```ts
// TS version
```
````

**Extract as:**
```markdown
[example] Basic usage:
```language
// Full code block with context
```

[example] TypeScript version:
```ts
// Alternative implementation
```
```

#### 5. API Signatures
**Pattern variants:**
```markdown
<!-- Method signatures -->
validate(data: array, rules: array): bool

<!-- Function signatures -->
useState<S>(initialState: S | (() => S)): [S, Dispatch<SetStateAction<S>>]

<!-- Class constructors -->
CharField(max_length=None, **options)

<!-- Component props -->
interface Props {
  value: string;
  onChange: (value: string) => void;
}
```

**Extract as:**
```markdown
[fact] Method signature: `validate(data: array, rules: array): bool`

[fact] Returns boolean indicating validation success

[requirement] data parameter must be associative array
[requirement] rules parameter must be validation rules array
```

#### 6. Configuration Options
**Pattern variants:**
```markdown
<!-- Option tables -->
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| strict | bool | false   | Enable strict mode |

<!-- Config blocks -->
config.strict = true
config.timeout = 5000

<!-- YAML/JSON config -->
{
  "validation": {
    "stopOnFirstFailure": true
  }
}
```

**Extract as:**
```markdown
[fact] Configuration option: `strict` (boolean, default: false)

[fact] When enabled, strict mode enforces additional type checking

[example] Enable strict mode:
```js
config.strict = true;
```
```

#### 7. Error Messages
**Pattern variants:**
```markdown
<!-- Error examples -->
ValidationException: The title field is required.

<!-- Error handling -->
try {
  await api.call();
} catch (error) {
  // Handle error
}

<!-- Error codes -->
Error: VALIDATION_FAILED (code: 422)
```

**Extract as:**
```markdown
[fact] Throws `ValidationException` when validation fails

[example] Error handling pattern:
```js
try {
  await validate(data);
} catch (error) {
  // Handle validation errors
}
```

[problem] Validation errors may contain multiple field errors
[solution] Access error bag to retrieve all field-specific messages
```

### Chunking Strategy

**Goal**: Create semantic, coherent chunks (not arbitrary size splits)

#### Size Guidelines

**Optimal range**: 500-2000 lines per markdown file

**Indicators for splitting:**
- Topic file exceeds 2000 lines → Consider splitting into sub-topics
- Concept section exceeds 500 lines → Consider extracting to separate topic

**Indicators for merging:**
- Topic file under 300 lines → Consider merging with related topic
- Multiple very small topics → Group under parent topic

#### Semantic Boundaries

**Split on:**
1. **Feature boundaries**: Distinct features or modules
2. **API groupings**: Related methods/functions
3. **Use case boundaries**: Different usage scenarios
4. **Version boundaries**: Features by version introduced

**Don't split on:**
1. Arbitrary line counts
2. Middle of code examples
3. Within closely related concepts
4. Breaking observation/relation context

#### Hierarchical Chunking

**Category level** (folders):
- Major functional areas
- Independent enough to stand alone
- 5-15 categories per library

**Topic level** (files):
- Feature sets within category
- 3-8 topics per category
- 500-2000 lines each

**Concept level** (sections):
- Individual methods/patterns
- Multiple concepts per file
- Grouped by relatedness

#### Examples

**Good chunking (Laravel Validation):**
```
Validation/                          # Category
├── form-request-validation.md      # Topic (800 lines)
│   ├── Creating Form Requests      # Concept
│   ├── Authorization Logic         # Concept
│   ├── Validation Rules            # Concept
│   └── Error Handling              # Concept
├── custom-validation-rules.md      # Topic (600 lines)
│   ├── Rule Objects                # Concept
│   ├── Closure Rules               # Concept
│   └── Implicit Rules              # Concept
└── validation-error-messages.md    # Topic (400 lines)
    ├── Default Messages            # Concept
    ├── Custom Messages             # Concept
    └── Localization                # Concept
```

**Bad chunking:**
```
Validation/
├── validation-part-1.md   # ❌ Arbitrary split
├── validation-part-2.md   # ❌ No semantic meaning
└── validation-part-3.md   # ❌ Unclear boundaries
```

**Good chunking (React Hooks):**
```
Hooks/                               # Category
├── state-hooks.md                   # Topic (900 lines)
│   ├── useState                     # Concept
│   ├── useReducer                   # Concept
│   └── State Hook Patterns          # Concept
├── effect-hooks.md                  # Topic (1200 lines)
│   ├── useEffect                    # Concept
│   ├── useLayoutEffect              # Concept
│   ├── Effect Dependencies          # Concept
│   └── Effect Cleanup               # Concept
└── performance-hooks.md             # Topic (700 lines)
    ├── useMemo                      # Concept
    ├── useCallback                  # Concept
    └── Performance Patterns         # Concept
```

### Metadata Schema

Every markdown file must include frontmatter with required fields:

```yaml
---
title: Topic or Concept Name               # Required
library: library-name                      # Required (lowercase, hyphenated)
version: x.y.z                             # Required (semver or official format)
category: Category Name                    # Required
topic: Topic Name                          # Required for concepts
tags: [tag1, tag2, tag3]                   # Required (3-10 tags)
source: https://docs.url/path              # Required (official docs URL)
last_updated: YYYY-MM-DD                   # Required (ISO format)
dependencies:                              # Optional
  required: ["package@version"]
  optional: ["package@version"]
deprecated: false                          # Optional (boolean)
deprecated_version: null                   # Optional (if deprecated)
replacement: "[[New Concept]]"             # Optional (if deprecated)
---
```

#### Field Specifications

**title**
- Human-readable name
- Title case for topics, lowercase for methods/functions
- Match official documentation naming

**library**
- Lowercase, hyphenated
- Examples: `laravel`, `react`, `django-rest-framework`, `vue-router`

**version**
- Use official version format
- Semver: `18.2.0`, `4.3.1`
- Frameworks: `11.x`, `4.x` (if docs cover range)
- Always specify what documentation version was analyzed

**category**
- Top-level functional area
- Title case
- Examples: `Validation`, `Hooks`, `Database`, `Routing`

**topic**
- Specific feature set
- Title case
- Examples: `Form Request Validation`, `State Hooks`, `Model Managers`

**tags**
- 3-10 relevant keywords
- Lowercase, hyphenated
- Include: feature type, use cases, related concepts
- Examples: `[validation, forms, http, requests, security]`

**source**
- Direct URL to official documentation
- Permalink if available
- Include version in URL if documentation is versioned

**last_updated**
- ISO 8601 format: `YYYY-MM-DD`
- Date documentation was analyzed/extracted
- Update when content is refreshed

**dependencies**
- List required and optional packages
- Use format: `"package@version"` or `"package: ^version"`

**deprecated**
- `true` if feature is deprecated in latest version
- Include `deprecated_version` and `replacement` if true

### Output Structure

Complete structure of extracted knowledge base:

```
knowledge-base/libraries/
├── {library-name}/
│   ├── README.md                  # Library overview
│   │   ├── Metadata (frontmatter)
│   │   ├── Overview section
│   │   ├── Installation
│   │   ├── Quick start
│   │   ├── Categories (links to folders)
│   │   └── Version history
│   │
│   ├── {category-1}/
│   │   ├── {topic-1}.md
│   │   │   ├── Frontmatter (metadata)
│   │   │   ├── Overview
│   │   │   ├── ## Concept 1
│   │   │   │   ├── ### Definition
│   │   │   │   ├── ### Key Observations (with [category] tags)
│   │   │   │   ├── ### Code Examples
│   │   │   │   └── ### Relations (WikiLinks)
│   │   │   ├── ## Concept 2
│   │   │   │   └── (same structure)
│   │   │   └── ## Related Topics (links)
│   │   │
│   │   ├── {topic-2}.md
│   │   └── {topic-3}.md
│   │
│   ├── {category-2}/
│   │   ├── {topic-1}.md
│   │   └── {topic-2}.md
│   │
│   └── {category-n}/
│       └── ...
│
└── {another-library}/
    └── (same structure)
```

#### README.md Template

```markdown
---
title: Library Name
library: library-slug
version: x.y.z
type: library-overview
tags: [primary-language, library-type, use-case]
source: https://official-website.com
last_updated: YYYY-MM-DD
---

# Library Name

## Overview

[fact] Brief description of what the library/framework does.

[insight] Key design philosophy or approach.

## Installation

[technique] Installation command:
```bash
command to install
```

[requirement] Minimum version requirements.

## Quick Start

[example] Minimal working example:
```language
// Basic usage
```

## Categories

Organized knowledge by functional area:

- **[[Category 1]]** - Description
- **[[Category 2]]** - Description
- **[[Category 3]]** - Description

## Version History

[fact] Current stable version: x.y.z
[decision] Major version changes and rationale

## Relations

- similar_to: [[Comparable Library]]
- part_of: [[Larger Ecosystem]]
```

#### Topic File Template

```markdown
---
title: Topic Name
library: library-slug
version: x.y.z
category: Category Name
topic: Topic Name
tags: [tag1, tag2, tag3, tag4, tag5]
source: https://docs.url/specific-section
last_updated: YYYY-MM-DD
---

# Topic Name

## Overview

[fact] High-level description of what this topic covers.

[insight] Why this topic matters or when to use it.

---

## Concept 1 Name

### Definition

[fact] Clear, concise definition of the concept.

### Key Observations

[technique] How to use this concept:
```language
// Implementation example
```

[best-practice] Recommended approach.

[requirement] Prerequisites or constraints.

[example] Complete working example:
```language
// Full code with context
```

[problem] Common issues or pitfalls.

[solution] How to avoid or fix problems.

[insight] Non-obvious behavior or implications.

### Relations

- requires: [[Dependency Concept]]
- part_of: [[Parent Feature]]
- uses: [[Utility Concept]]
- similar_to: [[Alternative Approach]]

---

## Concept 2 Name

(Same structure as Concept 1)

---

## Related Topics

Cross-references to related documentation:

- **[[Related Topic 1]]** - Brief description
- **[[Related Topic 2]]** - Brief description
```

### Integration with basic-memory

All extracted knowledge integrates with basic-memory MCP server for storage and retrieval.

#### Configuration

Ensure basic-memory is configured in Claude Code settings:

```json
{
  "mcp-servers": {
    "basic-memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "KNOWLEDGE_BASE": "knowledge-base/libraries"
      }
    }
  }
}
```

#### Operations

**Create knowledge note:**
```
When creating documentation, use basic-memory create_note:
- name: {library}/{category}/{topic}
- content: Full markdown content with frontmatter
```

**Search knowledge:**
```
When user asks about library feature:
1. Use basic-memory search with relevant keywords
2. Return matching concepts
3. Provide summaries with links
```

**Update knowledge:**
```
When documentation is updated:
1. Use basic-memory update_note
2. Preserve existing observations
3. Add new observations with [category] tags
4. Update last_updated field
```

**Retrieve knowledge:**
```
When user references concept:
1. Use basic-memory get_note
2. Parse markdown structure
3. Extract relevant observations and relations
4. Present in context
```

## Workflow

### Step 1: Identify Source

```
User provides: Documentation URL, file path, or library name
Action: Verify source is official documentation
Output: Confirmed source URL or file path
```

### Step 2: Determine Hierarchy

```
Action: Analyze documentation structure
Identify: Categories (top-level sections)
Identify: Topics (sub-sections within categories)
Identify: Concepts (individual methods, patterns, APIs)
Output: Hierarchical outline
```

### Step 3: Extract Categories

```
For each category:
1. Create folder: knowledge-base/libraries/{library}/{category}/
2. Identify all topics within category
3. Note category-level observations (if any)
```

### Step 4: Extract Topics

```
For each topic:
1. Create file: {category}/{topic}.md
2. Add frontmatter with metadata
3. Write overview section
4. Identify all concepts within topic
```

### Step 5: Extract Concepts

```
For each concept:
1. Create section (## heading)
2. Write definition
3. Extract observations (all 10 categories as applicable)
4. Include code examples
5. Map relations to other concepts
```

### Step 6: Apply Observations

```
For each concept:
1. [fact] - Objective statements
2. [technique] - How-to patterns
3. [best-practice] - Recommendations
4. [requirement] - Prerequisites
5. [example] - Code examples
6. [problem] - Issues/limitations
7. [solution] - How to solve problems
8. [insight] - Non-obvious implications
9. [decision] - Design rationale
10. [question] - Unanswered questions

Use multiple observation types per concept
```

### Step 7: Map Relations

```
For each concept:
1. Identify dependencies (requires)
2. Map hierarchy (part_of)
3. Note extensions (extends)
4. Document usage (uses)
5. Find alternatives (similar_to)
6. Add context (relates_to)
7. Highlight differences (contrasts_with)
8. Track causation (caused_by)
9. Note consequences (leads_to)

Use [[WikiLinks]] for all relations
```

### Step 8: Validate & Store

```
1. Validate frontmatter (all required fields present)
2. Validate markdown structure (proper headings)
3. Validate observations (correct [category] tags)
4. Validate relations (valid [[WikiLink]] targets)
5. Store via basic-memory create_note
6. Confirm successful storage
```

## Examples

### Complete Example: Laravel Form Request Validation

**Source**: https://laravel.com/docs/11.x/validation#form-request-validation

**Hierarchy**:
- Category: Validation
- Topic: Form Request Validation
- Concepts: Creating Requests, Authorization, Validation Rules, Error Handling

**Output**: `knowledge-base/libraries/laravel/Validation/form-request-validation.md`

```markdown
---
title: Form Request Validation
library: laravel
version: 11.x
category: Validation
topic: Form Request Validation
tags: [validation, forms, http, requests, authorization]
source: https://laravel.com/docs/11.x/validation#form-request-validation
last_updated: 2024-11-15
dependencies:
  required: ["laravel/framework: ^11.0"]
---

# Form Request Validation

## Overview

[fact] Form requests are custom request classes that encapsulate validation logic and authorization rules.

[insight] Form requests provide a clean separation between HTTP layer and validation logic, keeping controllers thin.

[best-practice] Use form requests for all non-trivial validation scenarios to maintain single responsibility principle.

---

## Creating Form Requests

### Definition

[fact] Form requests are classes that extend `Illuminate\Foundation\Http\FormRequest`.

[fact] Generated using Artisan command: `php artisan make:request {name}`.

### Key Observations

[technique] Generate a form request class:
```bash
php artisan make:request StorePostRequest
```

[fact] Created in `app/Http/Requests/` directory by default.

[example] Basic form request structure:
```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'title' => 'required|string|max:255',
            'body' => 'required|string',
            'author_id' => 'required|exists:users,id',
        ];
    }
}
```

[requirement] Must implement two methods: `authorize()` and `rules()`.

[best-practice] Return `false` from `authorize()` to prevent unauthorized access, not just for validation.

### Relations

- extends: [[HTTP Request]]
- uses: [[Validation Rules]]
- part_of: [[Validation]]

---

## Authorization Logic

### Definition

[fact] The `authorize()` method determines if the current user can make the request.

### Key Observations

[technique] Implement authorization logic:
```php
public function authorize(): bool
{
    $post = Post::find($this->route('post'));
    
    return $post && $this->user()->can('update', $post);
}
```

[fact] Returns boolean: `true` allows request, `false` throws `403 Forbidden`.

[insight] Authorization runs before validation, preventing validation of unauthorized requests.

[decision] Separate method for authorization enforces explicit security checks rather than implicit.

[example] Route parameter access:
```php
public function authorize(): bool
{
    // Access route parameters via $this->route()
    $commentId = $this->route('comment');
    
    return Comment::where('id', $commentId)
        ->where('user_id', $this->user()->id)
        ->exists();
}
```

[best-practice] Use policy methods via `$this->user()->can()` for complex authorization.

[problem] Forgetting to implement authorization returns `true` by default, allowing all requests.

[solution] Explicitly return `false` or implement proper authorization checks.

### Relations

- requires: [[Authentication]]
- uses: [[Policies]]
- relates_to: [[HTTP Middleware]]

---

## Validation Rules

### Definition

[fact] The `rules()` method returns an array of validation rules for request data.

### Key Observations

[technique] Define validation rules:
```php
public function rules(): array
{
    return [
        'title' => 'required|string|max:255',
        'body' => 'required|string',
        'published_at' => 'nullable|date',
        'tags.*' => 'string|max:50',
    ];
}
```

[fact] Rules use pipe-separated syntax or array syntax.

[example] Array syntax for complex rules:
```php
public function rules(): array
{
    return [
        'title' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'unique:users,email'],
    ];
}
```

[technique] Conditional rules based on input:
```php
public function rules(): array
{
    return [
        'role' => 'required|in:admin,user',
        'permissions' => [
            'required_if:role,admin',
            'array',
        ],
    ];
}
```

[best-practice] Use array syntax for rules with commas in parameters to avoid parsing issues.

[example] Dynamic rules based on route:
```php
public function rules(): array
{
    $userId = $this->route('user');
    
    return [
        'email' => "required|email|unique:users,email,{$userId}",
    ];
}
```

[insight] Rules are evaluated only if authorization passes, saving database queries for unauthorized requests.

### Relations

- uses: [[Validation Rules]]
- part_of: [[Form Request Validation]]
- relates_to: [[Custom Validation Rules]]

---

## Error Handling

### Definition

[fact] Validation errors automatically redirect back with errors in session.

### Key Observations

[fact] Failed validation throws `Illuminate\Validation\ValidationException`.

[fact] Exception is automatically caught and converted to redirect response.

[example] Accessing errors in Blade:
```blade
@error('title')
    <div class="text-red-500">{{ $message }}</div>
@enderror
```

[technique] Custom error messages:
```php
public function messages(): array
{
    return [
        'title.required' => 'Please provide a title for your post.',
        'body.required' => 'Post content cannot be empty.',
    ];
}
```

[technique] Custom attribute names:
```php
public function attributes(): array
{
    return [
        'email' => 'email address',
        'published_at' => 'publication date',
    ];
}
```

[best-practice] Override `messages()` for user-friendly error messages.

[example] Stopping on first failure:
```php
public function rules(): array
{
    return [
        'title' => 'required|string|max:255|stopOnFirstFailure',
    ];
}
```

[problem] Multiple validation errors can overwhelm users.

[solution] Use `stopOnFirstFailure` rule or configure per-field stopping.

[insight] Error messages are automatically flashed to session, available in next request.

### Relations

- uses: [[Validation Error Messages]]
- relates_to: [[Session Flashing]]
- part_of: [[Form Request Validation]]

---

## Using Form Requests

### Definition

[fact] Type-hint form request in controller methods to trigger validation.

### Key Observations

[technique] Controller usage:
```php
use App\Http\Requests\StorePostRequest;

class PostController extends Controller
{
    public function store(StorePostRequest $request)
    {
        // Validation already passed at this point
        $validated = $request->validated();
        
        Post::create($validated);
        
        return redirect()->route('posts.index');
    }
}
```

[fact] Laravel automatically resolves and validates form request before controller method execution.

[insight] Controller method only executes if both authorization and validation pass.

[example] Accessing validated data:
```php
$validated = $request->validated(); // Only validated fields
$all = $request->all(); // All request data
$only = $request->only(['title', 'body']); // Specific fields
```

[best-practice] Use `validated()` to ensure only validated data is used, preventing mass assignment vulnerabilities.

[technique] API JSON responses:
```php
public function store(StorePostRequest $request)
{
    $post = Post::create($request->validated());
    
    return response()->json($post, 201);
}
```

[fact] For API requests, validation errors return JSON response automatically.

### Relations

- requires: [[Dependency Injection]]
- uses: [[Controller Methods]]
- part_of: [[Form Request Validation]]

---

## Related Topics

- **[[Manual Validation]]** - Alternative validation approach using Validator facade
- **[[Custom Validation Rules]]** - Creating custom validation logic
- **[[Validation Error Messages]]** - Customizing error message display
- **[[API Validation]]** - Validation for JSON APIs
```

### Complete Example: React useState Hook

**Source**: https://react.dev/reference/react/useState

**Hierarchy**:
- Category: Hooks
- Topic: State Management Hooks
- Concepts: Basic Usage, State Updates, Initialization, Troubleshooting

**Output**: `knowledge-base/libraries/react/Hooks/state-management-hooks.md`

```markdown
---
title: State Management Hooks
library: react
version: 18.x
category: Hooks
topic: State Management Hooks
tags: [hooks, state, useState, useReducer, state-management]
source: https://react.dev/reference/react/useState
last_updated: 2024-11-15
dependencies:
  required: ["react: ^18.0.0"]
---

# State Management Hooks

## Overview

[fact] React provides hooks for managing component state in functional components.

[insight] State hooks replace class component state with a simpler, more composable API.

---

## useState - Basic Usage

### Definition

[fact] `useState` is a React Hook that lets you add state variables to functional components.

[fact] Signature: `const [state, setState] = useState(initialState)`

### Key Observations

[technique] Declare state variable:
```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

[fact] `useState` returns an array with exactly two elements:
1. Current state value
2. State setter function

[requirement] Must be called at the top level of component, not inside loops, conditions, or nested functions.

[best-practice] Use array destructuring for clear, semantic naming.

[example] Multiple state variables:
```jsx
function Form() {
  const [name, setName] = useState('');
  const [age, setAge] = useState(0);
  const [email, setEmail] = useState('');
  
  // Each state is independent
}
```

[insight] Each `useState` call creates independent state that doesn't affect others.

### Relations

- part_of: [[React Hooks]]
- similar_to: [[useReducer]]
- uses: [[Component State]]

---

## useState - State Updates

### Definition

[fact] The setter function from `useState` updates state and triggers re-render.

### Key Observations

[technique] Direct value update:
```jsx
const [count, setCount] = useState(0);

// Direct value
setCount(42);
```

[technique] Functional update:
```jsx
// Functional update based on previous state
setCount(prevCount => prevCount + 1);
```

[best-practice] Use functional updates when new state depends on previous state.

[insight] Functional updates guarantee correct state value in concurrent rendering.

[example] Multiple updates in same event:
```jsx
function handleClick() {
  // Wrong: may not work as expected
  setCount(count + 1);
  setCount(count + 1);
  setCount(count + 1);
  // Only increments by 1
  
  // Correct: use functional updates
  setCount(c => c + 1);
  setCount(c => c + 1);
  setCount(c => c + 1);
  // Increments by 3
}
```

[problem] Multiple `setState` calls with direct values batch and use same initial state.

[solution] Use functional updates: `setState(prev => prev + 1)` for dependent updates.

[fact] State updates are asynchronous and batched for performance.

[insight] React batches multiple `setState` calls in event handlers into single re-render.

[example] Object state updates:
```jsx
const [user, setUser] = useState({ name: '', age: 0 });

// Wrong: mutation
user.name = 'Alice'; // Don't do this!

// Correct: create new object
setUser({ ...user, name: 'Alice' });

// Or with functional update
setUser(prev => ({ ...prev, name: 'Alice' }));
```

[best-practice] Always create new object/array, never mutate state directly.

[problem] Forgetting to spread existing properties loses other state fields.

### Relations

- uses: [[Component Re-rendering]]
- relates_to: [[React Concurrent Mode]]
- contrasts_with: [[Class Component setState]]

---

## useState - Initialization

### Definition

[fact] The `initialState` argument is only used during first render.

### Key Observations

[technique] Simple initial value:
```jsx
const [count, setCount] = useState(0);
const [user, setUser] = useState({ name: 'Guest' });
```

[technique] Lazy initialization for expensive computation:
```jsx
const [data, setData] = useState(() => {
  // Only runs once on mount
  return expensiveComputation(props);
});
```

[best-practice] Use lazy initialization (function) when initial state requires expensive computation.

[insight] Lazy initializer function runs only once on mount, not on every render.

[example] Reading from localStorage:
```jsx
const [settings, setSettings] = useState(() => {
  const saved = localStorage.getItem('settings');
  return saved ? JSON.parse(saved) : defaultSettings;
});
```

[problem] Passing expensive computation directly runs on every render.

[solution] Wrap in function: `useState(() => expensive())` instead of `useState(expensive())`.

[fact] If you pass a function as initial state, it's treated as initializer function.

[example] Storing function in state:
```jsx
// Wrong: calls the function
const [fn, setFn] = useState(myFunction);

// Correct: wrap in arrow function
const [fn, setFn] = useState(() => myFunction);
```

### Relations

- uses: [[Component Mounting]]
- relates_to: [[Performance Optimization]]

---

## useState - Troubleshooting

### Definition

[fact] Common issues and solutions when using useState.

### Key Observations

[problem] State update doesn't reflect immediately:
```jsx
function handleClick() {
  setCount(count + 1);
  console.log(count); // Still shows old value!
}
```

[insight] State updates are asynchronous; new value available in next render.

[solution] Use useEffect to react to state changes:
```jsx
useEffect(() => {
  console.log('Count changed:', count);
}, [count]);
```

[problem] State resets unexpectedly:
```jsx
// Wrong: component re-mounts on every render of parent
function Parent() {
  return (
    <div>
      {someCondition && <Child />}
    </div>
  );
}
```

[insight] Conditional rendering can cause component to unmount/remount, resetting state.

[solution] Move state up to parent or use `key` prop to preserve identity.

[question] Does useState preserve state across re-renders?

[fact] Yes, useState preserves state as long as component remains mounted in same position.

[decision] React team chose simple API (array return) over object for easy destructuring with custom names.

### Relations

- relates_to: [[React Component Lifecycle]]
- relates_to: [[useEffect]]
- contrasts_with: [[Component Remounting]]

---

## useReducer - Alternative for Complex State

### Definition

[fact] `useReducer` is an alternative to `useState` for complex state logic.

### Key Observations

[technique] Basic useReducer usage:
```jsx
import { useReducer } from 'react';

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });
  
  return (
    <>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </>
  );
}
```

[fact] `useReducer` returns `[state, dispatch]` tuple.

[best-practice] Use `useReducer` when:
- State logic is complex
- Multiple related state values
- Next state depends on previous state
- State updates triggered from multiple places

[example] Complex form state:
```jsx
function formReducer(state, action) {
  switch (action.type) {
    case 'SET_FIELD':
      return { ...state, [action.field]: action.value };
    case 'RESET':
      return initialState;
    case 'SUBMIT':
      return { ...state, submitting: true };
    default:
      return state;
  }
}
```

[insight] Reducer pattern makes state transitions explicit and testable.

[contrasts_with] `useState` is simpler for independent values; `useReducer` better for related values.

### Relations

- similar_to: [[useState]]
- extends: [[useState]] functionality
- uses: [[Reducer Pattern]]
- part_of: [[React Hooks]]

---

## Related Topics

- **[[useEffect]]** - Side effects in function components
- **[[useContext]]** - Consuming context in function components
- **[[useMemo]]** - Memoizing expensive computations
- **[[useCallback]]** - Memoizing functions
- **[[Custom Hooks]]** - Building reusable stateful logic
```

## Key Principles

1. **Universal applicability**: Methodology works for any library/framework
2. **Semantic organization**: Hierarchical structure based on meaning, not arbitrary splits
3. **Rich observations**: Use all 10 categories to capture complete knowledge
4. **Explicit relations**: Map connections between concepts precisely
5. **Metadata completeness**: Always include version, source, dependencies
6. **Code examples**: Concrete, runnable code with context
7. **Integration**: Store in basic-memory for retrieval and search

## Success Criteria

Knowledge extraction is complete when:

- [ ] All major features documented (categories identified)
- [ ] Feature sets organized into topics (semantic groupings)
- [ ] Individual concepts extracted (methods, patterns, APIs)
- [ ] All 10 observation categories applied where relevant
- [ ] Relations mapped between related concepts
- [ ] Metadata complete (version, source, tags, dependencies)
- [ ] Code examples included for techniques
- [ ] Stored in basic-memory and searchable
- [ ] Follows universal markdown patterns
- [ ] Semantic chunking applied (500-2000 lines per file)

When user requests library documentation analysis, follow this methodology systematically to create comprehensive, structured, and searchable knowledge base.
