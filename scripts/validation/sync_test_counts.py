#!/usr/bin/env python3
"""
Sync test counts in docs/TESTING.md with actual pytest test counts.

DEPRECATED: This module is a thin wrapper around sync_artifacts.py.
All functionality has been consolidated into the unified artifact sync system.

For new code, import directly from sync_artifacts:
    from scripts.validation.sync_artifacts import (
        TestCountsByCategory,
        get_actual_counts,
        update_testing_md,
    )

Usage:
    python scripts/validation/sync_test_counts.py          # Check only
    python scripts/validation/sync_test_counts.py --sync   # Auto-fix

Categories synced:
- Total tests
- Unit tests (tests/unit/)
- Integration tests (tests/integration/)
- Validation tests (tests/validation/)
- Guardian tests (tests/guardian/)
- Memory tests (tests/memory/)
"""

import sys

# Handle imports for both direct script execution and module import
try:
    from scripts.validation.sync_artifacts import (
        CategoryTestCounts,
        TestCountsByCategory,  # Backward compat alias
        get_python_path,
        collect_test_count,
        get_actual_counts,
        extract_documented_counts,
        update_testing_md,
    )
except ModuleNotFoundError:
    # When running as a script, use relative import
    from sync_artifacts import (
        CategoryTestCounts,
        TestCountsByCategory,  # Backward compat alias
        get_python_path,
        collect_test_count,
        get_actual_counts,
        extract_documented_counts,
        update_testing_md,
    )

# Re-export with the original name for backward compatibility
# Tests may import CountsByCategory, so we alias it
CountsByCategory = CategoryTestCounts

# Export all public symbols
__all__ = [
    "CategoryTestCounts",
    "CountsByCategory",  # Deprecated alias
    "TestCountsByCategory",  # Deprecated alias
    "get_python_path",
    "collect_test_count",
    "get_actual_counts",
    "extract_documented_counts",
    "update_testing_md",
]


def main():
    """Main entry point - delegates to sync_artifacts for test counts."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    sync = "--sync" in sys.argv

    # Get actual counts
    actual = get_actual_counts()

    print("\nActual test counts:")
    print(f"  Total:       {actual.total}")
    print(f"  Unit:        {actual.unit}")
    print(f"  Integration: {actual.integration}")
    print(f"  Validation:  {actual.validation}")
    print(f"  Guardian:    {actual.guardian}")
    print(f"  Memory:      {actual.memory}")
    print()

    # Check/sync documentation
    changes = update_testing_md(actual, dry_run=not sync)

    if not changes:
        print("[OK] Test counts are in sync with documentation")
        return 0

    if sync:
        print(f"[SYNCED] {len(changes)} count(s) updated:")
        for change in changes:
            print(f"  - {change}")
        return 0
    else:
        print(f"[OUT OF SYNC] {len(changes)} count(s) differ:")
        for change in changes:
            print(f"  - {change}")
        print("\nRun with --sync to fix")
        return 1


if __name__ == "__main__":
    sys.exit(main())
