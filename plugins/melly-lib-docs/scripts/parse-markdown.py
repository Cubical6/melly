#!/usr/bin/env python3
"""
Universal Markdown Structure Parser

Extracts structured information from markdown files including headings,
code blocks, links, lists, and blockquotes.

Usage:
    python parse-markdown.py <markdown-file>
    python parse-markdown.py --help

Example:
    python parse-markdown.py docs/laravel/eloquent.md
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def parse_markdown_structure(content: str) -> Dict:
    """
    Extract headings, code blocks, links, lists, blockquotes from markdown.
    
    Args:
        content: Raw markdown content as string
        
    Returns:
        Dictionary with structured markdown elements:
        - headings: List of {'level': int, 'text': str}
        - code_blocks: List of {'language': str, 'code': str}
        - links: List of {'text': str, 'url': str}
        - inline_code: List of unique inline code snippets
        - lists: List of list items
        - blockquotes: List of blockquote content
        - raw_content: Original markdown content
    """
    result = {
        'headings': [],
        'code_blocks': [],
        'links': [],
        'inline_code': [],
        'lists': [],
        'blockquotes': [],
        'raw_content': content
    }
    
    # Extract headings (# to ######)
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2).strip()
        result['headings'].append({'level': level, 'text': text})
    
    # Extract code blocks (```language...```)
    code_block_pattern = r'```(\w*)\n(.*?)```'
    for match in re.finditer(code_block_pattern, content, re.DOTALL):
        language = match.group(1) or 'text'
        code = match.group(2).strip()
        result['code_blocks'].append({'language': language, 'code': code})
    
    # Extract markdown links [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(link_pattern, content):
        text = match.group(1).strip()
        url = match.group(2).strip()
        result['links'].append({'text': text, 'url': url})
    
    # Extract inline code `code`
    inline_code_pattern = r'`([^`]+)`'
    inline_code_matches = re.findall(inline_code_pattern, content)
    result['inline_code'] = list(set(inline_code_matches))  # Unique values
    
    # Extract list items (- or * or numbered)
    list_pattern = r'^[\s]*[-*]\s+(.+)$|^[\s]*\d+\.\s+(.+)$'
    for match in re.finditer(list_pattern, content, re.MULTILINE):
        item = match.group(1) or match.group(2)
        if item:
            result['lists'].append(item.strip())
    
    # Extract blockquotes (> quote)
    blockquote_pattern = r'^>\s+(.+)$'
    for match in re.finditer(blockquote_pattern, content, re.MULTILINE):
        result['blockquotes'].append(match.group(1).strip())
    
    return result


def parse_file(file_path: Path) -> Optional[Dict]:
    """
    Parse markdown file and return structured data.
    
    Args:
        file_path: Path to markdown file
        
    Returns:
        Parsed structure dictionary or None if error
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        return parse_markdown_structure(content)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Parse markdown file structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'markdown_file',
        type=Path,
        help='Path to markdown file to parse'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed output'
    )
    
    args = parser.parse_args()
    
    if not args.markdown_file.exists():
        print(f"Error: File not found: {args.markdown_file}", file=sys.stderr)
        return 2
    
    if not args.markdown_file.is_file():
        print(f"Error: Not a file: {args.markdown_file}", file=sys.stderr)
        return 2
    
    parsed = parse_file(args.markdown_file)
    if parsed is None:
        return 2
    
    # Print summary
    print(f"Parsed: {args.markdown_file}")
    print(f"  Headings: {len(parsed['headings'])}")
    print(f"  Code blocks: {len(parsed['code_blocks'])}")
    print(f"  Links: {len(parsed['links'])}")
    print(f"  Inline code: {len(parsed['inline_code'])}")
    print(f"  List items: {len(parsed['lists'])}")
    print(f"  Blockquotes: {len(parsed['blockquotes'])}")
    
    if args.verbose:
        print("\nHeadings:")
        for h in parsed['headings']:
            print(f"  {'#' * h['level']} {h['text']}")
        
        if parsed['code_blocks']:
            print(f"\nCode blocks ({len(parsed['code_blocks'])}):")
            for i, cb in enumerate(parsed['code_blocks'][:5], 1):
                print(f"  {i}. Language: {cb['language']}, Lines: {len(cb['code'].splitlines())}")
        
        if parsed['links']:
            print(f"\nLinks ({len(parsed['links'])}):")
            for link in parsed['links'][:10]:
                print(f"  [{link['text']}]({link['url']})")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
