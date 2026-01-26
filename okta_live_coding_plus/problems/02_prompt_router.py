"""
02_prompt_router.py
-------------------
Goal: Route prompts to different "models" based on simple business rules.

Why this matters:
- Enterprise AI platforms often "orchestrate" across providers (OpenAI, Anthropic, local).
- Basic routing + guardrails is a common live‑coding topic.

We simulate models with simple functions so there are **no external dependencies**.
"""

from typing import Dict

def route_prompt(prompt: str) -> str:
    """
    Decide which model to use based on simple keyword rules.
    Rules are **deterministic** to keep behavior predictable in a live interview.

    Example rules:
    - Finance / numbers → 'claude'
    - Security / auth / IAM → 'gpt-4'
    - Default → 'gpt-4o-mini' (a pretend cheaper model)

    Returns the **name** of the selected model.
    """
    p = prompt.lower()
    if any(k in p for k in ["revenue", "invoice", "balance sheet", "interest", "finance"]):
        return "claude"
    if any(k in p for k in ["okta", "iam", "sso", "oauth", "security", "mfa", "access"]):
        return "gpt-4"
    return "gpt-4o-mini"


def call_model(model_name: str, prompt: str) -> str:
    """
    Simulated model call — in production you would call a real API.
    We return a deterministic string for testability.
    """
    return f"[{model_name}] -> {prompt}"


def answer(prompt: str) -> str:
    """
    End‑to‑end: choose a model, then call it.
    """
    model = route_prompt(prompt)
    return call_model(model, prompt)


if __name__ == "__main__":
    examples = [
        "Summarize this Okta OAuth flow for a junior engineer.",
        "Explain the revenue recognition rules for SaaS.",
        "Write a friendly email about the team offsite.",
    ]
    for e in examples:
        print(answer(e))
