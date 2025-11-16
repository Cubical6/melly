#!/usr/bin/env python3
"""
Generate C1 (System Context) markdown documentation from JSON.

This script ensures CONSISTENT markdown structure by using deterministic
generation instead of AI-based markdown creation.

Usage:
    python generate-c1-markdown.py c1-systems.json

Output:
    knowledge-base/systems/{system-id}/c1/README.md (for each system)
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


def generate_frontmatter(system: Dict[str, Any]) -> str:
    """Generate YAML frontmatter - always same structure."""
    return f"""---
id: {system['id']}
title: {system['name']}
level: c1
type: {system.get('type', 'system')}
generated: auto
---"""


def generate_overview(system: Dict[str, Any]) -> str:
    """Generate overview section - always same structure."""
    overview = [
        f"# {system['name']}",
        "",
        "## Overview",
        "",
        f"**Type**: {system.get('type', 'N/A')}",
        f"**Scope**: {system.get('boundaries', {}).get('scope', 'N/A')}",
    ]

    if system.get('repositories'):
        overview.append("")
        overview.append("**Repositories**:")
        for repo in system['repositories']:
            overview.append(f"- `{repo}`")

    return "\n".join(overview)


def generate_observations(system: Dict[str, Any]) -> str:
    """Generate observations section - always grouped by category."""
    if not system.get('observations'):
        return "## Observations\n\nNo observations documented."

    sections = ["## Observations", ""]
    obs_by_category = group_by_category(system['observations'])

    # Always sort categories alphabetically for consistency
    for category in sorted(obs_by_category.keys()):
        sections.append(f"### {category.replace('-', ' ').title()}")
        sections.append("")

        # Sort by severity: critical > warning > info
        severity_order = {'critical': 0, 'warning': 1, 'info': 2}
        obs_list = sorted(
            obs_by_category[category],
            key=lambda x: severity_order.get(x.get('severity', 'info'), 3)
        )

        for obs in obs_list:
            severity = obs.get('severity', 'info')
            icon = {'critical': '🔴', 'warning': '⚠️', 'info': 'ℹ️'}.get(severity, '')

            sections.append(f"- {icon} **{obs.get('description', 'No description')}**")

            # Add evidence if present
            if obs.get('evidence'):
                ev = obs['evidence']
                sections.append(f"  - Evidence: `{ev.get('location', 'N/A')}`")
                if ev.get('snippet'):
                    sections.append(f"  ```{ev.get('type', 'text')}")
                    sections.append(f"  {ev['snippet']}")
                    sections.append(f"  ```")

            # Add tags if present
            if obs.get('tags'):
                tags = ' '.join(f"`{tag}`" for tag in obs['tags'])
                sections.append(f"  - Tags: {tags}")

            sections.append("")

    return "\n".join(sections)


def generate_relations(system: Dict[str, Any]) -> str:
    """Generate relations section - always table format."""
    if not system.get('relations'):
        return "## Relations\n\nNo relations documented."

    sections = [
        "## Relations",
        "",
        "| Target | Type | Direction | Description |",
        "|--------|------|-----------|-------------|"
    ]

    for rel in system['relations']:
        target = rel.get('target', 'N/A')
        rel_type = rel.get('type', 'N/A')
        direction = rel.get('direction', 'N/A')
        description = rel.get('description', 'N/A')

        sections.append(f"| {target} | `{rel_type}` | {direction} | {description} |")

    return "\n".join(sections)


def generate_metadata(system: Dict[str, Any], source_file: str) -> str:
    """Generate metadata section - always same structure."""
    return f"""## Metadata

**Source**: {source_file}
**Level**: C1 (System Context)
**ID**: `{system['id']}`"""


def generate_c1_markdown(system: Dict[str, Any], source_file: str = "c1-systems.json") -> str:
    """
    Generate complete C1 markdown from system JSON.

    ALWAYS generates the same structure:
    1. Frontmatter
    2. Overview
    3. Observations (grouped by category, sorted by severity)
    4. Relations (table format)
    5. Metadata

    This ensures CONSISTENCY - no duplicate sections, no random ordering.
    """
    sections = [
        generate_frontmatter(system),
        generate_overview(system),
        generate_observations(system),
        generate_relations(system),
        generate_metadata(system, source_file)
    ]

    return "\n\n".join(sections) + "\n"


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate-c1-markdown.py <c1-systems.json>")
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

    # Generate markdown for each system
    systems = data.get('systems', [])
    if not systems:
        print("Warning: No systems found in JSON")
        sys.exit(0)

    print(f"Generating markdown for {len(systems)} system(s)...")

    for system in systems:
        system_id = system.get('id')
        if not system_id:
            print(f"Warning: System without ID, skipping")
            continue

        # Generate markdown
        markdown = generate_c1_markdown(system, json_file)

        # Write to file
        output_dir = Path(f"knowledge-base/systems/{system_id}/c1")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "README.md"
        output_file.write_text(markdown)

        print(f"✓ Generated: {output_file}")

    print(f"\nDone! Generated {len(systems)} markdown file(s)")


if __name__ == "__main__":
    main()
