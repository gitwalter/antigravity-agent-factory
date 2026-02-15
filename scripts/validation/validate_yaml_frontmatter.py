#!/usr/bin/env python3
"""
YAML Frontmatter Validator for Markdown Files.

Validates YAML frontmatter in markdown files (.md) to catch syntax errors
before they cause issues in documentation or tooling.

Usage:
    # Validate all markdown files in repo
    python scripts/validation/validate_yaml_frontmatter.py

    # Validate specific files
    python scripts/validation/validate_yaml_frontmatter.py file1.md file2.md

    # Validate with verbose output
    python scripts/validation/validate_yaml_frontmatter.py --verbose

Exit Codes:
    0 - All files valid (or no frontmatter found)
    1 - Validation errors found
"""

import re
import sys
from pathlib import Path
from typing import Optional


# Directories to scan for markdown files
MARKDOWN_DIRS = [
    ".agent/agents",
    ".agent/skills",
    "docs",
    "blueprints",
    "patterns",
    "workflows",
]

# Files to always check (even if not in MARKDOWN_DIRS)
ADDITIONAL_FILES = [
    "README.md",
    "CHANGELOG.md",
    "PURPOSE.md",
]

# Pattern to extract YAML frontmatter
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def validate_yaml_syntax(content: str, filepath: str) -> Optional[str]:
    """
    Validate YAML syntax without external dependencies.

    Returns error message if invalid, None if valid.

    Args:
        content: The YAML content to validate
        filepath: Path to file (for error messages)

    Returns:
        Error message string if invalid, None if valid
    """
    lines = content.split("\n")
    indent_stack = [0]
    in_multiline = False
    multiline_indent = 0

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check for tabs (YAML prefers spaces)
        if "\t" in line and not in_multiline:
            return f"Line {line_num}: Tab character found (use spaces for indentation)"

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        # Handle multiline strings
        if in_multiline:
            if indent <= multiline_indent and stripped:
                in_multiline = False
            else:
                continue

        # Check for multiline indicators
        if stripped.endswith("|") or stripped.endswith(">"):
            in_multiline = True
            multiline_indent = indent
            continue

        # Check for key-value structure
        if ":" in stripped:
            # Extract key part
            key_part = stripped.split(":")[0].strip()

            # Check for unquoted special characters in keys
            if key_part and not key_part.startswith(("-", '"', "'")):
                # Key should not start with special YAML characters
                if key_part[0] in ["@", "`", "!", "&", "*"]:
                    return f"Line {line_num}: Key starts with special character '{key_part[0]}'"

            # Check value part for common issues
            value_part = ":".join(stripped.split(":")[1:]).strip()

            # Detect unquoted values with problematic characters
            if value_part and not value_part.startswith(('"', "'", "[", "{", "|", ">")):
                # Check for unbalanced quotes
                if value_part.count('"') % 2 != 0:
                    return f"Line {line_num}: Unbalanced double quotes in value"
                if value_part.count("'") % 2 != 0:
                    return f"Line {line_num}: Unbalanced single quotes in value"

                # Check for comma-separated values that should be a list
                # Pattern: "value1", "value2", unquoted value
                if re.search(r'"[^"]+",\s*"[^"]+",\s*[^"\[\]]+$', value_part):
                    return f"Line {line_num}: Mixed quoted and unquoted values - use YAML array syntax"

                # Check for values that look like lists but aren't properly formatted
                if re.search(r'^"[^"]+",\s*"[^"]+"', value_part):
                    return f"Line {line_num}: Comma-separated quoted strings - use YAML array syntax instead"

        # Check for array items
        elif stripped.startswith("-"):
            item_content = stripped[1:].strip()
            # Check array item syntax
            if item_content and item_content[0] == "-" and item_content[1:].strip():
                return f"Line {line_num}: Invalid array syntax (double dash)"

    return None


def check_common_yaml_errors(content: str, filepath: str) -> Optional[str]:
    """
    Check for common YAML errors that parsers might accept but are semantically wrong.

    These patterns are technically parseable but usually indicate a mistake.

    Args:
        content: The YAML content to validate
        filepath: Path to file (for error messages)

    Returns:
        Error message string if error found, None if valid
    """
    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        # Check for key-value pairs
        if ":" in stripped:
            value_part = ":".join(stripped.split(":")[1:]).strip()

            # Pattern: "value1", "value2" - comma-separated quoted strings
            # This is almost always a mistake (should be YAML array)
            if re.search(r'^"[^"]*",\s*"[^"]*"', value_part):
                return f"Line {line_num}: Comma-separated quoted strings detected - use YAML array syntax instead"

            # Pattern: unbalanced quotes in value (odd number)
            # Count quotes not escaped
            double_quotes = len(re.findall(r'(?<!\\)"', value_part))
            if double_quotes % 2 != 0:
                # Check if it's a multiline indicator
                if not value_part.rstrip().endswith(
                    "|"
                ) and not value_part.rstrip().endswith(">"):
                    return f"Line {line_num}: Unbalanced double quotes in value"

    return None


def validate_yaml_with_pyyaml(content: str, filepath: str) -> Optional[str]:
    """
    Validate YAML using PyYAML if available, plus common error patterns.

    Args:
        content: The YAML content to validate
        filepath: Path to file (for error messages)

    Returns:
        Error message string if invalid, None if valid
    """
    try:
        import yaml

        yaml.safe_load(content)
        # PyYAML passed, but also check for common semantic errors
        return check_common_yaml_errors(content, filepath)
    except yaml.YAMLError as e:
        return str(e)
    except ImportError:
        # PyYAML not available, use basic validation
        return validate_yaml_syntax(content, filepath)


def extract_frontmatter(content: str) -> Optional[str]:
    """
    Extract YAML frontmatter from markdown content.

    Args:
        content: Full markdown file content

    Returns:
        Frontmatter content (without ---), or None if not found
    """
    match = FRONTMATTER_PATTERN.match(content)
    if match:
        return match.group(1)
    return None


def validate_file(filepath: Path, verbose: bool = False) -> tuple[bool, Optional[str]]:
    """
    Validate YAML frontmatter in a markdown file.

    Args:
        filepath: Path to the markdown file
        verbose: Whether to print verbose output

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read file: {e}"

    frontmatter = extract_frontmatter(content)

    if frontmatter is None:
        if verbose:
            print(f"  {filepath}: No frontmatter found (OK)")
        return True, None

    # Try PyYAML first, fall back to basic validation
    error = validate_yaml_with_pyyaml(frontmatter, str(filepath))

    if error:
        return False, error

    if verbose:
        print(f"  {filepath}: Valid YAML frontmatter")

    return True, None


def find_markdown_files(repo_root: Path) -> list[Path]:
    """
    Find all markdown files to validate.

    Args:
        repo_root: Repository root directory

    Returns:
        List of Path objects for markdown files
    """
    files = []

    # Scan configured directories
    for dir_name in MARKDOWN_DIRS:
        dir_path = repo_root / dir_name
        if dir_path.exists():
            files.extend(dir_path.rglob("*.md"))

    # Add additional files
    for file_name in ADDITIONAL_FILES:
        file_path = repo_root / file_name
        if file_path.exists():
            files.append(file_path)

    return sorted(set(files))


def main(files: list[str] = None, verbose: bool = False) -> int:
    """
    Main validation function.

    Args:
        files: Optional list of specific files to validate
        verbose: Whether to print verbose output

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    # Determine repo root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent

    # Get files to validate
    if files:
        markdown_files = [Path(f) for f in files if f.endswith(".md")]
    else:
        markdown_files = find_markdown_files(repo_root)

    if not markdown_files:
        print("No markdown files found to validate")
        return 0

    if verbose:
        print(f"Validating {len(markdown_files)} markdown files...")

    errors = []

    for filepath in markdown_files:
        is_valid, error = validate_file(filepath, verbose)
        if not is_valid:
            errors.append((filepath, error))

    if errors:
        print("\nYAML Frontmatter Errors Found:")
        print("=" * 50)
        for filepath, error in errors:
            print(f"\n{filepath}:")
            print(f"  {error}")
        print("\n" + "=" * 50)
        print(f"Found {len(errors)} file(s) with invalid YAML frontmatter")
        return 1

    if verbose:
        print(f"\nAll {len(markdown_files)} files have valid YAML frontmatter")

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter in markdown files"
    )
    parser.add_argument(
        "files", nargs="*", help="Specific files to validate (default: scan repo)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()
    sys.exit(main(args.files, args.verbose))
