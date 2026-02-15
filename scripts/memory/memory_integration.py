"""
Memory Integration Hooks for Skills and Agents

Provides integration points for connecting the memory system
with existing Factory skills and agents.

Integration Points:
    - extend-knowledge: Query memory before creating new knowledge
    - pattern-feedback: Store observations for learning
    - knowledge-evolution: Use memory for update decisions

Usage:
    from scripts.memory.memory_integration import MemoryIntegration

    integration = MemoryIntegration()

    # Before creating knowledge
    context = integration.get_context_for_knowledge_creation("topic")

    # Record an observation
    proposal = integration.record_observation("user_correction", "content")

    # Get pending proposals for user
    proposals = integration.get_pending_for_approval()
"""

import logging
from typing import List, Optional, Dict, Any

from scripts.memory.memory_store import Memory, MemoryProposal
from scripts.memory.induction_engine import InductionEngine, get_induction_engine
from scripts.guardian.mutability_guard import MutabilityGuard, get_mutability_guard

logger = logging.getLogger(__name__)


class MemoryIntegration:
    """
    Integration layer connecting memory system with Factory skills.

    Provides high-level methods for skills and agents to interact
    with the memory system.

    Attributes:
        engine: InductionEngine instance
        guard: MutabilityGuard instance

    Example:
        >>> integration = MemoryIntegration()
        >>> context = integration.get_context_for_task("Python testing")
        >>> print(context)  # Relevant memories
    """

    def __init__(
        self,
        induction_engine: Optional[InductionEngine] = None,
        mutability_guard: Optional[MutabilityGuard] = None,
    ):
        """
        Initialize the integration layer.

        Args:
            induction_engine: InductionEngine instance (uses default if None)
            mutability_guard: MutabilityGuard instance (uses default if None)
        """
        self.engine = induction_engine or get_induction_engine()
        self.guard = mutability_guard or get_mutability_guard()

    # =========================================================================
    # Context Retrieval (for extend-knowledge skill)
    # =========================================================================

    def get_context_for_knowledge_creation(self, topic: str) -> str:
        """
        Get relevant context before creating new knowledge.

        Used by extend-knowledge skill to avoid duplicating existing knowledge.

        Args:
            topic: The topic being extended.

        Returns:
            Formatted context string with relevant memories.
        """
        # Get existing memories about the topic
        memories = self.engine.get_relevant_memories(topic, k=5)

        if not memories:
            return ""

        lines = ["**Existing Knowledge (from memory):**"]
        for memory in memories:
            similarity = memory.metadata.get("similarity", 0)
            source = memory.metadata.get("source", "memory")
            lines.append(
                f"- {memory.content} [Source: {source}, Relevance: {similarity * 100:.0f}%]"
            )

        lines.append("\n*Consider this existing knowledge when creating new content.*")

        return "\n".join(lines)

    def get_context_for_task(self, task_description: str) -> str:
        """
        Get relevant context for a general task.

        Args:
            task_description: Description of the current task.

        Returns:
            Formatted context string.
        """
        return self.engine.get_memory_context(task_description)

    def check_knowledge_exists(self, topic: str, threshold: float = 0.8) -> bool:
        """
        Check if knowledge about a topic already exists.

        Args:
            topic: Topic to check.
            threshold: Similarity threshold.

        Returns:
            True if similar knowledge exists.
        """
        memories = self.engine.get_relevant_memories(topic, k=1)

        if memories:
            similarity = memories[0].metadata.get("similarity", 0)
            return similarity >= threshold

        return False

    # =========================================================================
    # Observation Recording (for pattern-feedback skill)
    # =========================================================================

    def record_observation(
        self,
        observation_type: str,
        content: str,
        context: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[MemoryProposal]:
        """
        Record an observation that might become a memory.

        Used by pattern-feedback skill and agents to capture learning opportunities.

        Args:
            observation_type: Type of observation (user_correction, explicit_teaching, etc.)
            content: The content to potentially remember.
            context: Optional context about the observation.
            metadata: Optional additional metadata.

        Returns:
            MemoryProposal if a proposal was created, None otherwise.
        """
        event = {
            "type": observation_type,
            "content": content,
            "context": context,
            "metadata": metadata or {},
        }

        return self.engine.observe(event)

    def record_user_correction(
        self, original: str, correction: str
    ) -> Optional[MemoryProposal]:
        """
        Record when user corrects the agent.

        Args:
            original: What the agent originally said/did.
            correction: What the user corrected it to.

        Returns:
            MemoryProposal if created.
        """
        content = f"Use {correction} instead of {original}"
        return self.record_observation(
            "user_correction", content, context=f"Original: {original}"
        )

    def record_teaching(self, teaching: str) -> Optional[MemoryProposal]:
        """
        Record when user explicitly teaches something.

        Args:
            teaching: What the user taught.

        Returns:
            MemoryProposal if created.
        """
        return self.record_observation("explicit_teaching", teaching)

    def record_preference(self, preference: str) -> Optional[MemoryProposal]:
        """
        Record a detected user preference.

        Args:
            preference: The detected preference.

        Returns:
            MemoryProposal if created.
        """
        return self.record_observation("preference", preference)

    # =========================================================================
    # Proposal Management (for user interaction)
    # =========================================================================

    def get_pending_for_approval(self) -> List[MemoryProposal]:
        """
        Get all pending proposals for user approval.

        Returns:
            List of MemoryProposal objects.
        """
        return self.engine.get_pending_proposals()

    def format_proposals_for_display(self) -> str:
        """
        Format all pending proposals for display.

        Returns:
            Formatted string with all proposals.
        """
        proposals = self.get_pending_for_approval()

        if not proposals:
            return "No pending learning proposals."

        lines = [f"**{len(proposals)} Learning Proposals Awaiting Approval:**\n"]

        for i, proposal in enumerate(proposals, 1):
            lines.append(f"### Proposal {i}")
            lines.append(proposal.format_for_user())
            lines.append("")

        return "\n".join(lines)

    def approve_proposal(
        self, proposal_id: str, edited_content: Optional[str] = None
    ) -> Memory:
        """
        Approve a proposal (called when user accepts).

        Args:
            proposal_id: The proposal ID to approve.
            edited_content: Optional edited content.

        Returns:
            The created Memory object.
        """
        return self.engine.accept_proposal(proposal_id, edited_content)

    def reject_proposal(self, proposal_id: str) -> None:
        """
        Reject a proposal (called when user rejects).

        Args:
            proposal_id: The proposal ID to reject.
        """
        self.engine.reject_proposal(proposal_id)

    def approve_all_pending(self) -> int:
        """
        Approve all pending proposals.

        Returns:
            Number of proposals approved.
        """
        proposals = self.get_pending_for_approval()
        count = 0

        for proposal in proposals:
            try:
                self.approve_proposal(proposal.id)
                count += 1
            except Exception as e:
                logger.warning(f"Failed to approve proposal {proposal.id}: {e}")

        return count

    def reject_all_pending(self) -> int:
        """
        Reject all pending proposals.

        Returns:
            Number of proposals rejected.
        """
        proposals = self.get_pending_for_approval()
        count = 0

        for proposal in proposals:
            try:
                self.reject_proposal(proposal.id)
                count += 1
            except Exception as e:
                logger.warning(f"Failed to reject proposal {proposal.id}: {e}")

        return count

    # =========================================================================
    # Path Protection (for knowledge modification)
    # =========================================================================

    def can_modify_path(self, path: str) -> bool:
        """
        Check if a path can be modified by the memory system.

        Args:
            path: Path to check.

        Returns:
            True if modification is allowed.
        """
        result = self.guard.can_modify(path)
        return result.allowed

    def get_protection_reason(self, path: str) -> str:
        """
        Get the reason why a path is protected.

        Args:
            path: Path to check.

        Returns:
            Explanation string.
        """
        result = self.guard.can_modify(path)
        return result.reason

    # =========================================================================
    # Status and Utilities
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """
        Get integration status.

        Returns:
            Status dictionary.
        """
        return {
            "engine_status": self.engine.get_status(),
            "pending_proposals": len(self.get_pending_for_approval()),
            "memory_available": not self.engine.memory.is_empty,
        }

    def get_status_message(self) -> str:
        """
        Get human-readable status message.

        Returns:
            Status message string.
        """
        return self.engine.get_status_message()

    def get_memory_summary(self) -> str:
        """
        Get a summary of all stored memories.

        Returns:
            Formatted summary string.
        """
        stats = self.engine.memory.get_stats()

        lines = ["**Memory System Summary:**"]
        lines.append(f"- Semantic memories: {stats['semantic_count']}")
        lines.append(f"- Episodic observations: {stats['episodic_count']}")
        lines.append(f"- Pending proposals: {stats['pending_count']}")
        lines.append(f"- Rejected (tracked): {stats['rejected_count']}")

        return "\n".join(lines)


# Singleton instance for convenience
_default_integration: Optional[MemoryIntegration] = None


def get_memory_integration() -> MemoryIntegration:
    """
    Get or create the default integration instance.

    Returns:
        MemoryIntegration instance.
    """
    global _default_integration

    if _default_integration is None:
        _default_integration = MemoryIntegration()

    return _default_integration
