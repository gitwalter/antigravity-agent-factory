"""
Induction Engine for User-Validated Learning

Processes observations from agent interactions and creates memory proposals
that require user approval before being stored. This ensures the user
maintains control over what the agent learns (A2: User Primacy).

Learning Flow:
    1. OBSERVE: Agent notices something worth learning
    2. CHECK: Verify not similar to rejected memories
    3. PROPOSE: Create proposal for user approval
    4. WAIT: User reviews and decides (Accept/Reject/Edit)
    5. STORE: If approved, move to semantic memory
    6. RECALL: Future sessions can use the learned knowledge

Usage:
    from scripts.memory.induction_engine import InductionEngine
    
    engine = InductionEngine()
    
    # Observe an event
    proposal = engine.observe({
        "type": "user_correction",
        "content": "Use pytest instead of unittest"
    })
    
    # User approves
    if proposal:
        engine.accept_proposal(proposal.id)
"""

import logging
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

from scripts.memory.memory_store import (
    MemoryStore, 
    MemoryProposal, 
    Memory,
    get_memory_store
)
from scripts.guardian.mutability_guard import (
    MutabilityGuard,
    get_mutability_guard,
    ValidationResult
)

logger = logging.getLogger(__name__)


@dataclass
class ObservationEvent:
    """
    Represents an observation event that might become a memory.
    
    Attributes:
        type: Type of observation (user_correction, explicit_teaching, etc.)
        content: The main content of the observation
        context: Additional context about the observation
        session_id: Session identifier
        timestamp: When the observation occurred
        metadata: Additional metadata
    """
    type: str
    content: str
    context: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


# Observation types and their default confidence levels
OBSERVATION_TYPES = {
    "user_correction": {
        "description": "User corrected the agent's behavior",
        "confidence": 0.95,
        "proposal_template": "You corrected me to {content}. Remember this?",
        "scope": "global"
    },
    "explicit_teaching": {
        "description": "User explicitly taught something",
        "confidence": 1.0,
        "proposal_template": "You taught me: {content}. Store as knowledge?",
        "scope": "global"
    },
    "successful_pattern": {
        "description": "A pattern that worked well",
        "confidence": 0.7,
        "proposal_template": "Using {content} worked well. Remember this approach?",
        "scope": "project"
    },
    "error_resolution": {
        "description": "How an error was resolved",
        "confidence": 0.8,
        "proposal_template": "We fixed an issue by {content}. Remember for next time?",
        "scope": "global"
    },
    "preference": {
        "description": "User preference detected",
        "confidence": 0.85,
        "proposal_template": "I noticed you prefer {content}. Remember this preference?",
        "scope": "global"
    }
}


class InductionEngine:
    """
    Engine for inductive learning from agent interactions.
    
    Observes events, creates proposals, and manages the user-validated
    learning process. All learning requires explicit user approval.
    
    Attributes:
        memory: MemoryStore instance
        guard: MutabilityGuard instance
        config: Configuration dictionary
        
    Example:
        >>> engine = InductionEngine()
        >>> proposal = engine.observe({
        ...     "type": "user_correction",
        ...     "content": "Use black for formatting"
        ... })
        >>> if proposal:
        ...     print(proposal.format_for_user())
        ...     # User approves
        ...     engine.accept_proposal(proposal.id)
    """
    
    def __init__(
        self,
        memory_store: Optional[MemoryStore] = None,
        mutability_guard: Optional[MutabilityGuard] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the induction engine.
        
        Args:
            memory_store: MemoryStore instance (uses default if None)
            mutability_guard: MutabilityGuard instance (uses default if None)
            config: Configuration dictionary
        """
        self.memory = memory_store or get_memory_store()
        self.guard = mutability_guard or get_mutability_guard()
        self.config = config or self._default_config()
        
        # Track current session observations
        self._session_observations: List[ObservationEvent] = []
    
    def _default_config(self) -> dict:
        """Get default configuration."""
        return {
            "rejection_similarity_threshold": 0.9,
            "min_content_length": 10,
            "require_user_approval": True,
            "show_confidence": True,
            "show_source": True
        }
    
    # =========================================================================
    # Observation and Proposal
    # =========================================================================
    
    def observe(self, event: Dict[str, Any]) -> Optional[MemoryProposal]:
        """
        Observe an event and potentially create a proposal.
        
        Args:
            event: Dictionary with 'type' and 'content' keys at minimum.
                   Optional: 'context', 'session_id', 'metadata'
                   
        Returns:
            MemoryProposal if a proposal was created, None otherwise.
            Returns None if:
            - Content is too short
            - Similar to a rejected memory
            - Invalid observation type
            
        Example:
            >>> proposal = engine.observe({
            ...     "type": "user_correction",
            ...     "content": "Use pytest for testing"
            ... })
        """
        # Validate event structure
        if not isinstance(event, dict):
            logger.warning("Observation event must be a dictionary")
            return None
        
        event_type = event.get("type", "unknown")
        content = event.get("content", "")
        
        # Validate content
        if len(content) < self.config.get("min_content_length", 10):
            logger.debug(f"Content too short: {len(content)} chars")
            return None
        
        # Create observation event
        observation = ObservationEvent(
            type=event_type,
            content=content,
            context=event.get("context"),
            session_id=event.get("session_id"),
            metadata=event.get("metadata", {})
        )
        
        # Track observation
        self._session_observations.append(observation)
        
        # Check if similar to rejected
        if self._is_similar_to_rejected(content):
            logger.debug(f"Content similar to rejected memory, skipping")
            return None
        
        # Extract learning from observation
        learning = self._extract_learning(observation)
        
        # Determine scope and confidence
        type_config = OBSERVATION_TYPES.get(event_type, {})
        scope = type_config.get("scope", "global")
        confidence = type_config.get("confidence", 0.8)
        
        # Create proposal
        proposal = MemoryProposal(
            id=str(uuid.uuid4()),
            content=learning,
            source=event_type,
            scope=scope,
            status="pending",
            confidence=confidence,
            context=observation.context,
            timestamp=observation.timestamp
        )
        
        # Add to pending queue
        self.memory.add_pending_proposal(proposal)
        
        logger.info(f"Created proposal: {proposal.id} - {learning[:50]}...")
        
        return proposal
    
    def _extract_learning(self, observation: ObservationEvent) -> str:
        """
        Extract the learning from an observation.
        
        Cleans and normalizes the content for storage.
        """
        content = observation.content.strip()
        
        # Remove common prefixes that don't add value
        prefixes_to_remove = [
            "remember that ",
            "remember: ",
            "note: ",
            "note that ",
            "always ",
            "never ",
        ]
        
        content_lower = content.lower()
        for prefix in prefixes_to_remove:
            if content_lower.startswith(prefix):
                content = content[len(prefix):]
                break
        
        # Capitalize first letter
        if content:
            content = content[0].upper() + content[1:]
        
        return content
    
    def _is_similar_to_rejected(self, content: str) -> bool:
        """Check if content is similar to a rejected memory."""
        threshold = self.config.get("rejection_similarity_threshold", 0.9)
        return self.memory.is_similar_to_rejected(content, threshold)
    
    # =========================================================================
    # Proposal Management
    # =========================================================================
    
    def get_pending_proposals(self) -> List[MemoryProposal]:
        """
        Get all pending proposals.
        
        Returns:
            List of MemoryProposal objects awaiting approval.
        """
        return self.memory.get_pending_proposals()
    
    def accept_proposal(
        self, 
        proposal_id: str, 
        edited_content: Optional[str] = None
    ) -> Memory:
        """
        Accept a proposal and store it as semantic memory.
        
        Args:
            proposal_id: The proposal ID to accept.
            edited_content: Optional edited content if user modified.
            
        Returns:
            The created Memory object.
        """
        memory = self.memory.accept_proposal(proposal_id, edited_content)
        logger.info(f"Proposal accepted: {proposal_id}")
        return memory
    
    def reject_proposal(self, proposal_id: str) -> None:
        """
        Reject a proposal.
        
        The rejection is tracked to avoid re-proposing similar content.
        
        Args:
            proposal_id: The proposal ID to reject.
        """
        self.memory.reject_proposal(proposal_id)
        logger.info(f"Proposal rejected: {proposal_id}")
    
    def edit_and_accept_proposal(
        self, 
        proposal_id: str, 
        new_content: str
    ) -> Memory:
        """
        Edit a proposal's content and accept it.
        
        Args:
            proposal_id: The proposal ID to edit.
            new_content: The edited content.
            
        Returns:
            The created Memory object.
        """
        return self.accept_proposal(proposal_id, edited_content=new_content)
    
    # =========================================================================
    # Memory Retrieval
    # =========================================================================
    
    def get_relevant_memories(
        self, 
        query: str, 
        k: int = 5,
        include_episodic: bool = True
    ) -> List[Memory]:
        """
        Get memories relevant to a query.
        
        Args:
            query: Query text.
            k: Maximum number of results.
            include_episodic: Whether to include recent session observations.
            
        Returns:
            List of relevant Memory objects.
        """
        # Search semantic memory
        semantic_results = self.memory.search(query, "semantic", k=k, threshold=0.5)
        
        if include_episodic:
            # Also search episodic for recent observations
            episodic_results = self.memory.search(
                query, "episodic", k=k//2, threshold=0.5
            )
            return semantic_results + episodic_results
        
        return semantic_results
    
    def get_memory_context(self, query: str) -> str:
        """
        Get formatted memory context for a query.
        
        Args:
            query: Query text.
            
        Returns:
            Formatted string with relevant memories.
        """
        return self.memory.get_relevant_context(query)
    
    # =========================================================================
    # Session Management
    # =========================================================================
    
    def start_session(self, session_id: Optional[str] = None) -> str:
        """
        Start a new observation session.
        
        Args:
            session_id: Optional session ID (generates one if not provided).
            
        Returns:
            The session ID.
        """
        self._session_observations = []
        return session_id or str(uuid.uuid4())
    
    def end_session(self, store_episodic: bool = True) -> int:
        """
        End the current session.
        
        Args:
            store_episodic: Whether to store observations as episodic memories.
            
        Returns:
            Number of observations in the session.
        """
        count = len(self._session_observations)
        
        if store_episodic and self._session_observations:
            for observation in self._session_observations:
                self.memory.add_memory(
                    content=observation.content,
                    metadata={
                        "type": observation.type,
                        "context": observation.context,
                        "session_id": observation.session_id,
                        "timestamp": observation.timestamp
                    },
                    memory_type="episodic"
                )
        
        self._session_observations = []
        return count
    
    def get_session_observations(self) -> List[ObservationEvent]:
        """Get observations from the current session."""
        return self._session_observations.copy()
    
    # =========================================================================
    # Status and Utilities
    # =========================================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get engine status information."""
        return {
            "memory_stats": self.memory.get_stats(),
            "pending_proposals": len(self.get_pending_proposals()),
            "session_observations": len(self._session_observations),
            "config": self.config
        }
    
    def get_status_message(self) -> str:
        """Get human-readable status message."""
        pending = len(self.get_pending_proposals())
        memory_msg = self.memory.get_status_message()
        
        if pending > 0:
            return f"{memory_msg} You have {pending} learning proposals awaiting your approval."
        return memory_msg
    
    def format_proposal_for_display(self, proposal: MemoryProposal) -> str:
        """
        Format a proposal for display to the user.
        
        Args:
            proposal: The proposal to format.
            
        Returns:
            Formatted string for display in chat.
        """
        return proposal.format_for_user()


# Singleton instance for convenience
_default_engine: Optional[InductionEngine] = None


def get_induction_engine() -> InductionEngine:
    """
    Get or create the default induction engine instance.
    
    Returns:
        InductionEngine instance.
    """
    global _default_engine
    
    if _default_engine is None:
        _default_engine = InductionEngine()
    
    return _default_engine

def reset_induction_engine() -> None:
    """Reset the singleton instance (for testing)."""
    global _default_engine
    _default_engine = None
