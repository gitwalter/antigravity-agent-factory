"""
Automated Cognitive Memory System - Configuration
Defines endpoints, paths, and collection schemas across the dual-storage tier.
Ensures dynamic environment variable resolution for test isolation.
"""

import os
import sys
from pathlib import Path

# --- Platform Paths (Static) ---
USER_PROFILE = os.environ.get("USERPROFILE", str(Path.home()))
GEMINI_DIR = os.path.join(USER_PROFILE, ".gemini")

# --- Dynamic Lookup Functions ---


def get_sqlite_db_path() -> str:
    """Dynamically resolve the SQLite DB path from environment."""
    db_name = os.environ.get("ANTIGRAVITY_SQLITE_DB", "antigravity_memory.db")
    return os.environ.get("ANTIGRAVITY_SQLITE_PATH", os.path.join(GEMINI_DIR, db_name))


def get_qdrant_host() -> str:
    """Dynamically resolve Qdrant host."""
    return os.environ.get("QDRANT_HOST", "localhost")


def get_qdrant_port() -> int:
    """Dynamically resolve Qdrant port."""
    return int(os.environ.get("QDRANT_PORT", 6333))


def get_qdrant_path() -> str:
    """Dynamically resolve local Qdrant path."""
    return os.environ.get("QDRANT_PATH", None)


def get_collection_prefix() -> str:
    """Dynamically resolve collection prefix."""
    return os.environ.get("RAG_COLLECTION_PREFIX", "")


def get_collection_name(base_name: str) -> str:
    """Get the effective collection name with current prefix or override."""
    prefix = get_collection_prefix()
    override = os.environ.get("RAG_COLLECTION_OVERRIDE", None)

    if override and base_name not in ["episodic", "pending", "rejected"]:
        # Only override core semantic collections
        return override
    return f"{prefix}{base_name}"


# --- Collection Constants (Base Names) ---
# Note: These are base names. Prefixing happens via get_collection_name().
COLLECTION_SEMANTIC = "memory_semantic"
COLLECTION_PROCEDURAL = "memory_procedural"
COLLECTION_TOOLBOX = "memory_toolbox"
COLLECTION_ENTITY = "memory_entity"
COLLECTION_SUMMARY = "memory_summary"

VECTOR_SIZE_DEFAULT = 384
EMBEDDING_MODEL_DEFAULT = "all-MiniLM-L6-v2"


# --- Dynamic Attribute Bridge (Python 3.7+) ---
# This allows 'from memory_config import SQLITE_DB_PATH' to be dynamic
def __getattr__(name):
    if name == "SQLITE_DB_PATH":
        return get_sqlite_db_path()
    if name == "QDRANT_HOST":
        return get_qdrant_host()
    if name == "QDRANT_PORT":
        return get_qdrant_port()
    if name == "QDRANT_PATH":
        return get_qdrant_path()
    if name == "COLLECTION_PREFIX":
        return get_collection_prefix()
    if name == "VECTOR_SIZE":
        return int(os.environ.get("ANTIGRAVITY_VECTOR_SIZE", VECTOR_SIZE_DEFAULT))
    if name == "EMBEDDING_MODEL":
        return os.environ.get("ANTIGRAVITY_EMBEDDING_MODEL", EMBEDDING_MODEL_DEFAULT)

    if name in globals():
        return globals()[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
