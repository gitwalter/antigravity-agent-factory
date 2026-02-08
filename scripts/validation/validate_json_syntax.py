#!/usr/bin/env python3
"""
JSON Syntax Validator

Validates that JSON files in the repository are well-formed and use proper encoding (UTF-8).
Specially handles UTF-8-SIG for files with BOM to prevent common JSONDecodeErrors.

Usage:
    python scripts/validation/validate_json_syntax.py --all           # Validate all JSON files
    python scripts/validation/validate_json_syntax.py --file path/to.json # Validate specific file
    python scripts/validation/validate_json_syntax.py --staged        # Validate staged files (requires git)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class JSONValidator:
    def __init__(self, root_path: Path):
        self.root_path = root_path

    def validate_file(self, file_path: Path) -> Tuple[bool, str]:
        """Validate a single JSON file."""
        if not file_path.exists():
            return False, f"File not found: {file_path}"
        
        try:
            # Try utf-8-sig first to handle potential BOMs quietly
            with open(file_path, "r", encoding="utf-8-sig") as f:
                json.load(f)
            return True, ""
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {e}"
        except Exception as e:
            return False, f"Error reading file: {e}"

    def get_staged_files(self) -> List[Path]:
        """Get list of staged JSON files using git."""
        try:
            output = subprocess.check_output(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                universal_newlines=True
            )
            return [self.root_path / f for f in output.splitlines() if f.endswith(".json")]
        except Exception as e:
            print(f"Warning: Could not get staged files: {e}")
            return []

    def get_all_json_files(self) -> List[Path]:
        """Get all JSON files in the repository, excluding common ignore dirs."""
        ignore_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "fixtures"}
        json_files = []
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]
            for file in files:
                if file.endswith(".json"):
                    json_files.append(Path(root) / file)
        return json_files


def main():
    parser = argparse.ArgumentParser(description="Validate JSON syntax and encoding.")
    parser.add_argument("--all", action="store_true", help="Validate all JSON files in the repo")
    parser.add_argument("--file", type=str, help="Validate a specific JSON file")
    parser.add_argument("--staged", action="store_true", help="Validate staged JSON files only")
    
    args = parser.parse_args()
    root = Path(__file__).parent.parent.parent
    validator = JSONValidator(root)
    
    files_to_check = []
    if args.file:
        files_to_check.append(Path(args.file))
    elif args.staged:
        files_to_check = validator.get_staged_files()
    elif args.all:
        files_to_check = validator.get_all_json_files()
    else:
        parser.print_help()
        return 0

    if not files_to_check:
        print("No JSON files found to validate.")
        return 0

    errors = []
    print(f"Validating {len(files_to_check)} JSON files...")
    for file in files_to_check:
        relative_path = os.path.relpath(file, root)
        success, error_msg = validator.validate_file(file)
        if success:
            print(f"[PASS] {relative_path}")
        else:
            print(f"[FAIL] {relative_path}: {error_msg}")
            errors.append((relative_path, error_msg))

    if errors:
        print(f"\nValidation failed with {len(errors)} errors.")
        return 1
    
    print("\nAll JSON files validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
