"""
Tests for the Induction Engine.

Tests user-validated learning and proposal workflow.
"""

import pytest
import tempfile
import shutil

# Check if qdrant-client is available
try:
    import qdrant_client

    HAS_QDRANT = True
except ImportError:
    HAS_QDRANT = False

pytestmark = pytest.mark.skipif(not HAS_QDRANT, reason="qdrant-client not installed")


class TestInductionEngine:
    """Tests for InductionEngine class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test data."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def engine(self, temp_dir):
        """Create an induction engine with temp storage."""
        from scripts.memory.memory_store import MemoryStore
        from scripts.memory.induction_engine import InductionEngine

        store = MemoryStore(persist_dir=temp_dir)
        return InductionEngine(memory_store=store)

    def test_engine_initialization(self, engine):
        """Test that engine initializes correctly."""
        assert engine.memory is not None
        assert engine.guard is not None
        assert len(engine.get_pending_proposals()) == 0

    def test_observe_creates_proposal(self, engine):
        """Test that observation creates a proposal."""
        proposal = engine.observe(
            {
                "type": "user_correction",
                "content": "Use pytest instead of unittest for testing",
            }
        )

        assert proposal is not None
        assert "pytest" in proposal.content.lower()
        assert proposal.status == "pending"

    def test_observe_returns_none_for_short_content(self, engine):
        """Test that short content is rejected."""
        proposal = engine.observe(
            {
                "type": "user_correction",
                "content": "hi",  # Too short
            }
        )

        assert proposal is None

    def test_proposal_requires_user_approval(self, engine):
        """Verify memories are not stored without approval."""
        proposal = engine.observe(
            {"type": "user_correction", "content": "Use pytest for Python testing"}
        )

        # Memory should be in pending state
        pending = engine.get_pending_proposals()
        assert len(pending) == 1

        # Memory should NOT be in stored state yet
        memories = engine.get_relevant_memories("pytest", k=5)
        semantic_memories = [m for m in memories if m.memory_type == "semantic"]
        assert len(semantic_memories) == 0

    def test_accepted_proposal_is_stored(self, engine):
        """Verify accepted proposals are stored correctly."""
        proposal = engine.observe(
            {"type": "user_correction", "content": "Use pytest for all Python testing"}
        )

        # Accept the proposal
        memory = engine.accept_proposal(proposal.id)

        assert memory is not None
        assert memory.memory_type == "semantic"

        # Should now be searchable
        results = engine.memory.search("pytest", "semantic", k=5)
        assert len(results) >= 1

    def test_rejected_proposal_not_re_proposed(self, engine):
        """Verify rejected memories are not proposed again."""
        # First observation
        proposal = engine.observe(
            {"type": "user_correction", "content": "Use unittest for Python testing"}
        )

        # Reject it
        engine.reject_proposal(proposal.id)

        # Similar observation should not create new proposal
        proposal2 = engine.observe(
            {
                "type": "user_correction",
                "content": "Use unittest for testing Python code",
            }
        )

        # Should return None because similar to rejected
        assert proposal2 is None

    def test_edit_and_accept_proposal(self, engine):
        """Test editing a proposal before accepting."""
        proposal = engine.observe({"type": "user_correction", "content": "Use pytest"})

        # Edit and accept
        memory = engine.edit_and_accept_proposal(
            proposal.id, "Always use pytest with fixtures for Python testing"
        )

        assert "fixtures" in memory.content

    def test_different_observation_types(self, engine):
        """Test different types of observations."""
        # User correction
        p1 = engine.observe(
            {"type": "user_correction", "content": "Use black for code formatting"}
        )
        assert p1.source == "user_correction"
        assert p1.confidence == 0.95

        engine.reject_proposal(p1.id)  # Clean up

        # Explicit teaching
        p2 = engine.observe(
            {
                "type": "explicit_teaching",
                "content": "Always add type hints to function signatures",
            }
        )
        assert p2.source == "explicit_teaching"
        assert p2.confidence == 1.0

    def test_get_status(self, engine):
        """Test status reporting."""
        engine.observe(
            {"type": "user_correction", "content": "Test observation for status check"}
        )

        status = engine.get_status()

        assert "memory_stats" in status
        assert "pending_proposals" in status
        assert status["pending_proposals"] == 1

    def test_get_status_message(self, engine):
        """Test human-readable status message."""
        # Empty engine
        message = engine.get_status_message()
        assert "memories" in message.lower()

        # With pending proposal
        engine.observe(
            {"type": "user_correction", "content": "Test for status message"}
        )

        message = engine.get_status_message()
        assert "proposal" in message.lower() or "approval" in message.lower()


class TestInductionEngineSession:
    """Tests for session management."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test data."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def engine(self, temp_dir):
        """Create an induction engine."""
        from scripts.memory.memory_store import MemoryStore
        from scripts.memory.induction_engine import InductionEngine

        store = MemoryStore(persist_dir=temp_dir)
        return InductionEngine(memory_store=store)

    def test_start_session(self, engine):
        """Test starting a new session."""
        session_id = engine.start_session()

        assert session_id is not None
        assert len(engine.get_session_observations()) == 0

    def test_session_tracks_observations(self, engine):
        """Test that observations are tracked in session."""
        engine.start_session()

        engine.observe(
            {"type": "user_correction", "content": "First observation in session"}
        )
        engine.observe(
            {"type": "preference", "content": "Second observation in session"}
        )

        observations = engine.get_session_observations()
        assert len(observations) == 2

    def test_end_session_stores_episodic(self, engine):
        """Test ending session stores episodic memories."""
        engine.start_session()

        engine.observe(
            {"type": "user_correction", "content": "Session observation to store"}
        )

        count = engine.end_session(store_episodic=True)

        assert count == 1

        # Should be in episodic memory
        stats = engine.memory.get_stats()
        assert stats["episodic_count"] >= 1

    def test_end_session_clears_observations(self, engine):
        """Test ending session clears observation list."""
        engine.start_session()

        engine.observe({"type": "user_correction", "content": "Observation to clear"})

        engine.end_session()

        assert len(engine.get_session_observations()) == 0


class TestInductionEngineSingleton:
    """Tests for the singleton pattern."""

    def test_get_induction_engine_returns_instance(self, tmp_path):
        """Test singleton returns an instance."""
        from scripts.memory.induction_engine import (
            get_induction_engine,
            reset_induction_engine,
        )
        from scripts.memory.memory_store import reset_memory_store, get_memory_store

        # Reset singletons
        reset_induction_engine()
        reset_memory_store()

        try:
            # Initialize memory store with temp dir first (so induction engine uses it)
            temp_persist = str(tmp_path / "induction_singleton")
            get_memory_store(persist_dir=temp_persist)

            # Get engine
            engine = get_induction_engine()
            assert engine is not None

            # Second call should return same instance
            engine2 = get_induction_engine()
            assert engine2 is engine

        finally:
            reset_induction_engine()
            reset_memory_store()
