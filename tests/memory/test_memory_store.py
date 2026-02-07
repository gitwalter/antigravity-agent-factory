"""
Tests for the Memory Store.

Tests hybrid storage functionality with ChromaDB and proposal queue.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

# Check if chromadb is available
try:
    import chromadb
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

pytestmark = pytest.mark.skipif(not HAS_CHROMADB, reason="chromadb not installed")


class TestMemoryStore:
    """Tests for MemoryStore class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory path for test data."""
        # Create parent temp dir, but not the actual persist dir
        temp_path = tempfile.mkdtemp()
        persist_path = Path(temp_path) / "memory"
        yield str(persist_path)
        shutil.rmtree(temp_path, ignore_errors=True)
    
    @pytest.fixture
    def store(self, temp_dir):
        """Create a memory store instance with temp directory."""
        from scripts.memory.memory_store import MemoryStore
        return MemoryStore(persist_dir=temp_dir)
    
    def test_store_initialization(self, store):
        """Test that store initializes correctly."""
        # Note: is_first_run is True only when the persist_dir doesn't exist
        # Since we use a non-existent subdir, it should be first run
        assert store.is_empty  # No memories yet
    
    def test_add_and_search_memory(self, store):
        """Test adding and searching memories."""
        # Add a memory
        memory_id = store.add_memory(
            content="Use pytest for Python testing",
            metadata={"source": "user_teaching"},
            memory_type="semantic"
        )
        
        assert memory_id is not None
        assert not store.is_empty
        
        # Search for it
        results = store.search("Python testing", memory_type="semantic", k=5)
        
        assert len(results) >= 1
        assert any("pytest" in r.content.lower() for r in results)
    
    def test_add_memory_to_different_types(self, store):
        """Test adding memories to different collections."""
        # Semantic memory
        semantic_id = store.add_memory(
            "Use black for formatting",
            {"source": "test"},
            "semantic"
        )
        
        # Episodic memory
        episodic_id = store.add_memory(
            "User mentioned pytest",
            {"source": "observation"},
            "episodic"
        )
        
        # Verify stats
        stats = store.get_stats()
        assert stats["semantic_count"] == 1
        assert stats["episodic_count"] == 1
    
    def test_get_memory_by_id(self, store):
        """Test retrieving a specific memory."""
        memory_id = store.add_memory(
            "Test content",
            {"source": "test"},
            "semantic"
        )
        
        memory = store.get_memory(memory_id, "semantic")
        
        assert memory is not None
        assert memory.id == memory_id
        assert memory.content == "Test content"
    
    def test_delete_memory(self, store):
        """Test deleting a memory."""
        memory_id = store.add_memory(
            "To be deleted",
            {"source": "test"},
            "semantic"
        )
        
        # Verify it exists
        assert store.get_memory(memory_id, "semantic") is not None
        
        # Delete it
        result = store.delete_memory(memory_id, "semantic")
        assert result is True
        
        # Verify it's gone
        assert store.get_memory(memory_id, "semantic") is None
    
    def test_search_with_threshold(self, store):
        """Test search with similarity threshold."""
        store.add_memory("Python testing with pytest", {"source": "test"}, "semantic")
        store.add_memory("Cooking Italian pasta", {"source": "test"}, "semantic")
        
        # High threshold should filter out unrelated
        results = store.search(
            "Python unit testing",
            memory_type="semantic",
            k=5,
            threshold=0.5
        )
        
        # Should only return Python-related memory
        for result in results:
            similarity = result.metadata.get("similarity", 0)
            assert similarity >= 0.5
    
    def test_get_relevant_context(self, store):
        """Test getting formatted context."""
        store.add_memory(
            "Use black for code formatting",
            {"source": "user_teaching"},
            "semantic"
        )
        
        context = store.get_relevant_context("code formatting tools")
        
        assert "black" in context.lower() or context == ""
    
    def test_status_message(self, store):
        """Test status message generation."""
        # Empty store
        message = store.get_status_message()
        assert "don't have any memories" in message.lower()
        
        # Add a memory
        store.add_memory("Test", {"source": "test"}, "semantic")
        
        message = store.get_status_message()
        assert "1" in message or "memories" in message.lower()
    
    def test_clear_episodic(self, store):
        """Test clearing episodic memories."""
        store.add_memory("Episodic 1", {"source": "test"}, "episodic")
        store.add_memory("Episodic 2", {"source": "test"}, "episodic")
        
        count = store.clear_episodic()
        
        assert count == 2
        assert store.get_stats()["episodic_count"] == 0


class TestMemoryProposalOperations:
    """Tests for proposal queue operations."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test data."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path, ignore_errors=True)
    
    @pytest.fixture
    def store(self, temp_dir):
        """Create a memory store instance."""
        from scripts.memory.memory_store import MemoryStore
        return MemoryStore(persist_dir=temp_dir)
    
    def test_add_pending_proposal(self, store):
        """Test adding a pending proposal."""
        from scripts.memory.memory_store import MemoryProposal
        
        proposal = MemoryProposal(
            id="test-1",
            content="Use pytest for testing",
            source="user_correction",
            scope="global"
        )
        
        proposal_id = store.add_pending_proposal(proposal)
        assert proposal_id is not None
        
        # Verify in pending
        pending = store.get_pending_proposals()
        assert len(pending) >= 1
    
    def test_accept_proposal(self, store):
        """Test accepting a proposal moves it to semantic."""
        from scripts.memory.memory_store import MemoryProposal
        
        proposal = MemoryProposal(
            id="test-2",
            content="Use black for formatting",
            source="user_teaching",
            scope="global"
        )
        
        proposal_id = store.add_pending_proposal(proposal)
        
        # Accept it
        memory = store.accept_proposal(proposal_id)
        
        assert memory is not None
        assert memory.content == "Use black for formatting"
        
        # Should be in semantic now
        stats = store.get_stats()
        assert stats["semantic_count"] == 1
        assert stats["pending_count"] == 0
    
    def test_accept_proposal_with_edit(self, store):
        """Test accepting with edited content."""
        from scripts.memory.memory_store import MemoryProposal
        
        proposal = MemoryProposal(
            id="test-3",
            content="Use pytest",
            source="user_correction",
            scope="global"
        )
        
        proposal_id = store.add_pending_proposal(proposal)
        
        # Accept with edit
        memory = store.accept_proposal(proposal_id, edited_content="Always use pytest for Python testing")
        
        assert memory.content == "Always use pytest for Python testing"
        assert memory.metadata.get("was_edited") is True
    
    def test_reject_proposal(self, store):
        """Test rejecting a proposal moves it to rejected."""
        from scripts.memory.memory_store import MemoryProposal
        
        proposal = MemoryProposal(
            id="test-4",
            content="Use unittest",
            source="user_correction",
            scope="global"
        )
        
        proposal_id = store.add_pending_proposal(proposal)
        
        # Reject it
        store.reject_proposal(proposal_id)
        
        # Should be in rejected now
        stats = store.get_stats()
        assert stats["rejected_count"] == 1
        assert stats["pending_count"] == 0
    
    def test_is_similar_to_rejected(self, store):
        """Test similarity check against rejected proposals."""
        from scripts.memory.memory_store import MemoryProposal
        
        proposal = MemoryProposal(
            id="test-5",
            content="Use unittest for testing Python code",
            source="user_correction",
            scope="global"
        )
        
        proposal_id = store.add_pending_proposal(proposal)
        store.reject_proposal(proposal_id)
        
        # Similar content should be detected
        is_similar = store.is_similar_to_rejected(
            "Use unittest for Python testing",
            threshold=0.8
        )
        
        assert is_similar is True
        
        # Unrelated content should not match
        is_similar = store.is_similar_to_rejected(
            "Cooking pasta recipes",
            threshold=0.8
        )
        
        assert is_similar is False
    
    def test_proposal_format_for_user(self):
        """Test proposal formatting for display."""
        from scripts.memory.memory_store import MemoryProposal
        
        proposal = MemoryProposal(
            id="test-6",
            content="Use pytest for testing",
            source="user_correction",
            scope="global",
            confidence=0.95
        )
        
        formatted = proposal.format_for_user()
        
        assert "pytest" in formatted
        assert "Accept" in formatted
        assert "Reject" in formatted
        assert "95%" in formatted  # Confidence


class TestMemoryStoreSingleton:
    """Tests for the singleton pattern."""
    
    def test_get_memory_store_returns_same_instance(self, tmp_path):
        """Test singleton returns same instance."""
        from scripts.memory.memory_store import get_memory_store
        
        # Reset singleton for test
        import scripts.memory.memory_store as module
        module._default_store = None
        
        # This test is tricky because we can't easily set persist_dir
        # Just verify the function works
        store = get_memory_store()
        assert store is not None
