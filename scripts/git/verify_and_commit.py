#!/usr/bin/env python3
"""
Verify and Commit Pipeline (RCW)

A unified, sequential pipeline specifically designed for robust "fast commits".
Ensures synchronization, validation, and core testing before allowing a commit.

Optimization:
- Added timing logs for each stage.
- Conditional "full" vs "fast" modes for index updates.
- Integrated pre-commit for proactive linting and sync.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import List

# Configuration
PYTHON = sys.executable
ROOT = Path(__file__).resolve().parent.parent.parent
CORE_TESTS = [
    "tests/unit/test_pattern_loading.py",
    "tests/unit/sync/test_sync_artifacts.py",
    "tests/integration/test_system_steward_governance.py",
]


def run(cmd: List[str], description: str) -> bool:
    """Run a command and print status."""
    print(f"[RUN] {description}...")
    start_time = time.time()
    try:
        # If it's a python script, ensure we use the same interpreter
        if cmd[0].endswith(".py") or cmd[0] == "-m":
            full_cmd = [PYTHON] + cmd
        else:
            full_cmd = cmd

        result = subprocess.run(
            full_cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        duration = time.time() - start_time

        if result.returncode == 0:
            print(f"  [OK] Success ({duration:.1f}s)")
            if result.stdout.strip():
                # Print only first few lines if too long
                lines = result.stdout.strip().splitlines()
                for line in lines[:3]:
                    print(f"     {line}")
                if len(lines) > 3:
                    print(f"     ... ({len(lines)-3} more lines)")
            return True
        else:
            print(f"\n[ERROR] Verification failed. ({duration:.1f}s)")
            # Print stderr if stdout is empty
            output = result.stdout.strip() or result.stderr.strip()
            print(f"     OUTPUT: {output[:300]}...")
            return False
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        return False


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="RCW: Robust Commit Workflow")
    parser.add_argument("--fast", action="store_true", help="Run in extra-fast mode")
    args = parser.parse_args()

    print(f"RCW: Starting Robust Commit Workflow (RCW) in {ROOT}")
    total_start = time.time()

    # STAGE 0: Pre-Commit (Handled by git commit hooks - skipping full scan for speed)
    # Note: git commit will naturally trigger hooks for staged files.
    # We only run sync here to ensure factory integrity.

    # STAGE 1: Sync
    if not run(
        ["scripts/validation/sync_artifacts.py", "--sync", "--fast"],
        "Synchronizing Artifacts",
    ):
        return 1

    # Skip full index update if in fast mode
    index_flag = "--full" if not args.fast else "--check"
    if not run(
        ["scripts/validation/update_index.py", index_flag],
        f"Updating Repository Index ({index_flag})",
    ):
        return 1

    # STAGE 2: Stage Changes
    if not run(["git", "add", "."], "Staging All Changes (including new files)"):
        return 1

    # STAGE 3: Validate
    if not run(
        ["scripts/validation/validate_json_syntax.py", "--all"],
        "Validating JSON Syntax",
    ):
        return 1

    if not run(
        ["scripts/validation/validate_readme_structure.py", "--check"],
        "Validating README Structure",
    ):
        return 1

    # STAGE 4: Smoke Test (Skipped in fast mode)
    if not args.fast:
        print(f"[RUN] Running Core Smoke Tests ({len(CORE_TESTS)} files)...")
        test_cmd = ["-m", "pytest", "-n", "auto"] + CORE_TESTS
        if not run(test_cmd, "Smoke Testing Core Modules"):
            return 1
    else:
        print("  [SKIP] Smoke tests skipped in --fast mode.")

    total_duration = time.time() - total_start
    print(
        f"\n[DONE] High-Velocity Verification passed in {total_duration:.1f}s! Ready to commit."
    )
    return 0

    total_duration = time.time() - total_start
    print(
        f"\n[DONE] All verification stages passed in {total_duration:.1f}s! Ready to commit."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
