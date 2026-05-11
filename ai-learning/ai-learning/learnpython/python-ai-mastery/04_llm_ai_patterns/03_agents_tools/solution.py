"""
SOLUTION: Phase 4 | LLM / AI Patterns | 03 Agents & Tools
"""
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[[str], str]

    def __call__(self, input_str: str) -> str:
        return self.fn(input_str)


@dataclass
class Message:
    role: str
    content: str


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def call(self, tool_name: str, input_str: str) -> str:
        if tool_name not in self._tools:
            return f"Error: unknown tool '{tool_name}'"
        try:
            return self._tools[tool_name](input_str)
        except Exception as e:
            return f"Error running {tool_name}: {e}"

    def describe_all(self) -> str:
        return "\n".join(
            f"  - {t.name}: {t.description}" for t in self._tools.values()
        )


def parse_action(llm_response: str) -> tuple[str, str] | None:
    marker = "ACTION:"
    idx = llm_response.find(marker)
    if idx == -1:
        return None
    action_str = llm_response[idx + len(marker):].strip()
    # action_str is like "tool_name(input)"
    paren_open = action_str.find("(")
    paren_close = action_str.rfind(")")   # rfind in case input contains parens
    if paren_open == -1 or paren_close == -1:
        return None
    tool_name = action_str[:paren_open].strip()
    tool_input = action_str[paren_open + 1 : paren_close].strip()
    return (tool_name, tool_input)


class ReActAgent:
    def __init__(self, tools: list[Tool], max_steps: int = 5):
        self.registry = ToolRegistry()
        for tool in tools:
            self.registry.register(tool)
        self.max_steps = max_steps
        self.history: list[Message] = []

    def _build_prompt(self, user_query: str) -> str:
        tool_desc = self.registry.describe_all()
        history_str = "\n".join(f"{m.role}: {m.content}" for m in self.history)
        return (
            f"Available tools:\n{tool_desc}\n\n"
            f"To use a tool, write: ACTION: tool_name(input)\n"
            f"When done, write: FINAL: your answer\n\n"
            f"History:\n{history_str}\n\nuser: {user_query}"
        )

    def run(self, user_query: str, llm_fn: Callable[[str], str]) -> str:
        self.history.append(Message("user", user_query))

        for step in range(self.max_steps):
            prompt = self._build_prompt(user_query)
            response = llm_fn(prompt)
            self.history.append(Message("assistant", response))
            print(f"  [step {step+1}] {response[:100]}")

            if "FINAL:" in response:
                final_idx = response.find("FINAL:") + len("FINAL:")
                return response[final_idx:].strip()

            action = parse_action(response)
            if action:
                tool_name, tool_input = action
                result = self.registry.call(tool_name, tool_input)
                print(f"  [tool:{tool_name}] {result}")
                self.history.append(Message("tool", f"{tool_name}({tool_input}) → {result}"))
            else:
                break   # LLM didn't act or finish — exit loop

        return "Agent could not complete task"


# ── Interview talking points ───────────────────────────────────────────────────
"""
Q: How does this compare to your smolagents work?
A: smolagents CodeAgent generates Python code as actions rather than
   tool_name(input) strings. The loop structure is identical — think, act,
   observe. The difference is the action format and execution sandbox.

Q: What are the failure modes of ReAct agents?
A: 1. Hallucinated tool calls (wrong tool name, bad input format)
   2. Infinite loops (max_steps prevents this)
   3. Tool errors not handled gracefully
   4. Context window overflow on long histories
   5. LLM "gives up" and writes FINAL: too early

Q: How would you make this production-ready?
A: - Structured output (JSON tool calls) instead of text parsing
   - Tool input validation with Pydantic
   - Async tool execution for parallel calls
   - Streaming responses
   - Observability: log each step to LangSmith/DeepEval
   This is exactly the gap between your prototype and a production agent.
"""

if __name__ == "__main__":
    tools = [
        Tool("calculator", "Evaluates a math expression.",
             lambda expr: str(eval(expr))),
        Tool("upper", "Converts text to uppercase.",
             lambda text: text.upper()),
        Tool("word_count", "Counts words in text.",
             lambda text: str(len(text.split()))),
    ]

    responses = iter([
        "Let me calculate that. ACTION: calculator(15 * 7)",
        "The result is 105. FINAL: 15 multiplied by 7 equals 105.",
    ])

    def mock_llm(prompt: str) -> str:
        return next(responses)

    agent = ReActAgent(tools)
    result = agent.run("What is 15 multiplied by 7?", mock_llm)
    print(f"\nFinal answer: {result}")

    print("\n=== Action Parser ===")
    print(parse_action("ACTION: web_search(Python decorators)"))
    print(parse_action("The answer is 42."))
    print(parse_action("Thinking... ACTION: calculator(2 + 2)"))
