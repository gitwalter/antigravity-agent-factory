#!/usr/bin/env python3
"""
Verify and Commit Pipeline (RCW)

A unified, sequential pipeline specifically designed for robust "fast commits".
Ensures synchronization, validation, and core testing before allowing a commit.

Stages:
1. Sync: Apply minor fixes (test counts, skill ID mappings) to docs/blueprints.
2. Stage: Auto-stage modified files to prepare the commit.
3. Validate: Run syntax and structural checks.
4. Test: Run critical smoke tests to guarantee core features.
"""

import subprocess
import sys
import time
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
        # Use full path for python scripts if needed
        full_cmd = [PYTHON] + cmd if cmd[0].endswith(".py") else cmd
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
            print(f"  ✅ Success ({duration:.1f}s)")
            if result.stdout.strip():
                # Print only first few lines if too long
                lines = result.stdout.strip().splitlines()
                for line in lines[:5]:
                    print(f"     {line}")
                if len(lines) > 5:
                    print(f"     ... ({len(lines)-5} more lines)")
            return True
        else:
            print(f"  ❌ Failed ({duration:.1f}s)")
            print(f"     STDOUT: {result.stdout.strip()[:200]}")
            print(f"     STDERR: {result.stderr.strip()[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    print(f"🚀 Starting Robust Commit Workflow (RCW) in {ROOT}\n")

    # STAGE 1: Sync
    if not run(
        ["scripts/validation/sync_artifacts.py", "--sync", "--fast"],
        "Synchronizing Artifacts",
    ):
        return 1

    if not run(
        ["scripts/validation/update_index.py", "--full"], "Updating Repository Index"
    ):
        return 1

    # STAGE 2: Stage Changes
    # This ensures that fixes applied during Sync are actually included in the commit
    if not run(["git", "add", "-u"], "Staging Updated Artifacts"):
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

    # STAGE 4: Smoke Test
    # Running only core tests for "Fast Commit" - full suite should be run in CI or manually
    print(f"[RUN] Running Core Smoke Tests ({len(CORE_TESTS)} files)...")
    test_cmd = [PYTHON, "-m", "pytest", "-n", "auto"] + CORE_TESTS
    if not run(test_cmd, "Smoke Testing Core Modules"):
        return 1

    print("\n✨ All verification stages passed! Ready to commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
