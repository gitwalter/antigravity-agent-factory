"""
Hybrid Memory Store for Antigravity Agent Factory
Provides persistent memory storage using ChromaDB for vector search
and JSON for structured data. Includes proposal queue for user-validated
memory creation.

Features:
    - Semantic memory: Long-term validated knowledge
    - Episodic memory: Session-based observations
    - Pending queue: Proposals awaiting user approval
    - Rejected tracking: Prevents re-proposing rejected memories
    - First-run initialization: Graceful setup on new machines

Collections:
    - semantic: User-approved long-term memories
    - episodic: Session observations (temporary)
    - pending: Proposals awaiting approval
    - rejected: Rejected proposals (to avoid re-proposing)

Usage:
    from scripts.memory.memory_store import MemoryStore

    store = MemoryStore()

    # Add a memory (after user approval)
    store.add_memory(
        content="Use pytest for testing",
        metadata={"source": "user_teaching", "scope": "global"},
        memory_type="memory_semantic"
    )

    # Search memories
    results = store.search("testing frameworks", memory_type="memory_semantic", k=5)
"""

import json
import logging
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from scripts.memory.memory_config import (
    QDRANT_HOST,
    QDRANT_PORT,
    VECTOR_SIZE,
    COLLECTION_SEMANTIC,
    COLLECTION_PROCEDURAL,
    COLLECTION_TOOLBOX,
    COLLECTION_ENTITY,
    COLLECTION_SUMMARY,
)

# Short-name aliases for backwards compatibility
_COLLECTION_ALIASES = {
    "semantic": COLLECTION_SEMANTIC,
    "procedural": COLLECTION_PROCEDURAL,
    "toolbox": COLLECTION_TOOLBOX,
    "entity": COLLECTION_ENTITY,
    "summary": COLLECTION_SUMMARY,
    "episodic": "episodic",  # kept as-is
    "pending": "pending",  # kept as-is
    "rejected": "rejected",  # kept as-is
}

logger = logging.getLogger(__name__)


@dataclass
class Memory:
    """
    Represents a stored memory.

    Attributes:
        id: Unique identifier for the memory
        content: The memory content (what was learned)
        metadata: Additional metadata (source, scope, timestamp, etc.)
        memory_type: Type of memory (semantic, episodic, pending, rejected)
        embedding: Optional cached embedding vector
        created_at: When the memory was created
        accessed_count: Number of times this memory was retrieved
        last_accessed: When the memory was last accessed
    """

    id: str
    content: str
    metadata: Dict[str, Any]
    memory_type: str
    embedding: Optional[List[float]] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    accessed_count: int = 0
    last_accessed: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Memory":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class MemoryProposal:
    """
    Represents a memory proposal awaiting user approval.

    Attributes:
        id: Unique identifier for the proposal
        content: What to remember
        source: Where the observation came from
        scope: "project" or "global"
        status: "pending", "accepted", "rejected", "edited"
        confidence: Confidence score (0.0 to 1.0)
        user_response: User's edit if they modified the content
        timestamp: When the proposal was created
        context: Additional context about the observation
    """

    id: str
    content: str
    source: str
    scope: str = "global"
    status: str = "pending"
    confidence: float = 1.0
    user_response: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    context: Optional[str] = None
    target_collection: str = COLLECTION_SEMANTIC

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryProposal":
        """Create from dictionary."""
        return cls(**data)

    def format_for_user(self) -> str:
        """Format proposal for display in chat."""
        scope_display = (
            "All projects" if self.scope == "global" else "This project only"
        )
        return f"""
💡 **Learning Opportunity**

I noticed: "{self.content}"

Source: {self.source}
Scope: {scope_display}
Confidence: {self.confidence * 100:.0f}%

Should I remember this for future sessions?

[✓ Accept]  [✗ Reject]  [✎ Edit]
"""


class MemoryStore:
    """
    Hybrid memory store using Qdrant for vectors and JSON for structured data.

    Provides persistent storage for the inductive memory system with support
    for user-validated proposals.

    Attributes:
        config: Configuration dictionary
        persist_dir: Directory for Qdrant persistence
        _client: Qdrant client (internal, lazy)
        semantic: Semantic memory collection
        episodic: Episodic memory collection
        pending: Pending proposals collection
        rejected: Rejected proposals collection

    Example:
        >>> store = MemoryStore()
        >>> store.add_memory("Use black for formatting", {"source": "user"}, "semantic")
        >>> results = store.search("code formatting", "semantic", k=3)
    """

    DEFAULT_CONFIG = {
        "storage": {
            "vector_db": "qdrant",
            "persist_dir": "data/memory",
            "collections": [
                COLLECTION_SEMANTIC,
                COLLECTION_PROCEDURAL,
                COLLECTION_TOOLBOX,
                COLLECTION_ENTITY,
                COLLECTION_SUMMARY,
                "episodic",
                "pending",
                "rejected",
            ],
        },
        "proposals": {
            "require_user_approval": True,
            "show_confidence": True,
            "show_source": True,
            "rejection_similarity_threshold": 0.9,
        },
    }

    def __init__(
        self, config_path: Optional[str] = None, persist_dir: Optional[str] = None
    ):
        """
        Initialize the memory store.

        Args:
            config_path: Path to memory-config.json. If None, uses defaults.
            persist_dir: Override persist directory from config.
        """
        # Load configuration
        self.config = self._load_config(config_path)

        # Set persist directory
        self._explicit_persist = persist_dir is not None
        if persist_dir:
            self.persist_dir = Path(persist_dir)
        else:
            self.persist_dir = Path(self.config["storage"]["persist_dir"])

        # Track first run
        self._is_first_run = not self.persist_dir.exists()

        # Create directory if needed
        if self._is_first_run:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Memory system initialized (first run - no memories yet)")
            logger.info(f"Memory directory: {self.persist_dir.absolute()}")

        # Initialize Qdrant Client (Lazy)
        self._client = None

        # Lazy-load embedding service
        self._embedding_service = None

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or use defaults."""
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Merge with defaults
                return {**self.DEFAULT_CONFIG, **config}
        return self.DEFAULT_CONFIG.copy()

    @property
    def client(self):
        """Lazy-loaded Qdrant client."""
        if self._client is None:
            self._init_qdrant()
        return self._client

    def _init_qdrant(self) -> None:
        """Initialize Qdrant client and collections."""
        try:
            # IMPORTANT: Lazy imports to keep memory store initialization fast
            from qdrant_client import QdrantClient
            from qdrant_client.http.models import Distance, VectorParams
            from scripts.memory.memory_config import (
                QDRANT_HOST,
                QDRANT_PORT,
                QDRANT_PATH,
                VECTOR_SIZE,
            )

            # Ensure collections exist
            self._client = (
                QdrantClient(path=str(self.persist_dir))
                if self._explicit_persist
                else (
                    QdrantClient(path=QDRANT_PATH)
                    if QDRANT_PATH
                    else QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
                )
            )

            collections = self._client.get_collections().collections
            existing_names = [c.name for c in collections]

            target_collections = self.config["storage"]["collections"]

            for name in target_collections:
                effective_name = self._get_collection_name(name)

                if effective_name not in existing_names:
                    logger.info(
                        f"Creating Qdrant collection for memory: {effective_name}"
                    )
                    self._client.create_collection(
                        collection_name=effective_name,
                        vectors_config=VectorParams(
                            size=VECTOR_SIZE, distance=Distance.COSINE
                        ),
                    )

            logger.debug("Qdrant collections initialized")

        except ImportError:
            raise ImportError(
                "qdrant-client is required for the memory store. "
                "Install with: pip install qdrant-client"
            )
        except Exception as e:
            if QDRANT_PATH:
                logger.error(f"Failed to initialize local Qdrant at {QDRANT_PATH}: {e}")
            else:
                logger.error(
                    f"Failed to connect to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}. Is Docker running? Error: {e}"
                )

    @property
    def embedding_service(self):
        """Lazy-load embedding service."""
        if self._embedding_service is None:
            from scripts.memory.embedding_service import get_embedding_service

            self._embedding_service = get_embedding_service()
        return self._embedding_service

    def _get_collection_name(self, memory_type: str) -> str:
        """Get collection name by memory type. Supports both full names and short aliases."""
        from scripts.memory.memory_config import get_collection_name

        # Resolve short-name alias first
        resolved = _COLLECTION_ALIASES.get(memory_type, memory_type)

        # Apply prefix/override logic
        effective_name = get_collection_name(resolved)

        logger.debug(
            f"Resolved collection name: {memory_type} -> {resolved} -> {effective_name}"
        )
        return effective_name

    # =========================================================================
    # Core Memory Operations
    # =========================================================================

    def add_memory(
        self,
        content: str,
        metadata: Dict[str, Any],
        memory_type: str = COLLECTION_SEMANTIC,
    ) -> str:
        """
        Add a memory to the store.

        Args:
            content: The memory content.
            metadata: Additional metadata.
            memory_type: Type of memory (semantic, episodic, pending, rejected).

        Returns:
            The memory ID (either newly created, or existing if deduplicated).
        """
        # Pre-Consolidation Validation (Deduplication Gate)
        # Prevent semantic drift by rejecting high-similarity duplicates
        # Generate embedding once and reuse for both search and insertion
        embedding_vector = self.embedding_service.embed_single(content)
        embedding = embedding_vector.tolist()

        existing = self.search(
            query=content,
            query_embedding=embedding,
            memory_type=memory_type,
            k=1,
            threshold=0.95,
        )
        if existing:
            duplicates = [e for e in existing if e.metadata.get("similarity", 0) > 0.95]
            if duplicates:
                logger.debug(
                    f"SSGM Deduplication Gate: Similar memory found in {memory_type}. Rejecting insertion."
                )
                return duplicates[0].id

        memory_id = str(uuid.uuid4())

        # Prepare metadata
        full_metadata = {
            **metadata,
            "created_at": datetime.now().isoformat(),
            "memory_type": memory_type,
        }

        # Filter out None values
        full_metadata = {k: v for k, v in full_metadata.items() if v is not None}

        # Add to collection
        collection_name = self._get_collection_name(memory_type)

        from qdrant_client.http.models import PointStruct

        self.client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=memory_id,
                    vector=embedding,
                    payload={"content": content, **full_metadata},
                )
            ],
        )

        logger.debug(f"Added memory to {memory_type}: {memory_id}")
        return memory_id

    def search(
        self,
        query: str,
        memory_type: str = COLLECTION_SEMANTIC,
        k: int = 5,
        threshold: float = 0.0,
        where: Optional[Dict[str, Any]] = None,
        query_embedding: Optional[List[float]] = None,
    ) -> List[Memory]:
        """
        Search for memories by semantic similarity.

        Args:
            query: Query text.
            memory_type: Type of memory to search.
            k: Maximum number of results.
            threshold: Minimum similarity score (0.0 to 1.0).
            where: Optional metadata filter.
            query_embedding: Optional pre-computed embedding vector.

        Returns:
            List of Memory objects, sorted by similarity.
        """
        collection_name = self._get_collection_name(memory_type)

        count = self.client.count(collection_name=collection_name).count
        if count == 0:
            return []

        # Generate query embedding if not provided
        if query_embedding is None:
            query_embedding = self.embedding_service.embed_single(query).tolist()

        # Search
        results = self.client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=k,
            score_threshold=threshold if threshold > 0 else None,
        )

        # Convert to Memory objects
        memories = []
        for hit in results.points:
            payload = hit.payload or {}
            content = payload.pop("content", "")

            # Qdrant returns similarity score directly
            metadata = payload
            metadata["similarity"] = hit.score

            memories.append(
                Memory(
                    id=str(hit.id),
                    content=content,
                    metadata=metadata,
                    memory_type=memory_type,
                )
            )

        return memories

    def get_memory(
        self, memory_id: str, memory_type: str = COLLECTION_SEMANTIC
    ) -> Optional[Memory]:
        """
        Get a specific memory by ID.

        Args:
            memory_id: The memory ID.
            memory_type: Type of memory.

        Returns:
            Memory object or None if not found.
        """
        collection_name = self._get_collection_name(memory_type)

        try:
            results = self.client.retrieve(
                collection_name=collection_name,
                ids=[memory_id],
                with_payload=True,
            )

            if results:
                hit = results[0]
                payload = hit.payload or {}
                content = payload.pop("content", "")

                return Memory(
                    id=str(hit.id),
                    content=content,
                    metadata=payload,
                    memory_type=memory_type,
                )
        except Exception as e:
            logger.debug(f"Memory not found: {memory_id} - {e}")

        return None

    def delete_memory(
        self, memory_id: str, memory_type: str = COLLECTION_SEMANTIC
    ) -> bool:
        """
        Delete a memory by ID.

        Args:
            memory_id: The memory ID.
            memory_type: Type of memory.

        Returns:
            True if deleted, False if not found.
        """
        collection_name = self._get_collection_name(memory_type)

        try:
            self.client.delete(
                collection_name=collection_name,
                points_selector=[memory_id],
            )
            logger.debug(f"Deleted memory: {memory_id}")
            return True
        except Exception as e:
            logger.debug(f"Failed to delete memory: {memory_id} - {e}")
            return False

    def get_relevant_context(self, query: str, k: int = 5) -> str:
        """
        Get relevant context from memories for a query.

        Searches both semantic and episodic memories and formats
        the results for inclusion in agent context.

        Args:
            query: Query text.
            k: Maximum number of memories to include.

        Returns:
            Formatted context string.
        """
        # Search semantic memory
        semantic_results = self.search(query, COLLECTION_SEMANTIC, k=k, threshold=0.5)

        # Search episodic memory (recent observations)
        episodic_results = self.search(query, "episodic", k=k // 2, threshold=0.5)

        if not semantic_results and not episodic_results:
            return ""

        context_parts = []

        if semantic_results:
            context_parts.append("**Relevant Memories:**")
            for memory in semantic_results:
                similarity = memory.metadata.get("similarity", 0)
                source = memory.metadata.get("source", "unknown")
                context_parts.append(
                    f"- {memory.content} "
                    f"[Source: {source} | Confidence: {similarity * 100:.0f}%]"
                )

        if episodic_results:
            context_parts.append("\n**Recent Observations:**")
            for memory in episodic_results:
                context_parts.append(f"- {memory.content}")

        return "\n".join(context_parts)

    # =========================================================================
    # Proposal Operations
    # =========================================================================

    def add_pending_proposal(self, proposal: MemoryProposal) -> str:
        """
        Add a proposal to the pending queue.

        Args:
            proposal: The memory proposal.

        Returns:
            The proposal ID (preserved from proposal.id).
        """
        # Generate embedding
        embedding = self.embedding_service.embed_single(proposal.content).tolist()

        # Prepare metadata
        metadata = proposal.to_dict()
        metadata["created_at"] = datetime.now().isoformat()
        metadata["memory_type"] = "pending"
        metadata = {k: v for k, v in metadata.items() if v is not None}

        # Add to pending collection using the proposal's ID
        from qdrant_client.http.models import PointStruct

        self.client.upsert(
            collection_name=self._get_collection_name("pending"),
            points=[
                PointStruct(
                    id=proposal.id,
                    vector=embedding,
                    payload={"content": proposal.content, **metadata},
                )
            ],
        )

        logger.debug(f"Added pending proposal: {proposal.id}")
        return proposal.id

    def get_pending_proposals(self) -> List[MemoryProposal]:
        """
        Get all pending proposals.

        Returns:
            List of MemoryProposal objects.
        """
        collection_name = self._get_collection_name("pending")
        count = self.client.count(collection_name=collection_name).count
        if count == 0:
            return []

        # Get all points
        results, _ = self.client.scroll(
            collection_name=collection_name,
            limit=count,
            with_payload=True,
        )

        proposals = []
        for hit in results:
            payload = hit.payload or {}
            content = payload.pop("content", "")

            proposals.append(
                MemoryProposal(
                    id=str(hit.id),
                    content=content,
                    source=payload.get("source", "unknown"),
                    scope=payload.get("scope", "global"),
                    status=payload.get("status", "pending"),
                    confidence=payload.get("confidence", 1.0),
                    user_response=payload.get("user_response"),
                    timestamp=payload.get("timestamp", ""),
                    context=payload.get("context"),
                )
            )

        return proposals

    def accept_proposal(
        self,
        proposal_id: str,
        edited_content: Optional[str] = None,
        target_collection: Optional[str] = None,
    ) -> Memory:
        """
        Accept a proposal and move it to the target memory collection.

        Args:
            proposal_id: The proposal ID.
            edited_content: Optional edited content (if user modified).

        Returns:
            The created Memory object.
        """
        # Get the proposal
        proposal_memory = self.get_memory(proposal_id, "pending")
        if not proposal_memory:
            raise ValueError(f"Proposal not found: {proposal_id}")

        # Use edited content if provided
        content = edited_content or proposal_memory.content

        # Determine target collection: provided > proposal metadata > default
        if not target_collection:
            target_collection = proposal_memory.metadata.get(
                "target_collection", COLLECTION_SEMANTIC
            )

        # Update metadata if edited
        metadata = proposal_memory.metadata.copy()
        if edited_content:
            metadata["was_edited"] = True

        memory_id = self.add_memory(content, metadata, target_collection)

        # Remove from pending
        self.delete_memory(proposal_id, "pending")

        logger.info(
            f"Accepted proposal {proposal_id} -> {target_collection} memory {memory_id}"
        )

        return self.get_memory(memory_id, target_collection)

    def reject_proposal(self, proposal_id: str) -> None:
        """
        Reject a proposal and move it to rejected collection.

        Args:
            proposal_id: The proposal ID.
        """
        # Get the proposal
        proposal_memory = self.get_memory(proposal_id, "pending")
        if not proposal_memory:
            raise ValueError(f"Proposal not found: {proposal_id}")

        # Move to rejected
        metadata = {
            **proposal_memory.metadata,
            "status": "rejected",
            "rejected_at": datetime.now().isoformat(),
        }

        self.add_memory(proposal_memory.content, metadata, "rejected")

        # Remove from pending
        self.delete_memory(proposal_id, "pending")

        logger.info(f"Rejected proposal: {proposal_id}")

    def is_similar_to_rejected(self, content: str, threshold: float = 0.9) -> bool:
        """
        Check if content is similar to a previously rejected proposal.

        Args:
            content: Content to check.
            threshold: Similarity threshold.

        Returns:
            True if similar to a rejected proposal.
        """
        rejected_collection = self._get_collection_name("rejected")
        count = self.client.count(collection_name=rejected_collection).count
        if count == 0:
            return False

        results = self.search(content, "rejected", k=1, threshold=threshold)
        return len(results) > 0

    # =========================================================================
    # Status and Utilities
    # =========================================================================

    @property
    def is_empty(self) -> bool:
        """Check if memory store has any memories."""
        return (
            self.client.count(
                collection_name=self._get_collection_name(COLLECTION_SEMANTIC)
            ).count
            == 0
        )

    @property
    def is_first_run(self) -> bool:
        """Check if this is the first run."""
        return self._is_first_run

    def get_status_message(self) -> str:
        """Get human-readable status for agent to report."""
        semantic_collection = self._get_collection_name(COLLECTION_SEMANTIC)
        pending_collection = self._get_collection_name("pending")

        if self.is_empty:
            return "I don't have any memories yet. I'll learn from our interactions."
        else:
            count = self.client.count(collection_name=semantic_collection).count
            pending = self.client.count(collection_name=pending_collection).count

            msg = f"I have {count} memories from previous sessions."
            if pending > 0:
                msg += f" ({pending} proposals pending your approval)"
            return msg

    def get_stats(self) -> dict:
        """Get memory store statistics."""
        return {
            "semantic_count": self.client.count(
                collection_name=self._get_collection_name(COLLECTION_SEMANTIC)
            ).count,
            "episodic_count": self.client.count(
                collection_name=self._get_collection_name("episodic")
            ).count,
            "pending_count": self.client.count(
                collection_name=self._get_collection_name("pending")
            ).count,
            "rejected_count": self.client.count(
                collection_name=self._get_collection_name("rejected")
            ).count,
            "persist_dir": str(self.persist_dir.absolute()),
            "is_first_run": self._is_first_run,
        }

    def clear_episodic(self) -> int:
        """
        Clear all episodic memories (session cleanup).

        Returns:
            Number of memories cleared.
        """
        collection_name = self._get_collection_name("episodic")
        count = self.client.count(collection_name=collection_name).count
        if count > 0:
            from qdrant_client.http.models import Filter

            self.client.delete(
                collection_name=collection_name,
                points_selector=Filter(),  # Delete all
            )
        logger.info(f"Cleared {count} episodic memories")
        return count

    def close(self) -> None:
        """
        Close the Qdrant client and release resources.

        This is critical on Windows to avoid file locks and resource exhaustion
        during large test runs.
        """
        if hasattr(self, "client"):
            try:
                self.client.close()
                logger.debug("MemoryStore Qdrant client closed")
            except Exception as e:
                logger.warning(f"Error closing MemoryStore client: {e}")


# Singleton instance for convenience
_default_store: Optional[MemoryStore] = None


def get_memory_store(
    config_path: Optional[str] = None, persist_dir: Optional[str] = None
) -> MemoryStore:
    """
    Get or create the default memory store instance.

    Args:
        config_path: Config path (only applies on first call).
        persist_dir: Override persist directory (only applies on first call).

    Returns:
        MemoryStore instance.
    """
    global _default_store

    if _default_store is None:
        _default_store = MemoryStore(config_path=config_path, persist_dir=persist_dir)

    return _default_store


def reset_memory_store() -> None:
    """Reset the singleton instance (for testing)."""
    global _default_store
    _default_store = None
