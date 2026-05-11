"""
agent.py — The core agent loop.

═══════════════════════════════════════════════════════════════════════════════
HOW AN LLM AGENT WORKS  (read this first)
═══════════════════════════════════════════════════════════════════════════════

A "tool-use agent" is just a while-loop around the Claude API:

  ┌─────────────────────────────────────────────────────────────┐
  │  1. Send conversation history + tool schemas to Claude      │
  │  2. Claude responds with text AND/OR tool_use blocks        │
  │  3. If stop_reason == "end_turn"  → we're done, show answer │
  │  4. If stop_reason == "tool_use"  → execute each tool,      │
  │     append results to history, go to step 1                 │
  └─────────────────────────────────────────────────────────────┘

The KEY insight: Claude doesn't execute tools — YOU do.
Claude just says "please call web_search with these args".
Your code calls the function and tells Claude what it returned.

TRADE-OFFS:
  • Simple loop vs. complex orchestration:
      This file uses the simplest possible loop.  Real agents add
      memory, context window management, retry logic, and observability.
  • Stateless vs. stateful:
      We keep messages[] in memory. After the process exits the conversation
      is lost.  To persist it: serialize messages[] to a database.
  • Cost:
      Every turn sends the FULL history to the API.  Long conversations
      cost more. Mitigation: summarize old turns (compaction) or use
      prompt caching (see config.py for cache_control ideas).

═══════════════════════════════════════════════════════════════════════════════
"""

import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import provider as prov

import config
from tools import TOOL_SCHEMAS, dispatch_tool


# ─────────────────────────────────────────────────────────────────────────────
# Helper: validate setup
# ─────────────────────────────────────────────────────────────────────────────

def _check_setup() -> None:
    """Fail fast with a clear message if provider or API key is missing."""
    if not config.PROVIDER:
        print("ERROR: No provider selected. Call provider.choose_provider() first.")
        sys.exit(1)
    if config.PROVIDER == "anthropic" and not config.ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY is not set.")
        print("  Option 1: export ANTHROPIC_API_KEY='sk-ant-...'")
        print("  Option 2: edit config.py and set ANTHROPIC_API_KEY directly.")
        sys.exit(1)
    if config.PROVIDER == "openai" and not config.OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is not set.")
        print("  Option 1: export OPENAI_API_KEY='sk-...'")
        print("  Option 2: edit config.py and set OPENAI_API_KEY directly.")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Core agent function
# ─────────────────────────────────────────────────────────────────────────────

def run_agent(user_message: str) -> str:
    """
    Run a single agent conversation and return the final text response.

    Parameters
    ----------
    user_message : str
        The question or task from the user.

    Returns
    -------
    str
        The final natural-language answer from Claude.

    FLOW:
        1. Build initial messages list with the user's input.
        2. Enter the tool-use loop.
        3. On each iteration, call the Claude API.
        4. If Claude wants tools → execute them, append results, loop again.
        5. If Claude is done → extract and return the text.
    """
    _check_setup()

    # Initialise the provider client.
    # TRADE-OFF: creating the client once and reusing it is more efficient
    # than creating it on every call, but for simplicity we create it here.
    api_key = config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic" else config.OPENAI_API_KEY
    model   = config.MODEL if config.PROVIDER == "anthropic" else config.MODEL_OPENAI
    client  = prov.create_client(config.PROVIDER, api_key)

    # ── Conversation history ──────────────────────────────────────────────────
    # The Claude API is STATELESS — every call sends the full conversation.
    # We maintain history locally as a list of message dicts.
    #
    # Message format:
    #   {"role": "user",      "content": "...string or content blocks..."}
    #   {"role": "assistant", "content": [...content blocks...]}
    #
    # Tool results are sent as a "user" message with type "tool_result".
    messages: list[dict] = [
        {"role": "user", "content": user_message}
    ]

    if config.VERBOSE:
        print(f"\n{'═'*60}")
        print(f"USER: {user_message}")
        print(f"{'═'*60}")

    # ── Agentic loop ─────────────────────────────────────────────────────────
    # We limit iterations to MAX_TURNS to prevent runaway loops.
    for turn in range(config.MAX_TURNS):

        if config.VERBOSE:
            print(f"\n[TURN {turn + 1}/{config.MAX_TURNS}] Calling Claude...")

        # ── Step 1: Call Claude API ───────────────────────────────────────────
        #
        # IMPORTANT PARAMETERS:
        #   model       – which Claude model to use
        #   max_tokens  – upper bound on output length (prevent runaway)
        #   system      – Claude's "personality"/instructions (stays constant)
        #   tools       – list of tool schemas (what Claude CAN call)
        #   messages    – full conversation history so far
        #
        # TRADE-OFF on max_tokens:
        #   Too low → Claude truncates mid-sentence.
        #   Too high → expensive if you're paying per token.
        response = prov.call_api(
            client=client,
            provider=config.PROVIDER,
            model=model,
            max_tokens=config.MAX_TOKENS,
            system=config.SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        if config.VERBOSE:
            print(f"  stop_reason: {response.stop_reason}")
            print(f"  content blocks: {[b.type for b in response.content]}")

        # ── Step 2: Append Claude's response to history ───────────────────────
        # We must preserve the FULL content (including tool_use blocks) so that
        # the next API call can reference the tool_use IDs when we send results.
        # COMMON MISTAKE: only appending the text part breaks tool result pairing.
        messages.append({
            "role": "assistant",
            "content": response.content,   # list of ContentBlock objects
        })

        # ── Step 3: Check stop reason ─────────────────────────────────────────
        if response.stop_reason == "end_turn":
            # Claude finished — extract the final text
            final_text = _extract_text(response.content)
            if config.VERBOSE:
                print(f"\n{'─'*60}")
                print(f"FINAL ANSWER:\n{final_text}")
                print(f"{'─'*60}")
                print(f"Tokens used — input: {response.usage.input_tokens}, "
                      f"output: {response.usage.output_tokens}")
                print(f"Provider: {config.PROVIDER} | Model: {model}")
            return final_text

        # ── Step 4: Handle tool_use ───────────────────────────────────────────
        if response.stop_reason == "tool_use":
            tool_results = _execute_tools(response.content)

            # Tool results go back as a USER message with type "tool_result".
            # IMPORTANT: each result must include the tool_use_id that matches
            # the tool_use block in the previous assistant message.
            messages.append({
                "role": "user",
                "content": tool_results,
            })
            continue   # ← loop back and call Claude again with the results

        # ── Step 5: Handle unexpected stop reasons ────────────────────────────
        # pause_turn → server-side tool hit its iteration limit; resend to continue
        if response.stop_reason == "pause_turn":
            if config.VERBOSE:
                print("  [INFO] pause_turn received — continuing...")
            continue

        # Any other stop reason (max_tokens, stop_sequence, refusal, …)
        if config.VERBOSE:
            print(f"  [WARN] Unexpected stop_reason: {response.stop_reason}")
        return _extract_text(response.content) or f"[Stopped: {response.stop_reason}]"

    # Reached MAX_TURNS without a final answer
    return "[Agent stopped: maximum turns reached without a final answer]"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers used inside the loop
# ─────────────────────────────────────────────────────────────────────────────

def _extract_text(content_blocks) -> str:
    """
    Pull the text out of a list of content blocks.

    Content blocks are a discriminated union — each block has a .type field.
    We only want the text blocks; tool_use blocks contain the call details.
    """
    parts = []
    for block in content_blocks:
        if hasattr(block, "type") and block.type == "text":
            parts.append(block.text)
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(parts).strip()


def _execute_tools(content_blocks) -> list[dict]:
    """
    Find all tool_use blocks in the response and execute each one.

    Returns a list of tool_result dicts ready to send back to Claude.

    LEARNING NOTE — Multiple tools in one turn:
        Claude can request several tools in a single response (parallel tool use).
        We must return ALL results before the next API call.
        Missing a result causes an API error ("missing tool_result for tool_use_id").
    """
    tool_results = []

    for block in content_blocks:
        # Detect tool_use blocks (handle both object and dict forms)
        block_type = getattr(block, "type", block.get("type") if isinstance(block, dict) else None)
        if block_type != "tool_use":
            continue

        # Extract the tool name, id, and input arguments
        tool_name  = getattr(block, "name",  block.get("name",  ""))
        tool_id    = getattr(block, "id",    block.get("id",    ""))
        tool_input = getattr(block, "input", block.get("input", {}))

        if config.VERBOSE:
            print(f"\n  ▶ Executing tool: {tool_name}")

        # Call the actual tool function (defined in tools.py)
        result_text = dispatch_tool(tool_name, tool_input)

        # Package the result in the format Claude expects
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": tool_id,       # ← must match the tool_use block's id
            "content": result_text,        # ← plain string or list of content blocks
        })

    return tool_results


# ─────────────────────────────────────────────────────────────────────────────
# Streaming variant (optional, for real-time UIs)
# ─────────────────────────────────────────────────────────────────────────────

def run_agent_streaming(user_message: str) -> str:
    """
    Same as run_agent() but streams text tokens to stdout in real time.

    TRADE-OFF:
        Streaming improves perceived responsiveness (user sees output immediately)
        but adds complexity: you must collect the full response before executing
        tools, and you need to handle stream events rather than a single response.

    WHEN TO USE:
        • Chat UIs where the user waits for a response
        • Long text generation tasks

    WHEN NOT TO USE:
        • Batch processing / programmatic usage
        • When you just need the final answer string
    """
    _check_setup()
    if config.PROVIDER != "anthropic":
        # Streaming is Anthropic-specific — fall back to non-streaming for OpenAI
        print("[INFO] Streaming is only supported with Anthropic. Using non-streaming mode.")
        return run_agent(user_message)

    import anthropic as _anthropic
    api_key = config.ANTHROPIC_API_KEY
    model   = config.MODEL
    client  = _anthropic.Anthropic(api_key=api_key)
    messages: list[dict] = [{"role": "user", "content": user_message}]

    for turn in range(config.MAX_TURNS):
        # Use the streaming context manager
        with client.messages.stream(
            model=model,
            max_tokens=config.MAX_TOKENS,
            system=config.SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        ) as stream:
            # Print text tokens as they arrive
            for text_chunk in stream.text_stream:
                print(text_chunk, end="", flush=True)

            # Once streaming is done, get the complete response object
            # .get_final_message() blocks until all tokens are received
            response = stream.get_final_message()

        print()  # newline after streaming

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return _extract_text(response.content)

        if response.stop_reason == "tool_use":
            tool_results = _execute_tools(response.content)
            messages.append({"role": "user", "content": tool_results})
            continue

    return "[Agent stopped: maximum turns reached]"


# ─────────────────────────────────────────────────────────────────────────────
# Multi-turn conversation helper
# ─────────────────────────────────────────────────────────────────────────────

class AgentSession:
    """
    Maintain a multi-turn conversation across multiple user inputs.

    LEARNING NOTE:
        The Claude API is stateless — every call must include full history.
        This class wraps the loop so you can have a back-and-forth chat
        without re-sending the same message to start.

    TRADE-OFF:
        Keeping all history in memory is simple but will eventually hit
        the context window limit (200K tokens for Claude Opus 4.6).
        For long sessions: summarize old turns or use context compaction.
    """

    def __init__(self):
        _check_setup()
        api_key = config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic" else config.OPENAI_API_KEY
        self._model  = config.MODEL if config.PROVIDER == "anthropic" else config.MODEL_OPENAI
        self.client  = prov.create_client(config.PROVIDER, api_key)
        self.messages: list[dict] = []
        self.turn_count: int = 0

    def chat(self, user_message: str) -> str:
        """Send a message and get a reply, preserving conversation history."""
        self.messages.append({"role": "user", "content": user_message})

        for _ in range(config.MAX_TURNS):
            response = prov.call_api(
                client=self.client,
                provider=config.PROVIDER,
                model=self._model,
                max_tokens=config.MAX_TOKENS,
                system=config.SYSTEM_PROMPT,
                tools=TOOL_SCHEMAS,
                messages=self.messages,
            )
            self.messages.append({"role": "assistant", "content": response.content})
            self.turn_count += 1

            if response.stop_reason == "end_turn":
                return _extract_text(response.content)

            if response.stop_reason == "tool_use":
                results = _execute_tools(response.content)
                self.messages.append({"role": "user", "content": results})

        return "[Max turns reached]"

    def reset(self):
        """Clear history to start a new conversation."""
        self.messages = []
        self.turn_count = 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Single Agent Demo")

    # Ask which provider to use before starting
    _provider, _api_key = prov.choose_provider()
    config.PROVIDER = _provider
    if _provider == "anthropic":
        config.ANTHROPIC_API_KEY = _api_key
    else:
        config.OPENAI_API_KEY = _api_key

    print("Type 'quit' to exit, 'reset' to start a new conversation.\n")

    session = AgentSession()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "reset":
            session.reset()
            print("[Conversation reset]\n")
            continue

        answer = session.chat(user_input)
        print(f"\nAgent: {answer}\n")
