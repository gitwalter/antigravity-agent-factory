"""
Harm Detector - Detects potentially harmful operations.

This module provides comprehensive harm detection without LLM calls.
Combines axiom checking, secret scanning, and additional patterns.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
try:
    from . import axiom_checker
    from . import secret_scanner
except ImportError:
    # Allow running as standalone script for testing
    import axiom_checker
    import secret_scanner


@dataclass
class HarmReport:
    """Comprehensive harm assessment report."""
    safe: bool
    level: int  # 0-4 Guardian response level
    category: str  # 'command', 'file', 'content', 'secret', 'combined'
    summary: str
    details: List[str]
    recommendations: List[str]
    
    def __str__(self):
        if self.safe:
            return "No harm detected"
        return f"[LEVEL {self.level}] {self.category}: {self.summary}"


# Patterns for potentially harmful content generation
HARMFUL_CONTENT_PATTERNS = [
    # Deceptive patterns (A3 - Transparency)
    (r'(?i)pretend\s+to\s+be\s+(?:a\s+)?human', "Deceptive identity claim", "A3"),
    (r"(?i)don'?t\s+tell\s+(?:the\s+)?user", "Hidden information from user", "A3"),
    
    # Instruction override attempts (A5 - Consistency)
    (r'(?i)ignore\s+(?:all\s+)?(?:previous\s+)?instructions', "Instruction override attempt", "A5"),
    (r'(?i)disregard\s+(?:all\s+)?(?:previous\s+)?(?:instructions|rules)', "Instruction override attempt", "A5"),
    
    # Manipulation patterns (A4 - Non-Harm)
    (r'(?i)manipulate\s+(?:the\s+)?user', "User manipulation", "A4"),
    (r'(?i)trick\s+(?:the\s+)?user', "User deception", "A4"),
    
    # Harmful action patterns (A4 - Non-Harm)
    (r'(?i)bypass\s+(?:security|authentication|authorization)', "Security bypass", "A4"),
    (r'(?i)exfiltrate\s+data', "Data exfiltration", "A4"),
    (r'(?i)cover\s+(?:up|your)\s+tracks', "Evidence concealment", "A3"),
]

# File patterns that should trigger extra caution
CAUTION_FILE_PATTERNS = [
    (r'\.agentrules$', "Modifying agent behavior rules"),
    (r'\.env', "Environment/secrets file"),
    (r'package\.json$', "Package dependencies"),
    (r'requirements\.txt$', "Python dependencies"),
    (r'Gemfile$', "Ruby dependencies"),
    (r'go\.mod$', "Go dependencies"),
    (r'Dockerfile', "Container configuration"),
    (r'docker-compose', "Container orchestration"),
    (r'\.github/workflows', "CI/CD pipeline"),
    (r'gitlab-ci\.yml', "CI/CD pipeline"),
]


def analyze_command(command: str) -> HarmReport:
    """
    Analyze a shell command for potential harm.
    
    Args:
        command: The command to analyze
        
    Returns:
        HarmReport with analysis results
    """
    result = axiom_checker.check_command(command)
    
    if result.passed:
        return HarmReport(
            safe=True,
            level=0,
            category="command",
            summary="Command appears safe",
            details=[],
            recommendations=[]
        )
    
    return HarmReport(
        safe=False,
        level=result.level,
        category="command",
        summary=result.message or "Potentially harmful command",
        details=[f"Axiom: {result.axiom}", f"Pattern matched: {result.details.get('pattern', 'N/A')}"],
        recommendations=[
            "Review the command carefully before execution",
            "Consider if there's a safer alternative",
            "Ensure you have backups if this is destructive"
        ]
    )


def analyze_file_operation(operation: str, path: str, content: Optional[str] = None) -> HarmReport:
    """
    Analyze a file operation for potential harm.
    
    Args:
        operation: The operation type ('write', 'delete', etc.)
        path: The file path
        content: Optional file content to analyze
        
    Returns:
        HarmReport with analysis results
    """
    details = []
    recommendations = []
    max_level = 0
    
    # Check operation against axioms
    op_result = axiom_checker.check_file_operation(operation, path)
    if not op_result.passed:
        max_level = max(max_level, op_result.level)
        details.append(op_result.message)
    
    # Check for caution-worthy files
    for pattern, reason in CAUTION_FILE_PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            max_level = max(max_level, 2)  # At least pause level
            details.append(f"Caution: {reason}")
            recommendations.append(f"This file affects {reason.lower()}")
    
    # If content provided, scan for secrets
    if content:
        secrets = secret_scanner.scan_content(content)
        if secrets:
            secret_level = secret_scanner.get_severity_level(secrets)
            max_level = max(max_level, secret_level)
            details.append(f"Found {len(secrets)} potential secret(s)")
            for s in secrets[:3]:  # Show first 3
                details.append(f"  - {s}")
            recommendations.append("Remove secrets and use environment variables")
    
    if max_level == 0:
        return HarmReport(
            safe=True,
            level=0,
            category="file",
            summary="File operation appears safe",
            details=[],
            recommendations=[]
        )
    
    return HarmReport(
        safe=False,
        level=max_level,
        category="file",
        summary=f"File operation requires attention: {path}",
        details=details,
        recommendations=recommendations
    )


def analyze_content(content: str) -> HarmReport:
    """
    Analyze content for harmful patterns.
    
    Args:
        content: The content to analyze
        
    Returns:
        HarmReport with analysis results
    """
    details = []
    max_level = 0
    axioms_involved = set()
    
    # Check for harmful content patterns
    for pattern, description, axiom in HARMFUL_CONTENT_PATTERNS:
        if re.search(pattern, content):
            max_level = max(max_level, 3)  # Block level
            details.append(f"{description} ({axiom})")
            axioms_involved.add(axiom)
    
    # Check for secrets
    secrets = secret_scanner.scan_content(content)
    if secrets:
        secret_level = secret_scanner.get_severity_level(secrets)
        max_level = max(max_level, secret_level)
        details.append(f"Contains {len(secrets)} potential secret(s)")
        axioms_involved.add("A4")
    
    # Check for unverifiable claims (informational)
    claims_result = axiom_checker.check_content_for_claims(content)
    if claims_result.level > 0:
        details.append(claims_result.message)
    
    if max_level == 0:
        return HarmReport(
            safe=True,
            level=0,
            category="content",
            summary="Content appears safe",
            details=[],
            recommendations=[]
        )
    
    return HarmReport(
        safe=False,
        level=max_level,
        category="content",
        summary="Content contains concerning patterns",
        details=details,
        recommendations=[
            "Review flagged patterns carefully",
            f"Axioms involved: {', '.join(axioms_involved)}"
        ]
    )


def comprehensive_check(
    command: Optional[str] = None,
    file_path: Optional[str] = None,
    file_operation: Optional[str] = None,
    content: Optional[str] = None
) -> HarmReport:
    """
    Perform comprehensive harm analysis on multiple inputs.
    
    Args:
        command: Optional shell command to check
        file_path: Optional file path to check
        file_operation: Optional file operation type
        content: Optional content to check
        
    Returns:
        HarmReport with combined analysis
    """
    reports = []
    
    if command:
        reports.append(analyze_command(command))
    
    if file_path and file_operation:
        reports.append(analyze_file_operation(file_operation, file_path, content))
    elif content:
        reports.append(analyze_content(content))
    
    # Combine reports
    if not reports:
        return HarmReport(
            safe=True,
            level=0,
            category="combined",
            summary="Nothing to check",
            details=[],
            recommendations=[]
        )
    
    # Find highest level
    max_level = max(r.level for r in reports)
    unsafe_reports = [r for r in reports if not r.safe]
    
    if not unsafe_reports:
        return HarmReport(
            safe=True,
            level=0,
            category="combined",
            summary="All checks passed",
            details=[],
            recommendations=[]
        )
    
    return HarmReport(
        safe=False,
        level=max_level,
        category="combined",
        summary=f"{len(unsafe_reports)} issue(s) detected",
        details=[d for r in unsafe_reports for d in r.details],
        recommendations=list(set(rec for r in unsafe_reports for rec in r.recommendations))
    )


if __name__ == "__main__":
    # Quick self-test
    print("Harm Detector Self-Test")
    print("=" * 40)
    
    # Test command
    print("\n1. Testing dangerous command:")
    report = analyze_command("rm -rf /")
    print(f"   {report}")
    
    # Test file with secrets
    print("\n2. Testing content with secrets:")
    test_content = 'api_key = "sk-1234567890abcdefghijklmnopqrstuv"'
    report = analyze_content(test_content)
    print(f"   {report}")
    for d in report.details:
        print(f"     - {d}")
    
    # Test safe operation
    print("\n3. Testing safe operation:")
    report = analyze_command("ls -la")
    print(f"   {report}")
    
    print("\n" + "=" * 40)
    print("Self-test complete")
