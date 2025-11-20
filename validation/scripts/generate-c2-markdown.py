#!/usr/bin/env python3
"""
Generate C2 (Container) markdown documentation from JSON.

This script ensures CONSISTENT markdown structure by using deterministic
generation instead of AI-based markdown creation.

Usage:
    python generate-c2-markdown.py c2-containers.json [--project PROJECT_NAME]

Output:
    {project-root}/systems/{system-id}/c2/{container-id}.md (for each container)
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Import project root detection
sys.path.insert(0, str(Path(__file__).parent.resolve()))
try:
    from get_project_root import get_project_root
except ImportError:
    # Fallback if import fails
    def get_project_root(interactive=False):
        """Fallback: use knowledge-base in git root or cwd"""
        try:
            import subprocess
            git_root = subprocess.check_output(
                ['git', 'rev-parse', '--show-toplevel'],
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            return Path(git_root) / "knowledge-base", "main"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return Path.cwd() / "knowledge-base", "main"


def group_by_category(observations: List[Dict]) -> Dict[str, List[Dict]]:
    """Group observations by category."""
    grouped = {}
    for obs in observations:
        category = obs.get('category', 'uncategorized')
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(obs)
    return grouped


def generate_frontmatter(container: Dict[str, Any]) -> str:
    """Generate YAML frontmatter - always same structure."""
    return f"""---
id: {container['id']}
title: {container['name']}
level: c2
type: {container.get('type', 'container')}
system: {container.get('system_id', 'unknown')}
generated: auto
---"""


def generate_overview(container: Dict[str, Any]) -> str:
    """Generate overview section - always same structure."""
    overview = [
        f"# {container['name']}",
        "",
        "## Overview",
        "",
        f"**Type**: {container.get('type', 'N/A')}",
        f"**System**: {container.get('system_id', 'N/A')}",
        f"**Responsibility**: {container.get('responsibility', 'N/A')}",
    ]

    return "\n".join(overview)


def generate_technology_stack(container: Dict[str, Any]) -> str:
    """Generate technology stack section - always same structure."""
    tech = container.get('technology', {})

    sections = [
        "## Technology Stack",
        "",
        f"**Primary Language**: {tech.get('primary_language', 'N/A')}",
        f"**Framework**: {tech.get('framework', 'N/A')}",
    ]

    # Libraries
    if tech.get('libraries'):
        sections.append("")
        sections.append("**Libraries**:")
        sections.append("")
        sections.append("| Name | Version | Purpose |")
        sections.append("|------|---------|---------|")

        for lib in tech['libraries']:
            name = lib.get('name', 'N/A')
            version = lib.get('version', 'N/A')
            purpose = lib.get('purpose', 'N/A')
            sections.append(f"| {name} | {version} | {purpose} |")

    return "\n".join(sections)


def generate_runtime(container: Dict[str, Any]) -> str:
    """Generate runtime section - always same structure."""
    runtime = container.get('runtime', {})

    sections = [
        "## Runtime Environment",
        "",
        f"**Environment**: {runtime.get('environment', 'N/A')}",
        f"**Platform**: {runtime.get('platform', 'N/A')}",
        f"**Containerized**: {runtime.get('containerized', False)}",
    ]

    if runtime.get('containerized'):
        sections.append(f"**Container Technology**: {runtime.get('container_technology', 'N/A')}")

    return "\n".join(sections)


def generate_observations(container: Dict[str, Any]) -> str:
    """Generate observations section - always grouped by category."""
    if not container.get('observations'):
        return "## Observations\n\nNo observations documented."

    sections = ["## Observations", ""]
    obs_by_category = group_by_category(container['observations'])

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

            if obs.get('evidence'):
                ev = obs['evidence']
                sections.append(f"  - Evidence: `{ev.get('location', 'N/A')}`")

            if obs.get('tags'):
                tags = ' '.join(f"`{tag}`" for tag in obs['tags'])
                sections.append(f"  - Tags: {tags}")

            sections.append("")

    return "\n".join(sections)


def generate_relations(container: Dict[str, Any]) -> str:
    """Generate relations section - always table format."""
    if not container.get('relations'):
        return "## Relations\n\nNo relations documented."

    sections = [
        "## Relations",
        "",
        "| Target | Type | Description |",
        "|--------|------|-------------|"
    ]

    for rel in container['relations']:
        target = rel.get('target', 'N/A')
        rel_type = rel.get('type', 'N/A')
        description = rel.get('description', 'N/A')

        sections.append(f"| {target} | `{rel_type}` | {description} |")

    return "\n".join(sections)


def generate_metadata(container: Dict[str, Any], source_file: str) -> str:
    """Generate metadata section - always same structure."""
    return f"""## Metadata

**Source**: {source_file}
**Level**: C2 (Container)
**ID**: `{container['id']}`
**System**: `{container.get('system_id', 'N/A')}`"""


def generate_c2_markdown(container: Dict[str, Any], source_file: str = "c2-containers.json") -> str:
    """
    Generate complete C2 markdown from container JSON.

    ALWAYS generates the same structure - ensures CONSISTENCY.
    """
    sections = [
        generate_frontmatter(container),
        generate_overview(container),
        generate_technology_stack(container),
        generate_runtime(container),
        generate_observations(container),
        generate_relations(container),
        generate_metadata(container, source_file)
    ]

    return "\n\n".join(sections) + "\n"


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate C2 markdown documentation from JSON'
    )
    parser.add_argument('json_file', help='Input JSON file (c2-containers.json)')
    parser.add_argument(
        '--project',
        help='Specific basic-memory project to use (if multiple exist)'
    )

    args = parser.parse_args()
    json_file = args.json_file

    # Detect project root
    try:
        if args.project:
            # User specified project - use get_project_root.py CLI
            import subprocess
            result = subprocess.run(
                [sys.executable, Path(__file__).parent / "get-project-root.py",
                 "--project", args.project, "--quiet"],
                capture_output=True,
                text=True,
                check=True
            )
            project_root = Path(result.stdout.strip())
            project_name = args.project
        else:
            # Auto-detect project
            project_root, project_name = get_project_root(interactive=False)

        print(f"Using project: {project_name}")
        print(f"Project root: {project_root}")
        print()
    except Exception as e:
        print(f"Error detecting project root: {e}", file=sys.stderr)
        print("Falling back to: ./knowledge-base", file=sys.stderr)
        project_root = Path("knowledge-base")
        project_name = "default"

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

    # Generate markdown for each container
    containers = data.get('containers', [])
    if not containers:
        print("Warning: No containers found in JSON")
        sys.exit(0)

    print(f"Generating markdown for {len(containers)} container(s)...")

    for container in containers:
        container_id = container.get('id')
        system_id = container.get('system_id')

        if not container_id or not system_id:
            print("Warning: Container without ID or system_id, skipping")
            continue

        # Generate markdown
        markdown = generate_c2_markdown(container, json_file)

        # Write to file using detected project root
        output_dir = project_root / "systems" / system_id / "c2"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{container_id}.md"
        output_file.write_text(markdown)

        print(f"✓ Generated: {output_file}")

    print(f"\nDone! Generated {len(containers)} markdown file(s)")


if __name__ == "__main__":
    main()
