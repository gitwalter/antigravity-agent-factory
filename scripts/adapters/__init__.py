"""
Knowledge Evolution - Source Adapters

This package contains adapters for fetching knowledge updates from various sources.
Each adapter implements the BaseAdapter interface and can be enabled/disabled
through the settings.json configuration.

Available Adapters:
    - GitHubAdapter: Trending repos, releases, and documentation from GitHub
    - PyPIAdapter: Python package trends and best practices
    - NPMAdapter: JavaScript/TypeScript package trends
    - DocsAdapter: Official framework documentation
    - CommunityAdapter: Community-curated sources (Awesome lists, blogs)
    - FeedbackAdapter: User feedback from generated projects

Usage:
    from scripts.adapters import GitHubAdapter, create_adapter
    
    # Create specific adapter
    adapter = GitHubAdapter(config)
    updates = await adapter.fetch_updates()
    
    # Create adapter by name
    adapter = create_adapter("github", config)

Author: Antigravity Agent Factory
Version: 1.0.0
"""

from typing import Dict, Type, Optional
from .base_adapter import BaseAdapter, AdapterConfig, KnowledgeUpdate, UpdateSource

# Adapter registry - populated by imports
_ADAPTER_REGISTRY: Dict[str, Type[BaseAdapter]] = {}


def register_adapter(name: str, adapter_class: Type[BaseAdapter]) -> None:
    """Register an adapter class in the registry.
    
    Args:
        name: Unique identifier for the adapter (e.g., "github", "pypi")
        adapter_class: Adapter class that implements BaseAdapter
    """
    _ADAPTER_REGISTRY[name] = adapter_class


def create_adapter(name: str, config: AdapterConfig) -> Optional[BaseAdapter]:
    """Create an adapter instance by name.
    
    Args:
        name: Adapter name from the registry
        config: Configuration for the adapter
        
    Returns:
        Adapter instance or None if not found
        
    Raises:
        ValueError: If adapter name is not registered
    """
    if name not in _ADAPTER_REGISTRY:
        raise ValueError(f"Unknown adapter: {name}. Available: {list(_ADAPTER_REGISTRY.keys())}")
    return _ADAPTER_REGISTRY[name]


def get_available_adapters() -> Dict[str, Type[BaseAdapter]]:
    """Get all registered adapters.
    
    Returns:
        Dictionary mapping adapter names to their classes
    """
    return _ADAPTER_REGISTRY.copy()


# Import and register adapters (lazy imports to avoid circular dependencies)
def _register_all_adapters() -> None:
    """Register all available adapters. Called on first use."""
    # These imports are deferred to allow the module to load without all adapters
    try:
        from .github_adapter import GitHubAdapter
        register_adapter("github", GitHubAdapter)
    except ImportError:
        pass
    
    try:
        from .pypi_adapter import PyPIAdapter
        register_adapter("pypi", PyPIAdapter)
    except ImportError:
        pass
    
    try:
        from .npm_adapter import NPMAdapter
        register_adapter("npm", NPMAdapter)
    except ImportError:
        pass
    
    try:
        from .docs_adapter import DocsAdapter
        register_adapter("official_docs", DocsAdapter)
    except ImportError:
        pass
    
    try:
        from .community_adapter import CommunityAdapter
        register_adapter("community", CommunityAdapter)
    except ImportError:
        pass
    
    try:
        from .feedback_adapter import FeedbackAdapter
        register_adapter("user_feedback", FeedbackAdapter)
    except ImportError:
        pass


# Register adapters on module load
_register_all_adapters()

__all__ = [
    "BaseAdapter",
    "AdapterConfig", 
    "KnowledgeUpdate",
    "UpdateSource",
    "register_adapter",
    "create_adapter",
    "get_available_adapters",
]
