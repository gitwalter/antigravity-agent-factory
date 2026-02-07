"""
Memory System for Antigravity Agent Factory

This module provides the inductive memory system that enables the Factory
to learn from experience through user-validated proposals.

Components:
    - EmbeddingService: Local embeddings using sentence-transformers
    - MemoryStore: Hybrid storage with ChromaDB + JSON
    - MemoryProposal: User-validated memory proposals
    - InductionEngine: Pattern recognition and learning

Architecture:
    - Semantic Memory: Long-term validated knowledge
    - Episodic Memory: Session-based observations
    - Pending: Proposals awaiting user approval
    - Rejected: Rejected proposals (to avoid re-proposing)

Usage:
    from scripts.memory import EmbeddingService, MemoryStore, InductionEngine
    
    # Initialize services
    embeddings = EmbeddingService()
    memory = MemoryStore()
    engine = InductionEngine(memory)
    
    # Observe and propose
    proposal = engine.observe({"type": "user_correction", "content": "Use pytest"})
    
    # User approves
    engine.accept_proposal(proposal.id)
"""

__version__ = "1.0.0"
__author__ = "Antigravity Agent Factory"

from pathlib import Path

# Memory module directory
MEMORY_DIR = Path(__file__).parent

# Default paths
DEFAULT_CONFIG_PATH = "knowledge/memory-config.json"
DEFAULT_PERSIST_DIR = "data/memory"
DEFAULT_MODEL_CACHE = "data/models"

# Import main classes
from scripts.memory.embedding_service import EmbeddingService, get_embedding_service
from scripts.memory.memory_store import (
    MemoryStore, 
    Memory, 
    MemoryProposal,
    get_memory_store
)
from scripts.memory.induction_engine import (
    InductionEngine,
    ObservationEvent,
    get_induction_engine
)
from scripts.memory.memory_integration import (
    MemoryIntegration,
    get_memory_integration
)

# Re-export main classes
__all__ = [
    # Classes
    "EmbeddingService",
    "MemoryStore", 
    "Memory",
    "MemoryProposal",
    "InductionEngine",
    "ObservationEvent",
    "MemoryIntegration",
    # Factory functions
    "get_embedding_service",
    "get_memory_store",
    "get_induction_engine",
    "get_memory_integration",
    # Constants
    "MEMORY_DIR",
    "DEFAULT_CONFIG_PATH",
    "DEFAULT_PERSIST_DIR",
    "DEFAULT_MODEL_CACHE",
]
