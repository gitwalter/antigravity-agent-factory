"""
Blockchain Anchor

Anchors agent events and contracts to blockchain for immutability.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class MerkleNode:
    """
    Node in a Merkle tree.
    
    Attributes:
        hash: Hash of this node.
        left: Left child node.
        right: Right child node.
        data: Original data (for leaf nodes).
    """
    hash: str
    left: Optional["MerkleNode"] = None
    right: Optional["MerkleNode"] = None
    data: Optional[str] = None
    
    @property
    def is_leaf(self) -> bool:
        """Check if this is a leaf node."""
        return self.left is None and self.right is None


class MerkleTree:
    """
    Merkle tree for batching event hashes.
    
    Allows efficient proof of inclusion for individual events
    while only storing the root hash on-chain.
    
    Usage:
        tree = MerkleTree()
        tree.add_leaf("event_hash_1")
        tree.add_leaf("event_hash_2")
        tree.build()
        
        root = tree.root_hash
        proof = tree.get_proof("event_hash_1")
    """
    
    def __init__(self):
        """Initialize empty Merkle tree."""
        self._leaves: List[MerkleNode] = []
        self._root: Optional[MerkleNode] = None
        self._built = False
    
    @staticmethod
    def _hash(data: str) -> str:
        """Compute SHA-256 hash."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def _combine_hash(left: str, right: str) -> str:
        """Combine two hashes."""
        combined = left + right
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def add_leaf(self, data: str) -> None:
        """
        Add a leaf to the tree.
        
        Args:
            data: Data to hash and add as leaf.
        """
        if self._built:
            raise RuntimeError("Cannot add leaves after tree is built")
        
        leaf_hash = self._hash(data)
        self._leaves.append(MerkleNode(hash=leaf_hash, data=data))
    
    def build(self) -> None:
        """Build the Merkle tree from leaves."""
        if not self._leaves:
            return
        
        # Copy leaves to build tree
        nodes = self._leaves.copy()
        
        # Build tree bottom-up
        while len(nodes) > 1:
            next_level = []
            
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                
                # If odd number of nodes, duplicate the last one
                if i + 1 < len(nodes):
                    right = nodes[i + 1]
                else:
                    right = left
                
                parent_hash = self._combine_hash(left.hash, right.hash)
                parent = MerkleNode(
                    hash=parent_hash,
                    left=left,
                    right=right,
                )
                next_level.append(parent)
            
            nodes = next_level
        
        self._root = nodes[0]
        self._built = True
    
    @property
    def root_hash(self) -> Optional[str]:
        """Get the root hash."""
        if not self._built:
            self.build()
        return self._root.hash if self._root else None
    
    @property
    def leaf_count(self) -> int:
        """Get number of leaves."""
        return len(self._leaves)
    
    def get_proof(self, data: str) -> Optional[List[tuple]]:
        """
        Get Merkle proof for a piece of data.
        
        Args:
            data: Original data that was added as leaf.
            
        Returns:
            List of (hash, position) tuples for proof, or None if not found.
        """
        if not self._built:
            self.build()
        
        if not self._root:
            return None
        
        target_hash = self._hash(data)
        
        # Find the leaf
        leaf_index = None
        for i, leaf in enumerate(self._leaves):
            if leaf.hash == target_hash:
                leaf_index = i
                break
        
        if leaf_index is None:
            return None
        
        # Build proof by traversing up
        proof = []
        nodes = self._leaves.copy()
        current_index = leaf_index
        
        while len(nodes) > 1:
            next_level = []
            
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                
                if i + 1 < len(nodes):
                    right = nodes[i + 1]
                else:
                    right = left
                
                # Add sibling to proof if current node is in this pair
                if i == current_index or i + 1 == current_index:
                    if i == current_index:
                        proof.append((right.hash, "right"))
                    else:
                        proof.append((left.hash, "left"))
                
                parent_hash = self._combine_hash(left.hash, right.hash)
                next_level.append(MerkleNode(hash=parent_hash, left=left, right=right))
            
            nodes = next_level
            current_index = current_index // 2
        
        return proof
    
    @staticmethod
    def verify_proof(
        data: str,
        proof: List[tuple],
        root_hash: str
    ) -> bool:
        """
        Verify a Merkle proof.
        
        Args:
            data: Original data.
            proof: Proof from get_proof().
            root_hash: Expected root hash.
            
        Returns:
            True if proof is valid.
        """
        current_hash = MerkleTree._hash(data)
        
        for sibling_hash, position in proof:
            if position == "left":
                current_hash = MerkleTree._combine_hash(sibling_hash, current_hash)
            else:
                current_hash = MerkleTree._combine_hash(current_hash, sibling_hash)
        
        return current_hash == root_hash


@dataclass
class AnchorRecord:
    """
    Record of data anchored to blockchain.
    
    Attributes:
        anchor_id: Unique identifier.
        merkle_root: Root hash of the Merkle tree.
        event_count: Number of events in this anchor.
        timestamp: When anchor was created.
        transaction_id: Blockchain transaction ID (if submitted).
        status: Current status.
    """
    anchor_id: str
    merkle_root: str
    event_count: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    transaction_id: Optional[str] = None
    status: str = "pending"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "anchor_id": self.anchor_id,
            "merkle_root": self.merkle_root,
            "event_count": self.event_count,
            "timestamp": self.timestamp.isoformat(),
            "transaction_id": self.transaction_id,
            "status": self.status,
        }


class BlockchainAnchor(ABC):
    """
    Abstract base class for blockchain anchoring.
    
    Implementations provide connectivity to specific blockchains.
    """
    
    @property
    @abstractmethod
    def chain_name(self) -> str:
        """Get blockchain name."""
        pass
    
    @abstractmethod
    def submit_anchor(self, merkle_root: str, metadata: Dict[str, Any]) -> Optional[str]:
        """
        Submit an anchor to the blockchain.
        
        Args:
            merkle_root: The Merkle root to anchor.
            metadata: Additional metadata.
            
        Returns:
            Transaction ID if successful.
        """
        pass
    
    @abstractmethod
    def verify_anchor(self, transaction_id: str, expected_root: str) -> bool:
        """
        Verify an anchor on the blockchain.
        
        Args:
            transaction_id: The transaction to verify.
            expected_root: Expected Merkle root.
            
        Returns:
            True if anchor is valid and confirmed.
        """
        pass
    
    @abstractmethod
    def get_anchor_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get status of an anchor transaction.
        
        Args:
            transaction_id: The transaction ID.
            
        Returns:
            Status information.
        """
        pass


class LocalAnchor(BlockchainAnchor):
    """
    Local anchor for development and testing.
    
    Simulates blockchain anchoring without actual blockchain connectivity.
    Useful for testing and development environments.
    """
    
    def __init__(self):
        """Initialize local anchor."""
        self._anchors: Dict[str, Dict[str, Any]] = {}
        self._tx_counter = 0
    
    @property
    def chain_name(self) -> str:
        return "local"
    
    def submit_anchor(
        self,
        merkle_root: str,
        metadata: Dict[str, Any]
    ) -> Optional[str]:
        """Submit anchor (simulated)."""
        self._tx_counter += 1
        tx_id = f"local-tx-{self._tx_counter}"
        
        self._anchors[tx_id] = {
            "merkle_root": merkle_root,
            "metadata": metadata,
            "timestamp": datetime.utcnow().isoformat(),
            "confirmed": True,
            "block": self._tx_counter,
        }
        
        logger.info(f"Local anchor submitted: {tx_id} (root: {merkle_root[:16]}...)")
        return tx_id
    
    def verify_anchor(self, transaction_id: str, expected_root: str) -> bool:
        """Verify anchor (simulated)."""
        anchor = self._anchors.get(transaction_id)
        if not anchor:
            return False
        
        return (
            anchor["confirmed"] and
            anchor["merkle_root"] == expected_root
        )
    
    def get_anchor_status(self, transaction_id: str) -> Dict[str, Any]:
        """Get anchor status."""
        anchor = self._anchors.get(transaction_id)
        if not anchor:
            return {"status": "not_found"}
        
        return {
            "status": "confirmed" if anchor["confirmed"] else "pending",
            "block": anchor["block"],
            "timestamp": anchor["timestamp"],
            "merkle_root": anchor["merkle_root"],
        }


class AnchorService:
    """
    Service for managing blockchain anchoring.
    
    Features:
    - Batches events into Merkle trees
    - Submits anchors to blockchain
    - Provides verification and proofs
    
    Usage:
        service = AnchorService(LocalAnchor())
        service.add_event("event_hash_1")
        service.add_event("event_hash_2")
        
        anchor = service.create_anchor()
        service.submit_anchor(anchor.anchor_id)
        
        # Later, verify inclusion
        proof = service.get_proof("event_hash_1")
    """
    
    BATCH_SIZE = 100  # Events per anchor
    
    def __init__(self, blockchain: BlockchainAnchor):
        """
        Initialize anchor service.
        
        Args:
            blockchain: Blockchain connector to use.
        """
        self.blockchain = blockchain
        self._pending_events: List[str] = []
        self._trees: Dict[str, MerkleTree] = {}
        self._anchors: Dict[str, AnchorRecord] = {}
        self._event_to_anchor: Dict[str, str] = {}  # event_hash -> anchor_id
    
    def add_event(self, event_hash: str) -> None:
        """
        Add an event hash to the pending batch.
        
        Args:
            event_hash: Hash of the event to anchor.
        """
        self._pending_events.append(event_hash)
        
        # Auto-anchor if batch is full
        if len(self._pending_events) >= self.BATCH_SIZE:
            self.create_anchor()
    
    def create_anchor(self, metadata: Optional[Dict[str, Any]] = None) -> Optional[AnchorRecord]:
        """
        Create an anchor from pending events.
        
        Args:
            metadata: Optional metadata to include.
            
        Returns:
            AnchorRecord if events were pending.
        """
        if not self._pending_events:
            return None
        
        # Build Merkle tree
        tree = MerkleTree()
        for event_hash in self._pending_events:
            tree.add_leaf(event_hash)
        tree.build()
        
        # Create anchor record
        anchor_id = f"anchor-{len(self._anchors) + 1}"
        anchor = AnchorRecord(
            anchor_id=anchor_id,
            merkle_root=tree.root_hash,
            event_count=len(self._pending_events),
        )
        
        # Store mappings
        self._trees[anchor_id] = tree
        self._anchors[anchor_id] = anchor
        
        for event_hash in self._pending_events:
            self._event_to_anchor[event_hash] = anchor_id
        
        self._pending_events = []
        
        logger.info(f"Created anchor {anchor_id} with {anchor.event_count} events")
        return anchor
    
    def submit_anchor(
        self,
        anchor_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Submit an anchor to the blockchain.
        
        Args:
            anchor_id: The anchor to submit.
            metadata: Optional additional metadata.
            
        Returns:
            True if submission was successful.
        """
        anchor = self._anchors.get(anchor_id)
        if not anchor:
            return False
        
        if anchor.transaction_id:
            logger.warning(f"Anchor {anchor_id} already submitted")
            return False
        
        tx_id = self.blockchain.submit_anchor(
            anchor.merkle_root,
            metadata or {"anchor_id": anchor_id},
        )
        
        if tx_id:
            anchor.transaction_id = tx_id
            anchor.status = "submitted"
            logger.info(f"Submitted anchor {anchor_id}: {tx_id}")
            return True
        
        return False
    
    def get_proof(self, event_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get proof of inclusion for an event.
        
        Args:
            event_hash: Hash of the event.
            
        Returns:
            Proof data if event is anchored.
        """
        anchor_id = self._event_to_anchor.get(event_hash)
        if not anchor_id:
            return None
        
        tree = self._trees.get(anchor_id)
        anchor = self._anchors.get(anchor_id)
        
        if not tree or not anchor:
            return None
        
        proof = tree.get_proof(event_hash)
        if proof is None:
            return None
        
        return {
            "anchor_id": anchor_id,
            "merkle_root": anchor.merkle_root,
            "transaction_id": anchor.transaction_id,
            "proof": proof,
        }
    
    def verify_event(self, event_hash: str, proof_data: Dict[str, Any]) -> bool:
        """
        Verify an event is anchored.
        
        Args:
            event_hash: Hash of the event.
            proof_data: Proof data from get_proof().
            
        Returns:
            True if event is verified.
        """
        merkle_root = proof_data.get("merkle_root")
        proof = proof_data.get("proof")
        transaction_id = proof_data.get("transaction_id")
        
        if not merkle_root or proof is None:
            return False
        
        # Verify Merkle proof
        if not MerkleTree.verify_proof(event_hash, proof, merkle_root):
            return False
        
        # If transaction submitted, verify on-chain
        if transaction_id:
            return self.blockchain.verify_anchor(transaction_id, merkle_root)
        
        return True
    
    def get_anchor(self, anchor_id: str) -> Optional[AnchorRecord]:
        """Get an anchor record."""
        return self._anchors.get(anchor_id)
    
    def get_pending_count(self) -> int:
        """Get count of pending events."""
        return len(self._pending_events)
    
    def export(self) -> Dict[str, Any]:
        """Export anchor data."""
        return {
            "chain": self.blockchain.chain_name,
            "anchors": [a.to_dict() for a in self._anchors.values()],
            "pending_events": len(self._pending_events),
        }
