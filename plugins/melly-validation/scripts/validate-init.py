#!/usr/bin/env python3
"""
Validate init.json structure.

Exit codes:
  0 - Validation passed
  1 - Non-blocking warning (continue with user notification)
  2 - Blocking error (halt workflow immediately)
"""

import sys
import json
import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Any


# Allowed manifest types
ALLOWED_MANIFEST_TYPES = [
    "npm", "composer", "cargo", "go-mod", "gradle", "maven",
    "requirements-txt", "pyproject-toml", "gemfile", "unknown"
]

# Semver pattern
SEMVER_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')


def error(message: str, location: str = "", expected: str = "", actual: str = "") -> None:
    """Print formatted error message to stderr."""
    print(f"[VALIDATE-INIT] ERROR: {message}", file=sys.stderr)
    if location:
        print(f"  Location: {location}", file=sys.stderr)
    if expected:
        print(f"  Expected: {expected}", file=sys.stderr)
    if actual:
        print(f"  Actual: {actual}", file=sys.stderr)
    print("", file=sys.stderr)


def warning(message: str, recommendation: str = "") -> None:
    """Print formatted warning message to stderr."""
    print(f"[VALIDATE-INIT] WARNING: {message}", file=sys.stderr)
    if recommendation:
        print(f"  Recommendation: {recommendation}", file=sys.stderr)
    print("", file=sys.stderr)


def validate_schema_structure(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate basic schema structure."""
    errors = []

    # Check required top-level fields
    if "metadata" not in data:
        errors.append("Missing required field: metadata")
        return False, errors

    metadata = data["metadata"]

    # Check metadata fields
    required_metadata = ["schema_version", "generator", "generated_by", "timestamp", "melly_version"]
    for field in required_metadata:
        if field not in metadata:
            errors.append(f"Missing required field: metadata.{field}")

    # Validate schema_version format
    if "schema_version" in metadata:
        if not SEMVER_PATTERN.match(metadata["schema_version"]):
            errors.append(f"Invalid schema_version format: {metadata['schema_version']} (expected semver)")

    # Validate timestamp format
    if "timestamp" in metadata:
        try:
            datetime.fromisoformat(metadata["timestamp"].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            errors.append(f"Invalid timestamp format: {metadata.get('timestamp')} (expected ISO 8601)")

    # Check repositories array
    if "repositories" not in data:
        errors.append("Missing required field: repositories")
    elif not isinstance(data["repositories"], list):
        errors.append("Field 'repositories' must be an array")
    elif len(data["repositories"]) == 0:
        errors.append("No repositories found (repositories array is empty)")

    return len(errors) == 0, errors


def validate_repository_paths(repositories: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate repository paths."""
    errors = []
    warnings = []
    seen_paths = set()
    seen_names = set()

    for idx, repo in enumerate(repositories):
        if not isinstance(repo, dict):
            errors.append(f"Repository at index {idx} is not an object")
            continue

        # Check for required fields
        if "path" not in repo:
            errors.append(f"Repository at index {idx}: Missing 'path' field")
            continue

        path = repo["path"]

        # Check if path is absolute
        if not os.path.isabs(path):
            errors.append(f"Repository path must be absolute: {path}")
            continue

        # Check for duplicates
        if path in seen_paths:
            errors.append(f"Duplicate repository path: {path}")
        seen_paths.add(path)

        # Check if path exists
        if not os.path.exists(path):
            errors.append(f"Repository path does not exist: {path}")
            continue

        # Check if path is a directory
        if not os.path.isdir(path):
            errors.append(f"Repository path is not a directory: {path}")

        # Check for duplicate names (warning only)
        if "name" in repo:
            name = repo["name"]
            if name in seen_names:
                warnings.append(f"Duplicate repository name: {name}")
            seen_names.add(name)

    return len(errors) == 0, errors, warnings


def validate_package_manifests(repositories: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate package manifests."""
    errors = []
    warnings = []

    for repo in repositories:
        if not isinstance(repo, dict):
            continue

        if "manifests" not in repo:
            continue

        manifests = repo["manifests"]
        if not isinstance(manifests, list):
            errors.append(f"Repository '{repo.get('name', 'unknown')}': manifests must be an array")
            continue

        repo_path = repo.get("path", "")

        for idx, manifest in enumerate(manifests):
            if not isinstance(manifest, dict):
                errors.append(f"Manifest at index {idx} in '{repo.get('name', 'unknown')}' is not an object")
                continue

            # Check required fields
            required_fields = ["type", "path", "data"]
            for field in required_fields:
                if field not in manifest:
                    errors.append(f"Manifest at index {idx}: Missing '{field}' field")

            # Validate type
            if "type" in manifest:
                if manifest["type"] not in ALLOWED_MANIFEST_TYPES:
                    warnings.append(f"Unknown manifest type: {manifest['type']}")

            # Validate path (should be relative)
            if "path" in manifest:
                manifest_path = manifest["path"]
                if os.path.isabs(manifest_path):
                    errors.append(f"Manifest path should be relative: {manifest_path}")

                # Check if full path exists (warning only)
                if repo_path and not os.path.isabs(manifest_path):
                    full_path = os.path.join(repo_path, manifest_path)
                    if not os.path.exists(full_path):
                        warnings.append(f"Manifest file not found: {full_path}")

            # Validate data field
            if "data" in manifest:
                if not isinstance(manifest["data"], dict):
                    errors.append("Manifest 'data' field must be an object")
                else:
                    # Manifest-specific validation
                    manifest_type = manifest.get("type", "")
                    data = manifest["data"]

                    if manifest_type == "npm":
                        if "name" not in data:
                            warnings.append("NPM manifest missing 'name' field in data")
                    elif manifest_type == "composer":
                        if "name" not in data:
                            warnings.append("Composer manifest missing 'name' field in data")
                    elif manifest_type == "cargo":
                        if "package" in data and "name" not in data["package"]:
                            warnings.append("Cargo manifest missing 'package.name' field in data")

    return len(errors) == 0, errors, warnings


def validate_timestamps(metadata: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate timestamps."""
    warnings = []

    if "timestamp" not in metadata:
        return True, warnings

    try:
        timestamp_str = metadata["timestamp"]
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)

        # Check if timestamp is in the future
        if timestamp > now:
            warnings.append(f"Timestamp is in the future: {timestamp_str}")

        # Check if metadata.generated_at exists and is within 1 hour
        if "generated_at" in metadata:
            try:
                generated_at = datetime.fromisoformat(metadata["generated_at"].replace('Z', '+00:00'))
                diff = abs((timestamp - generated_at).total_seconds())
                if diff > 3600:  # 1 hour
                    warnings.append("Timestamp and generated_at differ by more than 1 hour")
            except (ValueError, AttributeError):
                warnings.append(f"Invalid generated_at format: {metadata.get('generated_at')}")

    except (ValueError, AttributeError):
        # Already caught in schema validation
        pass

    return True, warnings


def main() -> int:
    """Main validation function."""
    # Check if init.json file exists
    init_file = "knowledge-base/init.json"
    if not os.path.exists(init_file):
        # Try alternative path
        init_file = os.path.join(os.getcwd(), "knowledge-base", "init.json")
        if not os.path.exists(init_file):
            # No init.json file found - skip validation
            print("[VALIDATE-INIT] No init.json file found - skipping validation", file=sys.stderr)
            return 0

    # Load and validate the init.json file
    try:
        with open(init_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        error(f"Invalid JSON in {init_file}", actual=str(e))
        return 2
    except Exception as e:
        error(f"Failed to read {init_file}: {str(e)}")
        return 2

    has_errors = False
    has_warnings = False

    # 1. Validate schema structure
    valid, errors = validate_schema_structure(data)
    if not valid:
        has_errors = True
        for err in errors:
            error(err)

    # If critical structure is missing, stop here
    if has_errors:
        return 2

    # 2. Validate repository paths
    repositories = data.get("repositories", [])
    valid, errors, warns = validate_repository_paths(repositories)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="repositories")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 3. Validate package manifests
    valid, errors, warns = validate_package_manifests(repositories)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="manifests")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 4. Validate timestamps
    metadata = data.get("metadata", {})
    valid, warns = validate_timestamps(metadata)
    for warn in warns:
        has_warnings = True
        warning(warn)

    # No manifests warning
    total_manifests = sum(len(repo.get("manifests", [])) for repo in repositories)
    if total_manifests == 0:
        has_warnings = True
        warning("No package manifests found", recommendation="Ensure repositories contain package manifest files")

    # Return appropriate exit code
    if has_errors:
        print("[VALIDATE-INIT] FAILED with errors", file=sys.stderr)
        return 2
    elif has_warnings:
        print("[VALIDATE-INIT] PASSED with warnings", file=sys.stderr)
        return 1
    else:
        print("[VALIDATE-INIT] PASSED", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
