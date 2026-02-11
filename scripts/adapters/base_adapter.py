"""
Base Adapter Interface for Knowledge Evolution

This module defines the abstract base class and data structures that all
knowledge source adapters must implement. The adapter pattern allows the
system to fetch knowledge updates from various sources (GitHub, PyPI, npm,
official docs, community sources, user feedback) in a consistent way.

Design Patterns:
    - Strategy Pattern: Each adapter implements the same interface
    - Factory Pattern: Adapters are created through the registry
    - Template Method: Common workflow with customizable steps

Axiom Alignment:
    - A1 (Verifiability): All updates include checksums and source tracking
    - A3 (Transparency): Sources and reasoning are documented
    - A10 (Learning): System evolves from multiple knowledge sources

Author: Antigravity Agent FactoryVersion: 1.0.0
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
import json


class UpdatePriority(Enum):
    """Priority levels for knowledge updates.
    
    Determines order of processing and notification urgency.
    """
    CRITICAL = 1    # Security fixes, breaking changes
    HIGH = 2        # Important new patterns, deprecations
    MEDIUM = 3      # New features, improvements
    LOW = 4         # Minor updates, cosmetic changes
    INFO = 5        # Informational only, no action needed


class TrustLevel(Enum):
    """Trust levels for knowledge sources.
    
    Affects merge strategy and user confirmation requirements.
    """
    OFFICIAL = 1      # Official framework/library documentation
    VERIFIED = 2      # Verified community contributors
    COMMUNITY = 3     # General community sources
    EXPERIMENTAL = 4  # Experimental or unverified sources


class ChangeType(Enum):
    """Types of changes to knowledge content."""
    ADDED = "added"
    CHANGED = "changed"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
    FIXED = "fixed"
    SECURITY = "security"


@dataclass
class AdapterConfig:
    """Configuration for a knowledge source adapter.
    
    Attributes:
        enabled: Whether this adapter is active
        api_key: Optional API key for authenticated access
        base_url: Base URL for the source API
        rate_limit_rpm: Requests per minute limit
        timeout_seconds: Request timeout in seconds
        cache_ttl_hours: How long to cache responses
        trust_level: Default trust level for this source
        custom_settings: Additional adapter-specific settings
    """
    enabled: bool = True
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    rate_limit_rpm: int = 60
    timeout_seconds: int = 30
    cache_ttl_hours: int = 24
    trust_level: TrustLevel = TrustLevel.COMMUNITY
    custom_settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UpdateSource:
    """Represents the source of a knowledge update.
    
    Provides full traceability for where knowledge came from,
    supporting Axiom A3 (Transparency).
    
    Attributes:
        adapter_type: Which adapter produced this (github, pypi, etc.)
        identifier: Unique identifier within the source (repo URL, package name)
        version: Version of the source when fetched
        url: Direct link to the source
        fetched_at: When this source was queried
        trust_level: Trust level of this specific source
        raw_data: Original data from the source (for debugging)
    """
    adapter_type: str
    identifier: str
    version: Optional[str] = None
    url: Optional[str] = None
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    trust_level: TrustLevel = TrustLevel.COMMUNITY
    raw_data: Optional[Dict[str, Any]] = None


@dataclass
class KnowledgeChange:
    """Represents a single change to knowledge content.
    
    Attributes:
        change_type: Type of change (added, changed, etc.)
        path: JSON path to the changed element
        description: Human-readable description
        old_value: Previous value (for changed/removed)
        new_value: New value (for added/changed)
        impact: Impact level (low, medium, high)
        related_blueprints: Blueprints affected by this change
        related_skills: Skills affected by this change
    """
    change_type: ChangeType
    path: str
    description: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    impact: str = "medium"
    related_blueprints: List[str] = field(default_factory=list)
    related_skills: List[str] = field(default_factory=list)


@dataclass
class KnowledgeUpdate:
    """Represents a proposed update to a knowledge file.
    
    This is the primary output of adapters - a structured proposal
    for updating knowledge that can be reviewed, approved, and merged.
    
    Attributes:
        target_file: Knowledge file to update (e.g., "fastapi-patterns.json")
        priority: Priority level for this update
        source: Source information for traceability
        changes: List of specific changes proposed
        new_version: Proposed new version number
        breaking: Whether this contains breaking changes
        requires_confirmation: Whether user must confirm
        merge_strategy: Suggested merge strategy
        checksum: SHA-256 of the proposed content
        proposed_content: Full proposed content (optional)
        rationale: Why this update is recommended
        axiom_alignment: Which axioms this update supports
    """
    target_file: str
    priority: UpdatePriority
    source: UpdateSource
    changes: List[KnowledgeChange]
    new_version: str
    breaking: bool = False
    requires_confirmation: bool = True
    merge_strategy: str = "balanced"
    checksum: Optional[str] = None
    proposed_content: Optional[Dict[str, Any]] = None
    rationale: str = ""
    axiom_alignment: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate checksum if content provided."""
        if self.proposed_content and not self.checksum:
            content_str = json.dumps(self.proposed_content, sort_keys=True)
            self.checksum = hashlib.sha256(content_str.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.
        
        Returns:
            Dictionary representation of the update
        """
        return {
            "target_file": self.target_file,
            "priority": self.priority.name,
            "source": {
                "adapter_type": self.source.adapter_type,
                "identifier": self.source.identifier,
                "version": self.source.version,
                "url": self.source.url,
                "fetched_at": self.source.fetched_at.isoformat(),
                "trust_level": self.source.trust_level.name,
            },
            "changes": [
                {
                    "type": c.change_type.value,
                    "path": c.path,
                    "description": c.description,
                    "impact": c.impact,
                }
                for c in self.changes
            ],
            "new_version": self.new_version,
            "breaking": self.breaking,
            "requires_confirmation": self.requires_confirmation,
            "checksum": self.checksum,
            "rationale": self.rationale,
            "axiom_alignment": self.axiom_alignment,
        }


class BaseAdapter(ABC):
    """Abstract base class for all knowledge source adapters.
    
    Adapters are responsible for:
    1. Connecting to external knowledge sources
    2. Fetching relevant updates
    3. Transforming raw data into KnowledgeUpdate objects
    4. Handling rate limiting and caching
    5. Providing source attribution
    
    Example:
        class GitHubAdapter(BaseAdapter):
            async def fetch_updates(self) -> List[KnowledgeUpdate]:
                # Fetch trending repos, analyze patterns
                ...
    """
    
    def __init__(self, config: AdapterConfig):
        """Initialize the adapter with configuration.
        
        Args:
            config: Adapter configuration including credentials
        """
        self.config = config
        self._cache: Dict[str, Any] = {}
        self._last_fetch: Optional[datetime] = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of this adapter (e.g., 'github', 'pypi').
        
        Returns:
            Adapter identifier string
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this adapter does.
        
        Returns:
            Description string
        """
        pass
    
    @property
    def supported_knowledge_files(self) -> List[str]:
        """List of knowledge files this adapter can update.
        
        Override this to restrict which files an adapter can modify.
        Default is all files (empty list means no restriction).
        
        Returns:
            List of knowledge file names, or empty for all
        """
        return []
    
    @abstractmethod
    async def fetch_updates(
        self,
        target_files: Optional[List[str]] = None,
        since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Fetch available updates from this source.
        
        This is the main method adapters must implement. It should:
        1. Query the external source for new/updated content
        2. Compare against current knowledge
        3. Generate KnowledgeUpdate objects for changes
        
        Args:
            target_files: Optional list of specific files to check
            since: Optional datetime to only fetch updates after
            
        Returns:
            List of proposed knowledge updates
        """
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate that the adapter can connect to its source.
        
        Used for health checks and configuration validation.
        
        Returns:
            True if connection is valid, False otherwise
        """
        pass
    
    async def get_source_version(self) -> Optional[str]:
        """Get the current version/timestamp of the source.
        
        Optional method for sources that have versioning.
        
        Returns:
            Version string or None if not applicable
        """
        return None
    
    def create_source(
        self,
        identifier: str,
        version: Optional[str] = None,
        url: Optional[str] = None,
        raw_data: Optional[Dict[str, Any]] = None
    ) -> UpdateSource:
        """Helper to create an UpdateSource with this adapter's info.
        
        Args:
            identifier: Source identifier (repo URL, package name)
            version: Source version if applicable
            url: Direct link to source
            raw_data: Original data for debugging
            
        Returns:
            UpdateSource object with adapter info filled in
        """
        return UpdateSource(
            adapter_type=self.name,
            identifier=identifier,
            version=version,
            url=url,
            trust_level=self.config.trust_level,
            raw_data=raw_data,
        )
    
    def _should_refresh_cache(self, cache_key: str) -> bool:
        """Check if cached data should be refreshed.
        
        Args:
            cache_key: Key for the cached data
            
        Returns:
            True if cache should be refreshed
        """
        if cache_key not in self._cache:
            return True
        
        cached = self._cache[cache_key]
        if "timestamp" not in cached:
            return True
        
        cache_age = datetime.now(timezone.utc) - cached["timestamp"]
        cache_ttl = self.config.cache_ttl_hours * 3600
        
        return cache_age.total_seconds() > cache_ttl
    
    def _get_cached(self, cache_key: str) -> Optional[Any]:
        """Get data from cache if valid.
        
        Args:
            cache_key: Key for the cached data
            
        Returns:
            Cached data or None if not available/expired
        """
        if self._should_refresh_cache(cache_key):
            return None
        return self._cache[cache_key].get("data")
    
    def _set_cached(self, cache_key: str, data: Any) -> None:
        """Store data in cache.
        
        Args:
            cache_key: Key for the cached data
            data: Data to cache
        """
        self._cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now(timezone.utc),
        }
    
    def __repr__(self) -> str:
        """String representation of the adapter."""
        status = "enabled" if self.config.enabled else "disabled"
        return f"<{self.__class__.__name__} ({status})>"
