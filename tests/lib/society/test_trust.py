"""
Tests for the trust module.

Tests identity, reputation, and trust delegation.
"""

import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

from lib.society.trust import (
    KeyPair,
    AgentIdentity,
    IdentityRegistry,
    ReputationType,
    ReputationEvent,
    ReputationScore,
    ReputationSystem,
    TrustDelegation,
    TrustGraph,
)


class TestKeyPair:
    """Tests for KeyPair."""

    def test_generate_keypair(self):
        """Test generating a key pair."""
        keypair = KeyPair.generate()

        assert keypair.private_key is not None
        assert keypair.public_key is not None
        assert keypair.private_key != keypair.public_key

    def test_sign_and_verify(self):
        """Test signing and verifying a message."""
        keypair = KeyPair.generate()
        message = b"Hello, World!"

        signature = keypair.sign(message)
        assert signature is not None

        # Should verify successfully
        is_valid = keypair.verify(message, signature)
        assert is_valid

    def test_verify_fails_for_wrong_message(self):
        """Test that verification fails for wrong message."""
        keypair = KeyPair.generate()

        signature = keypair.sign(b"Original message")
        is_valid = keypair.verify(b"Different message", signature)

        assert not is_valid

    def test_to_dict_without_private(self):
        """Test serialization without private key."""
        keypair = KeyPair.generate()
        data = keypair.to_dict(include_private=False)

        assert "public_key" in data
        assert "private_key" not in data

    def test_to_dict_with_private(self):
        """Test serialization with private key."""
        keypair = KeyPair.generate()
        data = keypair.to_dict(include_private=True)

        assert "public_key" in data
        assert "private_key" in data


class TestAgentIdentity:
    """Tests for AgentIdentity."""

    def test_create_identity(self):
        """Test creating an agent identity."""
        identity = AgentIdentity.create(name="TestAgent", agent_type="worker")

        assert identity.name == "TestAgent"
        assert identity.agent_id is not None
        assert len(identity.agent_id) == 16
        assert identity.metadata["type"] == "worker"

    def test_sign_message(self):
        """Test signing a message."""
        identity = AgentIdentity.create(name="Signer")

        signature = identity.sign("Test message")
        assert signature is not None

    def test_verify_signature(self):
        """Test verifying a signature."""
        identity = AgentIdentity.create(name="Signer")
        message = "Test message"

        signature = identity.sign(message)
        is_valid = identity.verify(message, signature)

        assert is_valid

    def test_sign_json(self):
        """Test signing JSON data."""
        identity = AgentIdentity.create(name="Signer")
        data = {"action": "test", "value": 42}

        signature = identity.sign_json(data)
        assert signature is not None

    def test_to_public_dict(self):
        """Test public serialization."""
        identity = AgentIdentity.create(name="Public")
        data = identity.to_public_dict()

        assert data["name"] == "Public"
        assert "public_key" in data
        assert "keypair" not in data

    def test_save_and_load(self):
        """Test saving and loading identity."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "identity.json"

            identity1 = AgentIdentity.create(name="Persistent")
            identity1.save(str(filepath))

            identity2 = AgentIdentity.load(str(filepath))

            assert identity2.agent_id == identity1.agent_id
            assert identity2.name == identity1.name
            assert identity2.public_key == identity1.public_key


class TestIdentityRegistry:
    """Tests for IdentityRegistry."""

    def test_register_identity(self):
        """Test registering an identity."""
        registry = IdentityRegistry()
        identity = AgentIdentity.create(name="Agent1")

        registry.register(identity)

        retrieved = registry.get(identity.agent_id)
        assert retrieved == identity

    def test_get_public_key(self):
        """Test getting public key."""
        registry = IdentityRegistry()
        identity = AgentIdentity.create(name="Agent1")
        registry.register(identity)

        public_key = registry.get_public_key(identity.agent_id)
        assert public_key == identity.public_key

    def test_verify_signature(self):
        """Test verifying signature through registry."""
        registry = IdentityRegistry()
        identity = AgentIdentity.create(name="Agent1")
        registry.register(identity)

        message = "Test message"
        signature = identity.sign(message)

        is_valid = registry.verify_signature(
            identity.agent_id,
            message,
            signature,
        )
        assert is_valid

    def test_list_agents(self):
        """Test listing registered agents."""
        registry = IdentityRegistry()

        id1 = AgentIdentity.create(name="Agent1")
        id2 = AgentIdentity.create(name="Agent2")

        registry.register(id1)
        registry.register(id2)

        agents = registry.list_agents()
        assert len(agents) == 2


class TestReputationScore:
    """Tests for ReputationScore."""

    def test_initial_score(self):
        """Test initial reputation score."""
        score = ReputationScore(agent_id="agent-1")

        assert score.current_score == 50.0
        assert score.trust_level == "medium"

    def test_add_positive_event(self):
        """Test adding positive reputation event."""
        score = ReputationScore(agent_id="agent-1")

        event = ReputationEvent(
            timestamp=datetime.now(timezone.utc),
            type=ReputationType.AXIOM_COMPLIANCE,
            delta=5.0,
            reason="Good behavior",
        )

        score.add_event(event)
        assert score.current_score == 55.0

    def test_add_negative_event(self):
        """Test adding negative reputation event."""
        score = ReputationScore(agent_id="agent-1")

        event = ReputationEvent(
            timestamp=datetime.now(timezone.utc),
            type=ReputationType.AXIOM_COMPLIANCE,
            delta=-10.0,
            reason="Violation",
        )

        score.add_event(event)
        assert score.current_score == 40.0

    def test_score_bounds(self):
        """Test that score stays within bounds."""
        score = ReputationScore(agent_id="agent-1", current_score=95.0)

        # Try to exceed max
        event = ReputationEvent(
            timestamp=datetime.now(timezone.utc),
            type=ReputationType.PEER_ENDORSEMENT,
            delta=20.0,
        )
        score.add_event(event)

        assert score.current_score == 100.0  # Capped at max

    def test_trust_levels(self):
        """Test trust level thresholds."""
        high = ReputationScore(agent_id="a", current_score=85.0)
        medium = ReputationScore(agent_id="b", current_score=60.0)
        low = ReputationScore(agent_id="c", current_score=30.0)
        untrusted = ReputationScore(agent_id="d", current_score=10.0)

        assert high.trust_level == "high"
        assert medium.trust_level == "medium"
        assert low.trust_level == "low"
        assert untrusted.trust_level == "untrusted"


class TestReputationSystem:
    """Tests for ReputationSystem."""

    def test_get_score_creates_default(self):
        """Test that get_score creates default for new agents."""
        system = ReputationSystem(decay_enabled=False)

        score = system.get_score("new-agent")

        assert score.agent_id == "new-agent"
        assert score.current_score == 50.0

    def test_record_compliance(self):
        """Test recording compliance."""
        system = ReputationSystem(decay_enabled=False)

        system.record_compliance("agent-1", True, "Good action")
        score = system.get_score("agent-1")

        assert score.current_score > 50.0

    def test_record_violation(self):
        """Test recording violation."""
        system = ReputationSystem(decay_enabled=False)

        system.record_compliance("agent-1", False, "Bad action")
        score = system.get_score("agent-1")

        assert score.current_score < 50.0

    def test_record_contract_event(self):
        """Test recording contract event."""
        system = ReputationSystem(decay_enabled=False)

        system.record_contract_event("agent-1", True, "contract-1")
        score = system.get_score("agent-1")

        assert score.current_score > 50.0

    def test_record_endorsement(self):
        """Test recording endorsement."""
        system = ReputationSystem(decay_enabled=False)

        # Set up endorser with high reputation
        system.get_score("endorser").current_score = 80.0

        system.record_endorsement("agent-1", "endorser", positive=True)
        score = system.get_score("agent-1")

        assert score.current_score > 50.0

    def test_get_trusted_agents(self):
        """Test getting trusted agents."""
        system = ReputationSystem(decay_enabled=False)

        # Create agents with different scores
        system.get_score("trusted").current_score = 75.0
        system.get_score("untrusted").current_score = 25.0

        trusted = system.get_trusted_agents(min_score=50.0)
        assert "trusted" in trusted
        assert "untrusted" not in trusted

    def test_get_rankings(self):
        """Test getting rankings."""
        system = ReputationSystem(decay_enabled=False)

        system.get_score("a").current_score = 80.0
        system.get_score("b").current_score = 60.0
        system.get_score("c").current_score = 90.0

        rankings = system.get_rankings(limit=3)

        assert rankings[0][0] == "c"  # Highest first
        assert rankings[1][0] == "a"
        assert rankings[2][0] == "b"


class TestTrustDelegation:
    """Tests for TrustDelegation."""

    def test_create_delegation(self):
        """Test creating a trust delegation."""
        delegation = TrustDelegation(
            delegator="alice",
            delegate="bob",
            trust_level=0.8,
            scope=["execute", "read"],
        )

        assert delegation.delegator == "alice"
        assert delegation.delegate == "bob"
        assert delegation.trust_level == 0.8

    def test_is_valid(self):
        """Test validity checking."""
        valid = TrustDelegation(
            delegator="a",
            delegate="b",
            trust_level=0.5,
        )
        assert valid.is_valid

        expired = TrustDelegation(
            delegator="a",
            delegate="b",
            trust_level=0.5,
            expires=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        assert not expired.is_valid

    def test_covers_scope(self):
        """Test scope coverage."""
        delegation = TrustDelegation(
            delegator="a",
            delegate="b",
            trust_level=0.5,
            scope=["execute", "read"],
        )

        assert delegation.covers_scope("execute")
        assert delegation.covers_scope("read")
        assert not delegation.covers_scope("delete")

    def test_wildcard_scope(self):
        """Test wildcard scope."""
        delegation = TrustDelegation(
            delegator="a",
            delegate="b",
            trust_level=0.5,
            scope=["*"],
        )

        assert delegation.covers_scope("anything")
        assert delegation.covers_scope("delete")


class TestTrustGraph:
    """Tests for TrustGraph."""

    def test_delegate_trust(self):
        """Test delegating trust."""
        graph = TrustGraph()

        delegation = graph.delegate_trust("alice", "bob", 0.8)

        assert delegation.delegator == "alice"
        assert delegation.delegate == "bob"
        assert delegation.trust_level == 0.8

    def test_get_direct_trust(self):
        """Test getting direct trust."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.8)

        trust = graph.get_direct_trust("alice", "bob")
        assert trust == 0.8

        # No delegation
        trust = graph.get_direct_trust("bob", "alice")
        assert trust == 0.0

    def test_revoke_trust(self):
        """Test revoking trust."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.8)

        revoked = graph.revoke_trust("alice", "bob")
        assert revoked

        trust = graph.get_direct_trust("alice", "bob")
        assert trust == 0.0

    def test_effective_trust_direct(self):
        """Test effective trust for direct delegation."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.8)

        trust = graph.get_effective_trust("alice", "bob")
        assert trust == 0.8

    def test_effective_trust_transitive(self):
        """Test transitive trust computation."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.9)
        graph.delegate_trust("bob", "charlie", 0.8)

        # Trust from alice to charlie via bob
        trust = graph.get_effective_trust("alice", "charlie")

        # Should be > 0 but < direct trust due to decay
        assert trust > 0.0
        assert trust < 0.9

    def test_find_trust_path(self):
        """Test finding trust path."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.9)
        graph.delegate_trust("bob", "charlie", 0.8)

        path = graph.find_trust_path("alice", "charlie")

        assert path is not None
        assert path == ["alice", "bob", "charlie"]

    def test_get_delegates(self):
        """Test getting delegates."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.8)
        graph.delegate_trust("alice", "charlie", 0.7)

        delegates = graph.get_delegates("alice")
        assert len(delegates) == 2

    def test_get_delegators(self):
        """Test getting delegators."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "charlie", 0.8)
        graph.delegate_trust("bob", "charlie", 0.7)

        delegators = graph.get_delegators("charlie")
        assert len(delegators) == 2

    def test_get_trust_network(self):
        """Test getting trust network."""
        graph = TrustGraph()
        graph.delegate_trust("alice", "bob", 0.8)
        graph.delegate_trust("bob", "charlie", 0.7)

        network = graph.get_trust_network("bob", depth=1)

        assert "bob" in network["nodes"]
        assert "alice" in network["nodes"]
        assert "charlie" in network["nodes"]
