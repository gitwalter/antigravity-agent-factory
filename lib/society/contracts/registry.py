"""
Contract Registry

Storage and lookup for agent contracts.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import logging
import threading

from lib.society.contracts.schema import AgentContract, Party

logger = logging.getLogger(__name__)


class ContractRegistry:
    """
    Registry for managing agent contracts.
    
    Features:
    - Contract storage and retrieval
    - Lookup by agent or party pair
    - Signature management
    - Optional persistence
    
    Usage:
        registry = ContractRegistry()
        contract = registry.create_contract(parties, capabilities)
        registry.sign(contract.contract_id, agent_id, signature)
        
        active = registry.find_contracts(agent_a, agent_b)
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize registry.
        
        Args:
            storage_path: Optional path for JSON persistence.
        """
        self.storage_path = Path(storage_path) if storage_path else None
        self._contracts: Dict[str, AgentContract] = {}
        self._lock = threading.RLock()
        
        if self.storage_path and self.storage_path.exists():
            self._load()
    
    @property
    def contracts(self) -> List[AgentContract]:
        """Get all contracts."""
        with self._lock:
            return list(self._contracts.values())
    
    @property
    def active_contracts(self) -> List[AgentContract]:
        """Get all active (signed and not expired) contracts."""
        with self._lock:
            return [c for c in self._contracts.values() if c.is_active]
    
    def add(self, contract: AgentContract) -> None:
        """
        Add a contract to the registry.
        
        Args:
            contract: The contract to add.
        """
        with self._lock:
            self._contracts[contract.contract_id] = contract
            logger.info(f"Added contract {contract.contract_id}")
            
            if self.storage_path:
                self._save()
    
    def get(self, contract_id: str) -> Optional[AgentContract]:
        """
        Get contract by ID.
        
        Args:
            contract_id: The contract ID.
            
        Returns:
            The contract if found.
        """
        with self._lock:
            return self._contracts.get(contract_id)
    
    def remove(self, contract_id: str) -> bool:
        """
        Remove a contract from the registry.
        
        Args:
            contract_id: The contract ID to remove.
            
        Returns:
            True if contract was found and removed.
        """
        with self._lock:
            if contract_id in self._contracts:
                del self._contracts[contract_id]
                logger.info(f"Removed contract {contract_id}")
                
                if self.storage_path:
                    self._save()
                return True
            return False
    
    def create_contract(
        self,
        parties: List[Party],
        capabilities: Dict[str, List[str]],
        **kwargs
    ) -> AgentContract:
        """
        Create and register a new contract.
        
        Args:
            parties: Contract parties.
            capabilities: Role -> action list mapping.
            **kwargs: Additional contract attributes.
            
        Returns:
            The created contract.
        """
        contract = AgentContract.create(parties, capabilities, **kwargs)
        self.add(contract)
        return contract
    
    def sign(
        self,
        contract_id: str,
        agent_id: str,
        signature: str
    ) -> bool:
        """
        Sign a contract.
        
        Args:
            contract_id: The contract to sign.
            agent_id: The signing agent.
            signature: The cryptographic signature.
            
        Returns:
            True if signature was added.
        """
        with self._lock:
            contract = self._contracts.get(contract_id)
            if not contract:
                logger.warning(f"Contract {contract_id} not found")
                return False
            
            # Verify agent is a party
            if not contract.get_party(agent_id):
                logger.warning(f"Agent {agent_id} is not a party to contract {contract_id}")
                return False
            
            # Add signature
            contract.signatures[agent_id] = signature
            logger.info(f"Agent {agent_id} signed contract {contract_id}")
            
            if contract.is_fully_signed:
                logger.info(f"Contract {contract_id} is now fully signed and active")
            
            if self.storage_path:
                self._save()
            
            return True
    
    def find_contracts(
        self,
        agent_a: str,
        agent_b: Optional[str] = None,
        active_only: bool = True
    ) -> List[AgentContract]:
        """
        Find contracts involving specified agents.
        
        Args:
            agent_a: First agent ID (required).
            agent_b: Optional second agent ID.
            active_only: Only return active contracts.
            
        Returns:
            Matching contracts.
        """
        with self._lock:
            results = []
            
            for contract in self._contracts.values():
                if active_only and not contract.is_active:
                    continue
                
                party_ids = {p.agent_id for p in contract.parties}
                
                # Check if agent_a is a party
                if agent_a not in party_ids:
                    continue
                
                # If agent_b specified, check if it's also a party
                if agent_b and agent_b not in party_ids:
                    continue
                
                results.append(contract)
            
            return results
    
    def find_by_role(
        self,
        agent_id: str,
        role: str,
        active_only: bool = True
    ) -> List[AgentContract]:
        """
        Find contracts where agent has specific role.
        
        Args:
            agent_id: The agent ID.
            role: The role to match.
            active_only: Only return active contracts.
            
        Returns:
            Matching contracts.
        """
        with self._lock:
            results = []
            
            for contract in self._contracts.values():
                if active_only and not contract.is_active:
                    continue
                
                agent_role = contract.get_role(agent_id)
                if agent_role == role:
                    results.append(contract)
            
            return results
    
    def get_agent_roles(self, agent_id: str) -> Dict[str, str]:
        """
        Get all roles an agent has across contracts.
        
        Args:
            agent_id: The agent ID.
            
        Returns:
            Dict mapping contract_id -> role.
        """
        with self._lock:
            roles = {}
            
            for contract in self._contracts.values():
                role = contract.get_role(agent_id)
                if role:
                    roles[contract.contract_id] = role
            
            return roles
    
    def cleanup_expired(self) -> int:
        """
        Remove expired contracts.
        
        Returns:
            Number of contracts removed.
        """
        with self._lock:
            now = datetime.utcnow()
            expired = [
                cid for cid, c in self._contracts.items()
                if c.expires and c.expires < now
            ]
            
            for cid in expired:
                del self._contracts[cid]
            
            if expired:
                logger.info(f"Cleaned up {len(expired)} expired contracts")
                if self.storage_path:
                    self._save()
            
            return len(expired)
    
    def export(self) -> Dict[str, any]:
        """Export registry data."""
        with self._lock:
            return {
                "contracts": {
                    cid: c.to_dict() for cid, c in self._contracts.items()
                }
            }
    
    def _save(self) -> None:
        """Save to storage file."""
        if not self.storage_path:
            return
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.storage_path, "w") as f:
            json.dump(self.export(), f, indent=2)
    
    def _load(self) -> None:
        """Load from storage file."""
        if not self.storage_path or not self.storage_path.exists():
            return
        
        with open(self.storage_path, "r") as f:
            data = json.load(f)
        
        for cid, cdata in data.get("contracts", {}).items():
            self._contracts[cid] = AgentContract.from_dict(cdata)
