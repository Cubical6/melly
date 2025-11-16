#!/usr/bin/env python3
"""
Extract Observations and Relations from Parsed Markdown

Extracts observations (facts, requirements, best practices, techniques,
examples, problems, solutions, insights, decisions, questions) and relations (links, cross-references) from markdown structure.

Usage:
    python extract-metadata.py <markdown-file> <library-name> <entity-id>
    python extract-metadata.py --help

Example:
    python extract-metadata.py docs/laravel/eloquent.md laravel laravel-eloquent
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse


def extract_observations(parsed: Dict, library: str) -> List[Dict]:
    """
    Extract observations using regex patterns.
    
    Patterns for:
    - fact: Version info like "Introduced in X", "Added in Y", "Requires X+"
    - requirement: Dependencies like "Requires X", "Depends on Y"
    - best-practice: "Best practice", "Recommended", "Should"
    - technique: H2/H3 headings with "How to", "Using", etc.
    - example: Code blocks
    - problem: Warnings like "Note:", "Warning:", "Caution:"
    - solution: Solutions to problems
    - insight: Blockquotes with tips, notes
    - decision: Architectural decisions
    - question: Open questions
    
    Args:
        parsed: Dictionary from parse_markdown_structure()
        library: Library name (e.g., "laravel", "react")
        
    Returns:
        List of observation dictionaries with category, content, source
    """
    observations = []
    
    # Version patterns -> fact category
    version_patterns = [
        r'(?i)introduced in ([\w\s.]+)',
        r'(?i)added in ([\w\s.]+)',
        r'(?i)requires? ([\w\s.]+\d+[\w.]*)\+?',
        r'(?i)available (?:since|from) ([\w\s.]+)',
        r'(?i)new in ([\w\s.]+)',
    ]
    
    content = parsed['raw_content']
    for pattern in version_patterns:
        for match in re.finditer(pattern, content):
            observations.append({
                'category': 'fact',
                'description': match.group(0).strip(),
                'source': 'text_pattern',
                'metadata': {'version': match.group(1).strip()}
            })
    
    # Dependency patterns -> requirement category
    dependency_patterns = [
        r'(?i)requires? ([\w\-]+(?:\s+[\w\-]+)*)',
        r'(?i)depends on ([\w\-]+(?:\s+[\w\-]+)*)',
        r'(?i)needs ([\w\-]+(?:\s+[\w\-]+)*)',
        r'(?i)built on ([\w\-]+(?:\s+[\w\-]+)*)',
    ]
    
    for pattern in dependency_patterns:
        for match in re.finditer(pattern, content):
            observations.append({
                'category': 'requirement',
                'description': match.group(0).strip(),
                'source': 'text_pattern',
                'metadata': {'dependency': match.group(1).strip()}
            })
    
    # Best practices patterns -> best-practice category (with hyphen)
    best_practice_patterns = [
        r'(?i)best practice[:\s]+([^.\n]+)',
        r'(?i)recommended[:\s]+([^.\n]+)',
        r'(?i)should[:\s]+([^.\n]+)',
        r'(?i)it\'s recommended to ([^.\n]+)',
        r'(?i)you should ([^.\n]+)',
    ]
    
    for pattern in best_practice_patterns:
        for match in re.finditer(pattern, content):
            observations.append({
                'category': 'best-practice',
                'description': match.group(0).strip(),
                'source': 'text_pattern'
            })
    
    # Extract techniques from H2/H3 headings
    technique_heading_patterns = [
        r'(?i)how to',
        r'(?i)using',
        r'(?i)working with',
        r'(?i)creating',
        r'(?i)building',
        r'(?i)implementing',
    ]
    
    for heading in parsed['headings']:
        if heading['level'] in [2, 3]:
            for pattern in technique_heading_patterns:
                if re.search(pattern, heading['text']):
                    observations.append({
                        'category': 'technique',
                        'description': heading['text'],
                        'source': 'heading',
                        'metadata': {'heading_level': heading['level']}
                    })
                    break
    
    # Extract examples from code blocks
    for idx, code_block in enumerate(parsed['code_blocks']):
        observations.append({
            'category': 'example',
            'description': code_block['code'],
            'source': 'code_block',
            'metadata': {
                'language': code_block['language'],
                'index': idx
            }
        })
    
    # Warning patterns -> problem category
    warning_patterns = [
        r'(?i)(?:^|\n)(?:note|warning|caution|important):\s*([^\n]+)',
        r'(?i)⚠️\s*([^\n]+)',
        r'(?i)❗\s*([^\n]+)',
    ]
    
    for pattern in warning_patterns:
        for match in re.finditer(pattern, content):
            observations.append({
                'category': 'problem',
                'description': match.group(0).strip(),
                'source': 'text_pattern'
            })
    
    # Extract from blockquotes (often contain notes/tips) -> insight category
    for blockquote in parsed['blockquotes']:
        # Determine category based on content
        category = 'insight'
        if re.search(r'(?i)(warning|caution|danger)', blockquote):
            category = 'problem'
        elif re.search(r'(?i)(tip|hint|pro tip|best practice)', blockquote):
            category = 'best-practice'
        
        observations.append({
            'category': category,
            'description': blockquote,
            'source': 'blockquote'
        })
    
    return observations


def extract_relations(parsed: Dict, entity_id: str) -> List[Dict]:
    """
    Extract relations from links and cross-references.
    
    Extract from:
    - Markdown links (internal docs)
    - "See also" sections
    - Determine relation type from context
    
    Args:
        parsed: Dictionary from parse_markdown_structure()
        entity_id: Current entity ID
        
    Returns:
        List of relation dictionaries with source, target, type
    """
    relations = []
    
    # Process markdown links
    for link in parsed['links']:
        url = link['url']
        text = link['text']
        
        # Determine relation type based on URL and context
        relation_type = 'references'
        
        # Parse URL
        if url.startswith('#'):
            # Internal anchor - same document reference
            relation_type = 'references_section'
        elif url.startswith('http://') or url.startswith('https://'):
            # External link
            parsed_url = urlparse(url)
            if 'github.com' in parsed_url.netloc:
                relation_type = 'source_code'
            elif 'docs' in parsed_url.netloc or 'documentation' in parsed_url.path:
                relation_type = 'official_docs'
            else:
                relation_type = 'external_reference'
        elif url.endswith('.md'):
            # Internal documentation link
            relation_type = 'related_docs'
        
        # Determine target from URL or text
        target = url
        if url.startswith('#'):
            target = f"{entity_id}#{url[1:]}"
        elif url.endswith('.md'):
            # Convert file path to entity ID
            target = url.replace('/', '-').replace('.md', '')
        
        relations.append({
            'source': entity_id,
            'target': target,
            'type': relation_type,
            'metadata': {
                'link_text': text,
                'original_url': url
            }
        })
    
    # Extract from "See also" or "Related" sections
    content = parsed['raw_content']
    see_also_pattern = r'(?i)(?:^|\n)#{1,3}\s*(?:see also|related|further reading)[:\s]*\n((?:[-*]\s+.+\n?)+)'
    
    for match in re.finditer(see_also_pattern, content):
        section_content = match.group(1)
        # Extract items from list
        items = re.findall(r'[-*]\s+(.+)', section_content)
        
        for item in items:
            # Try to extract link from item
            link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', item)
            if link_match:
                target = link_match.group(2)
                relations.append({
                    'source': entity_id,
                    'target': target,
                    'type': 'related',
                    'metadata': {
                        'link_text': link_match.group(1),
                        'context': 'see_also_section'
                    }
                })
            else:
                # Plain text reference
                relations.append({
                    'source': entity_id,
                    'target': item.strip(),
                    'type': 'mentions',
                    'metadata': {
                        'context': 'see_also_section'
                    }
                })
    
    return relations


def load_parsed_markdown(markdown_file: Path) -> Optional[Dict]:
    """Load and parse markdown file."""
    try:
        # Import parse function from parse-markdown.py
        import importlib.util
        script_dir = Path(__file__).parent
        parse_script = script_dir / 'parse-markdown.py'
        
        spec = importlib.util.spec_from_file_location("parse_markdown", parse_script)
        parse_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parse_module)
        
        content = markdown_file.read_text(encoding='utf-8')
        return parse_module.parse_markdown_structure(content)
    except Exception as e:
        print(f"Error parsing markdown: {e}", file=sys.stderr)
        return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Extract metadata from markdown file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'markdown_file',
        type=Path,
        help='Path to markdown file'
    )
    parser.add_argument(
        'library',
        help='Library name (e.g., laravel, react)'
    )
    parser.add_argument(
        'entity_id',
        help='Entity ID for relations'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output JSON file (default: stdout)'
    )
    
    args = parser.parse_args()
    
    if not args.markdown_file.exists():
        print(f"Error: File not found: {args.markdown_file}", file=sys.stderr)
        return 2
    
    # Parse markdown
    parsed = load_parsed_markdown(args.markdown_file)
    if parsed is None:
        return 2
    
    # Extract metadata
    observations = extract_observations(parsed, args.library)
    relations = extract_relations(parsed, args.entity_id)
    
    # Build result
    result = {
        'entity_id': args.entity_id,
        'library': args.library,
        'source_file': str(args.markdown_file),
        'observations': observations,
        'relations': relations,
        'stats': {
            'observations_count': len(observations),
            'relations_count': len(relations),
            'observations_by_category': {}
        }
    }
    
    # Count observations by category
    for obs in observations:
        category = obs['category']
        result['stats']['observations_by_category'][category] = \
            result['stats']['observations_by_category'].get(category, 0) + 1
    
    # Output
    json_output = json.dumps(result, indent=2)
    
    if args.output:
        args.output.write_text(json_output, encoding='utf-8')
        print(f"Metadata written to: {args.output}")
    else:
        print(json_output)
    
    # Print summary
    print(f"\nExtracted from: {args.markdown_file}", file=sys.stderr)
    print(f"  Observations: {len(observations)}", file=sys.stderr)
    print(f"  Relations: {len(relations)}", file=sys.stderr)
    print(f"  Categories: {', '.join(result['stats']['observations_by_category'].keys())}", file=sys.stderr)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
