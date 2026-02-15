"""
Official Documentation Adapter for Knowledge Evolution

This adapter fetches knowledge updates from official framework documentation
sources, tracking changes to best practices, API updates, and recommended
patterns.

Features:
    - Documentation version tracking
    - Change detection in official guides
    - Best practice extraction
    - API change monitoring

Note: This is a foundational implementation. Full documentation parsing
would require framework-specific handling or use of documentation APIs.

Author: Antigravity Agent Factory
Version: 1.0.0
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

try:
    import aiohttp
except ImportError:
    aiohttp = None

from .base_adapter import (
    BaseAdapter,
    AdapterConfig,
    KnowledgeUpdate,
    KnowledgeChange,
    UpdatePriority,
    TrustLevel,
    ChangeType,
)


@dataclass
class DocumentationSource:
    """A documentation source being tracked.

    Attributes:
        name: Framework name
        knowledge_file: Target knowledge file
        docs_url: Documentation URL
        version_url: URL to check for version
        trust_level: Trust level for this source
    """

    name: str
    knowledge_file: str
    docs_url: str
    version_url: Optional[str] = None
    trust_level: TrustLevel = TrustLevel.OFFICIAL


class DocsAdapter(BaseAdapter):
    """Adapter for fetching updates from official documentation.

    This adapter monitors official framework documentation for changes
    and extracts relevant patterns and best practices.

    Example:
        config = AdapterConfig(trust_level=TrustLevel.OFFICIAL)
        adapter = DocsAdapter(config)
        updates = await adapter.fetch_updates()
    """

    # Documentation sources to track
    DOCUMENTATION_SOURCES: List[DocumentationSource] = [
        DocumentationSource(
            name="FastAPI",
            knowledge_file="fastapi-patterns.json",
            docs_url="https://fastapi.tiangolo.com",
            version_url="https://pypi.org/pypi/fastapi/json",
        ),
        DocumentationSource(
            name="Next.js",
            knowledge_file="nextjs-patterns.json",
            docs_url="https://nextjs.org/docs",
            version_url="https://registry.npmjs.org/next",
        ),
        DocumentationSource(
            name="LangChain",
            knowledge_file="langchain-patterns.json",
            docs_url="https://python.langchain.com/docs",
            version_url="https://pypi.org/pypi/langchain/json",
        ),
        DocumentationSource(
            name="Spring Boot",
            knowledge_file="spring-patterns.json",
            docs_url="https://docs.spring.io/spring-boot/docs/current/reference/html/",
        ),
        DocumentationSource(
            name="React",
            knowledge_file="react-patterns.json",
            docs_url="https://react.dev",
            version_url="https://registry.npmjs.org/react",
        ),
    ]

    def __init__(self, config: AdapterConfig):
        """Initialize the documentation adapter.

        Args:
            config: Adapter configuration
        """
        super().__init__(config)
        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def name(self) -> str:
        """Adapter identifier."""
        return "official_docs"

    @property
    def description(self) -> str:
        """Human-readable description."""
        return "Fetches updates from official framework documentation"

    @property
    def supported_knowledge_files(self) -> List[str]:
        """Knowledge files this adapter can update."""
        return list(set(src.knowledge_file for src in self.DOCUMENTATION_SOURCES))

    async def _get_session(self) -> "aiohttp.ClientSession":
        """Get or create the HTTP session."""
        if aiohttp is None:
            raise ImportError("aiohttp required for DocsAdapter")

        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"User-Agent": "Antigravity-Agent-Factory/1.0"},
                timeout=aiohttp.ClientTimeout(total=self.config.timeout_seconds),
            )

        return self._session

    async def _close_session(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def validate_connection(self) -> bool:
        """Validate documentation sources are reachable."""
        try:
            session = await self._get_session()
            async with session.head("https://fastapi.tiangolo.com") as resp:
                return resp.status < 400
        except Exception:
            return False

    async def fetch_updates(
        self, target_files: Optional[List[str]] = None, since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Fetch updates from documentation sources.

        Args:
            target_files: Optional filter by knowledge files
            since: Optional date filter

        Returns:
            List of knowledge updates
        """
        updates: List[KnowledgeUpdate] = []

        sources = self.DOCUMENTATION_SOURCES
        if target_files:
            sources = [s for s in sources if s.knowledge_file in target_files]

        for source in sources:
            source_updates = await self._check_source(source, since)
            updates.extend(source_updates)

        await self._close_session()
        return updates

    async def _check_source(
        self, source: DocumentationSource, since: Optional[datetime]
    ) -> List[KnowledgeUpdate]:
        """Check a documentation source for updates.

        This is a simplified implementation. A full version would:
        1. Fetch documentation content
        2. Parse and extract patterns
        3. Compare against cached version
        4. Generate detailed changes

        Args:
            source: Documentation source to check
            since: Date filter

        Returns:
            List of updates from this source
        """
        updates: List[KnowledgeUpdate] = []

        # Check if we can get version info
        version = await self._get_framework_version(source)

        if version:
            # Create an update indicating new documentation available
            changes = [
                KnowledgeChange(
                    change_type=ChangeType.CHANGED,
                    path=f"frameworks.{source.name}.version",
                    description=f"{source.name} documentation for version {version}",
                    new_value=version,
                    impact="low",
                )
            ]

            update = KnowledgeUpdate(
                target_file=source.knowledge_file,
                priority=UpdatePriority.LOW,  # Docs updates are low priority
                source=self.create_source(
                    identifier=source.name,
                    version=version,
                    url=source.docs_url,
                ),
                changes=changes,
                new_version=self._suggest_version(version),
                breaking=False,
                rationale=f"Documentation update for {source.name} {version}",
                axiom_alignment={
                    "A1": "Verified from official documentation",
                    "A10": "Learning from authoritative source",
                },
            )
            updates.append(update)

        return updates

    async def _get_framework_version(
        self, source: DocumentationSource
    ) -> Optional[str]:
        """Get the current version of a framework.

        Args:
            source: Documentation source

        Returns:
            Version string or None
        """
        if not source.version_url:
            return None

        session = await self._get_session()

        try:
            async with session.get(source.version_url) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    # PyPI format
                    if "info" in data and "version" in data["info"]:
                        return data["info"]["version"]

                    # NPM format
                    if "dist-tags" in data and "latest" in data["dist-tags"]:
                        return data["dist-tags"]["latest"]
        except Exception:
            pass

        return None

    def _suggest_version(self, framework_version: str) -> str:
        """Suggest knowledge file version based on framework version."""
        parts = framework_version.split(".")
        if len(parts) >= 2:
            return f"{parts[0]}.{parts[1]}.0"
        return "1.0.0"
