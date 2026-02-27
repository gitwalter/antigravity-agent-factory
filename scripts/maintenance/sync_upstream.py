#!/usr/bin/env python3
"""
Sync Upstream Script

This script synchronizes the local repository with the upstream reference repository.
Reference: https://github.com/gitwalter/antigravity-agent-factory.git

It intelligently handles conflicts by prioritizing local branding (Antigravity) and
structure (.agent) while adopting functional updates from upstream.

Usage:
    python scripts/maintenance/sync_upstream.py [--dry-run] [--branch <branch_name>]
"""

import argparse
import subprocess
import sys
import shutil
import re
from pathlib import Path
from typing import List, Tuple

UPSTREAM_URL = "https://github.com/gitwalter/antigravity-agent-factory.git"
UPSTREAM_REMOTE_NAME = "upstream"
DEFAULT_BRANCH = "main"


def run_command(
    command: List[str], cwd: str = None, check: bool = True
) -> Tuple[int, str, str]:
    """Run a shell command and return returncode, stdout, stderr."""

    # Use absolute path for git on Windows if available
    git_cmd = r"C:\Program Files\Git\cmd\git.exe"
    if not shutil.which(git_cmd) and shutil.which("git"):
        git_cmd = (
            "git"  # Fallback to standard git if absolute path fails but git is in PATH
        )

    # Prepend git command to arguments
    full_command = [git_cmd] + command[1:] if command[0] == "git" else command

    try:
        result = subprocess.run(
            full_command,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            encoding="utf-8",  # Force UTF-8
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return (
            e.returncode,
            e.stdout.strip() if e.stdout else "",
            e.stderr.strip() if e.stderr else str(e),
        )


def check_remote_exists(remote_name: str) -> bool:
    """Check if a git remote exists."""
    code, stdout, _ = run_command(["git", "remote"])
    if code != 0:
        print(f"Error checking remotes: {_}")
        sys.exit(1)
    return remote_name in stdout.splitlines()


def add_upstream_remote():
    """Add the upstream remote."""
    print(f"Adding upstream remote: {UPSTREAM_REMOTE_NAME} -> {UPSTREAM_URL}")
    code, _, stderr = run_command(
        ["git", "remote", "add", UPSTREAM_REMOTE_NAME, UPSTREAM_URL]
    )
    if code != 0:
        print(f"Failed to add remote: {stderr}")
        sys.exit(1)


def fetch_upstream():
    """Fetch from upstream."""
    print(f"Fetching from {UPSTREAM_REMOTE_NAME}...")
    code, _, stderr = run_command(["git", "fetch", UPSTREAM_REMOTE_NAME])
    if code != 0:
        print(f"Failed to fetch upstream: {stderr}")
        sys.exit(1)


def get_conflicted_files() -> List[str]:
    """Get list of files with merge conflicts."""
    code, stdout, _ = run_command(["git", "diff", "--name-only", "--diff-filter=U"])
    if code != 0:
        return []
    return stdout.splitlines()


def resolve_content_conflict(content: str) -> str:
    """
    Resolve conflicts in content by taking upstream changes but applying
    local branding/structure preferences.
    """
    # Regex to find conflict blocks
    # <<<<<<< HEAD
    # ... ours ...
    # =======
    # ... theirs ...
    # >>>>>>> upstream/main

    pattern = re.compile(
        r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> .*?\n", re.DOTALL
    )

    def replacer(match):
        ours = match.group(1)
        theirs = match.group(2)

        # Strategy:
        # Take 'theirs' (upstream) to get new features/logic.
        # But apply our branding transforms to 'theirs'.

        resolved = theirs

        # 1. Branding: Cursor -> Antigravity
        resolved = resolved.replace(
            "Antigravity Agent Factory", "Antigravity Agent Factory"
        )
        resolved = resolved.replace("Cursor Agent", "Antigravity Agent")
        resolved = resolved.replace(
            "Cursor", "Antigravity"
        )  # Be careful with this one, might be too aggressive?
        # Maybe stick to specific phrases to be safe, but 'Cursor' is the product name likely used everywhere.

        # 2. Structure: .cursor -> .agent
        resolved = resolved.replace(".cursor", ".agent")

        # 3. Reference: gitwalter -> local intent?
        # Actually gitwalter is the upstream, we might want to keep it in some places (like sync script),
        # but in general docs/comments we want Antigravity.

        return resolved

    return pattern.sub(replacer, content)


def resolve_conflicts():
    """Attempt to resolve conflicts automatically."""
    conflicted_files = get_conflicted_files()
    if not conflicted_files:
        print("No conflicts detected.")
        return

    print(f"Attempting to resolve {len(conflicted_files)} conflicts wisely...")

    resolved_count = 0
    for filepath in conflicted_files:
        path = Path(filepath)

        # 1. Strategy: Docs are strictly local. Always keep ours.
        if filepath.startswith("docs/") or filepath.startswith("docs\\"):
            print(f"  Docs detected: {filepath}. Keeping local version (ours).")
            run_command(["git", "checkout", "--ours", filepath])
            run_command(["git", "add", filepath])
            resolved_count += 1
            continue

        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8")
            resolved_content = resolve_content_conflict(content)

            # Write back unresolved content
            path.write_text(resolved_content, encoding="utf-8")

            # Check if markers still exist (failures to resolve)
            if "<<<<<<< HEAD" not in resolved_content:
                # Successfully resolved (or at least markers removed)
                run_command(["git", "add", filepath])
                resolved_count += 1
                print(f"  Resulted: {filepath}")
            else:
                print(
                    f"  Failed to fully resolve: {filepath}. Keeping local version (ours)."
                )
                # Fallback: Keep our version
                run_command(["git", "checkout", "--ours", filepath])
                run_command(["git", "add", filepath])
                resolved_count += 1
        except Exception as e:
            print(f"  Error resolving {filepath}: {e}")

    print(f"Resolved {resolved_count}/{len(conflicted_files)} files.")

    if resolved_count == len(conflicted_files):
        print("All conflicts resolved. Committing...")
        run_command(
            [
                "git",
                "commit",
                "-m",
                "chore: sync upstream with intelligent branding preservation",
            ]
        )
    else:
        print("Some conflicts remain. Please resolve manually.")


def merge_upstream(branch: str, dry_run: bool = False):
    """Merge upstream changes into current branch."""
    upstream_ref = f"{UPSTREAM_REMOTE_NAME}/{branch}"

    if dry_run:
        print(f"[DRY-RUN] Would merge {upstream_ref} into current branch.")
        return

    print(f"Merging {upstream_ref} into current branch...")
    # Allow unrelated histories for the first sync
    code, stdout, stderr = run_command(
        ["git", "merge", upstream_ref, "--allow-unrelated-histories"]
    )

    if code != 0:
        print("Merge encountered conflicts. Starting intelligent resolution...")
        resolve_conflicts()
    else:
        print("Merge successful (no conflicts).")
        if stdout:
            print(stdout)


def prune_docs():
    """Remove extraneous documentation from upstream."""
    print("Pruning extraneous documentation...")
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return

    # Directories to remove
    dirs_to_remove = [
        "agents",
        "articles",
        "design",
        "examples",
        "guides",
        "moments",
        "pm-system",
        "research",
        "workshops",
    ]

    # Files to remove
    files_to_remove = [
        "ASP_VALUE_PROPOSITION.md",
        "COMPLETE_GUIDE.md",
        "CULTURE_AND_VALUES.md",
        "FACTORY_REFERENCE.md",
        "FIRST_WEEK_GUIDE.md",
        "KNOWLEDGE_EVOLUTION.md",
        "LAYERED_ARCHITECTURE.md",
        "LAYERED_ONBOARDING_CONCEPT.md",
        "LEARNING_WORKSHOPS.md",
        "MCP-SERVERS.md",
        "MEMORY_SYSTEM.md",
        "ONBOARDING_GUIDE.md",
        "PATH_CONFIGURATION.md",
        "PREREQUISITES.md",
        "SAP_GROUNDING_DESIGN.md",
        "SOCIETY_USAGE.md",
        "TEAM_WORKSHOP_GUIDE.md",
        "USAGE_GUIDE.md",
        "VERIFICATION.md",
        "WORKFLOW_AUTHORING.md",
    ]

    for d in dirs_to_remove:
        path = docs_dir / d
        if path.exists():
            print(f"  Removing directory: {path}")
            shutil.rmtree(path, ignore_errors=True)

    for f in files_to_remove:
        path = docs_dir / f
        if path.exists():
            print(f"  Removing file: {path}")
            try:
                path.unlink()
            except Exception as e:
                print(f"  Error removing {path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Sync with upstream repository.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the sync process without making changes.",
    )
    parser.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help=f"Upstream branch to sync with (default: {DEFAULT_BRANCH})",
    )

    args = parser.parse_args()

    # 1. Check/Add Remote
    if not check_remote_exists(UPSTREAM_REMOTE_NAME):
        if args.dry_run:
            print(f"[DRY-RUN] Would add remote {UPSTREAM_REMOTE_NAME} ({UPSTREAM_URL})")
        else:
            add_upstream_remote()
    else:
        print(f"Remote '{UPSTREAM_REMOTE_NAME}' already exists.")

    # 2. Fetch
    if args.dry_run:
        print(f"[DRY-RUN] Would fetch {UPSTREAM_REMOTE_NAME}")
    else:
        fetch_upstream()

    # 3. Merge & Resolve
    merge_upstream(args.branch, args.dry_run)

    # 4. Prune Docs
    if not args.dry_run:
        prune_docs()
    else:
        print("[DRY-RUN] Would prune extraneous documentation.")


if __name__ == "__main__":
    main()
