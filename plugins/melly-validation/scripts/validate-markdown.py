#!/usr/bin/env python3
"""
Validate markdown documentation files.

Exit codes:
  0 - Validation passed
  1 - Non-blocking warning (continue with user notification)
  2 - Blocking error (halt workflow immediately)
"""

import sys
import os
import re
import glob
from typing import List, Tuple, Dict


def error(message: str, location: str = "") -> None:
    """Print formatted error message to stderr."""
    print(f"[VALIDATE-MD] ERROR: {message}", file=sys.stderr)
    if location:
        print(f"  File: {location}", file=sys.stderr)
    print("", file=sys.stderr)


def warning(message: str, recommendation: str = "") -> None:
    """Print formatted warning message to stderr."""
    print(f"[VALIDATE-MD] WARNING: {message}", file=sys.stderr)
    if recommendation:
        print(f"  Recommendation: {recommendation}", file=sys.stderr)
    print("", file=sys.stderr)


def validate_frontmatter(content: str, file_path: str) -> Tuple[bool, List[str], List[str], Dict[str, str]]:
    """Validate YAML frontmatter."""
    errors = []
    warnings = []
    frontmatter = {}

    # Check if starts with ---
    if not content.startswith("---"):
        errors.append(f"{file_path}: Missing YAML frontmatter (must start with ---)")
        return False, errors, warnings, frontmatter

    # Extract frontmatter
    lines = content.split('\n')
    if len(lines) < 3:
        errors.append(f"{file_path}: Invalid frontmatter structure")
        return False, errors, warnings, frontmatter

    # Find end of frontmatter
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        errors.append(f"{file_path}: Frontmatter not properly closed (missing closing ---)")
        return False, errors, warnings, frontmatter

    # Parse frontmatter
    for i in range(1, end_idx):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    # Validate required fields
    required_fields = ["id", "title", "level", "type", "generated"]
    for field in required_fields:
        if field not in frontmatter:
            errors.append(f"{file_path}: Missing required frontmatter field: {field}")

    # Validate level
    if "level" in frontmatter:
        if frontmatter["level"] not in ["c1", "c2", "c3"]:
            errors.append(f"{file_path}: Invalid level: {frontmatter['level']} (must be c1, c2, or c3)")

    # Validate generated
    if "generated" in frontmatter:
        if frontmatter["generated"] != "auto":
            warnings.append(f"{file_path}: generated field should be 'auto' for automated generation")

    # Warn if parent missing for c2/c3
    if "level" in frontmatter and frontmatter["level"] in ["c2", "c3"]:
        if "parent" not in frontmatter and "container" not in frontmatter and "system" not in frontmatter:
            warnings.append(f"{file_path}: C{frontmatter['level'][1]} file missing parent reference")

    return len(errors) == 0, errors, warnings, frontmatter


def validate_heading_hierarchy(content: str, file_path: str) -> Tuple[bool, List[str], List[str]]:
    """Validate heading hierarchy."""
    errors = []
    warnings = []

    lines = content.split('\n')
    h1_count = 0
    h1_line = None

    # Find frontmatter boundaries
    frontmatter_end = 0
    if lines and lines[0].strip() == "---":
        # Find closing ---
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                frontmatter_end = i + 1
                break

    for i, line in enumerate(lines):
        # Skip frontmatter block
        if i < frontmatter_end:
            continue

        # Count H1
        if line.startswith("# ") and not line.startswith("##"):
            h1_count += 1
            h1_line = line

    # Check exactly one H1
    if h1_count == 0:
        errors.append(f"{file_path}: Missing H1 heading")
    elif h1_count > 1:
        errors.append(f"{file_path}: Multiple H1 headings found ({h1_count})")

    # Validate H1 pattern (optional)
    if h1_line:
        # Should contain level indicator like (C1, C2, C3)
        if not re.search(r'\(C[123]', h1_line):
            warnings.append(f"{file_path}: H1 should follow pattern: # {{name}} (C1|C2|C3 - ...)")

    return len(errors) == 0, errors, warnings


def validate_sections(content: str, level: str) -> Tuple[bool, List[str], List[str]]:
    """Validate required sections."""
    errors = []
    warnings = []

    # Required sections for all levels
    required_sections = ["Overview", "Observations", "Relations"]

    # Level-specific sections
    if level == "c2":
        required_sections.append("Technology Stack")
    elif level == "c3":
        required_sections.append("Code Structure")

    # Find sections
    found_sections = set()
    for line in content.split('\n'):
        if line.startswith("## "):
            section_name = line[3:].strip()
            found_sections.add(section_name)

    # Check required sections
    if "Overview" not in found_sections:
        errors.append("Missing required section: ## Overview")

    if "Observations" not in found_sections:
        warnings.append("Missing section: ## Observations")

    if "Relations" not in found_sections:
        warnings.append("Missing section: ## Relations")

    # Check level-specific
    if level == "c2" and "Technology Stack" not in found_sections:
        warnings.append("Missing section: ## Technology Stack (recommended for C2)")

    if level == "c3" and "Code Structure" not in found_sections:
        warnings.append("Missing section: ## Code Structure (recommended for C3)")

    return len(errors) == 0, errors, warnings


def validate_content_quality(content: str) -> Tuple[bool, List[str]]:
    """Validate content quality."""
    warnings = []

    # Check for placeholders
    placeholders = ["TODO", "TBD", "FIXME", "XXX"]
    for placeholder in placeholders:
        if placeholder in content:
            warnings.append(f"Found placeholder text: {placeholder}")

    # Check for empty code blocks
    if "```\n```" in content or "```\n\n```" in content:
        warnings.append("Found empty code block")

    # Check for broken links (basic check)
    broken_links = re.findall(r'\[([^\]]+)\]\(\)', content)
    if broken_links:
        warnings.append(f"Found {len(broken_links)} empty link(s)")

    return True, warnings


def validate_file(file_path: str) -> Tuple[int, List[str], List[str]]:
    """Validate a single markdown file."""
    errors = []
    warnings = []

    # Check file exists
    if not os.path.exists(file_path):
        return 2, [f"File not found: {file_path}"], []

    # Read file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return 2, [f"Failed to read file: {str(e)}"], []

    # 1. Validate frontmatter
    valid, errs, warns, frontmatter = validate_frontmatter(content, file_path)
    errors.extend(errs)
    warnings.extend(warns)

    if not valid:
        return 2, errors, warnings

    # 2. Validate heading hierarchy
    valid, errs, warns = validate_heading_hierarchy(content, file_path)
    errors.extend(errs)
    warnings.extend(warns)

    # 3. Validate sections
    level = frontmatter.get("level", "c1")
    valid, errs, warns = validate_sections(content, level)
    errors.extend(errs)
    warnings.extend(warns)

    # 4. Validate content quality
    valid, warns = validate_content_quality(content)
    warnings.extend(warns)

    # Determine exit code
    if errors:
        return 2, errors, warnings
    elif warnings:
        return 1, errors, warnings
    else:
        return 0, errors, warnings


def main() -> int:
    """Main validation function."""
    if len(sys.argv) < 2:
        # No arguments provided - find all generated markdown files to validate
        file_paths = list(glob.glob("knowledge-base/systems/**/*.md", recursive=True))
        if not file_paths:
            # No markdown files found - skip validation
            print("[VALIDATE-MD] No generated markdown files found - skipping validation", file=sys.stderr)
            return 0
    else:
        file_paths = sys.argv[1:]
    has_errors = False
    has_warnings = False
    total_files = len(file_paths)
    passed_files = 0

    for file_path in file_paths:
        exit_code, errors, warnings = validate_file(file_path)

        if exit_code == 2:
            has_errors = True
            for err in errors:
                error(err, location=file_path)
            for warn in warnings:
                warning(warn)
        elif exit_code == 1:
            has_warnings = True
            passed_files += 1
            for warn in warnings:
                warning(warn)
        else:
            passed_files += 1

    # Summary
    print(f"[VALIDATE-MD] Validated {total_files} file(s): {passed_files} passed", file=sys.stderr)

    if has_errors:
        print("[VALIDATE-MD] FAILED with errors", file=sys.stderr)
        return 2
    elif has_warnings:
        print("[VALIDATE-MD] PASSED with warnings", file=sys.stderr)
        return 1
    else:
        print("[VALIDATE-MD] PASSED", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
