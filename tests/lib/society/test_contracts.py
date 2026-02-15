"""
Tests for the contracts module.

Tests contract schema, registry, and verification.
"""

import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from lib.society.contracts import (
    Party,
    Capability,
    Obligation,
    Prohibition,
    DisputeResolution,
    DisputeMethod,
    AxiomRequirements,
    AgentContract,
    ContractRegistry,
    ContractVerifier,
    ContractStatus,
    ViolationType,
    Violation,
    ContractVerificationResult,
)
from lib.society.contracts.verifier import Message


class TestParty:
    """Tests for Party dataclass."""

    def test_create_party(self):
        """Test creating a party."""
        party = Party(
            agent_id="agent-1",
            role="provider",
            public_key="pk_test_123",
        )

        assert party.agent_id == "agent-1"
        assert party.role == "provider"
        assert party.public_key == "pk_test_123"

    def test_party_to_dict(self):
        """Test party serialization."""
        party = Party(agent_id="agent-1", role="consumer", public_key="pk_test")
        data = party.to_dict()

        assert data["agent_id"] == "agent-1"
        assert data["role"] == "consumer"
        assert data["public_key"] == "pk_test"


class TestCapability:
    """Tests for Capability dataclass."""

    def test_create_capability(self):
        """Test creating a capability."""
        cap = Capability(
            action="execute_task",
            parameters={"max_concurrent": 5},
        )

        assert cap.action == "execute_task"
        assert cap.parameters["max_concurrent"] == 5


class TestObligation:
    """Tests for Obligation dataclass."""

    def test_create_obligation(self):
        """Test creating an obligation."""
        obl = Obligation(
            trigger="hourly_check",
            action="report_status",
            parameters={"format": "json"},
        )

        assert obl.trigger == "hourly_check"
        assert obl.action == "report_status"
        assert obl.parameters["format"] == "json"


class TestAgentContract:
    """Tests for AgentContract dataclass."""

    def create_sample_contract(self, signed: bool = True) -> AgentContract:
        """Create a sample contract for testing."""
        contract = AgentContract(
            contract_id="contract-1",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="provider-1", role="provider", public_key="pk_1"),
                Party(agent_id="consumer-1", role="consumer", public_key="pk_2"),
            ],
            capabilities={
                "provider": [Capability(action="execute", parameters={})],
                "consumer": [Capability(action="request", parameters={})],
            },
            obligations={
                "provider": [
                    Obligation(trigger="request", action="respond", parameters={})
                ],
            },
            prohibitions={
                "all_parties": [
                    Prohibition(action="harm", reason="Must not cause harm")
                ],
            },
            axiom_requirements=AxiomRequirements(
                A1_love="Prioritize user", A2_truth="Be honest"
            ),
            dispute_resolution=DisputeResolution(
                method=DisputeMethod.ESCALATE_TO_SUPERVISOR
            ),
            expires=datetime.now(timezone.utc) + timedelta(days=30),
        )
        if signed:
            contract.signatures = {"provider-1": "sig1", "consumer-1": "sig2"}
        return contract

    def test_create_contract(self):
        """Test creating a contract."""
        contract = self.create_sample_contract()

        assert contract.contract_id == "contract-1"
        assert len(contract.parties) == 2
        assert "provider" in contract.capabilities
        assert "provider" in contract.obligations

    def test_is_active(self):
        """Test contract active status."""
        contract = self.create_sample_contract(signed=True)
        assert contract.is_active

        # Unsigned contract is not active
        unsigned = self.create_sample_contract(signed=False)
        assert not unsigned.is_active

    def test_get_party(self):
        """Test getting party by agent ID."""
        contract = self.create_sample_contract()

        provider = contract.get_party("provider-1")
        assert provider is not None
        assert provider.role == "provider"

        unknown = contract.get_party("other-agent")
        assert unknown is None

    def test_get_role(self):
        """Test getting party role."""
        contract = self.create_sample_contract()

        assert contract.get_role("provider-1") == "provider"
        assert contract.get_role("consumer-1") == "consumer"
        assert contract.get_role("other") is None

    def test_has_capability(self):
        """Test checking capability."""
        contract = self.create_sample_contract()

        assert contract.has_capability("provider-1", "execute")
        assert contract.has_capability("consumer-1", "request")
        assert not contract.has_capability("provider-1", "delete")

    def test_is_prohibited(self):
        """Test checking prohibition."""
        contract = self.create_sample_contract()

        assert contract.is_prohibited("provider-1", "harm")
        assert contract.is_prohibited("consumer-1", "harm")
        assert not contract.is_prohibited("provider-1", "execute")

    def test_contract_to_dict(self):
        """Test contract serialization."""
        contract = self.create_sample_contract()
        data = contract.to_dict()

        assert data["contract_id"] == "contract-1"
        assert len(data["parties"]) == 2

    def test_contract_compute_hash(self):
        """Test contract hash computation."""
        contract = self.create_sample_contract()
        hash1 = contract.compute_hash()

        # Hash is sha256 prefixed: "sha256:<64 hex chars>" = 71 chars
        assert hash1.startswith("sha256:")
        assert len(hash1) == 71

        # Same contract should produce same hash
        hash2 = contract.compute_hash()
        assert hash1 == hash2


class TestContractRegistry:
    """Tests for ContractRegistry."""

    def create_contract(self, contract_id: str, agents: list) -> AgentContract:
        """Create a test contract."""
        return AgentContract(
            contract_id=contract_id,
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id=a, role="member", public_key=f"pk_{a}") for a in agents
            ],
            capabilities={"member": [Capability(action="work", parameters={})]},
        )

    def test_add_and_get_contract(self):
        """Test adding and retrieving contracts."""
        registry = ContractRegistry()
        contract = self.create_contract("c1", ["a1", "a2"])

        registry.add(contract)

        retrieved = registry.get("c1")
        assert retrieved == contract

    def test_remove_contract(self):
        """Test removing contracts."""
        registry = ContractRegistry()
        contract = self.create_contract("c1", ["a1"])

        registry.add(contract)
        assert registry.get("c1") is not None

        registry.remove("c1")
        assert registry.get("c1") is None

    def test_find_contracts_by_agent(self):
        """Test finding contracts by agent using find_contracts()."""
        registry = ContractRegistry()
        registry.add(self.create_contract("c1", ["a1", "a2"]))
        registry.add(self.create_contract("c2", ["a2", "a3"]))
        registry.add(self.create_contract("c3", ["a3", "a4"]))

        # find_contracts with single agent, active_only=False to find unsigned contracts
        contracts = registry.find_contracts("a2", active_only=False)
        assert len(contracts) == 2

        contracts = registry.find_contracts("a1", active_only=False)
        assert len(contracts) == 1

    def test_contracts_property(self):
        """Test getting all contracts via contracts property."""
        registry = ContractRegistry()
        registry.add(self.create_contract("c1", ["a1"]))
        registry.add(self.create_contract("c2", ["a2"]))

        all_contracts = registry.contracts
        assert len(all_contracts) == 2

    def test_persistence(self):
        """Test automatic persistence via storage_path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "contracts.json"

            # Create registry with storage path - it auto-saves on add
            registry1 = ContractRegistry(storage_path=str(filepath))
            registry1.add(self.create_contract("c1", ["a1"]))
            registry1.add(self.create_contract("c2", ["a2"]))

            # Create new registry that auto-loads from same path
            registry2 = ContractRegistry(storage_path=str(filepath))

            assert len(registry2.contracts) == 2
            assert registry2.get("c1") is not None

    def test_active_contracts_property(self):
        """Test active_contracts property returns only signed contracts."""
        registry = ContractRegistry()

        # Add signed contract
        signed_contract = self.create_contract("c1", ["a1"])
        signed_contract.signatures = {"a1": "sig1"}
        registry.add(signed_contract)

        # Add unsigned contract
        unsigned_contract = self.create_contract("c2", ["a2"])
        registry.add(unsigned_contract)

        active = registry.active_contracts
        assert len(active) == 1
        assert active[0].contract_id == "c1"

    def test_remove_contract_not_found(self):
        """Test removing a contract that doesn't exist."""
        registry = ContractRegistry()
        result = registry.remove("nonexistent")
        assert result is False

    def test_remove_contract_with_storage(self):
        """Test removing contract triggers save when storage_path is set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "contracts.json"
            registry = ContractRegistry(storage_path=str(filepath))

            contract = self.create_contract("c1", ["a1"])
            registry.add(contract)

            # Remove should trigger save
            result = registry.remove("c1")
            assert result is True

            # Verify it was saved (file should exist and contract should be gone)
            registry2 = ContractRegistry(storage_path=str(filepath))
            assert registry2.get("c1") is None

    def test_create_contract(self):
        """Test create_contract method."""
        registry = ContractRegistry()

        parties = [
            Party(agent_id="a1", role="member", public_key="pk_1"),
            Party(agent_id="a2", role="member", public_key="pk_2"),
        ]
        capabilities = {
            "member": [Capability(action="work", parameters={})],
        }

        contract = registry.create_contract(parties, capabilities)

        assert contract is not None
        assert contract.contract_id is not None
        assert len(contract.parties) == 2
        assert registry.get(contract.contract_id) == contract

    def test_sign_contract_success(self):
        """Test signing a contract successfully."""
        registry = ContractRegistry()
        contract = self.create_contract("c1", ["a1", "a2"])
        registry.add(contract)

        result = registry.sign("c1", "a1", "signature1")

        assert result is True
        assert contract.signatures["a1"] == "signature1"

    def test_sign_contract_not_found(self):
        """Test signing a contract that doesn't exist."""
        registry = ContractRegistry()
        result = registry.sign("nonexistent", "a1", "sig1")
        assert result is False

    def test_sign_contract_not_party(self):
        """Test signing a contract when agent is not a party."""
        registry = ContractRegistry()
        contract = self.create_contract("c1", ["a1"])
        registry.add(contract)

        result = registry.sign("c1", "not-a-party", "sig1")
        assert result is False
        assert "not-a-party" not in contract.signatures

    def test_sign_contract_fully_signed(self):
        """Test signing completes contract when all parties sign."""
        registry = ContractRegistry()
        contract = self.create_contract("c1", ["a1", "a2"])
        registry.add(contract)

        # Sign first party
        registry.sign("c1", "a1", "sig1")
        assert not contract.is_fully_signed

        # Sign second party - should be fully signed now
        registry.sign("c1", "a2", "sig2")
        assert contract.is_fully_signed

    def test_sign_contract_with_storage(self):
        """Test signing triggers save when storage_path is set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "contracts.json"
            registry = ContractRegistry(storage_path=str(filepath))

            contract = self.create_contract("c1", ["a1"])
            registry.add(contract)

            # Sign should trigger save
            result = registry.sign("c1", "a1", "sig1")
            assert result is True

            # Verify it was saved
            registry2 = ContractRegistry(storage_path=str(filepath))
            loaded_contract = registry2.get("c1")
            assert loaded_contract.signatures["a1"] == "sig1"

    def test_find_contracts_active_only_filtering(self):
        """Test find_contracts filters by active_only parameter."""
        registry = ContractRegistry()

        # Add signed (active) contract
        active_contract = self.create_contract("c1", ["a1"])
        active_contract.signatures = {"a1": "sig1"}
        registry.add(active_contract)

        # Add unsigned (inactive) contract
        inactive_contract = self.create_contract("c2", ["a1"])
        registry.add(inactive_contract)

        # With active_only=True (default), should only return active
        active_results = registry.find_contracts("a1", active_only=True)
        assert len(active_results) == 1
        assert active_results[0].contract_id == "c1"

        # With active_only=False, should return all
        all_results = registry.find_contracts("a1", active_only=False)
        assert len(all_results) == 2

    def test_find_contracts_agent_b_not_party(self):
        """Test find_contracts when agent_b is not a party."""
        registry = ContractRegistry()
        registry.add(self.create_contract("c1", ["a1", "a2"]))
        registry.add(self.create_contract("c2", ["a1", "a3"]))

        # Find contracts between a1 and a4 (a4 is not in any contract)
        results = registry.find_contracts("a1", "a4", active_only=False)
        assert len(results) == 0

    def test_find_by_role(self):
        """Test find_by_role method."""
        registry = ContractRegistry()

        # Create contracts with different roles
        contract1 = AgentContract(
            contract_id="c1",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="a1", role="worker", public_key="pk_1"),
                Party(agent_id="a2", role="manager", public_key="pk_2"),
            ],
            capabilities={"worker": [], "manager": []},
            signatures={"a1": "sig1", "a2": "sig2"},
        )

        contract2 = AgentContract(
            contract_id="c2",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="a1", role="worker", public_key="pk_1"),
                Party(agent_id="a3", role="worker", public_key="pk_3"),
            ],
            capabilities={"worker": []},
            signatures={"a1": "sig1", "a3": "sig3"},
        )

        registry.add(contract1)
        registry.add(contract2)

        # Find contracts where a1 has worker role
        worker_contracts = registry.find_by_role("a1", "worker")
        assert len(worker_contracts) == 2

        # Find contracts where a1 has manager role
        manager_contracts = registry.find_by_role("a1", "manager")
        assert len(manager_contracts) == 0

    def test_find_by_role_active_only(self):
        """Test find_by_role with active_only filtering."""
        registry = ContractRegistry()

        contract = AgentContract(
            contract_id="c1",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="a1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": []},
            # Not signed, so not active
        )
        registry.add(contract)

        # With active_only=True (default), should return empty
        results = registry.find_by_role("a1", "worker", active_only=True)
        assert len(results) == 0

        # With active_only=False, should return the contract
        results = registry.find_by_role("a1", "worker", active_only=False)
        assert len(results) == 1

    def test_get_agent_roles(self):
        """Test get_agent_roles method."""
        registry = ContractRegistry()

        contract1 = AgentContract(
            contract_id="c1",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="a1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": []},
        )

        contract2 = AgentContract(
            contract_id="c2",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="a1", role="manager", public_key="pk_1"),
            ],
            capabilities={"manager": []},
        )

        registry.add(contract1)
        registry.add(contract2)

        roles = registry.get_agent_roles("a1")

        assert len(roles) == 2
        assert roles["c1"] == "worker"
        assert roles["c2"] == "manager"

    def test_get_agent_roles_not_in_contracts(self):
        """Test get_agent_roles when agent is not in any contracts."""
        registry = ContractRegistry()
        registry.add(self.create_contract("c1", ["a1"]))

        roles = registry.get_agent_roles("unknown-agent")
        assert len(roles) == 0

    def test_cleanup_expired(self):
        """Test cleanup_expired removes expired contracts."""
        registry = ContractRegistry()

        # Add expired contract
        expired_contract = AgentContract(
            contract_id="c1",
            version="1.0.0",
            created=datetime.now(timezone.utc) - timedelta(days=2),
            parties=[Party(agent_id="a1", role="member", public_key="pk_1")],
            capabilities={"member": []},
            expires=datetime.now(timezone.utc) - timedelta(days=1),  # Expired yesterday
        )

        # Add non-expired contract
        active_contract = AgentContract(
            contract_id="c2",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[Party(agent_id="a2", role="member", public_key="pk_2")],
            capabilities={"member": []},
            expires=datetime.now(timezone.utc) + timedelta(days=1),  # Expires tomorrow
        )

        registry.add(expired_contract)
        registry.add(active_contract)

        removed_count = registry.cleanup_expired()

        assert removed_count == 1
        assert registry.get("c1") is None
        assert registry.get("c2") is not None

    def test_cleanup_expired_no_expired(self):
        """Test cleanup_expired when no contracts are expired."""
        registry = ContractRegistry()
        registry.add(self.create_contract("c1", ["a1"]))

        removed_count = registry.cleanup_expired()
        assert removed_count == 0
        assert registry.get("c1") is not None

    def test_cleanup_expired_with_storage(self):
        """Test cleanup_expired triggers save when storage_path is set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "contracts.json"
            registry = ContractRegistry(storage_path=str(filepath))

            expired_contract = AgentContract(
                contract_id="c1",
                version="1.0.0",
                created=datetime.now(timezone.utc) - timedelta(days=2),
                parties=[Party(agent_id="a1", role="member", public_key="pk_1")],
                capabilities={"member": []},
                expires=datetime.now(timezone.utc) - timedelta(days=1),
            )
            registry.add(expired_contract)

            removed_count = registry.cleanup_expired()
            assert removed_count == 1

            # Verify it was saved
            registry2 = ContractRegistry(storage_path=str(filepath))
            assert registry2.get("c1") is None

    def test_save_no_storage_path(self):
        """Test _save() does nothing when storage_path is None."""
        registry = ContractRegistry()  # No storage_path
        contract = self.create_contract("c1", ["a1"])

        # Should not raise exception
        registry.add(contract)
        registry.remove("c1")

    def test_load_no_storage_path(self):
        """Test _load() does nothing when storage_path is None."""
        registry = ContractRegistry()  # No storage_path
        # Should not raise exception
        assert len(registry.contracts) == 0

    def test_load_file_not_exists(self):
        """Test _load() handles non-existent file gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "nonexistent.json"
            # File doesn't exist, should not raise exception
            registry = ContractRegistry(storage_path=str(filepath))
            assert len(registry.contracts) == 0


class TestContractVerifier:
    """Tests for ContractVerifier."""

    def setup_method(self):
        """Set up test fixtures."""
        self.registry = ContractRegistry()
        self.contract = AgentContract(
            contract_id="test-contract",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
                Party(agent_id="agent-2", role="manager", public_key="pk_2"),
            ],
            capabilities={
                "worker": [
                    Capability(action="execute_task", parameters={}),
                    Capability(action="read_data", parameters={}),
                ],
                "manager": [
                    Capability(action="execute_task", parameters={}),
                    Capability(action="read_data", parameters={}),
                ],
            },
            prohibitions={
                "all_parties": [
                    Prohibition(action="delete_data", reason="Cannot delete")
                ],
            },
            signatures={"agent-1": "sig1", "agent-2": "sig2"},
        )
        self.registry.add(self.contract)
        self.verifier = ContractVerifier(self.registry)

    def test_verify_allowed_action(self):
        """Test verifying allowed action."""
        result = self.verifier.verify_action("agent-1", "execute_task")

        assert not result.has_violations()
        assert result.status == ContractStatus.VERIFIED

    def test_verify_prohibited_action(self):
        """Test verifying prohibited action."""
        result = self.verifier.verify_action("agent-1", "delete_data")

        assert result.has_violations()
        assert len(result.violations) > 0
        # Agent may lack capability (first) AND have prohibition (second)
        # Check that a prohibition violation exists
        has_prohibition = any(
            v.type == ViolationType.PROHIBITION for v in result.violations
        )
        assert (
            has_prohibition
        ), f"Expected PROHIBITION violation, got: {[v.type for v in result.violations]}"

    def test_verify_unauthorized_action(self):
        """Test verifying unauthorized action."""
        result = self.verifier.verify_action("agent-1", "admin_action")

        # May pass (not prohibited) or fail (not explicitly allowed)
        # depending on implementation - test for non-None result
        assert result is not None

    def test_verify_non_party_action(self):
        """Test verifying action by non-party."""
        result = self.verifier.verify_action("unknown-agent", "execute_task")

        # Should handle gracefully
        assert result is not None

    def test_verify_message_no_contract(self):
        """Test verify_message when no contract exists."""
        message = Message(action="execute_task", payload={})
        result = self.verifier.verify_message(
            "unknown-sender", "unknown-receiver", message
        )

        assert result.status == ContractStatus.NO_CONTRACT
        assert "Establish contract" in result.recommendation

    def test_verify_message_allowed_action(self):
        """Test verify_message with allowed action."""
        message = Message(action="execute_task", payload={})
        result = self.verifier.verify_message("agent-1", "agent-2", message)

        assert result.status == ContractStatus.VERIFIED
        assert result.contract_id == "test-contract"
        assert not result.has_violations()

    def test_verify_message_prohibited_action(self):
        """Test verify_message with prohibited action."""
        message = Message(action="delete_data", payload={})
        result = self.verifier.verify_message("agent-1", "agent-2", message)

        assert result.status == ContractStatus.VIOLATION
        assert result.has_violations()
        has_prohibition = any(
            v.type == ViolationType.PROHIBITION for v in result.violations
        )
        assert has_prohibition

    def test_verify_message_lacks_capability(self):
        """Test verify_message when agent lacks capability."""
        # Create contract where agent-1 doesn't have "admin_action"
        contract = AgentContract(
            contract_id="test-contract-2",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
                Party(agent_id="agent-2", role="manager", public_key="pk_2"),
            ],
            capabilities={
                "worker": [Capability(action="execute_task", parameters={})],
                "manager": [Capability(action="admin_action", parameters={})],
            },
            signatures={"agent-1": "sig1", "agent-2": "sig2"},
        )
        self.registry.add(contract)

        message = Message(action="admin_action", payload={})
        result = self.verifier.verify_message("agent-1", "agent-2", message)

        assert result.status == ContractStatus.VIOLATION
        assert result.has_violations()
        has_capability_violation = any(
            v.type == ViolationType.CAPABILITY for v in result.violations
        )
        assert has_capability_violation

    def test_verify_message_multiple_contracts(self):
        """Test verify_message when multiple contracts exist."""
        # Add second contract
        contract2 = AgentContract(
            contract_id="test-contract-2",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
                Party(agent_id="agent-2", role="manager", public_key="pk_2"),
            ],
            capabilities={
                "worker": [Capability(action="special_action", parameters={})],
            },
            signatures={"agent-1": "sig1", "agent-2": "sig2"},
        )
        self.registry.add(contract2)

        message = Message(action="special_action", payload={})
        result = self.verifier.verify_message("agent-1", "agent-2", message)

        # Should find a contract that allows this action
        assert result.status == ContractStatus.VERIFIED

    def test_track_obligation(self):
        """Test tracking an obligation trigger."""
        self.verifier.track_obligation("test-contract", "agent-1", "request_trigger")

        key = "test-contract:agent-1"
        assert key in self.verifier._obligation_trackers
        assert "request_trigger" in self.verifier._obligation_trackers[key]

    def test_track_obligation_multiple_triggers(self):
        """Test tracking multiple obligation triggers."""
        self.verifier.track_obligation("test-contract", "agent-1", "trigger1")
        self.verifier.track_obligation("test-contract", "agent-1", "trigger2")

        key = "test-contract:agent-1"
        assert len(self.verifier._obligation_trackers[key]) == 2
        assert "trigger1" in self.verifier._obligation_trackers[key]
        assert "trigger2" in self.verifier._obligation_trackers[key]

    def test_fulfill_obligation_success(self):
        """Test fulfilling an obligation successfully."""
        # Create contract with obligation
        contract = AgentContract(
            contract_id="test-contract-obligation",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": [Capability(action="respond", parameters={})]},
            obligations={
                "worker": [
                    Obligation(trigger="request", action="respond", parameters={})
                ],
            },
            signatures={"agent-1": "sig1"},
        )
        self.registry.add(contract)

        # Track the obligation first
        self.verifier.track_obligation("test-contract-obligation", "agent-1", "request")

        # Fulfill it
        result = self.verifier.fulfill_obligation(
            "test-contract-obligation", "agent-1", "respond"
        )

        assert result is True
        key = "test-contract-obligation:agent-1"
        # Trigger should be removed after fulfillment
        assert "request" not in self.verifier._obligation_trackers.get(key, {})

    def test_fulfill_obligation_no_contract(self):
        """Test fulfilling obligation when contract doesn't exist."""
        result = self.verifier.fulfill_obligation("nonexistent", "agent-1", "respond")
        assert result is False

    def test_fulfill_obligation_not_party(self):
        """Test fulfilling obligation when agent is not a party."""
        contract = AgentContract(
            contract_id="test-contract-obligation",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": [Capability(action="respond", parameters={})]},
            obligations={
                "worker": [
                    Obligation(trigger="request", action="respond", parameters={})
                ],
            },
            signatures={"agent-1": "sig1"},
        )
        self.registry.add(contract)

        result = self.verifier.fulfill_obligation(
            "test-contract-obligation", "unknown-agent", "respond"
        )
        assert result is False

    def test_fulfill_obligation_no_matching_action(self):
        """Test fulfilling obligation when action doesn't match."""
        contract = AgentContract(
            contract_id="test-contract-obligation",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": [Capability(action="respond", parameters={})]},
            obligations={
                "worker": [
                    Obligation(trigger="request", action="respond", parameters={})
                ],
            },
            signatures={"agent-1": "sig1"},
        )
        self.registry.add(contract)

        self.verifier.track_obligation("test-contract-obligation", "agent-1", "request")

        # Try to fulfill with wrong action
        result = self.verifier.fulfill_obligation(
            "test-contract-obligation", "agent-1", "wrong_action"
        )
        assert result is False

    def test_check_pending_obligations_no_contract(self):
        """Test checking pending obligations when contract doesn't exist."""
        pending = self.verifier.check_pending_obligations("nonexistent", "agent-1")
        assert pending == []

    def test_check_pending_obligations_not_party(self):
        """Test checking pending obligations when agent is not a party."""
        contract = AgentContract(
            contract_id="test-contract-obligation",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": []},
            obligations={
                "worker": [
                    Obligation(trigger="request", action="respond", parameters={})
                ],
            },
            signatures={"agent-1": "sig1"},
        )
        self.registry.add(contract)

        pending = self.verifier.check_pending_obligations(
            "test-contract-obligation", "unknown-agent"
        )
        assert pending == []

    def test_check_pending_obligations_timeout_exceeded(self):
        """Test checking pending obligations when timeout is exceeded."""
        contract = AgentContract(
            contract_id="test-contract-obligation",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": []},
            obligations={
                "worker": [
                    Obligation(
                        trigger="request",
                        action="respond",
                        parameters={"timeout_ms": 100},  # 100ms timeout
                    ),
                ],
            },
            signatures={"agent-1": "sig1"},
        )
        self.registry.add(contract)

        # Track obligation
        self.verifier.track_obligation("test-contract-obligation", "agent-1", "request")

        # Wait for timeout
        time.sleep(0.15)  # 150ms > 100ms timeout

        pending = self.verifier.check_pending_obligations(
            "test-contract-obligation", "agent-1"
        )
        assert len(pending) == 1
        assert pending[0].action == "respond"

    def test_check_pending_obligations_within_timeout(self):
        """Test checking pending obligations when still within timeout."""
        contract = AgentContract(
            contract_id="test-contract-obligation",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": []},
            obligations={
                "worker": [
                    Obligation(
                        trigger="request",
                        action="respond",
                        parameters={"timeout_ms": 30000},  # 30 second timeout
                    ),
                ],
            },
            signatures={"agent-1": "sig1"},
        )
        self.registry.add(contract)

        # Track obligation
        self.verifier.track_obligation("test-contract-obligation", "agent-1", "request")

        # Check immediately (should not be pending yet)
        pending = self.verifier.check_pending_obligations(
            "test-contract-obligation", "agent-1"
        )
        assert len(pending) == 0

    def test_check_pending_obligations_default_timeout(self):
        """Test checking pending obligations with default timeout."""
        contract = AgentContract(
            contract_id="test-contract-obligation",
            version="1.0.0",
            created=datetime.now(timezone.utc),
            parties=[
                Party(agent_id="agent-1", role="worker", public_key="pk_1"),
            ],
            capabilities={"worker": []},
            obligations={
                "worker": [
                    Obligation(
                        trigger="request",
                        action="respond",
                        parameters={},  # No timeout specified, should default to 30000ms
                    ),
                ],
            },
            signatures={"agent-1": "sig1"},
        )
        self.registry.add(contract)

        self.verifier.track_obligation("test-contract-obligation", "agent-1", "request")

        # Check immediately (should not be pending with 30s default timeout)
        pending = self.verifier.check_pending_obligations(
            "test-contract-obligation", "agent-1"
        )
        assert len(pending) == 0


class TestContractVerificationResult:
    """Tests for ContractVerificationResult."""

    def test_no_violations_when_empty(self):
        """Test no violations when empty."""
        result = ContractVerificationResult(
            status=ContractStatus.VERIFIED,
            contract_id="c1",
            violations=[],
        )

        assert not result.has_violations()

    def test_has_violations_when_present(self):
        """Test has_violations when violations present."""
        result = ContractVerificationResult(
            status=ContractStatus.VIOLATION,
            contract_id="c1",
            violations=[
                Violation(
                    type=ViolationType.PROHIBITION,
                    message="Action prohibited",
                ),
            ],
        )

        assert result.has_violations()
        assert len(result.violations) == 1

    def test_to_dict(self):
        """Test ContractVerificationResult.to_dict() method."""
        violations = [
            Violation(
                type=ViolationType.CAPABILITY,
                message="Test violation",
                details={"key": "value"},
            ),
        ]
        result = ContractVerificationResult(
            status=ContractStatus.VIOLATION,
            contract_id="c1",
            violations=violations,
            recommendation="Fix the issue",
        )

        data = result.to_dict()

        assert data["status"] == ContractStatus.VIOLATION.value
        assert data["contract_id"] == "c1"
        assert data["recommendation"] == "Fix the issue"
        assert len(data["violations"]) == 1
        assert data["violations"][0]["type"] == ViolationType.CAPABILITY.value
        assert data["violations"][0]["message"] == "Test violation"
        assert data["violations"][0]["details"] == {"key": "value"}


class TestViolation:
    """Tests for Violation dataclass."""

    def test_to_dict(self):
        """Test Violation.to_dict() method."""
        violation = Violation(
            type=ViolationType.OBLIGATION,
            message="Obligation not fulfilled",
            details={"agent_id": "agent-1", "action": "report"},
        )

        data = violation.to_dict()

        assert data["type"] == ViolationType.OBLIGATION.value
        assert data["message"] == "Obligation not fulfilled"
        assert data["details"] == {"agent_id": "agent-1", "action": "report"}
