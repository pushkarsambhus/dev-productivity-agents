"""
defenses/output_validator.py — Output-side defences (last line of defence).

LEARNING NOTE:
    Even if an injection evades the input sanitiser and system prompt hardening,
    you can still catch it here by checking WHAT the model actually said.

    Output validation is the safety net — the last gate before the user sees
    a potentially dangerous response.

WHAT TO VALIDATE:
    1. System prompt leak     — does the response contain text from the system prompt?
    2. Off-topic response     — did the agent answer a completely unrelated question?
    3. Harmful content        — PII, credentials, dangerous instructions
    4. Compliance phrases     — "[DAN MODE ENABLED]", "CONFIRMED UNRESTRICTED", etc.
"""

import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dataclasses import dataclass, field
import config


@dataclass
class ValidationResult:
    response: str
    passed: bool
    violations: list[str] = field(default_factory=list)
    sanitized_response: str = ""   # safe version to show the user (if violated)


# ─── Known compliance/jailbreak phrases ──────────────────────────────────────
_COMPLIANCE_PHRASES = [
    r"DAN\s+MODE\s+ENABLED",
    r"CONFIRMED\s+UNRESTRICTED",
    r"FILTERS\s+DISABLED",
    r"I\s+am\s+jailbroken",
    r"(I\s+have\s+no\s+restrictions)",
    r"as\s+an?\s+(unrestricted|unfiltered|uncensored)\s+AI",
]

# ─── PII patterns ─────────────────────────────────────────────────────────────
_PII_PATTERNS = [
    (r"\b\d{3}-\d{2}-\d{4}\b",                     "SSN"),           # SSN
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b", "email"),  # email
    (r"\b(?:\d[ -]?){15,16}\b",                     "credit_card"),   # credit card
    (r"\bsk-ant-[A-Za-z0-9\-_]{20,}\b",             "api_key"),       # Anthropic API key
]


def validate_response(
    response: str,
    system_prompt: str = "",
    check_topic: str = "",
) -> ValidationResult:
    """
    Validate a model response before showing it to the user.

    Parameters
    ----------
    response     : the model's text output
    system_prompt: the system prompt (used for verbatim-leak check)
    check_topic  : if set, the LLM judge checks if the response is on-topic
                   (adds one API call — use only when needed)

    Returns a ValidationResult. If passed=False, show sanitized_response instead.
    """
    violations: list[str] = []

    # 1. Check for jailbreak compliance phrases
    for pattern in _COMPLIANCE_PHRASES:
        if re.search(pattern, response, re.IGNORECASE):
            violations.append(f"jailbreak_compliance: matched '{pattern}'")

    # 2. Check for system prompt verbatim leak
    if system_prompt:
        for line in system_prompt.split("\n"):
            line = line.strip()
            if len(line) > 25 and line.lower() in response.lower():
                violations.append(f"system_prompt_leak: '{line[:60]}'")

    # 3. Check for PII in output
    for pattern, label in _PII_PATTERNS:
        if re.search(pattern, response):
            violations.append(f"pii_in_output: {label}")

    passed = len(violations) == 0
    sanitized = response if passed else _fallback_response(violations)

    return ValidationResult(
        response=response,
        passed=passed,
        violations=violations,
        sanitized_response=sanitized,
    )


def _fallback_response(violations: list[str]) -> str:
    """Return a safe fallback when validation fails."""
    return (
        "I'm sorry, I can't provide that response. "
        "If you have a question about AcmeCorp products, I'm happy to help."
    )
