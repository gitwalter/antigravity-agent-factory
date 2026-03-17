#!/usr/bin/env python
"""
Script Registry Sync — Introspects CLI scripts and syncs signatures to Memory MCP.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/maintenance/sync/sync_script_registry.py
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/maintenance/sync/sync_script_registry.py --dry-run

Purpose:
    Scans targeted directories for Python CLI scripts with argparse,
    introspects them via --help, and syncs the output to Memory MCP
    as 'script_usage' entities. This keeps skills and memory MCP
    always current with actual script interfaces.
"""

import argparse
import json
import os
import subprocess
import sys

# Directories to scan for CLI scripts
# We use relative paths from PROJECT_ROOT
SCAN_DIRS = [
    "scripts/ai/rag",
    "scripts/maintenance/sync",
    "scripts/validation",
    "scripts/git",
    ".agent/skills/routing/managing-plane-tasks/scripts",
]

# Scripts known to have --help  (basename → entity name mapping)
KNOWN_SCRIPTS = {
    "rag_cli.py": "SKILL:rag-operations",
    "sync_script_registry.py": "SKILL:registry-sync",
    "sync_manifest_versions.py": "SKILL:version-sync",
    "safe_commit.py": "SKILL:git-governance",
    "create_task.py": "SKILL:plane-task-creation",
    "sync_project_context.py": "SKILL:plane-context-sync",
    "post_solution.py": "SKILL:plane-solution-posting",
    "update_task.py": "SKILL:plane-task-update",
}

# New paths to scan for Plane skills
SCAN_DIRS.append(".agent/skills/routing/managing-plane-tasks/scripts")
# Correct script locations:
# scripts/ai/rag/rag_cli.py
# scripts/maintenance/sync/sync_script_registry.py
# scripts/maintenance/sync/sync_manifest_versions.py
# scripts/git/safe_commit.py
# .agent/skills/routing/managing-plane-tasks/scripts/create_task.py
# .agent/skills/routing/managing-plane-tasks/scripts/sync_project_context.py
# .agent/skills/routing/managing-plane-tasks/scripts/post_solution.py
# .agent/skills/routing/managing-plane-tasks/scripts/update_task.py
# CONDA_PREFIX removed to allow for environment-aware execution via sys.executable
# PROJECT_ROOT should be the current working directory where the script is executed from
PROJECT_ROOT = os.getcwd()


def get_help_output(script_path: str) -> str:
    """Run a script with --help and capture the output."""
    cmd = [
        sys.executable,
        script_path,
        "--help",
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, cwd=PROJECT_ROOT
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error getting help: {e}"


def parse_help_to_commands(help_text: str) -> list:
    """Extract command names and descriptions from argparse --help output."""
    commands = []
    in_commands = False
    for line in help_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("{") and "}" in stripped:
            # argparse command list like {search,list,ingest,...}
            cmds = stripped.strip("{}").split(",")
            for c in cmds:
                c = c.strip()
                if c:
                    commands.append(c)
        if (
            "positional arguments:" in stripped.lower()
            or "commands:" in stripped.lower()
        ):
            in_commands = True
            continue
        if in_commands and stripped and not stripped.startswith("-"):
            parts = stripped.split(None, 1)
            if len(parts) >= 1:
                cmd_name = parts[0]
                if cmd_name not in commands and not cmd_name.startswith("{"):
                    commands.append(cmd_name)
        if stripped.startswith("options:") or stripped.startswith(
            "optional arguments:"
        ):
            in_commands = False
    return commands


def sync_to_memory_mcp(entity_name: str, observations: list, dry_run: bool = False):
    """Print or sync observations to memory MCP."""
    if dry_run:
        print(f"\n[DRY RUN] Would sync entity: {entity_name}")
        for obs in observations:
            print(f"  - {obs}")
        return

    # In actual use, the agent calls mcp_memory_create_entities or mcp_memory_add_observations.
    # This script outputs the JSON payload for the agent to use.
    payload = {
        "entity_name": entity_name,
        "entity_type": "script_usage",
        "observations": observations,
    }
    print(json.dumps(payload, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Sync script signatures to Memory MCP")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without actually syncing",
    )
    parser.add_argument(
        "--scan-dirs",
        nargs="*",
        default=None,
        help="Override default scan directories",
    )
    args = parser.parse_args()

    scan_dirs = args.scan_dirs or SCAN_DIRS
    print("Script Registry Sync")
    print(f"{'=' * 40}")
    print(f"Scanning: {', '.join(scan_dirs)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'SYNC'}\n")

    synced = 0
    for scan_dir in scan_dirs:
        full_dir = os.path.join(PROJECT_ROOT, scan_dir)
        if not os.path.isdir(full_dir):
            print(f"Warning: {scan_dir} not found, skipping.")
            continue

        for filename in sorted(os.listdir(full_dir)):
            if filename not in KNOWN_SCRIPTS:
                continue

            script_path = os.path.join(full_dir, filename)
            entity_name = KNOWN_SCRIPTS[filename]

            print(f"Introspecting: {scan_dir}/{filename}")
            help_text = get_help_output(script_path)

            if not help_text or "Error" in help_text:
                print("  SKIP: Could not get --help output")
                continue

            # Build observations from help text
            commands = parse_help_to_commands(help_text)

            # Extract description from the first part of help text (before "usage:")
            description = "N/A"
            if "usage:" in help_text.lower():
                description = help_text.lower().split("usage:")[0].strip()

            observations = [
                f"Path: {scan_dir}/{filename}",
                f"Description: {description}",
                f"Goal: {description[:100]}...",  # Truncated for quick scanning
                f"Commands: {', '.join(commands)}" if commands else "No subcommands",
                f"Usage: conda run -p D:\\Anaconda\\envs\\cursor-factory python {scan_dir}/{filename} <cmd>",
                f"Keywords: {filename.replace('.py', '')}, {', '.join(commands)}",
            ]

            sync_to_memory_mcp(entity_name, observations, dry_run=args.dry_run)
            synced += 1

    print(f"\n{'=' * 40}")
    print(f"Synced {synced} script(s).")


if __name__ == "__main__":
    main()
