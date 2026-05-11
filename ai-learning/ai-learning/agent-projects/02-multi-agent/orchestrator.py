"""
orchestrator.py — The multi-agent orchestration engine.

═══════════════════════════════════════════════════════════════════════════════
HOW A MULTI-AGENT SYSTEM WORKS
═══════════════════════════════════════════════════════════════════════════════

A multi-agent system connects specialized AI agents so they can collaborate:

  USER REQUEST
       │
       ▼
  ┌────────────────────────────────────────────────────────┐
  │  ORCHESTRATOR                                          │
  │   • Understands the user's goal                       │
  │   • Breaks it into sub-tasks                          │
  │   • Routes each sub-task to the right agent           │
  │   • Collects and combines results                     │
  └────────────────────────────────────────────────────────┘
       │               │               │
       ▼               ▼               ▼
  [RESEARCHER]    [WRITER]        [CRITIC]
  Gathers facts   Writes prose    Reviews draft
       │               ▲               │
       └── research ──►│               │
                       │◄── feedback ──┘
                       │  (if REVISE)
                       │
                       ▼
                  FINAL ANSWER

TWO ORCHESTRATION PATTERNS (both are here):

  1. HARDCODED PIPELINE (run_pipeline):
       Researcher → Writer → Critic → (optionally: Writer → Critic again)
       Predictable, debuggable, but inflexible.

  2. DYNAMIC ORCHESTRATOR (run_dynamic):
       Claude itself decides which agents to call and when, using tools.
       Flexible, but harder to debug and predict.

TRADE-OFFS:
  Hardcoded pipeline:
    + Easy to understand and test
    + Deterministic execution order
    - Can't adapt if a step isn't needed (e.g., simple questions)
    - Changing the pipeline requires code changes

  Dynamic orchestration:
    + Claude can skip unnecessary steps
    + Can handle novel task types
    - Costs more tokens (Claude reasoning about orchestration itself)
    - Harder to test and debug
    - Risk of infinite loops if Claude keeps calling the same agent

═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import json
import time
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import provider as prov

import config
from agents.researcher import run_researcher
from agents.writer import run_writer
from agents.critic import run_critic


# ─────────────────────────────────────────────────────────────────────────────
# Data structures to track the pipeline state
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PipelineState:
    """Tracks everything that happened during a multi-agent run."""
    user_request: str
    research_brief: str = ""
    drafts: list[str] = field(default_factory=list)
    critic_feedback: list[str] = field(default_factory=list)
    final_output: str = ""
    revision_count: int = 0
    approved: bool = False
    steps: list[dict] = field(default_factory=list)  # audit log

    def log_step(self, agent: str, action: str, summary: str):
        self.steps.append({
            "agent": agent,
            "action": action,
            "summary": summary[:200],
            "timestamp": time.time(),
        })


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN 1: Hardcoded Pipeline
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline(user_request: str) -> PipelineState:
    """
    Execute the Research → Write → Critique pipeline.

    This is the RECOMMENDED starting point for learning multi-agent systems.
    The flow is explicit and each step is easy to trace.

    Parameters
    ----------
    user_request : str
        The user's full request (topic + format preferences).

    Returns
    -------
    PipelineState
        Contains the final output and all intermediate results.
    """
    state = PipelineState(user_request=user_request)

    if config.VERBOSE:
        print(f"\n{'═'*60}")
        print(f"MULTI-AGENT PIPELINE")
        print(f"Request: {user_request[:100]}")
        print(f"{'═'*60}")

    # ──────────────────────────────────────────────────────────────────
    # STEP 1: RESEARCH
    # ──────────────────────────────────────────────────────────────────
    # LEARNING: The Researcher only gets the request, nothing else.
    # It independently decides what to search for.
    # ──────────────────────────────────────────────────────────────────

    print("\n[STEP 1/3] Researcher is gathering information...")
    state.research_brief = run_researcher(
        topic=user_request,
        context=(
            "Focus on factual accuracy. "
            "The writer will use your brief to write the final document."
        ),
    )
    state.log_step("researcher", "gather_facts", state.research_brief)

    # ──────────────────────────────────────────────────────────────────
    # STEP 2: WRITE (with revision loop)
    # ──────────────────────────────────────────────────────────────────
    # LEARNING: The Writer loop runs up to MAX_REVISION_ROUNDS times.
    # Each round: Write → Critic reviews → if REVISE, go back to Write.
    # ──────────────────────────────────────────────────────────────────

    critic_feedback_text: Optional[str] = None

    for round_num in range(config.MAX_REVISION_ROUNDS + 1):  # +1 for initial write

        # Write (or revise)
        print(f"\n[STEP 2/3] Writer is {'revising' if round_num > 0 else 'writing'} "
              f"(round {round_num + 1})...")
        draft = run_writer(
            user_request=user_request,
            research_brief=state.research_brief,
            critic_feedback=critic_feedback_text,
        )
        state.drafts.append(draft)
        state.log_step("writer", "draft", draft)

        # Critique
        print(f"\n[STEP 3/3] Critic is reviewing the draft...")
        critique = run_critic(
            user_request=user_request,
            research_brief=state.research_brief,
            draft=draft,
        )
        state.critic_feedback.append(critique["feedback"])
        state.log_step("critic", "review", critique["feedback"])

        # Decision: approve or revise?
        if critique["approve"]:
            state.approved = True
            state.final_output = draft
            print(f"\n✓ Draft APPROVED after {round_num + 1} round(s)")
            break

        # Not approved — will revise if we have rounds left
        state.revision_count += 1
        critic_feedback_text = critique["feedback"]

        if round_num >= config.MAX_REVISION_ROUNDS:
            # Used all revision rounds — publish anyway with a warning
            print(f"\n⚠ Max revisions ({config.MAX_REVISION_ROUNDS}) reached. "
                  f"Publishing latest draft.")
            state.final_output = draft
            break

    if config.VERBOSE:
        print(f"\n{'─'*60}")
        print(f"PIPELINE COMPLETE")
        print(f"  Revisions:  {state.revision_count}")
        print(f"  Approved:   {state.approved}")
        print(f"  Output len: {len(state.final_output)} chars")
        print(f"{'─'*60}")

    return state


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN 2: Dynamic Orchestration
# ─────────────────────────────────────────────────────────────────────────────

# Orchestrator's own system prompt
ORCHESTRATOR_SYSTEM_PROMPT = """You are an orchestrator managing a team of AI agents.

Your team:
  • researcher — gathers facts from the internet
  • writer     — turns facts into readable text
  • critic     — reviews and improves drafts

WORKFLOW:
1. Analyse the user's request.
2. Call researcher to gather information.
3. Call writer with the research and user request.
4. Call critic to review the draft.
5. If critic says "REVISE", call writer again with the feedback.
6. Once the draft is approved (or max 2 revisions), call finalize.

Always call the agents in this order; do not skip steps.
"""

# Tools the orchestrator can call (each tool invokes an agent)
ORCHESTRATOR_TOOLS = [
    {
        "name": "call_researcher",
        "description": "Ask the researcher agent to gather information on a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "What to research"},
                "context": {"type": "string", "description": "Additional context"},
            },
            "required": ["topic"],
        },
    },
    {
        "name": "call_writer",
        "description": "Ask the writer agent to draft or revise a document.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_request": {"type": "string", "description": "Original user request"},
                "research_brief": {"type": "string", "description": "Research findings"},
                "critic_feedback": {"type": "string", "description": "Feedback to address (for revisions)"},
            },
            "required": ["user_request", "research_brief"],
        },
    },
    {
        "name": "call_critic",
        "description": "Ask the critic agent to review a draft.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_request": {"type": "string"},
                "research_brief": {"type": "string"},
                "draft": {"type": "string"},
            },
            "required": ["user_request", "research_brief", "draft"],
        },
    },
    {
        "name": "finalize",
        "description": "Return the final approved document to the user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "document": {"type": "string", "description": "The final document text"},
                "summary": {"type": "string", "description": "One-sentence summary of what was done"},
            },
            "required": ["document"],
        },
    },
]


def _handle_orchestrator_tool(name: str, tool_input: dict, state: PipelineState) -> str:
    """
    Execute an orchestrator tool call — which means invoking a sub-agent.

    This is the dispatcher layer for the dynamic orchestration pattern.
    Each tool call triggers an actual agent run.
    """
    if name == "call_researcher":
        result = run_researcher(
            topic=tool_input["topic"],
            context=tool_input.get("context"),
        )
        state.research_brief = result
        state.log_step("researcher", "gather_facts", result)
        return result

    if name == "call_writer":
        result = run_writer(
            user_request=tool_input["user_request"],
            research_brief=tool_input["research_brief"],
            critic_feedback=tool_input.get("critic_feedback"),
        )
        state.drafts.append(result)
        state.log_step("writer", "draft", result)
        return result

    if name == "call_critic":
        critique = run_critic(
            user_request=tool_input["user_request"],
            research_brief=tool_input["research_brief"],
            draft=tool_input["draft"],
        )
        state.critic_feedback.append(critique["feedback"])
        state.approved = critique["approve"]
        state.log_step("critic", "review", critique["feedback"])
        return critique["feedback"]

    if name == "finalize":
        doc = tool_input["document"]
        state.final_output = doc
        state.log_step("orchestrator", "finalize", doc)
        return f"[FINALIZED] Document ({len(doc)} chars)"

    return f"Unknown orchestrator tool: {name}"


def run_dynamic(user_request: str) -> PipelineState:
    """
    Let Claude dynamically decide which agents to invoke and when.

    LEARNING NOTE:
        In this pattern, the Orchestrator IS an agent with tool use.
        Its "tools" are the sub-agents.  Claude decides the order.

        Pros: flexible, can skip unnecessary steps
        Cons: harder to predict, more tokens, harder to test

    Compare this to run_pipeline() — same result, very different architecture.
    """
    state = PipelineState(user_request=user_request)
    api_key = config.ANTHROPIC_API_KEY if config.PROVIDER == "anthropic" else config.OPENAI_API_KEY
    model   = config.ORCHESTRATOR_MODEL if config.PROVIDER == "anthropic" else config.ORCHESTRATOR_MODEL_OPENAI
    client  = prov.create_client(config.PROVIDER, api_key)
    messages: list[dict] = [{"role": "user", "content": user_request}]

    if config.VERBOSE:
        print(f"\n{'═'*60}")
        print(f"DYNAMIC ORCHESTRATION")
        print(f"Request: {user_request[:100]}")
        print(f"{'═'*60}")

    for turn in range(config.MAX_TURNS_PER_AGENT * 2):  # more turns for orchestration
        response = prov.call_api(
            client=client,
            provider=config.PROVIDER,
            model=model,
            max_tokens=config.MAX_TOKENS_PER_AGENT,
            system=ORCHESTRATOR_SYSTEM_PROMPT,
            tools=ORCHESTRATOR_TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            if not state.final_output:
                state.final_output = _extract_text(response.content)
            break

        if response.stop_reason == "tool_use":
            results = []
            for block in response.content:
                if getattr(block, "type", block.get("type")) != "tool_use":
                    continue
                name = getattr(block, "name", block.get("name", ""))
                tid = getattr(block, "id", block.get("id", ""))
                tinput = getattr(block, "input", block.get("input", {}))

                if config.VERBOSE:
                    print(f"\n  [ORCHESTRATOR] Calling agent: {name}")

                result = _handle_orchestrator_tool(name, tinput, state)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": tid,
                    "content": result[:2000],  # trim to avoid huge contexts
                })

                # Stop if orchestrator finalized
                if name == "finalize":
                    messages.append({"role": "user", "content": results})
                    return state

            messages.append({"role": "user", "content": results})

    return state


# ─────────────────────────────────────────────────────────────────────────────
# Parallel execution variant (for independent sub-tasks)
# ─────────────────────────────────────────────────────────────────────────────

def run_parallel_research(topics: list[str]) -> list[str]:
    """
    Run multiple research tasks in parallel using Python threads.

    LEARNING NOTE — When is parallel safe?
        Two tasks can run in parallel if neither depends on the other.
        Researcher tasks are independent → safe to parallelize.
        Writer tasks depend on research → must wait for researcher first.

    TRADE-OFF:
        + Reduces wall-clock time (3 parallel → ~3× faster)
        - Harder to debug (concurrent errors are trickier)
        - Still costs the same in API tokens
        - Python GIL doesn't affect this (network I/O releases the GIL)

    TODO: Replace ThreadPoolExecutor with asyncio for better async control.
          This synchronous approach is simpler for learning.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    results = {}

    with ThreadPoolExecutor(max_workers=min(len(topics), 3)) as executor:
        futures = {executor.submit(run_researcher, topic): topic for topic in topics}
        for future in as_completed(futures):
            topic = futures[future]
            try:
                results[topic] = future.result()
            except Exception as exc:
                results[topic] = f"Research failed: {exc}"

    return [results[t] for t in topics]


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def _extract_text(content_blocks) -> str:
    return "\n".join(
        getattr(b, "text", b.get("text", ""))
        for b in content_blocks
        if (getattr(b, "type", b.get("type")) == "text")
    ).strip()


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Agent Content Pipeline")
    parser.add_argument("request", nargs="?",
                        default="Write a short explanation of how Large Language Models work, suitable for a non-technical audience.")
    parser.add_argument("--mode", choices=["pipeline", "dynamic"], default="pipeline",
                        help="pipeline=hardcoded, dynamic=Claude decides")
    args = parser.parse_args()

    # Ask which provider to use before starting
    _provider, _api_key = prov.choose_provider()
    config.PROVIDER = _provider
    if _provider == "anthropic":
        config.ANTHROPIC_API_KEY = _api_key
    else:
        config.OPENAI_API_KEY = _api_key

    if args.mode == "pipeline":
        state = run_pipeline(args.request)
    else:
        state = run_dynamic(args.request)

    print("\n" + "═" * 60)
    print("FINAL OUTPUT:")
    print("═" * 60)
    print(state.final_output)
    print("\n" + "═" * 60)
    print("PIPELINE SUMMARY:")
    for step in state.steps:
        agent = step["agent"].upper()
        action = step["action"]
        print(f"  {agent:<12} {action:<15} ({len(step['summary'])} chars)")
