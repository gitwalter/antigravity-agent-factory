#!/usr/bin/env python3
"""
Dependency Graph Validator for Antigravity Agent Factory.
Validates dependencies between Factory artifacts using:
- graphlib.TopologicalSorter (stdlib) for cycle detection and ordering
- packaging (PyPA standard) for version constraint validation

This module scans all Factory artifacts and builds a unified dependency graph,
enabling validation, impact analysis, and dependency ordering.

Node Types:
- knowledge:<filename> - Knowledge JSON files
- skill:<name> - Skills defined in .agent/skills/
- agent:<name> - Agents defined in .agent/agents/
- blueprint:<id> - Blueprints in .agent/blueprints/
- template:<path> - Templates in templates/
- pattern:<path> - Patterns in .agent/patterns/

Edge Types:
- requires: Hard dependency (must exist)
- references: Soft reference (used if present)
- extends: Specialization relationship
- triggers: Update propagation dependency

Usage:
    python scripts/validation/dependency_validator.py              # Full validation
    python scripts/validation/dependency_validator.py --cycles     # Cycle detection only
    python scripts/validation/dependency_validator.py --broken     # Broken refs only
    python scripts/validation/dependency_validator.py --impact knowledge:fastapi-patterns
    python scripts/validation/dependency_validator.py --dependents skill:grounding
    python scripts/validation/dependency_validator.py --order      # Installation order

Author: Antigravity Agent Factory
Version: 1.0.0
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from graphlib import TopologicalSorter, CycleError
from pathlib import Path
from typing import Any, Optional

import yaml

# Optional: packaging for version constraints
try:
    from packaging.version import Version
    from packaging.specifiers import SpecifierSet, InvalidSpecifier
    HAS_PACKAGING = True
except ImportError:
    HAS_PACKAGING = False


class EdgeType(Enum):
    """Types of dependency edges between artifacts."""
    REQUIRES = "requires"       # Hard dependency, must exist
    REFERENCES = "references"   # Soft reference, used if present
    EXTENDS = "extends"         # Specialization relationship
    TRIGGERS = "triggers"       # Update propagation


class NodeType(Enum):
    """Types of nodes (artifacts) in the dependency graph."""
    KNOWLEDGE = "knowledge"
    SKILL = "skill"
    AGENT = "agent"
    BLUEPRINT = "blueprint"
    TEMPLATE = "template"
    PATTERN = "pattern"


@dataclass
class DependencyNode:
    """Represents a node in the dependency graph."""
    id: str
    node_type: NodeType
    version: Optional[str] = None
    path: Optional[Path] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class DependencyEdge:
    """Represents an edge (dependency) between two nodes."""
    from_node: str
    to_node: str
    edge_type: EdgeType
    version_constraint: Optional[str] = None
    
    def __hash__(self):
        return hash((self.from_node, self.to_node, self.edge_type))
    
    def __eq__(self, other):
        if not isinstance(other, DependencyEdge):
            return False
        return (self.from_node == self.to_node == other.to_node and 
                self.edge_type == other.edge_type)


@dataclass
class ValidationResult:
    """Result of dependency validation."""
    cycles: list[list[str]] = field(default_factory=list)
    broken_refs: list[str] = field(default_factory=list)
    version_errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    
    @property
    def is_valid(self) -> bool:
        """Returns True if no critical errors found."""
        return len(self.cycles) == 0 and len(self.broken_refs) == 0
    
    @property
    def has_warnings(self) -> bool:
        """Returns True if warnings exist."""
        return len(self.warnings) > 0 or len(self.version_errors) > 0


class DependencyValidator:
    """
    Validates dependency graph using stdlib graphlib + packaging.
    
    Scans Factory artifacts (knowledge, skills, agents, blueprints) and builds
    a unified dependency graph for validation and analysis.
    
    Example:
        validator = DependencyValidator(Path("."))
        validator.scan_artifacts()
        result = validator.validate()
        if not result.is_valid:
            for cycle in result.cycles:
                print(f"Cycle: {' -> '.join(cycle)}")
    """
    
    def __init__(self, factory_root: Path):
        """
        Initialize the validator.
        
        Args:
            factory_root: Root directory of the Factory
        """
        self.factory_root = factory_root
        self.nodes: dict[str, DependencyNode] = {}
        self.edges: list[DependencyEdge] = []
        self._adjacency: dict[str, set[str]] = {}  # from -> set(to)
        self._reverse_adjacency: dict[str, set[str]] = {}  # to -> set(from)
    
    def scan_artifacts(self) -> None:
        """
        Scan all Factory artifacts and build the dependency graph.
        
        Scans:
        - knowledge/manifest.json for knowledge file dependencies
        - .agent/skills/*/SKILL.md for skill dependencies
        - .agent/agents/*.md for agent dependencies
        - .agent/blueprints/*/blueprint.json for blueprint references
        """
        self._scan_knowledge_files()
        self._scan_skills()
        self._scan_agents()
        self._scan_blueprints()
        self._scan_patterns()
        self._scan_templates()
        self._build_adjacency()
    
    def _scan_knowledge_files(self) -> None:
        """Scan knowledge/manifest.json for knowledge file dependencies."""
        manifest_path = self.factory_root / ".agent" / "knowledge" / "manifest.json"
        if not manifest_path.exists():
            return
        
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except (json.JSONDecodeError, IOError):
            return
        
        files = manifest.get("files", {})
        for filename, info in files.items():
            node_id = f"knowledge:{filename}"
            self.nodes[node_id] = DependencyNode(
                id=node_id,
                node_type=NodeType.KNOWLEDGE,
                version=info.get("version"),
                path=self.factory_root / ".agent" / "knowledge" / filename,
                metadata={
                    "category": info.get("category"),
                    "title": info.get("title"),
                    "tags": info.get("tags", []),
                }
            )
            
            # Parse dependencies
            deps = info.get("dependencies", [])
            for dep in deps:
                if isinstance(dep, str):
                    # Simple dependency: just filename
                    to_node = f"knowledge:{dep}"
                    self.edges.append(DependencyEdge(
                        from_node=node_id,
                        to_node=to_node,
                        edge_type=EdgeType.REQUIRES
                    ))
                elif isinstance(dep, dict):
                    # Complex dependency with version constraint
                    to_node = f"knowledge:{dep.get('file', dep.get('filename', ''))}"
                    self.edges.append(DependencyEdge(
                        from_node=node_id,
                        to_node=to_node,
                        edge_type=EdgeType.REQUIRES,
                        version_constraint=dep.get("minVersion")
                    ))
    
    def _scan_skills(self) -> None:
        """Scan .agent/skills/*/SKILL.md for skill dependencies.
        Note: Many skills don't have YAML frontmatter. In those cases,
        we use the directory name as the skill name and still register
        the skill as a node to enable proper dependency tracking.
        """
        skills_dir = self.factory_root / ".agent" / "skills"
        if not skills_dir.exists():
            return
        
        # Recursively find all SKILL.md files (handles nested pm/ skills)
        for skill_file in skills_dir.rglob("SKILL.md"):
            skill_dir = skill_file.parent
            
            frontmatter = self._parse_frontmatter(skill_file)
            
            # Use frontmatter name if available, otherwise use directory name
            if frontmatter:
                skill_name = frontmatter.get("name", skill_dir.name)
            else:
                skill_name = skill_dir.name
            
            node_id = f"skill:{skill_name}"
            
            # Skip if already registered (avoid duplicates)
            if node_id in self.nodes:
                continue
            
            self.nodes[node_id] = DependencyNode(
                id=node_id,
                node_type=NodeType.SKILL,
                path=skill_file,
                metadata={
                    "description": frontmatter.get("description") if frontmatter else None,
                    "type": frontmatter.get("type") if frontmatter else "skill",
                    "has_frontmatter": frontmatter is not None,
                }
            )
            
            # Only process dependencies if frontmatter exists
            if not frontmatter:
                continue
            
            # Skill dependencies (other skills)
            for dep_skill in frontmatter.get("skills", []):
                self.edges.append(DependencyEdge(
                    from_node=node_id,
                    to_node=f"skill:{dep_skill}",
                    edge_type=EdgeType.REQUIRES
                ))
            
            # Knowledge dependencies
            for knowledge in frontmatter.get("knowledge", []):
                # Handle both "file.json" and "file" formats
                if not knowledge.endswith(".json"):
                    knowledge = f"{knowledge}.json"
                self.edges.append(DependencyEdge(
                    from_node=node_id,
                    to_node=f"knowledge:{knowledge}",
                    edge_type=EdgeType.REFERENCES
                ))
            
            # Template dependencies
            for template in frontmatter.get("templates", []):
                self.edges.append(DependencyEdge(
                    from_node=node_id,
                    to_node=f"template:{template}",
                    edge_type=EdgeType.REFERENCES
                ))
            
            # Pattern dependencies
            for pattern in frontmatter.get("patterns", []):
                self.edges.append(DependencyEdge(
                    from_node=node_id,
                    to_node=f"pattern:{pattern}",
                    edge_type=EdgeType.REFERENCES
                ))
    
    def _scan_agents(self) -> None:
        """Scan .agent/agents/*.md for agent dependencies."""
        agents_dir = self.factory_root / ".agent" / "agents"
        if not agents_dir.exists():
            return
        
        for agent_file in agents_dir.rglob("*.md"):
            frontmatter = self._parse_frontmatter(agent_file)
            if not frontmatter:
                continue
            
            agent_name = frontmatter.get("name", agent_file.stem)
            node_id = f"agent:{agent_name}"
            
            self.nodes[node_id] = DependencyNode(
                id=node_id,
                node_type=NodeType.AGENT,
                path=agent_file,
                metadata={
                    "description": frontmatter.get("description"),
                    "type": frontmatter.get("type"),
                }
            )
            
            # Skill dependencies
            for skill in frontmatter.get("skills", []):
                self.edges.append(DependencyEdge(
                    from_node=node_id,
                    to_node=f"skill:{skill}",
                    edge_type=EdgeType.REQUIRES
                ))
            
            # Knowledge dependencies
            for knowledge in frontmatter.get("knowledge", []):
                # Handle both "file.json" and "file" formats
                if not knowledge.endswith(".json"):
                    knowledge = f"{knowledge}.json"
                self.edges.append(DependencyEdge(
                    from_node=node_id,
                    to_node=f"knowledge:{knowledge}",
                    edge_type=EdgeType.REFERENCES
                ))
    
    def _scan_blueprints(self) -> None:
        """Scan .agent/blueprints/*/blueprint.json for blueprint references."""
        blueprints_dir = self.factory_root / ".agent" / "blueprints"
        if not blueprints_dir.exists():
            return
        
        for bp_dir in blueprints_dir.iterdir():
            if not bp_dir.is_dir():
                continue
            
            bp_file = bp_dir / "blueprint.json"
            if not bp_file.exists():
                continue
            
            try:
                with open(bp_file, encoding="utf-8") as f:
                    blueprint = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue
            
            metadata = blueprint.get("metadata", {})
            bp_id = metadata.get("blueprintId", bp_dir.name)
            node_id = f"blueprint:{bp_id}"
            
            self.nodes[node_id] = DependencyNode(
                id=node_id,
                node_type=NodeType.BLUEPRINT,
                version=metadata.get("version"),
                path=bp_file,
                metadata={
                    "name": metadata.get("blueprintName"),
                    "description": metadata.get("description"),
                }
            )
            
            # Agent pattern references
            for agent in blueprint.get("agents", []):
                pattern_id = agent.get("patternId")
                if pattern_id:
                    self.edges.append(DependencyEdge(
                        from_node=node_id,
                        to_node=f"pattern:agents/{pattern_id}",
                        edge_type=EdgeType.REFERENCES
                    ))
            
            # Skill pattern references
            for skill in blueprint.get("skills", []):
                pattern_id = skill.get("patternId")
                if pattern_id:
                    self.edges.append(DependencyEdge(
                        from_node=node_id,
                        to_node=f"pattern:skills/{pattern_id}",
                        edge_type=EdgeType.REFERENCES
                    ))
            
            # Knowledge file references
            for knowledge in blueprint.get("knowledge", []):
                filename = None
                if isinstance(knowledge, str):
                    filename = knowledge
                elif isinstance(knowledge, dict):
                    filename = knowledge.get("filename")
                
                if filename:
                    self.edges.append(DependencyEdge(
                        from_node=node_id,
                        to_node=f"knowledge:{filename}",
                        edge_type=EdgeType.REFERENCES
                    ))

    def _scan_patterns(self) -> None:
        """Scan .agent/patterns/ for pattern definitions."""
        patterns_dir = self.factory_root / ".agent" / "patterns"
        if not patterns_dir.exists():
            return
        
        for pattern_file in patterns_dir.rglob("*.json"):
            rel_path = pattern_file.relative_to(patterns_dir)
            pattern_id = rel_path.with_suffix("").as_posix()
            
            node_id = f"pattern:{pattern_id}"
            
            # Extract metadata if possible
            metadata = {}
            try:
                with open(pattern_file, encoding="utf-8") as f:
                    content = json.load(f)
                    metadata["type"] = content.get("type")
                    metadata["description"] = content.get("description")
            except (json.JSONDecodeError, IOError):
                pass

            self.nodes[node_id] = DependencyNode(
                id=node_id,
                node_type=NodeType.PATTERN,
                path=pattern_file,
                metadata=metadata
            )

    def _scan_templates(self) -> None:
        """Scan .agent/templates/ for template files."""
        templates_dir = self.factory_root / ".agent" / "templates"
        if not templates_dir.exists():
            return
            
        for template_path in templates_dir.rglob("*"):
            if template_path.is_file():
                rel_path = template_path.relative_to(templates_dir)
                template_id = rel_path.as_posix()
                
                node_id = f"template:{template_id}"
                self.nodes[node_id] = DependencyNode(
                    id=node_id,
                    node_type=NodeType.TEMPLATE,
                    path=template_path
                )
    
    def _parse_frontmatter(self, filepath: Path) -> Optional[dict]:
        """
        Parse YAML frontmatter from a markdown file.
        
        Args:
            filepath: Path to the markdown file
            
        Returns:
            Parsed frontmatter dict or None if not found
        """
        try:
            content = filepath.read_text(encoding="utf-8")
        except IOError:
            return None
        
        # Match YAML frontmatter (between --- markers)
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None
        
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    
    def _build_adjacency(self) -> None:
        """Build adjacency lists from edges for graph operations."""
        self._adjacency = {}
        self._reverse_adjacency = {}
        
        for edge in self.edges:
            if edge.from_node not in self._adjacency:
                self._adjacency[edge.from_node] = set()
            self._adjacency[edge.from_node].add(edge.to_node)
            
            if edge.to_node not in self._reverse_adjacency:
                self._reverse_adjacency[edge.to_node] = set()
            self._reverse_adjacency[edge.to_node].add(edge.from_node)
    
    def detect_cycles(self) -> list[list[str]]:
        """
        Detect circular dependencies in the graph.
        
        Uses graphlib.TopologicalSorter to detect cycles.
        
        Returns:
            List of cycles (each cycle is a list of node IDs)
        """
        ts = TopologicalSorter()
        
        # Add all nodes (even those without dependencies)
        for node_id in self.nodes:
            ts.add(node_id)
        
        # Add edges (note: TopologicalSorter expects (node, *predecessors))
        for edge in self.edges:
            if edge.edge_type in (EdgeType.REQUIRES, EdgeType.EXTENDS):
                ts.add(edge.from_node, edge.to_node)
        
        try:
            list(ts.static_order())
            return []
        except CycleError as e:
            # Extract cycle information from exception
            cycle_info = str(e)
            # Parse the cycle from the error message
            match = re.search(r"nodes are in a cycle \[(.*?)\]", cycle_info)
            if match:
                cycle_nodes = [n.strip().strip("'") for n in match.group(1).split(",")]
                return [cycle_nodes]
            return [["cycle detected"]]
    
    def find_broken_refs(self) -> list[str]:
        """
        Find edges that reference non-existent nodes.
        
        Only checks REQUIRES edges (hard dependencies).
        
        Returns:
            List of error messages for broken references
        """
        errors = []
        
        for edge in self.edges:
            if edge.edge_type == EdgeType.REQUIRES:
                if edge.to_node not in self.nodes:
                    errors.append(
                        f"{edge.from_node} requires {edge.to_node} but it doesn't exist"
                    )
        
        return errors
    
    def find_missing_refs(self) -> list[str]:
        """
        Find soft references to non-existent nodes (warnings).
        
        Returns:
            List of warning messages for missing references
        """
        warnings = []
        
        for edge in self.edges:
            if edge.edge_type == EdgeType.REFERENCES:
                if edge.to_node not in self.nodes:
                    warnings.append(
                        f"{edge.from_node} references {edge.to_node} but it doesn't exist"
                    )
        
        return warnings
    
    def validate_versions(self) -> list[str]:
        """
        Validate version constraints on dependencies.
        
        Requires the 'packaging' library to be installed.
        
        Returns:
            List of version constraint violation messages
        """
        if not HAS_PACKAGING:
            return ["packaging library not installed, skipping version validation"]
        
        errors = []
        
        for edge in self.edges:
            if edge.version_constraint and edge.to_node in self.nodes:
                target = self.nodes[edge.to_node]
                if target.version:
                    try:
                        spec = SpecifierSet(f">={edge.version_constraint}")
                        actual = Version(target.version)
                        if actual not in spec:
                            errors.append(
                                f"{edge.from_node} requires {edge.to_node}>={edge.version_constraint}, "
                                f"but found {target.version}"
                            )
                    except (InvalidSpecifier, Exception) as e:
                        errors.append(f"Invalid version constraint: {e}")
        
        return errors
    
    def validate(self) -> ValidationResult:
        """
        Run full validation on the dependency graph.
        
        Returns:
            ValidationResult with all detected issues
        """
        return ValidationResult(
            cycles=self.detect_cycles(),
            broken_refs=self.find_broken_refs(),
            version_errors=self.validate_versions(),
            warnings=self.find_missing_refs()
        )
    
    def reverse_lookup(self, node_id: str) -> set[str]:
        """
        Find all nodes that depend on the given node.
        
        Args:
            node_id: The node to look up dependents for
            
        Returns:
            Set of node IDs that depend on this node
        """
        return self._reverse_adjacency.get(node_id, set())
    
    def impact_analysis(self, node_id: str) -> set[str]:
        """
        Find all nodes transitively affected by changes to the given node.
        
        Uses BFS to find all downstream dependents.
        
        Args:
            node_id: The node to analyze impact for
            
        Returns:
            Set of all affected node IDs
        """
        affected = set()
        queue = list(self.reverse_lookup(node_id))
        
        while queue:
            current = queue.pop(0)
            if current not in affected:
                affected.add(current)
                queue.extend(self.reverse_lookup(current))
        
        return affected
    
    def get_install_order(self) -> list[str]:
        """
        Get topologically sorted order for installing artifacts.
        
        Returns:
            List of node IDs in dependency order (dependencies first)
            
        Raises:
            CycleError: If circular dependencies exist
        """
        ts = TopologicalSorter()
        
        for node_id in self.nodes:
            ts.add(node_id)
        
        for edge in self.edges:
            if edge.edge_type in (EdgeType.REQUIRES, EdgeType.EXTENDS):
                ts.add(edge.from_node, edge.to_node)
        
        return list(ts.static_order())
    
    def get_statistics(self) -> dict[str, Any]:
        """
        Get statistics about the dependency graph.
        
        Returns:
            Dictionary with graph statistics
        """
        type_counts = {}
        for node in self.nodes.values():
            type_name = node.node_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        edge_type_counts = {}
        for edge in self.edges:
            type_name = edge.edge_type.value
            edge_type_counts[type_name] = edge_type_counts.get(type_name, 0) + 1
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "nodes_by_type": type_counts,
            "edges_by_type": edge_type_counts,
        }
    
    def export_graph(self) -> dict[str, Any]:
        """
        Export the dependency graph as a JSON-serializable dict.
        
        Returns:
            Dictionary representation of the graph
        """
        return {
            "version": "1.0.0",
            "nodes": {
                node_id: {
                    "type": node.node_type.value,
                    "version": node.version,
                    "path": str(node.path) if node.path else None,
                    "metadata": node.metadata,
                }
                for node_id, node in self.nodes.items()
            },
            "edges": [
                {
                    "from": edge.from_node,
                    "to": edge.to_node,
                    "type": edge.edge_type.value,
                    "version_constraint": edge.version_constraint,
                }
                for edge in self.edges
            ],
            "statistics": self.get_statistics(),
        }


def main():
    """CLI entry point for dependency validation."""
    parser = argparse.ArgumentParser(
        description="Validate Factory dependency graph"
    )
    parser.add_argument(
        "--root", "-r",
        type=Path,
        default=Path("."),
        help="Factory root directory (default: current directory)"
    )
    parser.add_argument(
        "--cycles",
        action="store_true",
        help="Check for circular dependencies only"
    )
    parser.add_argument(
        "--broken",
        action="store_true",
        help="Check for broken references only"
    )
    parser.add_argument(
        "--impact",
        type=str,
        metavar="NODE",
        help="Show impact analysis for a node (e.g., knowledge:fastapi-patterns)"
    )
    parser.add_argument(
        "--dependents",
        type=str,
        metavar="NODE",
        help="Show what depends on a node"
    )
    parser.add_argument(
        "--order",
        action="store_true",
        help="Show installation order"
    )
    parser.add_argument(
        "--export",
        type=Path,
        metavar="FILE",
        help="Export graph to JSON file"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show graph statistics"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Create validator and scan
    validator = DependencyValidator(args.root)
    validator.scan_artifacts()
    
    if args.verbose:
        print(f"Scanned {len(validator.nodes)} nodes, {len(validator.edges)} edges")
    
    # Handle specific operations
    if args.stats:
        stats = validator.get_statistics()
        print(json.dumps(stats, indent=2))
        return 0
    
    if args.export:
        graph = validator.export_graph()
        with open(args.export, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2)
        print(f"Exported graph to {args.export}")
        return 0
    
    if args.impact:
        affected = validator.impact_analysis(args.impact)
        if affected:
            print(f"Changes to {args.impact} would affect:")
            for node in sorted(affected):
                print(f"  - {node}")
        else:
            print(f"No nodes depend on {args.impact}")
        return 0
    
    if args.dependents:
        deps = validator.reverse_lookup(args.dependents)
        if deps:
            print(f"Nodes that depend on {args.dependents}:")
            for node in sorted(deps):
                print(f"  - {node}")
        else:
            print(f"No nodes depend on {args.dependents}")
        return 0
    
    if args.order:
        try:
            order = validator.get_install_order()
            print("Installation order:")
            for i, node in enumerate(order, 1):
                print(f"  {i}. {node}")
            return 0
        except CycleError as e:
            print(f"Cannot determine order: {e}", file=sys.stderr)
            return 1
    
    if args.cycles:
        cycles = validator.detect_cycles()
        if cycles:
            print("Circular dependencies detected:")
            for cycle in cycles:
                print(f"  {' -> '.join(cycle)}")
            return 1
        print("No circular dependencies found")
        return 0
    
    if args.broken:
        broken = validator.find_broken_refs()
        if broken:
            print("Broken references:")
            for ref in broken:
                print(f"  - {ref}")
            return 1
        print("No broken references found")
        return 0
    
    # Default: full validation
    result = validator.validate()
    
    exit_code = 0
    
    if result.cycles:
        print("ERROR: Circular dependencies detected:")
        for cycle in result.cycles:
            print(f"  {' -> '.join(cycle)}")
        exit_code = 1
    
    if result.broken_refs:
        print("ERROR: Broken references:")
        for ref in result.broken_refs:
            print(f"  - {ref}")
        exit_code = 1
    
    if result.version_errors:
        print("WARNING: Version constraint violations:")
        for err in result.version_errors:
            print(f"  - {err}")
    
    if result.warnings and args.verbose:
        print("WARNING: Missing soft references:")
        for warn in result.warnings:
            print(f"  - {warn}")
    
    if exit_code == 0:
        print(f"[OK] Dependency graph valid ({len(validator.nodes)} nodes, {len(validator.edges)} edges)")    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
