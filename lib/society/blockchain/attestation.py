"""
Attestation System

Cryptographic attestations for agent actions and contracts.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class AttestationType(Enum):
    """Types of attestations."""
    EVENT = "event"
    CONTRACT = "contract"
    COMPLIANCE = "compliance"
    IDENTITY = "identity"
    DELEGATION = "delegation"


@dataclass
class Attestation:
    """
    Cryptographic attestation for verifiable claims.
    
    Attributes:
        id: Unique attestation identifier.
        type: Type of attestation.
        subject: Subject being attested to.
        claim: The claim being made.
        attester: Agent making the attestation.
        evidence: Supporting evidence.
        timestamp: When attestation was created.
        expires: Optional expiration time.
        signature: Cryptographic signature.
        anchored: Whether anchored on-chain.
        anchor_tx: Blockchain transaction if anchored.
    """
    id: str
    type: AttestationType
    subject: str
    claim: Dict[str, Any]
    attester: str
    evidence: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    expires: Optional[datetime] = None
    signature: Optional[str] = None
    anchored: bool = False
    anchor_tx: Optional[str] = None
    
    @property
    def is_valid(self) -> bool:
        """Check if attestation is still valid."""
        if self.expires and datetime.now(timezone.utc) > self.expires:
            return False
        return True
    
    def compute_hash(self) -> str:
        """Compute attestation hash."""
        data = {
            "id": self.id,
            "type": self.type.value,
            "subject": self.subject,
            "claim": self.claim,
            "attester": self.attester,
            "evidence": self.evidence,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.expires:
            data["expires"] = self.expires.isoformat()
        
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "id": self.id,
            "type": self.type.value,
            "subject": self.subject,
            "claim": self.claim,
            "attester": self.attester,
            "evidence": self.evidence,
            "timestamp": self.timestamp.isoformat(),
            "signature": self.signature,
            "anchored": self.anchored,
            "anchor_tx": self.anchor_tx,
        }
        if self.expires:
            result["expires"] = self.expires.isoformat()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Attestation":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            type=AttestationType(data["type"]),
            subject=data["subject"],
            claim=data.get("claim", {}),
            attester=data["attester"],
            evidence=data.get("evidence", []),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.now(timezone.utc),
            expires=datetime.fromisoformat(data["expires"]) if data.get("expires") else None,
            signature=data.get("signature"),
            anchored=data.get("anchored", False),
            anchor_tx=data.get("anchor_tx"),
        )


@dataclass
class AttestationRequest:
    """
    Request for an attestation.
    
    Attributes:
        request_id: Unique request identifier.
        type: Type of attestation requested.
        subject: Subject to attest to.
        claim: Claim to verify and attest.
        requester: Agent requesting attestation.
        required_attesters: Agents whose attestation is needed.
        deadline: When attestation is needed by.
    """
    request_id: str
    type: AttestationType
    subject: str
    claim: Dict[str, Any]
    requester: str
    required_attesters: List[str] = field(default_factory=list)
    deadline: Optional[datetime] = None
    received_attestations: List[str] = field(default_factory=list)
    status: str = "pending"
    
    @property
    def is_complete(self) -> bool:
        """Check if all required attestations received."""
        if not self.required_attesters:
            return len(self.received_attestations) > 0
        
        return all(
            attester in self.received_attestations
            for attester in self.required_attesters
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "request_id": self.request_id,
            "type": self.type.value,
            "subject": self.subject,
            "claim": self.claim,
            "requester": self.requester,
            "required_attesters": self.required_attesters,
            "received_attestations": self.received_attestations,
            "status": self.status,
        }
        if self.deadline:
            result["deadline"] = self.deadline.isoformat()
        return result


class AttestationRegistry:
    """
    Registry for managing attestations.
    
    Features:
    - Create and store attestations
    - Verify attestation validity
    - Manage attestation requests
    - Track attestation chains
    
    Usage:
        registry = AttestationRegistry()
        
        attestation = registry.create_attestation(
            type=AttestationType.COMPLIANCE,
            subject="agent-123",
            claim={"axiom": "A1", "compliant": True},
            attester="guardian-1"
        )
        
        # Later, verify
        valid = registry.verify(attestation.id)
    """
    
    def __init__(self, anchor_service=None):
        """
        Initialize registry.
        
        Args:
            anchor_service: Optional AnchorService for blockchain anchoring.
        """
        self._attestations: Dict[str, Attestation] = {}
        self._requests: Dict[str, AttestationRequest] = {}
        self._by_subject: Dict[str, List[str]] = {}  # subject -> attestation_ids
        self._by_attester: Dict[str, List[str]] = {}  # attester -> attestation_ids
        self.anchor_service = anchor_service
    
    def create_attestation(
        self,
        type: AttestationType,
        subject: str,
        claim: Dict[str, Any],
        attester: str,
        evidence: Optional[List[str]] = None,
        expires_in: Optional[timedelta] = None,
        sign_fn=None
    ) -> Attestation:
        """
        Create a new attestation.
        
        Args:
            type: Type of attestation.
            subject: Subject being attested to.
            claim: The claim being made.
            attester: Agent making attestation.
            evidence: Optional supporting evidence.
            expires_in: Optional time until expiration.
            sign_fn: Optional signing function.
            
        Returns:
            Created Attestation.
        """
        attestation_id = f"attest-{len(self._attestations) + 1}"
        
        expires = None
        if expires_in:
            expires = datetime.now(timezone.utc) + expires_in
        
        attestation = Attestation(
            id=attestation_id,
            type=type,
            subject=subject,
            claim=claim,
            attester=attester,
            evidence=evidence or [],
            expires=expires,
        )
        
        # Sign if function provided
        if sign_fn:
            attestation.signature = sign_fn(attestation.compute_hash())
        
        # Store attestation
        self._attestations[attestation_id] = attestation
        
        # Index by subject
        if subject not in self._by_subject:
            self._by_subject[subject] = []
        self._by_subject[subject].append(attestation_id)
        
        # Index by attester
        if attester not in self._by_attester:
            self._by_attester[attester] = []
        self._by_attester[attester].append(attestation_id)
        
        logger.info(f"Attestation created: {attestation_id} by {attester} for {subject}")
        
        return attestation
    
    def get(self, attestation_id: str) -> Optional[Attestation]:
        """Get an attestation by ID."""
        return self._attestations.get(attestation_id)
    
    def get_for_subject(self, subject: str) -> List[Attestation]:
        """Get all attestations for a subject."""
        ids = self._by_subject.get(subject, [])
        return [
            self._attestations[id] for id in ids
            if id in self._attestations
        ]
    
    def get_by_attester(self, attester: str) -> List[Attestation]:
        """Get all attestations by an attester."""
        ids = self._by_attester.get(attester, [])
        return [
            self._attestations[id] for id in ids
            if id in self._attestations
        ]
    
    def verify(
        self,
        attestation_id: str,
        verify_signature_fn=None
    ) -> Dict[str, Any]:
        """
        Verify an attestation.
        
        Args:
            attestation_id: The attestation to verify.
            verify_signature_fn: Optional signature verification function.
            
        Returns:
            Verification result with details.
        """
        attestation = self.get(attestation_id)
        if not attestation:
            return {
                "valid": False,
                "reason": "Attestation not found",
            }
        
        # Check expiration
        if not attestation.is_valid:
            return {
                "valid": False,
                "reason": "Attestation expired",
                "expires": attestation.expires.isoformat() if attestation.expires else None,
            }
        
        # Verify signature if provided
        if verify_signature_fn and attestation.signature:
            expected_hash = attestation.compute_hash()
            if not verify_signature_fn(
                attestation.attester,
                expected_hash,
                attestation.signature
            ):
                return {
                    "valid": False,
                    "reason": "Invalid signature",
                }
        
        # Verify blockchain anchor if present
        if attestation.anchored and self.anchor_service:
            proof = self.anchor_service.get_proof(attestation.compute_hash())
            if not proof:
                return {
                    "valid": False,
                    "reason": "Blockchain anchor not found",
                }
            
            if not self.anchor_service.verify_event(attestation.compute_hash(), proof):
                return {
                    "valid": False,
                    "reason": "Blockchain verification failed",
                }
        
        return {
            "valid": True,
            "attestation_id": attestation_id,
            "type": attestation.type.value,
            "attester": attestation.attester,
            "anchored": attestation.anchored,
        }
    
    def anchor_attestation(self, attestation_id: str) -> bool:
        """
        Anchor an attestation to blockchain.
        
        Args:
            attestation_id: The attestation to anchor.
            
        Returns:
            True if anchoring was successful.
        """
        if not self.anchor_service:
            logger.warning("No anchor service configured")
            return False
        
        attestation = self.get(attestation_id)
        if not attestation:
            return False
        
        if attestation.anchored:
            logger.warning(f"Attestation {attestation_id} already anchored")
            return False
        
        # Add to anchor service
        self.anchor_service.add_event(attestation.compute_hash())
        
        # Create anchor
        anchor = self.anchor_service.create_anchor({
            "attestation_id": attestation_id,
            "type": attestation.type.value,
        })
        
        if anchor:
            # Submit to blockchain
            if self.anchor_service.submit_anchor(anchor.anchor_id):
                attestation.anchored = True
                attestation.anchor_tx = anchor.transaction_id
                logger.info(f"Attestation {attestation_id} anchored: {anchor.anchor_id}")
                return True
        
        return False
    
    def create_request(
        self,
        type: AttestationType,
        subject: str,
        claim: Dict[str, Any],
        requester: str,
        required_attesters: Optional[List[str]] = None,
        deadline: Optional[timedelta] = None
    ) -> AttestationRequest:
        """
        Create an attestation request.
        
        Args:
            type: Type of attestation needed.
            subject: Subject to attest to.
            claim: Claim to be attested.
            requester: Agent requesting attestation.
            required_attesters: Specific attesters needed.
            deadline: Time limit for attestation.
            
        Returns:
            Created AttestationRequest.
        """
        request_id = f"attest-req-{len(self._requests) + 1}"
        
        deadline_dt = None
        if deadline:
            deadline_dt = datetime.now(timezone.utc) + deadline
        
        request = AttestationRequest(
            request_id=request_id,
            type=type,
            subject=subject,
            claim=claim,
            requester=requester,
            required_attesters=required_attesters or [],
            deadline=deadline_dt,
        )
        
        self._requests[request_id] = request
        logger.info(f"Attestation request created: {request_id}")
        
        return request
    
    def fulfill_request(
        self,
        request_id: str,
        attester: str,
        evidence: Optional[List[str]] = None,
        sign_fn=None
    ) -> Optional[Attestation]:
        """
        Fulfill an attestation request.
        
        Args:
            request_id: The request to fulfill.
            attester: Agent providing attestation.
            evidence: Supporting evidence.
            sign_fn: Optional signing function.
            
        Returns:
            Created Attestation if successful.
        """
        request = self._requests.get(request_id)
        if not request or request.status != "pending":
            return None
        
        # Check if this attester is required
        if request.required_attesters and attester not in request.required_attesters:
            logger.warning(f"Attester {attester} not in required list for {request_id}")
            return None
        
        # Check deadline
        if request.deadline and datetime.now(timezone.utc) > request.deadline:
            request.status = "expired"
            return None
        
        # Create attestation
        attestation = self.create_attestation(
            type=request.type,
            subject=request.subject,
            claim=request.claim,
            attester=attester,
            evidence=evidence,
            sign_fn=sign_fn,
        )
        
        request.received_attestations.append(attester)
        
        if request.is_complete:
            request.status = "fulfilled"
            logger.info(f"Attestation request {request_id} fulfilled")
        
        return attestation
    
    def get_request(self, request_id: str) -> Optional[AttestationRequest]:
        """Get an attestation request."""
        return self._requests.get(request_id)
    
    def get_pending_requests(self, attester: Optional[str] = None) -> List[AttestationRequest]:
        """Get pending attestation requests."""
        requests = [
            r for r in self._requests.values()
            if r.status == "pending"
        ]
        
        if attester:
            requests = [
                r for r in requests
                if not r.required_attesters or attester in r.required_attesters
            ]
        
        return requests
    
    def export(self) -> Dict[str, Any]:
        """Export registry data."""
        return {
            "attestations": [a.to_dict() for a in self._attestations.values()],
            "requests": [r.to_dict() for r in self._requests.values()],
        }
