"""
Contract Verifier

Verifies agent messages and actions against contracts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import logging

from lib.society.contracts.schema import AgentContract, Obligation
from lib.society.contracts.registry import ContractRegistry

logger = logging.getLogger(__name__)


class ContractStatus(Enum):
    """Status of contract verification."""
    NO_CONTRACT = "no_contract"
    VERIFIED = "verified"
    VIOLATION = "violation"
    PENDING_SIGNATURE = "pending_signature"
    EXPIRED = "expired"


class ViolationType(Enum):
    """Types of contract violations."""
    CAPABILITY = "capability"
    PROHIBITION = "prohibition"
    OBLIGATION = "obligation"
    AXIOM = "axiom"


@dataclass
class Violation:
    """
    Contract violation record.
    
    Attributes:
        type: Type of violation.
        message: Description of the violation.
        details: Additional violation details.
    """
    type: ViolationType
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.type.value,
            "message": self.message,
            "details": self.details,
        }


@dataclass
class ContractVerificationResult:
    """
    Result of contract verification.
    
    Attributes:
        status: Overall verification status.
        contract_id: ID of the verified contract (if any).
        violations: List of violations found.
        recommendation: Suggested action.
    """
    status: ContractStatus
    contract_id: Optional[str] = None
    violations: List[Violation] = field(default_factory=list)
    recommendation: str = ""
    
    def has_violations(self) -> bool:
        """Check if any violations were found."""
        return len(self.violations) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "status": self.status.value,
            "contract_id": self.contract_id,
            "violations": [v.to_dict() for v in self.violations],
            "recommendation": self.recommendation,
        }


@dataclass
class Message:
    """
    Agent message for verification.
    
    Attributes:
        action: The action being performed.
        payload: Action-specific data.
        timestamp: When the message was created.
    """
    action: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class ContractVerifier:
    """
    Verifies agent actions against contracts.
    
    Checks:
    - Capability: Agent has permission to perform action
    - Prohibition: Action is not forbidden
    - Obligation: Required actions are performed
    - Axiom: Actions align with declared axiom requirements
    
    Usage:
        verifier = ContractVerifier(registry)
        result = verifier.verify_message(sender, receiver, message)
        
        if result.has_violations():
            for v in result.violations:
                print(f"Violation: {v.message}")
    """
    
    def __init__(self, registry: ContractRegistry):
        """
        Initialize verifier.
        
        Args:
            registry: Contract registry for lookups.
        """
        self.registry = registry
        self._obligation_trackers: Dict[str, Dict[str, datetime]] = {}
    
    def verify_message(
        self,
        sender: str,
        receiver: str,
        message: Message
    ) -> ContractVerificationResult:
        """
        Verify a message against applicable contracts.
        
        Args:
            sender: Sender agent ID.
            receiver: Receiver agent ID.
            message: The message to verify.
            
        Returns:
            ContractVerificationResult with status and violations.
        """
        # Find applicable contracts
        contracts = self.registry.find_contracts(sender, receiver)
        
        if not contracts:
            return ContractVerificationResult(
                status=ContractStatus.NO_CONTRACT,
                recommendation="Establish contract before communication"
            )
        
        all_violations = []
        verified_contract = None
        
        for contract in contracts:
            violations = self._verify_against_contract(
                contract, sender, message
            )
            
            if not violations:
                # Found a contract that allows this action
                verified_contract = contract
                break
            
            all_violations.extend(violations)
        
        if verified_contract:
            return ContractVerificationResult(
                status=ContractStatus.VERIFIED,
                contract_id=verified_contract.contract_id,
            )
        
        return ContractVerificationResult(
            status=ContractStatus.VIOLATION,
            violations=all_violations,
            recommendation="Action violates contract terms",
        )
    
    def _verify_against_contract(
        self,
        contract: AgentContract,
        agent_id: str,
        message: Message
    ) -> List[Violation]:
        """Verify message against a specific contract."""
        violations = []
        
        # Check capability
        if not contract.has_capability(agent_id, message.action):
            violations.append(Violation(
                type=ViolationType.CAPABILITY,
                message=f"Agent lacks capability: {message.action}",
                details={
                    "agent_id": agent_id,
                    "action": message.action,
                    "role": contract.get_role(agent_id),
                },
            ))
        
        # Check prohibition
        if contract.is_prohibited(agent_id, message.action):
            violations.append(Violation(
                type=ViolationType.PROHIBITION,
                message=f"Action is prohibited: {message.action}",
                details={
                    "agent_id": agent_id,
                    "action": message.action,
                },
            ))
        
        return violations
    
    def verify_action(
        self,
        agent_id: str,
        action: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ContractVerificationResult:
        """
        Verify an agent action against all their contracts.
        
        Args:
            agent_id: The agent performing the action.
            action: The action being performed.
            context: Optional context data.
            
        Returns:
            ContractVerificationResult with status and violations.
        """
        # Find all contracts for this agent
        contracts = self.registry.find_contracts(agent_id)
        
        if not contracts:
            return ContractVerificationResult(
                status=ContractStatus.NO_CONTRACT,
            )
        
        all_violations = []
        verified = False
        
        for contract in contracts:
            # Check capability
            if contract.has_capability(agent_id, action):
                # Check prohibition
                if not contract.is_prohibited(agent_id, action):
                    verified = True
                    break
            
            # Collect violations
            if not contract.has_capability(agent_id, action):
                all_violations.append(Violation(
                    type=ViolationType.CAPABILITY,
                    message=f"Agent lacks capability: {action}",
                    details={"contract_id": contract.contract_id},
                ))
            
            if contract.is_prohibited(agent_id, action):
                all_violations.append(Violation(
                    type=ViolationType.PROHIBITION,
                    message=f"Action prohibited: {action}",
                    details={"contract_id": contract.contract_id},
                ))
        
        if verified:
            return ContractVerificationResult(
                status=ContractStatus.VERIFIED,
            )
        
        return ContractVerificationResult(
            status=ContractStatus.VIOLATION,
            violations=all_violations,
        )
    
    def track_obligation(
        self,
        contract_id: str,
        agent_id: str,
        trigger: str
    ) -> None:
        """
        Track that an obligation was triggered.
        
        Args:
            contract_id: The contract ID.
            agent_id: The obligated agent.
            trigger: The trigger event.
        """
        key = f"{contract_id}:{agent_id}"
        if key not in self._obligation_trackers:
            self._obligation_trackers[key] = {}
        
        self._obligation_trackers[key][trigger] = datetime.utcnow()
        logger.debug(f"Tracked obligation trigger: {trigger} for {agent_id}")
    
    def fulfill_obligation(
        self,
        contract_id: str,
        agent_id: str,
        action: str
    ) -> bool:
        """
        Mark an obligation as fulfilled.
        
        Args:
            contract_id: The contract ID.
            agent_id: The agent fulfilling.
            action: The fulfilled action.
            
        Returns:
            True if an obligation was fulfilled.
        """
        contract = self.registry.get(contract_id)
        if not contract:
            return False
        
        role = contract.get_role(agent_id)
        if not role:
            return False
        
        obligations = contract.obligations.get(role, [])
        
        for obligation in obligations:
            if obligation.action == action:
                key = f"{contract_id}:{agent_id}"
                if key in self._obligation_trackers:
                    self._obligation_trackers[key].pop(obligation.trigger, None)
                    logger.debug(f"Fulfilled obligation: {action} for {agent_id}")
                    return True
        
        return False
    
    def check_pending_obligations(
        self,
        contract_id: str,
        agent_id: str
    ) -> List[Obligation]:
        """
        Get pending (unfulfilled) obligations.
        
        Args:
            contract_id: The contract ID.
            agent_id: The agent to check.
            
        Returns:
            List of pending obligations.
        """
        contract = self.registry.get(contract_id)
        if not contract:
            return []
        
        role = contract.get_role(agent_id)
        if not role:
            return []
        
        key = f"{contract_id}:{agent_id}"
        tracked = self._obligation_trackers.get(key, {})
        
        pending = []
        for obligation in contract.obligations.get(role, []):
            if obligation.trigger in tracked:
                # Check if timeout exceeded
                triggered_at = tracked[obligation.trigger]
                timeout_ms = obligation.parameters.get("timeout_ms", 30000)
                elapsed_ms = (datetime.utcnow() - triggered_at).total_seconds() * 1000
                
                if elapsed_ms > timeout_ms:
                    pending.append(obligation)
        
        return pending
