#!/usr/bin/env python3
"""
Changelog Helper - Automated changelog maintenance.

This script helps maintain CHANGELOG.md by:
1. Checking if significant changes need changelog entries
2. Suggesting changelog entries based on staged files
3. Validating changelog format

Usage:
    python scripts/docs/changelog_helper.py --check      # Check if changelog needs update
    python scripts/docs/changelog_helper.py --suggest    # Suggest entries based on staged files
    python scripts/docs/changelog_helper.py --validate   # Validate changelog format

Author: Cursor Agent Factory
Date: 2026-02-08
"""

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ChangelogHelper:
    """
    Helper for maintaining CHANGELOG.md.
    
    Analyzes staged files and suggests appropriate changelog entries
    based on file types and locations.
    """
    
    # File patterns that indicate significant changes
    SIGNIFICANT_PATTERNS = {
        "blueprints/": ("Added", "New blueprint"),
        "knowledge/*.json": ("Added", "New knowledge file"),
        "templates/": ("Added", "New template"),
        ".cursor/agents/": ("Added", "New agent"),
        ".cursor/skills/": ("Added", "New skill"),
        "scripts/": ("Changed", "Script update"),
        "tests/": ("Changed", "Test update"),
    }
    
    # Minimum number of significant files to suggest changelog update
    SIGNIFICANT_THRESHOLD = 3
    
    def __init__(self, repo_root: Optional[Path] = None):
        """Initialize the changelog helper."""
        self.repo_root = repo_root or Path.cwd()
        self.changelog_path = self.repo_root / "CHANGELOG.md"
        
    def get_staged_files(self) -> List[str]:
        """Get list of staged files from git."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return [f for f in result.stdout.strip().split("\n") if f]
        except Exception:
            pass
        return []
    
    def get_recent_commits(self, count: int = 5) -> List[Tuple[str, str]]:
        """Get recent commit hashes and messages."""
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--oneline"],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                commits = []
                for line in result.stdout.strip().split("\n"):
                    if line:
                        parts = line.split(" ", 1)
                        if len(parts) == 2:
                            commits.append((parts[0], parts[1]))
                return commits
        except Exception:
            pass
        return []
    
    def categorize_files(self, files: List[str]) -> Dict[str, List[str]]:
        """Categorize files by type for changelog grouping."""
        categories = defaultdict(list)
        
        for file in files:
            if file.startswith("blueprints/"):
                categories["blueprints"].append(file)
            elif file.startswith("knowledge/") and file.endswith(".json"):
                categories["knowledge"].append(file)
            elif file.startswith("templates/"):
                categories["templates"].append(file)
            elif file.startswith(".cursor/agents/"):
                categories["agents"].append(file)
            elif file.startswith(".cursor/skills/"):
                categories["skills"].append(file)
            elif file.startswith("scripts/"):
                categories["scripts"].append(file)
            elif file.startswith("tests/"):
                categories["tests"].append(file)
            elif file.startswith("docs/"):
                categories["docs"].append(file)
            else:
                categories["other"].append(file)
        
        return dict(categories)
    
    def check_needs_update(self) -> Tuple[bool, str]:
        """
        Check if changelog likely needs an update.
        
        Returns:
            Tuple of (needs_update, reason)
        """
        staged = self.get_staged_files()
        if not staged:
            return False, "No staged files"
        
        categories = self.categorize_files(staged)
        
        # Check for significant additions
        significant_count = 0
        significant_types = []
        
        for cat in ["blueprints", "knowledge", "templates", "agents", "skills"]:
            if cat in categories:
                count = len(categories[cat])
                significant_count += count
                if count > 0:
                    significant_types.append(f"{count} {cat}")
        
        if significant_count >= self.SIGNIFICANT_THRESHOLD:
            return True, f"Significant changes: {', '.join(significant_types)}"
        
        # Check if changelog is in staged files (already being updated)
        if "CHANGELOG.md" in staged:
            return False, "CHANGELOG.md already staged"
        
        return False, f"Only {significant_count} significant files (threshold: {self.SIGNIFICANT_THRESHOLD})"
    
    def suggest_entries(self) -> str:
        """Generate suggested changelog entries based on staged files."""
        staged = self.get_staged_files()
        if not staged:
            return "No staged files to analyze."
        
        categories = self.categorize_files(staged)
        
        lines = ["## Suggested Changelog Entries\n"]
        lines.append(f"Based on {len(staged)} staged files:\n")
        
        # Added section
        added = []
        if "blueprints" in categories:
            for f in categories["blueprints"]:
                name = Path(f).parent.name
                added.append(f"- New blueprint: `{name}`")
        
        if "knowledge" in categories:
            for f in categories["knowledge"]:
                name = Path(f).stem
                added.append(f"- New knowledge file: `{name}`")
        
        if "templates" in categories:
            count = len(categories["templates"])
            added.append(f"- {count} new templates")
        
        if "agents" in categories:
            for f in categories["agents"]:
                name = Path(f).stem
                added.append(f"- New agent: `{name}`")
        
        if "skills" in categories:
            for f in categories["skills"]:
                name = Path(f).parent.name
                added.append(f"- New skill: `{name}`")
        
        if added:
            lines.append("\n### Added")
            lines.extend(added)
        
        # Changed section
        changed = []
        if "scripts" in categories:
            count = len(categories["scripts"])
            changed.append(f"- Updated {count} scripts")
        
        if "docs" in categories:
            count = len(categories["docs"])
            changed.append(f"- Updated {count} documentation files")
        
        if changed:
            lines.append("\n### Changed")
            lines.extend(changed)
        
        return "\n".join(lines)
    
    def validate_format(self) -> Tuple[bool, List[str]]:
        """
        Validate changelog format.
        
        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []
        
        if not self.changelog_path.exists():
            return False, ["CHANGELOG.md not found"]
        
        content = self.changelog_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        # Check header
        if not lines[0].startswith("# Changelog"):
            issues.append("Missing '# Changelog' header")
        
        # Check for Unreleased section
        if "## [Unreleased]" not in content:
            issues.append("Missing [Unreleased] section")
        
        # Check version format
        version_pattern = r"## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}"
        versions = re.findall(version_pattern, content)
        if not versions:
            issues.append("No properly formatted version entries found")
        
        # Check for common categories
        expected_categories = ["### Added", "### Changed", "### Fixed"]
        has_category = any(cat in content for cat in expected_categories)
        if not has_category:
            issues.append("No standard categories (Added/Changed/Fixed) found")
        
        return len(issues) == 0, issues
    
    def get_unreleased_content(self) -> str:
        """Get content under [Unreleased] section."""
        if not self.changelog_path.exists():
            return ""
        
        content = self.changelog_path.read_text(encoding="utf-8")
        
        # Find Unreleased section
        unreleased_match = re.search(
            r"## \[Unreleased\]\s*\n(.*?)(?=## \[|$)",
            content,
            re.DOTALL
        )
        
        if unreleased_match:
            return unreleased_match.group(1).strip()
        
        return ""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Changelog maintenance helper")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if changelog needs update"
    )
    parser.add_argument(
        "--suggest",
        action="store_true",
        help="Suggest changelog entries"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate changelog format"
    )
    
    args = parser.parse_args()
    
    helper = ChangelogHelper()
    
    if args.check:
        needs_update, reason = helper.check_needs_update()
        if needs_update:
            print(f"[WARN] Changelog may need update: {reason}")
            print("Run with --suggest to see recommended entries")
            sys.exit(1)
        else:
            print(f"[OK] Changelog check: {reason}")
            sys.exit(0)
    
    elif args.suggest:
        print(helper.suggest_entries())
        sys.exit(0)
    
    elif args.validate:
        is_valid, issues = helper.validate_format()
        if is_valid:
            print("[OK] Changelog format is valid")
            sys.exit(0)
        else:
            print("[WARN] Changelog format issues:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
    
    else:
        # Default: check and suggest if needed
        needs_update, reason = helper.check_needs_update()
        print(f"Status: {reason}")
        if needs_update:
            print("\n" + helper.suggest_entries())


if __name__ == "__main__":
    main()
