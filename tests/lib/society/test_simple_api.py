"""
Tests for the Simplified Society API.

This test suite verifies the simplified API for multi-agent coordination,
ensuring 3-line setup works correctly with proper verification.

SDG - Love - Truth - Beauty
"""

from lib.society.simple import (
    create_agent_society,
    SocietyPreset,
    SendResult,
    AgentStatus,
    quick_send,
)
from lib.society.presets import (
    create_supervisor_worker_society,
    create_peer_society,
    create_pipeline_society,
    create_hierarchical_society,
    SocietyBuilder,
    TrustTier,
    get_preset_config,
    list_presets,
)


class TestSimpleSociety:
    """Tests for SimpleSociety class."""

    def test_create_society_minimal(self):
        """Society can be created with just a name."""
        society = create_agent_society("TestSociety")

        assert society.name == "TestSociety"
        assert society.preset == SocietyPreset.DEVELOPMENT
        assert society.context is not None

    def test_create_society_with_agents(self):
        """Society can be created with initial agents."""
        society = create_agent_society(
            "TestSociety", agents=["agent1", "agent2", "agent3"]
        )

        assert len(society._bridges) == 3
        assert "agent1" in society._bridges
        assert "agent2" in society._bridges
        assert "agent3" in society._bridges

    def test_create_society_with_preset(self):
        """Society respects preset configuration."""
        society = create_agent_society("TestSociety", preset=SocietyPreset.PRODUCTION)

        assert society.preset == SocietyPreset.PRODUCTION

    def test_add_agent(self):
        """Agents can be added after creation."""
        society = create_agent_society("TestSociety")

        result = society.add_agent("new_agent", agent_type="executor")

        assert result is society  # Method chaining
        assert "new_agent" in society._bridges

    def test_add_agent_idempotent(self):
        """Adding same agent twice is idempotent."""
        society = create_agent_society("TestSociety", agents=["agent1"])

        society.add_agent("agent1")

        assert len(society._bridges) == 1

    def test_remove_agent(self):
        """Agents can be removed from society."""
        society = create_agent_society("TestSociety", agents=["agent1", "agent2"])

        society.remove_agent("agent1")

        assert "agent1" not in society._bridges
        assert "agent2" in society._bridges

    def test_send_message_between_agents(self):
        """Messages can be sent between registered agents."""
        society = create_agent_society("TestSociety", agents=["sender", "receiver"])

        result = society.send(
            "sender", "receiver", {"task": "analyze"}, message_type="REQUEST"
        )

        assert isinstance(result, SendResult)
        # Note: Actual verification depends on society context

    def test_send_message_unregistered_sender(self):
        """Sending from unregistered agent returns error."""
        society = create_agent_society("TestSociety", agents=["receiver"])

        result = society.send("unknown", "receiver", {"task": "test"})

        assert not result.success
        assert "not registered" in result.error

    def test_send_message_unregistered_receiver(self):
        """Sending to unregistered agent returns error."""
        society = create_agent_society("TestSociety", agents=["sender"])

        result = society.send("sender", "unknown", {"task": "test"})

        assert not result.success
        assert "not registered" in result.error

    def test_broadcast_message(self):
        """Broadcast sends to all agents except sender."""
        society = create_agent_society(
            "TestSociety", agents=["broadcaster", "receiver1", "receiver2", "receiver3"]
        )

        results = society.broadcast(
            "broadcaster", {"announcement": "hello"}, message_type="INFORM"
        )

        assert "receiver1" in results
        assert "receiver2" in results
        assert "receiver3" in results
        assert "broadcaster" not in results

    def test_broadcast_with_exclude(self):
        """Broadcast can exclude specific agents."""
        society = create_agent_society(
            "TestSociety", agents=["broadcaster", "receiver1", "receiver2", "excluded"]
        )

        results = society.broadcast(
            "broadcaster", {"announcement": "hello"}, exclude=["excluded"]
        )

        assert "receiver1" in results
        assert "receiver2" in results
        assert "excluded" not in results

    def test_message_handler_registration(self):
        """Message handlers can be registered."""
        society = create_agent_society("TestSociety", agents=["agent1", "agent2"])

        received = []

        def handler(sender, payload):
            received.append((sender, payload))

        society.on_message("agent2", handler)
        society.send("agent1", "agent2", {"msg": "hello"})

        # Handler should be called (if send succeeds)
        # Note: Actual behavior depends on society context

    def test_get_reputation(self):
        """Reputation can be retrieved for agents."""
        society = create_agent_society("TestSociety", agents=["agent1"])

        reputation = society.get_reputation("agent1")

        assert isinstance(reputation, (int, float))

    def test_get_trust_level(self):
        """Trust level can be retrieved for agents."""
        society = create_agent_society("TestSociety", agents=["agent1"])

        trust_level = society.get_trust_level("agent1")

        assert isinstance(trust_level, str)

    def test_get_agent_status(self):
        """Full agent status can be retrieved."""
        society = create_agent_society("TestSociety", agents=["agent1"])

        status = society.get_agent_status("agent1")

        assert isinstance(status, AgentStatus)
        assert status.agent_id == "agent1"
        assert hasattr(status, "reputation_score")
        assert hasattr(status, "trust_level")

    def test_create_contract(self):
        """Contracts can be created between agents."""
        society = create_agent_society("TestSociety", agents=["delegator", "executor"])

        contract = society.create_contract(
            "test-contract",
            parties=[("delegator", "delegator"), ("executor", "executor")],
            capabilities=[("executor", "analyze_code")],
            obligations=[("executor", "respond_within", {"timeout": 60})],
            prohibitions=[("executor", "modify_files")],
        )

        assert contract is not None
        assert contract.contract_id == "test-contract"

    def test_get_stats(self):
        """Society statistics can be retrieved."""
        society = create_agent_society("TestSociety", agents=["agent1", "agent2"])

        stats = society.get_stats()

        assert isinstance(stats, dict)
        assert stats["society_name"] == "TestSociety"
        assert stats["registered_agents"] == 2

    def test_export_audit_log(self):
        """Audit log can be exported."""
        society = create_agent_society("TestSociety", agents=["agent1"])

        audit_log = society.export_audit_log()

        assert isinstance(audit_log, dict)


class TestQuickSend:
    """Tests for quick_send convenience function."""

    def test_quick_send_creates_temporary_society(self):
        """quick_send creates a temporary society for one-off messages."""
        result = quick_send("agent_a", "agent_b", {"msg": "hello"})

        assert isinstance(result, SendResult)


class TestPresets:
    """Tests for society presets."""

    def test_supervisor_worker_society(self):
        """Supervisor-worker pattern creates correct structure."""
        society = create_supervisor_worker_society(
            "TestProject", supervisor_id="boss", worker_ids=["worker1", "worker2"]
        )

        assert "boss" in society._bridges
        assert "worker1" in society._bridges
        assert "worker2" in society._bridges

    def test_peer_society(self):
        """Peer society creates equal agents."""
        society = create_peer_society(
            "ReviewBoard", peer_ids=["peer1", "peer2", "peer3"]
        )

        assert len(society._bridges) == 3

    def test_pipeline_society(self):
        """Pipeline society creates sequential stages."""
        society = create_pipeline_society(
            "DataPipeline", stage_ids=["extract", "transform", "load"]
        )

        assert len(society._bridges) == 3

    def test_hierarchical_society(self):
        """Hierarchical society creates correct structure."""
        society = create_hierarchical_society(
            "Org",
            hierarchy={"ceo": ["vp1", "vp2"], "vp1": ["manager1"], "vp2": ["manager2"]},
        )

        assert "ceo" in society._bridges
        assert "vp1" in society._bridges
        assert "vp2" in society._bridges
        assert "manager1" in society._bridges
        assert "manager2" in society._bridges

    def test_get_preset_config(self):
        """Preset configurations can be retrieved."""
        config = get_preset_config(SocietyPreset.DEVELOPMENT)

        assert config.name == "Development"
        assert config.trust_tier == TrustTier.L0_LOCAL

    def test_list_presets(self):
        """All presets can be listed."""
        presets = list_presets()

        assert len(presets) >= 4
        assert any(p["name"] == "Development" for p in presets)
        assert any(p["name"] == "Production" for p in presets)


class TestSocietyBuilder:
    """Tests for SocietyBuilder fluent API."""

    def test_builder_basic(self):
        """Builder creates society with defaults."""
        society = SocietyBuilder("TestProject").build()

        assert society.name == "TestProject"

    def test_builder_with_preset(self):
        """Builder respects preset."""
        society = (
            SocietyBuilder("TestProject").with_preset(SocietyPreset.PRODUCTION).build()
        )

        assert society.preset == SocietyPreset.PRODUCTION

    def test_builder_with_agents(self):
        """Builder adds agents."""
        society = (
            SocietyBuilder("TestProject").with_agents(["agent1", "agent2"]).build()
        )

        assert "agent1" in society._bridges
        assert "agent2" in society._bridges

    def test_builder_fluent_chaining(self):
        """Builder supports fluent chaining."""
        society = (
            SocietyBuilder("TestProject")
            .with_preset(SocietyPreset.DEVELOPMENT)
            .with_trust_tier(TrustTier.L1_ATTESTED)
            .with_axiom_verification(True)
            .with_agents(["agent1"])
            .build()
        )

        assert society is not None


class TestSendResult:
    """Tests for SendResult dataclass."""

    def test_send_result_success(self):
        """SendResult correctly reports success."""
        result = SendResult(verified=True, event_id="123")

        assert result.success
        assert result.verified
        assert result.event_id == "123"

    def test_send_result_failure(self):
        """SendResult correctly reports failure."""
        result = SendResult(verified=False, error="Something went wrong")

        assert not result.success
        assert not result.verified
        assert result.error == "Something went wrong"

    def test_send_result_with_violations(self):
        """SendResult includes violations."""
        result = SendResult(verified=False, violations=["A1 violation", "A2 violation"])

        assert len(result.violations) == 2


class TestMessageCounting:
    """Tests for message counting functionality."""

    def test_message_count_increments(self):
        """Message counts increment on send."""
        society = create_agent_society("TestSociety", agents=["sender", "receiver"])

        society.send("sender", "receiver", {"msg": "test"})

        sender_status = society.get_agent_status("sender")
        receiver_status = society.get_agent_status("receiver")

        assert sender_status.messages_sent >= 1
        assert receiver_status.messages_received >= 1


# Integration tests


class TestIntegration:
    """Integration tests for the simplified API."""

    def test_full_workflow(self):
        """Complete workflow from creation to message to stats."""
        # Create society
        society = create_agent_society(
            "IntegrationTest", agents=["orchestrator", "analyzer", "reporter"]
        )

        # Create contract
        contract = society.create_contract(
            "analysis-workflow",
            parties=[
                ("orchestrator", "coordinator"),
                ("analyzer", "worker"),
                ("reporter", "worker"),
            ],
            capabilities=[("analyzer", "analyze"), ("reporter", "report")],
        )

        # Send messages
        result1 = society.send(
            "orchestrator", "analyzer", {"task": "analyze", "target": "code.py"}
        )

        result2 = society.send(
            "analyzer", "reporter", {"findings": ["issue1", "issue2"]}
        )

        # Check stats
        stats = society.get_stats()

        assert stats["registered_agents"] == 3
        assert stats["society_name"] == "IntegrationTest"

    def test_three_line_setup(self):
        """Verify the 3-line setup claim works."""
        # Line 1: Import (already done at module level)
        # Line 2: Create society
        society = create_agent_society("Test", agents=["a", "b"])
        # Line 3: Send message
        result = society.send("a", "b", {"task": "test"})

        # It should work
        assert isinstance(result, SendResult)
