"""
Layer 0 Integrity Guardian - Technical Immune System

This module provides fast, LLM-free validation for the Guardian.
All checks are pattern-based and execute in milliseconds.

Components:
    - axiom_checker: Validates operations against core axioms
    - harm_detector: Detects potentially harmful operations
    - secret_scanner: Detects credentials and secrets in content
    - conflict_detector: Detects potential agent conflicts
    - mutability_guard: Protects Layers 0-2 from modification

Usage:
    from scripts.guardian import axiom_checker, harm_detector, secret_scanner
    from scripts.guardian.mutability_guard import MutabilityGuard, get_mutability_guard

    # Check for axiom violations
    result = axiom_checker.check_operation(operation_type, context)

    # Check for harmful patterns
    result = harm_detector.scan_content(content)

    # Check for secrets
    result = secret_scanner.scan_file(file_path)

    # Check if a file can be modified (Layer protection)
    guard = get_mutability_guard()
    result = guard.can_modify("knowledge/test.json")
"""

__version__ = "1.0.0"
__author__ = "Antigravity Agent Factory"
from pathlib import Path

# Guardian script directory
GUARDIAN_DIR = Path(__file__).parent

# Core axiom definitions
AXIOMS = {
    "A1": {
        "name": "Verifiability",
        "statement": "All outputs must be verifiable against source",
        "checks": ["unverified_claims", "missing_sources", "hallucination_patterns"],
    },
    "A2": {
        "name": "User Primacy",
        "statement": "User intent takes precedence over agent convenience",
        "checks": ["assumption_without_clarification", "override_user_preference"],
    },
    "A3": {
        "name": "Transparency",
        "statement": "Reasoning must be explainable on request",
        "checks": ["hidden_logic", "silent_failures", "unexplained_decisions"],
    },
    "A4": {
        "name": "Non-Harm",
        "statement": "No action may knowingly cause harm to users or systems",
        "checks": ["destructive_operations", "security_risks", "data_exposure"],
    },
    "A5": {
        "name": "Consistency",
        "statement": "No rule may contradict these axioms",
        "checks": ["axiom_conflicts", "rule_contradictions"],
    },
}

# Response levels
LEVELS = {
    0: {"name": "Flow", "action": "continue"},
    1: {"name": "Nudge", "action": "self_correct"},
    2: {"name": "Pause", "action": "ask_user"},
    3: {"name": "Block", "action": "stop_explain"},
    4: {"name": "Protect", "action": "prevent_harm"},
}
