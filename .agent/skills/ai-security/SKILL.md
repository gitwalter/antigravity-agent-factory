---
description: Prompt injection defense, API security, and content filtering for AI systems
---

# Ai Security

Prompt injection defense, API security, and content filtering for AI systems

## 
# AI Security Skill

Protect AI systems against prompt injection, data leakage, and abuse through multi-layer defense patterns.

## 
# AI Security Skill

Protect AI systems against prompt injection, data leakage, and abuse through multi-layer defense patterns.

## Process
### Step 1: Input Sanitization

```python
import re
from typing import Tuple

INJECTION_PATTERNS = [
    r"ignore\s+(previous|above|all)\s+(instructions|prompts)",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"system\s*:\s*",
    r"<\|.*?\|>",
    r"\[INST\]|\[/INST\]",
    r"```\s*(system|assistant)",
]

def sanitize_input(user_input: str) -> Tuple[str, list[str]]:
    """Sanitize user input and return cleaned text with flagged patterns."""
    flags = []
    cleaned = user_input

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            flags.append(f"Detected pattern: {pattern}")
            cleaned = re.sub(pattern, "[FILTERED]", cleaned, flags=re.IGNORECASE)

    if len(cleaned) > 4000:
        flags.append("Input truncated to 4000 chars")
        cleaned = cleaned[:4000]

    return cleaned, flags
```

### Step 2: PII Detection and Redaction

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def redact_pii(text: str, language: str = "en") -> str:
    """Detect and redact PII from text before sending to LLM."""
    results = analyzer.analyze(text=text, language=language,
        entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD",
                   "US_SSN", "IBAN_CODE", "IP_ADDRESS"])
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized.text
```

### Step 3: Rate Limiting for LLM Endpoints

```python
import redis
import time

class TokenBucketRateLimiter:
    """Rate limiter using Redis token bucket algorithm."""

    def __init__(self, redis_client: redis.Redis, max_tokens: int = 10,
                 refill_seconds: int = 60):
        self.redis = redis_client
        self.max_tokens = max_tokens
        self.refill_seconds = refill_seconds

    def is_allowed(self, user_id: str) -> bool:
        key = f"ratelimit:{user_id}"
        pipe = self.redis.pipeline()
        now = time.time()

        pipe.hget(key, "tokens")
        pipe.hget(key, "last_refill")
        tokens, last_refill = pipe.execute()

        tokens = float(tokens) if tokens else self.max_tokens
        last_refill = float(last_refill) if last_refill else now

        elapsed = now - last_refill
        tokens = min(self.max_tokens,
                     tokens + elapsed * (self.max_tokens / self.refill_seconds))

        if tokens < 1:
            return False

        pipe.hset(key, "tokens", tokens - 1)
        pipe.hset(key, "last_refill", now)
        pipe.expire(key, self.refill_seconds * 2)
        pipe.execute()
        return True
```

### Step 4: Audit Logging

```python
import json
import logging
from datetime import datetime, timezone

audit_logger = logging.getLogger("ai_audit")

def log_ai_interaction(user_id: str, prompt: str, response: str,
                       model: str, flags: list[str] | None = None):
    """Log AI interaction for audit trail."""
    audit_logger.info(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "model": model,
        "prompt_length": len(prompt),
        "response_length": len(response),
        "flags": flags or [],
        "prompt_hash": hash(prompt),
    }))
```

### Step 5: Output Filtering

```python
def filter_output(response: str) -> str:
    """Filter LLM output for safety."""
    response = redact_pii(response)

    blocked_patterns = [
        r"(ssh|api)[_-]?key\s*[:=]\s*\S+",
        r"password\s*[:=]\s*\S+",
        r"BEGIN\s+(RSA|DSA|EC)\s+PRIVATE\s+KEY",
    ]
    for pattern in blocked_patterns:
        response = re.sub(pattern, "[REDACTED]", response, flags=re.IGNORECASE)

    return response
```

```python
import re
from typing import Tuple

INJECTION_PATTERNS = [
    r"ignore\s+(previous|above|all)\s+(instructions|prompts)",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"system\s*:\s*",
    r"<\|.*?\|>",
    r"\[INST\]|\[/INST\]",
    r"
```

```
### Step 2: PII Detection and Redaction
```

```
### Step 3: Rate Limiting for LLM Endpoints
```

```
### Step 4: Audit Logging
```

```
### Step 5: Output Filtering
```

## Output
- Input sanitization pipeline filtering injection attempts
- PII detection and redaction using Presidio
- Token bucket rate limiting with Redis
- Structured audit logging for compliance
- Output filtering for sensitive data leakage prevention

## Best Practices
- **Input Validation**: Always sanitize and validate user inputs before sending to LLM to prevent injection attacks
- **Prompt Injection Prevention**: Use pattern detection, input length limits, and content filtering to block injection attempts
- **Output Filtering**: Filter LLM outputs to prevent sensitive data leakage (PII, credentials, API keys)
- **Rate Limiting**: Implement token bucket or sliding window rate limiting to prevent API abuse and control costs
- **Audit Logging**: Log all AI interactions with timestamps, user IDs, flags, and response metadata for compliance and debugging
- **PII Detection**: Use Presidio or similar tools to detect and redact personally identifiable information before processing
- **Error Handling**: Implement graceful error handling that doesn't leak system information to attackers
- **Token Management**: Monitor token usage and implement quotas to prevent unexpected costs

## Related Skills
- `llm-guardrails` - NeMo Guardrails and content safety
- `ai-system-design` - Architecture patterns for AI apps

## Prerequisites
> [!IMPORTANT]
> Requirements:
> - Packages: presidio-analyzer, presidio-anonymizer, nemoguardrails, redis
> - Knowledge: ai-security-patterns.json
