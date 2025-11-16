#!/usr/bin/env python3
"""
Validate c1-systems.json structure.

Exit codes:
  0 - Validation passed
  1 - Non-blocking warning (continue with user notification)
  2 - Blocking error (halt workflow immediately)
"""

import sys
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Set
from pathlib import Path


# ID pattern
ID_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

# Allowed system types
ALLOWED_SYSTEM_TYPES = [
    "web-application", "mobile-application", "desktop-application",
    "api-service", "database", "message-broker", "cache", "cdn",
    "external-service", "user-facing", "internal-service",
    "data-store", "integration", "other"
]

# Allowed observation categories
OBSERVATION_CATEGORIES = [
    "architectural", "technical", "quality", "security",
    "performance", "scalability", "maintainability", "integration",
    "deployment", "data", "testing", "documentation"
]

# Allowed observation severities
OBSERVATION_SEVERITIES = ["info", "warning", "critical"]

# Allowed relation types
RELATION_TYPES = [
    "http-rest", "http-graphql", "http-soap", "grpc", "websocket",
    "message-queue", "event-stream", "database-query", "database-write",
    "file-io", "dependency", "inheritance", "composition", "aggregation",
    "uses", "calls", "contains", "http", "https", "graphql", "rpc",
    "database-connection", "file-transfer", "authentication", "soap",
    "smtp", "external-api"
]


def error(message: str, location: str = "", expected: str = "", actual: str = "") -> None:
    """Print formatted error message to stderr."""
    print(f"[VALIDATE-C1] ERROR: {message}", file=sys.stderr)
    if location:
        print(f"  Location: {location}", file=sys.stderr)
    if expected:
        print(f"  Expected: {expected}", file=sys.stderr)
    if actual:
        print(f"  Actual: {actual}", file=sys.stderr)
    print("", file=sys.stderr)


def warning(message: str, recommendation: str = "") -> None:
    """Print formatted warning message to stderr."""
    print(f"[VALIDATE-C1] WARNING: {message}", file=sys.stderr)
    if recommendation:
        print(f"  Recommendation: {recommendation}", file=sys.stderr)
    print("", file=sys.stderr)


def validate_parent_reference(data: Dict[str, Any], init_file_path: str) -> Tuple[bool, List[str]]:
    """Validate parent file reference."""
    errors = []

    # Check if init.json exists
    if not os.path.exists(init_file_path):
        errors.append(f"Parent file not found: {init_file_path}")
        errors.append("RECOMMENDATION: Run /melly-init first")
        return False, errors

    # Load parent file
    try:
        with open(init_file_path, 'r') as f:
            init_data = json.load(f)
    except Exception as e:
        errors.append(f"Failed to read parent file: {str(e)}")
        return False, errors

    # Get parent timestamp
    parent_timestamp_str = init_data.get("metadata", {}).get("timestamp")
    if not parent_timestamp_str:
        errors.append("Parent file missing metadata.timestamp")
        return False, errors

    # Check metadata.parent structure
    if "metadata" not in data:
        errors.append("Missing metadata field")
        return False, errors

    metadata = data["metadata"]
    if "parent" in metadata:
        parent = metadata["parent"]

        # Check parent.timestamp
        if "timestamp" in parent:
            if parent["timestamp"] != parent_timestamp_str:
                errors.append("Parent timestamp mismatch")
                errors.append(f"  Expected: {parent_timestamp_str}")
                errors.append(f"  Actual: {parent['timestamp']}")
                return False, errors

    # Check timestamp ordering
    if "timestamp" in metadata:
        try:
            current_ts = datetime.fromisoformat(metadata["timestamp"].replace('Z', '+00:00'))
            parent_ts = datetime.fromisoformat(parent_timestamp_str.replace('Z', '+00:00'))

            if current_ts <= parent_ts:
                errors.append("Timestamp must be newer than parent timestamp")
                errors.append(f"  Parent: {parent_timestamp_str}")
                errors.append(f"  Current: {metadata['timestamp']}")
                errors.append("RECOMMENDATION: Ensure file is generated after parent")
                return False, errors
        except (ValueError, AttributeError) as e:
            errors.append(f"Invalid timestamp format: {str(e)}")
            return False, errors

    return True, errors


def validate_systems(systems: List[Dict[str, Any]], init_repos: List[str]) -> Tuple[bool, List[str], List[str]]:
    """Validate systems array."""
    errors = []
    warnings = []
    seen_ids = set()

    if not systems:
        errors.append("No systems found (systems array is empty)")
        return False, errors, warnings

    for idx, system in enumerate(systems):
        if not isinstance(system, dict):
            errors.append(f"System at index {idx} is not an object")
            continue

        # Validate required fields
        required_fields = ["id", "name", "type", "repositories", "description", "observations", "relations"]
        for field in required_fields:
            if field not in system:
                errors.append(f"System at index {idx}: Missing required field '{field}'")

        # Validate ID
        if "id" in system:
            system_id = system["id"]

            # Check ID pattern
            if not ID_PATTERN.match(system_id):
                errors.append(f"Invalid system ID format: {system_id} (must match ^[a-z0-9]+(-[a-z0-9]+)*$)")

            # Check for duplicates
            if system_id in seen_ids:
                errors.append(f"Duplicate system ID: {system_id}")
            seen_ids.add(system_id)

        # Validate type
        if "type" in system:
            if system["type"] not in ALLOWED_SYSTEM_TYPES:
                warnings.append(f"Unknown system type: {system['type']} (system: {system.get('id', 'unknown')})")

        # Validate repositories array
        if "repositories" in system:
            repos = system["repositories"]
            if not isinstance(repos, list):
                errors.append(f"System {system.get('id', idx)}: 'repositories' must be an array")
            elif len(repos) == 0:
                errors.append(f"System {system.get('id', idx)}: 'repositories' array is empty")
            else:
                # Check if repositories exist in init.json
                for repo in repos:
                    if repo not in init_repos:
                        warnings.append(f"System {system.get('id', idx)}: Repository '{repo}' not found in init.json")

    return len(errors) == 0, errors, warnings


def validate_observations(systems: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate observations in all systems."""
    errors = []
    warnings = []

    for system in systems:
        if not isinstance(system, dict):
            continue

        system_id = system.get("id", "unknown")
        observations = system.get("observations", [])

        if not isinstance(observations, list):
            errors.append(f"System {system_id}: 'observations' must be an array")
            continue

        seen_obs_ids = set()

        for idx, obs in enumerate(observations):
            if not isinstance(obs, dict):
                errors.append(f"System {system_id}: Observation at index {idx} is not an object")
                continue

            # Validate required fields
            required_fields = ["id", "category", "description"]
            for field in required_fields:
                if field not in obs:
                    errors.append(f"System {system_id}: Observation at index {idx} missing '{field}'")

            # Validate ID uniqueness within system
            if "id" in obs:
                obs_id = obs["id"]
                if obs_id in seen_obs_ids:
                    errors.append(f"System {system_id}: Duplicate observation ID: {obs_id}")
                seen_obs_ids.add(obs_id)

            # Validate category
            if "category" in obs:
                if obs["category"] not in OBSERVATION_CATEGORIES:
                    warnings.append(f"System {system_id}: Unknown observation category: {obs['category']}")

            # Validate severity
            if "severity" in obs:
                if obs["severity"] not in OBSERVATION_SEVERITIES:
                    errors.append(f"System {system_id}: Invalid severity: {obs['severity']}")

            # Validate description length
            if "description" in obs:
                if len(obs["description"]) < 10:
                    warnings.append(f"System {system_id}: Observation '{obs.get('id', idx)}' has short description (< 10 chars)")

    return len(errors) == 0, errors, warnings


def validate_relations(systems: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate relations and graph validity."""
    errors = []
    warnings = []

    # Collect all system IDs for reference validation
    system_ids = {sys.get("id") for sys in systems if isinstance(sys, dict) and "id" in sys}

    # Build adjacency list for circular dependency detection
    graph = {sys_id: [] for sys_id in system_ids}

    for system in systems:
        if not isinstance(system, dict):
            continue

        system_id = system.get("id", "unknown")
        relations = system.get("relations", [])

        if not isinstance(relations, list):
            errors.append(f"System {system_id}: 'relations' must be an array")
            continue

        seen_rel_ids = set()

        for idx, rel in enumerate(relations):
            if not isinstance(rel, dict):
                errors.append(f"System {system_id}: Relation at index {idx} is not an object")
                continue

            # Validate required fields
            required_fields = ["id", "source", "target", "type", "description"]
            for field in required_fields:
                if field not in rel:
                    errors.append(f"System {system_id}: Relation at index {idx} missing '{field}'")

            # Validate ID uniqueness within system
            if "id" in rel:
                rel_id = rel["id"]
                if rel_id in seen_rel_ids:
                    errors.append(f"System {system_id}: Duplicate relation ID: {rel_id}")
                seen_rel_ids.add(rel_id)

            # Validate type
            if "type" in rel:
                if rel["type"] not in RELATION_TYPES:
                    warnings.append(f"System {system_id}: Unknown relation type: {rel['type']}")

            # Validate source and target
            source = rel.get("source")
            target = rel.get("target")

            if source and target:
                # Check for self-references
                if source == target:
                    warnings.append(f"System {system_id}: Self-referencing relation: {rel.get('id', idx)}")

                # Check if source and target exist
                if source not in system_ids:
                    warnings.append(f"System {system_id}: Relation source not found: {source}")
                if target not in system_ids:
                    warnings.append(f"System {system_id}: Relation target not found: {target}")

                # Build graph for circular dependency detection
                if source in graph and target in system_ids:
                    graph[source].append(target)

            # Validate description length
            if "description" in rel:
                if len(rel["description"]) < 10:
                    warnings.append(f"System {system_id}: Relation '{rel.get('id', idx)}' has short description (< 10 chars)")

    # Detect circular dependencies using DFS
    def has_cycle(node: str, visited: Set[str], rec_stack: Set[str], path: List[str]) -> Tuple[bool, List[str]]:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                has_cycle_result, cycle_path = has_cycle(neighbor, visited, rec_stack, path.copy())
                if has_cycle_result:
                    return True, cycle_path
            elif neighbor in rec_stack:
                # Found cycle
                cycle_start = path.index(neighbor)
                return True, path[cycle_start:] + [neighbor]

        rec_stack.remove(node)
        return False, []

    visited = set()
    for node in graph:
        if node not in visited:
            has_cycle_result, cycle_path = has_cycle(node, visited, set(), [])
            if has_cycle_result:
                cycle_str = " → ".join(cycle_path)
                warnings.append(f"Circular dependency detected: {cycle_str}")

    return len(errors) == 0, errors, warnings


def main() -> int:
    """Main validation function."""
    try:
        # Read JSON from stdin
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        error("Invalid JSON", actual=str(e))
        return 2
    except Exception as e:
        error(f"Failed to read input: {str(e)}")
        return 2

    has_errors = False
    has_warnings = False

    # Determine init.json path (assume it's in knowledge-base/ directory)
    # This is a simplification - in real usage, path should be passed as argument
    init_file_path = "knowledge-base/init.json"
    if not os.path.exists(init_file_path):
        # Try alternative path
        init_file_path = os.path.join(os.getcwd(), "knowledge-base", "init.json")

    # 1. Validate parent reference
    valid, errors = validate_parent_reference(data, init_file_path)
    if not valid:
        has_errors = True
        for err in errors:
            error(err) if not err.startswith("RECOMMENDATION:") else warning(err.replace("RECOMMENDATION: ", ""))
        return 2

    # Load init.json to get repository names
    init_repos = []
    try:
        with open(init_file_path, 'r') as f:
            init_data = json.load(f)
            init_repos = [repo.get("name", repo.get("path", ""))
                         for repo in init_data.get("repositories", [])]
    except:
        pass

    # 2. Validate systems
    systems = data.get("systems", [])
    valid, errors, warns = validate_systems(systems, init_repos)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="systems")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 3. Validate observations
    valid, errors, warns = validate_observations(systems)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="observations")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 4. Validate relations
    valid, errors, warns = validate_relations(systems)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="relations")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # Check for empty observations/relations (warning)
    for system in systems:
        if isinstance(system, dict):
            system_id = system.get("id", "unknown")
            if not system.get("observations", []):
                has_warnings = True
                warning(f"System {system_id}: No observations",
                       recommendation="Add observations to document system characteristics")
            if not system.get("relations", []):
                has_warnings = True
                warning(f"System {system_id}: No relations",
                       recommendation="Add relations to document system dependencies")

    # Return appropriate exit code
    if has_errors:
        print("[VALIDATE-C1] FAILED with errors", file=sys.stderr)
        return 2
    elif has_warnings:
        print("[VALIDATE-C1] PASSED with warnings", file=sys.stderr)
        return 1
    else:
        print("[VALIDATE-C1] PASSED", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
