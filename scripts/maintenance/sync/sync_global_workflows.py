#!/usr/bin/env python3
"""
Sync local project workflows to the global Antigravity repository.
Ensures that any edits made to .agent/workflows/ are reflected in the global store.

Global Path: C:/Users/wpoga/.gemini/antigravity/global_workflows
Local Path: .agent/workflows/
"""

import os
import shutil
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def sync_workflows():
    # Define paths
    local_workflows_dir = Path(".agent/workflows")
    global_workflows_dir = Path("C:/Users/wpoga/.gemini/antigravity/global_workflows")

    if not local_workflows_dir.exists():
        logger.error(f"Local workflows directory not found: {local_workflows_dir}")
        return

    # Ensure global directory exists
    if not global_workflows_dir.exists():
        logger.info(f"Creating global workflows directory: {global_workflows_dir}")
        global_workflows_dir.mkdir(parents=True, exist_ok=True)

    logger.info(
        f"Syncing workflows from {local_workflows_dir} to {global_workflows_dir}..."
    )

    synced_count = 0
    for workflow_file in local_workflows_dir.glob("*.md"):
        target_path = global_workflows_dir / workflow_file.name

        # Check if sync is needed (content difference or missing file)
        should_copy = False
        if not target_path.exists():
            should_copy = True
        else:
            local_content = workflow_file.read_text(encoding="utf-8")
            global_content = target_path.read_text(encoding="utf-8")
            if local_content != global_content:
                should_copy = True

        if should_copy:
            try:
                shutil.copy2(workflow_file, target_path)
                logger.info(f"  [SYNCED] {workflow_file.name}")
                synced_count += 1
            except Exception as e:
                logger.error(f"  [ERROR] Failed to sync {workflow_file.name}: {e}")

    logger.info(f"Sync complete. {synced_count} files updated.")


if __name__ == "__main__":
    sync_workflows()
