#!/usr/bin/env python3
"""
Validate Library Documentation Metadata JSON

Validates the structure and content of lib-docs-{library}.json files.

Usage:
    python validate-lib-docs.py <json-file>
    python validate-lib-docs.py --help

Example:
    python validate-lib-docs.py knowledge-base/libraries/laravel/lib-docs-laravel.json

Exit codes:
    0 - Validation passed
    1 - Warning (non-critical issues)
    2 - Error (critical validation failure)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


REQUIRED_ROOT_FIELDS = ['library', 'version', 'source_url', 'entities', 'metadata']
REQUIRED_ENTITY_FIELDS = ['id', 'name', 'type', 'file_path', 'observations', 'tags']
REQUIRED_OBSERVATION_FIELDS = ['category', 'description']
VALID_OBSERVATION_CATEGORIES = [
    'version', 'dependency', 'best_practice', 'technique',
    'example', 'warning', 'note', 'api', 'configuration'
]
REQUIRED_RELATION_FIELDS = ['source', 'target', 'type']


def validate_metadata_json(json_file: Path) -> Tuple[int, List[str], List[str]]:
    """
    Validate lib-docs-{library}.json structure.
    
    Validates:
    - Required fields present
    - Entity IDs unique
    - Relations reference valid entities
    - Observations have valid categories
    - Tags are non-empty arrays
    
    Args:
        json_file: Path to JSON file
        
    Returns:
        Tuple of (exit_code, errors, warnings)
        exit_code: 0=success, 1=warning, 2=error
        errors: List of error messages
        warnings: List of warning messages
    """
    errors = []
    warnings = []
    
    # Load JSON
    try:
        data = json.loads(json_file.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return 2, errors, warnings
    except Exception as e:
        errors.append(f"Error reading file: {e}")
        return 2, errors, warnings
    
    # Validate root fields
    for field in REQUIRED_ROOT_FIELDS:
        if field not in data:
            errors.append(f"Missing required root field: {field}")
    
    if errors:
        return 2, errors, warnings
    
    # Validate entities
    if not isinstance(data['entities'], list):
        errors.append("'entities' must be an array")
        return 2, errors, warnings
    
    if len(data['entities']) == 0:
        warnings.append("No entities found in documentation")
    
    entity_ids = set()
    
    for idx, entity in enumerate(data['entities']):
        entity_prefix = f"Entity #{idx}"
        
        # Check required fields
        for field in REQUIRED_ENTITY_FIELDS:
            if field not in entity:
                errors.append(f"{entity_prefix}: Missing required field '{field}'")
        
        if 'id' not in entity:
            continue
        
        entity_id = entity['id']
        entity_prefix = f"Entity '{entity_id}'"
        
        # Check ID uniqueness
        if entity_id in entity_ids:
            errors.append(f"{entity_prefix}: Duplicate entity ID")
        entity_ids.add(entity_id)
        
        # Validate observations
        if 'observations' in entity:
            if not isinstance(entity['observations'], list):
                errors.append(f"{entity_prefix}: 'observations' must be an array")
            else:
                for obs_idx, obs in enumerate(entity['observations']):
                    obs_prefix = f"{entity_prefix}, Observation #{obs_idx}"
                    
                    # Check required fields
                    for field in REQUIRED_OBSERVATION_FIELDS:
                        if field not in obs:
                            errors.append(f"{obs_prefix}: Missing required field '{field}'")
                    
                    # Validate category
                    if 'category' in obs:
                        if obs['category'] not in VALID_OBSERVATION_CATEGORIES:
                            warnings.append(
                                f"{obs_prefix}: Unknown category '{obs['category']}'. "
                                f"Valid: {', '.join(VALID_OBSERVATION_CATEGORIES)}"
                            )
                    
                    # Check content not empty
                    if 'description' in obs and not obs['description']:
                        warnings.append(f"{obs_prefix}: Empty description")
        
        # Validate tags
        if 'tags' in entity:
            if not isinstance(entity['tags'], list):
                errors.append(f"{entity_prefix}: 'tags' must be an array")
            elif len(entity['tags']) == 0:
                warnings.append(f"{entity_prefix}: Empty tags array")
            else:
                # Check for duplicate tags
                if len(entity['tags']) != len(set(entity['tags'])):
                    warnings.append(f"{entity_prefix}: Duplicate tags found")
        
        # Validate file_path exists
        if 'file_path' in entity:
            file_path = Path(entity['file_path'])
            if not file_path.is_absolute():
                # Try relative to json file
                file_path = json_file.parent / file_path
            
            if not file_path.exists():
                warnings.append(f"{entity_prefix}: File not found: {entity['file_path']}")
    
    # Validate relations (if present)
    if 'relations' in data:
        if not isinstance(data['relations'], list):
            errors.append("'relations' must be an array")
        else:
            for rel_idx, relation in enumerate(data['relations']):
                rel_prefix = f"Relation #{rel_idx}"
                
                # Check required fields
                for field in REQUIRED_RELATION_FIELDS:
                    if field not in relation:
                        errors.append(f"{rel_prefix}: Missing required field '{field}'")
                
                # Validate source and target reference valid entities
                if 'source' in relation:
                    source_id = relation['source']
                    if source_id not in entity_ids:
                        # Check if it's an external reference
                        if not source_id.startswith('http') and '#' not in source_id:
                            warnings.append(
                                f"{rel_prefix}: Source '{source_id}' not found in entities "
                                "(may be external reference)"
                            )
                
                if 'target' in relation:
                    target_id = relation['target']
                    if target_id not in entity_ids:
                        # Check if it's an external reference
                        if not target_id.startswith('http') and '#' not in target_id:
                            warnings.append(
                                f"{rel_prefix}: Target '{target_id}' not found in entities "
                                "(may be external reference)"
                            )
    
    # Validate metadata
    if 'metadata' in data:
        if not isinstance(data['metadata'], dict):
            errors.append("'metadata' must be an object")
        else:
            # Check for generated_at timestamp
            if 'generated_at' not in data['metadata']:
                warnings.append("'metadata' missing 'generated_at' timestamp")
    
    # Determine exit code
    if errors:
        return 2, errors, warnings
    elif warnings:
        return 1, errors, warnings
    else:
        return 0, errors, warnings


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Validate library documentation metadata JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'json_file',
        type=Path,
        help='Path to lib-docs-*.json file'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print detailed validation results'
    )
    
    args = parser.parse_args()
    
    if not args.json_file.exists():
        print(f"Error: File not found: {args.json_file}", file=sys.stderr)
        return 2
    
    if not args.json_file.is_file():
        print(f"Error: Not a file: {args.json_file}", file=sys.stderr)
        return 2
    
    # Validate
    exit_code, errors, warnings = validate_metadata_json(args.json_file)
    
    # Print results
    if exit_code == 0:
        print(f"✓ Validation passed: {args.json_file}")
        if warnings and args.verbose:
            print(f"\nWarnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  ⚠ {warning}")
    elif exit_code == 1:
        print(f"⚠ Validation passed with warnings: {args.json_file}")
        print(f"\nWarnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  ⚠ {warning}")
    else:
        print(f"✗ Validation failed: {args.json_file}", file=sys.stderr)
        if errors:
            print(f"\nErrors ({len(errors)}):", file=sys.stderr)
            for error in errors:
                print(f"  ✗ {error}", file=sys.stderr)
        if warnings:
            print(f"\nWarnings ({len(warnings)}):", file=sys.stderr)
            for warning in warnings:
                print(f"  ⚠ {warning}", file=sys.stderr)
    
    # Summary
    if args.verbose:
        # Load and count
        try:
            data = json.loads(args.json_file.read_text(encoding='utf-8'))
            entity_count = len(data.get('entities', []))
            relation_count = len(data.get('relations', []))
            
            obs_count = sum(
                len(entity.get('observations', []))
                for entity in data.get('entities', [])
            )
            
            print(f"\nSummary:")
            print(f"  Library: {data.get('library', 'unknown')}")
            print(f"  Entities: {entity_count}")
            print(f"  Observations: {obs_count}")
            print(f"  Relations: {relation_count}")
        except:
            pass
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
