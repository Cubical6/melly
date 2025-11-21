#!/usr/bin/env python3
"""
Validate Content Preservation

Compares original and enhanced documentation files to ensure that:
1. 100% of original content is preserved
2. Only metadata section is added at the beginning
3. No content is modified, removed, or corrupted

Outputs validation results in JSON format.
"""

import sys
import json
import re
from pathlib import Path
from difflib import unified_diff


def extract_metadata_section(content):
    """
    Extract the metadata section from enhanced content.

    Args:
        content (str): File content

    Returns:
        tuple: (metadata_section, content_after_metadata)
    """
    # Look for metadata section patterns
    patterns = [
        # YAML front matter followed by metadata section and separator
        # Pattern: ---\nYAML\n---\n\n## Metadata\n...\n---\n\n
        (r'^---\n.*?\n---\n+.*?\n---\n+', re.DOTALL),
        # YAML front matter only
        (r'^---\n(.*?)\n---\n', re.DOTALL),
        # HTML comment metadata
        (r'^<!--\s*METADATA\s*\n(.*?)\n-->\n', re.DOTALL),
        # JSON metadata block
        (r'^```json\n(.*?)\n```\n', re.DOTALL),
    ]

    for pattern, flags in patterns:
        match = re.match(pattern, content, flags)
        if match:
            metadata = match.group(0)
            content_after = content[len(metadata):]
            return metadata, content_after

    # No metadata section found
    return None, content


def normalize_content(content):
    """
    Normalize content for comparison.

    Args:
        content (str): File content

    Returns:
        str: Normalized content
    """
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Remove trailing whitespace from each line
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]

    # Remove trailing empty lines
    while lines and lines[-1] == '':
        lines.pop()

    return '\n'.join(lines)


def compare_content(original, enhanced):
    """
    Compare original and enhanced content.

    Args:
        original (str): Original file content
        enhanced (str): Enhanced file content

    Returns:
        dict: Comparison results
    """
    # Extract metadata section from enhanced content
    metadata_section, content_after_metadata = extract_metadata_section(enhanced)

    # Normalize both contents
    original_normalized = normalize_content(original)
    enhanced_normalized = normalize_content(content_after_metadata)

    # Check if content matches
    content_matches = original_normalized == enhanced_normalized

    # Calculate similarity metrics
    original_lines = original_normalized.split('\n')
    enhanced_lines = enhanced_normalized.split('\n')

    # Generate diff if content doesn't match
    diff = None
    if not content_matches:
        diff_lines = list(unified_diff(
            original_lines,
            enhanced_lines,
            fromfile='original',
            tofile='enhanced',
            lineterm=''
        ))
        diff = '\n'.join(diff_lines)

    return {
        'has_metadata_section': metadata_section is not None,
        'metadata_section_length': len(metadata_section) if metadata_section else 0,
        'content_matches': content_matches,
        'original_line_count': len(original_lines),
        'enhanced_line_count': len(enhanced_lines),
        'original_char_count': len(original_normalized),
        'enhanced_char_count': len(enhanced_normalized),
        'diff': diff
    }


def validate_files(original_path, enhanced_path):
    """
    Validate that enhanced file preserves original content.

    Args:
        original_path (Path): Path to original file
        enhanced_path (Path): Path to enhanced file

    Returns:
        dict: Validation results
    """
    # Read files
    try:
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return {
            'success': False,
            'error': f"Failed to read original file: {e}",
            'original_path': str(original_path),
            'enhanced_path': str(enhanced_path)
        }

    try:
        with open(enhanced_path, 'r', encoding='utf-8') as f:
            enhanced_content = f.read()
    except Exception as e:
        return {
            'success': False,
            'error': f"Failed to read enhanced file: {e}",
            'original_path': str(original_path),
            'enhanced_path': str(enhanced_path)
        }

    # Compare content
    comparison = compare_content(original_content, enhanced_content)

    # Determine validation success
    success = comparison['content_matches']

    result = {
        'success': success,
        'original_path': str(original_path.absolute()),
        'enhanced_path': str(enhanced_path.absolute()),
        'validation': {
            'content_preserved': comparison['content_matches'],
            'has_metadata': comparison['has_metadata_section'],
            'metadata_bytes': comparison['metadata_section_length']
        },
        'metrics': {
            'original_lines': comparison['original_line_count'],
            'enhanced_lines': comparison['enhanced_line_count'],
            'original_chars': comparison['original_char_count'],
            'enhanced_chars': comparison['enhanced_char_count']
        }
    }

    # Add diff if validation failed
    if not success and comparison['diff']:
        result['diff'] = comparison['diff']
        result['error'] = 'Content does not match after metadata section'

    return result


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 3:
        print("Usage: python validate-content.py <original_path> <enhanced_path>",
              file=sys.stderr)
        sys.exit(1)

    original_path = Path(sys.argv[1])
    enhanced_path = Path(sys.argv[2])

    # Validate files exist
    if not original_path.exists():
        print(json.dumps({
            'success': False,
            'error': f'Original file not found: {original_path}'
        }, indent=2))
        sys.exit(1)

    if not enhanced_path.exists():
        print(json.dumps({
            'success': False,
            'error': f'Enhanced file not found: {enhanced_path}'
        }, indent=2))
        sys.exit(1)

    try:
        # Validate files
        result = validate_files(original_path, enhanced_path)

        # Output JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # Exit with appropriate code
        sys.exit(0 if result['success'] else 1)

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': f'Unexpected error: {e}'
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
