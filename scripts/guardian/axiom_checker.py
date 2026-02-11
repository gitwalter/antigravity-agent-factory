"""
Axiom Checker - Validates operations against core axioms.

This module provides fast, pattern-based validation without LLM calls.
Execution time: <10ms for typical operations.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any
from pathlib import Path


class AxiomViolation(Enum):
    """Types of axiom violations."""
    NONE = 0
    A1_UNVERIFIABLE = 1
    A2_USER_OVERRIDE = 2
    A3_HIDDEN_LOGIC = 3
    A4_HARMFUL = 4
    A5_INCONSISTENT = 5


@dataclass
class CheckResult:
    """Result of an axiom check."""
    passed: bool
    level: int  # 0-4 based on severity
    axiom: Optional[str] = None
    violation: Optional[AxiomViolation] = None
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    
    @property
    def requires_user(self) -> bool:
        """Whether this result requires user intervention."""
        return self.level >= 2
    
    @property
    def is_emergency(self) -> bool:
        """Whether this is a Level 4 emergency."""
        return self.level >= 4


# Patterns for A4 (Non-Harm) violations
DESTRUCTIVE_PATTERNS = [
    # File system dangers
    (r'\brm\s+-rf\s+[/~]', "Recursive deletion of root or home directory"),
    (r'\brmdir\s+/s\s+/q\s+[A-Z]:\\', "Recursive Windows directory deletion"),
    (r'Remove-Item.*-Recurse.*-Force.*[/\\]$', "PowerShell recursive root deletion"),
    (r'\bformat\s+[A-Z]:', "Disk format command"),
    (r'\bdd\s+.*of=/dev/', "Direct disk write"),
    
    # Database dangers
    (r'DROP\s+DATABASE', "Database drop command"),
    (r'DROP\s+TABLE(?!.*IF\s+EXISTS)', "Table drop without IF EXISTS"),
    (r'TRUNCATE\s+TABLE', "Table truncation"),
    (r'DELETE\s+FROM\s+\w+\s*(?:;|$)', "DELETE without WHERE clause"),
    
    # System dangers
    (r'\bkill\s+-9\s+-1', "Kill all processes"),
    (r'\bshutdown\b', "System shutdown"),
    (r'\breboot\b', "System reboot"),
]

# Patterns for sensitive file access
SENSITIVE_PATHS = [
    r'\.env(?:\.local|\.prod(?:uction)?|\.secret)?$',
    r'secrets?\.ya?ml$',
    r'credentials?\.json$',
    r'\.ssh/id_',
    r'\.aws/credentials',
    r'\.kube/config',
]

# Critical system paths
CRITICAL_PATHS = [
    r'^/etc/',
    r'^/usr/',
    r'^/bin/',
    r'^/sbin/',
    r'^C:\\Windows\\',
    r'^C:\\Program Files',
]


def check_command(command: str) -> CheckResult:
    """
    Check a shell command for potential axiom violations.
    
    Args:
        command: The shell command to check
        
    Returns:
        CheckResult with violation details if any
    """
    command_lower = command.lower()    
    # Check for destructive patterns (A4)
    for pattern, description in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return CheckResult(
                passed=False,
                level=4,
                axiom="A4",
                violation=AxiomViolation.A4_HARMFUL,
                message=f"Potentially harmful command detected: {description}",
                details={"command": command, "pattern": pattern}
            )
    
    # Check for operations on sensitive paths (A4, lower severity)
    for pattern in SENSITIVE_PATHS:
        if re.search(pattern, command, re.IGNORECASE):
            return CheckResult(
                passed=False,
                level=2,
                axiom="A4",
                violation=AxiomViolation.A4_HARMFUL,
                message="Command involves sensitive file",
                details={"command": command, "pattern": pattern}
            )
    
    # Check for operations on critical system paths
    for pattern in CRITICAL_PATHS:
        if re.search(pattern, command, re.IGNORECASE):
            return CheckResult(
                passed=False,
                level=3,
                axiom="A4",
                violation=AxiomViolation.A4_HARMFUL,
                message="Command involves critical system path",
                details={"command": command, "pattern": pattern}
            )
    
    return CheckResult(passed=True, level=0)


def check_file_operation(operation: str, file_path: str) -> CheckResult:
    """
    Check a file operation for potential axiom violations.
    
    Args:
        operation: The operation type ('write', 'delete', 'move', etc.)
        file_path: The target file path
        
    Returns:
        CheckResult with violation details if any
    """
    path = Path(file_path)
    operation = operation.lower()
    
    # Deletion operations need extra scrutiny
    if operation in ('delete', 'remove', 'rm'):
        # Check for sensitive files
        for pattern in SENSITIVE_PATHS:
            if re.search(pattern, str(path), re.IGNORECASE):
                return CheckResult(
                    passed=False,
                    level=3,
                    axiom="A4",
                    violation=AxiomViolation.A4_HARMFUL,
                    message=f"Deletion of sensitive file: {path}",
                    details={"operation": operation, "path": str(path)}
                )
        
        # Check for critical system files
        for pattern in CRITICAL_PATHS:
            if re.search(pattern, str(path), re.IGNORECASE):
                return CheckResult(
                    passed=False,
                    level=4,
                    axiom="A4",
                    violation=AxiomViolation.A4_HARMFUL,
                    message=f"Deletion of critical system file: {path}",
                    details={"operation": operation, "path": str(path)}
                )
    
    # Write to sensitive locations
    if operation in ('write', 'create', 'overwrite'):
        for pattern in CRITICAL_PATHS:
            if re.search(pattern, str(path), re.IGNORECASE):
                return CheckResult(
                    passed=False,
                    level=3,
                    axiom="A4",
                    violation=AxiomViolation.A4_HARMFUL,
                    message=f"Write to critical system location: {path}",
                    details={"operation": operation, "path": str(path)}
                )
    
    return CheckResult(passed=True, level=0)


def check_content_for_claims(content: str) -> CheckResult:
    """
    Check content for unverifiable claims (A1).
    
    This is a lightweight heuristic check. Full verification requires
    context that only the LLM has.
    
    Args:
        content: The content to check
        
    Returns:
        CheckResult with violation details if any
    """
    # Patterns that suggest claims needing verification
    claim_patterns = [
        (r'\b(always|never|definitely|certainly|guaranteed)\b', "Absolute claim"),
        (r'\baccording to\s+(?!the\s+(?:documentation|source|file))', "External reference claim"),
        (r'\b\d+\s*%', "Statistical claim"),
    ]
    
    # This is informational only - LLM context determines actual handling
    for pattern, description in claim_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return CheckResult(
                passed=True,  # Not a block, just awareness
                level=1,
                axiom="A1",
                message=f"Content contains {description} - verify if possible",
                details={"pattern": pattern}
            )
    
    return CheckResult(passed=True, level=0)


def validate_operation(operation_type: str, context: Dict[str, Any]) -> CheckResult:
    """
    Main validation entry point.
    
    Args:
        operation_type: Type of operation ('command', 'file_write', 'file_delete', etc.)
        context: Dictionary with operation-specific context
        
    Returns:
        CheckResult with the most severe violation found
    """
    if operation_type == 'command':
        return check_command(context.get('command', ''))
    
    elif operation_type in ('file_write', 'file_delete', 'file_move'):
        return check_file_operation(
            operation_type.replace('file_', ''),
            context.get('path', '')
        )
    
    elif operation_type == 'content':
        return check_content_for_claims(context.get('content', ''))
    
    return CheckResult(passed=True, level=0)


if __name__ == "__main__":
    # Quick self-test
    print("Axiom Checker Self-Test")
    print("=" * 40)
    
    tests = [
        ("command", {"command": "rm -rf /"}),
        ("command", {"command": "ls -la"}),
        ("command", {"command": "cat .env"}),
        ("file_delete", {"path": "/etc/passwd"}),
        ("file_write", {"path": "README.md"}),
    ]
    
    for op_type, ctx in tests:
        result = validate_operation(op_type, ctx)
        status = "PASS" if result.passed else f"LEVEL {result.level}"
        print(f"{op_type}: {ctx} -> {status}")
        if not result.passed:
            print(f"  -> {result.message}")
