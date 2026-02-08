#!/usr/bin/env python3
"""
Generate a structured test catalog from the test suite.

This script scans the tests/ directory, extracts metadata from test files
using Python's AST module, and generates a comprehensive TEST_CATALOG.md
document with test counts, descriptions, and structure.

Usage:
    python scripts/docs/generate_test_catalog.py [--check] [--output PATH]

Options:
    --check     Check if catalog is up-to-date without writing
    --output    Custom output path (default: docs/TEST_CATALOG.md)
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


@dataclass
class TestMethod:
    """Represents a single test method."""
    
    name: str
    docstring: str = ""
    markers: list[str] = field(default_factory=list)


@dataclass
class TestClass:
    """Represents a test class containing test methods."""
    
    name: str
    docstring: str = ""
    methods: list[TestMethod] = field(default_factory=list)
    
    @property
    def test_count(self) -> int:
        """Return number of test methods in this class."""
        return len(self.methods)


@dataclass
class TestFile:
    """Represents a test file containing test classes and standalone functions."""
    
    path: Path
    module_docstring: str = ""
    classes: list[TestClass] = field(default_factory=list)
    standalone_tests: list[TestMethod] = field(default_factory=list)
    
    @property
    def test_count(self) -> int:
        """Return total number of tests in this file."""
        class_tests = sum(c.test_count for c in self.classes)
        return class_tests + len(self.standalone_tests)
    
    @property
    def filename(self) -> str:
        """Return just the filename."""
        return self.path.name


@dataclass
class TestCategory:
    """Represents a category of tests (e.g., unit, integration)."""
    
    name: str
    directory: str
    files: list[TestFile] = field(default_factory=list)
    
    @property
    def file_count(self) -> int:
        """Return number of test files in this category."""
        return len(self.files)
    
    @property
    def test_count(self) -> int:
        """Return total number of tests in this category."""
        return sum(f.test_count for f in self.files)


class TestCatalogGenerator:
    """
    Generates a structured test catalog from the test suite.
    
    Scans test files using AST to extract:
    - Module-level docstrings
    - Test class names and docstrings
    - Test method names and docstrings
    - Pytest markers (when possible)
    """
    
    # Test categories to scan, in order
    CATEGORIES = [
        ("Unit Tests", "unit"),
        ("Integration Tests", "integration"),
        ("Validation Tests", "validation"),
        ("Guardian Tests", "guardian"),
        ("Memory Tests", "memory"),
        ("Library Tests", "lib"),
    ]
    
    def __init__(self, tests_dir: Path):
        """
        Initialize the generator.
        
        Args:
            tests_dir: Path to the tests/ directory
        """
        self.tests_dir = tests_dir
        self.categories: list[TestCategory] = []
    
    def scan_all(self) -> None:
        """Scan all test categories and populate the categories list."""
        self.categories = []
        
        for cat_name, cat_dir in self.CATEGORIES:
            category = self._scan_category(cat_name, cat_dir)
            if category.files:
                self.categories.append(category)
    
    def _scan_category(self, name: str, directory: str) -> TestCategory:
        """
        Scan a single test category directory.
        
        Args:
            name: Display name for the category
            directory: Directory name relative to tests/
            
        Returns:
            TestCategory with all files scanned
        """
        category = TestCategory(name=name, directory=directory)
        cat_path = self.tests_dir / directory
        
        if not cat_path.exists():
            return category
        
        # Find all test files recursively
        test_files = sorted(cat_path.rglob("test_*.py"))
        
        for test_file in test_files:
            parsed = self._parse_test_file(test_file)
            if parsed:
                category.files.append(parsed)
        
        return category
    
    def _parse_test_file(self, filepath: Path) -> Optional[TestFile]:
        """
        Parse a test file using AST to extract metadata.
        
        Args:
            filepath: Path to the test file
            
        Returns:
            TestFile with extracted metadata, or None on error
        """
        try:
            source = filepath.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(filepath))
        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
            return None
        
        test_file = TestFile(path=filepath)
        
        # Extract module docstring
        test_file.module_docstring = ast.get_docstring(tree) or ""
        
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                # Parse test class
                test_class = self._parse_test_class(node)
                if test_class.methods:
                    test_file.classes.append(test_class)
            
            elif isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                # Parse standalone test function
                test_method = self._parse_test_method(node)
                test_file.standalone_tests.append(test_method)
        
        return test_file
    
    def _parse_test_class(self, node: ast.ClassDef) -> TestClass:
        """
        Parse a test class node.
        
        Args:
            node: AST ClassDef node
            
        Returns:
            TestClass with methods extracted
        """
        test_class = TestClass(
            name=node.name,
            docstring=ast.get_docstring(node) or ""
        )
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                test_method = self._parse_test_method(item)
                test_class.methods.append(test_method)
        
        return test_class
    
    def _parse_test_method(self, node: ast.FunctionDef) -> TestMethod:
        """
        Parse a test method/function node.
        
        Args:
            node: AST FunctionDef node
            
        Returns:
            TestMethod with docstring and markers
        """
        markers = []
        
        # Extract pytest markers from decorators
        for decorator in node.decorator_list:
            marker = self._extract_marker(decorator)
            if marker:
                markers.append(marker)
        
        return TestMethod(
            name=node.name,
            docstring=ast.get_docstring(node) or "",
            markers=markers
        )
    
    def _extract_marker(self, decorator: ast.expr) -> Optional[str]:
        """
        Extract pytest marker name from a decorator.
        
        Args:
            decorator: AST decorator node
            
        Returns:
            Marker name if it's a pytest marker, None otherwise
        """
        # Handle @pytest.mark.name
        if isinstance(decorator, ast.Attribute):
            if isinstance(decorator.value, ast.Attribute):
                if (isinstance(decorator.value.value, ast.Name) and 
                    decorator.value.value.id == "pytest" and
                    decorator.value.attr == "mark"):
                    return decorator.attr
        
        # Handle @pytest.mark.name(args)
        if isinstance(decorator, ast.Call):
            return self._extract_marker(decorator.func)
        
        return None
    
    def get_total_stats(self) -> dict[str, int]:
        """
        Get total statistics across all categories.
        
        Returns:
            Dictionary with total_files and total_tests
        """
        total_files = sum(c.file_count for c in self.categories)
        total_tests = sum(c.test_count for c in self.categories)
        return {"total_files": total_files, "total_tests": total_tests}
    
    def generate_markdown(self) -> str:
        """
        Generate the complete markdown catalog.
        
        Returns:
            Markdown string for the catalog
        """
        lines = []
        stats = self.get_total_stats()
        
        # Header
        lines.append("# Test Catalog")
        lines.append("")
        lines.append(f"> **Auto-generated** from test suite on {datetime.now().strftime('%Y-%m-%d %H:%M')}.")
        lines.append("> Do not edit manually. Run `python scripts/docs/generate_test_catalog.py` to regenerate.")
        lines.append("")
        
        # Overview
        lines.append("## Overview")
        lines.append("")
        lines.append(f"The test suite contains **{stats['total_tests']} tests** across **{stats['total_files']} files**.")
        lines.append("")
        
        # Summary table
        lines.append("### Summary by Category")
        lines.append("")
        lines.append("| Category | Files | Tests |")
        lines.append("|----------|-------|-------|")
        for category in self.categories:
            lines.append(f"| {category.name} | {category.file_count} | {category.test_count} |")
        lines.append(f"| **Total** | **{stats['total_files']}** | **{stats['total_tests']}** |")
        lines.append("")
        
        # Detailed sections for each category
        for category in self.categories:
            lines.extend(self._generate_category_section(category))
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*Part of the Cursor Agent Factory test suite documentation.*")
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_category_section(self, category: TestCategory) -> list[str]:
        """
        Generate markdown section for a category.
        
        Args:
            category: TestCategory to document
            
        Returns:
            List of markdown lines
        """
        lines = []
        
        lines.append(f"## {category.name}")
        lines.append("")
        lines.append(f"**Directory:** `tests/{category.directory}/`")
        lines.append(f"**Files:** {category.file_count} | **Tests:** {category.test_count}")
        lines.append("")
        
        for test_file in category.files:
            lines.extend(self._generate_file_section(test_file, category.directory))
        
        return lines
    
    def _generate_file_section(self, test_file: TestFile, category_dir: str) -> list[str]:
        """
        Generate markdown section for a test file.
        
        Args:
            test_file: TestFile to document
            category_dir: Category directory for relative path
            
        Returns:
            List of markdown lines
        """
        lines = []
        
        # File header with relative path
        rel_path = test_file.path.relative_to(self.tests_dir)
        lines.append(f"### {test_file.filename}")
        lines.append("")
        
        # Purpose from module docstring
        if test_file.module_docstring:
            # Take first paragraph only
            purpose = test_file.module_docstring.split("\n\n")[0].strip()
            purpose = purpose.replace("\n", " ")
            lines.append(f"**Purpose:** {purpose}")
            lines.append("")
        
        lines.append(f"**Path:** `tests/{rel_path}`")
        lines.append(f"**Tests:** {test_file.test_count}")
        lines.append("")
        
        # Test classes table
        if test_file.classes:
            lines.append("| Class | Tests | Description |")
            lines.append("|-------|-------|-------------|")
            for test_class in test_file.classes:
                desc = test_class.docstring.split("\n")[0] if test_class.docstring else ""
                lines.append(f"| `{test_class.name}` | {test_class.test_count} | {desc} |")
            lines.append("")
        
        # Standalone tests
        if test_file.standalone_tests:
            lines.append("**Standalone Tests:**")
            lines.append("")
            for test in test_file.standalone_tests:
                desc = f" - {test.docstring.split(chr(10))[0]}" if test.docstring else ""
                lines.append(f"- `{test.name}`{desc}")
            lines.append("")
        
        return lines


def get_factory_root() -> Path:
    """
    Get the factory root directory.
    
    Returns:
        Path to the factory root
    """
    # Try relative to this script
    script_path = Path(__file__).resolve()
    factory_root = script_path.parent.parent.parent
    
    if (factory_root / "tests").exists():
        return factory_root
    
    # Fallback to current working directory
    cwd = Path.cwd()
    if (cwd / "tests").exists():
        return cwd
    
    raise RuntimeError("Could not find factory root with tests/ directory")


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Generate test catalog from test suite"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if catalog is up-to-date without writing"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Custom output path (default: docs/TEST_CATALOG.md)"
    )
    args = parser.parse_args()
    
    try:
        factory_root = get_factory_root()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    tests_dir = factory_root / "tests"
    output_path = args.output or (factory_root / "docs" / "TEST_CATALOG.md")
    
    print(f"Scanning tests in: {tests_dir}")
    
    # Generate catalog
    generator = TestCatalogGenerator(tests_dir)
    generator.scan_all()
    
    stats = generator.get_total_stats()
    print(f"Found {stats['total_tests']} tests in {stats['total_files']} files")
    
    new_content = generator.generate_markdown()
    
    if args.check:
        # Check mode: compare with existing
        if output_path.exists():
            existing_content = output_path.read_text(encoding="utf-8")
            
            # Compare ignoring timestamp line
            def normalize(content: str) -> str:
                lines = content.split("\n")
                # Skip the auto-generated timestamp line for comparison
                return "\n".join(
                    line for line in lines 
                    if not line.startswith("> **Auto-generated**")
                )
            
            if normalize(existing_content) != normalize(new_content):
                print(f"\nTest catalog is OUT OF SYNC!")
                print(f"Run 'python scripts/docs/generate_test_catalog.py' to update")
                return 1
            else:
                print(f"\nTest catalog is up-to-date: {output_path}")
                return 0
        else:
            print(f"\nTest catalog does not exist: {output_path}")
            print(f"Run 'python scripts/docs/generate_test_catalog.py' to create")
            return 1
    
    # Write mode
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(new_content, encoding="utf-8")
    print(f"\nGenerated: {output_path}")
    
    # Print category breakdown
    print("\nCategory breakdown:")
    for category in generator.categories:
        print(f"  {category.name}: {category.test_count} tests in {category.file_count} files")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
