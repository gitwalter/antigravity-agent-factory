"""
Tests for the society module.

Tests organizational patterns and communication protocols.
"""

from lib.society.society import (
    GovernanceModel,
    DecisionType,
    Role,
    Proposal,
    FlatDemocracy,
    Meritocracy,
    Hierarchy,
    Federation,
    DAOSociety,
    create_society,
    MessageType,
    Message,
    DirectProtocol,
    BroadcastProtocol,
    ConsensusProtocol,
    MessageRouter,
    create_message,
)
from lib.society.trust import ReputationSystem


class TestRole:
    """Tests for Role dataclass."""

    def test_create_role(self):
        """Test creating a role."""
        role = Role(
            name="admin",
            capabilities=["read", "write", "delete"],
            responsibilities=["manage_users"],
            trust_required=0.8,
        )

        assert role.name == "admin"
        assert len(role.capabilities) == 3

    def test_has_capability(self):
        """Test capability checking."""
        role = Role(name="worker", capabilities=["read", "execute"])

        assert role.has_capability("read")
        assert role.has_capability("execute")
        assert not role.has_capability("delete")

    def test_wildcard_capability(self):
        """Test wildcard capability."""
        role = Role(name="superadmin", capabilities=["*"])

        assert role.has_capability("anything")
        assert role.has_capability("delete")


class TestProposal:
    """Tests for Proposal dataclass."""

    def test_create_proposal(self):
        """Test creating a proposal."""
        proposal = Proposal(
            id="prop-1",
            proposer="agent-1",
            type=DecisionType.OPERATIONAL,
            description="Test proposal",
        )

        assert proposal.id == "prop-1"
        assert proposal.status == "open"

    def test_vote_count(self):
        """Test vote counting."""
        proposal = Proposal(
            id="prop-1",
            proposer="agent-1",
            type=DecisionType.OPERATIONAL,
            description="Test",
            votes={"a": True, "b": True, "c": False},
        )

        yes, no = proposal.vote_count
        assert yes == 2
        assert no == 1


class TestFlatDemocracy:
    """Tests for FlatDemocracy pattern."""

    def test_governance_model(self):
        """Test governance model type."""
        society = FlatDemocracy("Test Democracy")
        assert society.governance_model == GovernanceModel.FLAT_DEMOCRACY

    def test_add_member(self):
        """Test adding members."""
        society = FlatDemocracy()
        society.add_member("agent-1")
        society.add_member("agent-2")

        assert "agent-1" in society._members
        assert "agent-2" in society._members

    def test_equal_voting_weight(self):
        """Test that all members have equal weight."""
        society = FlatDemocracy()
        society.add_member("agent-1")
        society.add_member("agent-2")

        assert society.get_voting_weight("agent-1") == 1.0
        assert society.get_voting_weight("agent-2") == 1.0

    def test_create_proposal(self):
        """Test creating proposals."""
        society = FlatDemocracy()
        society.add_member("agent-1")

        proposal = society.create_proposal(
            "agent-1",
            DecisionType.OPERATIONAL,
            "Test proposal",
        )

        assert proposal is not None
        assert proposal.proposer == "agent-1"

    def test_vote_on_proposal(self):
        """Test voting on proposals."""
        society = FlatDemocracy()
        society.add_member("agent-1")
        society.add_member("agent-2")

        proposal = society.create_proposal(
            "agent-1",
            DecisionType.OPERATIONAL,
            "Test",
        )

        society.vote(proposal.id, "agent-1", True)
        society.vote(proposal.id, "agent-2", True)

        assert len(proposal.votes) == 2

    def test_evaluate_proposal_majority(self):
        """Test majority wins."""
        society = FlatDemocracy()
        society.add_member("a")
        society.add_member("b")
        society.add_member("c")

        proposal = society.create_proposal("a", DecisionType.OPERATIONAL, "Test")

        society.vote(proposal.id, "a", True)
        society.vote(proposal.id, "b", True)
        society.vote(proposal.id, "c", False)

        result = society.finalize_proposal(proposal.id)
        assert result is True  # 2 yes > 1 no


class TestMeritocracy:
    """Tests for Meritocracy pattern."""

    def test_governance_model(self):
        """Test governance model type."""
        society = Meritocracy("Test Meritocracy")
        assert society.governance_model == GovernanceModel.MERITOCRACY

    def test_reputation_weighted_voting(self):
        """Test reputation-weighted voting."""
        reputation = ReputationSystem(decay_enabled=False)
        reputation.get_score("high-rep").current_score = 90.0
        reputation.get_score("low-rep").current_score = 30.0

        society = Meritocracy(reputation_system=reputation)
        society.add_member("high-rep")
        society.add_member("low-rep")

        # High reputation = higher weight
        assert society.get_voting_weight("high-rep") > society.get_voting_weight(
            "low-rep"
        )


class TestHierarchy:
    """Tests for Hierarchy pattern."""

    def test_governance_model(self):
        """Test governance model type."""
        society = Hierarchy()
        assert society.governance_model == GovernanceModel.HIERARCHY

    def test_default_roles(self):
        """Test default roles are created."""
        society = Hierarchy()

        assert Hierarchy.LEADER_ROLE in society._roles
        assert Hierarchy.MANAGER_ROLE in society._roles
        assert Hierarchy.MEMBER_ROLE in society._roles

    def test_role_voting_weight(self):
        """Test role-based voting weight."""
        society = Hierarchy()
        society.add_member("leader")
        society.add_member("manager")
        society.add_member("member")

        society.assign_role("leader", Hierarchy.LEADER_ROLE)
        society.assign_role("manager", Hierarchy.MANAGER_ROLE)
        society.assign_role("member", Hierarchy.MEMBER_ROLE)

        assert society.get_voting_weight("leader") > society.get_voting_weight(
            "manager"
        )
        assert society.get_voting_weight("manager") > society.get_voting_weight(
            "member"
        )

    def test_leader_has_final_say(self):
        """Test that leader's vote decides."""
        society = Hierarchy()
        society.add_member("leader")
        society.add_member("m1")
        society.add_member("m2")

        society.assign_role("leader", Hierarchy.LEADER_ROLE)
        society.assign_role("m1", Hierarchy.MEMBER_ROLE)
        society.assign_role("m2", Hierarchy.MEMBER_ROLE)

        proposal = society.create_proposal("m1", DecisionType.OPERATIONAL, "Test")

        society.vote(proposal.id, "m1", True)
        society.vote(proposal.id, "m2", True)
        society.vote(proposal.id, "leader", False)  # Leader says no

        result = society.finalize_proposal(proposal.id)
        assert result is False  # Leader's no overrides majority


class TestFederation:
    """Tests for Federation pattern."""

    def test_governance_model(self):
        """Test governance model type."""
        society = Federation()
        assert society.governance_model == GovernanceModel.FEDERATION

    def test_create_sub_society(self):
        """Test creating sub-societies."""
        society = Federation()
        society.create_sub_society("group-a")
        society.create_sub_society("group-b")

        assert "group-a" in society._sub_societies
        assert "group-b" in society._sub_societies

    def test_add_to_sub_society(self):
        """Test adding members to sub-societies."""
        society = Federation()
        society.add_member("agent-1")
        society.create_sub_society("group-a")

        result = society.add_to_sub_society("agent-1", "group-a")
        assert result
        assert "agent-1" in society._sub_societies["group-a"]

    def test_representative_voting(self):
        """Test that representatives vote for groups."""
        society = Federation()

        # Set up two groups with representatives
        for agent in ["a1", "a2", "b1", "b2"]:
            society.add_member(agent)

        society.create_sub_society("group-a")
        society.create_sub_society("group-b")

        society.add_to_sub_society("a1", "group-a")
        society.add_to_sub_society("a2", "group-a")
        society.add_to_sub_society("b1", "group-b")
        society.add_to_sub_society("b2", "group-b")

        society.set_representative("group-a", "a1")
        society.set_representative("group-b", "b1")

        # Representatives should have higher weight
        assert society.get_voting_weight("a1") > society.get_voting_weight("a2")


class TestDAOSociety:
    """Tests for DAOSociety pattern."""

    def test_governance_model(self):
        """Test governance model type."""
        society = DAOSociety()
        assert society.governance_model == GovernanceModel.DAO

    def test_stake_based_voting(self):
        """Test stake-based voting weight."""
        society = DAOSociety()
        society.add_member("high-stake")
        society.add_member("low-stake")

        society.set_stake("high-stake", 100.0)
        society.set_stake("low-stake", 10.0)

        high_weight = society.get_voting_weight("high-stake")
        low_weight = society.get_voting_weight("low-stake")

        assert high_weight > low_weight

    def test_quorum_requirement(self):
        """Test quorum requirement."""
        society = DAOSociety()
        society.quorum = 0.5  # 50% must vote

        society.add_member("a")
        society.add_member("b")
        society.add_member("c")
        society.add_member("d")

        for member in ["a", "b", "c", "d"]:
            society.set_stake(member, 25.0)  # Equal stakes

        proposal = society.create_proposal("a", DecisionType.OPERATIONAL, "Test")

        # Only 1 vote (25%) - below quorum
        society.vote(proposal.id, "a", True)
        result = society.finalize_proposal(proposal.id)

        assert result is False  # Failed due to quorum


class TestCreateSociety:
    """Tests for create_society factory function."""

    def test_create_flat_democracy(self):
        """Test creating flat democracy."""
        society = create_society(GovernanceModel.FLAT_DEMOCRACY, "Demo")
        assert isinstance(society, FlatDemocracy)

    def test_create_meritocracy(self):
        """Test creating meritocracy."""
        society = create_society(GovernanceModel.MERITOCRACY, "Merit")
        assert isinstance(society, Meritocracy)

    def test_create_hierarchy(self):
        """Test creating hierarchy."""
        society = create_society(GovernanceModel.HIERARCHY, "Hier")
        assert isinstance(society, Hierarchy)

    def test_create_federation(self):
        """Test creating federation."""
        society = create_society(GovernanceModel.FEDERATION, "Fed")
        assert isinstance(society, Federation)

    def test_create_dao(self):
        """Test creating DAO."""
        society = create_society(GovernanceModel.DAO, "DAO")
        assert isinstance(society, DAOSociety)


class TestMessage:
    """Tests for Message dataclass."""

    def test_create_message(self):
        """Test creating a message."""
        msg = Message(
            id="msg-1",
            type=MessageType.REQUEST,
            sender="agent-1",
            recipients=["agent-2"],
            content={"action": "test"},
        )

        assert msg.id == "msg-1"
        assert msg.type == MessageType.REQUEST

    def test_is_broadcast(self):
        """Test broadcast detection."""
        broadcast = Message(
            id="msg-1",
            type=MessageType.BROADCAST,
            sender="agent-1",
            recipients=[],
            content={},
        )
        assert broadcast.is_broadcast

        direct = Message(
            id="msg-2",
            type=MessageType.REQUEST,
            sender="agent-1",
            recipients=["agent-2"],
            content={},
        )
        assert not direct.is_broadcast

    def test_compute_hash(self):
        """Test message hash computation."""
        msg = Message(
            id="msg-1",
            type=MessageType.REQUEST,
            sender="agent-1",
            content={"data": "test"},
        )

        hash1 = msg.compute_hash()
        hash2 = msg.compute_hash()

        assert len(hash1) == 64
        assert hash1 == hash2


class TestDirectProtocol:
    """Tests for DirectProtocol."""

    def test_send_and_receive(self):
        """Test sending and receiving messages."""
        protocol = DirectProtocol()
        protocol.register_agent("sender")
        protocol.register_agent("receiver")

        msg = create_message(
            sender="sender",
            content={"hello": "world"},
            recipients=["receiver"],
        )

        protocol.send(msg)

        messages = protocol.receive("receiver")
        assert len(messages) == 1
        assert messages[0].content["hello"] == "world"

    def test_receive_clears_queue(self):
        """Test that receive clears the queue."""
        protocol = DirectProtocol()
        protocol.register_agent("agent")

        msg = create_message(
            sender="other",
            content={},
            recipients=["agent"],
        )
        protocol.send(msg)

        # First receive gets the message
        assert len(protocol.receive("agent")) == 1

        # Second receive is empty
        assert len(protocol.receive("agent")) == 0


class TestBroadcastProtocol:
    """Tests for BroadcastProtocol."""

    def test_subscribe_and_receive(self):
        """Test subscribing and receiving broadcasts."""
        protocol = BroadcastProtocol()
        protocol.subscribe("agent-1", "news")
        protocol.subscribe("agent-2", "news")

        msg = create_message(
            sender="publisher",
            content={"topic": "news", "data": "Hello"},
            message_type=MessageType.BROADCAST,
        )

        protocol.send(msg)

        messages = protocol.receive("agent-1")
        assert len(messages) > 0


class TestConsensusProtocol:
    """Tests for ConsensusProtocol."""

    def test_propose_and_vote(self):
        """Test proposing and voting."""
        protocol = ConsensusProtocol()
        protocol.add_participant("a")
        protocol.add_participant("b")
        protocol.add_participant("c")

        round_id = protocol.propose("a", "topic", "value")
        assert round_id is not None

        # All 3 vote yes for acceptance (quorum is 0.67, need > 2/3 of 3 = 2.01)
        protocol.vote(round_id, "a", True)
        protocol.vote(round_id, "b", True)
        protocol.vote(round_id, "c", True)

        status, value = protocol.get_result(round_id)
        assert status == "accepted"  # Unanimous passes quorum


class TestMessageRouter:
    """Tests for MessageRouter."""

    def test_register_and_route(self):
        """Test registering protocols and routing."""
        router = MessageRouter()
        direct = DirectProtocol()
        direct.register_agent("receiver")

        router.register_protocol(direct, default=True)

        msg = create_message(
            sender="sender",
            content={"test": True},
            recipients=["receiver"],
        )

        result = router.route(msg)
        assert result
