"""
Taxonomy Module for Knowledge Evolution

This module provides topic taxonomies that define what knowledge should exist
in the knowledge base. Taxonomies are used by the gap analyzer to identify
missing or shallow coverage areas.

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class TopicNode:
    """Represents a node in the topic taxonomy tree.

    Attributes:
        name: Topic identifier
        description: Human-readable description
        required_depth: Minimum coverage depth (0-3)
        keywords: Keywords to search for in knowledge files
        subtopics: Child topics
        knowledge_files: Files that should cover this topic
    """

    name: str
    description: str = ""
    required_depth: int = 2
    keywords: List[str] = field(default_factory=list)
    subtopics: Dict[str, "TopicNode"] = field(default_factory=dict)
    knowledge_files: List[str] = field(default_factory=list)

    def get_all_keywords(self) -> List[str]:
        """Get all keywords including from subtopics.

        Returns:
            Flattened list of all keywords
        """
        all_keywords = list(self.keywords)
        for subtopic in self.subtopics.values():
            all_keywords.extend(subtopic.get_all_keywords())
        return all_keywords

    def get_leaf_topics(self) -> List["TopicNode"]:
        """Get all leaf nodes (topics without subtopics).

        Returns:
            List of leaf TopicNode objects
        """
        if not self.subtopics:
            return [self]

        leaves = []
        for subtopic in self.subtopics.values():
            leaves.extend(subtopic.get_leaf_topics())
        return leaves

    def count_topics(self) -> int:
        """Count total topics including subtopics.

        Returns:
            Total number of topics
        """
        count = 1
        for subtopic in self.subtopics.values():
            count += subtopic.count_topics()
        return count


class TaxonomyLoader:
    """Loads and manages topic taxonomies.

    This class provides methods to load taxonomy JSON files and
    convert them into navigable TopicNode structures.

    Example:
        loader = TaxonomyLoader()
        taxonomy = loader.load_taxonomy("agent_taxonomy.json")
        for domain in taxonomy.domains:
            print(f"{domain.name}: {domain.count_topics()} topics")
    """

    def __init__(self, taxonomy_dir: Optional[Path] = None):
        """Initialize the taxonomy loader.

        Args:
            taxonomy_dir: Directory containing taxonomy files.
                          Defaults to the directory containing this module.
        """
        if taxonomy_dir is None:
            taxonomy_dir = Path(__file__).parent
        self.taxonomy_dir = Path(taxonomy_dir)
        self._cache: Dict[str, Dict[str, TopicNode]] = {}

    def load_taxonomy(self, filename: str) -> Dict[str, TopicNode]:
        """Load a taxonomy from a JSON file.

        Args:
            filename: Name of the taxonomy file

        Returns:
            Dictionary of domain name to TopicNode

        Raises:
            FileNotFoundError: If taxonomy file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        if filename in self._cache:
            return self._cache[filename]

        file_path = self.taxonomy_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Taxonomy file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        domains = self._parse_domains(raw_data.get("domains", {}))
        self._cache[filename] = domains
        return domains

    def _parse_domains(self, domains_data: Dict[str, Any]) -> Dict[str, TopicNode]:
        """Parse domain definitions into TopicNode objects.

        Args:
            domains_data: Raw domain data from JSON

        Returns:
            Dictionary of domain name to TopicNode
        """
        domains = {}
        for domain_name, domain_data in domains_data.items():
            domains[domain_name] = self._parse_topic_node(domain_name, domain_data)
        return domains

    def _parse_topic_node(self, name: str, data: Dict[str, Any]) -> TopicNode:
        """Parse a single topic node from JSON data.

        Args:
            name: Topic name
            data: Topic data dictionary

        Returns:
            TopicNode object
        """
        node = TopicNode(
            name=name,
            description=data.get("description", ""),
            required_depth=data.get("required_depth", 2),
            keywords=data.get("keywords", []),
            knowledge_files=data.get("knowledge_files", []),
        )

        # Parse subtopics recursively
        if "topics" in data:
            for topic_name, topic_data in data["topics"].items():
                node.subtopics[topic_name] = self._parse_topic_node(
                    topic_name, topic_data
                )

        if "subtopics" in data:
            for subtopic_name, subtopic_data in data["subtopics"].items():
                node.subtopics[subtopic_name] = self._parse_topic_node(
                    subtopic_name, subtopic_data
                )

        return node

    def get_available_taxonomies(self) -> List[str]:
        """Get list of available taxonomy files.

        Returns:
            List of taxonomy filenames
        """
        return [f.name for f in self.taxonomy_dir.glob("*_taxonomy.json")]

    def get_all_topics_flat(self, taxonomy_name: str) -> List[TopicNode]:
        """Get a flat list of all topics from a taxonomy.

        Args:
            taxonomy_name: Name of the taxonomy file

        Returns:
            Flat list of all TopicNode objects
        """
        domains = self.load_taxonomy(taxonomy_name)
        all_topics = []

        for domain in domains.values():
            all_topics.extend(self._flatten_topics(domain))

        return all_topics

    def _flatten_topics(
        self, node: TopicNode, parent_path: str = ""
    ) -> List[TopicNode]:
        """Recursively flatten a topic tree.

        Args:
            node: Current node
            parent_path: Path to parent node

        Returns:
            Flat list of topics
        """
        current_path = f"{parent_path}.{node.name}" if parent_path else node.name
        result = [node]

        for subtopic in node.subtopics.values():
            result.extend(self._flatten_topics(subtopic, current_path))

        return result


# Convenience function for loading the default agent taxonomy
def load_agent_taxonomy() -> Dict[str, TopicNode]:
    """Load the default agent building taxonomy.

    Returns:
        Dictionary of domain name to TopicNode
    """
    loader = TaxonomyLoader()
    return loader.load_taxonomy("agent_taxonomy.json")
