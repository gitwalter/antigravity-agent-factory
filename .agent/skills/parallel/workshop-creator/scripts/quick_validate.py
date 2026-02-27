#!/usr/bin/env python3
"""
Quick validation script for workshops
"""

import sys
import os
import re
from pathlib import Path


def validate_workshop(path):
    path = Path(path)
    if not path.exists():
        return False, f"Workshop file not found at {path}"

    # Check naming convention (LX_name.md)
    if not re.match(r"^L\d+_[a-z0-9_]+\.md$", path.name):
        return (
            False,
            f"Workshop filename '{path.name}' must follow the pattern LX_name.md (e.g., L1_intro.md)",
        )

    content = path.read_text(encoding="utf-8")

    # Check for required sections (headers)
    required_headers = ["Learning Objectives", "Practice"]
    missing = [
        h
        for h in required_headers
        if f"# {h}" not in content and f"## {h}" not in content
    ]

    if missing:
        return False, f"Missing required sections: {', '.join(missing)}"

    return True, "Workshop is valid!"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <workshop_file_path>")
        sys.exit(1)

    valid, message = validate_workshop(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
