"""
Community Adapter for Knowledge Evolution

This adapter fetches knowledge updates from community-curated sources such as
Awesome lists, popular dev blogs, and community repositories.

Features:
    - Awesome list monitoring
    - Blog post pattern extraction
    - Community repository analysis
    - Trending pattern detection

Note: This is a foundational implementation. Production use would require
additional parsing for specific community sources.

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
class CommunitySource:
    """A community source being tracked.
    
    Attributes:
        name: Source name
        source_type: Type of source (awesome_list, blog, repository)
        knowledge_file: Target knowledge file
        url: Source URL
        github_repo: GitHub repo if applicable
    """
    name: str
    source_type: str
    knowledge_file: str
    url: str
    github_repo: Optional[str] = None


class CommunityAdapter(BaseAdapter):
    """Adapter for fetching updates from community sources.
    
    This adapter monitors community-curated sources like Awesome lists
    and extracts emerging patterns and tools.
    
    Example:
        config = AdapterConfig(trust_level=TrustLevel.COMMUNITY)
        adapter = CommunityAdapter(config)
        updates = await adapter.fetch_updates()
    """
    
    # Community sources to track
    COMMUNITY_SOURCES: List[CommunitySource] = [
        CommunitySource(
            name="Awesome Python",
            source_type="awesome_list",
            knowledge_file="best-practices.json",
            url="https://github.com/vinta/awesome-python",
            github_repo="vinta/awesome-python",
        ),
        CommunitySource(
            name="Awesome React",
            source_type="awesome_list",
            knowledge_file="react-patterns.json",
            url="https://github.com/enaqx/awesome-react",
            github_repo="enaqx/awesome-react",
        ),
        CommunitySource(
            name="Awesome LangChain",
            source_type="awesome_list",
            knowledge_file="langchain-patterns.json",
            url="https://github.com/kyrolabs/awesome-langchain",
            github_repo="kyrolabs/awesome-langchain",
        ),
        CommunitySource(
            name="Awesome FastAPI",
            source_type="awesome_list",
            knowledge_file="fastapi-patterns.json",
            url="https://github.com/mjhea0/awesome-fastapi",
            github_repo="mjhea0/awesome-fastapi",
        ),
        CommunitySource(
            name="Awesome AI Agents",
            source_type="awesome_list",
            knowledge_file="multi-agent-patterns.json",
            url="https://github.com/e2b-dev/awesome-ai-agents",
            github_repo="e2b-dev/awesome-ai-agents",
        ),
    ]
    
    def __init__(self, config: AdapterConfig):
        """Initialize the community adapter.
        
        Args:
            config: Adapter configuration
        """
        super().__init__(config)
        config.trust_level = TrustLevel.COMMUNITY  # Always community trust
        self._session: Optional[aiohttp.ClientSession] = None
    
    @property
    def name(self) -> str:
        """Adapter identifier."""
        return "community"
    
    @property
    def description(self) -> str:
        """Human-readable description."""
        return "Fetches patterns from community-curated sources"
    
    @property
    def supported_knowledge_files(self) -> List[str]:
        """Knowledge files this adapter can update."""
        return list(set(src.knowledge_file for src in self.COMMUNITY_SOURCES))
    
    async def _get_session(self) -> "aiohttp.ClientSession":
        """Get or create the HTTP session."""
        if aiohttp is None:
            raise ImportError("aiohttp required for CommunityAdapter")
        
        if self._session is None or self._session.closed:
            headers = {
                "User-Agent": "Antigravity-Agent-Factory/1.0",                "Accept": "application/vnd.github.v3+json",
            }
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
    
    async def validate_connection(self) -> bool:
        """Validate GitHub API connection."""
        try:
            session = await self._get_session()
            async with session.get("https://api.github.com/rate_limit") as resp:
                return resp.status == 200
        except Exception:
            return False
    
    async def fetch_updates(
        self,
        target_files: Optional[List[str]] = None,
        since: Optional[datetime] = None
    ) -> List[KnowledgeUpdate]:
        """Fetch updates from community sources.
        
        Args:
            target_files: Optional filter by knowledge files
            since: Optional date filter
            
        Returns:
            List of knowledge updates
        """
        updates: List[KnowledgeUpdate] = []
        
        sources = self.COMMUNITY_SOURCES
        if target_files:
            sources = [s for s in sources if s.knowledge_file in target_files]
        
        for source in sources:
            source_updates = await self._check_source(source, since)
            updates.extend(source_updates)
        
        await self._close_session()
        return updates
    
    async def _check_source(
        self,
        source: CommunitySource,
        since: Optional[datetime]
    ) -> List[KnowledgeUpdate]:
        """Check a community source for updates.
        
        Args:
            source: Source to check
            since: Date filter
            
        Returns:
            List of updates
        """
        updates: List[KnowledgeUpdate] = []
        
        if source.github_repo:
            repo_info = await self._get_repo_info(source.github_repo)
            
            if repo_info:
                # Check if repo was updated recently
                updated_at = repo_info.get("pushed_at")
                if updated_at:
                    updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                    
                    if since and updated_dt < since:
                        return updates
                
                changes = [
                    KnowledgeChange(
                        change_type=ChangeType.CHANGED,
                        path=f"community.{source.name}",
                        description=f"Community source {source.name} updated",
                        impact="low",
                    )
                ]
                
                update = KnowledgeUpdate(
                    target_file=source.knowledge_file,
                    priority=UpdatePriority.LOW,
                    source=self.create_source(
                        identifier=source.name,
                        url=source.url,
                        raw_data={"stars": repo_info.get("stargazers_count")},
                    ),
                    changes=changes,
                    new_version="1.0.0",
                    breaking=False,
                    rationale=f"Updates from {source.name}",
                    axiom_alignment={
                        "A10": "Learning from community wisdom",
                    }
                )
                updates.append(update)
        
        return updates
    
    async def _get_repo_info(self, repo: str) -> Optional[Dict[str, Any]]:
        """Get GitHub repository information.
        
        Args:
            repo: Repository in owner/name format
            
        Returns:
            Repository info or None
        """
        session = await self._get_session()
        
        try:
            url = f"https://api.github.com/repos/{repo}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception:
            pass
        
        return None
