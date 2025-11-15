---
name: your-skill-name
description: Use this skill when [describe specific situations when this skill should be invoked]. This includes [list concrete use cases and trigger keywords that should activate this skill].
---

# [Skill Name]

[Brief overview of what this skill does and why it exists - keep concise]

# Core Approach

[Describe the fundamental methodology this skill uses]

# Step-by-Step Instructions

## 1. [First Major Step]

[Clear, actionable instructions for the first step]

- Specific action using CLI tools where applicable
- Another action item
- Validation step

**CLI Tools:**
- `command-name` - What it does
- `another-command` - What it does

## 2. [Second Major Step]

[Clear, actionable instructions]

**Python Example:**
```python
#!/usr/bin/env python3
from pathlib import Path

# Your implementation here
data = Path('input.txt').read_text()
print(data)
```

## 3. [Third Major Step]

[Clear, actionable instructions with complete, runnable commands]

```bash
gh repo view --json name,description
pip install useful-package
aws s3 ls s3://bucket-name/
```

# Examples

## Example 1: [Use Case Name]

**User Query**: "[Example of what user might say]"

**Approach**:
1. Use `cli-tool` to gather information
2. Process with Python script
3. Validate output with another CLI command

**Complete Commands:**
```bash
# Step 1
gh api repos/owner/repo

# Step 2 - Python processing
python process-data.py

# Step 3 - Validation
pytest
```

**Expected Outcome**: [What should result]

## Example 2: [Another Use Case]

**User Query**: "[Another example query]"

**Approach**:
1. [Step using CLI tools]
2. [Step using Python]
3. [Verification step]

# CLI Tools to Leverage

**Essential tools for this skill:**
- `gh` - GitHub CLI operations
- `pip` - Package management
- `aws` - AWS CLI operations (if applicable)
- `git` - Version control operations
- `jq` - JSON processing
- [Other relevant CLI tools]

**Global Python Packages to Consider:**
- `pip install package-name` - [Purpose]
- `pip install another-package` - [Purpose]

# Python Patterns

**File Operations:**
```python
#!/usr/bin/env python3
from pathlib import Path

content = Path('input.txt').read_text()
Path('output.txt').write_text(content.upper())
```

**Running CLI Commands from Python:**
```python
#!/usr/bin/env python3
import subprocess
import json

result = subprocess.run(['gh', 'repo', 'view', '--json', 'name'],
                       capture_output=True, text=True)
repo = json.loads(result.stdout)
print(repo['name'])
```

**Processing JSON Data:**
```python
#!/usr/bin/env python3
from pathlib import Path
import json

data = json.loads(Path('data.json').read_text())
filtered = [item for item in data if item.get('active')]
print(filtered)
```

# Best Practices

- Challenge each instruction: "Does Claude really need this context?"
- Keep SKILL.md under 500 lines
- Use CLI tools liberally for operations
- Write Python scripts (not Node.js) for complex logic
- Provide complete, runnable commands
- Reference supporting files with relative paths (e.g., `./details.md`)
- Use intention-revealing names for all files
- Show command chaining when helpful

# Validation Checklist

When completing a task with this skill, verify:
- [ ] CLI commands executed successfully
- [ ] Output matches expected format
- [ ] No errors in console output
- [ ] Results are validated with test commands
- [ ] [Domain-specific validation item]

# Troubleshooting

## Issue: [Common Problem]

**Symptoms**: [What user sees]

**Investigation**:
```bash
# Check logs or status
command-to-diagnose
```

**Solution**: [How to fix with specific commands]

## Issue: [Another Problem]

**Symptoms**: [What user sees]

**Investigation**:
```bash
# Diagnostic command
another-diagnostic-command
```

**Solution**: [How to fix]

# Supporting Files

[Reference other files in the skill directory using relative paths]

- See `./detailed-methodology.md` for [what it contains]
- See `./templates/` for [what templates are available]
- See `./scripts/` for [what helper scripts exist]

Remember: All scripts should be Python, not Node.js!
