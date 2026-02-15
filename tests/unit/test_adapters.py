"""
Unit Tests for Knowledge Source Adapters

Tests the source adapters including:
- Base adapter functionality
- GitHub adapter
- PyPI adapter
- NPM adapter

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

import pytest
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from adapters.base_adapter import (
    BaseAdapter,
    AdapterConfig,
    KnowledgeUpdate,
    KnowledgeChange,
    UpdateSource,
    UpdatePriority,
    TrustLevel,
    ChangeType,
)


class TestAdapterConfig:
    """Tests for AdapterConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AdapterConfig()

        assert config.enabled is True
        assert config.api_key is None
        assert config.rate_limit_rpm == 60
        assert config.timeout_seconds == 30
        assert config.trust_level == TrustLevel.COMMUNITY

    def test_custom_values(self):
        """Test custom configuration values."""
        config = AdapterConfig(
            enabled=False, api_key="test_key", trust_level=TrustLevel.OFFICIAL
        )

        assert config.enabled is False
        assert config.api_key == "test_key"
        assert config.trust_level == TrustLevel.OFFICIAL


class TestUpdateSource:
    """Tests for UpdateSource dataclass."""

    def test_creation(self):
        """Test creating an update source."""
        source = UpdateSource(
            adapter_type="github",
            identifier="tiangolo/fastapi",
            version="0.115.0",
            url="https://github.com/tiangolo/fastapi",
        )

        assert source.adapter_type == "github"
        assert source.identifier == "tiangolo/fastapi"
        assert source.version == "0.115.0"

    def test_default_timestamp(self):
        """Test that timestamp is set automatically."""
        source = UpdateSource(adapter_type="test", identifier="test")

        assert source.fetched_at is not None
        assert isinstance(source.fetched_at, datetime)


class TestKnowledgeChange:
    """Tests for KnowledgeChange dataclass."""

    def test_creation(self):
        """Test creating a knowledge change."""
        change = KnowledgeChange(
            change_type=ChangeType.ADDED,
            path="patterns.new_pattern",
            description="Added new pattern for async handlers",
        )

        assert change.change_type == ChangeType.ADDED
        assert change.path == "patterns.new_pattern"
        assert change.impact == "medium"  # default

    def test_with_values(self):
        """Test change with old and new values."""
        change = KnowledgeChange(
            change_type=ChangeType.CHANGED,
            path="version",
            description="Updated version",
            old_value="1.0.0",
            new_value="2.0.0",
        )

        assert change.old_value == "1.0.0"
        assert change.new_value == "2.0.0"


class TestKnowledgeUpdate:
    """Tests for KnowledgeUpdate dataclass."""

    def test_creation(self):
        """Test creating a knowledge update."""
        source = UpdateSource(adapter_type="test", identifier="test")
        changes = [
            KnowledgeChange(
                change_type=ChangeType.ADDED, path="test", description="Test change"
            )
        ]

        update = KnowledgeUpdate(
            target_file="test-patterns.json",
            priority=UpdatePriority.MEDIUM,
            source=source,
            changes=changes,
            new_version="1.1.0",
        )

        assert update.target_file == "test-patterns.json"
        assert update.priority == UpdatePriority.MEDIUM
        assert len(update.changes) == 1

    def test_checksum_generation(self):
        """Test that checksum is generated for proposed content."""
        source = UpdateSource(adapter_type="test", identifier="test")

        update = KnowledgeUpdate(
            target_file="test.json",
            priority=UpdatePriority.LOW,
            source=source,
            changes=[],
            new_version="1.0.0",
            proposed_content={"key": "value"},
        )

        assert update.checksum is not None
        assert len(update.checksum) == 64  # SHA-256 hex

    def test_to_dict(self):
        """Test serialization to dictionary."""
        source = UpdateSource(adapter_type="github", identifier="test/repo")
        changes = [
            KnowledgeChange(
                change_type=ChangeType.ADDED, path="test", description="Test"
            )
        ]

        update = KnowledgeUpdate(
            target_file="test.json",
            priority=UpdatePriority.HIGH,
            source=source,
            changes=changes,
            new_version="1.0.0",
        )

        result = update.to_dict()

        assert result["target_file"] == "test.json"
        assert result["priority"] == "HIGH"
        assert result["source"]["adapter_type"] == "github"
        assert len(result["changes"]) == 1


class TestUpdatePriority:
    """Tests for UpdatePriority enum."""

    def test_priority_ordering(self):
        """Test that priorities are correctly ordered."""
        assert UpdatePriority.CRITICAL.value < UpdatePriority.HIGH.value
        assert UpdatePriority.HIGH.value < UpdatePriority.MEDIUM.value
        assert UpdatePriority.MEDIUM.value < UpdatePriority.LOW.value
        assert UpdatePriority.LOW.value < UpdatePriority.INFO.value


class TestTrustLevel:
    """Tests for TrustLevel enum."""

    def test_trust_levels(self):
        """Test trust level values."""
        assert TrustLevel.OFFICIAL.value < TrustLevel.VERIFIED.value
        assert TrustLevel.VERIFIED.value < TrustLevel.COMMUNITY.value
        assert TrustLevel.COMMUNITY.value < TrustLevel.EXPERIMENTAL.value


class ConcreteAdapter(BaseAdapter):
    """Concrete implementation for testing."""

    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Test adapter"

    async def fetch_updates(self, target_files=None, since=None):
        return []

    async def validate_connection(self) -> bool:
        return True


class TestBaseAdapter:
    """Tests for BaseAdapter abstract class."""

    def test_concrete_implementation(self):
        """Test that concrete implementation works."""
        config = AdapterConfig()
        adapter = ConcreteAdapter(config)

        assert adapter.name == "test"
        assert adapter.description == "Test adapter"

    def test_create_source(self):
        """Test create_source helper method."""
        config = AdapterConfig(trust_level=TrustLevel.OFFICIAL)
        adapter = ConcreteAdapter(config)

        source = adapter.create_source(
            identifier="test/repo", version="1.0.0", url="https://example.com"
        )

        assert source.adapter_type == "test"
        assert source.identifier == "test/repo"
        assert source.trust_level == TrustLevel.OFFICIAL

    def test_caching(self):
        """Test cache methods."""
        config = AdapterConfig(cache_ttl_hours=24)
        adapter = ConcreteAdapter(config)

        # Should need refresh initially
        assert adapter._should_refresh_cache("test_key") is True

        # Set cache
        adapter._set_cached("test_key", {"data": "test"})

        # Should not need refresh
        assert adapter._should_refresh_cache("test_key") is False

        # Should get cached data
        cached = adapter._get_cached("test_key")
        assert cached == {"data": "test"}

    def test_repr(self):
        """Test string representation."""
        config = AdapterConfig(enabled=True)
        adapter = ConcreteAdapter(config)

        repr_str = repr(adapter)
        assert "ConcreteAdapter" in repr_str
        assert "enabled" in repr_str


class TestGitHubAdapter:
    """Tests for GitHub adapter."""

    def test_import(self):
        """Test that GitHub adapter can be imported."""
        from adapters.github_adapter import GitHubAdapter

        config = AdapterConfig()
        adapter = GitHubAdapter(config)

        assert adapter.name == "github"

    def test_tracked_repos(self):
        """Test that tracked repos are defined."""
        from adapters.github_adapter import GitHubAdapter

        config = AdapterConfig()
        adapter = GitHubAdapter(config)

        assert len(adapter.TRACKED_REPOS) > 0
        assert any(r.name == "fastapi" for r in adapter.TRACKED_REPOS)


class TestPyPIAdapter:
    """Tests for PyPI adapter."""

    def test_import(self):
        """Test that PyPI adapter can be imported."""
        from adapters.pypi_adapter import PyPIAdapter

        config = AdapterConfig()
        adapter = PyPIAdapter(config)

        assert adapter.name == "pypi"

    def test_tracked_packages(self):
        """Test that tracked packages are defined."""
        from adapters.pypi_adapter import PyPIAdapter

        config = AdapterConfig()
        adapter = PyPIAdapter(config)

        assert len(adapter.TRACKED_PACKAGES) > 0
        assert any(p.name == "fastapi" for p in adapter.TRACKED_PACKAGES)


class TestNPMAdapter:
    """Tests for NPM adapter."""

    def test_import(self):
        """Test that NPM adapter can be imported."""
        from adapters.npm_adapter import NPMAdapter

        config = AdapterConfig()
        adapter = NPMAdapter(config)

        assert adapter.name == "npm"

    def test_tracked_packages(self):
        """Test that tracked packages are defined."""
        from adapters.npm_adapter import NPMAdapter

        config = AdapterConfig()
        adapter = NPMAdapter(config)

        assert len(adapter.TRACKED_PACKAGES) > 0
        assert any(p.name == "react" for p in adapter.TRACKED_PACKAGES)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
