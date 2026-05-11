"""
PHASE 4 | LLM / AI PATTERNS | 03 AGENTS & TOOLS
=================================================
Topic: Build a minimal ReAct-style agent loop from scratch.
ReAct = Reason + Act. The agent loop you built with smolagents follows this pattern.

Pattern:
  while not done:
      thought = llm.think(history)
      action  = parse_action(thought)
      result  = execute_tool(action)
      history.append(thought + result)

No LLM API needed here — we simulate the LLM with scripted responses
so you can focus on the agent loop architecture.
"""
from dataclasses import dataclass, field
from typing import Callable


# ── Tool definition ────────────────────────────────────────────────────────────
@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[[str], str]   # takes a string input, returns a string result

    def __call__(self, input_str: str) -> str:
        return self.fn(input_str)


# ── Agent Message types ────────────────────────────────────────────────────────
@dataclass
class Message:
    role: str    # "user", "assistant", "tool"
    content: str


# ── Step 1: Tool Registry ──────────────────────────────────────────────────────
class ToolRegistry:
    """Manages available tools and dispatches calls by name."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        # TODO: store tool by name
        pass

    def call(self, tool_name: str, input_str: str) -> str:
        """Call a tool by name. Return error string if tool not found."""
        # TODO: look up tool, call it, return result
        # If tool_name not found: return f"Error: unknown tool '{tool_name}'"
        pass

    def describe_all(self) -> str:
        """Return a formatted string describing all available tools."""
        # TODO: return each tool's name + description, one per line
        pass


# ── Step 2: Action Parser ──────────────────────────────────────────────────────
def parse_action(llm_response: str) -> tuple[str, str] | None:
    """
    Parse a tool call from LLM output.
    Expected format: ACTION: tool_name(input)
    Returns: (tool_name, input) or None if no action found.

    Examples:
      "I need to search. ACTION: web_search(Python decorators)"
        → ("web_search", "Python decorators")
      "The answer is 42."
        → None
    """
    # TODO: find "ACTION:" in the string, extract tool_name and input
    # Hint: str.find(), string slicing, strip()
    pass


# ── Step 3: Agent Loop ─────────────────────────────────────────────────────────
class ReActAgent:
    """
    Minimal ReAct agent: think → act → observe → repeat.
    """

    def __init__(self, tools: list[Tool], max_steps: int = 5):
        self.registry = ToolRegistry()
        for tool in tools:
            self.registry.register(tool)
        self.max_steps = max_steps
        self.history: list[Message] = []

    def _build_prompt(self, user_query: str) -> str:
        """Build the full prompt from history + available tools."""
        tool_desc = self.registry.describe_all()
        history_str = "\n".join(f"{m.role}: {m.content}" for m in self.history)
        return (
            f"Available tools:\n{tool_desc}\n\n"
            f"To use a tool, write: ACTION: tool_name(input)\n"
            f"When done, write: FINAL: your answer\n\n"
            f"History:\n{history_str}\n\nuser: {user_query}"
        )

    def run(self, user_query: str, llm_fn: Callable[[str], str]) -> str:
        """
        Run the agent loop.

        Args:
            user_query: the user's question
            llm_fn: function that takes a prompt string, returns LLM response string

        TODO:
        1. Add user query to history
        2. Loop up to max_steps:
           a. Build prompt from history
           b. Call llm_fn(prompt)
           c. Add assistant response to history
           d. If response contains "FINAL:": extract and return the answer
           e. If response contains "ACTION:": parse it, call the tool,
              add tool result to history as a "tool" message
           f. If neither: break (LLM confused)
        3. If max_steps reached without FINAL: return "Agent could not complete task"
        """
        pass


# ── Self-check ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Define some tools
    tools = [
        Tool("calculator", "Evaluates a math expression. Input: a math string like '2+2'",
             lambda expr: str(eval(expr))),  # noqa: S307 (safe in this demo)
        Tool("upper", "Converts text to uppercase. Input: any string",
             lambda text: text.upper()),
        Tool("word_count", "Counts words in text. Input: any string",
             lambda text: str(len(text.split()))),
    ]

    # Simulate LLM responses for a scripted demo
    responses = iter([
        "Let me calculate that. ACTION: calculator(15 * 7)",
        "The result is 105. FINAL: 15 multiplied by 7 equals 105.",
    ])

    def mock_llm(prompt: str) -> str:
        return next(responses)

    agent = ReActAgent(tools)
    result = agent.run("What is 15 multiplied by 7?", mock_llm)
    print(f"Result: {result}")

    print("\n=== Action Parser ===")
    print(parse_action("ACTION: web_search(Python decorators)"))   # ('web_search', 'Python decorators')
    print(parse_action("The answer is 42."))                        # None
    print(parse_action("Thinking... ACTION: calculator(2 + 2)"))   # ('calculator', '2 + 2')
