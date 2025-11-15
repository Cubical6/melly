# Melly - Claude Code Workflow Configuration Guide

> A marketplace of Claude Code components for contextual knowledge retrieval

## Overview

Melly is a marketplace consisting of Claude Code components for contextual retrieval from a knowledge base that Claude Code can use.

**This document serves as an implementation guide** to help build and configure production-ready agents, hooks, slash commands, and skills that enable intelligent knowledge retrieval and workflow automation for the Melly marketplace.

## Repository Structure

```
melly/
├── .claude-plugin/           # Plugin configuration
│   └── marketplace.json      # Marketplace definition
├── docs/                     # Documentation knowledge base
│   └── claude-code/         # Claude Code documentation
│       ├── sub-agents.md
│       ├── slash-commands.md
│       ├── skills.md
│       ├── hooks.md
│       ├── hooks-guide.md
│       ├── common-workflows.md
│       ├── cli-reference.md
│       └── ...
├── CLAUDE.md                # This guide
└── README.md

Future structure:
├── .claude/
│   ├── agents/              # Project subagents
│   ├── commands/            # Project slash commands
│   ├── skills/              # Project skills
│   ├── hooks/               # Hook scripts
│   └── settings.json        # Project settings
```

---

## 1. Subagents (Specialized AI Assistants)

### What are Subagents?

Subagents are specialized AI assistants that handle specific tasks with:
- Own context window (separate from main conversation)
- Custom system prompt
- Restricted tool access (optional)
- Specific area of expertise

> **Complete Guide**: See `docs/claude-code/sub-agents.md` for detailed subagent documentation and advanced patterns.

### Locations

| Type | Location | Scope | Priority |
|------|---------|-------|----------|
| **Project** | `.claude/agents/` | Current project | Highest |
| **User** | `~/.claude/agents/` | All projects | Lower |
| **CLI** | `--agents` flag | Current session | Between project and user |

### File Format

```markdown
---
name: agent-name
description: When this agent should be used and what it does
tools: Read, Grep, Glob, Bash  # Optional - inherits all tools if omitted
model: sonnet  # Optional - sonnet, opus, haiku, or 'inherit'
---

# System Prompt

You are a [role]. When invoked:

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Checklist

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Best Practices

- Principle 1
- Principle 2
```

### Practical Examples

#### Code Reviewer Agent

```markdown
---
name: code-reviewer
description: Expert code reviewer. Use PROACTIVELY after code changes to check quality, security, and maintainability.
tools: Read, Grep, Glob, Bash
model: inherit
---

# Code Reviewer

You are a senior code reviewer ensuring high standards of code quality and security.

## Workflow

When invoked:
1. Run `git diff` to see recent changes
2. Focus on modified files
3. Begin review immediately

## Review Checklist

### Critical (must fix)
- Security: exposed secrets, API keys, SQL injection
- Bugs: logic errors, unhandled edge cases
- Breaking changes without migration path

### Warnings (should fix)
- Code duplication
- Missing error handling
- Performance issues
- Missing tests for new features

### Suggestions (consider improving)
- Code complexity can be simplified
- Better naming possible
- Documentation can be expanded
- Refactoring opportunities

## Output Format

Provide feedback organized by priority:
- File name and line number
- Issue description
- Specific example of how to fix
```

#### Test Runner Agent

```markdown
---
name: test-runner
description: Test automation expert. Use PROACTIVELY to run tests and fix failures after code changes.
tools: Read, Edit, Bash, Grep
model: sonnet
---

# Test Runner

You are a test automation expert who runs tests and automatically resolves failures.

## Workflow

1. Detect test framework (pytest, jest, go test, etc.)
2. Run relevant tests for changed code
3. If tests fail:
   - Analyze the failure
   - Identify root cause
   - Fix the issue while preserving test intent
4. Re-run tests until everything passes

## Test Strategy

- Run unit tests first (fast feedback)
- Run integration tests next
- On failures: focus on first failure first
- Maintain test coverage when fixing

## Output

Always report:
- Which tests were run
- Test results (passed/failed/skipped)
- For failures: diagnosis and fix
```

#### Debugger Agent

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use PROACTIVELY when encountering issues.
tools: Read, Edit, Bash, Grep, Glob
---

# Debugger

You are an expert debugger specializing in root cause analysis.

## Debug Process

1. **Capture Context**
   - Error message and stack trace
   - Reproduction steps
   - Environment info (OS, versions, etc.)

2. **Isolate**
   - Locate where failure occurs
   - Identify recent changes
   - Test hypotheses

3. **Fix**
   - Implement minimal fix
   - Verify solution works
   - Add preventive measures

4. **Document**
   - Root cause explanation
   - Fix description
   - Prevention recommendations

## Debug Techniques

- Binary search for regression bugs
- Add strategic logging
- Inspect variable states
- Check recent commits (`git log`, `git blame`)
```

### Creating Agents

**Via CLI Interface (Recommended):**

```bash
/agents
```

Select "Create New Agent" and follow the prompts.

**Via File:**

```bash
# Project agent
mkdir -p .claude/agents
cat > .claude/agents/my-agent.md << 'EOF'
---
name: my-agent
description: Description of when to use this agent
---
System prompt here...
EOF

# User agent
mkdir -p ~/.claude/agents
cat > ~/.claude/agents/my-agent.md << 'EOF'
...
EOF
```

**Via CLI Flag:**

```bash
claude --agents '{
  "reviewer": {
    "description": "Code reviewer. Use after changes.",
    "prompt": "You are a code reviewer...",
    "tools": ["Read", "Grep"],
    "model": "sonnet"
  }
}'
```

### Using Agents

**Automatic (recommended):**

Claude delegates automatically based on the `description` field.

**Explicit:**

```
> Use the code-reviewer agent to check my changes
> Have the debugger agent investigate this error
```

### Best Practices

1. **Focused agents**: One responsibility per agent
2. **Detailed prompts**: Specific instructions and examples
3. **Limit tools**: Only necessary tools
4. **Descriptive descriptions**: Include "use PROACTIVELY" for automatic use
5. **Version control**: Check project agents into git for team use

---

## 2. Slash Commands (Reusable Prompts)

### What are Slash Commands?

Slash commands are reusable prompt templates stored as Markdown files.

> **Complete Guide**: See `docs/claude-code/slash-commands.md` for detailed command syntax and advanced features.

### Locations

| Type | Location | Scope | Indicator in /help |
|------|---------|-------|-------------------|
| **Project** | `.claude/commands/` | Current project | (project) |
| **User** | `~/.claude/commands/` | All projects | (user) |
| **Plugin** | Plugin `commands/` dir | Via plugin | (plugin-name) |

### Basic Format

```markdown
---
description: Brief description of the command
argument-hint: [arg1] [arg2]  # Optional
allowed-tools: Bash(git:*), Read, Edit  # Optional
model: claude-3-5-haiku-20241022  # Optional
disable-model-invocation: false  # Optional
---

Command prompt text here.

Use $ARGUMENTS for all arguments.
Use $1, $2, $3 for individual arguments.
```

### Practical Examples

#### Git Commit Command

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit with structured message
---

## Context

- Current git status: !`git status`
- Git diff (staged and unstaged): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Task

Create a git commit:

1. Analyze all changes (staged and unstaged)
2. Draft a concise commit message (1-2 sentences) focusing on the "why"
3. Follow the commit message style from recent commits
4. Stage relevant files
5. Create the commit
6. Run `git status` for verification

Commit message format:
- First line: <type>: <short description> (max 50 chars)
- Types: feat, fix, docs, refactor, test, chore
- Body: Optional, more details if needed
```

#### Code Review Command

```markdown
---
description: Review code for bugs and improvements
argument-hint: [file-path]
allowed-tools: Read, Grep, Bash(git diff:*)
---

Review $1 for:

1. **Security**: SQL injection, XSS, exposed secrets
2. **Bugs**: Logic errors, edge cases, null checks
3. **Performance**: N+1 queries, inefficient loops
4. **Code Quality**: Duplication, complexity, naming
5. **Tests**: Coverage for new functionality

Provide specific examples and line numbers.
```

#### PR Creation Command

```markdown
---
description: Create a pull request with comprehensive context
allowed-tools: Bash(gh:*), Bash(git:*)
---

## Gather Context

1. Git status: !`git status`
2. Branch info: !`git log origin/main..HEAD --oneline`
3. Diff vs main: !`git diff origin/main...HEAD`

## Create PR

1. Analyze ALL commits in the branch (not just the latest!)
2. Draft PR summary:
   - ## Summary: 2-3 bullet points
   - ## Changes: List of main changes
   - ## Testing: Test plan checklist
   - ## Notes: Extra context, breaking changes, etc.

3. Push branch if needed
4. Create PR with gh CLI:

```bash
gh pr create --title "title" --body "$(cat <<'EOF'
## Summary
- Point 1
- Point 2

## Testing
- [ ] Unit tests
- [ ] Integration tests
EOF
)"
```

Return PR URL.
```

#### Fix Issue Command

```markdown
---
description: Fix a GitHub issue systematically
argument-hint: [issue-number]
---

Fix issue #$1:

1. **Understand the issue**
   - Read issue description and comments
   - Identify root cause

2. **Locate code**
   - Find relevant files
   - Analyze current implementation

3. **Implement solution**
   - Fix the root cause (not just symptoms)
   - Follow codebase conventions

4. **Test**
   - Add/update tests
   - Run test suite

5. **Document**
   - Update docs if needed
   - Draft PR description that links the issue
```

### Bash Execution in Commands

```markdown
---
allowed-tools: Bash(npm:*), Bash(git:*)
---

Current package version: !`npm version --json | jq -r '.version'`
Git status: !`git status --short`

[Rest of command...]
```

### File References in Commands

```markdown
Review the implementation in @src/utils/auth.js

Compare @src/old.js with @src/new.js
```

### Creating Commands

**Project command:**

```bash
mkdir -p .claude/commands
echo "Optimize this code for performance:" > .claude/commands/optimize.md
```

**User command:**

```bash
mkdir -p ~/.claude/commands
echo "Review code for security vulnerabilities:" > ~/.claude/commands/security.md
```

**With namespacing:**

```bash
mkdir -p .claude/commands/git
echo "Create feature branch:" > .claude/commands/git/feature.md
# Command: /feature (description shows: "project:git")
```

### Using Commands

```
> /optimize
> /security
> /fix-issue 123
> /commit
```

### Best Practices

1. **Use for frequent prompts**: Repeatable tasks
2. **Clear descriptions**: How and when to use
3. **Argument hints**: Help users with syntax
4. **Tool restrictions**: Limit to necessary tools
5. **Include context**: Use !`command` for runtime data

---

## 3. Skills (Extensible Capabilities)

### What are Skills?

Skills are modular capabilities that extend Claude's functionality via:
- Organized folders with instructions, scripts, and resources
- **Model-invoked**: Claude decides automatically when to use them
- Progressive disclosure: Files loaded only when needed

> **Complete Guide**: See `docs/claude-code/skills.md` for detailed skill authoring and best practices.

### Locations

| Type | Location | Scope |
|------|---------|-------|
| **Personal** | `~/.claude/skills/` | All projects |
| **Project** | `.claude/skills/` | Current project |
| **Plugin** | Plugin `skills/` dir | Via plugin |

### Structure

```
skill-name/
├── SKILL.md              # Required: Main skill definition
├── reference.md          # Optional: Detailed reference
├── examples.md           # Optional: Usage examples
├── scripts/              # Optional: Helper scripts
│   ├── helper.py
│   └── validate.sh
└── templates/            # Optional: Templates
    └── template.txt
```

### SKILL.md Format

```yaml
---
name: skill-name
description: What this skill does and when Claude should use it. Very important for discovery!
allowed-tools: Read, Bash, Edit  # Optional: restrict tool access
---

# Skill Name

## Instructions

Step-by-step instructions for Claude.

## Examples

Concrete examples of skill usage.

## Requirements

Packages that need to be installed:
```bash
pip install package1 package2
```

## Advanced

See [reference.md](reference.md) for detailed documentation.
```

### Practical Examples

#### Commit Message Generator Skill

```yaml
---
name: commit-message-generator
description: Generate clear git commit messages from diffs. Use when writing commit messages or reviewing staged changes.
allowed-tools: Bash(git:*), Read
---

# Commit Message Generator

## Instructions

1. Run `git diff --staged` to see changes
2. Analyze the changes:
   - What was added/removed/modified?
   - Which components are affected?
   - What is the business impact?
3. Generate commit message:
   - Summary under 50 characters
   - Type: feat/fix/docs/refactor/test/chore
   - Body with details if needed

## Format

```
<type>: <short description>

Optional body with more context:
- Why this change?
- What problem does it solve?
- Special notes
```

## Best Practices

- Use present tense ("Add feature" not "Added feature")
- Explain what and why, not how
- Reference issue numbers: "Fixes #123"
```

#### PDF Processing Skill

```yaml
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
allowed-tools: Bash, Read, Write
---

# PDF Processing

## Quick Start

### Extract Text

```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    print(text)
```

### Fill Forms

See [FORMS.md](FORMS.md) for form filling examples.

### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

merger = PdfWriter()
for pdf in ["file1.pdf", "file2.pdf"]:
    merger.append(pdf)
merger.write("merged.pdf")
```

## Requirements

```bash
pip install pypdf pdfplumber
```

## Scripts

- `scripts/extract.py`: Batch text extraction
- `scripts/fill_form.py`: Automated form filling
- `scripts/validate.py`: PDF validation

See [REFERENCE.md](REFERENCE.md) for complete API reference.
```

#### Code Quality Checker Skill

```yaml
---
name: code-quality-checker
description: Analyze code quality and generate reports. Use for code review, refactoring planning, or quality audits.
allowed-tools: Read, Grep, Bash
---

# Code Quality Checker

## Instructions

1. Scan codebase for quality issues:
   - Code duplication (>10 lines)
   - Complex functions (cyclomatic complexity >10)
   - Long files (>500 lines)
   - Missing documentation
   - Deprecated APIs

2. Generate report with:
   - Issue severity (critical/warning/info)
   - File and line number
   - Recommendation for fix

3. Prioritize issues by impact

## Quality Metrics

### Cyclomatic Complexity
- 1-10: Simple, low risk
- 11-20: Moderate, medium risk
- 21+: Complex, high risk

### Code Duplication
- Threshold: 10 lines exact match
- Impact: Maintenance burden, inconsistency risk

### File Length
- Threshold: 500 lines
- Recommendation: Split on logical boundaries

## Tools

```bash
# Python complexity
radon cc src/ -a

# Find duplicates
jscpd src/

# Count lines
cloc src/
```
```

### Creating Skills

```bash
# Project skill
mkdir -p .claude/skills/my-skill
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does and when to use it. Include keywords!
---

# My Skill

Instructions here...
EOF

# Personal skill
mkdir -p ~/.claude/skills/my-skill
# ... same structure
```

### Testing Skills

```
> Can you help me with [keyword from description]?
```

Claude automatically activates the skill if it matches.

### Debugging Skills

**Skill not being used:**

1. **Check description**: Specific enough? Include keywords?
   ```yaml
   # Too vague
   description: Helps with documents

   # Specific
   description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
   ```

2. **Verify path**:
   ```bash
   ls ~/.claude/skills/my-skill/SKILL.md
   ls .claude/skills/my-skill/SKILL.md
   ```

3. **Check YAML syntax**:
   ```bash
   cat SKILL.md | head -n 10
   ```

4. **View errors**:
   ```bash
   claude --debug
   ```

### Best Practices

1. **Focused skills**: One capability per skill
2. **Clear descriptions**: Include what, when, and keywords
3. **Progressive disclosure**: Link to extra docs, load only when needed
4. **Document dependencies**: List required packages in description
5. **Test with team**: Verify skill activation expectations
6. **Version in SKILL.md**: Track changes over time

---

## 4. Hooks (Event-Driven Automation)

### What are Hooks?

Hooks are shell commands automatically executed on specific events in the Claude Code lifecycle. They provide deterministic control over behavior.

> **Quick Start**: See `docs/claude-code/hooks-guide.md` for a beginner-friendly introduction to hooks.
> **Complete Reference**: See `docs/claude-code/hooks.md` for detailed hook documentation.

### Use Cases

- **Notifications**: Desktop alerts for permission requests
- **Auto-formatting**: Run prettier/gofmt after file edits
- **Logging**: Track all commands for compliance
- **Feedback**: Automatic feedback on convention violations
- **Permissions**: Block edits to sensitive files

### Hook Events

| Event | When | Can Block |
|-------|------|-----------|
| **PreToolUse** | Before tool call | ✅ Yes |
| **PostToolUse** | After tool call | ⚠️ Partially (tool already ran) |
| **PermissionRequest** | On permission dialog | ✅ Yes |
| **Notification** | On notifications | ❌ No |
| **UserPromptSubmit** | Before prompt processing | ✅ Yes |
| **Stop** | When agent stops | ✅ Yes (force continue) |
| **SubagentStop** | When subagent stops | ✅ Yes (force continue) |
| **PreCompact** | Before compact operation | ❌ No |
| **SessionStart** | On session start | ❌ No |
| **SessionEnd** | On session end | ❌ No |

### Configuration Locations

Hooks are configured in settings files:
- `~/.claude/settings.json` - User settings
- `.claude/settings.json` - Project settings
- `.claude/settings.local.json` - Local project (not committed)
- Plugin `hooks/hooks.json` - Plugin hooks

### Basic Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // Optional for some events
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60  // Optional, seconds
          }
        ]
      }
    ]
  }
}
```

### Practical Examples

#### 1. Bash Command Logger (PreToolUse)

**Settings JSON:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \\\"No description\\\")\"' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

#### 2. Auto Formatting (PostToolUse)

**Settings JSON:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh"
          }
        ]
      }
    ]
  }
}
```

**Script: `.claude/hooks/format.sh`**
```bash
#!/bin/bash
set -euo pipefail

# Parse input
FILE_PATH=$(jq -r '.tool_input.file_path' | head -1)

# Exit if no file path
if [ -z "$FILE_PATH" ] || [ "$FILE_PATH" = "null" ]; then
    exit 0
fi

# Format based on extension
case "$FILE_PATH" in
    *.ts|*.tsx|*.js|*.jsx)
        npx prettier --write "$FILE_PATH" 2>/dev/null || true
        ;;
    *.py)
        black "$FILE_PATH" 2>/dev/null || true
        ;;
    *.go)
        gofmt -w "$FILE_PATH" 2>/dev/null || true
        ;;
esac

exit 0
```

#### 3. File Protection (PreToolUse)

**Settings JSON:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.py"
          }
        ]
      }
    ]
  }
}
```

**Script: `.claude/hooks/protect-files.py`**
```python
#!/usr/bin/env python3
import json
import sys
import os

# Blocked paths
BLOCKED_PATTERNS = [
    '.env',
    '.env.local',
    '.env.production',
    'package-lock.json',
    'yarn.lock',
    '.git/',
    'node_modules/',
    'secrets/',
    'credentials.json'
]

try:
    data = json.load(sys.stdin)
    file_path = data.get('tool_input', {}).get('file_path', '')

    # Check if path contains blocked pattern
    for pattern in BLOCKED_PATTERNS:
        if pattern in file_path:
            print(f"❌ Blocked: Cannot modify {pattern}", file=sys.stderr)
            print(f"File '{file_path}' matches protected pattern '{pattern}'", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks the tool

    # Allow the operation
    sys.exit(0)

except Exception as e:
    print(f"Error in protection hook: {e}", file=sys.stderr)
    sys.exit(1)  # Non-blocking error
```

#### 4. Desktop Notifications (Notification)

**macOS:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs permission\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Linux:**
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting input'"
          }
        ]
      }
    ]
  }
}
```

#### 5. Session Context Injection (SessionStart)

**Settings JSON:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-context.sh"
          }
        ]
      }
    ]
  }
}
```

**Script: `.claude/hooks/session-context.sh`**
```bash
#!/bin/bash
set -euo pipefail

# Output context that Claude should know
cat <<EOF
# Session Context

## Environment
- Branch: $(git branch --show-current 2>/dev/null || echo "unknown")
- Uncommitted changes: $(git status --short | wc -l)
- Node version: $(node --version 2>/dev/null || echo "not installed")

## Recent Activity
$(git log --oneline -5 2>/dev/null || echo "No git history")

## Open Issues
$(gh issue list --limit 5 2>/dev/null || echo "No GitHub CLI or issues")

## TODOs in Code
$(grep -r "TODO" src/ 2>/dev/null | head -5 || echo "No TODOs found")
EOF

exit 0
```

#### 6. Persist Environment Variables (SessionStart)

**Script:**
```bash
#!/bin/bash

# Save current env
ENV_BEFORE=$(export -p | sort)

# Setup environment
source ~/.nvm/nvm.sh
nvm use 20
export API_URL="https://api.example.com"
export DEBUG=true

# Persist all changes
if [ -n "$CLAUDE_ENV_FILE" ]; then
    ENV_AFTER=$(export -p | sort)
    comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

#### 7. Command Validation (PreToolUse)

**Script: `.claude/hooks/validate-commands.py`**
```python
#!/usr/bin/env python3
import json
import sys
import re

# Validation rules
VALIDATION_RULES = [
    (r"\bgrep\b(?!.*\|)", "Use 'rg' instead of 'grep' for better performance"),
    (r"\bfind\s+\S+\s+-name\b", "Use 'rg --files -g pattern' instead of 'find -name'"),
    (r"rm\s+-rf\s+/", "DANGER: Do not rm -rf root paths"),
]

try:
    data = json.load(sys.stdin)
    tool_name = data.get('tool_name', '')
    command = data.get('tool_input', {}).get('command', '')

    if tool_name != 'Bash' or not command:
        sys.exit(0)

    # Validate
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)

    if issues:
        for msg in issues:
            print(f"• {msg}", file=sys.stderr)
        sys.exit(2)  # Block command

    sys.exit(0)

except Exception as e:
    print(f"Validation error: {e}", file=sys.stderr)
    sys.exit(1)
```

### Hook Input/Output

**Input via stdin (JSON):**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/dir",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

**Output via exit codes:**
- **0**: Success (stdout shown to user in transcript mode)
- **2**: Blocking error (stderr shown to Claude, blocks action)
- **Other**: Non-blocking error (stderr shown to user)

**Advanced JSON output:**
```json
{
  "continue": true,
  "stopReason": "optional stop message",
  "suppressOutput": false,
  "systemMessage": "optional warning to user",
  "decision": "block",
  "reason": "why blocked",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "reason"
  }
}
```

### Environment Variables

Available in hook commands:
- `$CLAUDE_PROJECT_DIR`: Absolute path to project root
- `$CLAUDE_ENV_FILE`: File for persisting env vars (SessionStart only)
- `$CLAUDE_CODE_REMOTE`: "true" if remote/web, empty if local CLI

### Prompt-Based Hooks (LLM Evaluation)

For intelligent, context-aware decisions:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

LLM response format:
```json
{
  "decision": "approve",  // or "block"
  "reason": "explanation"
}
```

### Hook Management via CLI

```bash
# Open hooks interface
/hooks

# In interface:
# - Select event (PreToolUse, PostToolUse, etc.)
# - Add matcher (Bash, Edit, Write, etc.)
# - Add hook command
# - Choose storage location (user/project)
```

### Best Practices

1. **Validate inputs**: Always quote shell variables (`"$VAR"`)
2. **Block path traversal**: Check for `..` in paths
3. **Use absolute paths**: Use `$CLAUDE_PROJECT_DIR`
4. **Skip sensitive files**: Avoid `.env`, `.git/`, keys
5. **Test in isolation**: Test hooks manually first
6. **Handle errors gracefully**: Don't crash on unexpected input
7. **Use appropriate exit codes**: 0=success, 2=block, other=warning
8. **Keep hooks fast**: Use timeouts, optimize scripts
9. **Log for debugging**: Use `claude --debug` to inspect execution

### Security Considerations

⚠️ **WARNING**: Hooks execute arbitrary shell commands automatically.

- Test hooks in safe environment first
- Review any hook code before adding
- Never trust input data blindly
- Hooks can modify/delete any accessible files
- Use at your own risk

### Debugging Hooks

```bash
# Run with debug output
claude --debug

# Check hook execution
# Look for:
# [DEBUG] Executing hooks for EventName:ToolName
# [DEBUG] Hook command completed with status X

# View transcript (Ctrl-R) for hook progress
# Check ~/.claude/settings.json for config
```

---

## 5. Workflow Integration

### Complete Workflow Example

A typical workflow combining all components:

**1. Project Setup**

```bash
# Project structure
mkdir -p .claude/{agents,commands,skills,hooks}

# Version control
cat > .gitignore << 'EOF'
.claude/settings.local.json
.claude/.cache/
EOF
```

**2. Agents for Team**

```bash
# Code reviewer
cat > .claude/agents/reviewer.md << 'EOF'
---
name: code-reviewer
description: PROACTIVE code review after changes
tools: Read, Grep, Bash
---
[reviewer prompt]
EOF

# Test runner
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: PROACTIVELY run and fix tests
tools: Read, Edit, Bash
---
[test runner prompt]
EOF
```

**3. Commands for Productivity**

```bash
# Commit
cat > .claude/commands/commit.md << 'EOF'
---
allowed-tools: Bash(git:*)
description: Smart git commit
---
[commit logic]
EOF

# PR
cat > .claude/commands/pr.md << 'EOF'
---
allowed-tools: Bash(gh:*), Bash(git:*)
description: Create detailed PR
---
[pr logic]
EOF
```

**4. Skills for Specialization**

```bash
# PDF processing skill
mkdir -p .claude/skills/pdf-processing
cat > .claude/skills/pdf-processing/SKILL.md << 'EOF'
---
name: pdf-processing
description: PDF operations - extract, merge, fill
---
[skill instructions]
EOF
```

**5. Hooks for Quality**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh"
          },
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect.py"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/context.sh"
          }
        ]
      }
    ]
  }
}
```

### Team Sharing

**Via Git (Project-level):**

```bash
# Commit configuration
git add .claude/
git commit -m "feat: add Claude Code workflow configuration"
git push

# Team automatically gets:
# - Agents in .claude/agents/
# - Commands in .claude/commands/
# - Skills in .claude/skills/
# - Hooks config in .claude/settings.json
```

**Via Plugin (Reusable across projects):**

1. Create plugin structure
2. Add to marketplace
3. Team installs plugin
4. Automatically available in all projects

See `docs/claude-code/plugins.md` and `docs/claude-code/plugins-reference.md` for complete plugin development guide.

---

## 6. Tips & Best Practices

### Agent Development

1. **Start with Claude-generated**: Use `/agents` and let Claude draft
2. **Iterate**: Test and refine based on usage
3. **Focused responsibility**: One task per agent
4. **Rich prompts**: Detailed instructions and examples
5. **Tool restrictions**: Only what's needed
6. **Proactive triggers**: Include "PROACTIVELY" in description

### Command Design

1. **Frequent tasks**: Commands for repeatable actions
2. **Clear purpose**: One clear goal per command
3. **Good defaults**: Work without arguments where possible
4. **Flexible**: Support arguments for variation
5. **Context aware**: Use !`command` for runtime data

### Skill Authoring

1. **Discovery keywords**: Include in description what users would say
2. **Progressive detail**: Main SKILL.md concise, link to details
3. **Document deps**: List required packages
4. **Examples**: Concrete examples in skill
5. **Test discovery**: Verify Claude activates skill as expected

### Hook Development

1. **Test locally first**: Run command manually
2. **Handle errors**: Graceful failures
3. **Fast execution**: Keep under 5 seconds ideally
4. **Quote variables**: Always `"$VAR"`
5. **Validate input**: Never trust blindly
6. **Use exit codes**: 0=success, 2=block, other=warning
7. **Debug mode**: Test with `claude --debug`

### Performance

1. **Agent context**: Agents have their own context window (good)
2. **Skill loading**: Progressive disclosure (load on demand)
3. **Hook timeouts**: Set appropriate timeouts (default 60s)
4. **Command caching**: Commands cached per session

### Security

1. **Review all code**: Before adding to config
2. **Principle of least privilege**: Minimal tool access
3. **Protect sensitive files**: Use hooks to block
4. **Audit logs**: Track what Claude does
5. **Test in isolation**: Safe environment first

---

## 7. Troubleshooting

### Agent Not Being Used

**Diagnose:**
```bash
/agents  # Check if agent is listed
claude --debug  # See agent selection logic
```

**Fix:**
- Description too vague → Add specific keywords
- Wrong priority → Project agents override user agents
- Tool mismatch → Verify agent has necessary tools

### Command Not Working

**Diagnose:**
```bash
/help  # Check if command is listed
cat .claude/commands/my-cmd.md  # Verify syntax
```

**Fix:**
- Invalid frontmatter → Fix YAML syntax
- File permissions → `chmod +x` for scripts
- Wrong location → Check `.claude/commands/` vs `~/.claude/commands/`

### Skill Not Activated

**Diagnose:**
```bash
claude --debug  # See skill loading
ls .claude/skills/*/SKILL.md  # Verify exists
```

**Fix:**
- Description too generic → Add specific triggers
- YAML syntax error → Validate frontmatter
- Wrong file name → Must be `SKILL.md` (case sensitive)

### Hook Fails

**Diagnose:**
```bash
claude --debug  # See hook execution
# Test command manually:
echo '{"tool_name":"Write","tool_input":{"file_path":"test.txt"}}' | .claude/hooks/my-hook.sh
```

**Fix:**
- Command not found → Use absolute paths or `$CLAUDE_PROJECT_DIR`
- Timeout → Increase timeout in config
- Exit code → Check 0=success, 2=block
- Permissions → `chmod +x .claude/hooks/*`

---

## 8. References

### Documentation

**Core Components:**
- `docs/claude-code/sub-agents.md` - Complete agent guide
- `docs/claude-code/slash-commands.md` - Command reference
- `docs/claude-code/skills.md` - Skill authoring
- `docs/claude-code/hooks.md` - Hook reference
- `docs/claude-code/hooks-guide.md` - Hook quickstart

**Plugins & Extensions:**
- `docs/claude-code/plugins.md` - Plugin development guide
- `docs/claude-code/plugins-reference.md` - Plugin API reference
- `docs/claude-code/mcp.md` - Model Context Protocol integration

**Workflows & Usage:**
- `docs/claude-code/common-workflows.md` - Workflow examples
- `docs/claude-code/interactive-mode.md` - Interactive mode guide
- `docs/claude-code/headless.md` - Headless mode and automation
- `docs/claude-code/claude-code-on-the-web.md` - Web version guide

**CLI & Configuration:**
- `docs/claude-code/cli-reference.md` - CLI flags and options
- `docs/claude-code/checkpointing.md` - Session checkpointing
- `docs/claude-code/output-styles.md` - Output formatting options
- `docs/claude-code/memory.md` - Memory management

### CLI Commands

```bash
# Management
/agents          # Manage agents
/hooks           # Manage hooks
/help            # List commands
/status          # System status

# Usage
claude           # Start interactive
claude -p "q"    # Headless query
claude --debug   # Debug mode
claude --agents '{}' # Dynamic agents
```

> **Mode Guides**: See `docs/claude-code/interactive-mode.md` for interactive sessions and `docs/claude-code/headless.md` for automation.
> **Full Reference**: See `docs/claude-code/cli-reference.md` for all CLI options.

### Useful Patterns

```bash
# Check config
cat ~/.claude/settings.json
cat .claude/settings.json

# Test hook manually
echo '{}' | .claude/hooks/test.sh

# View logs
claude --debug

# Update Claude
claude update
```

---

## 9. Quick Reference

### File Locations

```
~/.claude/
├── settings.json         # User configuration
├── agents/              # User agents (all projects)
├── commands/            # User commands (all projects)
└── skills/              # User skills (all projects)

.claude/
├── settings.json        # Project configuration
├── settings.local.json  # Local overrides (gitignored)
├── agents/              # Project agents (team shared)
├── commands/            # Project commands (team shared)
├── skills/              # Project skills (team shared)
└── hooks/               # Hook scripts
```

### Priority Order

1. **Agents**: CLI → Project → User → Plugin
2. **Commands**: Project → User → Plugin
3. **Skills**: Project → Personal → Plugin
4. **Settings**: Local → Project → User → Enterprise

### Quick Commands

```bash
# Setup
mkdir -p .claude/{agents,commands,skills,hooks}

# Create agent
cat > .claude/agents/name.md

# Create command
cat > .claude/commands/name.md

# Create skill
mkdir .claude/skills/name
cat > .claude/skills/name/SKILL.md

# Configure hooks
code .claude/settings.json

# Test
claude --debug
```

---

## Conclusion

This implementation guide provides everything needed to build production-ready Claude Code components for the Melly marketplace. Use this guide to:

1. **Implement Agents** - Specialized AI assistants for contextual knowledge retrieval
2. **Create Commands** - Reusable prompts that leverage the knowledge base
3. **Develop Skills** - Extensible capabilities for intelligent information extraction
4. **Configure Hooks** - Automation and quality control for production workflows

By following this guide, you'll create a production-ready marketplace of Claude Code components that enable powerful contextual retrieval from your knowledge base.

For questions or updates, refer to the docs folder or the official Claude Code documentation.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Maintainer**: Melly Team
