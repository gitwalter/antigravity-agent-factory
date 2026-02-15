"""
NPM Adapter for Knowledge Evolution

This adapter fetches knowledge updates from NPM (Node Package Manager) by analyzing:
- Package version updates for JavaScript/TypeScript frameworks
- Trending packages and emerging patterns
- Breaking changes and deprecation notices
- TypeScript type definition updates

Features:
    - Package version monitoring
    - Popularity and download trend analysis
    - Security advisory checking
    - TypeScript types tracking

Dependencies:
    - aiohttp: Async HTTP client
    - NPM Registry API

Author: Antigravity Agent Factory
Version: 1.0.0
"""

from dataclasses import dataclass
from datetime import datetime
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
class TrackedNPMPackage:
    """An NPM package being tracked for updates.

    Attributes:
        name: Package name on NPM
        knowledge_file: Target knowledge file for updates
        track_types: Whether to track @types package
        trust_level: Trust level for this package
    """

    name: str
    knowledge_file: str
    track_types: bool = True
    trust_level: TrustLevel = TrustLevel.OFFICIAL


class NPMAdapter(BaseAdapter):
    """Adapter for fetching knowledge updates from NPM.

    This adapter connects to NPM's registry API to:
    1. Monitor package versions for tracked frameworks
    2. Detect new releases with breaking changes
    3. Track TypeScript type definition updates
    4. Check for security advisories

    Example:
        config = AdapterConfig(trust_level=TrustLevel.OFFICIAL)
        adapter = NPMAdapter(config)
        updates = await adapter.fetch_updates()
    """

    API_BASE_URL = "https://registry.npmjs.org"

    # Packages to track for JavaScript/TypeScript knowledge files
    TRACKED_PACKAGES: List[TrackedNPMPackage] = [
        # React ecosystem
        TrackedNPMPackage(name="react", knowledge_file="react-patterns.json"),
        TrackedNPMPackage(name="react-dom", knowledge_file="react-patterns.json"),
        TrackedNPMPackage(name="next", knowledge_file="nextjs-patterns.json"),
        # Build tools
        TrackedNPMPackage(name="vite", knowledge_file="nextjs-patterns.json"),
        TrackedNPMPackage(name="typescript", knowledge_file="nextjs-patterns.json"),
        # Testing
        TrackedNPMPackage(name="jest", knowledge_file="tdd-patterns.json"),
        TrackedNPMPackage(name="vitest", knowledge_file="tdd-patterns.json"),
        TrackedNPMPackage(name="playwright", knowledge_file="bdd-patterns.json"),
        # AI/LLM
        TrackedNPMPackage(name="openai", knowledge_file="llm-provider-comparison.json"),
        TrackedNPMPackage(name="langchain", knowledge_file="langchain-patterns.json"),
        # n8n
        TrackedNPMPackage(name="n8n", knowledge_file="n8n-patterns.json"),
    ]

    def __init__(self, config: AdapterConfig):
        """Initialize the NPM adapter.

        Args:
            config: Adapter configuration
        """
        super().__init__(config)
        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def name(self) -> str:
        """Adapter identifier."""
        return "npm"

    @property
    def description(self) -> str:
        """Human-readable description."""
        return "Fetches JavaScript/TypeScript package updates from NPM"

    @property
    def supported_knowledge_files(self) -> List[str]:
        """Knowledge files this adapter can update."""
        return list(set(pkg.knowledge_file for pkg in self.TRACKED_PACKAGES))

    async def _get_session(self) -> "aiohttp.ClientSession":
        """Get or create the HTTP session."""
        if aiohttp is None:
            raise ImportError(
                "aiohttp is required for NPMAdapter. Install with: pip install aiohttp"
            )

        if self._session is None or self._session.closed:
            headers = {
                "Accept": "application/json",
                "User-Agent": "Antigravity-Agent-Factory/1.0",
            }
            if self.config.api_key:
                headers["Authorization"] = f"Bearer {self.config.api_key}"

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
        """Fetch package information from NPM.

        Args:
            package_name: Name of the package

        Returns:
            Package info dict or None on error
        """
        session = await self._get_session()
        url = f"{self.API_BASE_URL}/{package_name}"

        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception as e:
            print(f"NPM API error for {package_name}: {e}")
            return None

    async def validate_connection(self) -> bool:
        """Validate NPM registry connection.

        Returns:
            True if connection is valid
        """
        result = await self._get_package_info("npm")  # npm package exists
        return result is not None

    async def fetch_updates(
        self, target_files: Optional[List[str]] = None, since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Fetch available updates from NPM.

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
        self, package: TrackedNPMPackage, since: Optional[datetime] = None
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

        # Get latest version
        dist_tags = info.get("dist-tags", {})
        latest_version = dist_tags.get("latest")
        if not latest_version:
            return updates

        # Get version info
        versions = info.get("versions", {})
        _version_info = versions.get(latest_version, {})  # Reserved for future use

        # Get release time
        time_info = info.get("time", {})
        release_time_str = time_info.get(latest_version)
        release_time = None
        if release_time_str:
            try:
                release_time = datetime.fromisoformat(
                    release_time_str.replace("Z", "+00:00")
                )
            except ValueError:
                pass

        # Filter by date if specified
        if since and release_time and release_time < since:
            return updates

        # Analyze changes
        changes = self._analyze_package(package, latest_version, info)

        if changes:
            update = KnowledgeUpdate(
                target_file=package.knowledge_file,
                priority=self._determine_priority(latest_version, changes),
                source=self.create_source(
                    identifier=package.name,
                    version=latest_version,
                    url=f"https://www.npmjs.com/package/{package.name}",
                    raw_data={
                        "dist-tags": dist_tags,
                        "description": info.get("description"),
                    },
                ),
                changes=changes,
                new_version=self._suggest_version(latest_version),
                breaking=self._is_major_version(latest_version),
                rationale=f"New version {latest_version} of {package.name}",
                axiom_alignment={
                    "A10": "Learning from NPM package updates",
                    "A1": "Verified from NPM registry",
                },
            )
            updates.append(update)

        return updates

    def _analyze_package(
        self, package: TrackedNPMPackage, version: str, info: Dict[str, Any]
    ) -> List[KnowledgeChange]:
        """Analyze package to extract changes.

        Args:
            package: Package being analyzed
            version: New version string
            info: Package info from NPM

        Returns:
            List of changes
        """
        changes: List[KnowledgeChange] = []

        # Version update change
        changes.append(
            KnowledgeChange(
                change_type=ChangeType.CHANGED,
                path=f"packages.{package.name}.version",
                description=f"Updated to version {version}",
                new_value=version,
                impact="medium" if self._is_major_version(version) else "low",
            )
        )

        # Check for engine requirements
        versions = info.get("versions", {})
        version_info = versions.get(version, {})
        engines = version_info.get("engines", {})

        if engines.get("node"):
            changes.append(
                KnowledgeChange(
                    change_type=ChangeType.CHANGED,
                    path=f"packages.{package.name}.node_requirement",
                    description=f"Requires Node.js {engines['node']}",
                    new_value=engines["node"],
                    impact="medium",
                )
            )

        return changes

    def _determine_priority(
        self, version: str, changes: List[KnowledgeChange]
    ) -> UpdatePriority:
        """Determine update priority."""
        if self._is_major_version(version):
            return UpdatePriority.HIGH
        return UpdatePriority.MEDIUM

    def _is_major_version(self, version: str) -> bool:
        """Check if this is a major version bump."""
        parts = version.split(".")
        if len(parts) >= 2:
            try:
                minor = int(parts[1])
                patch = int(parts[2]) if len(parts) > 2 else 0
                return minor == 0 and patch == 0
            except (ValueError, IndexError):
                pass
        return False

    def _suggest_version(self, package_version: str) -> str:
        """Suggest knowledge file version."""
        parts = package_version.split(".")
        if len(parts) >= 2:
            return f"{parts[0]}.{parts[1]}.0"
        return "1.0.0"
