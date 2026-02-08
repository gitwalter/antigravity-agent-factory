#!/usr/bin/env python3
"""
Unified Artifact Sync System

A configuration-driven system that automatically synchronizes artifact documentation
(counts, tables, lists, trees) with the actual filesystem state.

Sync Types:
- count: Update numeric counts in markdown (e.g., "(27 blueprints)")
- tree_annotation: Update counts in directory tree diagrams
- markdown_table: Validate/update markdown tables with artifact lists
- json_field: Update JSON file fields with counts
- json_list: Validate/update JSON arrays with artifact entries
- category_counts: Update categorized counts (like test categories)

Usage:
    python scripts/validation/sync_artifacts.py                    # Check all
    python scripts/validation/sync_artifacts.py --sync             # Sync all
    python scripts/validation/sync_artifacts.py --sync agents      # Sync specific artifact
    python scripts/validation/sync_artifacts.py --dirs .agent/agents blueprints  # Sync by dirs
"""

import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, NamedTuple, Optional


# =============================================================================
# DATA STRUCTURES
# =============================================================================

class CategoryTestCounts(NamedTuple):
    """Counts of tests organized by category.
    
    This is the single source of truth for test count data structures.
    Used by both sync_artifacts.py and the deprecated sync_test_counts.py wrapper.
    
    Note: Named 'CategoryTestCounts' (not 'TestCountsByCategory') to avoid 
    pytest trying to collect it as a test class.
    """
    total: int
    unit: int
    integration: int
    validation: int
    guardian: int
    memory: int


# Backward compatibility alias
TestCountsByCategory = CategoryTestCounts


class ArtifactInfo(NamedTuple):
    """Information about a discovered artifact."""
    id: str
    path: Path
    metadata: dict[str, Any] = {}


@dataclass
class SyncTarget:
    """A target location to sync artifact information to."""
    type: str
    file: str
    pattern: str = ""
    replacement: str = ""
    section: str = ""
    json_path: str = ""
    columns: list[str] = field(default_factory=list)
    id_column: str = ""
    sync_mode: str = "full"
    categories: dict = field(default_factory=dict)
    key_field: str = ""
    line_pattern: str = ""
    annotation_pattern: str = ""


@dataclass
class ArtifactConfig:
    """Configuration for an artifact type."""
    name: str
    description: str
    source_dir: str
    pattern: str
    recursive: bool = False
    exclude: list[str] = field(default_factory=list)
    id_extractor: str = "filename_stem"
    metadata_extractor: Optional[dict] = None
    file_types_only: bool = False
    count_method: str = "file_count"
    targets: list[SyncTarget] = field(default_factory=list)


@dataclass
class SyncResult:
    """Result of a sync operation."""
    artifact: str
    target_file: str
    target_type: str
    changed: bool
    old_value: Any
    new_value: Any
    message: str


# =============================================================================
# ARTIFACT SCANNER
# =============================================================================

class ArtifactScanner:
    """Scans directories for artifacts based on configuration."""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
    
    def scan(self, config: ArtifactConfig) -> list[ArtifactInfo]:
        """Scan for artifacts based on configuration."""
        source_dir = self.root_path / config.source_dir
        if not source_dir.exists():
            return []
        
        artifacts = []
        
        if config.recursive:
            matches = list(source_dir.rglob(config.pattern))
        else:
            matches = list(source_dir.glob(config.pattern))
        
        for path in matches:
            # Check exclusions
            if self._should_exclude(path, config.exclude, source_dir):
                continue
            
            # Check file_types_only
            if config.file_types_only and not path.is_file():
                continue
            
            # Extract ID
            artifact_id = self._extract_id(path, config.id_extractor, source_dir)
            
            # Extract metadata
            metadata = self._extract_metadata(path, config.metadata_extractor)
            
            # Create artifact info
            artifacts.append(ArtifactInfo(
                id=artifact_id,
                path=path,
                metadata=metadata
            ))
        
        return artifacts
    
    def _extract_metadata(self, path: Path, extractor_config: Optional[dict]) -> dict:
        """Extract metadata from file based on configuration."""
        if not extractor_config:
            return {}
        
        extractor_type = extractor_config.get("type")
        fields = extractor_config.get("fields", [])
        
        if extractor_type == "markdown_frontmatter":
            return self._extract_yaml_frontmatter(path, fields)
        
        return {}
    
    def _extract_yaml_frontmatter(self, path: Path, fields: list[str]) -> dict:
        """Extract YAML frontmatter from markdown file."""
        try:
            content = path.read_text(encoding='utf-8')
            
            # Check for YAML frontmatter (--- ... ---)
            if not content.startswith('---'):
                return {}
            
            # Find the closing ---
            lines = content.split('\n')
            end_idx = None
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_idx = i
                    break
            
            if end_idx is None:
                return {}
            
            # Parse YAML
            import yaml
            frontmatter_text = '\n'.join(lines[1:end_idx])
            frontmatter = yaml.safe_load(frontmatter_text) or {}
            
            # Extract requested fields
            metadata = {}
            for field in fields:
                if field in frontmatter:
                    metadata[field] = frontmatter[field]
            
            return metadata
        except Exception:
            return {}

    
    def count_pytest(self, test_dir: Optional[str] = None) -> int:
        """Count tests using pytest --collect-only.
        
        NOTE: This is slow (~2-5 seconds per call). Prefer count_test_functions()
        for pre-commit hooks and use this only in CI for accurate counts.
        """
        tests_path = self.root_path / "tests"
        if test_dir:
            tests_path = tests_path / test_dir
        
        if not tests_path.exists():
            return 0
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(tests_path), "--collect-only", "-q"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.root_path
            )
            
            match = re.search(r"(\d+) tests? collected", result.stdout)
            if match:
                return int(match.group(1))
            return 0
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            return 0
    
    def count_test_functions(self, test_dir: Optional[str] = None) -> int:
        """Fast count of test functions via file scanning.
        
        This is ~100x faster than count_pytest() because it uses regex
        matching on file contents rather than subprocess calls.
        
        Trade-off: May slightly differ from pytest (e.g., parametrized tests
        count as 1 here but multiple in pytest). Use count_pytest() in CI
        for authoritative counts.
        
        Args:
            test_dir: Optional subdirectory within tests/ to count.
                      If None, counts all tests.
        
        Returns:
            Number of test functions found.
        """
        tests_path = self.root_path / "tests"
        if test_dir:
            tests_path = tests_path / test_dir
        
        if not tests_path.exists():
            return 0
        
        # Pattern matches: def test_*, async def test_*
        pattern = re.compile(r"^\s*(?:async\s+)?def\s+(test_\w+)", re.MULTILINE)
        count = 0
        
        for py_file in tests_path.rglob("test_*.py"):
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                count += len(pattern.findall(content))
            except (OSError, IOError):
                # Skip files that can't be read
                continue
        
        return count
    
    def _should_exclude(self, path: Path, excludes: list[str], source_dir: Path) -> bool:
        """Check if path should be excluded."""
        rel_path = str(path.relative_to(source_dir)).replace('\\', '/')
        for exclude in excludes:
            exclude = exclude.replace('\\', '/')
            if exclude.endswith('/'):
                # Directory exclusion - check if any parent matches
                dir_name = exclude.rstrip('/')
                if rel_path.startswith(dir_name + '/') or f"/{dir_name}/" in f"/{rel_path}":
                    return True
                # Also check if path is inside the excluded directory
                for parent in path.relative_to(source_dir).parents:
                    if str(parent).replace('\\', '/') == dir_name:
                        return True
            else:
                # File/pattern exclusion
                if path.name == exclude or rel_path == exclude:
                    return True
        return False
    
    def _extract_id(self, path: Path, extractor: str, source_dir: Path) -> str:
        """Extract artifact ID based on extractor type."""
        if extractor == "filename_stem":
            return path.stem
        elif extractor == "parent_dir_name":
            return path.parent.name
        elif extractor == "relative_path":
            return str(path.relative_to(source_dir))
        else:
            return path.stem

    def scan_test_details(self, test_dir: str = "tests") -> list[dict]:
        """Scan test files and extract detailed test case metadata using AST.
        
        Returns:
            List of dicts containing:
            - file: Path relative to root
            - class: Class name (if any)
            - name: Function/Method name
            - docstring: First line of docstring (or empty)
        """
        tests_path = self.root_path / test_dir
        if not tests_path.exists():
            return []
            
        test_cases = []
        
        for py_file in tests_path.rglob("test_*.py"):
            try:
                tree = ast.parse(py_file.read_text(encoding='utf-8', errors='ignore'))
                rel_path = str(py_file.relative_to(self.root_path)).replace('\\', '/')
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                        # Find parent class if any
                        parent_class = ""
                        # Note: Simple walk doesn't give parent context easily, 
                        # but for our purpose we can iterate through body
                        pass # handled below with better iteration
                        
                # Improved iteration to capture class context
                for node in tree.body:
                    if isinstance(node, ast.ClassDef):
                        class_name = node.name
                        for item in node.body:
                            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name.startswith("test_"):
                                doc = ast.get_docstring(item)
                                test_cases.append({
                                    "file": rel_path,
                                    "class": class_name,
                                    "name": item.name,
                                    "docstring": doc.split('\n')[0] if doc else ""
                                })
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                        doc = ast.get_docstring(node)
                        test_cases.append({
                            "file": rel_path,
                            "class": "",
                            "name": node.name,
                            "docstring": doc.split('\n')[0] if doc else ""
                        })
                        
            except Exception:
                continue
                
        return sorted(test_cases, key=lambda x: (x["file"], x["class"], x["name"]))


# =============================================================================
# SYNC STRATEGIES
# =============================================================================

class SyncStrategy:
    """Base class for sync strategies."""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
    
    def sync(self, target: SyncTarget, count: int, artifacts: list[ArtifactInfo], 
             dry_run: bool = True) -> SyncResult:
        """Perform sync operation. Override in subclasses."""
        raise NotImplementedError


class CountSyncStrategy(SyncStrategy):
    """Syncs numeric counts in markdown files."""
    
    def sync(self, target: SyncTarget, count: int, artifacts: list[ArtifactInfo],
             dry_run: bool = True) -> SyncResult:
        file_path = self.root_path / target.file
        if not file_path.exists():
            return SyncResult(
                artifact="", target_file=target.file, target_type="count",
                changed=False, old_value=None, new_value=count,
                message=f"File not found: {target.file}"
            )
        
        content = file_path.read_text(encoding='utf-8')
        
        # Extract current count
        match = re.search(target.pattern, content)
        old_count = int(match.group(1)) if match else 0
        
        if old_count == count:
            return SyncResult(
                artifact="", target_file=target.file, target_type="count",
                changed=False, old_value=old_count, new_value=count,
                message="Already in sync"
            )
        
        # Build replacement
        replacement = target.replacement.format(count=count)
        
        if not dry_run:
            new_content = re.sub(target.pattern, replacement, content)
            file_path.write_text(new_content, encoding='utf-8')
        
        return SyncResult(
            artifact="", target_file=target.file, target_type="count",
            changed=True, old_value=old_count, new_value=count,
            message=f"Count: {old_count} -> {count}"
        )


class JsonFieldSyncStrategy(SyncStrategy):
    """Syncs counts to JSON file fields."""
    
    def sync(self, target: SyncTarget, count: int, artifacts: list[ArtifactInfo],
             dry_run: bool = True) -> SyncResult:
        file_path = self.root_path / target.file
        if not file_path.exists():
            return SyncResult(
                artifact="", target_file=target.file, target_type="json_field",
                changed=False, old_value=None, new_value=count,
                message=f"File not found: {target.file}"
            )
        
        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            return SyncResult(
                artifact="", target_file=target.file, target_type="json_field",
                changed=False, old_value=None, new_value=count,
                message=f"JSON parse error: {e}"
            )
        
        # Navigate to field using dot notation
        path_parts = target.json_path.split('.')
        current = data
        for part in path_parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        field_name = path_parts[-1]
        old_value = current.get(field_name, 0)
        
        if old_value == count:
            return SyncResult(
                artifact="", target_file=target.file, target_type="json_field",
                changed=False, old_value=old_value, new_value=count,
                message="Already in sync"
            )
        
        if not dry_run:
            current[field_name] = count
            file_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + '\n',
                encoding='utf-8'
            )
        
        return SyncResult(
            artifact="", target_file=target.file, target_type="json_field",
            changed=True, old_value=old_value, new_value=count,
            message=f"JSON field: {old_value} -> {count}"
        )


class CategoryCountsSyncStrategy(SyncStrategy):
    """Syncs categorized counts (like test categories)."""
    
    def __init__(self, root_path: Path, scanner: ArtifactScanner):
        super().__init__(root_path)
        self.scanner = scanner
    
    def sync(self, target: SyncTarget, count: int, artifacts: list[ArtifactInfo],
             dry_run: bool = True) -> SyncResult:
        file_path = self.root_path / target.file
        if not file_path.exists():
            return SyncResult(
                artifact="", target_file=target.file, target_type="category_counts",
                changed=False, old_value=None, new_value=None,
                message=f"File not found: {target.file}"
            )
        
        content = file_path.read_text(encoding='utf-8')
        new_content = content
        changes = []
        
        for category, config in target.categories.items():
            source_subdir = config.get("source_subdir", category)
            pattern = config.get("pattern", "")
            
            # Get actual count
            actual_count = self.scanner.count_pytest(source_subdir)
            
            # Extract current count
            match = re.search(pattern, content)
            old_count = int(match.group(1)) if match else 0
            
            if old_count != actual_count:
                changes.append(f"{category}: {old_count} -> {actual_count}")
                # Update in content
                replacement = pattern.replace("~?(\\d+)", f"~{actual_count}")
                replacement = replacement.replace("(\\d+)", str(actual_count))
                new_content = re.sub(pattern, f"| {category.title()} Tests | ~{actual_count} |", new_content, flags=re.IGNORECASE)
        
        if not changes:
            return SyncResult(
                artifact="", target_file=target.file, target_type="category_counts",
                changed=False, old_value=None, new_value=None,
                message="All categories in sync"
            )
        
        if not dry_run:
            file_path.write_text(new_content, encoding='utf-8')
        
        return SyncResult(
            artifact="", target_file=target.file, target_type="category_counts",
            changed=True, old_value=None, new_value=None,
            message="; ".join(changes)
        )


class TreeAnnotationSyncStrategy(SyncStrategy):
    """Syncs count annotations in directory tree diagrams."""
    
    def sync(self, target: SyncTarget, count: int, artifacts: list[ArtifactInfo],
             dry_run: bool = True) -> SyncResult:
        file_path = self.root_path / target.file
        if not file_path.exists():
            return SyncResult(
                artifact="", target_file=target.file, target_type="tree_annotation",
                changed=False, old_value=None, new_value=count,
                message=f"File not found: {target.file}"
            )
        
        content = file_path.read_text(encoding='utf-8')
        
        # Find lines containing the line_pattern and update annotation
        lines = content.split('\n')
        changed = False
        old_count = None
        
        for i, line in enumerate(lines):
            if target.line_pattern in line:
                match = re.search(target.annotation_pattern, line)
                if match:
                    old_count = int(match.group(1))
                    if old_count != count:
                        # Update the count in the annotation
                        new_line = re.sub(
                            target.annotation_pattern,
                            f"({count} " + target.annotation_pattern.split()[0].replace("\\(", "").replace("\\d+", str(count)) + ")",
                            line
                        )
                        lines[i] = new_line
                        changed = True
                break
        
        if not changed:
            return SyncResult(
                artifact="", target_file=target.file, target_type="tree_annotation",
                changed=False, old_value=old_count or count, new_value=count,
                message="Already in sync"
            )
        
        if not dry_run:
            file_path.write_text('\n'.join(lines), encoding='utf-8')
        
        return SyncResult(
            artifact="", target_file=target.file, target_type="tree_annotation",
            changed=True, old_value=old_count, new_value=count,
            message=f"Tree annotation: {old_count} -> {count}"
        )


class MarkdownTableSyncStrategy(SyncStrategy):
    """Syncs markdown tables with artifact lists."""
    
    def sync(self, target: SyncTarget, count: int, artifacts: list[ArtifactInfo],
             dry_run: bool = True) -> SyncResult:
        file_path = self.root_path / target.file
        if not file_path.exists():
            return SyncResult(
                artifact="", target_file=target.file, target_type="markdown_table",
                changed=False, old_value=None, new_value=count,
                message=f"File not found: {target.file}"
            )
        
        content = file_path.read_text(encoding='utf-8')
        
        # 1. Generate new table
        header = "| " + " | ".join(target.columns) + " |"
        separator = "| " + " | ".join(["---"] * len(target.columns)) + " |"
        
        rows = []
        # STABLE SORT: Sort by ID first, then by Path to ensure determinism 
        # especially when multiple files have the same ID (stem) in different dirs.
        # Use relative path to be independent of absolute checkout location (e.g. CI vs Local)
        sorted_artifacts = sorted(artifacts, key=lambda a: (a.id, str(a.path.relative_to(self.root_path)).replace('\\', '/')))
        
        for artifact in sorted_artifacts:
            row_data = []
            for col in target.columns:
                if col == target.id_column:
                    # Link formatting: [ID](link)
                    rel_path = str(artifact.path.relative_to(self.root_path)).replace('\\', '/')
                    row_data.append(f"[{artifact.id}](file:///{rel_path})")
                else:
                    # Metadata lookup
                    # 1. Try direct field match (e.g. "Description" -> metadata["description"])
                    # 2. Try lowercase match
                    val = artifact.metadata.get(col) or artifact.metadata.get(col.lower(), "")
                    # Escape pipes and remove newlines
                    val_str = str(val).replace("|", "\\|").replace("\n", " ")
                    row_data.append(val_str)
            
            rows.append("| " + " | ".join(row_data) + " |")
            
        new_table = f"{header}\n{separator}\n" + "\n".join(rows)
        
        # 2. Find and replace existing table
        # We look for the section header and then the table following it
        lines = content.split('\n')
        new_lines = []
        in_target_section = False
        table_replaced = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check for section header
            if target.section in line and line.startswith("#"):
                in_target_section = True
                new_lines.append(line)
                i += 1
                continue
            
            # If in section
            if in_target_section:
                # Check for end of section (next header)
                if line.startswith("#"):
                    if not table_replaced:
                        new_lines.append("")
                        new_lines.append(new_table)
                        new_lines.append("")
                        table_replaced = True
                    in_target_section = False
                    new_lines.append(line)
                    i += 1
                    continue
                
                if not table_replaced:
                    # Check if this line looks like a table start
                    if line.strip().startswith("|") and all(c in line for c in target.columns[:2]):
                        new_lines.append(new_table)
                        table_replaced = True
                        
                        # Skip existing table lines
                        while i < len(lines) and lines[i].strip().startswith("|"):
                            i += 1
                        continue
            
            new_lines.append(line)
            i += 1
            
        # If we reached EOF and still in section (or just finished section without table), append it
        if in_target_section and not table_replaced:
            new_lines.append("")
            new_lines.append(new_table)
            new_lines.append("")
            
        new_content = "\n".join(new_lines)
        
        if new_content == content:
             return SyncResult(
                artifact="", target_file=target.file, target_type="markdown_table",
                changed=False, old_value=len(rows), new_value=len(rows),
                message="Already in sync"
            )
            
        if not dry_run:
            file_path.write_text(new_content, encoding='utf-8')
            
        return SyncResult(
            artifact="", target_file=target.file, target_type="markdown_table",
            changed=True, old_value="?", new_value=len(rows),
            message=f"Table updated ({len(rows)} rows)"
        )


class CatalogSyncStrategy(SyncStrategy):
    """Syncs a comprehensive test catalog into a markdown file."""
    
    def __init__(self, root_path: Path, scanner: ArtifactScanner):
        super().__init__(root_path)
        self.scanner = scanner
        
    def sync(self, target: SyncTarget, count: int, artifacts: list[ArtifactInfo],
             dry_run: bool = True) -> SyncResult:
        file_path = self.root_path / target.file
        if not file_path.exists():
            return SyncResult(
                artifact="", target_file=target.file, target_type="catalog",
                changed=False, old_value=None, new_value=None,
                message=f"File not found: {target.file}"
            )
            
        test_cases = self.scanner.scan_test_details()
        
        # Generate Markdown
        lines = [
            "<!-- SYNC_START -->",
            "| File | Class | Test Case | Description |",
            "| --- | --- | --- | --- |"
        ]
        
        for tc in test_cases:
            file_link = f"[{Path(tc['file']).name}](file:///{tc['file']})"
            doc = tc['docstring'].replace("|", "\\|")
            lines.append(f"| {file_link} | {tc['class']} | `{tc['name']}` | {doc} |")
            
        lines.append("<!-- SYNC_END -->")
        new_catalog = "\n".join(lines)
        
        content = file_path.read_text(encoding='utf-8')
        
        # Replace between markers
        marker_start = "<!-- SYNC_START -->"
        marker_end = "<!-- SYNC_END -->"
        
        if marker_start in content and marker_end in content:
            pattern = f"{marker_start}.*?{marker_end}"
            new_content = re.sub(pattern, new_catalog, content, flags=re.DOTALL)
        else:
            # If markers missing, append or replace entirely
            new_content = content + "\n\n" + new_catalog
            
        if new_content == content:
            return SyncResult(
                artifact="", target_file=target.file, target_type="catalog",
                changed=False, old_value=len(test_cases), new_value=len(test_cases),
                message="Already in sync"
            )
            
        if not dry_run:
            file_path.write_text(new_content, encoding='utf-8')
            
        return SyncResult(
            artifact="", target_file=target.file, target_type="catalog",
            changed=True, old_value="?", new_value=len(test_cases),
            message=f"Catalog updated ({len(test_cases)} tests)"
        )


class SyncEngine:
    """Main orchestrator for artifact synchronization."""
    
    def __init__(self, root_path: Optional[Path] = None, config_path: Optional[Path] = None):
        if root_path is None:
            root_path = Path(__file__).parent.parent.parent
        self.root_path = root_path
        
        if config_path is None:
            config_path = root_path / "scripts" / "validation" / "sync_config.json"
        self.config_path = config_path
        
        self.scanner = ArtifactScanner(root_path)
        self.config = self._load_config()
        
        # Initialize strategies
        self.strategies: dict[str, SyncStrategy] = {
            "count": CountSyncStrategy(root_path),
            "json_field": JsonFieldSyncStrategy(root_path),
            "category_counts": CategoryCountsSyncStrategy(root_path, self.scanner),
            "tree_annotation": TreeAnnotationSyncStrategy(root_path),
            "markdown_table": MarkdownTableSyncStrategy(root_path),
            "catalog": CatalogSyncStrategy(root_path, self.scanner),
        }
    
    def _load_config(self) -> dict[str, ArtifactConfig]:
        """Load and parse configuration."""
        if not self.config_path.exists():
            return {}
        
        raw = json.loads(self.config_path.read_text(encoding='utf-8'))
        configs = {}
        
        for name, artifact_data in raw.get("artifacts", {}).items():
            targets = []
            for target_data in artifact_data.get("targets", []):
                targets.append(SyncTarget(
                    type=target_data.get("type", "count"),
                    file=target_data.get("file", ""),
                    pattern=target_data.get("pattern", ""),
                    replacement=target_data.get("replacement", ""),
                    section=target_data.get("section", ""),
                    json_path=target_data.get("json_path", ""),
                    columns=target_data.get("columns", []),
                    id_column=target_data.get("id_column", ""),
                    sync_mode=target_data.get("sync_mode", "full"),
                    categories=target_data.get("categories", {}),
                    key_field=target_data.get("key_field", ""),
                    line_pattern=target_data.get("line_pattern", ""),
                    annotation_pattern=target_data.get("annotation_pattern", ""),
                ))
            
            configs[name] = ArtifactConfig(
                name=name,
                description=artifact_data.get("description", ""),
                source_dir=artifact_data.get("source_dir", ""),
                pattern=artifact_data.get("pattern", "*"),
                recursive=artifact_data.get("recursive", False),
                exclude=artifact_data.get("exclude", []),
                id_extractor=artifact_data.get("id_extractor", "filename_stem"),
                metadata_extractor=artifact_data.get("metadata_extractor"),
                file_types_only=artifact_data.get("file_types_only", False),
                count_method=artifact_data.get("count_method", "file_count"),
                targets=targets,
            )
        
        return configs
    
    def get_directory_triggers(self) -> dict[str, list[str]]:
        """Get mapping of directories to artifact types they trigger."""
        if not self.config_path.exists():
            return {}
        raw = json.loads(self.config_path.read_text(encoding='utf-8'))
        return raw.get("directory_triggers", {})
    
    def get_artifacts_for_dirs(self, dirs: list[str]) -> list[str]:
        """Get artifact types that should be synced for given directories."""
        triggers = self.get_directory_triggers()
        artifacts = set()
        
        for dir_path in dirs:
            # Normalize path
            dir_path = dir_path.replace('\\', '/').rstrip('/')
            
            for trigger_dir, artifact_list in triggers.items():
                trigger_dir = trigger_dir.replace('\\', '/').rstrip('/')
                if dir_path.startswith(trigger_dir) or trigger_dir.startswith(dir_path):
                    artifacts.update(artifact_list)
        
        return list(artifacts)
    
    def sync_artifact(self, artifact_name: str, dry_run: bool = True, 
                       use_fast_count: bool = False) -> list[SyncResult]:
        """Sync a single artifact type.
        
        Args:
            artifact_name: Name of the artifact to sync.
            dry_run: If True, only check without modifying files.
            use_fast_count: If True, use fast file-based counting for tests.
                           Defaults to False for accurate pytest counts that
                           match CI validation. Set to True only for quick checks.
        """
        if artifact_name not in self.config:
            return [SyncResult(
                artifact=artifact_name, target_file="", target_type="",
                changed=False, old_value=None, new_value=None,
                message=f"Unknown artifact: {artifact_name}"
            )]
        
        config = self.config[artifact_name]
        results = []
        
        # Get count - use accurate pytest method by default, fast only when explicitly requested
        if config.count_method == "pytest_collect":
            if use_fast_count:
                count = self.scanner.count_test_functions()
            else:
                count = self.scanner.count_pytest()
        else:
            artifacts = self.scanner.scan(config)
            count = len(artifacts)
        
        # Process each target
        for target in config.targets:
            strategy = self.strategies.get(target.type)
            if strategy:
                artifacts_list = self.scanner.scan(config) if config.count_method != "pytest_collect" else []
                result = strategy.sync(target, count, artifacts_list, dry_run)
                result = SyncResult(
                    artifact=artifact_name,
                    target_file=result.target_file,
                    target_type=result.target_type,
                    changed=result.changed,
                    old_value=result.old_value,
                    new_value=result.new_value,
                    message=result.message
                )
                results.append(result)
            else:
                results.append(SyncResult(
                    artifact=artifact_name, target_file=target.file, target_type=target.type,
                    changed=False, old_value=None, new_value=None,
                    message=f"No strategy for target type: {target.type}"
                ))
        
        return results
    
    def sync_all(self, dry_run: bool = True, artifact_filter: Optional[list[str]] = None,
                  use_fast_count: bool = False) -> list[SyncResult]:
        """Sync all configured artifacts.
        
        Args:
            dry_run: If True, only check without modifying files.
            artifact_filter: Optional list of artifact names to sync.
            use_fast_count: If True, use fast file-based counting for tests.
                           Defaults to False for accurate counts.
        """
        all_results = []
        
        artifacts_to_sync = artifact_filter or list(self.config.keys())
        
        for artifact_name in artifacts_to_sync:
            results = self.sync_artifact(artifact_name, dry_run, use_fast_count)
            all_results.extend(results)
        
        return all_results
    
    def sync_by_dirs(self, dirs: list[str], dry_run: bool = True) -> list[SyncResult]:
        """Sync artifacts triggered by the given directories."""
        artifacts = self.get_artifacts_for_dirs(dirs)
        if not artifacts:
            return []
        return self.sync_all(dry_run, artifact_filter=artifacts)


# =============================================================================
# TEST COUNT PUBLIC API
# =============================================================================
# These functions provide a clean public interface for test count operations.
# They are used by sync_test_counts.py (deprecated wrapper) and tests.

def get_python_path() -> str:
    """Get the Python executable path.
    
    Returns:
        Path to the current Python interpreter.
    """
    return sys.executable


def collect_test_count(test_dir: Optional[str] = None, root_path: Optional[Path] = None) -> int:
    """Collect test count using pytest --collect-only.
    
    Args:
        test_dir: Subdirectory under tests/ to count, or None for all tests.
        root_path: Root path of the project. Defaults to current working directory.
        
    Returns:
        Number of tests collected.
    """
    if root_path is None:
        root_path = Path.cwd()
    
    scanner = ArtifactScanner(root_path)
    return scanner.count_pytest(test_dir)


def get_actual_counts(root_path: Optional[Path] = None) -> CategoryTestCounts:
    """Get actual test counts from pytest for all categories.
    
    Args:
        root_path: Root path of the project. Defaults to current working directory.
        
    Returns:
        TestCountsByCategory with counts for each test category.
    """
    if root_path is None:
        root_path = Path.cwd()
    
    print("Collecting test counts from pytest...")
    
    scanner = ArtifactScanner(root_path)
    
    return CategoryTestCounts(
        total=scanner.count_pytest(None),
        unit=scanner.count_pytest("unit"),
        integration=scanner.count_pytest("integration"),
        validation=scanner.count_pytest("validation"),
        guardian=scanner.count_pytest("guardian"),
        memory=scanner.count_pytest("memory"),
    )


def extract_documented_counts(content: str) -> CategoryTestCounts:
    """Extract test counts currently documented in TESTING.md content.
    
    Args:
        content: The content of TESTING.md file.
        
    Returns:
        TestCountsByCategory with documented counts.
    """
    # Pattern for total: "consists of **942 tests**"
    total_match = re.search(r'consists of \*\*(\d+) tests\*\*', content)
    total = int(total_match.group(1)) if total_match else 0
    
    # Pattern for categories in the overview table: "| Unit Tests | ~589 |"
    def extract_category(category_name: str) -> int:
        pattern = rf'\| {category_name} \| ~?(\d+) \|'
        match = re.search(pattern, content)
        return int(match.group(1)) if match else 0
    
    return CategoryTestCounts(
        total=total,
        unit=extract_category("Unit Tests"),
        integration=extract_category("Integration Tests"),
        validation=extract_category("Validation Tests"),
        guardian=extract_category("Guardian Tests"),
        memory=extract_category("Memory Tests"),
    )


def update_testing_md(actual: CategoryTestCounts, dry_run: bool = True, 
                      root_path: Optional[Path] = None) -> list[str]:
    """Update docs/TESTING.md with actual test counts.
    
    Args:
        actual: The actual test counts to sync.
        dry_run: If True, only check without modifying files.
        root_path: Root path of the project. Defaults to current working directory.
        
    Returns:
        List of changes made (or that would be made if dry_run).
    """
    if root_path is None:
        root_path = Path.cwd()
    
    testing_md = root_path / "docs" / "TESTING.md"
    if not testing_md.exists():
        return ["docs/TESTING.md not found"]
    
    content = testing_md.read_text(encoding='utf-8')
    documented = extract_documented_counts(content)
    
    changes = []
    new_content = content
    
    # Update total count
    if documented.total != actual.total:
        changes.append(f"Total tests: {documented.total} -> {actual.total}")
        new_content = re.sub(
            r'consists of \*\*\d+ tests\*\*',
            f'consists of **{actual.total} tests**',
            new_content
        )
    
    # Update category counts in overview table
    categories = [
        ("Unit Tests", documented.unit, actual.unit),
        ("Integration Tests", documented.integration, actual.integration),
        ("Validation Tests", documented.validation, actual.validation),
        ("Guardian Tests", documented.guardian, actual.guardian),
        ("Memory Tests", documented.memory, actual.memory),
    ]
    
    for name, old_count, new_count in categories:
        if old_count != new_count:
            changes.append(f"{name}: ~{old_count} -> ~{new_count}")
            # Update table row
            new_content = re.sub(
                rf'\| {name} \| ~?\d+ \|',
                f'| {name} | ~{new_count} |',
                new_content
            )
    
    # Update counts in test structure tree comments
    structure_updates = [
        (r'# Unit tests \(~\d+ tests\)', f'# Unit tests (~{actual.unit} tests)'),
        (r'# Integration tests \(~\d+ tests\)', f'# Integration tests (~{actual.integration} tests)'),
        (r'# Schema validation \(~\d+ tests\)', f'# Schema validation (~{actual.validation} tests)'),
        (r'# Guardian tests \(~\d+ tests\)', f'# Guardian tests (~{actual.guardian} tests)'),
        (r'# Memory system tests \(~\d+ tests\)', f'# Memory system tests (~{actual.memory} tests)'),
    ]
    
    for pattern, replacement in structure_updates:
        if re.search(pattern, new_content):
            new_content = re.sub(pattern, replacement, new_content)
    
    if not dry_run and changes:
        testing_md.write_text(new_content, encoding='utf-8')
    
    return changes


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Unified Artifact Sync System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s                     # Check all artifacts
    %(prog)s --sync              # Sync all artifacts
    %(prog)s --sync agents       # Sync only agents
    %(prog)s --dirs .agent/agents blueprints  # Sync by directory changes
        """
    )
    parser.add_argument("--sync", action="store_true", help="Perform sync (not just check)")
    parser.add_argument("--dirs", nargs="+", help="Sync artifacts for these directories")
    parser.add_argument("--fast", action="store_true", 
                        help="Use fast file-based counting for tests. Default uses accurate pytest counting.")
    parser.add_argument("artifacts", nargs="*", help="Specific artifacts to sync")
    
    args = parser.parse_args()
    
    engine = SyncEngine()
    
    # Determine which artifacts to sync
    use_fast = args.fast  # Use accurate by default, fast only with --fast
    
    if args.dirs:
        results = engine.sync_by_dirs(args.dirs, dry_run=not args.sync)
    elif args.artifacts:
        results = engine.sync_all(dry_run=not args.sync, artifact_filter=args.artifacts,
                                  use_fast_count=use_fast)
    else:
        results = engine.sync_all(dry_run=not args.sync, use_fast_count=use_fast)
    
    # Report results
    changes = [r for r in results if r.changed]
    errors = [r for r in results if "error" in r.message.lower() or "not found" in r.message.lower()]
    
    if not results:
        print("[INFO] No artifacts configured or no matching directories")
        return 0
    
    # Print results grouped by artifact
    current_artifact = None
    for result in results:
        if result.artifact != current_artifact:
            current_artifact = result.artifact
            print(f"\n{result.artifact}:")
        
        status = "[CHANGED]" if result.changed else "[OK]"
        if "error" in result.message.lower() or "not found" in result.message.lower():
            status = "[SKIP]"
        print(f"  {status} {result.target_file} ({result.target_type}): {result.message}")
    
    print()
    
    if not changes:
        print("[OK] All artifacts are in sync")
        return 0
    
    if args.sync:
        print(f"[SYNCED] {len(changes)} target(s) updated")
        return 0
    else:
        print(f"[OUT OF SYNC] {len(changes)} target(s) need update")
        print("\nRun with --sync to fix")
        return 1


if __name__ == "__main__":
    sys.exit(main())
