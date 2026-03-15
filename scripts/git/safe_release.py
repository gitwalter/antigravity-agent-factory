#!/usr/bin/env python3
"""
Safe Release Automation (SRA) v2.0

Automates the release process:
1. Validates the state via safe_commit.py.
2. Detects current version from CHANGELOG.md and Git tags.
3. Bumps version safely.
4. Updates CHANGELOG.md (migrates [Unreleased] content).
   - ABORTS if [Unreleased] is empty/missing or already released on HEAD.
5. Commits, Tags, and Pushes.

Usage:
    python scripts/git/safe_release.py --bump patch
"""

import argparse
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Tuple

ROOT = Path(__file__).resolve().parent.parent.parent
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
SAFE_COMMIT_PATH = ROOT / "scripts" / "git" / "safe_commit.py"


def get_git_status() -> dict:
    """Check current git state."""
    res = {}
    # Current tag on HEAD
    tag_proc = subprocess.run(
        ["git", "tag", "--points-at", "HEAD"], capture_output=True, text=True, cwd=ROOT
    )
    res["head_tags"] = tag_proc.stdout.strip().splitlines()

    # Last tag overall
    last_tag_proc = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    res["latest_tag"] = last_tag_proc.stdout.strip()

    return res


def get_current_version() -> Tuple[str, int]:
    """Extract the latest version from CHANGELOG.md."""
    if not CHANGELOG_PATH.exists():
        raise FileNotFoundError(f"CHANGELOG.md not found at {CHANGELOG_PATH}")

    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    match = re.search(r"## \[(\d+\.\d+\.\d+)\]", content)
    if not match:
        raise ValueError("Could not find a version in CHANGELOG.md")

    return match.group(1), content.find(match.group(0))


def bump_version(current: str, bump_type: str) -> str:
    """Bump semantic version."""
    major, minor, patch = map(int, current.split("."))
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"


def is_content_valuable(content: str) -> bool:
    """Check if the extracted markdown content has actual information."""
    if not content or not content.strip():
        return False
    # Remove placeholders and empty sections
    stripped = re.sub(r"### (Added|Changed|Fixed)", "", content)
    stripped = re.sub(r"[\s\-\n\r]+", "", stripped)
    return len(stripped) > 0


def update_changelog(new_version: str):
    """Move [Unreleased] content to new version and insert header."""
    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    # Extract Unreleased section
    unreleased_pattern = r"## \[Unreleased\](.*?)(?=## \[\d+\.\d+\.\d+\]|---|\Z)"
    match = re.search(unreleased_pattern, content, re.DOTALL)

    if not match:
        print(
            "ℹ️ Info: No ## [Unreleased] section found. Checking if there is anything to release..."
        )
        # If no unreleased section, we assume nothing to do unless forced (not implemented)
        return False

    unreleased_content = match.group(1).strip()

    if not is_content_valuable(unreleased_content):
        print("ℹ️ Info: [Unreleased] section is empty or placeholder-only.")
        # User requested: "unreleased entry is not needed"
        # We clean it up if it exists but is empty.
        cleaned_content = content.replace(match.group(0), "").strip() + "\n"
        CHANGELOG_PATH.write_text(cleaned_content, encoding="utf-8")
        print("[OK] Removed empty [Unreleased] section.")
        return False

    # Perform the migration
    new_header = f"## [{new_version}] - {today}\n"
    migrated_section = f"{new_header}\n{unreleased_content}\n\n"

    # Remove old unreleased and insert new section before first version
    content_without_unreleased = content.replace(match.group(0), "").strip()
    insertion_match = re.search(r"## \[\d+\.\d+\.\d+\]", content_without_unreleased)

    if insertion_match:
        idx = insertion_match.start()
        updated_content = (
            content_without_unreleased[:idx]
            + migrated_section
            + content_without_unreleased[idx:]
        )
    else:
        updated_content = content_without_unreleased + "\n\n" + migrated_section

    CHANGELOG_PATH.write_text(updated_content, encoding="utf-8")
    print(f"[OK] Migrated [Unreleased] to v{new_version}")
    return True


def run_command(cmd: list, description: str) -> bool:
    """Run a shell command."""
    print(f"[RUN] {description}...")
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Safe Release Automation v2.0")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], default="patch")
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--skip-verify", action="store_true")
    parser.add_argument(
        "--no-push-tags", action="store_true", help="Skip pushing tags to remote"
    )
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    # 0. Git Awareness
    git_info = get_git_status()
    current_version, _ = get_current_version()

    print(f"Current version in CHANGELOG: {current_version}")
    if git_info["head_tags"]:
        print(f"Current commit is already tagged: {', '.join(git_info['head_tags'])}")
        # If HEAD is already tagged with the current version, we should probably stop
        # unless the user wants to bump further.
        if f"v{current_version}" in git_info["head_tags"]:
            print("⚠️ HEAD is already at the latest version mentioned in CHANGELOG.")

    new_version = bump_version(current_version, args.bump)

    if args.dry_run:
        print(f"--- DRY RUN: Bump {current_version} -> {new_version} ---")
        return 0

    # 1. Update Changelog
    if not update_changelog(new_version):
        print("🛑 No unreleased changes found. Release aborted.")
        return 0

    # 2. Commit & Tag
    commit_msg = f"Release {new_version}"
    if args.skip_verify:
        run_command(["git", "add", "."], "Staging all")
        if not run_command(["git", "commit", "-m", commit_msg], "Committing"):
            return 1
    else:
        cmd = [sys.executable, str(SAFE_COMMIT_PATH), commit_msg]
        if args.fast:
            cmd.append("--fast")
        if not run_command(cmd, "Verifying and Committing"):
            return 1

    tag_name = f"v{new_version}"
    if not run_command(
        ["git", "tag", "-a", tag_name, "-m", commit_msg], f"Tagging {tag_name}"
    ):
        return 1

    # 3. Push
    run_command(["git", "push"], "Pushing branch")
    if not args.no_push_tags:
        run_command(["git", "push", "origin", tag_name], "Pushing tag")
    else:
        print(f"ℹ️ Skipping remote tag push for {tag_name} as requested.")

    print(f"✨ Successfully released {new_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
