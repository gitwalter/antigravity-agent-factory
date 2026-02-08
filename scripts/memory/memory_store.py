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
        memory_type="semantic"
    )
    
    # Search memories
    results = store.search("testing frameworks", memory_type="semantic", k=5)
"""

import json
import logging
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

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
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "MemoryProposal":
        """Create from dictionary."""
        return cls(**data)
    
    def format_for_user(self) -> str:
        """Format proposal for display in chat."""
        scope_display = "All projects" if self.scope == "global" else "This project only"
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
    Hybrid memory store using ChromaDB for vectors and JSON for structured data.
    
    Provides persistent storage for the inductive memory system with support
    for user-validated proposals.
    
    Attributes:
        config: Configuration dictionary
        persist_dir: Directory for ChromaDB persistence
        vector_db: ChromaDB client
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
            "vector_db": "chromadb",
            "persist_dir": "data/memory",
            "collections": ["semantic", "episodic", "pending", "rejected"]
        },
        "proposals": {
            "require_user_approval": True,
            "show_confidence": True,
            "show_source": True,
            "rejection_similarity_threshold": 0.9
        }
    }
    
    def __init__(
        self, 
        config_path: Optional[str] = None,
        persist_dir: Optional[str] = None
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
        if persist_dir:
            self.persist_dir = Path(persist_dir)
        else:
            self.persist_dir = Path(self.config["storage"]["persist_dir"])
        
        # Track first run
        self._is_first_run = not self.persist_dir.exists()
        
        # Create directory if needed
        if self._is_first_run:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Memory system initialized (first run - no memories yet)")
            logger.info(f"Memory directory: {self.persist_dir.absolute()}")
        
        # Initialize ChromaDB
        self._init_chromadb()
        
        # Lazy-load embedding service
        self._embedding_service = None
    
    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or use defaults."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults
                return {**self.DEFAULT_CONFIG, **config}
        return self.DEFAULT_CONFIG.copy()
    
    def _init_chromadb(self) -> None:
        """Initialize ChromaDB client and collections."""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Create persistent client
            self.vector_db = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Create or get collections
            self.semantic = self.vector_db.get_or_create_collection(
                name="semantic",
                metadata={"description": "User-approved long-term memories"}
            )
            self.episodic = self.vector_db.get_or_create_collection(
                name="episodic",
                metadata={"description": "Session-based observations"}
            )
            self.pending = self.vector_db.get_or_create_collection(
                name="pending",
                metadata={"description": "Proposals awaiting user approval"}
            )
            self.rejected = self.vector_db.get_or_create_collection(
                name="rejected",
                metadata={"description": "Rejected proposals"}
            )
            
            logger.debug("ChromaDB collections initialized")
            
        except ImportError:
            raise ImportError(
                "chromadb is required for the memory store. "
                "Install with: pip install chromadb"
            )
    
    @property
    def embedding_service(self):
        """Lazy-load embedding service."""
        if self._embedding_service is None:
            from scripts.memory.embedding_service import get_embedding_service
            self._embedding_service = get_embedding_service()
        return self._embedding_service
    
    def _get_collection(self, memory_type: str):
        """Get collection by memory type."""
        collections = {
            "semantic": self.semantic,
            "episodic": self.episodic,
            "pending": self.pending,
            "rejected": self.rejected
        }
        if memory_type not in collections:
            raise ValueError(f"Unknown memory type: {memory_type}")
        return collections[memory_type]
    
    # =========================================================================
    # Core Memory Operations
    # =========================================================================
    
    def add_memory(
        self, 
        content: str, 
        metadata: Dict[str, Any],
        memory_type: str = "semantic"
    ) -> str:
        """
        Add a memory to the store.
        
        Args:
            content: The memory content.
            metadata: Additional metadata.
            memory_type: Type of memory (semantic, episodic, pending, rejected).
            
        Returns:
            The memory ID.
        """
        memory_id = str(uuid.uuid4())
        
        # Generate embedding
        embedding = self.embedding_service.embed_single(content).tolist()
        
        # Prepare metadata - ChromaDB doesn't accept None values
        full_metadata = {
            **metadata,
            "created_at": datetime.now().isoformat(),
            "memory_type": memory_type
        }
        
        # Filter out None values (ChromaDB requirement)
        full_metadata = {k: v for k, v in full_metadata.items() if v is not None}
        
        # Add to collection
        collection = self._get_collection(memory_type)
        collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[full_metadata]
        )
        
        logger.debug(f"Added memory to {memory_type}: {memory_id}")
        return memory_id
    
    def search(
        self, 
        query: str, 
        memory_type: str = "semantic",
        k: int = 5,
        threshold: float = 0.0,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Memory]:
        """
        Search for memories by semantic similarity.
        
        Args:
            query: Query text.
            memory_type: Type of memory to search.
            k: Maximum number of results.
            threshold: Minimum similarity score (0.0 to 1.0).
            where: Optional metadata filter.
            
        Returns:
            List of Memory objects, sorted by similarity.
        """
        collection = self._get_collection(memory_type)
        
        if collection.count() == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_single(query).tolist()
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, collection.count()),
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        # Convert to Memory objects
        memories = []
        if results["ids"] and results["ids"][0]:
            for i, memory_id in enumerate(results["ids"][0]):
                # ChromaDB returns distances, convert to similarity
                # For cosine distance: similarity = 1 - distance
                distance = results["distances"][0][i] if results["distances"] else 0
                similarity = 1 - distance
                
                if similarity >= threshold:
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    metadata["similarity"] = similarity
                    
                    memories.append(Memory(
                        id=memory_id,
                        content=results["documents"][0][i],
                        metadata=metadata,
                        memory_type=memory_type
                    ))
        
        return memories
    
    def get_memory(self, memory_id: str, memory_type: str = "semantic") -> Optional[Memory]:
        """
        Get a specific memory by ID.
        
        Args:
            memory_id: The memory ID.
            memory_type: Type of memory.
            
        Returns:
            Memory object or None if not found.
        """
        collection = self._get_collection(memory_type)
        
        try:
            result = collection.get(
                ids=[memory_id],
                include=["documents", "metadatas"]
            )
            
            if result["ids"]:
                return Memory(
                    id=result["ids"][0],
                    content=result["documents"][0],
                    metadata=result["metadatas"][0],
                    memory_type=memory_type
                )
        except Exception as e:
            logger.debug(f"Memory not found: {memory_id} - {e}")
        
        return None
    
    def delete_memory(self, memory_id: str, memory_type: str = "semantic") -> bool:
        """
        Delete a memory by ID.
        
        Args:
            memory_id: The memory ID.
            memory_type: Type of memory.
            
        Returns:
            True if deleted, False if not found.
        """
        collection = self._get_collection(memory_type)
        
        try:
            collection.delete(ids=[memory_id])
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
        semantic_results = self.search(query, "semantic", k=k, threshold=0.5)
        
        # Search episodic memory (recent observations)
        episodic_results = self.search(query, "episodic", k=k//2, threshold=0.5)
        
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
                    f"[Source: {source} | Confidence: {similarity*100:.0f}%]"
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
        
        # Prepare metadata - ChromaDB doesn't accept None values
        metadata = proposal.to_dict()
        metadata["created_at"] = datetime.now().isoformat()
        metadata["memory_type"] = "pending"
        metadata = {k: v for k, v in metadata.items() if v is not None}
        
        # Add to pending collection using the proposal's ID
        self.pending.add(
            ids=[proposal.id],
            embeddings=[embedding],
            documents=[proposal.content],
            metadatas=[metadata]
        )
        
        logger.debug(f"Added pending proposal: {proposal.id}")
        return proposal.id
    
    def get_pending_proposals(self) -> List[MemoryProposal]:
        """
        Get all pending proposals.
        
        Returns:
            List of MemoryProposal objects.
        """
        if self.pending.count() == 0:
            return []
        
        results = self.pending.get(include=["documents", "metadatas"])
        
        proposals = []
        if results["ids"]:
            for i, proposal_id in enumerate(results["ids"]):
                metadata = results["metadatas"][i] if results["metadatas"] else {}
                proposals.append(MemoryProposal(
                    id=proposal_id,
                    content=results["documents"][i],
                    source=metadata.get("source", "unknown"),
                    scope=metadata.get("scope", "global"),
                    status=metadata.get("status", "pending"),
                    confidence=metadata.get("confidence", 1.0),
                    user_response=metadata.get("user_response"),
                    timestamp=metadata.get("timestamp", ""),
                    context=metadata.get("context")
                ))
        
        return proposals
    
    def accept_proposal(self, proposal_id: str, edited_content: Optional[str] = None) -> Memory:
        """
        Accept a proposal and move it to semantic memory.
        
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
        
        # Create semantic memory
        metadata = {
            "source": proposal_memory.metadata.get("source", "proposal"),
            "scope": proposal_memory.metadata.get("scope", "global"),
            "original_proposal_id": proposal_id,
            "approved_at": datetime.now().isoformat(),
            "was_edited": edited_content is not None
        }
        
        memory_id = self.add_memory(content, metadata, "semantic")
        
        # Remove from pending
        self.delete_memory(proposal_id, "pending")
        
        logger.info(f"Accepted proposal {proposal_id} -> semantic memory {memory_id}")
        
        return self.get_memory(memory_id, "semantic")
    
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
            "rejected_at": datetime.now().isoformat()
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
        if self.rejected.count() == 0:
            return False
        
        results = self.search(content, "rejected", k=1, threshold=threshold)
        return len(results) > 0
    
    # =========================================================================
    # Status and Utilities
    # =========================================================================
    
    @property
    def is_empty(self) -> bool:
        """Check if memory store has any memories."""
        return self.semantic.count() == 0
    
    @property
    def is_first_run(self) -> bool:
        """Check if this is the first run."""
        return self._is_first_run
    
    def get_status_message(self) -> str:
        """Get human-readable status for agent to report."""
        if self.is_empty:
            return "I don't have any memories yet. I'll learn from our interactions."
        else:
            count = self.semantic.count()
            pending = self.pending.count()
            
            msg = f"I have {count} memories from previous sessions."
            if pending > 0:
                msg += f" ({pending} proposals pending your approval)"
            return msg
    
    def get_stats(self) -> dict:
        """Get memory store statistics."""
        return {
            "semantic_count": self.semantic.count(),
            "episodic_count": self.episodic.count(),
            "pending_count": self.pending.count(),
            "rejected_count": self.rejected.count(),
            "persist_dir": str(self.persist_dir.absolute()),
            "is_first_run": self._is_first_run
        }
    
    def clear_episodic(self) -> int:
        """
        Clear all episodic memories (session cleanup).
        
        Returns:
            Number of memories cleared.
        """
        count = self.episodic.count()
        if count > 0:
            # Get all IDs and delete
            results = self.episodic.get()
            if results["ids"]:
                self.episodic.delete(ids=results["ids"])
        logger.info(f"Cleared {count} episodic memories")
        return count


# Singleton instance for convenience
_default_store: Optional[MemoryStore] = None


def get_memory_store(config_path: Optional[str] = None) -> MemoryStore:
    """
    Get or create the default memory store instance.
    
    Args:
        config_path: Config path (only applies on first call).
        
    Returns:
        MemoryStore instance.
    """
    global _default_store
    
    if _default_store is None:
        _default_store = MemoryStore(config_path=config_path)
    
    return _default_store
