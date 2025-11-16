#!/usr/bin/env python3
"""
Validate c2-containers.json structure.

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


# ID pattern
ID_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

# Allowed container types
ALLOWED_CONTAINER_TYPES = [
    "web-server", "app-server", "database", "cache", "message-broker",
    "spa", "api", "worker", "file-storage", "web-application", "application-server",
    "spa-client", "mobile-app", "desktop-app"
]

# Allowed environments
ALLOWED_ENVIRONMENTS = ["browser", "server", "cloud", "edge", "mobile"]

# Observation and relation categories (same as C1)
OBSERVATION_CATEGORIES = [
    "architectural", "technical", "quality", "security",
    "performance", "scalability", "maintainability", "integration",
    "deployment", "data", "testing", "documentation", "technology",
    "runtime", "communication", "data-storage", "authentication",
    "configuration", "monitoring", "dependencies"
]

OBSERVATION_SEVERITIES = ["info", "warning", "critical"]

RELATION_TYPES = [
    "http-rest", "http-graphql", "grpc", "websocket",
    "database-connection", "database-query", "database-write", "database-read-write",
    "cache-access", "cache-read", "cache-write", "cache-read-write",
    "message-publish", "message-subscribe", "message-consumer",
    "file-read", "file-write", "cdn-fetch", "stream",
    "dependency", "uses", "calls", "contains"
]


def error(message: str, location: str = "", expected: str = "", actual: str = "") -> None:
    """Print formatted error message to stderr."""
    print(f"[VALIDATE-C2] ERROR: {message}", file=sys.stderr)
    if location:
        print(f"  Location: {location}", file=sys.stderr)
    if expected:
        print(f"  Expected: {expected}", file=sys.stderr)
    if actual:
        print(f"  Actual: {actual}", file=sys.stderr)
    print("", file=sys.stderr)


def warning(message: str, recommendation: str = "") -> None:
    """Print formatted warning message to stderr."""
    print(f"[VALIDATE-C2] WARNING: {message}", file=sys.stderr)
    if recommendation:
        print(f"  Recommendation: {recommendation}", file=sys.stderr)
    print("", file=sys.stderr)


def validate_parent_reference(data: Dict[str, Any], c1_file_path: str) -> Tuple[bool, List[str], str]:
    """Validate parent file reference and return parent timestamp."""
    errors = []

    # Check if c1-systems.json exists
    if not os.path.exists(c1_file_path):
        errors.append(f"Parent file not found: {c1_file_path}")
        errors.append("RECOMMENDATION: Run /melly-c1-systems first")
        return False, errors, ""

    # Load parent file
    try:
        with open(c1_file_path, 'r') as f:
            c1_data = json.load(f)
    except Exception as e:
        errors.append(f"Failed to read parent file: {str(e)}")
        return False, errors, ""

    # Get parent timestamp
    parent_timestamp_str = c1_data.get("metadata", {}).get("timestamp")
    if not parent_timestamp_str:
        errors.append("Parent file missing metadata.timestamp")
        return False, errors, ""

    # Check metadata
    if "metadata" not in data:
        errors.append("Missing metadata field")
        return False, errors, ""

    metadata = data["metadata"]

    # Check timestamp ordering: init < c1 < c2
    if "timestamp" in metadata:
        try:
            current_ts = datetime.fromisoformat(metadata["timestamp"].replace('Z', '+00:00'))
            parent_ts = datetime.fromisoformat(parent_timestamp_str.replace('Z', '+00:00'))

            if current_ts <= parent_ts:
                errors.append("Timestamp must be newer than parent timestamp")
                errors.append(f"  Parent (c1-systems.json): {parent_timestamp_str}")
                errors.append(f"  Current (c2-containers.json): {metadata['timestamp']}")
                return False, errors, ""
        except (ValueError, AttributeError) as e:
            errors.append(f"Invalid timestamp format: {str(e)}")
            return False, errors, ""

    return True, errors, parent_timestamp_str


def validate_containers(containers: List[Dict[str, Any]], c1_system_ids: Set[str]) -> Tuple[bool, List[str], List[str]]:
    """Validate containers array."""
    errors = []
    warnings = []
    seen_ids = set()

    if not containers:
        errors.append("No containers found (containers array is empty)")
        return False, errors, warnings

    for idx, container in enumerate(containers):
        if not isinstance(container, dict):
            errors.append(f"Container at index {idx} is not an object")
            continue

        # Validate required fields
        required_fields = ["id", "name", "type", "system_id", "responsibility", "technology", "runtime"]
        for field in required_fields:
            if field not in container:
                errors.append(f"Container at index {idx}: Missing required field '{field}'")

        # Validate ID
        if "id" in container:
            container_id = container["id"]

            # Check ID pattern
            if not ID_PATTERN.match(container_id):
                errors.append(f"Invalid container ID format: {container_id}")

            # Check for duplicates
            if container_id in seen_ids:
                errors.append(f"Duplicate container ID: {container_id}")
            seen_ids.add(container_id)

        # Validate type
        if "type" in container:
            if container["type"] not in ALLOWED_CONTAINER_TYPES:
                warnings.append(f"Unknown container type: {container['type']} (container: {container.get('id', 'unknown')})")

        # Validate system_id (must reference valid C1 system)
        if "system_id" in container:
            system_id = container["system_id"]
            if system_id not in c1_system_ids:
                errors.append(f"Container {container.get('id', idx)}: System not found: {system_id}")
                errors.append(f"  Available systems: {', '.join(sorted(c1_system_ids))}")

        # Validate technology
        if "technology" in container:
            tech = container["technology"]
            if not isinstance(tech, dict):
                errors.append(f"Container {container.get('id', idx)}: 'technology' must be an object")
            else:
                if "primary_language" not in tech:
                    errors.append(f"Container {container.get('id', idx)}: Missing 'technology.primary_language'")
                if "framework" not in tech:
                    errors.append(f"Container {container.get('id', idx)}: Missing 'technology.framework'")

        # Validate runtime
        if "runtime" in container:
            runtime = container["runtime"]
            if not isinstance(runtime, dict):
                errors.append(f"Container {container.get('id', idx)}: 'runtime' must be an object")
            else:
                if "environment" not in runtime:
                    errors.append(f"Container {container.get('id', idx)}: Missing 'runtime.environment'")
                elif runtime["environment"] not in ALLOWED_ENVIRONMENTS:
                    warnings.append(f"Container {container.get('id', idx)}: Unknown environment: {runtime['environment']}")

                if "platform" not in runtime:
                    errors.append(f"Container {container.get('id', idx)}: Missing 'runtime.platform'")

                if "containerized" not in runtime:
                    errors.append(f"Container {container.get('id', idx)}: Missing 'runtime.containerized'")
                elif runtime["containerized"] and "container_technology" not in runtime:
                    errors.append(f"Container {container.get('id', idx)}: Missing 'runtime.container_technology' (required when containerized=true)")

    return len(errors) == 0, errors, warnings


def validate_observations(containers: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate observations in all containers."""
    errors = []
    warnings = []

    for container in containers:
        if not isinstance(container, dict):
            continue

        container_id = container.get("id", "unknown")
        observations = container.get("observations", [])

        if not isinstance(observations, list):
            errors.append(f"Container {container_id}: 'observations' must be an array")
            continue

        seen_obs_ids = set()

        for idx, obs in enumerate(observations):
            if not isinstance(obs, dict):
                errors.append(f"Container {container_id}: Observation at index {idx} is not an object")
                continue

            # Validate required fields
            required_fields = ["id", "category", "description"]
            for field in required_fields:
                if field not in obs:
                    errors.append(f"Container {container_id}: Observation at index {idx} missing '{field}'")

            # Validate ID uniqueness
            if "id" in obs:
                obs_id = obs["id"]
                if obs_id in seen_obs_ids:
                    errors.append(f"Container {container_id}: Duplicate observation ID: {obs_id}")
                seen_obs_ids.add(obs_id)

            # Validate category
            if "category" in obs:
                if obs["category"] not in OBSERVATION_CATEGORIES:
                    warnings.append(f"Container {container_id}: Unknown observation category: {obs['category']}")

            # Validate severity
            if "severity" in obs:
                if obs["severity"] not in OBSERVATION_SEVERITIES:
                    errors.append(f"Container {container_id}: Invalid severity: {obs['severity']}")

            # Validate description length
            if "description" in obs:
                if len(obs["description"]) < 10:
                    warnings.append(f"Container {container_id}: Observation '{obs.get('id', idx)}' has short description")

    return len(errors) == 0, errors, warnings


def validate_relations(containers: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate relations between containers."""
    errors = []
    warnings = []

    # Collect all container IDs
    container_ids = {c.get("id") for c in containers if isinstance(c, dict) and "id" in c}

    for container in containers:
        if not isinstance(container, dict):
            continue

        container_id = container.get("id", "unknown")
        relations = container.get("relations", [])

        if not isinstance(relations, list):
            errors.append(f"Container {container_id}: 'relations' must be an array")
            continue

        seen_rel_ids = set()

        for idx, rel in enumerate(relations):
            if not isinstance(rel, dict):
                errors.append(f"Container {container_id}: Relation at index {idx} is not an object")
                continue

            # Validate required fields
            required_fields = ["target", "type", "description"]
            for field in required_fields:
                if field not in rel:
                    errors.append(f"Container {container_id}: Relation at index {idx} missing '{field}'")

            # Validate type
            if "type" in rel:
                if rel["type"] not in RELATION_TYPES:
                    warnings.append(f"Container {container_id}: Unknown relation type: {rel['type']}")

            # Validate target
            if "target" in rel:
                target = rel["target"]
                if target not in container_ids:
                    warnings.append(f"Container {container_id}: Relation target not found: {target}")

            # Validate description length
            if "description" in rel:
                if len(rel["description"]) < 10:
                    warnings.append(f"Container {container_id}: Relation has short description")

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

    # Determine c1-systems.json path
    c1_file_path = "knowledge-base/c1-systems.json"
    if not os.path.exists(c1_file_path):
        c1_file_path = os.path.join(os.getcwd(), "knowledge-base", "c1-systems.json")

    # 1. Validate parent reference
    valid, errors, parent_ts = validate_parent_reference(data, c1_file_path)
    if not valid:
        has_errors = True
        for err in errors:
            if err.startswith("RECOMMENDATION:"):
                warning(err.replace("RECOMMENDATION: ", ""))
            else:
                error(err)
        return 2

    # Load c1-systems.json to get system IDs
    c1_system_ids = set()
    try:
        with open(c1_file_path, 'r') as f:
            c1_data = json.load(f)
            c1_system_ids = {sys.get("id") for sys in c1_data.get("systems", []) if isinstance(sys, dict) and "id" in sys}
    except:
        pass

    # 2. Validate containers
    containers = data.get("containers", [])
    valid, errors, warns = validate_containers(containers, c1_system_ids)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="containers")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 3. Validate observations
    valid, errors, warns = validate_observations(containers)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="observations")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 4. Validate relations
    valid, errors, warns = validate_relations(containers)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="relations")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # Check for systems with no containers (warning)
    containers_by_system = {}
    for container in containers:
        if isinstance(container, dict):
            system_id = container.get("system_id")
            if system_id:
                containers_by_system.setdefault(system_id, []).append(container.get("id"))

    for sys_id in c1_system_ids:
        if sys_id not in containers_by_system:
            has_warnings = True
            warning(f"System '{sys_id}' has no containers")

    # Return appropriate exit code
    if has_errors:
        print("[VALIDATE-C2] FAILED with errors", file=sys.stderr)
        return 2
    elif has_warnings:
        print("[VALIDATE-C2] PASSED with warnings", file=sys.stderr)
        return 1
    else:
        print("[VALIDATE-C2] PASSED", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
