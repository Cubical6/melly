# melly-writer-lib

Universal library documentation analyzer with metadata extraction for the Melly marketplace.

## Overview

The `melly-writer-lib` plugin provides a systematic methodology for analyzing and documenting third-party libraries, frameworks, and packages. It extracts structured knowledge from documentation sources into a hierarchical format compatible with the C4 model knowledge base.

## Features

- **Universal Documentation Analysis**: Works with any library/framework documentation (Laravel, React, Django, Vue, etc.)
- **Hierarchical Organization**: Three-level structure (Category → Topic → Concept)
- **Rich Metadata Extraction**: Version info, dependencies, best practices, code examples
- **10 Observation Categories**: Facts, techniques, best practices, requirements, examples, and more
- **9 Relation Types**: Comprehensive relationship mapping (requires, extends, uses, etc.)
- **Semantic Chunking**: Intelligent content splitting based on meaning, not arbitrary size limits
- **Integration with basic-memory**: Direct integration with MCP knowledge base

## Installation

### Prerequisites

- Claude Code CLI with MCP support
- basic-memory MCP server configured

### Install Plugin

```bash
# From Melly repository root
cd /path/to/melly
/plugin add ./plugins/melly-writer-lib
```

Or via marketplace:

```bash
/plugin add melly-writer-lib
```

## Components

### Skills

- **lib-doc-methodology** - Complete methodology for universal library documentation analysis
  - Hierarchical level definitions (Category, Topic, Concept)
  - 10 observation categories with examples
  - 9 relation types with examples
  - Chunking strategy and best practices
  - Metadata schema and output structure

### Usage

The skill is automatically activated when Claude detects library documentation analysis tasks. Keywords that trigger activation:

- "document this library"
- "analyze [framework] documentation"
- "extract knowledge from [package] docs"
- "create knowledge base for [library]"

#### Example Usage

```
> I need to document the Laravel validation features from the official docs. Can you help?
```

Claude will automatically activate the `lib-doc-methodology` skill and guide you through the extraction process.

#### Manual Activation

You can also explicitly request the skill:

```
> Use the lib-doc-methodology skill to analyze the React hooks documentation
```

## Workflow

### 1. Identify Documentation Source

Provide Claude with the documentation URL or file path:

```
> Analyze the Laravel validation documentation at https://laravel.com/docs/11.x/validation
```

### 2. Hierarchical Extraction

The methodology extracts knowledge in three levels:

**Level 1: Category**
- Broad functional area (e.g., "Validation", "Authentication", "Database")
- Parent folder in knowledge base

**Level 2: Topic**
- Specific feature set (e.g., "Form Request Validation", "Custom Validation Rules")
- Markdown file with overview

**Level 3: Concept**
- Individual concept, method, or technique
- Section within markdown file with full details

### 3. Metadata Extraction

Each knowledge entry includes:

```yaml
---
title: Concept Name
library: library-name
version: x.y.z
category: category-name
topic: topic-name
tags: [tag1, tag2, tag3]
source: https://docs.url/path
last_updated: YYYY-MM-DD
---
```

### 4. Observation Categories

10 types of observations are extracted:

1. **[fact]** - Definitive statements about functionality
2. **[technique]** - Specific implementation patterns
3. **[best-practice]** - Recommended approaches
4. **[requirement]** - Prerequisites and dependencies
5. **[example]** - Code examples and usage patterns
6. **[problem]** - Known issues or limitations
7. **[solution]** - How to solve specific problems
8. **[insight]** - Non-obvious implications or behaviors
9. **[decision]** - Design decisions and their rationale
10. **[question]** - Unanswered questions or ambiguities

### 5. Relation Mapping

9 types of relations between concepts:

1. **requires** - Direct dependency (A requires B to function)
2. **part_of** - Compositional relationship (A is part of B)
3. **extends** - Inheritance or extension (A extends B)
4. **uses** - Utilization (A uses B as a tool/utility)
5. **similar_to** - Analogous functionality (A similar to B)
6. **relates_to** - General connection (A relates to B)
7. **contrasts_with** - Differences (A contrasts with B)
8. **caused_by** - Causation (A caused by B)
9. **leads_to** - Consequence (A leads to B)

### 6. Output Structure

Knowledge is organized as:

```
knowledge-base/libraries/{library-name}/
├── {category-1}/
│   ├── {topic-1}.md
│   ├── {topic-2}.md
│   └── {topic-3}.md
├── {category-2}/
│   ├── {topic-1}.md
│   └── {topic-2}.md
└── README.md  # Library overview
```

## Examples

### Laravel Validation Documentation

**Input:**
```
> Document Laravel's Form Request Validation feature
```

**Output:**
```markdown
---
title: Form Request Validation
library: laravel
version: 11.x
category: Validation
topic: Form Request Validation
tags: [validation, forms, http, requests]
source: https://laravel.com/docs/11.x/validation#form-request-validation
last_updated: 2024-11-15
---

## Overview

[fact] Form requests are custom request classes that encapsulate validation logic.

## Key Observations

### Creating Form Requests

[technique] Generate a form request class using Artisan:
```bash
php artisan make:request StorePostRequest
```

[example] Basic form request structure:
```php
class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => 'required|max:255',
            'body' => 'required',
        ];
    }
}
```

### Usage Patterns

[technique] Type-hint the form request in your controller:
```php
public function store(StorePostRequest $request)
{
    // Validation automatically performed
    $validated = $request->validated();
}
```

[best-practice] Keep authorization and validation logic in form requests, not controllers.

## Relations

- requires: [[Laravel HTTP Requests]]
- part_of: [[Validation]]
- uses: [[Validation Rules]]
- relates_to: [[Validation Error Messages]]
```

### React Hooks Documentation

**Input:**
```
> Analyze React's useState hook from the official documentation
```

**Output:**
```markdown
---
title: useState Hook
library: react
version: 18.x
category: Hooks
topic: State Management Hooks
tags: [hooks, state, useState]
source: https://react.dev/reference/react/useState
last_updated: 2024-11-15
---

## Overview

[fact] useState is a React Hook that lets you add state to functional components.

## Key Observations

### Basic Usage

[technique] Declare state with useState:
```jsx
const [count, setCount] = useState(0);
```

[fact] useState returns an array with two elements: current state value and setter function.

### State Updates

[example] Increment state value:
```jsx
setCount(count + 1);  // Direct value
setCount(c => c + 1); // Functional update
```

[best-practice] Use functional updates when next state depends on previous state.

[insight] Functional updates guarantee correct state in concurrent renders.

### Initialization

[technique] Lazy initialization for expensive computations:
```jsx
const [state, setState] = useState(() => {
  return expensiveComputation(props);
});
```

[requirement] Initial state is only used during first render.

## Relations

- part_of: [[React Hooks]]
- similar_to: [[useReducer]]
- uses: [[React Component State]]
- relates_to: [[Component Re-rendering]]
```

## Best Practices

### 1. Semantic Chunking

- Keep related concepts together in one markdown file
- Split by semantic boundaries (features, modules), not arbitrary size
- Aim for 500-2000 lines per file
- Use clear section headings with `##` and `###`

### 2. Rich Metadata

- Always include version information
- Tag liberally with relevant keywords
- Link to official source documentation
- Update `last_updated` when documentation changes

### 3. Observation Categories

- Use multiple observation types per concept
- Include code examples for all techniques
- Document both what works and what doesn't (problems/solutions)
- Capture design decisions and rationale

### 4. Relation Mapping

- Create bidirectional relations where appropriate
- Use specific relation types (not just "relates_to")
- Link to other concepts using [[WikiLinks]]
- Map dependencies explicitly

### 5. Universal Patterns

- Identify common patterns across frameworks (e.g., validation, routing, state management)
- Document framework-specific idioms
- Note version differences explicitly
- Include migration guides when breaking changes occur

## Integration with basic-memory

All extracted knowledge is stored in the basic-memory MCP server:

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

### Operations

- **create_note**: Store new concept documentation
- **search**: Full-text search across all library docs
- **get_note**: Retrieve specific concept by name
- **update_note**: Modify existing documentation
- **list_notes**: Browse all documented concepts

## Troubleshooting

### Skill Not Activating

**Check description keywords**: Ensure your prompt includes terms like "document", "library", "framework", "analyze docs"

**Explicit activation**: Use "Use the lib-doc-methodology skill to..."

**Verify installation**: Run `/plugins` to confirm melly-writer-lib is installed

### Metadata Missing

**Check frontmatter syntax**: YAML must be valid (use validators)

**Required fields**: Ensure title, library, category, topic are present

**Version format**: Use semver or official version scheme (e.g., "11.x", "18.2.0")

### Observations Not Categorized

**Use brackets**: Observations must start with [category] marker

**Valid categories**: Use only the 10 defined categories

**Multiple per section**: A concept can have multiple observation types

## Contributing

To extend or improve this plugin:

1. **Add new observation categories**: Edit SKILL.md with rationale
2. **Add new relation types**: Document use cases and examples
3. **Improve chunking strategy**: Propose heuristics for better semantic splitting
4. **Add framework-specific patterns**: Document unique idioms

Submit improvements via pull request to the Melly repository.

## References

- **Methodology**: See `skills/lib-doc-methodology/SKILL.md` for complete documentation
- **C4 Model Integration**: See `docs/c4model-methodology.md` for how library docs fit into C4
- **basic-memory MCP**: Official MCP documentation at https://modelcontextprotocol.io

## License

Part of the Melly marketplace. See main repository for license information.

## Support

- GitHub Issues: https://github.com/your-org/melly/issues
- Documentation: See `docs/` folder in main repository
- Community: [Community link]

---

**Version**: 1.0.0
**Last Updated**: 2024-11-15
**Maintainer**: Melly Team
