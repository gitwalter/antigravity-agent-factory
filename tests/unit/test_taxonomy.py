"""
Unit tests for scripts/taxonomy/__init__.py

Tests for TopicNode, TaxonomyLoader, and load_agent_taxonomy functionality.
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.taxonomy import TopicNode, TaxonomyLoader, load_agent_taxonomy


class TestTopicNode:
    """Tests for TopicNode dataclass."""

    def test_create_topic_node(self):
        """Test creating a basic TopicNode."""
        node = TopicNode(
            name="test_topic", description="A test topic", required_depth=2
        )

        assert node.name == "test_topic"
        assert node.description == "A test topic"
        assert node.required_depth == 2
        assert node.keywords == []
        assert node.subtopics == {}
        assert node.knowledge_files == []

    def test_create_topic_node_with_keywords(self):
        """Test creating a TopicNode with keywords."""
        node = TopicNode(name="test", keywords=["keyword1", "keyword2", "keyword3"])

        assert len(node.keywords) == 3
        assert "keyword1" in node.keywords

    def test_get_all_keywords_no_subtopics(self):
        """Test get_all_keywords with no subtopics."""
        node = TopicNode(name="test", keywords=["a", "b", "c"])

        all_keywords = node.get_all_keywords()

        assert len(all_keywords) == 3
        assert set(all_keywords) == {"a", "b", "c"}

    def test_get_all_keywords_with_subtopics(self):
        """Test get_all_keywords includes subtopic keywords."""
        child = TopicNode(name="child", keywords=["child_kw"])
        parent = TopicNode(
            name="parent", keywords=["parent_kw"], subtopics={"child": child}
        )

        all_keywords = parent.get_all_keywords()

        assert "parent_kw" in all_keywords
        assert "child_kw" in all_keywords
        assert len(all_keywords) == 2

    def test_get_leaf_topics_no_children(self):
        """Test get_leaf_topics when node has no children."""
        node = TopicNode(name="leaf")

        leaves = node.get_leaf_topics()

        assert len(leaves) == 1
        assert leaves[0].name == "leaf"

    def test_get_leaf_topics_with_children(self):
        """Test get_leaf_topics returns only leaves."""
        leaf1 = TopicNode(name="leaf1")
        leaf2 = TopicNode(name="leaf2")
        parent = TopicNode(name="parent", subtopics={"leaf1": leaf1, "leaf2": leaf2})

        leaves = parent.get_leaf_topics()

        assert len(leaves) == 2
        names = {l.name for l in leaves}
        assert names == {"leaf1", "leaf2"}

    def test_count_topics_single(self):
        """Test count_topics for single node."""
        node = TopicNode(name="single")

        assert node.count_topics() == 1

    def test_count_topics_with_subtopics(self):
        """Test count_topics includes subtopics."""
        grandchild = TopicNode(name="grandchild")
        child = TopicNode(name="child", subtopics={"grandchild": grandchild})
        parent = TopicNode(name="parent", subtopics={"child": child})

        assert parent.count_topics() == 3

    def test_nested_subtopics_deep(self):
        """Test deeply nested subtopics."""
        level3 = TopicNode(name="level3", keywords=["l3"])
        level2 = TopicNode(name="level2", subtopics={"level3": level3})
        level1 = TopicNode(name="level1", subtopics={"level2": level2})
        root = TopicNode(name="root", subtopics={"level1": level1})

        assert root.count_topics() == 4
        assert len(root.get_all_keywords()) == 1


class TestTaxonomyLoader:
    """Tests for TaxonomyLoader class."""

    def test_init_default_directory(self):
        """Test TaxonomyLoader uses default directory."""
        loader = TaxonomyLoader()

        assert loader.taxonomy_dir.exists()
        assert loader._cache == {}

    def test_init_custom_directory(self, tmp_path):
        """Test TaxonomyLoader with custom directory."""
        loader = TaxonomyLoader(tmp_path)

        assert loader.taxonomy_dir == tmp_path

    def test_load_taxonomy_success(self, tmp_path, sample_taxonomy_data):
        """Test successful taxonomy loading."""
        taxonomy_file = tmp_path / "test_taxonomy.json"
        taxonomy_file.write_text(json.dumps(sample_taxonomy_data))

        loader = TaxonomyLoader(tmp_path)
        domains = loader.load_taxonomy("test_taxonomy.json")

        assert "test_domain" in domains
        assert isinstance(domains["test_domain"], TopicNode)

    def test_load_taxonomy_file_not_found(self, tmp_path):
        """Test loading non-existent taxonomy raises error."""
        loader = TaxonomyLoader(tmp_path)

        with pytest.raises(FileNotFoundError):
            loader.load_taxonomy("nonexistent.json")

    def test_load_taxonomy_invalid_json(self, tmp_path):
        """Test loading invalid JSON raises error."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{ invalid json }")

        loader = TaxonomyLoader(tmp_path)

        with pytest.raises(json.JSONDecodeError):
            loader.load_taxonomy("invalid.json")

    def test_cache_works(self, tmp_path, sample_taxonomy_data):
        """Test that taxonomy is cached after first load."""
        taxonomy_file = tmp_path / "cached.json"
        taxonomy_file.write_text(json.dumps(sample_taxonomy_data))

        loader = TaxonomyLoader(tmp_path)

        # First load
        result1 = loader.load_taxonomy("cached.json")

        # Modify file (but cache should return same result)
        taxonomy_file.write_text(json.dumps({"domains": {}}))

        # Second load should return cached version
        result2 = loader.load_taxonomy("cached.json")

        assert result1 is result2
        assert "test_domain" in result2

    def test_get_available_taxonomies(self, tmp_path):
        """Test getting list of available taxonomies."""
        (tmp_path / "agent_taxonomy.json").write_text("{}")
        (tmp_path / "other_taxonomy.json").write_text("{}")
        (tmp_path / "not_a_taxonomy.json").write_text("{}")

        loader = TaxonomyLoader(tmp_path)
        available = loader.get_available_taxonomies()

        assert "agent_taxonomy.json" in available
        assert "other_taxonomy.json" in available

    def test_get_all_topics_flat(self, tmp_path, sample_taxonomy_data):
        """Test flattening all topics from taxonomy."""
        taxonomy_file = tmp_path / "flat_test.json"
        taxonomy_file.write_text(json.dumps(sample_taxonomy_data))

        loader = TaxonomyLoader(tmp_path)
        topics = loader.get_all_topics_flat("flat_test.json")

        # Should include domain + topics
        assert len(topics) >= 3
        names = {t.name for t in topics}
        assert "test_domain" in names
        assert "test_topic" in names

    def test_parse_topic_with_subtopics(self, tmp_path):
        """Test parsing topics with nested subtopics key."""
        data = {
            "domains": {
                "domain": {
                    "description": "Test",
                    "subtopics": {
                        "sub1": {"description": "Subtopic 1", "keywords": ["kw1"]}
                    },
                }
            }
        }
        taxonomy_file = tmp_path / "subtopics_test.json"
        taxonomy_file.write_text(json.dumps(data))

        loader = TaxonomyLoader(tmp_path)
        domains = loader.load_taxonomy("subtopics_test.json")

        assert "domain" in domains
        assert "sub1" in domains["domain"].subtopics


class TestLoadAgentTaxonomy:
    """Tests for the load_agent_taxonomy convenience function."""

    def test_load_default_taxonomy(self):
        """Test loading the default agent taxonomy."""
        taxonomy = load_agent_taxonomy()

        assert isinstance(taxonomy, dict)
        assert len(taxonomy) > 0

    def test_taxonomy_has_domains(self):
        """Test that taxonomy has expected domains."""
        taxonomy = load_agent_taxonomy()

        # Should have at least some domains
        assert len(taxonomy) >= 1

        # All values should be TopicNodes
        for domain in taxonomy.values():
            assert isinstance(domain, TopicNode)

    def test_taxonomy_topics_have_keywords(self):
        """Test that taxonomy topics have keywords defined."""
        taxonomy = load_agent_taxonomy()

        def find_keywords(node):
            """Recursively check for keywords in node or subtopics."""
            if node.keywords:
                return True
            for subtopic in node.subtopics.values():
                if find_keywords(subtopic):
                    return True
            return False

        # Check at least one domain has topics with keywords
        has_keywords = False
        for domain in taxonomy.values():
            if find_keywords(domain):
                has_keywords = True
                break

        assert has_keywords, "Taxonomy should have topics with keywords"
