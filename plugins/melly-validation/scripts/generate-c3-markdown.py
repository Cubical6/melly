#!/usr/bin/env python3
"""
Generate C3 (Component) markdown documentation from JSON.

This script ensures CONSISTENT markdown structure by using deterministic
generation instead of AI-based markdown creation.

Usage:
    python generate-c3-markdown.py c3-components.json

Output:
    knowledge-base/systems/{system-id}/c3/{component-id}.md (for each component)
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def group_by_category(observations: List[Dict]) -> Dict[str, List[Dict]]:
    """Group observations by category."""
    grouped = {}
    for obs in observations:
        category = obs.get('category', 'uncategorized')
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(obs)
    return grouped


def generate_frontmatter(component: Dict[str, Any]) -> str:
    """Generate YAML frontmatter - always same structure."""
    return f"""---
id: {component['id']}
title: {component['name']}
level: c3
type: {component.get('type', 'component')}
container: {component.get('container_id', 'unknown')}
generated: auto
---"""


def generate_overview(component: Dict[str, Any]) -> str:
    """Generate overview section - always same structure."""
    overview = [
        f"# {component['name']}",
        "",
        "## Overview",
        "",
        f"**Type**: {component.get('type', 'N/A')}",
        f"**Container**: {component.get('container_id', 'N/A')}",
        f"**Responsibility**: {component.get('responsibility', 'N/A')}",
    ]

    return "\n".join(overview)


def generate_code_structure(component: Dict[str, Any]) -> str:
    """Generate code structure section - always same structure."""
    structure = component.get('structure', {})

    sections = [
        "## Code Structure",
        "",
        f"**Path**: `{structure.get('path', 'N/A')}`",
        f"**Language**: {structure.get('language', 'N/A')}",
    ]

    # Files
    if structure.get('files'):
        sections.append("")
        sections.append("**Files**:")
        sections.append("")

        for file_info in structure['files']:
            path = file_info.get('path', 'N/A')
            lines = file_info.get('lines', 0)
            file_type = file_info.get('type', 'N/A')
            sections.append(f"- `{path}` ({lines} lines, {file_type})")

    # Exports
    if structure.get('exports'):
        sections.append("")
        sections.append("**Exports**:")
        sections.append("")

        for export in structure['exports']:
            name = export.get('name', 'N/A')
            export_type = export.get('type', 'N/A')
            sections.append(f"- `{name}` ({export_type})")

    return "\n".join(sections)


def generate_patterns(component: Dict[str, Any]) -> str:
    """Generate design patterns section - always same structure."""
    patterns = component.get('patterns', [])

    if not patterns:
        return "## Design Patterns\n\nNo patterns identified."

    sections = ["## Design Patterns", ""]

    for pattern in patterns:
        name = pattern.get('name', 'Unknown')
        category = pattern.get('category', 'N/A')
        description = pattern.get('description', 'No description')

        sections.append(f"### {name}")
        sections.append(f"**Category**: {category}")
        sections.append(f"{description}")
        sections.append("")

    return "\n".join(sections)


def generate_metrics(component: Dict[str, Any]) -> str:
    """Generate metrics section - always same structure."""
    metrics = component.get('metrics', {})

    if not metrics:
        return "## Metrics\n\nNo metrics available."

    sections = [
        "## Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Lines of Code | {metrics.get('lines_of_code', 'N/A')} |",
        f"| Cyclomatic Complexity | {metrics.get('cyclomatic_complexity', 'N/A')} |",
        f"| Test Coverage | {metrics.get('test_coverage', 'N/A')}% |",
    ]

    return "\n".join(sections)


def generate_observations(component: Dict[str, Any]) -> str:
    """Generate observations section - always grouped by category."""
    if not component.get('observations'):
        return "## Observations\n\nNo observations documented."

    sections = ["## Observations", ""]
    obs_by_category = group_by_category(component['observations'])

    # Always sort categories alphabetically for consistency
    for category in sorted(obs_by_category.keys()):
        sections.append(f"### {category.replace('-', ' ').title()}")
        sections.append("")

        # Sort by severity
        severity_order = {'critical': 0, 'warning': 1, 'info': 2}
        obs_list = sorted(
            obs_by_category[category],
            key=lambda x: severity_order.get(x.get('severity', 'info'), 3)
        )

        for obs in obs_list:
            severity = obs.get('severity', 'info')
            icon = {'critical': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}.get(severity, '')

            sections.append(f"- {icon} **{obs.get('description', 'No description')}**")

            if obs.get('tags'):
                tags = ' '.join(f"`{tag}`" for tag in obs['tags'])
                sections.append(f"  - Tags: {tags}")

            sections.append("")

    return "\n".join(sections)


def generate_relations(component: Dict[str, Any]) -> str:
    """Generate relations section - always table format."""
    if not component.get('relations'):
        return "## Relations\n\nNo relations documented."

    sections = [
        "## Relations",
        "",
        "| Target | Type | Coupling | Description |",
        "|--------|------|----------|-------------|"
    ]

    for rel in component['relations']:
        target = rel.get('target', 'N/A')
        rel_type = rel.get('type', 'N/A')
        coupling = rel.get('coupling', 'N/A')
        description = rel.get('description', 'N/A')

        sections.append(f"| {target} | `{rel_type}` | {coupling} | {description} |")

    return "\n".join(sections)


def generate_metadata(component: Dict[str, Any], source_file: str) -> str:
    """Generate metadata section - always same structure."""
    return f"""## Metadata

**Source**: {source_file}
**Level**: C3 (Component)
**ID**: `{component['id']}`
**Container**: `{component.get('container_id', 'N/A')}`"""


def generate_c3_markdown(component: Dict[str, Any], source_file: str = "c3-components.json") -> str:
    """
    Generate complete C3 markdown from component JSON.

    ALWAYS generates the same structure - ensures CONSISTENCY.
    """
    sections = [
        generate_frontmatter(component),
        generate_overview(component),
        generate_code_structure(component),
        generate_patterns(component),
        generate_metrics(component),
        generate_observations(component),
        generate_relations(component),
        generate_metadata(component, source_file)
    ]

    return "\n\n".join(sections) + "\n"


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate-c3-markdown.py <c3-components.json>")
        sys.exit(1)

    json_file = sys.argv[1]

    # Load JSON
    try:
        with open(json_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_file}: {e}")
        sys.exit(2)

    # Generate markdown for each component
    components = data.get('components', [])
    if not components:
        print("Warning: No components found in JSON")
        sys.exit(0)

    print(f"Generating markdown for {len(components)} component(s)...")

    for component in components:
        component_id = component.get('id')
        container_id = component.get('container_id')

        if not component_id or not container_id:
            print(f"Warning: Component without ID or container_id, skipping")
            continue

        # Note: We need to know system_id to create correct path
        # This would typically come from reading c2-containers.json first
        # For now, we'll use a placeholder approach
        system_id = "unknown-system"  # TODO: Map container_id to system_id

        # Generate markdown
        markdown = generate_c3_markdown(component, json_file)

        # Write to file
        output_dir = Path(f"knowledge-base/systems/{system_id}/c3")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{component_id}.md"
        output_file.write_text(markdown)

        print(f"✓ Generated: {output_file}")

    print(f"\nDone! Generated {len(components)} markdown file(s)")


if __name__ == "__main__":
    main()
