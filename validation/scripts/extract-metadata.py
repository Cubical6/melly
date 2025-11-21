#!/usr/bin/env python3
"""
Extract Semantic Metadata from Documentation

Analyzes markdown documentation to extract:
- Observations (key concepts, patterns, features)
- Relations (cross-references, dependencies)
- Tags (categorization)

Outputs structured JSON metadata for library documentation.
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict


def extract_observations(content, library_name):
    """
    Extract observations from markdown content.

    Args:
        content (str): Markdown file content
        library_name (str): Name of the library

    Returns:
        list: List of observation strings
    """
    observations = []
    lines = content.split('\n')

    # Extract key phrases and patterns
    patterns = {
        'feature': r'(?:provides?|supports?|enables?|allows?|offers?)\s+(.{10,100})',
        'requirement': r'(?:requires?|needs?|must|should)\s+(.{10,100})',
        'capability': r'(?:can|able to|capable of)\s+(.{10,100})',
        'usage': r'(?:used for|use case|example|usage)\s*:?\s*(.{10,100})',
    }

    for line in lines:
        # Skip code blocks, headings, and empty lines
        if line.strip().startswith(('```', '#', '')) or len(line.strip()) < 10:
            continue

        for pattern_type, pattern in patterns.items():
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                observation = match.group(1).strip().rstrip('.,;:')
                if len(observation) > 15:  # Meaningful observations only
                    observations.append(observation)

    # Extract from list items (often contain key information)
    list_pattern = r'^\s*[-*+]\s+(.+)$'
    for line in lines:
        match = re.match(list_pattern, line)
        if match:
            item = match.group(1).strip()
            if len(item) > 15 and not item.startswith('['):
                observations.append(item)

    # Deduplicate while preserving order
    seen = set()
    unique_observations = []
    for obs in observations:
        obs_lower = obs.lower()
        if obs_lower not in seen:
            seen.add(obs_lower)
            unique_observations.append(obs)

    return unique_observations[:50]  # Limit to top 50 observations


def extract_relations(content, library_name):
    """
    Extract relations and cross-references from content.

    Args:
        content (str): Markdown file content
        library_name (str): Name of the library

    Returns:
        list: List of relation objects
    """
    relations = []

    # Extract markdown links to other documentation files
    link_pattern = r'\[([^\]]+)\]\(([^\)]+\.md(?:#[^\)]+)?)\)'
    for match in re.finditer(link_pattern, content):
        link_text = match.group(1)
        link_url = match.group(2)

        # Parse anchor if present
        parts = link_url.split('#')
        target_file = parts[0]
        anchor = parts[1] if len(parts) > 1 else None

        relations.append({
            'type': 'references',
            'target': target_file,
            'context': link_text,
            'anchor': anchor
        })

    # Extract code references (common patterns)
    code_ref_patterns = [
        r'`([A-Z][a-zA-Z]+(?:\.[a-zA-Z]+)+)`',  # Class/module references
        r'`([a-z_]+\([^)]*\))`',  # Function calls
    ]

    for pattern in code_ref_patterns:
        for match in re.finditer(pattern, content):
            code_ref = match.group(1)
            relations.append({
                'type': 'code_reference',
                'target': code_ref,
                'context': None,
                'anchor': None
            })

    # Extract "see also" style references
    see_also_pattern = r'(?:see also|refer to|check|see)\s+\[([^\]]+)\]\(([^\)]+)\)'
    for match in re.finditer(see_also_pattern, content, re.IGNORECASE):
        relations.append({
            'type': 'see_also',
            'target': match.group(2),
            'context': match.group(1),
            'anchor': None
        })

    return relations


def extract_tags(content, file_path, library_name):
    """
    Extract categorization tags from content and file structure.

    Args:
        content (str): Markdown file content
        file_path (Path): Path to the file
        library_name (str): Name of the library

    Returns:
        list: List of tag strings
    """
    tags = [library_name]

    # Tags from file path
    path_parts = file_path.parts
    for part in path_parts:
        if part.lower() not in ['docs', 'documentation', '.', '..']:
            clean_part = re.sub(r'[^a-zA-Z0-9-]', '', part)
            if clean_part:
                tags.append(clean_part.lower())

    # Tags from headings
    heading_pattern = r'^#{1,6}\s+(.+)$'
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        heading = match.group(1).strip()
        # Extract key words from headings
        words = re.findall(r'\b[A-Z][a-z]+\b', heading)
        tags.extend([w.lower() for w in words if len(w) > 3])

    # Common documentation categories
    category_keywords = {
        'api': ['api', 'endpoint', 'method', 'route'],
        'tutorial': ['tutorial', 'guide', 'getting started', 'quickstart'],
        'reference': ['reference', 'documentation', 'specification'],
        'configuration': ['config', 'configuration', 'settings', 'options'],
        'authentication': ['auth', 'authentication', 'authorization', 'login'],
        'database': ['database', 'db', 'query', 'model', 'schema'],
        'testing': ['test', 'testing', 'unit test', 'integration test'],
        'deployment': ['deploy', 'deployment', 'production', 'hosting'],
    }

    content_lower = content.lower()
    for category, keywords in category_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            tags.append(category)

    # Deduplicate and sort
    tags = sorted(list(set(tags)))

    return tags


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 3:
        print("Usage: python extract-metadata.py <file_path> <library_name>",
              file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])
    library_name = sys.argv[2]

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

        # Extract metadata
        observations = extract_observations(content, library_name)
        relations = extract_relations(content, library_name)
        tags = extract_tags(content, file_path, library_name)

        # Build result
        result = {
            'file_path': str(file_path.absolute()),
            'file_name': file_path.name,
            'library_name': library_name,
            'observations': observations,
            'relations': relations,
            'tags': tags
        }

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
