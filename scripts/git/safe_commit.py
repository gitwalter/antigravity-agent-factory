#!/usr/bin/env python3
"""
Safe Commit Wrapper (Robust Commit Workflow - RCW)

Provides a safe way to commit with automatic validation, synchronization,
and core smoke testing before committing/pushing.

Usage:
    python scripts/git/safe_commit.py "commit message"
    python scripts/git/safe_commit.py "commit message" --push
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_verification(root_dir: Path) -> bool:
    """
    Run the unified verify_and_commit pipeline.
    """
    verifier = root_dir / "scripts" / "git" / "verify_and_commit.py"
    if not verifier.exists():
        print(f"[ERROR] Verifier script not found: {verifier}")
        return False

    try:
        # We use sys.executable to ensure we use the same python environment
        result = subprocess.run(
            [sys.executable, str(verifier)], cwd=root_dir, capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[FAIL] Error running verification: {e}")
        return False


def commit(root_dir: Path, message: str) -> bool:
    """Create git commit."""
    try:
        # Note: verify_and_commit already staged changes,
        # but we do a final check to ensure we have something to commit.
        status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=root_dir)
        if status.returncode == 0:
            print("[INFO] No changes staged. Nothing to commit.")
            # We return True because "nothing to commit" isn't strictly an error
            # for a "safe commit" routine that just verified everything.
            return True

        result = subprocess.run(
            ["git", "commit", "-m", message], cwd=root_dir, capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[FAIL] Error creating commit: {e}")
        return False


def push(root_dir: Path) -> bool:
    """Push commits to remote."""
    try:
        result = subprocess.run(["git", "push"], cwd=root_dir, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"[FAIL] Error pushing: {e}")
        return False


def main():
    """Main entry point."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Safe commit with Robust Commit Workflow (RCW)"
    )
    parser.add_argument("message", type=str, help="Commit message")
    parser.add_argument(
        "--push", action="store_true", help="Push to remote after commit"
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip verification (NOT recommended)",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Project root directory",
    )

    args = parser.parse_args()
    root_dir = Path(args.root).resolve()

    # 1. Verification
    if not args.skip_verify:
        print("🔍 Running Robust Verification Pipeline...")
        if not run_verification(root_dir):
            print("\n❌ Verification failed. Commit aborted.")
            return 1

    # 2. Commit
    print(f"\n📦 Committing changes: {args.message}")
    if not commit(root_dir, args.message):
        return 1

    # 3. Push
    if args.push:
        print("\n🚀 Pushing to remote...")
        if not push(root_dir):
            return 1

    print("\n✅ Successfully committed and verified changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
