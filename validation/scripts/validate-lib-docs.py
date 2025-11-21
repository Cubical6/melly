#!/usr/bin/env python3
"""
Validate Library Documentation Metadata

Validates the structure and content of lib-docs-{library}.json files.

Checks:
1. JSON structure and syntax
2. Required fields presence
3. Data type correctness
4. Relation integrity
5. File path references
6. Duplicate detection

Outputs detailed validation report.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict


# Schema definition for lib-docs metadata
SCHEMA = {
    'library_name': {'type': str, 'required': True},
    'version': {'type': str, 'required': False},
    'description': {'type': str, 'required': False},
    'source_url': {'type': str, 'required': False},
    'documentation': {'type': list, 'required': True},
}

DOC_ENTRY_SCHEMA = {
    'file_path': {'type': str, 'required': True},
    'title': {'type': str, 'required': True},
    'observations': {'type': list, 'required': True},
    'relations': {'type': list, 'required': False},
    'tags': {'type': list, 'required': False},
}

RELATION_SCHEMA = {
    'type': {'type': str, 'required': True},
    'target': {'type': str, 'required': True},
    'context': {'type': str, 'required': False},
}


def validate_schema(data, schema, path=''):
    """
    Validate data against schema.

    Args:
        data (dict): Data to validate
        schema (dict): Schema definition
        path (str): Current path in data structure

    Returns:
        list: List of validation errors
    """
    errors = []

    for field, rules in schema.items():
        field_path = f'{path}.{field}' if path else field

        # Check required fields
        if rules.get('required', False) and field not in data:
            errors.append({
                'type': 'missing_field',
                'path': field_path,
                'message': f'Required field missing: {field}'
            })
            continue

        # Check field type
        if field in data:
            expected_type = rules['type']
            actual_value = data[field]

            if not isinstance(actual_value, expected_type):
                errors.append({
                    'type': 'type_error',
                    'path': field_path,
                    'message': f'Expected {expected_type.__name__}, got {type(actual_value).__name__}',
                    'value': str(actual_value)[:100]
                })

    return errors


def validate_metadata(metadata):
    """
    Validate library documentation metadata structure.

    Args:
        metadata (dict): Parsed metadata JSON

    Returns:
        dict: Validation results
    """
    errors = []
    warnings = []

    # Validate top-level schema
    errors.extend(validate_schema(metadata, SCHEMA))

    # Validate documentation entries
    if 'documentation' in metadata:
        docs = metadata['documentation']

        if not isinstance(docs, list):
            errors.append({
                'type': 'type_error',
                'path': 'documentation',
                'message': 'documentation must be a list'
            })
        else:
            file_paths = set()
            titles = []

            for i, doc in enumerate(docs):
                doc_path = f'documentation[{i}]'

                # Validate document entry schema
                errors.extend(validate_schema(doc, DOC_ENTRY_SCHEMA, doc_path))

                # Check for duplicate file paths
                if 'file_path' in doc:
                    file_path = doc['file_path']
                    if file_path in file_paths:
                        errors.append({
                            'type': 'duplicate',
                            'path': f'{doc_path}.file_path',
                            'message': f'Duplicate file_path: {file_path}'
                        })
                    file_paths.add(file_path)

                # Track titles
                if 'title' in doc:
                    titles.append(doc['title'])

                # Validate observations
                if 'observations' in doc:
                    obs = doc['observations']
                    if not isinstance(obs, list):
                        errors.append({
                            'type': 'type_error',
                            'path': f'{doc_path}.observations',
                            'message': 'observations must be a list'
                        })
                    elif len(obs) == 0:
                        warnings.append({
                            'type': 'empty_field',
                            'path': f'{doc_path}.observations',
                            'message': 'observations list is empty'
                        })

                # Validate relations
                if 'relations' in doc:
                    relations = doc['relations']
                    if not isinstance(relations, list):
                        errors.append({
                            'type': 'type_error',
                            'path': f'{doc_path}.relations',
                            'message': 'relations must be a list'
                        })
                    else:
                        for j, relation in enumerate(relations):
                            rel_path = f'{doc_path}.relations[{j}]'
                            errors.extend(validate_schema(relation, RELATION_SCHEMA, rel_path))

                            # Validate relation target references
                            if 'target' in relation:
                                target = relation['target']
                                # Check if target references another doc in the same metadata
                                if target.endswith('.md') and target not in file_paths:
                                    warnings.append({
                                        'type': 'broken_reference',
                                        'path': f'{rel_path}.target',
                                        'message': f'Relation target not found in documentation: {target}'
                                    })

                # Validate tags
                if 'tags' in doc:
                    tags = doc['tags']
                    if not isinstance(tags, list):
                        errors.append({
                            'type': 'type_error',
                            'path': f'{doc_path}.tags',
                            'message': 'tags must be a list'
                        })
                    else:
                        for tag in tags:
                            if not isinstance(tag, str):
                                errors.append({
                                    'type': 'type_error',
                                    'path': f'{doc_path}.tags',
                                    'message': f'Tag must be string, got {type(tag).__name__}'
                                })

            # Statistics
            stats = {
                'total_documents': len(docs),
                'unique_file_paths': len(file_paths),
                'unique_titles': len(set(titles)),
                'total_observations': sum(len(doc.get('observations', [])) for doc in docs),
                'total_relations': sum(len(doc.get('relations', [])) for doc in docs),
                'total_tags': sum(len(doc.get('tags', [])) for doc in docs),
            }
    else:
        stats = {}

    # Determine validation status
    is_valid = len(errors) == 0

    return {
        'valid': is_valid,
        'errors': errors,
        'warnings': warnings,
        'statistics': stats
    }


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python validate-lib-docs.py <metadata_json_path>",
              file=sys.stderr)
        sys.exit(1)

    json_path = Path(sys.argv[1])

    # Validate file exists
    if not json_path.exists():
        print(json.dumps({
            'valid': False,
            'error': f'File not found: {json_path}',
            'errors': [],
            'warnings': []
        }, indent=2))
        sys.exit(1)

    # Validate file extension
    if json_path.suffix.lower() != '.json':
        print(json.dumps({
            'valid': False,
            'error': f'File must have .json extension: {json_path}',
            'errors': [],
            'warnings': []
        }, indent=2))
        sys.exit(1)

    try:
        # Read and parse JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Validate metadata
        result = validate_metadata(metadata)

        # Add file info
        result['file_path'] = str(json_path.absolute())
        result['file_name'] = json_path.name

        # Output validation report
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # Exit with appropriate code
        sys.exit(0 if result['valid'] else 1)

    except json.JSONDecodeError as e:
        print(json.dumps({
            'valid': False,
            'error': f'Invalid JSON: {e}',
            'file_path': str(json_path.absolute()),
            'errors': [{
                'type': 'json_parse_error',
                'message': str(e),
                'line': e.lineno if hasattr(e, 'lineno') else None,
                'column': e.colno if hasattr(e, 'colno') else None
            }],
            'warnings': []
        }, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            'valid': False,
            'error': f'Unexpected error: {e}',
            'file_path': str(json_path.absolute()),
            'errors': [{
                'type': 'unexpected_error',
                'message': str(e)
            }],
            'warnings': []
        }, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
