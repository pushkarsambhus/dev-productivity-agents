#!/usr/bin/env python3
"""
smolagents-research-agent — CLI tool that uses a CodeAgent with DuckDuckGoSearchTool
to answer research questions via web search and code execution.

Usage:
    python main.py "your question here"
    python main.py --model anthropic/claude-3-5-sonnet-20241022 --max-steps 15 "your question"
    python main.py --verbose "your question"
"""

import argparse
import sys
import os

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live
from rich.rule import Rule

# ---------------------------------------------------------------------------
# Initialise a single Rich console used throughout the script
# ---------------------------------------------------------------------------
console = Console()


# ---------------------------------------------------------------------------
# Helper: print banner
# ---------------------------------------------------------------------------
def print_banner() -> None:
    banner = Text("smolagents Research Agent", style="bold cyan", justify="center")
    subtitle = Text(
        "Powered by CodeAgent + DuckDuckGoSearchTool + LiteLLM/Claude",
        style="dim",
        justify="center",
    )
    console.print()
    console.print(Panel.fit(banner, subtitle=str(subtitle), border_style="cyan"))
    console.print()


# ---------------------------------------------------------------------------
# Helper: build the agent system prompt addendum
# ---------------------------------------------------------------------------
ADDITIONAL_SYSTEM_PROMPT = """
You are a research assistant. When answering a question, follow these steps:

1. SEARCH FIRST — use the DuckDuckGo search tool to gather information relevant to the question.
   Make multiple targeted searches if needed (e.g., search for different aspects separately).

2. PROCESS — if the answer requires computation, comparison, or summarisation of numbers or data,
   write concise Python code to do so. Execute it and use the result.

3. ANSWER CONCISELY — synthesise what you found and provide a clear, well-structured final answer.
   Include sources or data points where relevant. Keep the final answer readable.

Do not make up facts. If you cannot find reliable information, say so.
"""


# ---------------------------------------------------------------------------
# Core: run the agent
# ---------------------------------------------------------------------------
def run_agent(question: str, model_id: str, max_steps: int, verbose: bool) -> str:
    """
    Instantiate the smolagents CodeAgent and run it on `question`.
    Returns the final answer as a string.
    Raises specific exceptions on failure so the caller can handle them cleanly.
    """
    # Import here so import errors surface with a helpful message
    try:
        from smolagents import LiteLLMModel, CodeAgent, DuckDuckGoSearchTool
    except ImportError as exc:
        raise RuntimeError(
            "Could not import smolagents. Did you run `pip install -r requirements.txt`?"
        ) from exc

    # Build the model — ANTHROPIC_API_KEY is picked up automatically by LiteLLM
    model = LiteLLMModel(model_id=model_id)

    # Build tools list
    tools = [DuckDuckGoSearchTool()]

    # Build the agent
    # `verbosity_level` controls how much the agent prints internally:
    #   0 = silent, 1 = tool calls, 2 = full reasoning
    verbosity = 2 if verbose else 0

    agent = CodeAgent(
        tools=tools,
        model=model,
        max_steps=max_steps,
        verbosity_level=verbosity,
        additional_authorized_imports=["json", "re", "math", "statistics", "datetime"],
    )

    # Prepend extra context to the question so the agent follows our workflow
    full_prompt = f"{ADDITIONAL_SYSTEM_PROMPT.strip()}\n\nQuestion: {question}"

    result = agent.run(full_prompt)
    return str(result)


# ---------------------------------------------------------------------------
# Core: parse args
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Research agent that answers questions via web search + code execution.",
    )
    parser.add_argument(
        "question",
        nargs="?",
        default=None,
        help="The research question to answer. If omitted, you will be prompted.",
    )
    parser.add_argument(
        "--model",
        default="anthropic/claude-3-5-sonnet-20241022",
        help="LiteLLM model ID to use (default: anthropic/claude-3-5-sonnet-20241022).",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=15,
        dest="max_steps",
        help="Maximum agent reasoning steps before giving up (default: 15).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show full agent reasoning and tool-call details.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    args = parse_args()

    # Resolve the question — positional arg or interactive prompt
    question = args.question
    if not question:
        console.print("[bold yellow]No question provided.[/bold yellow]")
        question = console.input("[bold]Enter your research question:[/bold] ").strip()
        if not question:
            console.print("[red]Error:[/red] No question supplied. Exiting.")
            sys.exit(1)

    print_banner()

    # Echo the question back to the user
    console.print(
        Panel(
            Text(question, style="bold white"),
            title="[bold yellow]Research Question[/bold yellow]",
            border_style="yellow",
        )
    )
    console.print()

    # Check for API key early to give a clear error
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print(
            Panel(
                "[bold red]ANTHROPIC_API_KEY is not set.[/bold red]\n"
                "Export it before running:\n"
                "  [cyan]export ANTHROPIC_API_KEY=sk-ant-...[/cyan]",
                title="[red]Missing API Key[/red]",
                border_style="red",
            )
        )
        sys.exit(1)

    console.print(f"[dim]Model:[/dim] [cyan]{args.model}[/cyan]   "
                  f"[dim]Max steps:[/dim] [cyan]{args.max_steps}[/cyan]")
    console.print()

    # Run the agent — show a spinner while waiting (unless verbose, which prints its own output)
    answer: str | None = None
    error_msg: str | None = None

    if not args.verbose:
        # Spinner mode: suppress agent's own output
        with Live(
            Spinner("dots", text="[bold cyan]Agent is thinking...[/bold cyan]"),
            console=console,
            refresh_per_second=10,
        ):
            try:
                answer = run_agent(question, args.model, args.max_steps, verbose=False)
            except Exception as exc:
                error_msg = _format_error(exc)
    else:
        # Verbose mode: let the agent print its own reasoning, no spinner
        console.print(Rule("[dim]Agent Trace[/dim]"))
        try:
            answer = run_agent(question, args.model, args.max_steps, verbose=True)
        except Exception as exc:
            error_msg = _format_error(exc)
        console.print(Rule())
        console.print()

    # Display result or error
    if answer is not None:
        console.print(
            Panel(
                Text(answer, style="white"),
                title="[bold green]Final Answer[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )
    else:
        console.print(
            Panel(
                error_msg or "An unknown error occurred.",
                title="[bold red]Error[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
        )
        sys.exit(1)

    console.print()


# ---------------------------------------------------------------------------
# Error formatter — translates exception types into friendly messages
# ---------------------------------------------------------------------------
def _format_error(exc: Exception) -> str:
    """
    Map known exception types to friendly messages.
    Falls back to a generic message for unexpected errors.
    """
    exc_type = type(exc).__name__
    exc_module = type(exc).__module__ or ""

    # smolagents: agent exceeded max steps
    if "AgentMaxStepsError" in exc_type or (
        "max" in str(exc).lower() and "step" in str(exc).lower()
    ):
        return (
            "[bold yellow]The agent hit its maximum step limit and could not complete "
            "the answer.[/bold yellow]\n\n"
            f"Partial output (if any):\n{exc}\n\n"
            "Try increasing [cyan]--max-steps[/cyan] or rephrasing the question."
        )

    # smolagents: tool call error
    if "AgentToolCallError" in exc_type or (
        "tool" in str(exc).lower() and "error" in str(exc).lower()
    ):
        return (
            f"[bold red]A tool call failed:[/bold red] {exc}\n\n"
            "This may be a transient DuckDuckGo search error. Try again in a moment."
        )

    # anthropic: network / connectivity
    if "APIConnectionError" in exc_type:
        return (
            "[bold red]Could not connect to the Anthropic API.[/bold red]\n"
            "Check your internet connection and try again.\n\n"
            f"Details: {exc}"
        )

    # anthropic: rate limit
    if "RateLimitError" in exc_type:
        return (
            "[bold red]Anthropic API rate limit exceeded.[/bold red]\n"
            "Wait a moment and retry, or switch to a different model with [cyan]--model[/cyan].\n\n"
            f"Details: {exc}"
        )

    # Import / setup error (our own RuntimeError wrapper)
    if isinstance(exc, RuntimeError):
        return f"[bold red]Setup error:[/bold red] {exc}"

    # Generic fallback
    return (
        f"[bold red]Unexpected error ({exc_type}):[/bold red] {exc}\n\n"
        "If this persists, check your ANTHROPIC_API_KEY and dependencies."
    )


if __name__ == "__main__":
    main()
