#!/usr/bin/env python3
"""
README Project Structure Validator

Validates that the project structure documented in README.md matches
the actual filesystem structure. Can also generate updated structure.

Usage:
    python scripts/validation/validate_readme_structure.py --check      # Validate only
    python scripts/validation/validate_readme_structure.py --generate   # Generate structure
    python scripts/validation/validate_readme_structure.py --update     # Update README in place
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


class StructureValidator:
    """
    Validates and generates project structure documentation.
    
    Scans the filesystem and compares against README.md documentation,
    or generates updated structure sections.
    
    Attributes:
        root_path (Path): Root directory of the project.
        readme_path (Path): Path to README.md file.
        ignore_patterns (list): Patterns to ignore during scanning.
    """
    
    # Directories to ignore when scanning
    IGNORE_DIRS = {
        '__pycache__', '.git', 'node_modules', '.pytest_cache',
        '.mypy_cache', '.ruff_cache', 'dist', 'build', '.eggs',
        '*.egg-info', '.tox', '.coverage', 'htmlcov', '.venv', 'venv'
    }
    
    # Files to ignore
    IGNORE_FILES = {
        '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo', '.gitkeep'
    }
    
    def __init__(self, root_path: Optional[Path] = None):
        """
        Initialize the validator.
        
        Args:
            root_path: Root directory of the project. Defaults to script's parent's parent.
        """
        if root_path is None:
            root_path = Path(__file__).parent.parent.parent
        self.root_path = root_path
        self.readme_path = root_path / "README.md"
    
    def _should_ignore(self, path: Path) -> bool:
        """
        Check if a path should be ignored.
        
        Args:
            path: Path to check.
            
        Returns:
            True if the path should be ignored, False otherwise.
        """
        name = path.name
        if path.is_dir():
            return name in self.IGNORE_DIRS or name.startswith('.')
        return name in self.IGNORE_FILES or name.endswith('.pyc')
    
    def _count_files_by_extension(self, directory: Path, extension: str) -> int:
        """
        Count files with a specific extension in a directory tree.
        
        Args:
            directory: Directory to search.
            extension: File extension to count (e.g., '.json').
            
        Returns:
            Number of files with the given extension.
        """
        count = 0
        for item in directory.rglob(f"*{extension}"):
            if not any(p.name in self.IGNORE_DIRS for p in item.parents):
                count += 1
        return count
    
    def scan_agents(self) -> dict:
        """
        Scan .agent/agents/ directory.        
        Returns:
            Dictionary with agent count and list of agent names.
        """
        agents_dir = self.root_path / ".agent" / "agents"        if not agents_dir.exists():
            return {"count": 0, "agents": []}
        
        agents = sorted([
            f.stem for f in agents_dir.glob("*.md")
            if not self._should_ignore(f)
        ])
        return {"count": len(agents), "agents": agents}
    
    def scan_skills(self) -> dict:
        """
        Scan .agent/skills/ directory.        
        Returns:
            Dictionary with skill count and list of skill names.
        """
        skills_dir = self.root_path / ".agent" / "skills"        if not skills_dir.exists():
            return {"count": 0, "skills": []}
        
        skills = sorted([
            d.name for d in skills_dir.iterdir()
            if d.is_dir() and not self._should_ignore(d) and (d / "SKILL.md").exists()
        ])
        return {"count": len(skills), "skills": skills}
    
    def scan_blueprints(self) -> dict:
        """
        Scan blueprints/ directory.
        
        Returns:
            Dictionary with blueprint count and list of blueprint names.
        """
        blueprints_dir = self.root_path / "blueprints"
        if not blueprints_dir.exists():
            return {"count": 0, "blueprints": []}
        
        blueprints = sorted([
            d.name for d in blueprints_dir.iterdir()
            if d.is_dir() and not self._should_ignore(d) and (d / "blueprint.json").exists()
        ])
        return {"count": len(blueprints), "blueprints": blueprints}
    
    def scan_patterns(self) -> dict:
        """
        Scan patterns/ directory.
        
        Returns:
            Dictionary with pattern categories and file counts.
        """
        patterns_dir = self.root_path / "patterns"
        if not patterns_dir.exists():
            return {"categories": [], "total_files": 0}
        
        categories = {}
        for d in sorted(patterns_dir.iterdir()):
            if d.is_dir() and not self._should_ignore(d):
                files = list(d.glob("*.json"))
                categories[d.name] = [f.name for f in sorted(files)]
        
        total = sum(len(files) for files in categories.values())
        return {"categories": categories, "total_files": total}
    
    def scan_knowledge(self) -> dict:
        """
        Scan knowledge/ directory.
        
        Returns:
            Dictionary with knowledge file count and list of files.
        """
        knowledge_dir = self.root_path / "knowledge"
        if not knowledge_dir.exists():
            return {"count": 0, "files": []}
        
        files = sorted([f.name for f in knowledge_dir.glob("*.json")])
        return {"count": len(files), "files": files}
    
    def scan_templates(self) -> dict:
        """
        Scan templates/ directory.
        
        Returns:
            Dictionary with template categories and file counts.
        """
        templates_dir = self.root_path / "templates"
        if not templates_dir.exists():
            return {"categories": [], "total_files": 0}
        
        categories = {}
        for d in sorted(templates_dir.iterdir()):
            if d.is_dir() and not self._should_ignore(d):
                files = list(d.rglob("*.tmpl")) + list(d.rglob("*.md"))
                categories[d.name] = len(files)
        
        total = sum(categories.values())
        return {"categories": categories, "total_files": total}
    
    def scan_all(self) -> dict:
        """
        Scan all project components.
        
        Returns:
            Complete structure dictionary with all scanned components.
        """
        return {
            "agents": self.scan_agents(),
            "skills": self.scan_skills(),
            "blueprints": self.scan_blueprints(),
            "patterns": self.scan_patterns(),
            "knowledge": self.scan_knowledge(),
            "templates": self.scan_templates(),
        }
    
    def generate_structure_markdown(self) -> str:
        """
        Generate the project structure markdown section.
        
        Returns:
            Formatted markdown string for the project structure section.
        """
        data = self.scan_all()
        
        # Build skills list with selected descriptions
        skills_list = []
        for skill in data["skills"]["skills"][:7]:  # Show first 7 explicitly
            skills_list.append(f"│       ├── {skill}/")
        skills_list.append("│       └── ...                       # + more skills")
        
        # Build patterns list
        pattern_cats = list(data["patterns"]["categories"].keys())
        
        # Build blueprints list
        blueprints = data["blueprints"]["blueprints"]
        
        # Use thresholds for sustainable counts that don't break when repo grows
        patterns_threshold = self._round_to_threshold(data["patterns"]["total_files"])
        knowledge_threshold = self._round_to_threshold(data["knowledge"]["count"])
        templates_threshold = self._round_to_threshold(data["templates"]["total_files"])
        
        structure = f'''```
cursor-agent-factory/
├── .agent/│   ├── agents/                  # Factory's own agents ({data["agents"]["count"]} agents)
│   │   └── *.md                 # {", ".join(data["agents"]["agents"][:3])}, etc.
│   └── skills/                  # Factory's own skills ({data["skills"]["count"]} skills)
{chr(10).join(skills_list)}
├── patterns/                    # Reusable patterns ({patterns_threshold}+ files)
│   ├── axioms/                  # Layer 0 axiom definitions
│   ├── principles/              # Layer 2 principle patterns
│   ├── methodologies/           # Layer 3 methodology templates
│   ├── enforcement/             # Enforcement patterns
│   ├── practices/               # Practice patterns
│   ├── agents/                  # Agent pattern definitions
│   ├── skills/                  # Skill pattern definitions
│   ├── games/                   # Workshop game definitions
│   ├── workshops/               # Workshop pattern definitions
│   ├── team-formats/            # Team size adaptations
│   ├── stacks/                  # Stack blueprint patterns
│   ├── templates/               # Template patterns
│   └── workflows/               # Workflow patterns
├── blueprints/                  # Technology stack blueprints ({data["blueprints"]["count"]} blueprints)
│   ├── python-fastapi/
│   ├── python-streamlit/
│   ├── ai-agent-development/
│   ├── multi-agent-systems/
│   ├── typescript-react/
│   ├── nextjs-fullstack/
│   ├── java-spring/
│   ├── kotlin-spring/
│   ├── csharp-dotnet/
│   ├── n8n-automation/
│   ├── sap-abap/
│   ├── sap-rap/
│   ├── sap-cap/
│   └── sap-cpi-pi/
├── knowledge/                   # Reference data ({knowledge_threshold}+ files)
│   └── *.json                   # Stack, workflow, MCP, security, AI patterns
├── templates/                   # Code and document templates ({templates_threshold}+ files)
│   ├── factory/                 # Factory templates (cursorrules, PURPOSE.md, etc.)│   ├── ai/                      # AI agent templates
│   ├── python/                  # Python templates (FastAPI, Streamlit)
│   ├── typescript/              # TypeScript templates (Next.js)
│   ├── java/                    # Java Spring templates
│   ├── csharp/                  # C# Clean Architecture templates
│   ├── abap/                    # SAP ABAP/RAP templates
│   ├── cap/                     # SAP CAP templates
│   ├── integration/             # SAP CPI/PI integration templates
│   ├── automation/              # n8n automation templates
│   ├── workflows/               # CI/CD workflow templates
│   ├── methodology/             # Methodology templates
│   └── docs/                    # Documentation templates
├── docs/                        # Documentation
│   ├── reference/               # Detailed reference docs
│   ├── research/                # Research paper series
│   ├── examples/                # Example walkthroughs
│   └── *.md                     # Guides and tutorials
├── diagrams/                    # Architecture diagrams (Mermaid)
├── scripts/                     # Utility scripts
├── cli/                         # CLI interface
│   └── factory_cli.py
├── tests/                       # Test suite
│   ├── unit/
│   ├── integration/
│   ├── validation/
│   └── fixtures/
├── .github/
│   └── workflows/               # CI/CD workflows
├── .agentrules                 # Factory behavior rules├── CHANGELOG.md                 # Version history
└── README.md                    # This file
```'''
        return structure
    
    def _round_to_threshold(self, count: int) -> int:
        """
        Round count down to nearest threshold for sustainable documentation.
        
        Uses thresholds: 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, etc.
        This allows the repo to grow without breaking tests.
        
        Args:
            count: Actual count to round.
            
        Returns:
            Threshold value (count rounded down to nearest threshold).
        """
        thresholds = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 300, 500]
        for i, threshold in enumerate(thresholds):
            if count < threshold:
                return thresholds[i - 1] if i > 0 else 0
        return thresholds[-1]
    
    def generate_counts_summary(self) -> dict:
        """
        Generate a summary of component counts for validation.
        
        Returns:
            Dictionary with component counts.
        """
        data = self.scan_all()
        return {
            "agents": data["agents"]["count"],
            "skills": data["skills"]["count"],
            "blueprints": data["blueprints"]["count"],
            "patterns": data["patterns"]["total_files"],
            "knowledge": data["knowledge"]["count"],
            "templates": data["templates"]["total_files"],
        }
    
    def extract_readme_counts(self) -> dict:
        """
        Extract component counts from README.md.
        
        Handles both exact counts (e.g., "14 skills") and threshold counts
        (e.g., "50+ files"). Threshold counts are marked with is_threshold=True.
        
        Returns:
            Dictionary with counts as documented in README.
            Each value is a dict with 'count' and 'is_threshold' keys.
        """
        if not self.readme_path.exists():
            return {}
        
        content = self.readme_path.read_text(encoding="utf-8")
        counts = {}
        
        # Extract patterns - handles both "14 skills" and "50+ files" formats
        patterns = [
            (r"skills/\s*#.*?\((\d+)\s*skills\)", "skills"),
            (r"agents/\s*#.*?\((\d+)\s*agents\)", "agents"),
            (r"blueprints/\s*#.*?\((\d+)\s*blueprints\)", "blueprints"),
            (r"knowledge/\s*#.*?\((\d+)\+?\s*files\)", "knowledge"),
            (r"patterns/\s*#.*?\((\d+)\+?\s*files\)", "patterns"),
            (r"templates/\s*#.*?\((\d+)\+?\s*files\)", "templates"),
        ]
        
        for pattern, key in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                count_str = match.group(0)
                is_threshold = '+' in count_str
                counts[key] = {
                    'count': int(match.group(1)),
                    'is_threshold': is_threshold
                }
        
        return counts
    
    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate README structure against actual filesystem.
        
        For threshold counts (e.g., "50+ files"), validates actual >= documented.
        For exact counts (e.g., "14 blueprints"), validates actual == documented.
        
        Returns:
            Tuple of (is_valid, list of discrepancy messages).
        """
        actual = self.generate_counts_summary()
        documented = self.extract_readme_counts()
        
        discrepancies = []
        
        for key, actual_count in actual.items():
            if key in documented:
                doc_info = documented[key]
                doc_count = doc_info['count']
                is_threshold = doc_info['is_threshold']
                
                if is_threshold:
                    # Threshold count: actual must be >= documented minimum
                    if actual_count < doc_count:
                        discrepancies.append(
                            f"{key}: README says {doc_count}+ (minimum), actual is {actual_count} (below minimum!)"
                        )
                else:
                    # Exact count: must match exactly
                    if actual_count != doc_count:
                        discrepancies.append(
                            f"{key}: README says {doc_count}, actual is {actual_count}"
                        )
            else:
                discrepancies.append(
                    f"{key}: Not found in README (actual: {actual_count})"
                )
        
        return len(discrepancies) == 0, discrepancies
    
    def update_readme(self) -> bool:
        """
        Update the README.md with correct project structure.
        
        Returns:
            True if updated successfully, False otherwise.
        """
        if not self.readme_path.exists():
            print(f"Error: README.md not found at {self.readme_path}")
            return False
        
        content = self.readme_path.read_text(encoding="utf-8")
        
        # Find the project structure section
        # Look for "## Project Structure" followed by a code block
        pattern = r'(## Project Structure\s*\n\s*```[\s\S]*?```)'
        
        new_structure = "## Project Structure\n\n" + self.generate_structure_markdown()
        
        if re.search(pattern, content):
            updated = re.sub(pattern, new_structure, content, count=1)
        else:
            print("Warning: Could not find Project Structure section to update")
            return False
        
        self.readme_path.write_text(updated, encoding="utf-8")
        return True


def main():
    """Main entry point for the validation script."""
    parser = argparse.ArgumentParser(
        description="Validate or update README project structure"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate README against actual structure (exit 1 if mismatch)"
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate and print the correct structure markdown"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update README.md in place with correct structure"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output scan results as JSON"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Project root directory (default: script's parent's parent)"
    )
    
    args = parser.parse_args()
    
    # Default to check if no action specified
    if not any([args.check, args.generate, args.update, args.json]):
        args.check = True
    
    validator = StructureValidator(args.root)
    
    if args.json:
        data = validator.scan_all()
        print(json.dumps(data, indent=2))
        return 0
    
    if args.generate:
        print(validator.generate_structure_markdown())
        return 0
    
    if args.update:
        if validator.update_readme():
            print("README.md updated successfully")
            # Run validation after update
            is_valid, _ = validator.validate()
            if is_valid:
                print("Validation passed")
                return 0
            else:
                print("Warning: Validation still shows discrepancies after update")
                return 1
        else:
            print("Failed to update README.md")
            return 1
    
    if args.check:
        is_valid, discrepancies = validator.validate()
        
        if is_valid:
            print("[OK] README project structure is up to date")
            counts = validator.generate_counts_summary()
            for key, count in counts.items():
                print(f"  {key}: {count}")
            return 0
        else:
            print("[FAIL] README project structure is OUT OF DATE")
            print("\nDiscrepancies found:")
            for d in discrepancies:
                print(f"  - {d}")
            print("\nRun with --update to fix, or --generate to see correct structure")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
