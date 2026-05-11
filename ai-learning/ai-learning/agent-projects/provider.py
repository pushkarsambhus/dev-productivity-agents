"""
provider.py — Unified provider abstraction for Anthropic and OpenAI APIs.

LEARNING NOTE:
    Both providers offer similar capabilities (chat, tool use, streaming) but
    with different SDKs and message formats. This module translates between them
    so the rest of the code stays provider-agnostic.

TRADE-OFFS:
    - Abstraction adds a layer of indirection and reduces visibility into each
      provider's unique features (e.g., Anthropic prompt caching, OpenAI assistants).
    - Keeping the canonical format as Anthropic-style dicts means OpenAI users
      see a slight translation overhead; the reverse would be equally valid.
    - For production: use a framework like LiteLLM instead of rolling your own.
"""

import json
import os
import sys
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Optional


# ─────────────────────────────────────────────────────────────────────────────
# Normalized response — same shape regardless of which provider replied
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class NormalizedResponse:
    """
    Provider-agnostic response from a chat/completions call.

    stop_reason : "end_turn"  → model finished naturally
                  "tool_use"  → model wants to call a tool
                  "other"     → anything else (max_tokens, stop_sequence, …)
    content     : list of dicts in Anthropic-style format:
                    {"type": "text",     "text": "…"}
                    {"type": "tool_use", "id": "…", "name": "…", "input": {…}}
    usage       : SimpleNamespace(input_tokens=N, output_tokens=N)
    """
    stop_reason: str
    content: list
    usage: Any


# ─────────────────────────────────────────────────────────────────────────────
# Client creation
# ─────────────────────────────────────────────────────────────────────────────

def create_client(provider: str, api_key: str):
    """Create and return the provider's SDK client."""
    if provider == "anthropic":
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    elif provider == "openai":
        import openai
        return openai.OpenAI(api_key=api_key)
    else:
        raise ValueError(f"Unknown provider: {provider!r}. Choose 'anthropic' or 'openai'.")


# ─────────────────────────────────────────────────────────────────────────────
# Tool schema conversion  (Anthropic format → provider format)
# ─────────────────────────────────────────────────────────────────────────────

def convert_tools(tools: list, provider: str) -> list:
    """
    Convert Anthropic-format tool schemas to the target provider's format.

    Anthropic:
        {"name": str, "description": str, "input_schema": {json_schema}}

    OpenAI:
        {"type": "function", "function": {"name": str, "description": str,
                                          "parameters": {json_schema}}}
    """
    if not tools:
        return tools
    if provider == "anthropic":
        return tools  # already in Anthropic format
    # OpenAI
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t.get("input_schema", {"type": "object", "properties": {}}),
            },
        }
        for t in tools
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Message format conversion  (Anthropic messages → OpenAI messages)
# ─────────────────────────────────────────────────────────────────────────────

def _to_openai_messages(system: str, messages: list) -> list:
    """
    Convert Anthropic-style messages (+ separate system prompt) to OpenAI
    chat format (system as first message, tool results as role=tool messages).

    LEARNING NOTE on format differences:
        Anthropic: tool results are { role: "user", content: [{ type: "tool_result", … }] }
        OpenAI:    tool results are { role: "tool", tool_call_id: "…", content: "…" }

        Anthropic: assistant message has content = list of blocks
        OpenAI:    assistant message has content = string (or None) + tool_calls list
    """
    result = [{"role": "system", "content": system}]

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        # ── Plain string message ─────────────────────────────────────────────
        if isinstance(content, str):
            result.append({"role": role, "content": content})
            continue

        # ── User message ─────────────────────────────────────────────────────
        if role == "user":
            if (
                isinstance(content, list)
                and content
                and (
                    content[0].get("type") == "tool_result"
                    if isinstance(content[0], dict)
                    else getattr(content[0], "type", None) == "tool_result"
                )
            ):
                # Tool-result messages → individual role=tool messages in OpenAI
                for block in content:
                    b = block if isinstance(block, dict) else {
                        "type": getattr(block, "type", ""),
                        "tool_use_id": getattr(block, "tool_use_id", ""),
                        "content": getattr(block, "content", ""),
                    }
                    result.append({
                        "role": "tool",
                        "tool_call_id": b.get("tool_use_id", ""),
                        "content": b.get("content", ""),
                    })
            else:
                # Normal user text (may be a list with a single text block)
                if isinstance(content, list):
                    text_parts = [
                        b.get("text", "") if isinstance(b, dict) else getattr(b, "text", "")
                        for b in content
                        if (b.get("type") if isinstance(b, dict) else getattr(b, "type", "")) == "text"
                    ]
                    result.append({"role": "user", "content": "\n".join(text_parts) or ""})
                else:
                    result.append({"role": "user", "content": str(content)})
            continue

        # ── Assistant message ─────────────────────────────────────────────────
        if role == "assistant":
            text_parts = []
            tool_calls = []
            for b in content:
                btype = b.get("type") if isinstance(b, dict) else getattr(b, "type", "")
                if btype == "text":
                    text_parts.append(
                        b.get("text", "") if isinstance(b, dict) else getattr(b, "text", "")
                    )
                elif btype == "tool_use":
                    bid   = b.get("id",    "") if isinstance(b, dict) else getattr(b, "id",    "")
                    bname = b.get("name",  "") if isinstance(b, dict) else getattr(b, "name",  "")
                    binput= b.get("input", {}) if isinstance(b, dict) else getattr(b, "input", {})
                    tool_calls.append({
                        "id": bid,
                        "type": "function",
                        "function": {"name": bname, "arguments": json.dumps(binput)},
                    })

            oai_msg: dict = {"role": "assistant"}
            oai_msg["content"] = "\n".join(text_parts) if text_parts else None
            if tool_calls:
                oai_msg["tool_calls"] = tool_calls
            result.append(oai_msg)

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Content normalization helpers
# ─────────────────────────────────────────────────────────────────────────────

def _normalize_anthropic_content(content) -> list:
    """Convert Anthropic ContentBlock SDK objects → plain dicts."""
    result = []
    for block in content:
        if isinstance(block, dict):
            result.append(block)
        else:
            t = getattr(block, "type", "")
            if t == "text":
                result.append({"type": "text", "text": getattr(block, "text", "")})
            elif t == "tool_use":
                result.append({
                    "type": "tool_use",
                    "id":    getattr(block, "id",    ""),
                    "name":  getattr(block, "name",  ""),
                    "input": getattr(block, "input", {}),
                })
            else:
                result.append({"type": t})
    return result


def _normalize_openai_response(response) -> NormalizedResponse:
    """Convert an OpenAI ChatCompletion → NormalizedResponse."""
    choice = response.choices[0]
    message = choice.message
    finish_reason = choice.finish_reason

    content = []
    if message.content:
        content.append({"type": "text", "text": message.content})
    if message.tool_calls:
        for tc in message.tool_calls:
            try:
                parsed_input = json.loads(tc.function.arguments)
            except (json.JSONDecodeError, TypeError):
                parsed_input = {}
            content.append({
                "type":  "tool_use",
                "id":    tc.id,
                "name":  tc.function.name,
                "input": parsed_input,
            })

    # Map OpenAI finish_reason → Anthropic-style stop_reason
    if finish_reason == "stop":
        stop_reason = "end_turn"
    elif finish_reason == "tool_calls":
        stop_reason = "tool_use"
    else:
        stop_reason = finish_reason or "other"

    usage = SimpleNamespace(
        input_tokens=response.usage.prompt_tokens     if response.usage else 0,
        output_tokens=response.usage.completion_tokens if response.usage else 0,
    )
    return NormalizedResponse(stop_reason=stop_reason, content=content, usage=usage)


# ─────────────────────────────────────────────────────────────────────────────
# Unified API call
# ─────────────────────────────────────────────────────────────────────────────

def call_api(
    client,
    provider: str,
    model: str,
    system: str,
    messages: list,
    tools: Optional[list],
    max_tokens: int,
) -> NormalizedResponse:
    """
    Make a chat/completions call to the chosen provider.

    Parameters
    ----------
    client      : SDK client created by create_client()
    provider    : "anthropic" or "openai"
    model       : model name (provider-specific)
    system      : system prompt string
    messages    : conversation history in Anthropic-style format
    tools       : Anthropic-style tool schemas (or None / empty list)
    max_tokens  : max output tokens

    Returns
    -------
    NormalizedResponse with .stop_reason, .content (list of dicts), .usage
    """
    if provider == "anthropic":
        kwargs: dict = dict(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        if tools:
            kwargs["tools"] = tools
        response = client.messages.create(**kwargs)
        content = _normalize_anthropic_content(response.content)
        usage = SimpleNamespace(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )
        return NormalizedResponse(
            stop_reason=response.stop_reason,
            content=content,
            usage=usage,
        )

    elif provider == "openai":
        oai_messages = _to_openai_messages(system, messages)
        kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            messages=oai_messages,
        )
        if tools:
            kwargs["tools"] = convert_tools(tools, "openai")
        response = client.chat.completions.create(**kwargs)
        return _normalize_openai_response(response)

    else:
        raise ValueError(f"Unknown provider: {provider!r}")


# ─────────────────────────────────────────────────────────────────────────────
# Interactive provider selection — called at app startup
# ─────────────────────────────────────────────────────────────────────────────

def choose_provider() -> tuple[str, str]:
    """
    Ask the user which API provider to use, then return (provider, api_key).

    The caller should store these in config.PROVIDER and the appropriate key field:

        provider, api_key = provider.choose_provider()
        config.PROVIDER = provider
        if provider == "anthropic":
            config.ANTHROPIC_API_KEY = api_key
        else:
            config.OPENAI_API_KEY = api_key
    """
    print("\n" + "─" * 50)
    print("Which API provider would you like to use?")
    print("  1. Anthropic  (Claude models — claude-opus-4-6, claude-sonnet-4-6, …)")
    print("  2. OpenAI     (GPT models   — gpt-4o, gpt-4o-mini, …)")
    print("─" * 50)

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice in ("1", "anthropic", "Anthropic"):
            provider = "anthropic"
            break
        elif choice in ("2", "openai", "OpenAI"):
            provider = "openai"
            break
        else:
            print("  Please enter 1 (Anthropic) or 2 (OpenAI).")

    env_var = "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY"
    api_key = os.environ.get(env_var, "")

    if api_key:
        print(f"  Using {env_var} from environment.\n")
    else:
        key_hint = "sk-ant-..." if provider == "anthropic" else "sk-..."
        print(f"\n  {env_var} not found in environment.")
        api_key = input(f"  Enter your {provider.capitalize()} API key ({key_hint}): ").strip()

    if not api_key:
        print("ERROR: No API key provided. Set the environment variable or enter it above.")
        sys.exit(1)

    return provider, api_key
