"""
Governance Gates for the SSGM Framework
Provides ReadFilteringGate and WriteValidationGate to enforce
relevance, stability, and safety in the memory system.
"""

import math
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from scripts.memory.memory_store import Memory, MemoryProposal

from scripts.api.llm_config import chat_with_aisuite

logger = logging.getLogger(__name__)

# --- Axioms for Governance ---
AXIOMS = """
- A1-Verifiability: All knowledge must be traceable to logs or verifiable sources.
- A2-User Primacy: User intent and safety always take precedence.
- A3-Transparency: Memory operations must be logged and explainable.
- A4-Non-Harm: Prevent learning of dangerous or malicious patterns.
- A5-Consistency: New memories must not contradict established Layer 0-2 principles.
"""


def weibull_decay(
    last_accessed: datetime,
    current_time: datetime,
    alpha: float = 1.0,
    beta: float = 0.5,
) -> float:
    """
    Implements Weibull decay for memory relevance.
    R(t) = exp(-(t/alpha)^beta)
    """
    dt = (current_time - last_accessed).total_seconds() / (24 * 3600)  # Time in days
    return math.exp(-pow(dt / alpha, beta))


class ReadFilteringGate:
    """
    Filters memory retrieval based on intent and temporal relevance.
    """

    def __init__(self, relevance_threshold: float = 0.1):
        self.relevance_threshold = relevance_threshold

    def filter_memories(
        self, query: str, memories: List[Memory], current_intent: Optional[str] = None
    ) -> List[Memory]:
        """
        Filters and ranks memories using temporal decay and LLM intent-awareness.
        """
        if not memories:
            return []

        now = datetime.now()
        decayed_memories = []

        # 1. First Pass: Temporal Decay (Heuristic)
        for memory in memories:
            last_accessed_str = (
                memory.metadata.get("last_accessed") or memory.created_at
            )
            try:
                last_accessed = datetime.fromisoformat(last_accessed_str)
                relevance = weibull_decay(last_accessed, now)
            except Exception:
                relevance = 1.0

            if relevance >= self.relevance_threshold:
                memory.metadata["relevance_score"] = relevance
                decayed_memories.append(memory)

        if not decayed_memories or not current_intent:
            return decayed_memories

        # 2. Second Pass: LLM Intent Pruning (Cognitive)
        try:
            memory_context = "\n".join(
                [f"[{m.id}] {m.content}" for m in decayed_memories[:10]]
            )  # Limit to top 10 for latency
            prompt = f"""
            You are the Antigravity Memory Governor.
            User Intent: {current_intent}
            User Query: {query}

            Candidate Memories:
            {memory_context}

            Identify which memory IDs are TRULY RELEVANT and NECESSARY to fulfill this request.
            Ignore memories that are redundant, outdated, or semantically close but contextually irrelevant.
            Return ONLY a comma-separated list of IDs.
            """

            response = chat_with_aisuite([{"role": "user", "content": prompt}])
            relevant_ids = [rid.strip() for rid in response["content"].split(",")]

            # Filter based on LLM recommendation
            final_memories = [m for m in decayed_memories if m.id in relevant_ids]
            return (
                final_memories if final_memories else decayed_memories
            )  # Fallback to heuristic if LLM filters everything
        except Exception as e:
            logger.warning(
                f"LLM Intent Pruning failed: {e}. Falling back to heuristic filtering."
            )
            return decayed_memories


class WriteValidationGate:
    """
    Validates memory proposals for safety, consistency, and stability using LLM.
    """

    def __init__(self, permanent_knowledge: Optional[List[Dict[str, Any]]] = None):
        self.permanent_knowledge = permanent_knowledge or []

    def validate_proposal(self, proposal: MemoryProposal) -> bool:
        """
        Validates a proposal against core axioms using LLM reasoning.
        """
        # 1. Heuristic Safety Check (Fast)
        unsafe_keywords = ["disable security", "ignore axioms", "skip validation"]
        if any(kw in proposal.content.lower() for kw in unsafe_keywords):
            logger.error(
                f"Safety violation (Heuristic) in proposal: {proposal.content}"
            )
            return False

        # 2. Axiomatic Consistency Check (LLM)
        try:
            prompt = f"""
            You are the Antigravity Integrity Governor.
            Core Axioms:
            {AXIOMS}

            Memory Proposal:
            Source: {proposal.source}
            Content: {proposal.content}
            Confidence: {proposal.confidence}

            Does this proposal violate any Core Axioms or introduce dangerous inconsistencies?
            Analyze carefully. If it's safe and consistent, return 'APPROVED'.
            Otherwise, return 'REJECTED: [Reason]'.
            """

            response = chat_with_aisuite([{"role": "user", "content": prompt}])
            decision = response["content"].upper()

            if "APPROVED" in decision:
                return True
            else:
                logger.warning(f"Proposal rejected by Axiomatic Gate: {decision}")
                return False
        except Exception as e:
            logger.warning(
                f"Axiomatic validation failed: {e}. Falling back to heuristic-only mode."
            )
            return True  # In elective mode, we allow if heuristics passed
