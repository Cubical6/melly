#!/usr/bin/env python3
"""
Validate Content Preservation

Verifies that original markdown content is 100% preserved in enhanced files.
Enhanced files have metadata frontmatter followed by "---" separator and
the original content.

Usage:
    python validate-content.py <original-file> <enhanced-file>
    python validate-content.py --help

Example:
    python validate-content.py docs/original/eloquent.md knowledge-base/libraries/laravel/eloquent.md

Exit codes:
    0 - Content preserved correctly
    1 - Warning (minor whitespace differences)
    2 - Error (content mismatch)
"""

import argparse
import difflib
import sys
from pathlib import Path
from typing import Tuple, Optional


def normalize_whitespace(text: str, strict: bool = False) -> str:
    """
    Normalize whitespace for comparison.
    
    Args:
        text: Input text
        strict: If True, only normalize line endings. If False, also strip trailing spaces.
        
    Returns:
        Normalized text
    """
    # Normalize line endings to \n
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    if not strict:
        # Remove trailing whitespace from each line
        lines = text.split('\n')
        lines = [line.rstrip() for line in lines]
        text = '\n'.join(lines)
    
    # Ensure single trailing newline
    text = text.rstrip('\n') + '\n'
    
    return text


def strip_all_whitespace(text: str) -> str:
    """
    Strip all whitespace characters for comparison.
    
    Used to detect if content is identical except for whitespace differences.
    
    Args:
        text: Input text
        
    Returns:
        Text with all whitespace removed
    """
    return text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')


def extract_original_from_enhanced(enhanced_content: str) -> Optional[str]:
    """
    Extract original content from enhanced file.
    
    Enhanced files have structure:
    ---
    metadata...
    ---
    
    Original content here...
    
    Args:
        enhanced_content: Content of enhanced file
        
    Returns:
        Original content or None if not found
    """
    # Find the second --- separator (end of frontmatter)
    parts = enhanced_content.split('\n---\n', 2)
    
    if len(parts) < 3:
        # No frontmatter found, might be original content only
        return enhanced_content
    
    # parts[0] should be empty or start with ---
    # parts[1] is the frontmatter
    # parts[2] is the original content
    
    original = parts[2]
    
    # Remove leading blank line if present
    if original.startswith('\n'):
        original = original[1:]
    
    return original


def validate_content_preservation(
    original_file: Path,
    enhanced_file: Path,
    strict: bool = False
) -> Tuple[bool, str]:
    """
    Verify original content is 100% preserved in enhanced file.
    
    Steps:
    1. Read both files
    2. Extract original from enhanced (content after "---" separator)
    3. Normalize whitespace
    4. Compare byte-for-byte
    5. Print diff if mismatch
    
    Args:
        original_file: Path to original markdown file
        enhanced_file: Path to enhanced markdown file
        strict: If True, require exact match including whitespace
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Read files
        original_content = original_file.read_text(encoding='utf-8')
        enhanced_content = enhanced_file.read_text(encoding='utf-8')
        
    except Exception as e:
        return False, f"Error reading files: {e}"
    
    # Extract original from enhanced
    extracted = extract_original_from_enhanced(enhanced_content)
    if extracted is None:
        return False, "Could not extract original content from enhanced file"
    
    # Normalize
    original_normalized = normalize_whitespace(original_content, strict=strict)
    extracted_normalized = normalize_whitespace(extracted, strict=strict)
    
    # Compare
    if original_normalized == extracted_normalized:
        return True, "Content preserved correctly"
    
    # Content mismatch - generate diff
    original_lines = original_normalized.splitlines(keepends=True)
    extracted_lines = extracted_normalized.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        extracted_lines,
        fromfile=str(original_file),
        tofile=str(enhanced_file),
        lineterm=''
    )
    
    diff_text = ''.join(diff)
    
    # Check if only whitespace differences
    if strip_all_whitespace(original_content) == strip_all_whitespace(extracted):
        return True, f"Content preserved (minor whitespace differences):\n{diff_text}"
    
    return False, f"Content mismatch detected:\n{diff_text}"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Validate content preservation in enhanced files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'original_file',
        type=Path,
        help='Path to original markdown file'
    )
    parser.add_argument(
        'enhanced_file',
        type=Path,
        help='Path to enhanced markdown file'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Require exact match including all whitespace'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed output'
    )
    
    args = parser.parse_args()
    
    # Validate files exist
    if not args.original_file.exists():
        print(f"Error: Original file not found: {args.original_file}", file=sys.stderr)
        return 2
    
    if not args.enhanced_file.exists():
        print(f"Error: Enhanced file not found: {args.enhanced_file}", file=sys.stderr)
        return 2
    
    # Validate content
    success, message = validate_content_preservation(
        args.original_file,
        args.enhanced_file,
        strict=args.strict
    )
    
    if success:
        print(f"✓ {message}")
        if args.verbose:
            print(f"  Original: {args.original_file}")
            print(f"  Enhanced: {args.enhanced_file}")
        return 0
    else:
        print("✗ Content validation failed", file=sys.stderr)
        print(f"  {message}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
