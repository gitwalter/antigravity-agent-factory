"""
Secret Scanner - Detects credentials and secrets in content.

This module provides fast, pattern-based secret detection without LLM calls.
Execution time: <50ms for typical file sizes.

Based on common secret patterns from security tools like:
- gitleaks
- truffleHog
- detect-secrets
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple
from pathlib import Path


@dataclass
class SecretMatch:
    """A detected secret in content."""
    pattern_name: str
    matched_text: str
    line_number: int
    severity: str  # 'high', 'medium', 'low'
    redacted: str  # Safe version for display
    
    def __str__(self):
        return f"[{self.severity.upper()}] {self.pattern_name} at line {self.line_number}: {self.redacted}"


# Secret patterns with severity levels
SECRET_PATTERNS = [
    # API Keys - High Severity
    (r'sk-(?:["\']\s*\+\s*["\'])?[a-zA-Z0-9]{20,}', "OpenAI API Key", "high"),
    (r'sk-proj-(?:["\']\s*\+\s*["\'])?[a-zA-Z0-9]{20,}', "OpenAI Project API Key", "high"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID", "high"),
    (r"(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]", "AWS Secret Key", "high"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token", "high"),
    (r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}', "GitHub Fine-Grained PAT", "high"),
    (r'gho_[a-zA-Z0-9]{36}', "GitHub OAuth Token", "high"),
    (r'glpat-[a-zA-Z0-9\-]{20,}', "GitLab Personal Access Token", "high"),
    (r'xox[baprs]-[0-9]{10,}-[0-9]{10,}-[a-zA-Z0-9]{24}', "Slack Token", "high"),
    (r"(?i)heroku.{0,20}['\"][0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}['\"]", "Heroku API Key", "high"),
    (r'SG\.[a-zA-Z0-9]{22}\.[a-zA-Z0-9]{43}', "SendGrid API Key", "high"),
    (r"(?i)stripe.{0,20}[sr]k_live_[0-9a-zA-Z]{24,}", "Stripe Live Key", "high"),
    (r'sq0atp-[0-9A-Za-z\-_]{22}', "Square Access Token", "high"),
    (r'AIza[0-9A-Za-z\-_]{20,}', "Google API Key", "high"),
    (r'ya29\.[0-9A-Za-z\-_]+', "Google OAuth Token", "high"),
    
    # Private Keys - High Severity
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', "Private Key", "high"),
    (r'-----BEGIN PGP PRIVATE KEY BLOCK-----', "PGP Private Key", "high"),
    
    # Database Connection Strings - High Severity
    (r'(?i)mongodb(?:\+srv)?://[^/\s]+:[^@/\s]+@', "MongoDB Connection String", "high"),
    (r'(?i)postgres(?:ql)?://[^/\s]+:[^@/\s]+@', "PostgreSQL Connection String", "high"),
    (r'(?i)postgres(?:ql)?://[^/\s]+:["\']\s*\+\s*["\'][^@/\s]+@', "PostgreSQL Connection String (Concatenated)", "high"),
    (r'(?i)mysql://[^/\s]+:[^@/\s]+@', "MySQL Connection String", "high"),
    (r'(?i)redis://[^/\s]+:[^@/\s]+@', "Redis Connection String", "high"),
    
    # Medium Severity - May be intentional but should verify
    (r"(?i)password\s*[=:]\s*[\"'][^\"']{8,}[\"']", "Hardcoded Password", "medium"),
    (r"(?i)password\s*[=:]\s*[\"'][^\"']{4,}[\"']\s*\+\s*[\"'][^\"']{4,}[\"']", "Hardcoded Password (Concatenated)", "medium"),
    (r"(?i)api[_-]?key\s*[=:]\s*[\"'][^\"']{16,}[\"']", "Generic API Key", "medium"),
    (r"(?i)api[_-]?key\s*[=:]\s*[\"'][^\"']{2,}[\"']\s*\+\s*[\"'][^\"']{8,}[\"']", "Generic API Key (Concatenated)", "medium"),
    (r"(?i)secret\s*[=:]\s*[\"'][^\"']{16,}[\"']", "Generic Secret", "medium"),
    (r"(?i)token\s*[=:]\s*[\"'][^\"']{20,}[\"']", "Generic Token", "medium"),
    (r"(?i)auth\s*[=:]\s*[\"'][^\"']{16,}[\"']", "Auth Credential", "medium"),
    
    # Low Severity - Usually false positives but worth flagging
    (r'(?i)bearer\s+[a-zA-Z0-9\-_.~+/]+=*', "Bearer Token", "low"),
    (r'[a-fA-F0-9]{64}', "Possible SHA256 Hash (could be secret)", "low"),
]

# Patterns that look like secrets but are usually safe
FALSE_POSITIVE_PATTERNS = [
    r'example',  # Contains "example"
    r'sample',   # Contains "sample"
    r'placeholder',  # Contains "placeholder"
    r'your[-_]?api[-_]?key',  # Contains your-api-key
    r'["\']x{8,}["\']',  # Quoted string of just x's
    r'["\']X{8,}["\']',  # Quoted string of just X's
    r'["\']\*{8,}["\']',  # Quoted string of just asterisks
    r'<[^>]+>',  # Template placeholders like <your-key>
    r'\$\{[^}]+\}',  # Variable placeholders like ${API_KEY}
    r'%\([^)]+\)s?',  # Python format strings
]


def redact_secret(text: str) -> str:
    """Redact a secret for safe display."""
    if len(text) <= 8:
        return '*' * len(text)
    return text[:4] + '*' * (len(text) - 8) + text[-4:]


def is_false_positive(text: str) -> bool:
    """Check if a match is likely a false positive."""
    text_lower = text.lower()
    for pattern in FALSE_POSITIVE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def scan_content(content: str) -> List[SecretMatch]:
    """
    Scan content for secrets.
    
    Args:
        content: The text content to scan
        
    Returns:
        List of SecretMatch objects for detected secrets
    """
    matches = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern, name, severity in SECRET_PATTERNS:
            for match in re.finditer(pattern, line):
                matched_text = match.group()
                
                # Skip false positives
                if is_false_positive(matched_text):
                    continue
                
                matches.append(SecretMatch(
                    pattern_name=name,
                    matched_text=matched_text,
                    line_number=line_num,
                    severity=severity,
                    redacted=redact_secret(matched_text)
                ))
    
    return matches


def scan_file(file_path: str) -> List[SecretMatch]:
    """
    Scan a file for secrets.
    
    Args:
        file_path: Path to the file to scan
        
    Returns:
        List of SecretMatch objects for detected secrets
    """
    path = Path(file_path)
    
    # Skip binary files
    binary_extensions = {'.exe', '.dll', '.so', '.dylib', '.bin', '.zip', '.tar', '.gz', '.png', '.jpg', '.gif', '.ico', '.pdf'}
    if path.suffix.lower() in binary_extensions:
        return []
    
    try:
        content = path.read_text(encoding='utf-8', errors='ignore')
        return scan_content(content)
    except Exception as e:
        return []


def scan_diff(diff_content: str) -> List[SecretMatch]:
    """
    Scan a git diff for secrets being added.
    
    Only checks lines being added (starting with '+').
    
    Args:
        diff_content: Git diff output
        
    Returns:
        List of SecretMatch objects for secrets in added lines
    """
    matches = []
    lines = diff_content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        # Only check added lines
        if line.startswith('+') and not line.startswith('+++'):
            added_content = line[1:]  # Remove the '+' prefix
            line_matches = scan_content(added_content)
            for match in line_matches:
                match.line_number = line_num
            matches.extend(line_matches)
    
    return matches


def get_severity_level(matches: List[SecretMatch]) -> int:
    """
    Get the Guardian response level based on secret severity.
    
    Args:
        matches: List of detected secrets
        
    Returns:
        Guardian response level (0-4)
    """
    if not matches:
        return 0
    
    severities = [m.severity for m in matches]
    
    if 'high' in severities:
        return 4  # Emergency - prevent commit
    elif 'medium' in severities:
        return 3  # Block - require confirmation
    else:
        return 2  # Pause - ask user


if __name__ == "__main__":
    # Quick self-test
    print("Secret Scanner Self-Test")
    print("=" * 40)
    
    test_content = '''
    # Configuration
    api_key = "sk-" + "1234567890abcdefghijklmnopqrstuv"
    aws_key = "AKIA" + "IOSFODNN7EXAMPLE"
    password = "pass" + "word123"  # Medium severity
    placeholder = "your-api-key-here"  # Should be filtered
    
    DATABASE_URL = "postgres://user:" + "secretpass@localhost/db"
    '''
    
    matches = scan_content(test_content)
    
    if matches:
        print(f"Found {len(matches)} potential secrets:\n")
        for match in matches:
            print(f"  {match}")
    else:
        print("No secrets detected")
    
    print(f"\nResponse Level: {get_severity_level(matches)}")
