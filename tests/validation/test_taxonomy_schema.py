"""
Validation tests for taxonomy file structure.

Tests validate that taxonomy JSON files conform to expected structure.
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestAgentTaxonomyStructure:
    """Tests for agent taxonomy file structure."""

    def test_taxonomy_file_exists(self, taxonomy_dir):
        """Test that agent_taxonomy.json exists."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"
        assert taxonomy_path.exists(), "agent_taxonomy.json should exist"

    def test_taxonomy_valid_json(self, taxonomy_dir):
        """Test that taxonomy file is valid JSON."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        try:
            with open(taxonomy_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict), "Taxonomy should be a JSON object"
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in taxonomy: {e}")

    def test_has_required_fields(self, taxonomy_dir):
        """Test that taxonomy has required top-level fields."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        required_fields = ["$schema", "title", "domains"]
        for field in required_fields:
            assert field in data, f"Taxonomy should have '{field}' field"

    def test_has_domains(self, taxonomy_dir):
        """Test that taxonomy has domains defined."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        domains = data.get("domains", {})
        assert len(domains) >= 1, "Taxonomy should have at least one domain"

    def test_domains_have_topics(self, taxonomy_dir):
        """Test that domains have topics or subtopics."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for domain_name, domain_data in data.get("domains", {}).items():
            has_topics = "topics" in domain_data or "subtopics" in domain_data
            assert has_topics, f"Domain '{domain_name}' should have topics or subtopics"

    def test_topics_have_required_depth(self, taxonomy_dir):
        """Test that topics define required_depth."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        def check_depth(node, path=""):
            # Domains may or may not have required_depth
            topics = node.get("topics", {})
            topics.update(node.get("subtopics", {}))

            for topic_name, topic_data in topics.items():
                if isinstance(topic_data, dict):
                    # Topics should have required_depth
                    if "required_depth" in topic_data:
                        depth = topic_data["required_depth"]
                        assert isinstance(
                            depth, int
                        ), f"required_depth in {path}.{topic_name} should be int"
                        assert (
                            0 <= depth <= 3
                        ), f"required_depth in {path}.{topic_name} should be 0-3"
                    check_depth(topic_data, f"{path}.{topic_name}")

        for domain_name, domain_data in data.get("domains", {}).items():
            check_depth(domain_data, domain_name)

    def test_keywords_are_lists(self, taxonomy_dir):
        """Test that keywords fields are lists of strings."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        def check_keywords(node, path=""):
            if "keywords" in node:
                keywords = node["keywords"]
                assert isinstance(
                    keywords, list
                ), f"keywords in {path} should be a list"
                for kw in keywords:
                    assert isinstance(
                        kw, str
                    ), f"keyword '{kw}' in {path} should be a string"

            for key in ["topics", "subtopics"]:
                for name, child in node.get(key, {}).items():
                    if isinstance(child, dict):
                        check_keywords(child, f"{path}.{name}")

        for domain_name, domain_data in data.get("domains", {}).items():
            check_keywords(domain_data, domain_name)

    def test_knowledge_files_are_lists(self, taxonomy_dir):
        """Test that knowledge_files fields are lists of strings."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        def check_files(node, path=""):
            if "knowledge_files" in node:
                files = node["knowledge_files"]
                assert isinstance(
                    files, list
                ), f"knowledge_files in {path} should be a list"
                for f in files:
                    assert isinstance(
                        f, str
                    ), f"file '{f}' in {path} should be a string"

            for key in ["topics", "subtopics"]:
                for name, child in node.get(key, {}).items():
                    if isinstance(child, dict):
                        check_files(child, f"{path}.{name}")

        for domain_name, domain_data in data.get("domains", {}).items():
            check_files(domain_data, domain_name)


class TestTaxonomyMetadata:
    """Tests for taxonomy metadata section."""

    def test_has_version(self, taxonomy_dir):
        """Test that taxonomy has version field."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "version" in data, "Taxonomy should have version field"
        assert isinstance(data["version"], str), "version should be a string"

    def test_has_metadata(self, taxonomy_dir):
        """Test that taxonomy has metadata section."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "metadata" in data, "Taxonomy should have metadata section"
        assert isinstance(data["metadata"], dict), "metadata should be an object"

    def test_has_coverage_scale(self, taxonomy_dir):
        """Test that metadata defines coverage scale."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        metadata = data.get("metadata", {})
        assert "coverage_scale" in metadata, "metadata should have coverage_scale"

    def test_coverage_scale_has_levels(self, taxonomy_dir):
        """Test that coverage scale defines levels 0-3."""
        taxonomy_path = taxonomy_dir / "agent_taxonomy.json"

        with open(taxonomy_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        scale = data.get("metadata", {}).get("coverage_scale", {})

        # Should have definitions for levels 0-3
        for level in ["0", "1", "2", "3"]:
            assert level in scale, f"coverage_scale should define level {level}"
