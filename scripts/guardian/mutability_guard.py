"""
Mutability Guard for Layer Protection

Extends the Guardian module to enforce protection of Layers 0-2 (Axioms, Purpose, 
Principles) from modification by the inductive memory system.

Protection Levels:
    - L0 (Axioms): .agentrules Layer 0, patterns/axioms/ - IMMUTABLE
    - L1 (Purpose): PURPOSE.md, patterns/purpose/ - IMMUTABLE  
    - L2 (Principles): patterns/principles/, patterns/enforcement/ - IMMUTABLE
    - L3-L4 (Methodology, Technical): Mutable by induction system

Usage:
    from scripts.guardian.mutability_guard import MutabilityGuard
    
    guard = MutabilityGuard()
    
    # Check if a file can be modified
    result = guard.can_modify("knowledge/fastapi-patterns.json")
    if result.allowed:
        # Proceed with modification
        pass
    else:
        print(f"Cannot modify: {result.reason}")
"""

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Any

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """
    Result of a mutability validation check.
    
    Attributes:
        allowed: Whether the modification is allowed
        reason: Explanation of why allowed/denied
        layer: Which layer the file belongs to (if any)
        path: The path that was checked
        policy: The protection policy applied
    """
    allowed: bool
    reason: str
    layer: Optional[str] = None
    path: Optional[str] = None
    policy: Optional[str] = None
    
    def __bool__(self) -> bool:
        """Allow using result in boolean context."""
        return self.allowed


# Protection configuration for each layer
PROTECTED_LAYERS: Dict[str, Dict[str, Any]] = {
    "L0": {
        "name": "Axioms & Guardian",
        "description": "Core axioms (A1-A5) and Guardian protocol - the foundation",
        "paths": [
            ".agentrules",  # Contains Layer 0 section
            "patterns/axioms/",
        ],
        "content_patterns": [
            r"# LAYER 0: INTEGRITY GUARDIAN",
            r"## Core Axioms \(Immutable\)",
            r"\*\*A[1-5]\*\*",  # Axiom references
        ],
        "policy": "immutable",
        "override": "never",
        "axiom_basis": ["A5_consistency"]
    },
    "L1": {
        "name": "Purpose",
        "description": "Mission, stakeholders, success criteria",
        "paths": [
            "PURPOSE.md",
            "patterns/purpose/",
        ],
        "content_patterns": [
            r"## Mission",
            r"## Stakeholders",
            r"## Success Criteria",
        ],
        "policy": "immutable",
        "override": "never",
        "axiom_basis": ["A2_user_primacy"]
    },
    "L2": {
        "name": "Principles",
        "description": "Ethical boundaries, quality standards, failure handling",
        "paths": [
            "patterns/principles/",
            "patterns/enforcement/",
        ],
        "content_patterns": [
            r"ethical.?boundaries",
            r"quality.?standards",
        ],
        "policy": "immutable",
        "override": "never",
        "axiom_basis": ["A4_non_harm", "A5_consistency"]
    }
}

# Paths that are explicitly mutable (for quick lookup)
MUTABLE_PATHS: List[str] = [
    "knowledge/",
    "blueprints/",
    "patterns/stacks/",
    "templates/",
    "data/",
]

# Files that are never modifiable regardless of path
NEVER_MODIFY: List[str] = [
    ".agentrules",
    "patterns/axioms/core-axioms.json",
    "patterns/axioms/axiom-zero.json",
    "patterns/principles/ethical-boundaries.json",
    "patterns/enforcement/integrity-enforcement.json",
]


class MutabilityGuard:
    """
    Guards against modifications to protected layers.
    
    Enforces the immutability of Layers 0-2 while allowing
    controlled modifications to Layers 3-4 (knowledge, blueprints, etc.).
    
    Attributes:
        config: Configuration dictionary
        protected_layers: Protection configuration for each layer
        
    Example:
        >>> guard = MutabilityGuard()
        >>> result = guard.can_modify("patterns/axioms/core-axioms.json")
        >>> print(result.allowed)  # False
        >>> print(result.reason)   # "Layer 0 (Axioms) is immutable"
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the mutability guard.
        
        Args:
            config_path: Path to memory-config.json for custom configuration.
        """
        self.config = self._load_config(config_path)
        self.protected_layers = PROTECTED_LAYERS.copy()
        
        # Apply any custom configuration
        if "protection" in self.config:
            self._apply_custom_config(self.config["protection"])
    
    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _apply_custom_config(self, protection_config: dict) -> None:
        """Apply custom protection configuration."""
        # Add custom protected paths
        if "protected_paths" in protection_config:
            for path in protection_config["protected_paths"]:
                if path not in NEVER_MODIFY:
                    NEVER_MODIFY.append(path)
        
        # Add custom mutable paths
        if "mutable_paths" in protection_config:
            for path in protection_config["mutable_paths"]:
                if path not in MUTABLE_PATHS:
                    MUTABLE_PATHS.append(path)
    
    def _normalize_path(self, path: str) -> str:
        """Normalize a path for comparison."""
        # Convert to forward slashes and remove leading ./
        normalized = str(path).replace("\\", "/")
        if normalized.startswith("./"):
            normalized = normalized[2:]
        return normalized
    
    def _get_layer_for_path(self, path: str) -> Optional[str]:
        """
        Determine which layer a path belongs to.
        
        Returns:
            Layer identifier (L0, L1, L2) or None if not in a protected layer.
        """
        normalized = self._normalize_path(path)
        
        for layer_id, layer_config in self.protected_layers.items():
            for protected_path in layer_config["paths"]:
                protected_normalized = self._normalize_path(protected_path)
                
                # Check exact match or path starts with protected path
                if normalized == protected_normalized:
                    return layer_id
                if normalized.startswith(protected_normalized):
                    return layer_id
        
        return None
    
    def _is_in_mutable_path(self, path: str) -> bool:
        """Check if path is in an explicitly mutable location."""
        normalized = self._normalize_path(path)
        
        for mutable_path in MUTABLE_PATHS:
            mutable_normalized = self._normalize_path(mutable_path)
            if normalized.startswith(mutable_normalized):
                return True
        
        return False
    
    def _is_never_modify(self, path: str) -> bool:
        """Check if path is in the never-modify list."""
        normalized = self._normalize_path(path)
        
        for never_path in NEVER_MODIFY:
            never_normalized = self._normalize_path(never_path)
            if normalized == never_normalized:
                return True
            if normalized.endswith(never_normalized):
                return True
        
        return False
    
    def can_modify(self, path: str) -> ValidationResult:
        """
        Check if a file/path can be modified.
        
        Args:
            path: Path to check (file or directory).
            
        Returns:
            ValidationResult with allowed status and reason.
            
        Example:
            >>> guard = MutabilityGuard()
            >>> result = guard.can_modify("knowledge/test.json")
            >>> if result.allowed:
            ...     print("Can modify!")
        """
        normalized = self._normalize_path(path)
        
        # Check never-modify list first
        if self._is_never_modify(normalized):
            return ValidationResult(
                allowed=False,
                reason="This file is in the never-modify list (core system file)",
                path=normalized,
                policy="never_modify"
            )
        
        # Check if in a protected layer
        layer = self._get_layer_for_path(normalized)
        if layer:
            layer_config = self.protected_layers[layer]
            return ValidationResult(
                allowed=False,
                reason=f"Layer {layer[1]} ({layer_config['name']}) is immutable - "
                       f"protected by axiom basis: {', '.join(layer_config['axiom_basis'])}",
                layer=layer,
                path=normalized,
                policy=layer_config["policy"]
            )
        
        # Check if in explicitly mutable path
        if self._is_in_mutable_path(normalized):
            return ValidationResult(
                allowed=True,
                reason="Path is in a mutable location (knowledge, blueprints, etc.)",
                path=normalized,
                policy="mutable"
            )
        
        # Default: allow with warning for unknown paths
        logger.warning(f"Path not in known locations, allowing with caution: {normalized}")
        return ValidationResult(
            allowed=True,
            reason="Path not in known protected or mutable locations - proceed with caution",
            path=normalized,
            policy="unknown"
        )
    
    def validate_modification(
        self, 
        path: str, 
        content: str,
        check_content: bool = True
    ) -> ValidationResult:
        """
        Validate a proposed modification to a file.
        
        Checks both path protection and content for axiom violations.
        
        Args:
            path: Path to the file being modified.
            content: The proposed new content.
            check_content: Whether to check content for axiom violations.
            
        Returns:
            ValidationResult with validation status.
        """
        # First check path-based protection
        path_result = self.can_modify(path)
        if not path_result.allowed:
            return path_result
        
        # Optionally check content for axiom references
        if check_content:
            content_result = self._check_content_for_violations(content)
            if not content_result.allowed:
                return content_result
        
        return ValidationResult(
            allowed=True,
            reason="Modification validated - path is mutable and content is valid",
            path=self._normalize_path(path),
            policy="validated"
        )
    
    def _check_content_for_violations(self, content: str) -> ValidationResult:
        """
        Check content for potential axiom violations.
        
        Looks for patterns that might indicate an attempt to modify
        or contradict axioms.
        """
        # Patterns that suggest axiom modification attempts
        violation_patterns = [
            (r"override.*(axiom|A[1-5])", "Attempt to override axioms"),
            (r"ignore.*(axiom|A[1-5])", "Attempt to ignore axioms"),
            (r"disable.*(guardian|protection)", "Attempt to disable protection"),
            (r"skip.*(validation|verification)", "Attempt to skip validation"),
        ]
        
        content_lower = content.lower()
        
        for pattern, description in violation_patterns:
            if re.search(pattern, content_lower):
                return ValidationResult(
                    allowed=False,
                    reason=f"Content contains potential axiom violation: {description}",
                    policy="content_violation"
                )
        
        return ValidationResult(
            allowed=True,
            reason="Content validation passed",
            policy="content_valid"
        )
    
    def get_layer_info(self, layer_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific layer.
        
        Args:
            layer_id: Layer identifier (L0, L1, L2).
            
        Returns:
            Layer configuration dictionary or None.
        """
        return self.protected_layers.get(layer_id)
    
    def get_all_protected_paths(self) -> List[str]:
        """
        Get all protected paths.
        
        Returns:
            List of all paths protected by any layer.
        """
        paths = []
        for layer_config in self.protected_layers.values():
            paths.extend(layer_config["paths"])
        paths.extend(NEVER_MODIFY)
        return list(set(paths))
    
    def get_protection_summary(self) -> str:
        """
        Get a human-readable summary of protection configuration.
        
        Returns:
            Formatted string describing protection levels.
        """
        lines = ["**Layer Protection Summary**\n"]
        
        for layer_id, config in self.protected_layers.items():
            lines.append(f"**{layer_id}: {config['name']}** ({config['policy']})")
            lines.append(f"  Description: {config['description']}")
            lines.append(f"  Protected paths: {', '.join(config['paths'])}")
            lines.append(f"  Axiom basis: {', '.join(config['axiom_basis'])}")
            lines.append("")
        
        lines.append("**Mutable Paths:**")
        lines.append(f"  {', '.join(MUTABLE_PATHS)}")
        
        return "\n".join(lines)


# Singleton instance for convenience
_default_guard: Optional[MutabilityGuard] = None


def get_mutability_guard(config_path: Optional[str] = None) -> MutabilityGuard:
    """
    Get or create the default mutability guard instance.
    
    Args:
        config_path: Config path (only applies on first call).
        
    Returns:
        MutabilityGuard instance.
    """
    global _default_guard
    
    if _default_guard is None:
        _default_guard = MutabilityGuard(config_path=config_path)
    
    return _default_guard
