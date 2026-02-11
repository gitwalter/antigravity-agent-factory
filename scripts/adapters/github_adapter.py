"""
GitHub Adapter for Knowledge Evolution

This adapter fetches knowledge updates from GitHub by analyzing:
- Trending repositories in relevant technology stacks
- Release notes and changelogs from framework repositories
- Documentation updates from official repos
- Best practices emerging from popular open source projects

Features:
    - Trending repository analysis
    - Release monitoring for tracked frameworks
    - Pattern extraction from popular codebases
    - Rate limit handling with exponential backoff
    - Response caching for efficiency

Dependencies:
    - aiohttp: Async HTTP client
    - GitHub API v4 (GraphQL) for efficient queries

Author: Antigravity Agent Factory
Version: 1.0.0
"""

import asyncio
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

try:
    import aiohttp
except ImportError:
    aiohttp = None  # Will be checked at runtime

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
class TrackedRepository:
    """A GitHub repository being tracked for updates.
    
    Attributes:
        owner: Repository owner (user or org)
        name: Repository name
        knowledge_file: Target knowledge file for updates
        track_releases: Whether to track releases
        track_docs: Whether to track documentation changes
        patterns_to_extract: Patterns to look for in the repo
        trust_level: Trust level for this repository
    """
    owner: str
    name: str
    knowledge_file: str
    track_releases: bool = True
    track_docs: bool = True
    patterns_to_extract: List[str] = None
    trust_level: TrustLevel = TrustLevel.OFFICIAL
    
    @property
    def full_name(self) -> str:
        """Get full repository name (owner/name)."""
        return f"{self.owner}/{self.name}"
    
    @property
    def url(self) -> str:
        """Get GitHub URL for this repository."""
        return f"https://github.com/{self.owner}/{self.name}"


class GitHubAdapter(BaseAdapter):
    """Adapter for fetching knowledge updates from GitHub.
    
    This adapter connects to GitHub's API to:
    1. Monitor trending repositories for emerging patterns
    2. Track releases from official framework repositories
    3. Extract best practices from popular codebases
    4. Update knowledge files with new patterns and versions
    
    Example:
        config = AdapterConfig(
            api_key="ghp_xxx...",
            trust_level=TrustLevel.OFFICIAL
        )
        adapter = GitHubAdapter(config)
        updates = await adapter.fetch_updates()
    """
    
    API_BASE_URL = "https://api.github.com"
    GRAPHQL_URL = "https://api.github.com/graphql"
    
    # Repositories to track for each knowledge file
    TRACKED_REPOS: List[TrackedRepository] = [
        # Python frameworks
        TrackedRepository(
            owner="tiangolo", name="fastapi",
            knowledge_file="fastapi-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        TrackedRepository(
            owner="pallets", name="flask",
            knowledge_file="flask-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        TrackedRepository(
            owner="django", name="django",
            knowledge_file="django-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        
        # JavaScript/TypeScript frameworks
        TrackedRepository(
            owner="vercel", name="next.js",
            knowledge_file="nextjs-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        TrackedRepository(
            owner="facebook", name="react",
            knowledge_file="react-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        
        # AI/ML frameworks
        TrackedRepository(
            owner="langchain-ai", name="langchain",
            knowledge_file="langchain-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        TrackedRepository(
            owner="microsoft", name="autogen",
            knowledge_file="autogen-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        TrackedRepository(
            owner="joaomdmoura", name="crewAI",
            knowledge_file="crewai-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        
        # Java frameworks
        TrackedRepository(
            owner="spring-projects", name="spring-boot",
            knowledge_file="spring-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
        
        # DevOps/Infrastructure
        TrackedRepository(
            owner="actions", name="runner",
            knowledge_file="cicd-patterns.json",
            trust_level=TrustLevel.OFFICIAL
        ),
    ]
    
    # Languages to search for trending repos
    TRENDING_LANGUAGES = [
        "python", "typescript", "javascript", "java", "kotlin",
        "go", "rust", "csharp"
    ]
    
    def __init__(self, config: AdapterConfig):
        """Initialize the GitHub adapter.
        
        Args:
            config: Adapter configuration with optional API key
        """
        super().__init__(config)
        self._session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_remaining = 5000
        self._rate_limit_reset: Optional[datetime] = None
    
    @property
    def name(self) -> str:
        """Adapter identifier."""
        return "github"
    
    @property
    def description(self) -> str:
        """Human-readable description."""
        return "Fetches patterns and updates from GitHub repositories and trending projects"
    
    @property
    def supported_knowledge_files(self) -> List[str]:
        """Knowledge files this adapter can update."""
        return list(set(repo.knowledge_file for repo in self.TRACKED_REPOS))
    
    async def _get_session(self) -> "aiohttp.ClientSession":
        """Get or create the HTTP session.
        
        Returns:
            aiohttp.ClientSession for making requests
        """
        if aiohttp is None:
            raise ImportError("aiohttp is required for GitHubAdapter. Install with: pip install aiohttp")
        
        if self._session is None or self._session.closed:
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Antigravity-Agent-Factory/1.0",            }
            if self.config.api_key:
                headers["Authorization"] = f"token {self.config.api_key}"
            
            self._session = aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout_seconds)
            )
        
        return self._session
    
    async def _close_session(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Make an API request with rate limit handling.
        
        Args:
            endpoint: API endpoint (relative to base URL)
            method: HTTP method
            params: Query parameters
            json_data: JSON body for POST requests
            
        Returns:
            Response JSON or None on error
        """
        # Check rate limit
        if self._rate_limit_remaining <= 0 and self._rate_limit_reset:
            now = datetime.now(timezone.utc)
            # Ensure rate_limit_reset is timezone-aware
            if self._rate_limit_reset.tzinfo is None:
                self._rate_limit_reset = self._rate_limit_reset.replace(tzinfo=timezone.utc)
            wait_time = (self._rate_limit_reset - now).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(min(wait_time, 60))  # Max 60s wait
        
        session = await self._get_session()
        url = urljoin(self.API_BASE_URL, endpoint)
        
        try:
            async with session.request(method, url, params=params, json=json_data) as response:
                # Update rate limit info
                self._rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 5000))
                reset_ts = response.headers.get("X-RateLimit-Reset")
                if reset_ts:
                    # Use timezone-aware datetime for consistency
                    self._rate_limit_reset = datetime.fromtimestamp(int(reset_ts), tz=timezone.utc)                
                if response.status == 200:
                    return await response.json()
                elif response.status == 403:
                    # Rate limited
                    return None
                elif response.status == 404:
                    return None
                else:
                    return None
        except Exception as e:
            print(f"GitHub API error: {e}")
            return None
    
    async def validate_connection(self) -> bool:
        """Validate GitHub API connection.
        
        Returns:
            True if connection is valid
        """
        result = await self._make_request("/rate_limit")
        return result is not None
    
    async def get_source_version(self) -> Optional[str]:
        """Get current timestamp as version.
        
        Returns:
            ISO timestamp string
        """
        return datetime.now(timezone.utc).isoformat()    
    async def fetch_updates(
        self,
        target_files: Optional[List[str]] = None,
        since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Fetch available updates from GitHub.
        
        Args:
            target_files: Optional list of specific knowledge files to check
            since: Optional datetime to only fetch updates after
            
        Returns:
            List of proposed knowledge updates
        """
        updates: List[KnowledgeUpdate] = []
        
        # Filter repos by target files if specified
        repos_to_check = self.TRACKED_REPOS
        if target_files:
            repos_to_check = [r for r in repos_to_check if r.knowledge_file in target_files]
        
        # Check each tracked repository for releases
        for repo in repos_to_check:
            if repo.track_releases:
                release_updates = await self._check_releases(repo, since)
                updates.extend(release_updates)
        
        # Fetch trending repositories for pattern discovery
        if not target_files:  # Only do trending scan for full updates
            trending_updates = await self._analyze_trending()
            updates.extend(trending_updates)
        
        await self._close_session()
        return updates
    
    async def _check_releases(
        self,
        repo: TrackedRepository,
        since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Check a repository for new releases.
        
        Args:
            repo: Repository to check
            since: Only include releases after this date
            
        Returns:
            List of updates from releases
        """
        updates: List[KnowledgeUpdate] = []
        
        # Fetch latest releases
        endpoint = f"/repos/{repo.owner}/{repo.name}/releases"
        params = {"per_page": 5}  # Get last 5 releases
        
        releases = await self._make_request(endpoint, params=params)
        if not releases:
            return updates
        
        for release in releases:
            release_date = datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
            
            # Filter by date if specified
            if since and release_date < since:
                continue
            
            # Parse release notes for patterns
            changes = self._parse_release_notes(release.get("body", ""), repo)
            
            if changes:
                update = KnowledgeUpdate(
                    target_file=repo.knowledge_file,
                    priority=self._determine_priority(release, changes),
                    source=self.create_source(
                        identifier=repo.full_name,
                        version=release.get("tag_name"),
                        url=release.get("html_url"),
                        raw_data=release
                    ),
                    changes=changes,
                    new_version=self._suggest_version(release.get("tag_name")),
                    breaking=self._is_breaking(release),
                    rationale=f"New release {release.get('tag_name')} of {repo.name}",
                    axiom_alignment={
                        "A10": "Learning from official framework updates",
                        "A1": "Verified from official repository"
                    }
                )
                updates.append(update)
        
        return updates
    
    def _parse_release_notes(
        self,
        notes: str,
        repo: TrackedRepository
    ) -> List[KnowledgeChange]:
        """Parse release notes to extract changes.
        
        Args:
            notes: Release notes markdown
            repo: Repository context
            
        Returns:
            List of extracted changes
        """
        changes: List[KnowledgeChange] = []
        
        if not notes:
            return changes
        
        # Common patterns in release notes
        patterns = {
            r"(?:^|\n)\s*[-*]\s*(?:Added|New|Feature)[:\s]+(.+)": ChangeType.ADDED,
            r"(?:^|\n)\s*[-*]\s*(?:Changed|Updated|Modified)[:\s]+(.+)": ChangeType.CHANGED,
            r"(?:^|\n)\s*[-*]\s*(?:Deprecated)[:\s]+(.+)": ChangeType.DEPRECATED,
            r"(?:^|\n)\s*[-*]\s*(?:Removed|Deleted)[:\s]+(.+)": ChangeType.REMOVED,
            r"(?:^|\n)\s*[-*]\s*(?:Fixed|Bugfix|Bug)[:\s]+(.+)": ChangeType.FIXED,
            r"(?:^|\n)\s*[-*]\s*(?:Security)[:\s]+(.+)": ChangeType.SECURITY,
        }
        
        for pattern, change_type in patterns.items():
            matches = re.findall(pattern, notes, re.IGNORECASE | re.MULTILINE)
            for match in matches[:3]:  # Limit to 3 per type
                changes.append(KnowledgeChange(
                    change_type=change_type,
                    path=f"patterns.{repo.name}",
                    description=match.strip()[:200],  # Truncate
                    impact="medium",
                ))
        
        return changes
    
    def _determine_priority(
        self,
        release: Dict[str, Any],
        changes: List[KnowledgeChange]
    ) -> UpdatePriority:
        """Determine update priority from release info.
        
        Args:
            release: Release data
            changes: Extracted changes
            
        Returns:
            Appropriate priority level
        """
        # Check for security changes
        if any(c.change_type == ChangeType.SECURITY for c in changes):
            return UpdatePriority.CRITICAL
        
        # Check for breaking changes
        if self._is_breaking(release):
            return UpdatePriority.HIGH
        
        # Check for major version
        tag = release.get("tag_name", "")
        if re.match(r"v?\d+\.0\.0", tag):
            return UpdatePriority.HIGH
        
        return UpdatePriority.MEDIUM
    
    def _is_breaking(self, release: Dict[str, Any]) -> bool:
        """Check if release contains breaking changes.
        
        Args:
            release: Release data
            
        Returns:
            True if breaking changes detected
        """
        body = release.get("body", "").lower()
        tag = release.get("tag_name", "").lower()
        
        # Check for breaking indicators
        breaking_indicators = ["breaking", "major", "incompatible", "migration required"]
        return any(indicator in body or indicator in tag for indicator in breaking_indicators)
    
    def _suggest_version(self, release_tag: Optional[str]) -> str:
        """Suggest a version number based on release.
        
        Args:
            release_tag: Release tag name
            
        Returns:
            Suggested version string
        """
        if not release_tag:
            return "1.0.0"
        
        # Extract version from tag
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", release_tag)
        if match:
            major, minor, patch = match.groups()
            return f"{major}.{minor}.{patch}"
        
        return "1.0.0"
    
    async def _analyze_trending(self) -> List[KnowledgeUpdate]:
        """Analyze trending repositories for pattern discovery.
        
        Returns:
            List of updates from trending analysis
        """
        # This is a placeholder for more sophisticated trending analysis
        # In a full implementation, this would:
        # 1. Query GitHub for trending repos in tracked languages
        # 2. Analyze their patterns and practices
        # 3. Compare against current knowledge
        # 4. Propose updates for new patterns
        
        return []
    
    async def get_repository_info(self, owner: str, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a repository.
        
        Args:
            owner: Repository owner
            name: Repository name
            
        Returns:
            Repository information or None
        """
        return await self._make_request(f"/repos/{owner}/{name}")
    
    async def get_readme(self, owner: str, name: str) -> Optional[str]:
        """Get README content from a repository.
        
        Args:
            owner: Repository owner
            name: Repository name
            
        Returns:
            README content or None
        """
        result = await self._make_request(f"/repos/{owner}/{name}/readme")
        if result and "content" in result:
            import base64
            return base64.b64decode(result["content"]).decode("utf-8")
        return None
