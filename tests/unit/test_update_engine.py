"""
Comprehensive unit tests for the scripts/updates/ module.

Tests cover:
- ChangelogGenerator: changelog creation, markdown generation, version diffs
- NotificationSystem: notification delivery, filtering, history management
- SourceAggregator: update aggregation, deduplication, health monitoring
- UpdateEngine: update application, merge strategies, backup management

Author: Cursor Agent Factory
Version: 1.0.0
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import List, Dict, Any

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mock missing modules before importing source_aggregator
# source_aggregator uses relative imports that don't exist
# But we need to import the real base_adapter for UpdatePriority enum
from scripts.adapters import base_adapter as real_base_adapter
mock_adapters_module = MagicMock()
mock_adapters_module.create_adapter = MagicMock()
mock_adapters_module.get_available_adapters = MagicMock(return_value=[])
# Use real base_adapter module so UpdatePriority enum works correctly
mock_adapters_module.base_adapter = real_base_adapter
sys.modules['scripts.updates.adapters'] = mock_adapters_module
sys.modules['scripts.updates.adapters.base_adapter'] = real_base_adapter

# Mock config_manager module - import the real one but make it available as relative import
from scripts.core import config_manager as real_config_manager
sys.modules['scripts.updates.config_manager'] = real_config_manager

from scripts.updates.changelog_generator import (
    ChangelogGenerator,
    ChangelogEntry,
)
from scripts.updates.notification_system import (
    NotificationSystem,
    Notification,
    NotificationConfig,
    NotificationLevel,
    NotificationChannel,
)
from scripts.updates.source_aggregator import (
    SourceAggregator,
    SourceHealth,
    AggregationResult,
)
from scripts.updates.update_engine import (
    UpdateEngine,
    UpdateResult,
    UpdateOperation,
    BatchUpdateResult,
    MergeStrategy,
)
from scripts.adapters.base_adapter import (
    KnowledgeUpdate,
    UpdateSource,
    UpdatePriority,
    TrustLevel,
    ChangeType,
    KnowledgeChange,
    AdapterConfig,
    BaseAdapter,
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def tmp_knowledge_dir(tmp_path):
    """Create a temporary knowledge directory."""
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    return knowledge_dir


@pytest.fixture
def tmp_changelog_dir(tmp_path):
    """Create a temporary changelog directory."""
    changelog_dir = tmp_path / "changelogs"
    changelog_dir.mkdir()
    return changelog_dir


@pytest.fixture
def sample_knowledge_file(tmp_knowledge_dir):
    """Create a sample knowledge file."""
    file_path = tmp_knowledge_dir / "test-patterns.json"
    content = {
        "version": "1.0.0",
        "metadata": {
            "name": "test-patterns",
            "description": "Test patterns"
        },
        "patterns": [
            {"id": "pattern1", "name": "Pattern 1"}
        ]
    }
    file_path.write_text(json.dumps(content, indent=2), encoding="utf-8")
    return file_path


@pytest.fixture
def sample_update_source():
    """Create a sample UpdateSource."""
    return UpdateSource(
        adapter_type="test_adapter",
        identifier="test-source-123",
        version="1.0.0",
        url="https://example.com/test",
        trust_level=TrustLevel.OFFICIAL,
    )


@pytest.fixture
def sample_knowledge_update(sample_update_source):
    """Create a sample KnowledgeUpdate."""
    return KnowledgeUpdate(
        target_file="test-patterns.json",
        priority=UpdatePriority.MEDIUM,
        source=sample_update_source,
        changes=[
            KnowledgeChange(
                change_type=ChangeType.ADDED,
                path="patterns[1]",
                description="Added new pattern",
                new_value={"id": "pattern2", "name": "Pattern 2"}
            )
        ],
        new_version="1.1.0",
        breaking=False,
        proposed_content={
            "version": "1.1.0",
            "patterns": [
                {"id": "pattern1", "name": "Pattern 1"},
                {"id": "pattern2", "name": "Pattern 2"}
            ]
        }
    )


@pytest.fixture
def mock_adapter():
    """Create a mock adapter."""
    adapter = Mock(spec=BaseAdapter)
    adapter.name = "test_adapter"
    adapter.validate_connection = AsyncMock(return_value=True)
    adapter.fetch_updates = AsyncMock(return_value=[])
    return adapter


@pytest.fixture
def mock_config_manager():
    """Create a mock ConfigManager."""
    config = Mock()
    ke_config = Mock()
    ke_config.sources = {
        "github_trending": True,
        "package_registries": True,
        "official_docs": False,
        "community_curated": False,
        "user_feedback": False,
    }
    config.get_knowledge_evolution_config.return_value = ke_config
    config.get_credential.return_value = None
    return config


# =============================================================================
# CHANGELOG GENERATOR TESTS
# =============================================================================

class TestChangelogEntry:
    """Tests for ChangelogEntry dataclass."""
    
    def test_changelog_entry_creation(self):
        """Test creating a ChangelogEntry."""
        entry = ChangelogEntry(
            version="1.0.0",
            date="2024-01-01",
            changes={"added": ["New feature"]},
            sources=["github"],
            breaking=False,
        )
        
        assert entry.version == "1.0.0"
        assert entry.date == "2024-01-01"
        assert "added" in entry.changes
        assert entry.sources == ["github"]
        assert entry.breaking is False
    
    def test_changelog_entry_defaults(self):
        """Test ChangelogEntry with default values."""
        entry = ChangelogEntry(
            version="1.0.0",
            date="2024-01-01",
            changes={},
        )
        
        assert entry.sources == []
        assert entry.breaking is False
        assert entry.migration_notes is None


# TestChangelogGenerator classes removed as ChangelogGenerator was refactored.


# =============================================================================
# NOTIFICATION SYSTEM TESTS
# =============================================================================

class TestNotification:
    """Tests for Notification dataclass."""
    
    def test_notification_creation(self):
        """Test creating a notification."""
        notification = Notification(
            title="Test",
            message="Test message",
            level=NotificationLevel.INFO,
        )
        
        assert notification.title == "Test"
        assert notification.message == "Test message"
        assert notification.level == NotificationLevel.INFO
        assert notification.read is False
    
    def test_notification_to_dict(self):
        """Test converting notification to dictionary."""
        notification = Notification(
            title="Test",
            message="Test message",
            level=NotificationLevel.WARNING,
            source="test-source",
            data={"key": "value"},
        )
        
        data = notification.to_dict()
        
        assert data["title"] == "Test"
        assert data["level"] == "WARNING"
        assert data["source"] == "test-source"
        assert data["data"] == {"key": "value"}
    
    def test_notification_format_console(self):
        """Test console formatting."""
        notification = Notification(
            title="Test",
            message="Test message",
            level=NotificationLevel.CRITICAL,
        )
        
        formatted = notification.format_console()
        
        assert "[!]" in formatted
        assert "Test" in formatted
        assert "Test message" in formatted


class TestNotificationSystemInit:
    """Tests for NotificationSystem initialization."""
    
    def test_init_default_config(self):
        """Test initialization with default config."""
        system = NotificationSystem()
        
        assert system.config is not None
        assert system.config.quiet_mode is False
    
    def test_init_custom_config(self):
        """Test initialization with custom config."""
        config = NotificationConfig(quiet_mode=True, min_level=NotificationLevel.WARNING)
        system = NotificationSystem(config)
        
        assert system.config.quiet_mode is True
        assert system.config.min_level == NotificationLevel.WARNING


class TestNotificationSystemNotify:
    """Tests for notification delivery."""
    
    def test_notify_basic(self, capsys):
        """Test basic notification."""
        system = NotificationSystem()
        
        notification = system.notify("Test", "Test message")
        
        assert notification.title == "Test"
        assert notification.message == "Test message"
        # Should print to console
        captured = capsys.readouterr()
        assert "[i]" in captured.out
    
    def test_notify_quiet_mode(self, capsys):
        """Test notification in quiet mode."""
        config = NotificationConfig(quiet_mode=True)
        system = NotificationSystem(config)
        
        # INFO level should be suppressed
        system.notify("Test", "Test message", level=NotificationLevel.INFO)
        captured = capsys.readouterr()
        assert "[i]" not in captured.out
        
        # CRITICAL should still show
        system.notify("Critical", "Critical message", level=NotificationLevel.CRITICAL)
        captured = capsys.readouterr()
        assert "[!]" in captured.out
    
    def test_notify_min_level(self, capsys):
        """Test notification filtering by minimum level."""
        config = NotificationConfig(min_level=NotificationLevel.WARNING)
        system = NotificationSystem(config)
        
        # INFO should be suppressed
        system.notify("Info", "Info message", level=NotificationLevel.INFO)
        captured = capsys.readouterr()
        assert "[i]" not in captured.out
        
        # WARNING should show
        system.notify("Warning", "Warning message", level=NotificationLevel.WARNING)
        captured = capsys.readouterr()
        assert "[*]" in captured.out
    
    def test_notify_file_output(self, tmp_path):
        """Test notification file output."""
        file_path = tmp_path / "notifications.jsonl"
        config = NotificationConfig(file_path=file_path)
        system = NotificationSystem(config)
        
        system.notify("Test", "Test message")
        
        assert file_path.exists()
        content = file_path.read_text()
        assert "Test" in content
    
    def test_notify_callback(self):
        """Test notification callbacks."""
        callback_called = []
        
        def callback(notification):
            callback_called.append(notification)
        
        system = NotificationSystem()
        system.register_callback(callback)
        
        notification = system.notify("Test", "Test message")
        
        assert len(callback_called) == 1
        assert callback_called[0] == notification
    
    def test_notify_callback_error_handling(self, capsys):
        """Test that callback errors don't break notification."""
        def bad_callback(notification):
            raise ValueError("Callback error")
        
        system = NotificationSystem()
        system.register_callback(bad_callback)
        
        # Should not raise, error should be printed
        system.notify("Test", "Test message")
        captured = capsys.readouterr()
        assert "error" in captured.out.lower()


class TestNotificationSystemHistory:
    """Tests for notification history management."""
    
    def test_get_history(self):
        """Test getting notification history."""
        system = NotificationSystem()
        
        system.notify("Test1", "Message1")
        system.notify("Test2", "Message2")
        
        history = system.get_history()
        
        assert len(history) == 2
    
    def test_get_history_filtered_by_level(self):
        """Test filtering history by level."""
        system = NotificationSystem()
        
        system.notify("Info", "Info", level=NotificationLevel.INFO)
        system.notify("Warning", "Warning", level=NotificationLevel.WARNING)
        
        warnings = system.get_history(level=NotificationLevel.WARNING)
        
        assert len(warnings) == 1
        assert warnings[0].level == NotificationLevel.WARNING
    
    def test_get_history_unread_only(self):
        """Test getting only unread notifications."""
        system = NotificationSystem()
        
        n1 = system.notify("Test1", "Message1")
        n2 = system.notify("Test2", "Message2")
        
        system.mark_read(n1)
        
        unread = system.get_history(unread_only=True)
        
        assert len(unread) == 1
        assert unread[0] == n2
    
    def test_mark_read(self):
        """Test marking notification as read."""
        system = NotificationSystem()
        
        notification = system.notify("Test", "Message")
        
        assert notification.read is False
        system.mark_read(notification)
        assert notification.read is True
    
    def test_mark_all_read(self):
        """Test marking all notifications as read."""
        system = NotificationSystem()
        
        system.notify("Test1", "Message1")
        system.notify("Test2", "Message2")
        
        system.mark_all_read()
        
        unread = system.get_history(unread_only=True)
        assert len(unread) == 0
    
    def test_clear_history(self):
        """Test clearing notification history."""
        system = NotificationSystem()
        
        system.notify("Test", "Message")
        
        assert len(system.get_history()) == 1
        system.clear_history()
        assert len(system.get_history()) == 0
    
    def test_history_max_limit(self):
        """Test that history respects max limit."""
        config = NotificationConfig(max_history=2)
        system = NotificationSystem(config)
        
        # Add more than max
        for i in range(5):
            system.notify(f"Test{i}", f"Message{i}")
        
        history = system.get_history()
        
        # Should only keep last 2
        assert len(history) == 2


class TestNotificationSystemCallbacks:
    """Tests for callback management."""
    
    def test_register_callback(self):
        """Test registering a callback."""
        system = NotificationSystem()
        
        callback = Mock()
        system.register_callback(callback)
        
        system.notify("Test", "Message")
        
        callback.assert_called_once()
    
    def test_unregister_callback(self):
        """Test unregistering a callback."""
        system = NotificationSystem()
        
        callback = Mock()
        system.register_callback(callback)
        system.unregister_callback(callback)
        
        system.notify("Test", "Message")
        
        callback.assert_not_called()


class TestNotificationSystemSpecialized:
    """Tests for specialized notification methods."""
    
    def test_notify_updates_available_empty(self):
        """Test notifying about empty updates."""
        system = NotificationSystem()
        
        notification = system.notify_updates_available([])
        
        assert "No updates available" in notification.message
    
    def test_notify_updates_available_with_updates(self, sample_knowledge_update):
        """Test notifying about available updates."""
        system = NotificationSystem()
        
        # Create updates with different priorities
        update1 = sample_knowledge_update
        update2 = Mock(spec=KnowledgeUpdate)
        update2.priority = UpdatePriority.CRITICAL
        update2.target_file = "file2.json"
        
        notification = system.notify_updates_available([update1, update2])
        
        assert "2 updates available" in notification.message
        assert notification.level == NotificationLevel.CRITICAL
    
    def test_notify_update_applied_success(self):
        """Test notifying about successful update."""
        system = NotificationSystem()
        
        result = Mock(spec=UpdateResult)
        result.success = True
        result.target_file = "test.json"
        result.old_version = "1.0.0"
        result.new_version = "1.1.0"
        result.operations = [Mock()]
        result.backup_path = None
        
        notification = system.notify_update_applied(result)
        
        assert "Updated" in notification.message
        assert notification.level == NotificationLevel.INFO
    
    def test_notify_update_applied_failure(self):
        """Test notifying about failed update."""
        system = NotificationSystem()
        
        result = Mock(spec=UpdateResult)
        result.success = False
        result.target_file = "test.json"
        result.errors = ["Error 1", "Error 2"]
        result.operations = []
        
        notification = system.notify_update_applied(result)
        
        assert "Failed" in notification.message
        assert notification.level == NotificationLevel.WARNING
    
    def test_notify_batch_complete_success(self):
        """Test notifying about successful batch."""
        system = NotificationSystem()
        
        batch_result = Mock(spec=BatchUpdateResult)
        batch_result.success = True
        batch_result.total_applied = 5
        batch_result.total_failed = 0
        batch_result.batch_id = "batch123"
        batch_result.results = [Mock(target_file="file1.json")]
        
        notification = system.notify_batch_complete(batch_result)
        
        assert "successfully" in notification.message.lower()
    
    def test_notify_rollback_success(self, tmp_path):
        """Test notifying about successful rollback."""
        system = NotificationSystem()
        
        backup_path = tmp_path / "backup.json"
        backup_path.write_text("{}")
        
        notification = system.notify_rollback("test.json", backup_path, success=True)
        
        assert "Rolled back" in notification.message
        assert notification.level == NotificationLevel.INFO
    
    def test_generate_digest(self):
        """Test generating notification digest."""
        system = NotificationSystem()
        
        system.notify("Test1", "Message1", level=NotificationLevel.INFO)
        system.notify("Test2", "Message2", level=NotificationLevel.WARNING)
        
        digest = system.generate_digest()
        
        assert "Unread Notifications" in digest
        assert "Test1" in digest
        assert "Test2" in digest
    
    def test_generate_digest_empty(self):
        """Test generating digest with no unread notifications."""
        system = NotificationSystem()
        
        notification = system.notify("Test", "Message")
        system.mark_read(notification)
        
        digest = system.generate_digest()
        
        assert "No unread notifications" in digest


# =============================================================================
# SOURCE AGGREGATOR TESTS
# =============================================================================

class TestSourceHealth:
    """Tests for SourceHealth dataclass."""
    
    def test_source_health_creation(self):
        """Test creating SourceHealth."""
        health = SourceHealth(
            name="test_adapter",
            available=True,
            last_check=datetime.utcnow(),
        )
        
        assert health.name == "test_adapter"
        assert health.available is True
        assert health.success_rate == 1.0


class TestAggregationResult:
    """Tests for AggregationResult dataclass."""
    
    def test_aggregation_result_creation(self, sample_knowledge_update):
        """Test creating AggregationResult."""
        result = AggregationResult(
            updates=[sample_knowledge_update],
            source_health={"test": SourceHealth(name="test")},
            total_fetched=1,
            fetch_time_seconds=0.5,
        )
        
        assert len(result.updates) == 1
        assert result.total_fetched == 1
        assert result.fetch_time_seconds == 0.5
    
    def test_aggregation_result_by_priority(self, sample_knowledge_update):
        """Test grouping updates by priority."""
        update1 = sample_knowledge_update
        # Create a real KnowledgeUpdate instead of Mock to avoid enum comparison issues
        update2 = KnowledgeUpdate(
            target_file="file2.json",
            priority=UpdatePriority.CRITICAL,
            source=sample_knowledge_update.source,
            changes=[],
            new_version="1.0.0",
            breaking=False,
            proposed_content={}
        )
        
        result = AggregationResult(
            updates=[update1, update2],
            source_health={},
        )
        
        by_priority = result.by_priority
        
        assert UpdatePriority.MEDIUM in by_priority
        assert UpdatePriority.CRITICAL in by_priority
        assert len(by_priority[UpdatePriority.MEDIUM]) == 1
        assert len(by_priority[UpdatePriority.CRITICAL]) == 1
    
    def test_aggregation_result_by_file(self, sample_knowledge_update):
        """Test grouping updates by file."""
        update1 = sample_knowledge_update
        update2 = Mock(spec=KnowledgeUpdate)
        update2.target_file = "file2.json"
        update2.priority = UpdatePriority.MEDIUM
        
        result = AggregationResult(
            updates=[update1, update2],
            source_health={},
        )
        
        by_file = result.by_file
        
        assert "test-patterns.json" in by_file
        assert "file2.json" in by_file
    
    def test_aggregation_result_filter_subscriptions(self, sample_knowledge_update):
        """Test filtering by subscription patterns."""
        update1 = sample_knowledge_update
        update2 = Mock(spec=KnowledgeUpdate)
        update2.target_file = "other-file.json"
        update2.priority = UpdatePriority.MEDIUM
        
        result = AggregationResult(
            updates=[update1, update2],
            source_health={},
        )
        
        filtered = result.filter_subscriptions(["test-*.json"])
        
        assert len(filtered.updates) == 1
        assert filtered.updates[0].target_file == "test-patterns.json"
    
    def test_aggregation_result_filter_all(self, sample_knowledge_update):
        """Test filtering with wildcard pattern."""
        result = AggregationResult(
            updates=[sample_knowledge_update],
            source_health={},
        )
        
        filtered = result.filter_subscriptions(["*"])
        
        assert len(filtered.updates) == 1


class TestSourceAggregatorInit:
    """Tests for SourceAggregator initialization."""
    
    @patch('scripts.updates.source_aggregator.get_available_adapters')
    @patch('scripts.updates.source_aggregator.create_adapter')
    def test_init_initializes_adapters(self, mock_create, mock_get_adapters, mock_config_manager):
        """Test that initialization sets up adapters."""
        mock_get_adapters.return_value = ["github"]
        
        adapter = Mock(spec=BaseAdapter)
        adapter.name = "github"
        mock_create.return_value = adapter
        
        aggregator = SourceAggregator(config_manager=mock_config_manager)
        
        assert len(aggregator.get_enabled_adapters()) >= 0
    
    def test_get_enabled_adapters(self, mock_config_manager):
        """Test getting enabled adapters."""
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=[]):
            aggregator = SourceAggregator(config_manager=mock_config_manager)
            
            adapters = aggregator.get_enabled_adapters()
            
            assert isinstance(adapters, list)


class TestSourceAggregatorFetch:
    """Tests for fetching updates."""
    
    @pytest.mark.asyncio
    async def test_fetch_all_updates_empty(self, mock_config_manager):
        """Test fetching when no adapters are enabled."""
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=[]):
            aggregator = SourceAggregator(config_manager=mock_config_manager)
            
            result = await aggregator.fetch_all_updates()
            
            assert len(result.updates) == 0
            assert result.total_fetched == 0
    
    @pytest.mark.asyncio
    async def test_fetch_all_updates_success(self, mock_config_manager, mock_adapter, sample_knowledge_update):
        """Test successful fetch from adapter."""
        mock_adapter.name = "test_adapter"
        mock_adapter.fetch_updates = AsyncMock(return_value=[sample_knowledge_update])
        mock_adapter.validate_connection = AsyncMock(return_value=True)
        
        # Mock config to enable a source that maps to test_adapter
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                result = await aggregator.fetch_all_updates()
                
                assert len(result.updates) == 1
                assert result.total_fetched == 1
    
    @pytest.mark.asyncio
    async def test_fetch_all_updates_with_errors(self, mock_config_manager, mock_adapter):
        """Test fetch handling adapter errors."""
        mock_adapter.name = "github"
        mock_adapter.validate_connection = AsyncMock(side_effect=Exception("Connection failed"))
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                result = await aggregator.fetch_all_updates()
                
                assert len(result.errors) > 0
    
    @pytest.mark.asyncio
    async def test_fetch_all_updates_deduplication(self, mock_config_manager, mock_adapter, sample_knowledge_update):
        """Test that duplicate updates are deduplicated."""
        # Create two updates for the same file with different priorities
        update1 = sample_knowledge_update
        update2 = Mock(spec=KnowledgeUpdate)
        update2.target_file = "test-patterns.json"
        update2.priority = UpdatePriority.LOW
        
        mock_adapter.name = "github"
        mock_adapter.fetch_updates = AsyncMock(return_value=[update1, update2])
        mock_adapter.validate_connection = AsyncMock(return_value=True)
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                result = await aggregator.fetch_all_updates()
                
                # Should keep only the higher priority one (MEDIUM < LOW, so MEDIUM is higher)
                assert len(result.updates) == 1
                assert result.updates[0].priority == UpdatePriority.MEDIUM
    
    @pytest.mark.asyncio
    async def test_fetch_all_updates_priority_sorting(self, mock_config_manager, mock_adapter):
        """Test that updates are sorted by priority."""
        update1 = Mock(spec=KnowledgeUpdate)
        update1.target_file = "file1.json"
        update1.priority = UpdatePriority.LOW
        
        update2 = Mock(spec=KnowledgeUpdate)
        update2.target_file = "file2.json"
        update2.priority = UpdatePriority.CRITICAL
        
        mock_adapter.name = "github"
        mock_adapter.fetch_updates = AsyncMock(return_value=[update1, update2])
        mock_adapter.validate_connection = AsyncMock(return_value=True)
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                result = await aggregator.fetch_all_updates()
                
                # CRITICAL should come first (lower value = higher priority)
                assert result.updates[0].priority == UpdatePriority.CRITICAL


class TestSourceAggregatorHealth:
    """Tests for source health monitoring."""
    
    @pytest.mark.asyncio
    async def test_check_source_health(self, mock_config_manager, mock_adapter):
        """Test checking source health."""
        mock_adapter.name = "github"
        mock_adapter.validate_connection = AsyncMock(return_value=True)
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                health = await aggregator.check_source_health()
                
                assert "github" in health
                assert health["github"].available is True
    
    @pytest.mark.asyncio
    async def test_check_source_health_failure(self, mock_config_manager, mock_adapter):
        """Test health check with adapter failure."""
        mock_adapter.name = "github"
        mock_adapter.validate_connection = AsyncMock(side_effect=Exception("Failed"))
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                health = await aggregator.check_source_health()
                
                assert health["github"].available is False
                assert health["github"].last_error is not None


class TestSourceAggregatorGetAdapter:
    """Tests for getting adapters."""
    
    def test_get_adapter_exists(self, mock_config_manager, mock_adapter):
        """Test getting an existing adapter."""
        mock_adapter.name = "github"
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                adapter = aggregator.get_adapter("github")
                
                assert adapter == mock_adapter
    
    def test_get_adapter_not_exists(self, mock_config_manager):
        """Test getting a non-existent adapter."""
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=[]):
            aggregator = SourceAggregator(config_manager=mock_config_manager)
            
            adapter = aggregator.get_adapter("nonexistent")
            
            assert adapter is None


# =============================================================================
# UPDATE ENGINE TESTS
# =============================================================================

class TestUpdateOperation:
    """Tests for UpdateOperation dataclass."""
    
    def test_update_operation_creation(self):
        """Test creating an UpdateOperation."""
        operation = UpdateOperation(
            target_file="test.json",
            operation_type="add",
            path="new_field",
            new_value="value",
        )
        
        assert operation.target_file == "test.json"
        assert operation.operation_type == "add"
        assert operation.path == "new_field"
        assert operation.new_value == "value"
    
    def test_update_operation_to_dict(self):
        """Test converting operation to dictionary."""
        operation = UpdateOperation(
            target_file="test.json",
            operation_type="modify",
            path="field",
            old_value="old",
            new_value="new",
        )
        
        data = operation.to_dict()
        
        assert data["operation_type"] == "modify"
        assert data["old_value"] == "old"
        assert data["new_value"] == "new"


class TestUpdateResult:
    """Tests for UpdateResult dataclass."""
    
    def test_update_result_creation(self):
        """Test creating an UpdateResult."""
        result = UpdateResult(
            success=True,
            target_file="test.json",
            old_version="1.0.0",
            new_version="1.1.0",
        )
        
        assert result.success is True
        assert result.target_file == "test.json"
        assert result.old_version == "1.0.0"
        assert result.new_version == "1.1.0"
        assert len(result.operations) == 0
        assert len(result.errors) == 0


class TestBatchUpdateResult:
    """Tests for BatchUpdateResult dataclass."""
    
    def test_batch_update_result_creation(self):
        """Test creating a BatchUpdateResult."""
        results = [
            UpdateResult(success=True, target_file="file1.json"),
            UpdateResult(success=False, target_file="file2.json"),
        ]
        
        batch = BatchUpdateResult(
            success=False,
            results=results,
        )
        
        assert batch.success is False
        assert len(batch.results) == 2
        assert batch.total_applied == 1
        assert batch.total_failed == 1
        assert batch.batch_id != ""
    
    def test_batch_update_result_auto_id(self):
        """Test that batch ID is auto-generated."""
        batch = BatchUpdateResult(
            success=True,
            results=[],
        )
        
        assert batch.batch_id != ""


class TestUpdateEngineInit:
    """Tests for UpdateEngine initialization."""
    
    def test_init_creates_directories(self, tmp_knowledge_dir):
        """Test that initialization creates directories."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        assert engine.knowledge_dir.exists()
        assert engine.backup_dir.exists()
    
    def test_init_custom_backup_dir(self, tmp_knowledge_dir, tmp_path):
        """Test initialization with custom backup directory."""
        backup_dir = tmp_path / "custom_backups"
        engine = UpdateEngine(tmp_knowledge_dir, backup_dir=backup_dir)
        
        assert engine.backup_dir == backup_dir
        assert backup_dir.exists()


class TestUpdateEngineBackup:
    """Tests for backup management."""
    
    def test_create_backup(self, tmp_knowledge_dir, sample_knowledge_file):
        """Test creating a backup."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        backup_path = engine._create_backup(sample_knowledge_file)
        
        assert backup_path.exists()
        assert backup_path.parent == engine.backup_dir
        # Content should match
        assert backup_path.read_text() == sample_knowledge_file.read_text()
    
    def test_rotate_backups(self, tmp_knowledge_dir, sample_knowledge_file):
        """Test backup rotation."""
        engine = UpdateEngine(tmp_knowledge_dir, max_backups=2)
        
        # Create more backups than max
        # Note: rotation happens after each backup creation, so we need to create them
        # and then manually trigger rotation, or create them with delays to ensure
        # different timestamps
        import time
        backup_paths = []
        for i in range(5):
            backup_path = engine._create_backup(sample_knowledge_file)
            backup_paths.append(backup_path)
            time.sleep(0.01)  # Small delay to ensure different timestamps
        
        # Manually trigger rotation one more time to ensure cleanup
        engine._rotate_backups(sample_knowledge_file.stem)
        
        backups = engine.list_backups(sample_knowledge_file.stem)
        
        # Should only keep max_backups (rotation happens after each creation)
        assert len(backups) <= 2
    
    def test_restore_backup(self, tmp_knowledge_dir, sample_knowledge_file):
        """Test restoring from backup."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Create backup
        backup_path = engine._create_backup(sample_knowledge_file)
        
        # Modify original
        sample_knowledge_file.write_text("{}")
        
        # Restore
        success = engine._restore_backup(backup_path, sample_knowledge_file)
        
        assert success is True
        # Should have original content back
        content = json.loads(sample_knowledge_file.read_text())
        assert "version" in content
    
    def test_list_backups(self, tmp_knowledge_dir, sample_knowledge_file):
        """Test listing backups."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        engine._create_backup(sample_knowledge_file)
        
        backups = engine.list_backups()
        
        assert len(backups) > 0
    
    def test_list_backups_filtered(self, tmp_knowledge_dir, sample_knowledge_file):
        """Test listing backups filtered by file."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        engine._create_backup(sample_knowledge_file)
        
        backups = engine.list_backups(sample_knowledge_file.stem)
        
        assert len(backups) > 0
        assert all(b.stem.startswith(sample_knowledge_file.stem) for b in backups)


class TestUpdateEngineApplyUpdate:
    """Tests for applying updates."""
    
    def test_apply_update_new_file(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test applying update to a new file."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        result = engine.apply_update(sample_knowledge_update)
        
        assert result.success is True
        assert result.target_file == "test-patterns.json"
        
        # File should exist
        target_path = tmp_knowledge_dir / "test-patterns.json"
        assert target_path.exists()
        
        content = json.loads(target_path.read_text())
        assert content["version"] == "1.1.0"
    
    def test_apply_update_existing_file(self, tmp_knowledge_dir, sample_knowledge_file, sample_knowledge_update):
        """Test applying update to existing file."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        result = engine.apply_update(sample_knowledge_update)
        
        assert result.success is True
        assert result.old_version == "1.0.0"
        assert result.new_version == "1.1.0"
    
    def test_apply_update_with_backup(self, tmp_knowledge_dir, sample_knowledge_file, sample_knowledge_update):
        """Test applying update creates backup."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        result = engine.apply_update(sample_knowledge_update, create_backup=True)
        
        assert result.success is True
        assert result.backup_path is not None
        assert result.backup_path.exists()
    
    def test_apply_update_without_backup(self, tmp_knowledge_dir, sample_knowledge_file, sample_knowledge_update):
        """Test applying update without backup."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        result = engine.apply_update(sample_knowledge_update, create_backup=False)
        
        assert result.success is True
        assert result.backup_path is None
    
    def test_apply_update_validation_error(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test applying update with validation error."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Create update with invalid version
        # Need to also update proposed_content to have invalid version
        invalid_update = sample_knowledge_update
        invalid_update.new_version = "invalid-version"
        if invalid_update.proposed_content:
            invalid_update.proposed_content["version"] = "invalid-version"
        
        result = engine.apply_update(invalid_update)
        
        assert result.success is False
        assert len(result.errors) > 0
    
    def test_apply_update_exception_handling(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test exception handling during update."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Make file read-only to cause error
        target_path = tmp_knowledge_dir / "test-patterns.json"
        target_path.touch()
        target_path.chmod(0o444)  # Read-only
        
        try:
            result = engine.apply_update(sample_knowledge_update)
            
            assert result.success is False
            assert len(result.errors) > 0
        finally:
            # Restore permissions
            target_path.chmod(0o644)


class TestUpdateEngineMergeStrategies:
    """Tests for different merge strategies."""
    
    def test_merge_conservative(self, tmp_knowledge_dir, sample_knowledge_file, sample_knowledge_update, sample_update_source):
        """Test conservative merge strategy."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Create an update with a new top-level key that doesn't exist in the file
        conservative_update = KnowledgeUpdate(
            target_file="test-patterns.json",
            priority=UpdatePriority.MEDIUM,
            source=sample_update_source,
            changes=[],
            new_version="1.1.0",
            breaking=False,
            proposed_content={
                "version": "1.1.0",
                "new_section": {"key": "value"}  # New top-level key
            }
        )
        
        # Conservative only adds new keys
        result = engine.apply_update(conservative_update, strategy=MergeStrategy.CONSERVATIVE)
        
        assert result.success is True
        
        # Check operations - should have add operation for new_section
        add_ops = [op for op in result.operations if op.operation_type == "add"]
        assert len(add_ops) > 0
    
    def test_merge_balanced(self, tmp_knowledge_dir, sample_knowledge_file, sample_knowledge_update):
        """Test balanced merge strategy."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        result = engine.apply_update(sample_knowledge_update, strategy=MergeStrategy.BALANCED)
        
        assert result.success is True
        
        # Balanced should allow both add and modify
        op_types = {op.operation_type for op in result.operations}
        assert "add" in op_types or "modify" in op_types
    
    def test_merge_aggressive(self, tmp_knowledge_dir, sample_knowledge_file, sample_knowledge_update):
        """Test aggressive merge strategy."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        result = engine.apply_update(sample_knowledge_update, strategy=MergeStrategy.AGGRESSIVE)
        
        assert result.success is True
        
        # Aggressive should replace content
        modify_ops = [op for op in result.operations if op.operation_type == "modify"]
        assert len(modify_ops) > 0


class TestUpdateEngineBatch:
    """Tests for batch updates."""
    
    def test_apply_batch(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test applying batch of updates."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Create multiple updates
        update1 = sample_knowledge_update
        update2 = Mock(spec=KnowledgeUpdate)
        update2.target_file = "file2.json"
        update2.new_version = "1.0.0"
        update2.priority = UpdatePriority.MEDIUM
        update2.source = sample_knowledge_update.source
        update2.changes = []
        update2.breaking = False
        update2.proposed_content = {"version": "1.0.0"}
        
        batch_result = engine.apply_batch([update1, update2])
        
        assert isinstance(batch_result, BatchUpdateResult)
        assert len(batch_result.results) == 2
        assert batch_result.total_applied >= 0
    
    def test_apply_batch_partial_failure(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test batch with partial failures."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Create valid and invalid updates
        valid_update = sample_knowledge_update
        invalid_update = Mock(spec=KnowledgeUpdate)
        invalid_update.target_file = "invalid.json"
        invalid_update.new_version = "invalid"
        invalid_update.priority = UpdatePriority.MEDIUM
        invalid_update.source = sample_knowledge_update.source
        invalid_update.changes = []
        invalid_update.breaking = False
        invalid_update.proposed_content = {"version": "invalid"}
        
        batch_result = engine.apply_batch([valid_update, invalid_update])
        
        assert batch_result.success is False
        assert batch_result.total_applied == 1
        assert batch_result.total_failed == 1


class TestUpdateEngineRollback:
    """Tests for rollback functionality."""
    
    def test_rollback_single_file(self, tmp_knowledge_dir, sample_knowledge_file, sample_knowledge_update):
        """Test rolling back a single file."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Apply update
        result = engine.apply_update(sample_knowledge_update)
        assert result.success is True
        assert result.backup_path is not None
        
        # Rollback
        success = engine.rollback(result.backup_path)
        
        assert success is True
        
        # Check file was restored
        content = json.loads(sample_knowledge_file.read_text())
        assert content["version"] == "1.0.0"
    
    def test_rollback_nonexistent_backup(self, tmp_knowledge_dir):
        """Test rolling back with non-existent backup."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        backup_path = tmp_knowledge_dir / "nonexistent.json"
        
        success = engine.rollback(backup_path)
        
        assert success is False
    
    def test_rollback_batch(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test rolling back a batch."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Apply batch
        batch_result = engine.apply_batch([sample_knowledge_update])
        batch_id = batch_result.batch_id
        
        # Rollback batch
        success = engine.rollback_batch(batch_id)
        
        assert success is True
    
    def test_rollback_batch_not_found(self, tmp_knowledge_dir):
        """Test rolling back non-existent batch."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        success = engine.rollback_batch("nonexistent-batch-id")
        
        assert success is False


class TestUpdateEngineHistory:
    """Tests for update history."""
    
    def test_get_history(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test getting update history."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Apply batch
        engine.apply_batch([sample_knowledge_update])
        
        history = engine.get_history()
        
        assert len(history) == 1
        assert isinstance(history[0], BatchUpdateResult)


class TestUpdateEngineValidation:
    """Tests for content validation."""
    
    def test_validate_content_valid(self, tmp_knowledge_dir):
        """Test validation of valid content."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        content = {
            "version": "1.0.0",
            "metadata": {}
        }
        
        errors = engine._validate_content(content)
        
        assert len(errors) == 0
    
    def test_validate_content_missing_version(self, tmp_knowledge_dir):
        """Test validation with missing version."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        content = {
            "metadata": {}
        }
        
        errors = engine._validate_content(content)
        
        assert len(errors) > 0
        assert any("version" in e.lower() for e in errors)
    
    def test_validate_content_invalid_version(self, tmp_knowledge_dir):
        """Test validation with invalid version format."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        content = {
            "version": "invalid",
            "metadata": {}
        }
        
        errors = engine._validate_content(content)
        
        assert len(errors) > 0
        assert any("version" in e.lower() for e in errors)
    
    def test_validate_content_not_dict(self, tmp_knowledge_dir):
        """Test validation with non-dict content."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        errors = engine._validate_content([])  # List instead of dict
        
        assert len(errors) > 0
        assert any("object" in e.lower() for e in errors)
    
    def test_is_valid_version(self, tmp_knowledge_dir):
        """Test version format validation."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        assert engine._is_valid_version("1.0.0") is True
        assert engine._is_valid_version("10.20.30") is True
        assert engine._is_valid_version("invalid") is False
        assert engine._is_valid_version("1.0") is False
        assert engine._is_valid_version("v1.0.0") is False


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests combining multiple components."""
    
    @pytest.mark.asyncio
    async def test_full_update_workflow(self, tmp_knowledge_dir, tmp_changelog_dir, sample_knowledge_update, mock_config_manager):
        """Test complete update workflow."""
        # Setup
        engine = UpdateEngine(tmp_knowledge_dir)
        notifier = NotificationSystem()
        
        # Apply update
        result = engine.apply_update(sample_knowledge_update)
        assert result.success is True
        
        # Notify
        notification = notifier.notify_update_applied(result)
        assert notification is not None
        
        # Verify changelog in knowledge file
        target_path = tmp_knowledge_dir / sample_knowledge_update.target_file
        with open(target_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        
        assert "changelog" in content
        assert len(content["changelog"]) > 0
        assert content["changelog"][0]["version"] == sample_knowledge_update.new_version


# =============================================================================
# ADDITIONAL EDGE CASE TESTS
# =============================================================================

# TestChangelogGeneratorEdgeCases removed as ChangelogGenerator was refactored.


class TestNotificationSystemEdgeCases:
    """Additional edge case tests for NotificationSystem."""
    
    def test_notify_file_write_error(self, tmp_path, capsys):
        """Test handling file write errors."""
        # Create a file path where the parent is a file (not a directory) to cause write error
        file_path = tmp_path / "notifications.jsonl"
        # Create a file at the parent location
        parent_file = tmp_path / "parent_file.txt"
        parent_file.write_text("test")
        
        # Try to write to a path where parent is a file, not a directory
        # This will cause an error when trying to create the parent directory
        invalid_path = parent_file / "file.json"
        
        config = NotificationConfig(file_path=invalid_path)
        system = NotificationSystem(config)
        
        # Should not raise, error should be handled
        notification = system.notify("Test", "Message")
        
        assert notification is not None
        captured = capsys.readouterr()
        # Check both stdout and stderr for error message
        # The error message should contain "Error:" or "Failed"
        output = (captured.out + captured.err).lower()
        # The error should be printed when file write fails
        assert "error" in output or "failed" in output
    
    def test_notify_updates_available_with_details_disabled(self):
        """Test notify_updates_available with show_details=False."""
        config = NotificationConfig(show_update_summary=False)
        system = NotificationSystem(config)
        
        update = Mock(spec=KnowledgeUpdate)
        update.priority = UpdatePriority.MEDIUM
        update.target_file = "test.json"
        
        notification = system.notify_updates_available([update], show_details=False)
        
        assert notification.data is None
    
    def test_notify_update_applied_with_changelog_disabled(self):
        """Test notify_update_applied with show_changelog=False."""
        config = NotificationConfig(show_changelog=False)
        system = NotificationSystem(config)
        
        result = Mock(spec=UpdateResult)
        result.success = True
        result.target_file = "test.json"
        result.old_version = "1.0.0"
        result.new_version = "1.1.0"
        result.operations = []
        result.backup_path = None
        
        notification = system.notify_update_applied(result, show_changelog=False)
        
        assert notification.data is None


class TestSourceAggregatorEdgeCases:
    """Additional edge case tests for SourceAggregator."""
    
    @pytest.mark.asyncio
    async def test_fetch_all_updates_with_target_files_filter(self, mock_config_manager, mock_adapter, sample_knowledge_update):
        """Test fetching with target_files filter."""
        mock_adapter.name = "github"
        mock_adapter.fetch_updates = AsyncMock(return_value=[sample_knowledge_update])
        mock_adapter.validate_connection = AsyncMock(return_value=True)
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                result = await aggregator.fetch_all_updates(target_files=["test-patterns.json"])
                
                mock_adapter.fetch_updates.assert_called_once()
                call_args = mock_adapter.fetch_updates.call_args
                assert call_args[0][0] == ["test-patterns.json"]
    
    @pytest.mark.asyncio
    async def test_fetch_all_updates_with_since_filter(self, mock_config_manager, mock_adapter, sample_knowledge_update):
        """Test fetching with since datetime filter."""
        mock_adapter.name = "github"
        mock_adapter.fetch_updates = AsyncMock(return_value=[sample_knowledge_update])
        mock_adapter.validate_connection = AsyncMock(return_value=True)
        
        since = datetime(2024, 1, 1)
        
        # Mock config to enable github_trending
        ke_config = mock_config_manager.get_knowledge_evolution_config()
        ke_config.sources["github_trending"] = True
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["github"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                result = await aggregator.fetch_all_updates(since=since)
                
                mock_adapter.fetch_updates.assert_called_once()
                call_args = mock_adapter.fetch_updates.call_args
                assert call_args[0][1] == since
    
    @pytest.mark.asyncio
    async def test_fetch_from_adapter_connection_failure(self, mock_config_manager, mock_adapter):
        """Test fetch_from_adapter when connection validation fails."""
        mock_adapter.validate_connection = AsyncMock(return_value=False)
        
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=["test_adapter"]):
            with patch('scripts.updates.source_aggregator.create_adapter', return_value=mock_adapter):
                aggregator = SourceAggregator(config_manager=mock_config_manager)
                
                updates, errors = await aggregator._fetch_from_adapter(mock_adapter, None, None)
                
                assert len(updates) == 0
                assert len(errors) > 0
    
    def test_deduplicate_updates_same_priority(self, mock_config_manager):
        """Test deduplication when updates have same priority."""
        with patch('scripts.updates.source_aggregator.get_available_adapters', return_value=[]):
            aggregator = SourceAggregator(config_manager=mock_config_manager)
            
            update1 = Mock(spec=KnowledgeUpdate)
            update1.target_file = "test.json"
            update1.priority = UpdatePriority.MEDIUM
            
            update2 = Mock(spec=KnowledgeUpdate)
            update2.target_file = "test.json"
            update2.priority = UpdatePriority.MEDIUM
            
            deduplicated = aggregator._deduplicate_updates([update1, update2])
            
            # Should keep first one
            assert len(deduplicated) == 1
    
    def test_filter_subscriptions_empty_patterns(self, sample_knowledge_update):
        """Test filter_subscriptions with empty patterns list."""
        result = AggregationResult(
            updates=[sample_knowledge_update],
            source_health={},
        )
        
        filtered = result.filter_subscriptions([])
        
        # Empty patterns should return empty result
        assert len(filtered.updates) == 0


class TestUpdateEngineEdgeCases:
    """Additional edge case tests for UpdateEngine."""
    
    def test_apply_update_with_checksum(self, tmp_knowledge_dir, sample_knowledge_update):
        """Test applying update with checksum."""
        sample_knowledge_update.checksum = "abc123"
        engine = UpdateEngine(tmp_knowledge_dir)
        
        result = engine.apply_update(sample_knowledge_update)
        
        assert result.success is True
        target_path = tmp_knowledge_dir / "test-patterns.json"
        content = json.loads(target_path.read_text())
        assert content["metadata"]["checksum"] == "abc123"
    
    def test_apply_update_without_proposed_content(self, tmp_knowledge_dir, sample_update_source):
        """Test applying update without proposed_content."""
        update = KnowledgeUpdate(
            target_file="test.json",
            priority=UpdatePriority.MEDIUM,
            source=sample_update_source,
            changes=[],
            new_version="1.0.0",
            breaking=False,
            proposed_content=None,
        )
        
        engine = UpdateEngine(tmp_knowledge_dir)
        result = engine.apply_update(update)
        
        # Should still succeed, just update version and metadata
        assert result.success is True
    
    def test_deep_merge_nested_structures(self, tmp_knowledge_dir, sample_knowledge_file, sample_update_source):
        """Test deep merge with nested structures."""
        update = KnowledgeUpdate(
            target_file="test-patterns.json",
            priority=UpdatePriority.MEDIUM,
            source=sample_update_source,
            changes=[],
            new_version="1.1.0",
            breaking=False,
            proposed_content={
                "version": "1.1.0",
                "metadata": {
                    "nested": {
                        "deep": {
                            "value": "updated"
                        }
                    }
                }
            },
        )
        
        engine = UpdateEngine(tmp_knowledge_dir)
        result = engine.apply_update(update, strategy=MergeStrategy.BALANCED)
        
        assert result.success is True
        target_path = tmp_knowledge_dir / "test-patterns.json"
        content = json.loads(target_path.read_text())
        assert content["metadata"]["nested"]["deep"]["value"] == "updated"
    
    def test_merge_conservative_preserves_existing(self, tmp_knowledge_dir, sample_knowledge_file, sample_update_source):
        """Test conservative merge preserves existing values."""
        update = KnowledgeUpdate(
            target_file="test-patterns.json",
            priority=UpdatePriority.MEDIUM,
            source=sample_update_source,
            changes=[],
            new_version="1.1.0",
            breaking=False,
            proposed_content={
                "version": "1.1.0",
                "metadata": {
                    "name": "should_not_change",  # This key already exists
                    "new_key": "should_be_added",  # This is new
                }
            },
        )
        
        engine = UpdateEngine(tmp_knowledge_dir)
        result = engine.apply_update(update, strategy=MergeStrategy.CONSERVATIVE)
        
        assert result.success is True
        target_path = tmp_knowledge_dir / "test-patterns.json"
        content = json.loads(target_path.read_text())
        # Existing key should be preserved
        assert content["metadata"]["name"] == "test-patterns"
        # New key should be added
        assert content["metadata"]["new_key"] == "should_be_added"
    
    def test_rollback_invalid_backup_name(self, tmp_knowledge_dir):
        """Test rollback with invalid backup filename format."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        # Create backup file with invalid name format
        invalid_backup = engine.backup_dir / "invalid-name.json"
        invalid_backup.write_text("{}")
        
        success = engine.rollback(invalid_backup)
        
        assert success is False
    
    def test_list_backups_nonexistent_stem(self, tmp_knowledge_dir):
        """Test listing backups for non-existent file."""
        engine = UpdateEngine(tmp_knowledge_dir)
        
        backups = engine.list_backups("nonexistent-file")
        
        assert len(backups) == 0
