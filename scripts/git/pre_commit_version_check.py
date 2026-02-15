#!/usr/bin/env python3
"""
Pre-commit hook wrapper for blueprint version updates.

This script checks if a week has passed since the last version update
and runs the update if needed. Designed to be called from pre-commit hooks.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Path to timestamp file
TIMESTAMP_FILE = Path(__file__).parent.parent / ".last_version_check"


def should_run_update() -> bool:
    """Check if a week has passed since last update.

    Returns:
        True if update should run, False otherwise
    """
    if not TIMESTAMP_FILE.exists():
        return True

    try:
        with open(TIMESTAMP_FILE, "r") as f:
            data = json.load(f)
            last_check = datetime.fromisoformat(data["last_check"])

        # Check if 7 days have passed
        if datetime.now() - last_check >= timedelta(days=7):
            return True

        return False
    except Exception:
        # If there's any error reading the file, run the update
        return True


def update_timestamp():
    """Update the timestamp file with current time."""
    try:
        data = {
            "last_check": datetime.now().isoformat(),
            "last_check_readable": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(TIMESTAMP_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not update timestamp file: {e}", file=sys.stderr)


def main():
    """Main entry point for pre-commit hook."""
    if not should_run_update():
        # Less than a week since last check, skip
        sys.exit(0)

    print("Running weekly blueprint version check...")

    # Import and run the version updater
    try:
        # Add maintenance directory to path to import VersionUpdater
        sys.path.insert(0, str(Path(__file__).parents[1] / "maintenance"))
        from update_blueprint_versions import VersionUpdater

        blueprints_dir = Path(__file__).parents[2] / ".agent" / "blueprints"
        updater = VersionUpdater(dry_run=False)
        updater.update_all_blueprints(blueprints_dir)

        # Update timestamp after successful run
        update_timestamp()

        print("✅ Version check complete")
        sys.exit(0)

    except Exception as e:
        print(f"⚠️  Warning: Version check failed: {e}", file=sys.stderr)
        # Don't fail the commit on version check errors
        sys.exit(0)


if __name__ == "__main__":
    main()
