"""
Tests for the blockchain module.

Tests Merkle trees, anchoring, and attestations.
"""

import pytest
from datetime import datetime, timedelta, timezone

from lib.society.blockchain import (
    MerkleTree,
    LocalAnchor,
    AnchorService,
    SolanaConfig,
    SolanaAnchor,
    create_solana_anchor,
    AttestationType,
    Attestation,
    AttestationRegistry,
)


class TestMerkleTree:
    """Tests for MerkleTree."""

    def test_empty_tree(self):
        """Test empty tree."""
        tree = MerkleTree()
        assert tree.leaf_count == 0
        assert tree.root_hash is None

    def test_single_leaf(self):
        """Test tree with single leaf."""
        tree = MerkleTree()
        tree.add_leaf("data1")
        tree.build()

        assert tree.leaf_count == 1
        assert tree.root_hash is not None

    def test_multiple_leaves(self):
        """Test tree with multiple leaves."""
        tree = MerkleTree()
        tree.add_leaf("data1")
        tree.add_leaf("data2")
        tree.add_leaf("data3")
        tree.build()

        assert tree.leaf_count == 3
        assert len(tree.root_hash) == 64

    def test_deterministic_root(self):
        """Test that same data produces same root."""
        tree1 = MerkleTree()
        tree1.add_leaf("a")
        tree1.add_leaf("b")
        tree1.build()

        tree2 = MerkleTree()
        tree2.add_leaf("a")
        tree2.add_leaf("b")
        tree2.build()

        assert tree1.root_hash == tree2.root_hash

    def test_different_data_different_root(self):
        """Test that different data produces different root."""
        tree1 = MerkleTree()
        tree1.add_leaf("a")
        tree1.build()

        tree2 = MerkleTree()
        tree2.add_leaf("b")
        tree2.build()

        assert tree1.root_hash != tree2.root_hash

    def test_get_proof(self):
        """Test getting Merkle proof."""
        tree = MerkleTree()
        tree.add_leaf("a")
        tree.add_leaf("b")
        tree.add_leaf("c")
        tree.build()

        proof = tree.get_proof("a")
        assert proof is not None
        assert len(proof) > 0

    def test_verify_proof(self):
        """Test verifying Merkle proof."""
        tree = MerkleTree()
        tree.add_leaf("data1")
        tree.add_leaf("data2")
        tree.add_leaf("data3")
        tree.build()

        proof = tree.get_proof("data1")
        is_valid = MerkleTree.verify_proof("data1", proof, tree.root_hash)

        assert is_valid

    def test_verify_proof_fails_for_wrong_data(self):
        """Test that proof verification fails for wrong data."""
        tree = MerkleTree()
        tree.add_leaf("data1")
        tree.add_leaf("data2")
        tree.build()

        proof = tree.get_proof("data1")
        is_valid = MerkleTree.verify_proof("wrong_data", proof, tree.root_hash)

        assert not is_valid

    def test_cannot_add_after_build(self):
        """Test that adding after build raises error."""
        tree = MerkleTree()
        tree.add_leaf("data")
        tree.build()

        with pytest.raises(RuntimeError):
            tree.add_leaf("more_data")


class TestLocalAnchor:
    """Tests for LocalAnchor."""

    def test_submit_anchor(self):
        """Test submitting an anchor."""
        anchor = LocalAnchor()

        tx_id = anchor.submit_anchor("merkle_root_hash", {"test": True})

        assert tx_id is not None
        assert tx_id.startswith("local-tx-")

    def test_verify_anchor(self):
        """Test verifying an anchor."""
        anchor = LocalAnchor()

        root = "merkle_root_hash"
        tx_id = anchor.submit_anchor(root, {})

        is_valid = anchor.verify_anchor(tx_id, root)
        assert is_valid

    def test_verify_fails_wrong_root(self):
        """Test that verification fails for wrong root."""
        anchor = LocalAnchor()

        tx_id = anchor.submit_anchor("correct_root", {})
        is_valid = anchor.verify_anchor(tx_id, "wrong_root")

        assert not is_valid

    def test_get_anchor_status(self):
        """Test getting anchor status."""
        anchor = LocalAnchor()

        tx_id = anchor.submit_anchor("root", {})
        status = anchor.get_anchor_status(tx_id)

        assert status["status"] == "confirmed"
        assert status["merkle_root"] == "root"

    def test_unknown_transaction(self):
        """Test status for unknown transaction."""
        anchor = LocalAnchor()

        status = anchor.get_anchor_status("unknown-tx")
        assert status["status"] == "not_found"


class TestAnchorService:
    """Tests for AnchorService."""

    def test_add_event(self):
        """Test adding events."""
        service = AnchorService(LocalAnchor())

        service.add_event("event_hash_1")
        service.add_event("event_hash_2")

        assert service.get_pending_count() == 2

    def test_create_anchor(self):
        """Test creating an anchor."""
        service = AnchorService(LocalAnchor())

        service.add_event("event_1")
        service.add_event("event_2")

        anchor = service.create_anchor()

        assert anchor is not None
        assert anchor.event_count == 2
        assert anchor.merkle_root is not None

    def test_submit_anchor(self):
        """Test submitting an anchor."""
        service = AnchorService(LocalAnchor())

        service.add_event("event")
        anchor = service.create_anchor()

        result = service.submit_anchor(anchor.anchor_id)
        assert result

        # Anchor should have transaction ID
        anchor = service.get_anchor(anchor.anchor_id)
        assert anchor.transaction_id is not None

    def test_get_proof(self):
        """Test getting event proof."""
        service = AnchorService(LocalAnchor())

        service.add_event("event_hash")
        anchor = service.create_anchor()
        service.submit_anchor(anchor.anchor_id)

        proof = service.get_proof("event_hash")

        assert proof is not None
        assert proof["anchor_id"] == anchor.anchor_id
        assert proof["merkle_root"] is not None

    def test_verify_event(self):
        """Test verifying an event."""
        service = AnchorService(LocalAnchor())

        service.add_event("event_hash")
        anchor = service.create_anchor()
        service.submit_anchor(anchor.anchor_id)

        proof = service.get_proof("event_hash")
        is_valid = service.verify_event("event_hash", proof)

        assert is_valid

    def test_auto_anchor_on_threshold(self):
        """Test auto-anchoring when threshold is reached."""
        service = AnchorService(LocalAnchor())
        service.BATCH_SIZE = 3  # Lower threshold for testing

        service.add_event("e1")
        service.add_event("e2")
        assert service.get_pending_count() == 2

        service.add_event("e3")  # Should trigger auto-anchor
        assert service.get_pending_count() == 0


class TestSolanaAnchor:
    """Tests for SolanaAnchor (stub mode)."""

    def test_create_with_config(self):
        """Test creating with configuration."""
        config = SolanaConfig(
            network="devnet",
            program_id="test-program",
        )
        anchor = SolanaAnchor(config)

        assert anchor.config.network == "devnet"
        assert "solana" in anchor.chain_name

    def test_connect(self):
        """Test connecting (stub mode)."""
        anchor = SolanaAnchor()

        result = anchor.connect()
        assert result
        assert anchor._connected

    def test_submit_and_verify(self):
        """Test submitting and verifying (stub mode)."""
        anchor = SolanaAnchor()
        anchor.connect()

        root = "test_merkle_root"
        tx_id = anchor.submit_anchor(root, {})

        assert tx_id is not None

        is_valid = anchor.verify_anchor(tx_id, root)
        assert is_valid

    def test_get_stats(self):
        """Test getting statistics."""
        anchor = SolanaAnchor()
        anchor.connect()
        anchor.submit_anchor("root1", {})
        anchor.submit_anchor("root2", {})

        stats = anchor.get_stats()

        assert stats["connected"]
        assert stats["total_transactions"] == 2


class TestCreateSolanaAnchor:
    """Tests for create_solana_anchor factory."""

    def test_create_devnet(self):
        """Test creating devnet anchor."""
        anchor = create_solana_anchor("devnet")
        assert "devnet" in anchor.config.rpc_url

    def test_create_testnet(self):
        """Test creating testnet anchor."""
        anchor = create_solana_anchor("testnet")
        assert "testnet" in anchor.config.rpc_url


class TestAttestation:
    """Tests for Attestation."""

    def test_create_attestation(self):
        """Test creating an attestation."""
        attestation = Attestation(
            id="attest-1",
            type=AttestationType.COMPLIANCE,
            subject="agent-1",
            claim={"axiom": "A1", "compliant": True},
            attester="guardian-1",
        )

        assert attestation.id == "attest-1"
        assert attestation.type == AttestationType.COMPLIANCE

    def test_is_valid(self):
        """Test validity checking."""
        valid = Attestation(
            id="a1",
            type=AttestationType.EVENT,
            subject="s1",
            claim={},
            attester="att1",
        )
        assert valid.is_valid

        expired = Attestation(
            id="a2",
            type=AttestationType.EVENT,
            subject="s1",
            claim={},
            attester="att1",
            expires=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        assert not expired.is_valid

    def test_compute_hash(self):
        """Test hash computation."""
        attestation = Attestation(
            id="attest-1",
            type=AttestationType.IDENTITY,
            subject="agent-1",
            claim={"verified": True},
            attester="authority",
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )

        hash1 = attestation.compute_hash()
        hash2 = attestation.compute_hash()

        assert len(hash1) == 64
        assert hash1 == hash2


class TestAttestationRegistry:
    """Tests for AttestationRegistry."""

    def test_create_attestation(self):
        """Test creating attestation through registry."""
        registry = AttestationRegistry()

        attestation = registry.create_attestation(
            type=AttestationType.COMPLIANCE,
            subject="agent-1",
            claim={"passed": True},
            attester="verifier-1",
        )

        assert attestation.id is not None
        assert attestation.attester == "verifier-1"

    def test_get_attestation(self):
        """Test getting attestation."""
        registry = AttestationRegistry()

        created = registry.create_attestation(
            type=AttestationType.EVENT,
            subject="event-1",
            claim={},
            attester="system",
        )

        retrieved = registry.get(created.id)
        assert retrieved == created

    def test_get_for_subject(self):
        """Test getting attestations by subject."""
        registry = AttestationRegistry()

        registry.create_attestation(
            type=AttestationType.COMPLIANCE,
            subject="agent-1",
            claim={"a": 1},
            attester="v1",
        )
        registry.create_attestation(
            type=AttestationType.IDENTITY,
            subject="agent-1",
            claim={"b": 2},
            attester="v2",
        )
        registry.create_attestation(
            type=AttestationType.COMPLIANCE,
            subject="agent-2",
            claim={"c": 3},
            attester="v1",
        )

        attestations = registry.get_for_subject("agent-1")
        assert len(attestations) == 2

    def test_verify_attestation(self):
        """Test verifying attestation."""
        registry = AttestationRegistry()

        attestation = registry.create_attestation(
            type=AttestationType.COMPLIANCE,
            subject="agent-1",
            claim={},
            attester="verifier",
        )

        result = registry.verify(attestation.id)
        assert result["valid"]

    def test_verify_expired_attestation(self):
        """Test verifying expired attestation."""
        registry = AttestationRegistry()

        attestation = registry.create_attestation(
            type=AttestationType.COMPLIANCE,
            subject="agent-1",
            claim={},
            attester="verifier",
            expires_in=timedelta(seconds=-1),  # Already expired
        )

        result = registry.verify(attestation.id)
        assert not result["valid"]
        assert "expired" in result["reason"].lower()

    def test_create_and_fulfill_request(self):
        """Test attestation request workflow."""
        registry = AttestationRegistry()

        # Create request
        request = registry.create_request(
            type=AttestationType.COMPLIANCE,
            subject="agent-1",
            claim={"needs_verification": True},
            requester="agent-1",
            required_attesters=["verifier-1"],
        )

        assert request.status == "pending"

        # Fulfill request
        attestation = registry.fulfill_request(
            request.request_id,
            attester="verifier-1",
        )

        assert attestation is not None

        request = registry.get_request(request.request_id)
        assert request.status == "fulfilled"
