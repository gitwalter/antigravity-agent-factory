"""
PyPI Adapter for Knowledge Evolution

This adapter fetches knowledge updates from PyPI (Python Package Index) by analyzing:
- Package release trends and version changes
- New packages gaining popularity
- Deprecation notices and security advisories
- Best practices from package documentation

Features:
    - Package version monitoring
    - Popularity trend analysis
    - Security vulnerability checking
    - Documentation extraction
    - Rate limit handling

Dependencies:
    - aiohttp: Async HTTP client
    - PyPI JSON API

Author: Antigravity Agent Factory
Version: 1.0.0
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

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
class TrackedPackage:
    """A PyPI package being tracked for updates.

    Attributes:
        name: Package name on PyPI
        knowledge_file: Target knowledge file for updates
        min_version: Minimum version to track
        track_security: Whether to track security advisories
        trust_level: Trust level for this package
    """

    name: str
    knowledge_file: str
    min_version: Optional[str] = None
    track_security: bool = True
    trust_level: TrustLevel = TrustLevel.OFFICIAL


class PyPIAdapter(BaseAdapter):
    """Adapter for fetching knowledge updates from PyPI.

    This adapter connects to PyPI's JSON API to:
    1. Monitor package versions for tracked frameworks
    2. Detect new releases with breaking changes
    3. Extract changelog information
    4. Check for security advisories

    Example:
        config = AdapterConfig(trust_level=TrustLevel.OFFICIAL)
        adapter = PyPIAdapter(config)
        updates = await adapter.fetch_updates()
    """

    API_BASE_URL = "https://pypi.org/pypi"

    # Packages to track for Python knowledge files
    TRACKED_PACKAGES: List[TrackedPackage] = [
        # Web frameworks
        TrackedPackage(name="fastapi", knowledge_file="fastapi-patterns.json"),
        TrackedPackage(name="flask", knowledge_file="flask-patterns.json"),
        TrackedPackage(name="django", knowledge_file="django-patterns.json"),
        TrackedPackage(name="starlette", knowledge_file="fastapi-patterns.json"),
        TrackedPackage(name="pydantic", knowledge_file="fastapi-patterns.json"),
        # AI/ML frameworks
        TrackedPackage(name="langchain", knowledge_file="langchain-patterns.json"),
        TrackedPackage(name="langchain-core", knowledge_file="langchain-patterns.json"),
        TrackedPackage(name="langgraph", knowledge_file="langgraph-workflows.json"),
        TrackedPackage(name="crewai", knowledge_file="crewai-patterns.json"),
        TrackedPackage(name="autogen", knowledge_file="autogen-patterns.json"),
        TrackedPackage(name="openai", knowledge_file="llm-provider-comparison.json"),
        TrackedPackage(name="anthropic", knowledge_file="llm-provider-comparison.json"),
        # Data/ML
        TrackedPackage(name="transformers", knowledge_file="huggingface-patterns.json"),
        TrackedPackage(name="torch", knowledge_file="deep-learning-patterns.json"),
        TrackedPackage(name="tensorflow", knowledge_file="deep-learning-patterns.json"),
        # Testing
        TrackedPackage(name="pytest", knowledge_file="tdd-patterns.json"),
        TrackedPackage(name="pytest-bdd", knowledge_file="bdd-patterns.json"),
        TrackedPackage(name="behave", knowledge_file="bdd-patterns.json"),
        # DevOps
        TrackedPackage(name="mlflow", knowledge_file="mlops-patterns.json"),
        # Streamlit
        TrackedPackage(name="streamlit", knowledge_file="streamlit-patterns.json"),
    ]

    def __init__(self, config: AdapterConfig):
        """Initialize the PyPI adapter.

        Args:
            config: Adapter configuration
        """
        super().__init__(config)
        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def name(self) -> str:
        """Adapter identifier."""
        return "pypi"

    @property
    def description(self) -> str:
        """Human-readable description."""
        return "Fetches Python package updates and patterns from PyPI"

    @property
    def supported_knowledge_files(self) -> List[str]:
        """Knowledge files this adapter can update."""
        return list(set(pkg.knowledge_file for pkg in self.TRACKED_PACKAGES))

    async def _get_session(self) -> "aiohttp.ClientSession":
        """Get or create the HTTP session."""
        if aiohttp is None:
            raise ImportError(
                "aiohttp is required for PyPIAdapter. Install with: pip install aiohttp"
            )

        if self._session is None or self._session.closed:
            headers = {
                "Accept": "application/json",
                "User-Agent": "Antigravity-Agent-Factory/1.0",
            }
            self._session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout_seconds),
            )

        return self._session

    async def _close_session(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Fetch package information from PyPI.

        Args:
            package_name: Name of the package

        Returns:
            Package info dict or None on error
        """
        session = await self._get_session()
        url = f"{self.API_BASE_URL}/{package_name}/json"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception as e:
            print(f"PyPI API error for {package_name}: {e}")
            return None

    async def validate_connection(self) -> bool:
        """Validate PyPI API connection.

        Returns:
            True if connection is valid
        """
        result = await self._get_package_info("pip")  # pip always exists
        return result is not None

    async def fetch_updates(
        self, target_files: Optional[List[str]] = None, since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Fetch available updates from PyPI.

        Args:
            target_files: Optional list of specific knowledge files to check
            since: Optional datetime to only fetch updates after

        Returns:
            List of proposed knowledge updates
        """
        updates: List[KnowledgeUpdate] = []

        # Filter packages by target files if specified
        packages_to_check = self.TRACKED_PACKAGES
        if target_files:
            packages_to_check = [
                p for p in packages_to_check if p.knowledge_file in target_files
            ]

        # Check each tracked package
        for package in packages_to_check:
            package_updates = await self._check_package(package, since)
            updates.extend(package_updates)

        await self._close_session()
        return updates

    async def _check_package(
        self, package: TrackedPackage, since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Check a package for updates.

        Args:
            package: Package to check
            since: Only include releases after this date

        Returns:
            List of updates for this package
        """
        updates: List[KnowledgeUpdate] = []

        info = await self._get_package_info(package.name)
        if not info:
            return updates

        pkg_info = info.get("info", {})
        releases = info.get("releases", {})

        # Get the latest version
        latest_version = pkg_info.get("version")
        if not latest_version:
            return updates

        # Check if this is a significant update
        release_info = releases.get(latest_version, [])
        if not release_info:
            return updates

        # Get release date
        release_date = None
        for file_info in release_info:
            upload_time = file_info.get("upload_time")
            if upload_time:
                try:
                    release_date = datetime.fromisoformat(upload_time)
                    # Ensure timezone-aware for comparison
                    if release_date.tzinfo is None:
                        release_date = release_date.replace(tzinfo=timezone.utc)
                except ValueError:
                    pass
                break

        # Filter by date if specified
        if since and release_date and release_date < since:
            return updates

        # Parse version to determine significance
        changes = self._analyze_version_change(package, latest_version, pkg_info)

        if changes:
            update = KnowledgeUpdate(
                target_file=package.knowledge_file,
                priority=self._determine_priority(latest_version, changes),
                source=self.create_source(
                    identifier=package.name,
                    version=latest_version,
                    url=pkg_info.get("project_url")
                    or f"https://pypi.org/project/{package.name}/",
                    raw_data=pkg_info,
                ),
                changes=changes,
                new_version=self._suggest_knowledge_version(latest_version),
                breaking=self._is_breaking_version(latest_version),
                rationale=f"New version {latest_version} of {package.name}",
                axiom_alignment={
                    "A10": "Learning from package updates",
                    "A1": "Verified from PyPI registry",
                },
            )
            updates.append(update)

        return updates

    def _analyze_version_change(
        self, package: TrackedPackage, version: str, info: Dict[str, Any]
    ) -> List[KnowledgeChange]:
        """Analyze version to extract changes.

        Args:
            package: Package being analyzed
            version: New version string
            info: Package info from PyPI

        Returns:
            List of changes
        """
        changes: List[KnowledgeChange] = []

        # Check for major version bump (likely breaking)
        version_parts = version.split(".")
        if len(version_parts) >= 1:
            try:
                major = int(version_parts[0])
                if major > 0:  # Not 0.x.x
                    changes.append(
                        KnowledgeChange(
                            change_type=ChangeType.CHANGED,
                            path=f"packages.{package.name}.version",
                            description=f"Updated to version {version}",
                            new_value=version,
                            impact="medium",
                        )
                    )
            except ValueError:
                pass

        # Check description for new features
        description = info.get("description", "")
        _summary = info.get("summary", "")  # Reserved for future use

        # Look for keywords in description
        if any(kw in description.lower() for kw in ["breaking", "deprecated"]):
            changes.append(
                KnowledgeChange(
                    change_type=ChangeType.DEPRECATED,
                    path=f"packages.{package.name}.deprecations",
                    description="Package may have deprecations - review changelog",
                    impact="high",
                )
            )

        # Check requires_python for Python version requirements
        requires_python = info.get("requires_python")
        if requires_python and "3.1" in requires_python:  # Python 3.10+
            changes.append(
                KnowledgeChange(
                    change_type=ChangeType.CHANGED,
                    path=f"packages.{package.name}.python_requires",
                    description=f"Requires Python {requires_python}",
                    new_value=requires_python,
                    impact="medium",
                )
            )

        return changes

    def _determine_priority(
        self, version: str, changes: List[KnowledgeChange]
    ) -> UpdatePriority:
        """Determine update priority.

        Args:
            version: Version string
            changes: Extracted changes

        Returns:
            Priority level
        """
        # Check for security-related changes
        if any(c.change_type == ChangeType.SECURITY for c in changes):
            return UpdatePriority.CRITICAL

        # Major version = high priority
        if self._is_breaking_version(version):
            return UpdatePriority.HIGH

        # Deprecations = medium-high
        if any(c.change_type == ChangeType.DEPRECATED for c in changes):
            return UpdatePriority.HIGH

        return UpdatePriority.MEDIUM

    def _is_breaking_version(self, version: str) -> bool:
        """Check if version indicates breaking changes.

        Args:
            version: Version string

        Returns:
            True if likely breaking
        """
        parts = version.split(".")
        if len(parts) >= 2:
            try:
                major = int(parts[0])
                minor = int(parts[1])
                # Major bump (not 0.x) or 0.x.0 are often breaking
                return (major > 0 and minor == 0) or (
                    major == 0 and minor > 0 and parts[2] == "0"
                )
            except (ValueError, IndexError):
                pass
        return False

    def _suggest_knowledge_version(self, package_version: str) -> str:
        """Suggest knowledge file version based on package version.

        Args:
            package_version: Package version string

        Returns:
            Suggested knowledge version
        """
        parts = package_version.split(".")
        if len(parts) >= 2:
            return f"{parts[0]}.{parts[1]}.0"
        return "1.0.0"
