"""
Source Aggregator for Knowledge Evolution

This module aggregates updates from multiple source adapters, deduplicates
them, prioritizes by importance, and provides a unified interface for
the update engine.

Features:
    - Parallel fetching from multiple adapters
    - Intelligent deduplication
    - Priority-based sorting
    - Subscription filtering
    - Source health monitoring

Design Patterns:
    - Facade: Unified interface to multiple adapters
    - Strategy: Different aggregation strategies
    - Observer: Source health monitoring

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pathlib import Path
import fnmatch

from .adapters import create_adapter, get_available_adapters
from .adapters.base_adapter import (
    BaseAdapter,
    AdapterConfig,
    KnowledgeUpdate,
    UpdatePriority,
    TrustLevel,
)
from .config_manager import ConfigManager


@dataclass
class SourceHealth:
    """Health status of a source adapter.

    Attributes:
        name: Adapter name
        available: Whether the source is reachable
        last_check: Last successful check time
        last_error: Last error message if any
        success_rate: Historical success rate
    """

    name: str
    available: bool = False
    last_check: Optional[datetime] = None
    last_error: Optional[str] = None
    success_rate: float = 1.0


@dataclass
class AggregationResult:
    """Result of aggregating updates from all sources.

    Attributes:
        updates: List of deduplicated, prioritized updates
        source_health: Health status of each source
        total_fetched: Total updates before deduplication
        fetch_time_seconds: Time taken to fetch all updates
        errors: Any errors encountered
    """

    updates: List[KnowledgeUpdate]
    source_health: Dict[str, SourceHealth]
    total_fetched: int = 0
    fetch_time_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)

    @property
    def by_priority(self) -> Dict[UpdatePriority, List[KnowledgeUpdate]]:
        """Group updates by priority."""
        # Initialize result with all UpdatePriority values as keys
        result: Dict[UpdatePriority, List[KnowledgeUpdate]] = {}
        # Ensure we have all UpdatePriority keys initialized
        for p in UpdatePriority:
            result[p] = []

        # Group updates by their priority
        if not hasattr(self, "updates") or self.updates is None:
            return result

        for update in self.updates:
            if not hasattr(update, "priority") or update.priority is None:
                continue

            priority = update.priority

            # Direct enum comparison - this should work for UpdatePriority enums
            if priority in result:
                result[priority].append(update)
            else:
                # Fallback: try to match by value or name
                try:
                    priority_value = getattr(priority, "value", None)
                    priority_name = getattr(priority, "name", None)

                    for p in UpdatePriority:
                        if priority_value is not None and p.value == priority_value:
                            result[p].append(update)
                            break
                        elif priority_name is not None and p.name == priority_name:
                            result[p].append(update)
                            break
                except (AttributeError, TypeError):
                    pass

        # Always return a dict with all UpdatePriority keys, even if empty
        return result

    @property
    def by_file(self) -> Dict[str, List[KnowledgeUpdate]]:
        """Group updates by target file."""
        result: Dict[str, List[KnowledgeUpdate]] = {}
        for update in self.updates:
            if update.target_file not in result:
                result[update.target_file] = []
            result[update.target_file].append(update)
        return result

    def filter_subscriptions(self, patterns: List[str]) -> "AggregationResult":
        """Filter updates by subscription patterns.

        Args:
            patterns: Glob patterns for knowledge files to include

        Returns:
            New AggregationResult with filtered updates
        """
        if not patterns:
            # Empty patterns means no matches
            return AggregationResult(
                updates=[],
                source_health=self.source_health,
                total_fetched=self.total_fetched,
                fetch_time_seconds=self.fetch_time_seconds,
                errors=self.errors,
            )

        if patterns == ["*"]:
            return self

        filtered = []
        for update in self.updates:
            for pattern in patterns:
                if fnmatch.fnmatch(update.target_file, pattern):
                    filtered.append(update)
                    break

        return AggregationResult(
            updates=filtered,
            source_health=self.source_health,
            total_fetched=self.total_fetched,
            fetch_time_seconds=self.fetch_time_seconds,
            errors=self.errors,
        )


class SourceAggregator:
    """Aggregates knowledge updates from multiple source adapters.

    This class provides a unified interface for fetching and processing
    updates from all configured source adapters. It handles:
    - Parallel fetching for performance
    - Deduplication of updates
    - Priority-based sorting
    - Subscription filtering
    - Source health monitoring

    Example:
        config = ConfigManager.get_instance()
        aggregator = SourceAggregator(config)
        result = await aggregator.fetch_all_updates()
        for update in result.updates:
            print(f"{update.target_file}: {update.priority}")
    """

    def __init__(
        self,
        config_manager: Optional[ConfigManager] = None,
        factory_root: Optional[Path] = None,
    ):
        """Initialize the source aggregator.

        Args:
            config_manager: Configuration manager instance
            factory_root: Factory root directory
        """
        self._config = config_manager or ConfigManager.get_instance(factory_root)
        self._adapters: Dict[str, BaseAdapter] = {}
        self._source_health: Dict[str, SourceHealth] = {}
        self._initialize_adapters()

    def _initialize_adapters(self) -> None:
        """Initialize enabled source adapters based on configuration."""
        ke_config = self._config.get_knowledge_evolution_config()
        sources = ke_config.sources

        # Map source config names to adapter names
        source_to_adapter = {
            "github_trending": "github",
            "package_registries": ["pypi", "npm"],
            "official_docs": "official_docs",
            "community_curated": "community",
            "user_feedback": "user_feedback",
        }

        available_adapters = get_available_adapters()

        for source_name, enabled in sources.items():
            if not enabled:
                continue

            adapter_names = source_to_adapter.get(source_name, source_name)
            if isinstance(adapter_names, str):
                adapter_names = [adapter_names]

            for adapter_name in adapter_names:
                if adapter_name in available_adapters:
                    try:
                        adapter_config = self._create_adapter_config(adapter_name)
                        adapter = create_adapter(adapter_name, adapter_config)
                        if adapter:
                            self._adapters[adapter_name] = adapter
                            self._source_health[adapter_name] = SourceHealth(
                                name=adapter_name
                            )
                    except Exception as e:
                        print(f"Failed to initialize adapter {adapter_name}: {e}")

    def _create_adapter_config(self, adapter_name: str) -> AdapterConfig:
        """Create configuration for an adapter.

        Args:
            adapter_name: Name of the adapter

        Returns:
            AdapterConfig with appropriate settings
        """
        ke_config = self._config.get_knowledge_evolution_config()

        # Get API key if needed
        api_key = None
        if adapter_name == "github":
            api_key = self._config.get_credential("github_token")
        elif adapter_name == "npm":
            api_key = self._config.get_credential("npm_token")

        # Determine trust level based on adapter
        trust_level = TrustLevel.COMMUNITY
        if adapter_name in ["github", "pypi", "npm"]:
            trust_level = TrustLevel.OFFICIAL

        return AdapterConfig(
            enabled=True,
            api_key=api_key,
            trust_level=trust_level,
            cache_ttl_hours=24,
        )

    async def fetch_all_updates(
        self, target_files: Optional[List[str]] = None, since: Optional[datetime] = None
    ) -> AggregationResult:
        """Fetch updates from all enabled adapters.

        Args:
            target_files: Optional list of specific files to check
            since: Optional datetime to only fetch updates after

        Returns:
            AggregationResult with all updates and metadata
        """
        start_time = datetime.now(timezone.utc)
        all_updates: List[KnowledgeUpdate] = []
        errors: List[str] = []

        # Fetch from all adapters in parallel
        tasks = []
        adapter_names = []

        for name, adapter in self._adapters.items():
            task = self._fetch_from_adapter(adapter, target_files, since)
            tasks.append(task)
            adapter_names.append(name)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for name, result in zip(adapter_names, results):
            if isinstance(result, Exception):
                errors.append(f"{name}: {str(result)}")
                self._source_health[name].available = False
                self._source_health[name].last_error = str(result)
            else:
                updates, adapter_errors = result
                all_updates.extend(updates)
                errors.extend(adapter_errors)
                self._source_health[name].available = True
                self._source_health[name].last_check = datetime.now(timezone.utc)
                self._source_health[name].last_error = None

        # Deduplicate updates
        total_fetched = len(all_updates)
        deduplicated = self._deduplicate_updates(all_updates)

        # Sort by priority
        deduplicated.sort(key=lambda u: u.priority.value)

        # Calculate fetch time
        fetch_time = (datetime.now(timezone.utc) - start_time).total_seconds()

        return AggregationResult(
            updates=deduplicated,
            source_health=self._source_health.copy(),
            total_fetched=total_fetched,
            fetch_time_seconds=fetch_time,
            errors=errors,
        )

    async def _fetch_from_adapter(
        self,
        adapter: BaseAdapter,
        target_files: Optional[List[str]],
        since: Optional[datetime],
    ) -> tuple[List[KnowledgeUpdate], List[str]]:
        """Fetch updates from a single adapter.

        Args:
            adapter: The adapter to fetch from
            target_files: Optional target file filter
            since: Optional date filter

        Returns:
            Tuple of (updates, errors)
        """
        errors: List[str] = []
        updates: List[KnowledgeUpdate] = []

        try:
            # Validate connection first
            if not await adapter.validate_connection():
                errors.append(f"{adapter.name}: Connection validation failed")
                return updates, errors

            # Fetch updates
            updates = await adapter.fetch_updates(target_files, since)

        except Exception as e:
            errors.append(f"{adapter.name}: {str(e)}")

        return updates, errors

    def _deduplicate_updates(
        self, updates: List[KnowledgeUpdate]
    ) -> List[KnowledgeUpdate]:
        """Deduplicate updates, keeping highest priority for each file.

        Args:
            updates: List of updates to deduplicate

        Returns:
            Deduplicated list
        """
        # Group by target file
        by_file: Dict[str, List[KnowledgeUpdate]] = {}
        for update in updates:
            if update.target_file not in by_file:
                by_file[update.target_file] = []
            by_file[update.target_file].append(update)

        # Keep highest priority for each file (lowest priority value)
        deduplicated: List[KnowledgeUpdate] = []
        for file_updates in by_file.values():
            # Sort by priority (lower value = higher priority)
            file_updates.sort(key=lambda u: u.priority.value)
            # Keep the highest priority update
            deduplicated.append(file_updates[0])

        return deduplicated

    async def check_source_health(self) -> Dict[str, SourceHealth]:
        """Check health of all source adapters.

        Returns:
            Dictionary of source health statuses
        """
        for name, adapter in self._adapters.items():
            try:
                available = await adapter.validate_connection()
                self._source_health[name].available = available
                self._source_health[name].last_check = datetime.now(timezone.utc)
                if not available:
                    self._source_health[
                        name
                    ].last_error = "Connection validation failed"
            except Exception as e:
                self._source_health[name].available = False
                self._source_health[name].last_error = str(e)

        return self._source_health.copy()

    def get_enabled_adapters(self) -> List[str]:
        """Get list of enabled adapter names.

        Returns:
            List of adapter names
        """
        return list(self._adapters.keys())

    def get_adapter(self, name: str) -> Optional[BaseAdapter]:
        """Get a specific adapter by name.

        Args:
            name: Adapter name

        Returns:
            Adapter instance or None
        """
        return self._adapters.get(name)
