#!/usr/bin/env python3
"""
Library Documentation Processor

Processes library documentation files through the complete workflow:
1. Parse markdown structure
2. Extract semantic metadata
3. Generate enhanced files with frontmatter
4. Validate content preservation
5. Generate comprehensive metadata JSON

Usage:
    python process-library-docs.py <docs_dir> <library_name> <version>
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import yaml


def run_command(cmd):
    """Run a shell command and return output."""
    try:
        # Convert all Path objects to strings
        cmd_str = [str(c) for c in cmd]
        result = subprocess.run(
            cmd_str,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(str(c) for c in cmd)}", file=sys.stderr)
        print(f"Error output: {e.stderr}", file=sys.stderr)
        return None


def parse_markdown_file(file_path, script_path):
    """Parse markdown file structure."""
    output = run_command(['python3', script_path, str(file_path)])
    if output:
        try:
            return json.loads(output)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from parse-markdown.py: {e}", file=sys.stderr)
            return None
    return None


def extract_metadata(file_path, library_name, script_path):
    """Extract metadata from markdown file."""
    output = run_command(['python3', script_path, str(file_path), library_name])
    if output:
        try:
            return json.loads(output)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from extract-metadata.py: {e}", file=sys.stderr)
            return None
    return None


def determine_category(file_name, parsed_data, metadata):
    """Determine the category for a file based on its name and content."""
    name = file_name.replace('.md', '').lower()

    # Category mapping
    categories = {
        'getting-started': ['installation', 'configuration', 'deployment', 'upgrade', 'structure', 'lifecycle'],
        'architecture': ['providers', 'facades', 'contracts', 'container'],
        'basics': ['routing', 'middleware', 'csrf', 'controllers', 'requests', 'responses', 'redirects', 'views', 'urls', 'session', 'validation', 'errors'],
        'frontend': ['blade', 'vite', 'mix', 'frontend', 'folio', 'precognition'],
        'security': ['authentication', 'authorization', 'verification', 'passwords', 'encryption', 'hashing'],
        'database': ['database', 'queries', 'pagination', 'migrations', 'seeding', 'redis', 'mongodb'],
        'eloquent': ['eloquent', 'eloquent-relationships', 'eloquent-collections', 'eloquent-resources', 'eloquent-serialization', 'eloquent-mutators', 'eloquent-factories'],
        'testing': ['testing', 'http-tests', 'console-tests', 'dusk', 'database-testing', 'mocking'],
        'packages': ['billing', 'cashier-paddle', 'envoy', 'fortify', 'folio', 'homestead', 'horizon', 'passport', 'pennant', 'pint', 'precognition', 'prompts', 'pulse', 'reverb', 'sail', 'sanctum', 'scout', 'socialite', 'telescope', 'valet'],
        'advanced': ['artisan', 'broadcasting', 'cache', 'collections', 'concurrency', 'context', 'events', 'filesystem', 'helpers', 'http-client', 'localization', 'logging', 'mail', 'notifications', 'octane', 'packages', 'processes', 'queues', 'rate-limiting', 'scheduling', 'strings', 'mcp'],
        'official-packages': ['starter-kits', 'billing', 'cashier-paddle', 'dusk', 'envoy', 'fortify', 'folio', 'homestead', 'horizon', 'passport', 'pennant', 'pint', 'precognition', 'prompts', 'pulse', 'reverb', 'sail', 'sanctum', 'scout', 'socialite', 'telescope', 'valet'],
        'reference': ['releases', 'contributions']
    }

    # Find matching category
    for category, keywords in categories.items():
        if name in keywords:
            return category

    return 'other'


def generate_enhanced_content(original_content, parsed_data, metadata, library_name, version):
    """Generate enhanced file content with YAML frontmatter."""
    file_name = metadata['file_name']

    # Determine category
    category = determine_category(file_name, parsed_data, metadata)

    # Build YAML frontmatter
    frontmatter = {
        'title': parsed_data.get('title', file_name.replace('.md', '').title()),
        'library': library_name,
        'version': version,
        'category': category,
        'tags': metadata.get('tags', []),
        'file_info': {
            'name': file_name,
            'path': metadata['file_path'],
            'size': len(original_content)
        },
        'structure': {
            'headings_count': len(parsed_data.get('headings', [])),
            'code_blocks_count': len(parsed_data.get('code_blocks', [])),
            'internal_links_count': len(parsed_data.get('links', []))
        },
        'processed_at': datetime.utcnow().isoformat() + 'Z'
    }

    # Build metadata section
    observations = metadata.get('observations', [])[:10]  # Top 10 observations
    relations = metadata.get('relations', [])[:20]  # Top 20 relations

    metadata_section = f"\n## Metadata\n\n"

    if observations:
        metadata_section += "### Key Observations\n\n"
        for i, obs in enumerate(observations, 1):
            metadata_section += f"{i}. {obs}\n"
        metadata_section += "\n"

    if relations:
        # Group relations by type
        refs = [r for r in relations if r['type'] == 'references']
        if refs:
            metadata_section += "### Related Documentation\n\n"
            for ref in refs[:10]:
                target = ref['target']
                context = ref['context'] or target
                metadata_section += f"- [{context}]({target})\n"
            metadata_section += "\n"

    # Combine everything
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)

    enhanced = f"---\n{yaml_str}---\n{metadata_section}---\n\n{original_content}"

    return enhanced


def validate_enhanced_file(original_path, enhanced_path, script_path):
    """Validate that enhanced file preserves original content."""
    output = run_command(['python3', script_path, str(original_path), str(enhanced_path)])
    if output:
        try:
            return json.loads(output)
        except json.JSONDecodeError as e:
            print(f"Error parsing validation JSON: {e}", file=sys.stderr)
            return {'success': False, 'error': str(e)}
    return {'success': False, 'error': 'Failed to run validation script'}


def main():
    """Main entry point."""
    if len(sys.argv) != 4:
        print("Usage: python process-library-docs.py <docs_dir> <library_name> <version>", file=sys.stderr)
        sys.exit(1)

    docs_dir = Path(sys.argv[1]).absolute()
    library_name = sys.argv[2]
    version = sys.argv[3]

    # Script paths
    script_dir = Path(__file__).parent
    parse_script = script_dir / 'parse-markdown.py'
    extract_script = script_dir / 'extract-metadata.py'
    validate_script = script_dir / 'validate-content.py'

    # Verify scripts exist
    for script in [parse_script, extract_script, validate_script]:
        if not script.exists():
            print(f"Error: Required script not found: {script}", file=sys.stderr)
            sys.exit(1)

    # Find markdown files (exclude special files and enhanced files)
    excluded_files = ['README.md', 'INDEX.md', 'METADATA.json', 'QUICK-REFERENCE.md',
                      'readme.md', 'license.md', 'documentation.md']

    md_files = [f for f in docs_dir.glob('*.md')
                if f.name not in excluded_files and not f.name.endswith('.enhanced.md')]
    md_files.sort()

    print(f"\n=== Laravel {version} Documentation Processor ===")
    print(f"Library: {library_name}")
    print(f"Directory: {docs_dir}")
    print(f"Total files to process: {len(md_files)}\n")

    # Storage for results
    all_metadata = []
    validation_results = []
    errors = []

    # Process each file
    for i, file_path in enumerate(md_files, 1):
        file_name = file_path.name

        # Progress indicator
        if i % 10 == 0 or i == 1:
            print(f"Processing {i}/{len(md_files)}: {file_name}")

        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Phase 2: Parse and Extract
            parsed_data = parse_markdown_file(file_path, parse_script)
            metadata = extract_metadata(file_path, library_name, extract_script)

            if not parsed_data or not metadata:
                errors.append({
                    'file': file_name,
                    'phase': 'parse/extract',
                    'error': 'Failed to parse or extract metadata'
                })
                continue

            # Phase 3: Generate Enhanced File
            enhanced_content = generate_enhanced_content(
                original_content, parsed_data, metadata, library_name, version
            )

            # Save enhanced file
            enhanced_path = file_path.parent / f"{file_path.stem}.enhanced.md"
            with open(enhanced_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)

            # Phase 4: Validate
            validation = validate_enhanced_file(file_path, enhanced_path, validate_script)
            validation_results.append({
                'file': file_name,
                'success': validation.get('success', False),
                'validation': validation
            })

            if not validation.get('success', False):
                errors.append({
                    'file': file_name,
                    'phase': 'validation',
                    'error': validation.get('error', 'Validation failed')
                })

            # Store metadata for JSON output
            all_metadata.append({
                'file_name': file_name,
                'file_path': str(file_path.absolute()),
                'enhanced_path': str(enhanced_path.absolute()),
                'title': parsed_data.get('title'),
                'category': determine_category(file_name, parsed_data, metadata),
                'tags': metadata.get('tags', []),
                'observations': metadata.get('observations', [])[:10],
                'relations': metadata.get('relations', [])[:20],
                'structure': {
                    'headings': len(parsed_data.get('headings', [])),
                    'code_blocks': len(parsed_data.get('code_blocks', [])),
                    'links': len(parsed_data.get('links', []))
                }
            })

        except Exception as e:
            errors.append({
                'file': file_name,
                'phase': 'processing',
                'error': str(e)
            })
            print(f"  ERROR processing {file_name}: {e}", file=sys.stderr)

    # Calculate statistics
    total_observations = sum(len(m.get('observations', [])) for m in all_metadata)
    total_relations = sum(len(m.get('relations', [])) for m in all_metadata)
    successful_validations = sum(1 for v in validation_results if v['success'])

    # Phase 5: Generate Metadata JSON
    output_json = {
        'library': {
            'name': library_name,
            'version': version,
            'processed_at': datetime.utcnow().isoformat() + 'Z'
        },
        'statistics': {
            'total_files': len(md_files),
            'processed_files': len(all_metadata),
            'total_observations': total_observations,
            'total_relations': total_relations,
            'successful_validations': successful_validations,
            'failed_validations': len(validation_results) - successful_validations,
            'errors': len(errors)
        },
        'files': all_metadata,
        'validation_summary': validation_results,
        'errors': errors
    }

    # Save metadata JSON
    output_path = docs_dir / f'lib-docs-{library_name}-{version.replace(".", "-")}.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n=== Processing Complete ===")
    print(f"Files processed: {len(all_metadata)}/{len(md_files)}")
    print(f"Total observations extracted: {total_observations}")
    print(f"Total relations found: {total_relations}")
    print(f"Successful validations: {successful_validations}/{len(validation_results)}")
    print(f"Failed validations: {len(validation_results) - successful_validations}")
    print(f"Errors encountered: {len(errors)}")
    print(f"\nMetadata JSON saved: {output_path}")
    print(f"Enhanced files saved with .enhanced.md suffix")

    if errors:
        print(f"\n=== Errors ===")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error['file']} ({error['phase']}): {error['error']}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

    # Return summary as JSON
    print(f"\n=== JSON Summary ===")
    print(json.dumps(output_json['statistics'], indent=2))


if __name__ == '__main__':
    main()
