import os
import shutil
import glob
import sys

from pathlib import Path

# Constants
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TMP_DIR = ROOT_DIR / "tmp"
FORBIDDEN_EXTENSIONS = [".py", ".json", ".log", ".txt", ".temp", ".tmp"]
ALLOWED_FILES = [
    "README.md",
    "AGENTS.md",
    ".agentrules",
    ".gitignore",
    "package.json",
    "tsconfig.json",
    "next.config.js",
    "llm_config.py",
    "memoization.py",
    "workflow_audit_report.md",
    "PURPOSE.md",
]


def enforce_tmp_usage():
    print(f"[*] Starting Root Cleanliness Enforcement in: {ROOT_DIR}")

    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
        print(f"[*] Created missing tmp directory: {TMP_DIR}")

    found_illegal = False
    for item in os.listdir(ROOT_DIR):
        item_path = os.path.join(ROOT_DIR, item)

        # Skip directories and allowed files
        if os.path.isdir(item_path) or item in ALLOWED_FILES:
            continue

        # Check extensions
        _, ext = os.path.splitext(item)
        if ext.lower() in FORBIDDEN_EXTENSIONS or (
            not ext and item.startswith("test_")
        ):
            found_illegal = True
            target_path = os.path.join(TMP_DIR, item)

            # Handle potential name collisions
            if os.path.exists(target_path):
                base, extension = os.path.splitext(item)
                import time

                new_name = f"{base}_{int(time.time())}{extension}"
                target_path = os.path.join(TMP_DIR, new_name)

            print(f"[!] Illegal root file detected: {item} -> Moving to tmp/")
            try:
                shutil.move(item_path, target_path)
            except Exception as e:
                print(f"[ERROR] Failed to move {item}: {e}")

    if not found_illegal:
        print("[+] Root directory is clean. No illegal temporary files found.")
    else:
        print("[+] Enrollment complete. All illegal artifacts moved to tmp/.")


if __name__ == "__main__":
    enforce_tmp_usage()
