#!/usr/bin/env python3
"""
Detect the correct basic-memory project root for storing generated documentation.

Priority order:
1. ~/.basic-memory/config.json (if exists)
2. BASIC_MEMORY_PROJECT_ROOT environment variable
3. ${CLAUDE_PROJECT_DIR}/knowledge-base (fallback)

Handles single-project auto-selection and multi-project user prompts.
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


def expand_path(path: str) -> Path:
    """Expand ~ and environment variables in path."""
    expanded = os.path.expandvars(os.path.expanduser(path))
    return Path(expanded).resolve()


def read_basic_memory_config() -> Optional[Dict]:
    """Read ~/.basic-memory/config.json if it exists."""
    config_path = Path.home() / ".basic-memory" / "config.json"

    if not config_path.exists():
        return None

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read {config_path}: {e}", file=sys.stderr)
        return None


def get_project_root_from_config(config: Dict) -> Tuple[Optional[Path], Optional[str]]:
    """
    Extract project root from config.

    Returns:
        (project_path, project_name) tuple or (None, None) if not found
    """
    projects = config.get('projects', {})

    if not projects:
        return None, None

    # Single project - use it automatically
    if len(projects) == 1:
        project_name = list(projects.keys())[0]
        project_path = expand_path(projects[project_name])
        return project_path, project_name

    # Multiple projects - check for default or prompt user
    default_project = config.get('default_project')
    default_mode = config.get('default_project_mode', False)

    if default_mode and default_project and default_project in projects:
        project_path = expand_path(projects[default_project])
        return project_path, default_project

    # Multiple projects without clear default - return list for user prompt
    return None, None


def get_project_root_from_env() -> Optional[Path]:
    """Get project root from BASIC_MEMORY_PROJECT_ROOT environment variable."""
    project_root = os.getenv('BASIC_MEMORY_PROJECT_ROOT')

    if project_root:
        return expand_path(project_root)

    return None


def get_fallback_project_root() -> Path:
    """
    Fallback: use knowledge-base in current working directory or git root.
    """
    # Try git root first
    try:
        import subprocess
        git_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return Path(git_root) / "knowledge-base"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback to current directory
    return Path.cwd() / "knowledge-base"


def get_project_root(interactive: bool = True) -> Tuple[Path, Optional[str]]:
    """
    Get the basic-memory project root path.

    Args:
        interactive: If True, prompt user when multiple projects exist

    Returns:
        (project_path, project_name) tuple
    """
    # Priority 1: ~/.basic-memory/config.json
    config = read_basic_memory_config()
    if config:
        project_path, project_name = get_project_root_from_config(config)

        if project_path:
            return project_path, project_name

        # Multiple projects detected - check if we should prompt
        projects = config.get('projects', {})
        if len(projects) > 1 and interactive:
            print("\nMultiple basic-memory projects found:", file=sys.stderr)
            for idx, (name, path) in enumerate(projects.items(), 1):
                print(f"  {idx}. {name}: {path}", file=sys.stderr)
            print("\nPlease specify which project to use via --project flag", file=sys.stderr)
            print("Example: --project main", file=sys.stderr)
            sys.exit(1)

    # Priority 2: BASIC_MEMORY_PROJECT_ROOT environment variable
    env_path = get_project_root_from_env()
    if env_path:
        return env_path, "main"

    # Priority 3: Fallback to knowledge-base in current directory
    fallback_path = get_fallback_project_root()
    return fallback_path, "main"


def main():
    """CLI interface for getting project root."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Get basic-memory project root path"
    )
    parser.add_argument(
        '--project',
        help='Specific project name to use (when multiple exist)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available projects'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only output the path, no additional info'
    )

    args = parser.parse_args()

    # List projects mode
    if args.list:
        config = read_basic_memory_config()
        if config and 'projects' in config:
            projects = config['projects']
            for name, path in projects.items():
                print(f"{name}: {expand_path(path)}")
        else:
            print("No projects configured in ~/.basic-memory/config.json", file=sys.stderr)
            fallback = get_fallback_project_root()
            print(f"Using fallback: {fallback}", file=sys.stderr)
        return

    # Specific project requested
    if args.project:
        config = read_basic_memory_config()
        if config and 'projects' in config:
            projects = config['projects']
            if args.project in projects:
                project_path = expand_path(projects[args.project])
                print(project_path)
                return
            else:
                print(f"Error: Project '{args.project}' not found", file=sys.stderr)
                print(f"Available: {', '.join(projects.keys())}", file=sys.stderr)
                sys.exit(1)

    # Auto-detect project
    try:
        project_path, project_name = get_project_root(interactive=True)

        if not args.quiet:
            print(f"# Using project: {project_name}", file=sys.stderr)
            print(f"# Project root: {project_path}", file=sys.stderr)

        print(project_path)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
