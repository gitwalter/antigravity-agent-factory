"""
Agent Contracts Module

Formal agreements defining agent capabilities, obligations, and prohibitions
based on deontic logic (permitted/obligated/forbidden).
"""

from lib.society.contracts.schema import (
    DisputeMethod,
    Party,
    Capability,
    Obligation,
    Prohibition,
    DisputeResolution,
    AxiomRequirements,
    AgentContract,
)
from lib.society.contracts.registry import ContractRegistry
from lib.society.contracts.verifier import (
    ContractStatus,
    ViolationType,
    Violation,
    ContractVerifier,
    ContractVerificationResult,
)

__all__ = [
    "DisputeMethod",
    "Party",
    "Capability",
    "Obligation",
    "Prohibition",
    "DisputeResolution",
    "AxiomRequirements",
    "AgentContract",
    "ContractRegistry",
    "ContractStatus",
    "ViolationType",
    "Violation",
    "ContractVerifier",
    "ContractVerificationResult",
]
