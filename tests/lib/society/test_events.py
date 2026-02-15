"""
Tests for the events module.

Tests event sourcing, hash chains, and event storage.
"""

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from lib.society.events import (
    Agent,
    AgentType,
    Action,
    ActionType,
    AxiomContext,
    AgentEvent,
    EventStore,
    HashChain,
    verify_chain_integrity,
)


class TestAgent:
    """Tests for Agent dataclass."""

    def test_create_agent(self):
        """Test creating an agent."""
        agent = Agent(
            id="agent-1",
            type=AgentType.WORKER,
            public_key="test_public_key_123",
            name="TestAgent",
        )

        assert agent.id == "agent-1"
        assert agent.name == "TestAgent"
        assert agent.type == AgentType.WORKER
        assert agent.public_key == "test_public_key_123"

    def test_agent_to_dict(self):
        """Test agent serialization."""
        agent = Agent(
            id="agent-1",
            type=AgentType.GUARDIAN,
            public_key="test_public_key_123",
            name="TestAgent",
        )
        data = agent.to_dict()

        assert data["id"] == "agent-1"
        assert data["name"] == "TestAgent"
        assert data["type"] == "guardian"
        assert data["public_key"] == "test_public_key_123"


class TestAction:
    """Tests for Action dataclass."""

    def test_create_action(self):
        """Test creating an action."""
        action = Action(
            type=ActionType.DECISION,
            description="Run a task",
            payload={"task": "test"},
        )

        assert action.type == ActionType.DECISION
        assert action.description == "Run a task"
        assert action.payload["task"] == "test"

    def test_action_to_dict(self):
        """Test action serialization."""
        action = Action(type=ActionType.MESSAGE, description="Send message")
        data = action.to_dict()

        assert data["type"] == "message"
        assert data["description"] == "Send message"


class TestAgentEvent:
    """Tests for AgentEvent dataclass."""

    def create_sample_event(self) -> AgentEvent:
        """Create a sample event for testing."""
        return AgentEvent(
            event_id="evt-1",
            timestamp=datetime(2026, 2, 5, 12, 0, 0),
            sequence=0,
            previous_hash="",
            agent=Agent(
                id="agent-1",
                type=AgentType.WORKER,
                public_key="test_public_key_123",
                name="Test",
            ),
            action=Action(type=ActionType.DECISION, description="Test action"),
            axiom_context=AxiomContext(
                declared_alignment=["A1"],
                justification="Follows love axiom",
            ),
            signature="",
            hash="",
        )

    def test_create_event(self):
        """Test creating an event."""
        event = self.create_sample_event()

        assert event.event_id == "evt-1"
        assert event.agent.id == "agent-1"
        assert event.action.type == ActionType.DECISION
        assert "A1" in event.axiom_context.declared_alignment

    def test_event_to_canonical_json(self):
        """Test canonical JSON serialization."""
        event = self.create_sample_event()
        json_str = event.to_canonical_json()

        # Should be valid JSON
        data = json.loads(json_str)
        assert data["event_id"] == "evt-1"

        # Canonical JSON should be deterministic
        json_str2 = event.to_canonical_json()
        assert json_str == json_str2

    def test_event_compute_hash(self):
        """Test event hash computation."""
        event = self.create_sample_event()
        hash1 = event.compute_hash()

        # Hash is sha256 prefixed: "sha256:<64 hex chars>" = 71 chars
        assert hash1.startswith("sha256:")
        assert len(hash1) == 71

        # Same event should produce same hash
        hash2 = event.compute_hash()
        assert hash1 == hash2

    def test_event_different_hash_for_different_events(self):
        """Test that different events have different hashes."""
        event1 = self.create_sample_event()
        event2 = AgentEvent(
            event_id="evt-2",
            timestamp=datetime(2026, 2, 5, 12, 0, 0),
            sequence=0,
            previous_hash="",
            agent=Agent(
                id="agent-1",
                type=AgentType.WORKER,
                public_key="test_public_key_123",
                name="Test",
            ),
            action=Action(type=ActionType.DECISION, description="Different action"),
            axiom_context=AxiomContext(),
            signature="",
            hash="",
        )

        assert event1.compute_hash() != event2.compute_hash()


class TestHashChain:
    """Tests for HashChain."""

    def test_compute_event_hash(self):
        """Test computing event hash."""
        event = AgentEvent(
            event_id="evt-1",
            timestamp=datetime.now(timezone.utc),
            sequence=1,  # First event has sequence 1
            previous_hash="",
            agent=Agent(id="a1", type=AgentType.WORKER, public_key="pk_test"),
            action=Action(type=ActionType.DECISION, description="Test"),
            axiom_context=AxiomContext(),
            signature="",
            hash="",
        )

        hash_val = HashChain.compute_event_hash(event)
        assert hash_val.startswith("sha256:")
        assert len(hash_val) == 71

    def test_verify_chain_link(self):
        """Test verifying chain links."""
        # Create first event (sequence 1 for genesis)
        event1 = AgentEvent(
            event_id="evt-1",
            timestamp=datetime.now(timezone.utc),
            sequence=1,
            previous_hash="",  # Genesis has empty previous
            agent=Agent(id="a1", type=AgentType.WORKER, public_key="pk_test"),
            action=Action(type=ActionType.DECISION, description="First"),
            axiom_context=AxiomContext(),
            signature="",
            hash="",
        )
        # Compute and set the hash
        event1_hash = event1.compute_hash()
        # Create event1 with proper hash set
        event1 = AgentEvent(
            event_id="evt-1",
            timestamp=event1.timestamp,
            sequence=1,
            previous_hash="",
            agent=event1.agent,
            action=event1.action,
            axiom_context=AxiomContext(),
            signature="",
            hash=event1_hash,
        )

        # Create second event (sequence 2)
        event2 = AgentEvent(
            event_id="evt-2",
            timestamp=datetime.now(timezone.utc),
            sequence=2,
            previous_hash=event1.hash,
            agent=Agent(id="a1", type=AgentType.WORKER, public_key="pk_test"),
            action=Action(type=ActionType.DECISION, description="Second"),
            axiom_context=AxiomContext(),
            signature="",
            hash="",
        )
        event2_hash = event2.compute_hash()
        event2 = AgentEvent(
            event_id="evt-2",
            timestamp=event2.timestamp,
            sequence=2,
            previous_hash=event1.hash,
            agent=event2.agent,
            action=event2.action,
            axiom_context=AxiomContext(),
            signature="",
            hash=event2_hash,
        )

        # Verify chain link - verify_chain_link returns (valid, error) tuple
        is_valid, error = HashChain.verify_chain_link(event2, event1)
        assert is_valid, f"Chain link should be valid: {error}"


class TestEventStore:
    """Tests for EventStore."""

    def create_agent(self, agent_id: str = "agent-1") -> Agent:
        """Create a test agent."""
        return Agent(id=agent_id, type=AgentType.WORKER, public_key="pk_test")

    def create_action(self, description: str = "Test action") -> Action:
        """Create a test action."""
        return Action(type=ActionType.DECISION, description=description)

    def test_append_event(self):
        """Test appending events using store.append()."""
        store = EventStore()
        agent = self.create_agent()
        action = self.create_action()

        # append() takes agent and action, creates and returns event
        event = store.append(agent, action)

        assert store.count == 1
        retrieved = store.get(event.event_id)
        assert retrieved is not None
        assert retrieved.agent.id == "agent-1"

    def test_append_sets_sequence(self):
        """Test that append sets sequence numbers (starting from 1)."""
        store = EventStore()
        agent = self.create_agent()

        event1 = store.append(agent, self.create_action("First"))
        event2 = store.append(agent, self.create_action("Second"))

        # Sequence starts at 1 for genesis event
        assert event1.sequence == 1
        assert event2.sequence == 2

    def test_append_sets_previous_hash(self):
        """Test that append sets previous hash for chain linking."""
        store = EventStore()
        agent = self.create_agent()

        event1 = store.append(agent, self.create_action("First"))
        event2 = store.append(agent, self.create_action("Second"))

        # First event has empty previous_hash (genesis)
        assert event1.previous_hash == ""
        # Second event links to first
        assert event2.previous_hash == event1.hash

    def test_query_by_agent(self):
        """Test querying events by agent using EventQuery."""
        from lib.society.events import EventQuery

        store = EventStore()
        agent1 = self.create_agent("agent-1")
        agent2 = self.create_agent("agent-2")

        store.append(agent1, self.create_action("Action 1"))
        store.append(agent2, self.create_action("Action 2"))
        store.append(agent1, self.create_action("Action 3"))

        # Use EventQuery to filter by agent
        query = EventQuery(agent_id="agent-1")
        events = store.query(query)
        assert len(events) == 2
        assert all(e.agent.id == "agent-1" for e in events)

    def test_chain_integrity(self):
        """Test chain integrity via verify_chain_integrity function."""
        store = EventStore()
        agent = self.create_agent()

        for i in range(5):
            store.append(agent, self.create_action(f"Action {i}"))

        # Use verify_chain_integrity function with store.events property
        result = verify_chain_integrity(store.events)
        assert result.valid

    def test_persistence(self):
        """Test automatic persistence via storage_path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "events.json"

            # Create store with storage path - it auto-saves on append
            store1 = EventStore(storage_path=str(filepath))
            agent = self.create_agent()
            evt1 = store1.append(agent, self.create_action("First"))
            evt2 = store1.append(agent, self.create_action("Second"))

            # Create new store that auto-loads from same path
            store2 = EventStore(storage_path=str(filepath))

            assert store2.count == 2
            assert store2.get(evt1.event_id) is not None
            assert store2.get(evt2.event_id) is not None


class TestVerifyChainIntegrity:
    """Tests for chain integrity verification."""

    def test_verify_empty_chain(self):
        """Test verifying empty chain."""
        result = verify_chain_integrity([])
        assert result.valid

    def test_verify_single_event(self):
        """Test verifying single event chain (sequence=1 for genesis)."""
        # Create event with sequence 1 (first event)
        event = AgentEvent(
            event_id="evt-1",
            timestamp=datetime.now(timezone.utc),
            sequence=1,  # Genesis event is sequence 1
            previous_hash="",
            agent=Agent(id="a1", type=AgentType.WORKER, public_key="pk_test"),
            action=Action(type=ActionType.DECISION, description="Test"),
            axiom_context=AxiomContext(),
            signature="",
            hash="",
        )
        # Compute hash and recreate with proper hash set
        computed_hash = event.compute_hash()
        event = AgentEvent(
            event_id="evt-1",
            timestamp=event.timestamp,
            sequence=1,
            previous_hash="",
            agent=event.agent,
            action=event.action,
            axiom_context=AxiomContext(),
            signature="",
            hash=computed_hash,
        )

        result = verify_chain_integrity([event])
        assert result.valid, f"Chain should be valid: {result.error_message}"

    def test_verify_valid_chain(self):
        """Test verifying valid chain using EventStore which handles chaining."""
        store = EventStore()
        agent = Agent(id="a1", type=AgentType.WORKER, public_key="pk_test")

        for i in range(3):
            action = Action(type=ActionType.DECISION, description=f"Action {i}")
            store.append(agent, action)

        # Use store.events property to get all events
        result = verify_chain_integrity(store.events)
        assert result.valid
