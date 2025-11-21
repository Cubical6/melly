#!/usr/bin/env python3
"""
Parse Markdown Files

Extracts structural elements from markdown files including:
- Headings (H1-H6)
- Code blocks (fenced and indented)
- Internal links

Outputs JSON format for further processing.
"""

import sys
import json
import re
from pathlib import Path


def parse_markdown(content):
    """
    Parse markdown content and extract structural elements.

    Args:
        content (str): Markdown file content

    Returns:
        dict: Structured data with title, headings, code_blocks, and links
    """
    lines = content.split('\n')

    headings = []
    code_blocks = []
    links = []
    title = None

    in_code_block = False
    current_code_block = []
    code_language = None

    for i, line in enumerate(lines):
        # Parse fenced code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block
                code_blocks.append({
                    'language': code_language,
                    'content': '\n'.join(current_code_block),
                    'line': i - len(current_code_block)
                })
                current_code_block = []
                code_language = None
                in_code_block = False
            else:
                # Start of code block
                in_code_block = True
                code_language = line.strip()[3:].strip() or 'plain'
            continue

        if in_code_block:
            current_code_block.append(line)
            continue

        # Parse headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()

            heading_data = {
                'level': level,
                'text': text,
                'line': i + 1
            }

            headings.append(heading_data)

            # First H1 is the title
            if level == 1 and title is None:
                title = text

        # Parse markdown links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        for match in re.finditer(link_pattern, line):
            link_text = match.group(1)
            link_url = match.group(2)

            # Only include internal links (relative paths, anchors)
            if not link_url.startswith(('http://', 'https://', 'mailto:')):
                links.append({
                    'text': link_text,
                    'url': link_url,
                    'line': i + 1
                })

    return {
        'title': title,
        'headings': headings,
        'code_blocks': code_blocks,
        'links': links
    }


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python parse-markdown.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])

    # Validate file exists
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Validate file is markdown
    if file_path.suffix.lower() not in ['.md', '.markdown']:
        print(f"Warning: File does not have .md or .markdown extension: {file_path}",
              file=sys.stderr)

    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse markdown
        result = parse_markdown(content)

        # Add metadata
        result['file_path'] = str(file_path.absolute())
        result['file_name'] = file_path.name

        # Output JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except UnicodeDecodeError as e:
        print(f"Error: Unable to decode file as UTF-8: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
