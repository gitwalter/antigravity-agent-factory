"""
Hybrid Verification Module

Combines all verification approaches into a unified system.

Components:
- HybridVerificationSystem: Unified verification combining all approaches
- EscalationManager: Violation escalation and resolution
- SystemConfig: Configuration for hybrid verification
"""

from lib.society.hybrid.system import (
    VerificationLevel,
    SystemConfig,
    HybridVerificationResult,
    HybridVerificationSystem,
)
from lib.society.hybrid.escalation import (
    EscalationLevel,
    EscalationStatus,
    Escalation,
    EscalationPolicy,
    DefaultPolicy,
    EscalationManager,
    create_escalation_from_violation,
)

__all__ = [
    # System
    "VerificationLevel",
    "SystemConfig",
    "HybridVerificationResult",
    "HybridVerificationSystem",
    # Escalation
    "EscalationLevel",
    "EscalationStatus",
    "Escalation",
    "EscalationPolicy",
    "DefaultPolicy",
    "EscalationManager",
    "create_escalation_from_violation",
]
