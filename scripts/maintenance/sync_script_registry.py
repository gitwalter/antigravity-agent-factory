#!/usr/bin/env python
"""
Script Registry Sync — Introspects CLI scripts and syncs signatures to Memory MCP.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/maintenance/sync_script_registry.py
    conda run -p D:\\Anaconda\\envs\\cursor-factory python scripts/maintenance/sync_script_registry.py --dry-run

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
SCAN_DIRS = [
    "scripts/ai/rag",
    "scripts/pms",
]

# Scripts known to have --help  (basename → entity name mapping)
KNOWN_SCRIPTS = {
    "rag_cli.py": "RAG_CLI_Commands",
    "manager.py": "PMS_CLI_Commands",
}

CONDA_PREFIX = r"D:\Anaconda\envs\cursor-factory"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


def get_help_output(script_path: str) -> str:
    """Run a script with --help and capture the output."""
    cmd = [
        "conda",
        "run",
        "-p",
        CONDA_PREFIX,
        "python",
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
            observations = [
                f"Script: {scan_dir}/{filename}",
                f"Commands: {', '.join(commands)}"
                if commands
                else "No subcommands detected",
                f"Run: conda run -p {CONDA_PREFIX} python {scan_dir}/{filename} <cmd>",
            ]

            # Add first 10 lines of help as raw reference
            help_lines = help_text.split("\n")[:10]
            observations.append(
                f"Help preview: {' | '.join(l.strip() for l in help_lines if l.strip())}"
            )

            sync_to_memory_mcp(entity_name, observations, dry_run=args.dry_run)
            synced += 1

    print(f"\n{'=' * 40}")
    print(f"Synced {synced} script(s).")


if __name__ == "__main__":
    main()
