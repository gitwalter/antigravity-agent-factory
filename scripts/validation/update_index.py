#!/usr/bin/env python3
"""
Reactive Artifact Index Updater

Updates the cached artifact index when files change. Designed to be triggered
by file save events (VS Code RunOnSave) or git hooks.

Usage:
    python scripts/validation/update_index.py <file_path>    # Update for specific file
    python scripts/validation/update_index.py --full         # Full rebuild
    python scripts/validation/update_index.py --check        # Check if index is fresh

Architecture:
    - Detects artifact type from file path
    - Updates only the relevant section of the index
    - Uses fast file-based counting (no subprocess calls)
    - Writes to .agent/cache/artifact-index.json

Research Source:
    See knowledge/reactive-indexing-patterns.json for design rationale.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional


# =============================================================================
# CONSTANTS
# =============================================================================

CACHE_DIR = ".agent/cache"
INDEX_FILE = "artifact-index.json"
STALENESS_THRESHOLD = timedelta(hours=1)

# Directory to artifact type mapping
DIRECTORY_MAPPING = {
    ".agent/agents": "agents",
    ".agent/skills": "skills",
    "blueprints": "blueprints",
    "knowledge": "knowledge",
    "templates": "templates",
    "patterns": "patterns",
    "tests": "tests",
    "docs": "docs",
    "diagrams": "diagrams",
}


# =============================================================================
# INDEX MANAGER
# =============================================================================

class ArtifactIndexManager:
    """Manages the artifact index cache."""
    
    def __init__(self, root_path: Optional[Path] = None):
        if root_path is None:
            root_path = Path(__file__).parent.parent.parent
        self.root_path = root_path
        self.cache_path = root_path / CACHE_DIR / INDEX_FILE
    
    def load_index(self) -> dict[str, Any]:
        """Load the current index or create a new one."""
        if self.cache_path.exists():
            try:
                return json.loads(self.cache_path.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                pass
        
        return self._create_empty_index()
    
    def save_index(self, index: dict[str, Any]) -> None:
        """Save the index to disk."""
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        index["updated_at"] = datetime.utcnow().isoformat() + "Z"
        self.cache_path.write_text(
            json.dumps(index, indent=2, ensure_ascii=False) + "\n",
            encoding='utf-8'
        )
    
    def is_fresh(self) -> bool:
        """Check if the index is fresh (not stale)."""
        if not self.cache_path.exists():
            return False
        
        try:
            index = self.load_index()
            updated_at = datetime.fromisoformat(
                index.get("updated_at", "1970-01-01T00:00:00Z").rstrip("Z")
            )
            return (datetime.utcnow() - updated_at) < STALENESS_THRESHOLD
        except (ValueError, KeyError):
            return False
    
    def detect_artifact_type(self, file_path: str) -> Optional[str]:
        """Detect which artifact type a file belongs to."""
        # Normalize path
        path = file_path.replace("\\", "/")
        
        for directory, artifact_type in DIRECTORY_MAPPING.items():
            if path.startswith(directory + "/") or path.startswith("./" + directory + "/"):
                return artifact_type
        
        return None
    
    def update_artifact(self, artifact_type: str, index: dict[str, Any]) -> dict[str, Any]:
        """Update a specific artifact type in the index."""
        if artifact_type not in index.get("artifacts", {}):
            index.setdefault("artifacts", {})[artifact_type] = {}
        
        artifact = index["artifacts"][artifact_type]
        
        # Count based on artifact type
        if artifact_type == "agents":
            count = self._count_agents()
            artifact["count"] = count["core"]
            artifact["breakdown"] = count
        elif artifact_type == "skills":
            count = self._count_skills()
            artifact["count"] = count["core"]
            artifact["breakdown"] = count
        elif artifact_type == "tests":
            count = self._count_tests()
            artifact["count"] = count["total"]
            artifact["breakdown"] = {k: v for k, v in count.items() if k != "total"}
        else:
            artifact["count"] = self._count_files(artifact_type)
        
        artifact["last_modified"] = datetime.utcnow().isoformat() + "Z"
        
        return index
    
    def full_rebuild(self) -> dict[str, Any]:
        """Rebuild the entire index."""
        index = self._create_empty_index()
        
        for artifact_type in DIRECTORY_MAPPING.values():
            index = self.update_artifact(artifact_type, index)
        
        return index
    
    # =========================================================================
    # COUNTING METHODS
    # =========================================================================
    
    def _count_agents(self) -> dict[str, int]:
        """Count agent files."""
        agents_dir = self.root_path / ".agent" / "agents"
        if not agents_dir.exists():
            return {"core": 0, "pm": 0}
        
        core_count = len(list(agents_dir.glob("*.md")))
        pm_dir = agents_dir / "pm"
        pm_count = len(list(pm_dir.glob("*.md"))) if pm_dir.exists() else 0
        
        return {"core": core_count, "pm": pm_count}
    
    def _count_skills(self) -> dict[str, int]:
        """Count skill directories."""
        skills_dir = self.root_path / ".agent" / "skills"
        if not skills_dir.exists():
            return {"core": 0, "pm": 0}
        
        # Count directories with SKILL.md (excluding pm/)
        core_count = 0
        pm_count = 0
        
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                if skill_dir.name == "pm":
                    # Count PM skills
                    for pm_skill in skill_dir.iterdir():
                        if pm_skill.is_dir() and (pm_skill / "SKILL.md").exists():
                            pm_count += 1
                elif (skill_dir / "SKILL.md").exists():
                    core_count += 1
        
        return {"core": core_count, "pm": pm_count}
    
    def _count_tests(self) -> dict[str, int]:
        """Count test functions using fast file-based method."""
        tests_dir = self.root_path / "tests"
        if not tests_dir.exists():
            return {"total": 0, "unit": 0, "integration": 0, "validation": 0}
        
        pattern = re.compile(r"^\s*(?:async\s+)?def\s+(test_\w+)", re.MULTILINE)
        
        counts = {"total": 0}
        
        # Count by subdirectory
        for subdir in ["unit", "integration", "validation", "guardian", "memory"]:
            subdir_path = tests_dir / subdir
            if subdir_path.exists():
                count = 0
                for py_file in subdir_path.rglob("test_*.py"):
                    try:
                        content = py_file.read_text(encoding='utf-8', errors='ignore')
                        count += len(pattern.findall(content))
                    except (OSError, IOError):
                        continue
                counts[subdir] = count
                counts["total"] += count
        
        return counts
    
    def _count_files(self, artifact_type: str) -> int:
        """Generic file count for an artifact type."""
        patterns = {
            "blueprints": ("blueprints", "*/blueprint.json"),
            "knowledge": ("knowledge", "*.json"),
            "templates": ("templates", "**/*"),
            "patterns": ("patterns", "*/*.json"),
            "docs": ("docs", "*.md"),
            "diagrams": ("diagrams", "*.md"),
        }
        
        if artifact_type not in patterns:
            return 0
        
        directory, glob_pattern = patterns[artifact_type]
        dir_path = self.root_path / directory
        
        if not dir_path.exists():
            return 0
        
        # Exclude common non-artifact files
        exclude = {"README.md", "manifest.json", "__init__.py"}
        
        count = 0
        for path in dir_path.glob(glob_pattern):
            if path.is_file() and path.name not in exclude:
                count += 1
        
        return count
    
    def _create_empty_index(self) -> dict[str, Any]:
        """Create an empty index structure."""
        return {
            "schema_version": "1.0.0",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "description": "Cached artifact counts for fast pre-commit validation. Auto-generated.",
            "artifacts": {}
        }


# =============================================================================
# CLI
# =============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Reactive Artifact Index Updater",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s src/.agent/agents/new-agent.md  # Update agents after adding new agent
    %(prog)s --full                           # Rebuild entire index
    %(prog)s --check                          # Check if index is fresh
        """
    )
    parser.add_argument("file", nargs="?", help="File that triggered the update")
    parser.add_argument("--full", action="store_true", help="Full index rebuild")
    parser.add_argument("--check", action="store_true", help="Check if index is fresh")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    
    args = parser.parse_args()
    
    manager = ArtifactIndexManager()
    
    # Check freshness
    if args.check:
        is_fresh = manager.is_fresh()
        if not args.quiet:
            status = "fresh" if is_fresh else "stale"
            print(f"Index is {status}")
        return 0 if is_fresh else 1
    
    # Full rebuild
    if args.full:
        if not args.quiet:
            print("Rebuilding full index...")
        index = manager.full_rebuild()
        manager.save_index(index)
        if not args.quiet:
            print(f"Index rebuilt with {len(index['artifacts'])} artifact types")
        return 0
    
    # Update for specific file
    if args.file:
        artifact_type = manager.detect_artifact_type(args.file)
        
        if artifact_type is None:
            if not args.quiet:
                print(f"File {args.file} does not map to any artifact type")
            return 0
        
        if not args.quiet:
            print(f"Updating {artifact_type} index...")
        
        index = manager.load_index()
        index = manager.update_artifact(artifact_type, index)
        manager.save_index(index)
        
        if not args.quiet:
            count = index["artifacts"][artifact_type].get("count", 0)
            print(f"Updated {artifact_type}: {count}")
        
        return 0
    
    # No arguments - show help
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
