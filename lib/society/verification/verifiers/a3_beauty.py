"""
A3 Beauty Verifier

Verifies actions exhibit simplicity and elegance.
Checks for unnecessary complexity and promotes clean design.
"""

from lib.society.events.schema import AgentEvent
from lib.society.verification.verifiers.base import AxiomVerifier, AxiomId, AxiomResult


class A3BeautyVerifier(AxiomVerifier):
    """
    Verifies actions exhibit simplicity and elegance (A3: Beauty).
    
    Checks for:
    - Absence of unnecessary complexity
    - Clean, focused actions
    - Elegant solutions over complicated ones
    
    Note: This axiom is primarily about design quality and is
    checked with lower confidence as it's more subjective.
    """
    
    # Keywords indicating unnecessary complexity
    COMPLEXITY_KEYWORDS = [
        "workaround",
        "hack",
        "kludge",
        "band-aid",
        "quick fix",
        "temporary",
        "TODO",
        "FIXME",
        "complicated",
        "convoluted",
    ]
    
    # Keywords indicating elegance
    ELEGANCE_KEYWORDS = [
        "elegant",
        "simple",
        "clean",
        "minimal",
        "focused",
        "streamlined",
        "refined",
        "polished",
    ]
    
    @property
    def axiom(self) -> AxiomId:
        return AxiomId.A3_BEAUTY
    
    @property
    def description(self) -> str:
        return "Verifies actions exhibit simplicity and elegance"
    
    def verify(self, event: AgentEvent) -> AxiomResult:
        """Check if action exhibits beauty (simplicity, elegance)."""
        description = event.action.description.lower()
        justification = event.axiom_context.justification.lower()
        combined_text = f"{description} {justification}"
        
        # Check for complexity indicators
        complexity_matches = self._check_keywords(
            combined_text, 
            self.COMPLEXITY_KEYWORDS
        )
        if complexity_matches:
            return self._make_fail(
                reason=f"Action may be unnecessarily complex: {', '.join(complexity_matches)}",
                confidence=0.5,  # Lower confidence - subjective
                matched_keywords=complexity_matches,
                pattern="complexity",
            )
        
        # Check for elegance indicators (positive)
        elegance_matches = self._check_keywords(combined_text, self.ELEGANCE_KEYWORDS)
        
        # Check payload for complexity signals
        payload = event.action.payload
        if self._is_overly_complex(payload):
            return self._make_fail(
                reason="Action payload appears overly complex",
                confidence=0.4,
                pattern="complex_payload",
            )
        
        return self._make_pass(
            reason="Action appears simple and focused" if not elegance_matches 
                   else "Action exhibits elegance",
            confidence=0.7 if elegance_matches else 0.5,
            elegance_indicators=elegance_matches,
        )
    
    def _is_overly_complex(self, payload: dict) -> bool:
        """Check if payload structure is overly complex."""
        # Deep nesting is a complexity smell
        depth = self._get_dict_depth(payload)
        if depth > 5:
            return True
        
        # Too many keys at one level
        if len(payload) > 20:
            return True
        
        return False
    
    def _get_dict_depth(self, d: dict, current_depth: int = 1) -> int:
        """Get the maximum nesting depth of a dictionary."""
        if not isinstance(d, dict) or not d:
            return current_depth
        
        max_depth = current_depth
        for value in d.values():
            if isinstance(value, dict):
                depth = self._get_dict_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)
        
        return max_depth
