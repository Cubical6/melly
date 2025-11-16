#!/usr/bin/env python3
"""
Validate c3-components.json structure.

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

# Allowed component types
ALLOWED_COMPONENT_TYPES = [
    "service", "controller", "repository", "model", "utility",
    "middleware", "view", "component", "config", "facade",
    "factory", "adapter"
]

# Observation categories
OBSERVATION_CATEGORIES = [
    "design-patterns", "code-quality", "dependencies", "testing",
    "complexity", "maintainability", "code-structure", "error-handling",
    "performance", "security", "documentation", "coupling", "cohesion"
]

OBSERVATION_SEVERITIES = ["info", "warning", "critical"]

# Relation types
RELATION_TYPES = [
    "dependency", "interface-implementation", "event-publisher", "event-subscriber",
    "uses", "calls", "imports", "injects", "observes", "delegates",
    "provides", "consumes", "inherits", "implements", "composes",
    "aggregates", "notifies", "extends"
]

# Coupling types
COUPLING_TYPES = ["loose", "tight"]


def error(message: str, location: str = "", expected: str = "", actual: str = "") -> None:
    """Print formatted error message to stderr."""
    print(f"[VALIDATE-C3] ERROR: {message}", file=sys.stderr)
    if location:
        print(f"  Location: {location}", file=sys.stderr)
    if expected:
        print(f"  Expected: {expected}", file=sys.stderr)
    if actual:
        print(f"  Actual: {actual}", file=sys.stderr)
    print("", file=sys.stderr)


def warning(message: str, recommendation: str = "") -> None:
    """Print formatted warning message to stderr."""
    print(f"[VALIDATE-C3] WARNING: {message}", file=sys.stderr)
    if recommendation:
        print(f"  Recommendation: {recommendation}", file=sys.stderr)
    print("", file=sys.stderr)


def validate_parent_reference(data: Dict[str, Any], c2_file_path: str) -> Tuple[bool, List[str]]:
    """Validate parent file reference."""
    errors = []

    # Check if c2-containers.json exists
    if not os.path.exists(c2_file_path):
        errors.append(f"Parent file not found: {c2_file_path}")
        errors.append("RECOMMENDATION: Run /melly-c2-containers first")
        return False, errors

    # Load parent file
    try:
        with open(c2_file_path, 'r') as f:
            c2_data = json.load(f)
    except Exception as e:
        errors.append(f"Failed to read parent file: {str(e)}")
        return False, errors

    # Get parent timestamp
    parent_timestamp_str = c2_data.get("metadata", {}).get("timestamp")
    if not parent_timestamp_str:
        errors.append("Parent file missing metadata.timestamp")
        return False, errors

    # Check metadata
    if "metadata" not in data:
        errors.append("Missing metadata field")
        return False, errors

    metadata = data["metadata"]

    # Check timestamp ordering: init < c1 < c2 < c3
    if "timestamp" in metadata:
        try:
            current_ts = datetime.fromisoformat(metadata["timestamp"].replace('Z', '+00:00'))
            parent_ts = datetime.fromisoformat(parent_timestamp_str.replace('Z', '+00:00'))

            if current_ts <= parent_ts:
                errors.append("Timestamp must be newer than parent timestamp")
                errors.append(f"  Parent (c2-containers.json): {parent_timestamp_str}")
                errors.append(f"  Current (c3-components.json): {metadata['timestamp']}")
                return False, errors
        except (ValueError, AttributeError) as e:
            errors.append(f"Invalid timestamp format: {str(e)}")
            return False, errors

    return True, errors


def validate_components(components: List[Dict[str, Any]], c2_container_ids: Set[str]) -> Tuple[bool, List[str], List[str]]:
    """Validate components array."""
    errors = []
    warnings = []
    seen_ids = set()

    if not components:
        errors.append("No components found (components array is empty)")
        return False, errors, warnings

    for idx, component in enumerate(components):
        if not isinstance(component, dict):
            errors.append(f"Component at index {idx} is not an object")
            continue

        # Validate required fields
        required_fields = ["id", "name", "type", "container_id", "responsibility", "structure"]
        for field in required_fields:
            if field not in component:
                errors.append(f"Component at index {idx}: Missing required field '{field}'")

        # Validate ID
        if "id" in component:
            component_id = component["id"]

            # Check ID pattern
            if not ID_PATTERN.match(component_id):
                errors.append(f"Invalid component ID format: {component_id}")

            # Check for duplicates
            if component_id in seen_ids:
                errors.append(f"Duplicate component ID: {component_id}")
            seen_ids.add(component_id)

        # Validate type
        if "type" in component:
            if component["type"] not in ALLOWED_COMPONENT_TYPES:
                warnings.append(f"Unknown component type: {component['type']} (component: {component.get('id', 'unknown')})")

        # Validate container_id (must reference valid C2 container)
        if "container_id" in component:
            container_id = component["container_id"]
            if container_id not in c2_container_ids:
                errors.append(f"Component {component.get('id', idx)}: Container not found: {container_id}")
                errors.append(f"  Available containers: {', '.join(sorted(c2_container_ids))}")

        # Validate structure
        if "structure" in component:
            struct = component["structure"]
            if not isinstance(struct, dict):
                errors.append(f"Component {component.get('id', idx)}: 'structure' must be an object")
            else:
                if "path" not in struct:
                    errors.append(f"Component {component.get('id', idx)}: Missing 'structure.path'")
                if "language" not in struct:
                    errors.append(f"Component {component.get('id', idx)}: Missing 'structure.language'")

                # Check for empty files array (warning)
                if "files" in struct and isinstance(struct["files"], list) and len(struct["files"]) == 0:
                    warnings.append(f"Component {component.get('id', idx)}: Empty 'files' array")

    return len(errors) == 0, errors, warnings


def validate_observations(components: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate observations in all components."""
    errors = []
    warnings = []

    for component in components:
        if not isinstance(component, dict):
            continue

        component_id = component.get("id", "unknown")
        observations = component.get("observations", [])

        if not isinstance(observations, list):
            errors.append(f"Component {component_id}: 'observations' must be an array")
            continue

        seen_obs_ids = set()

        for idx, obs in enumerate(observations):
            if not isinstance(obs, dict):
                errors.append(f"Component {component_id}: Observation at index {idx} is not an object")
                continue

            # Validate required fields
            required_fields = ["id", "category", "description"]
            for field in required_fields:
                if field not in obs:
                    errors.append(f"Component {component_id}: Observation at index {idx} missing '{field}'")

            # Validate ID uniqueness
            if "id" in obs:
                obs_id = obs["id"]
                if obs_id in seen_obs_ids:
                    errors.append(f"Component {component_id}: Duplicate observation ID: {obs_id}")
                seen_obs_ids.add(obs_id)

            # Validate category
            if "category" in obs:
                if obs["category"] not in OBSERVATION_CATEGORIES:
                    warnings.append(f"Component {component_id}: Unknown observation category: {obs['category']}")

            # Validate severity
            if "severity" in obs:
                if obs["severity"] not in OBSERVATION_SEVERITIES:
                    errors.append(f"Component {component_id}: Invalid severity: {obs['severity']}")

            # Validate description length
            if "description" in obs:
                if len(obs["description"]) < 10:
                    warnings.append(f"Component {component_id}: Observation '{obs.get('id', idx)}' has short description")

    return len(errors) == 0, errors, warnings


def validate_relations(components: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
    """Validate relations and coupling analysis."""
    errors = []
    warnings = []

    # Collect all component IDs
    component_ids = {c.get("id") for c in components if isinstance(c, dict) and "id" in c}

    # Track tight coupling and total relations
    tight_coupling_count = 0
    total_relations = 0

    for component in components:
        if not isinstance(component, dict):
            continue

        component_id = component.get("id", "unknown")
        relations = component.get("relations", [])

        if not isinstance(relations, list):
            errors.append(f"Component {component_id}: 'relations' must be an array")
            continue

        seen_rel_ids = set()

        for idx, rel in enumerate(relations):
            total_relations += 1

            if not isinstance(rel, dict):
                errors.append(f"Component {component_id}: Relation at index {idx} is not an object")
                continue

            # Validate required fields
            required_fields = ["target", "type", "coupling", "description"]
            for field in required_fields:
                if field not in rel:
                    errors.append(f"Component {component_id}: Relation at index {idx} missing '{field}'")

            # Validate type
            if "type" in rel:
                if rel["type"] not in RELATION_TYPES:
                    warnings.append(f"Component {component_id}: Unknown relation type: {rel['type']}")

            # Validate coupling
            if "coupling" in rel:
                if rel["coupling"] not in COUPLING_TYPES:
                    errors.append(f"Component {component_id}: Invalid coupling: {rel['coupling']} (must be 'loose' or 'tight')")
                elif rel["coupling"] == "tight":
                    tight_coupling_count += 1

            # Validate target
            if "target" in rel:
                target = rel["target"]
                if target not in component_ids:
                    warnings.append(f"Component {component_id}: Relation target not found: {target}")

            # Validate description length
            if "description" in rel:
                if len(rel["description"]) < 10:
                    warnings.append(f"Component {component_id}: Relation has short description")

    # Warn about high tight coupling (based on total relations, not component count)
    if total_relations > 0 and tight_coupling_count > total_relations * 0.3:  # > 30% tight coupling
        warnings.append(f"High tight coupling detected: {tight_coupling_count}/{total_relations} relations are tightly coupled (code smell)")

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

    # Determine c2-containers.json path
    c2_file_path = "knowledge-base/c2-containers.json"
    if not os.path.exists(c2_file_path):
        c2_file_path = os.path.join(os.getcwd(), "knowledge-base", "c2-containers.json")

    # 1. Validate parent reference
    valid, errors = validate_parent_reference(data, c2_file_path)
    if not valid:
        has_errors = True
        for err in errors:
            if err.startswith("RECOMMENDATION:"):
                warning(err.replace("RECOMMENDATION: ", ""))
            else:
                error(err)
        return 2

    # Load c2-containers.json to get container IDs
    c2_container_ids = set()
    try:
        with open(c2_file_path, 'r') as f:
            c2_data = json.load(f)
            c2_container_ids = {c.get("id") for c in c2_data.get("containers", []) if isinstance(c, dict) and "id" in c}
    except (OSError, json.JSONDecodeError):
        # Silent failure is acceptable here - we already validated parent file exists above
        # If we can't load it, validation will fail later when checking component references
        pass

    # 2. Validate components
    components = data.get("components", [])
    valid, errors, warns = validate_components(components, c2_container_ids)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="components")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 3. Validate observations
    valid, errors, warns = validate_observations(components)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="observations")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # 4. Validate relations
    valid, errors, warns = validate_relations(components)
    if not valid:
        has_errors = True
        for err in errors:
            error(err, location="relations")
    for warn in warns:
        has_warnings = True
        warning(warn)

    # Check for containers with no components (warning)
    components_by_container = {}
    for component in components:
        if isinstance(component, dict):
            container_id = component.get("container_id")
            if container_id:
                components_by_container.setdefault(container_id, []).append(component.get("id"))

    for container_id in c2_container_ids:
        if container_id not in components_by_container:
            has_warnings = True
            warning(f"Container '{container_id}' has no components")

    # Return appropriate exit code
    if has_errors:
        print("[VALIDATE-C3] FAILED with errors", file=sys.stderr)
        return 2
    elif has_warnings:
        print("[VALIDATE-C3] PASSED with warnings", file=sys.stderr)
        return 1
    else:
        print("[VALIDATE-C3] PASSED", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
