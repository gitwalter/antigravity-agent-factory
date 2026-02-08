"""
Blockchain Module

Blockchain integration for immutable audit trails.

Components:
- MerkleTree: Efficient batching of event hashes
- BlockchainAnchor: Abstract interface for blockchain anchoring
- LocalAnchor: Development/testing anchor
- SolanaAnchor: Solana blockchain integration
- AnchorService: Service for managing anchors
- AttestationRegistry: Cryptographic attestations
"""

from lib.society.blockchain.anchor import (
    MerkleNode,
    MerkleTree,
    AnchorRecord,
    BlockchainAnchor,
    LocalAnchor,
    AnchorService,
)
from lib.society.blockchain.solana_client import (
    SolanaConfig,
    SolanaTransaction,
    SolanaAnchor,
    create_solana_anchor,
)
from lib.society.blockchain.attestation import (
    AttestationType,
    Attestation,
    AttestationRequest,
    AttestationRegistry,
)

__all__ = [
    # Anchor
    "MerkleNode",
    "MerkleTree",
    "AnchorRecord",
    "BlockchainAnchor",
    "LocalAnchor",
    "AnchorService",
    # Solana
    "SolanaConfig",
    "SolanaTransaction",
    "SolanaAnchor",
    "create_solana_anchor",
    # Attestation
    "AttestationType",
    "Attestation",
    "AttestationRequest",
    "AttestationRegistry",
]
