# The agentic loop is the core pattern behind every LLM-powered agent.
# This file implements it from scratch — fully mocked so it runs without an API key —
# but the pattern mirrors exactly how real agents (Claude, GPT, LangChain) work.

# =============================================================================
# THE AGENTIC LOOP PATTERN
# =============================================================================
#
#  ┌─────────────────────────────────────────────────────────────┐
#  │                   AGENTIC LOOP                              │
#  │                                                             │
#  │  1. Build messages: system + conversation + user input      │
#  │           │                                                  │
#  │           ▼                                                  │
#  │  2. Call LLM API → response                                  │
#  │           │                                                  │
#  │           ▼                                                  │
#  │  3. Is stop_reason "tool_use"?                               │
#  │           │                                                  │
#  │      YES──┤──────────────────────────────────────────┐      │
#  │           │                                          │      │
#  │           ▼                                          ▼      │
#  │  4. NO → extract text response      4. YES → execute tool   │
#  │           │                                          │      │
#  │           ▼                                          ▼      │
#  │  5. Return final answer         5. Add tool result to msgs  │
#  │                                          │                  │
#  │                                          └──────────────────┘
#  │                                          (loop back to step 2)│
#  └─────────────────────────────────────────────────────────────┘

import json
import math
import datetime
import random
from typing import Any

# =============================================================================
# MOCK LLM (simulates what a real LLM API would return)
# =============================================================================

class MockLLM:
    """
    Simulates an LLM API response.
    In production, you'd replace this with a real API call:
      response = anthropic.messages.create(...)
      or
      response = openai.chat.completions.create(...)
    """

    def __init__(self):
        self.call_count = 0

    def complete(self, messages, tools=None, system=None):
        """
        Takes messages + tool definitions, returns a mock response.
        Mirrors the structure of real API responses.
        """
        self.call_count += 1

        # Look at the last user message to decide what to respond
        last_user_msg = ""
        last_tool_result = ""

        for msg in reversed(messages):
            if msg["role"] == "user":
                if isinstance(msg["content"], list):
                    # This is a tool_result message
                    for block in msg["content"]:
                        if block.get("type") == "tool_result":
                            last_tool_result = block.get("content", "")
                else:
                    last_user_msg = msg["content"]
                break

        # If we have a tool result, generate the final answer using it
        if last_tool_result:
            return MockResponse(
                stop_reason="end_turn",
                content=[MockTextBlock(f"Based on the information gathered: {last_tool_result}. That's my final answer!")]
            )

        # Decide whether to use a tool or answer directly
        text = last_user_msg.lower()

        if any(w in text for w in ["calculate", "math", "sqrt", "+", "*", "/"]):
            import re
            exprs = re.findall(r"[\d\s\+\-\*\/\.\(\)sqrt]+", last_user_msg)
            expr = max(exprs, key=len).strip() if exprs else "2+2"
            return MockResponse(
                stop_reason="tool_use",
                content=[MockToolUseBlock(
                    tool_use_id="tool_001",
                    name="calculator",
                    input={"expression": expr}
                )]
            )
        elif any(w in text for w in ["weather", "temperature", "forecast"]):
            city = "London"
            for w in text.split():
                if w.istitle():
                    city = w
                    break
            return MockResponse(
                stop_reason="tool_use",
                content=[MockToolUseBlock(
                    tool_use_id="tool_002",
                    name="get_weather",
                    input={"city": city}
                )]
            )
        elif any(w in text for w in ["time", "date", "today"]):
            return MockResponse(
                stop_reason="tool_use",
                content=[MockToolUseBlock(
                    tool_use_id="tool_003",
                    name="get_current_time",
                    input={}
                )]
            )
        elif any(w in text for w in ["search", "find", "who is", "what is"]):
            query = text.replace("search for", "").replace("who is", "").replace("what is", "").strip()
            return MockResponse(
                stop_reason="tool_use",
                content=[MockToolUseBlock(
                    tool_use_id="tool_004",
                    name="web_search",
                    input={"query": query}
                )]
            )
        else:
            # Direct answer — no tool needed
            return MockResponse(
                stop_reason="end_turn",
                content=[MockTextBlock(f"I can help with that! '{last_user_msg}' is an interesting question. Let me answer directly: [mock answer based on my training knowledge].")]
            )

class MockResponse:
    def __init__(self, stop_reason, content):
        self.stop_reason = stop_reason
        self.content = content

class MockTextBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text

class MockToolUseBlock:
    def __init__(self, tool_use_id, name, input):
        self.type = "tool_use"
        self.id = tool_use_id
        self.name = name
        self.input = input

# =============================================================================
# TOOL IMPLEMENTATIONS
# =============================================================================

def calculator(expression: str) -> str:
    try:
        allowed = {"sqrt": math.sqrt, "pi": math.pi, "abs": abs, "round": round}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Calculation error: {e}"

def get_weather(city: str) -> str:
    mock_weather = {
        "london": "Overcast, 13°C, humidity 82%",
        "paris":  "Sunny, 21°C, humidity 50%",
        "tokyo":  "Light rain, 17°C, humidity 87%",
        "sydney": "Clear skies, 26°C, humidity 40%",
    }
    result = mock_weather.get(city.lower(), f"No weather data for {city}")
    return f"Weather in {city}: {result}"

def get_current_time() -> str:
    return f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"

def web_search(query: str) -> str:
    mock_results = {
        "python":      "Python: a versatile, beginner-friendly language used in web dev, data science, and AI.",
        "langchain":   "LangChain: framework for building LLM-powered apps. Provides chains, agents, memory, tools.",
        "anthropic":   "Anthropic: AI safety company founded 2021, creator of Claude AI assistant.",
        "claude":      "Claude: AI assistant made by Anthropic. Known for safety, helpfulness, and long context.",
    }
    for key, val in mock_results.items():
        if key in query.lower():
            return f"Search results: {val}"
    return f"Search results for '{query}': [No mock data — in production this calls a real search API]"

TOOLS = {
    "calculator":     calculator,
    "get_weather":    get_weather,
    "get_current_time": get_current_time,
    "web_search":     web_search,
}

# Tool definitions (JSON schemas) — same format as real Anthropic API
TOOL_DEFINITIONS = [
    {"name": "calculator",        "description": "Evaluate math expressions",     "input_schema": {"type": "object", "properties": {"expression": {"type": "string"}}}},
    {"name": "get_weather",       "description": "Get weather for a city",         "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}}},
    {"name": "get_current_time",  "description": "Get current date and time",      "input_schema": {"type": "object", "properties": {}}},
    {"name": "web_search",        "description": "Search the web for information", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}}},
]

# =============================================================================
# THE AGENTIC LOOP (the core pattern)
# =============================================================================

class AgenticLoop:
    """
    A raw implementation of the agentic loop pattern.

    This is exactly what happens inside Claude, GPT, and LangChain agents:
    1. Build message list
    2. Send to LLM
    3. If LLM wants a tool: run it, add result, loop again
    4. If LLM is done: return the text response
    """

    def __init__(self, llm, tools, system_prompt, max_iterations=10):
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.total_llm_calls = 0
        self.total_tool_calls = 0

    def run(self, user_message: str, conversation_history: list = None) -> str:
        """
        Run the agentic loop for a single user message.
        Returns the final text response.
        """
        # Start with conversation history + new user message
        messages = list(conversation_history or [])
        messages.append({"role": "user", "content": user_message})

        print(f"\n{'═'*60}")
        print(f"USER: {user_message}")
        print(f"{'─'*60}")

        for iteration in range(self.max_iterations):
            # ──────────────────────────────────────────────
            # STEP 1: CALL THE LLM
            # ──────────────────────────────────────────────
            print(f"\n[Iteration {iteration + 1}] Calling LLM...")
            response = self.llm.complete(
                messages=messages,
                tools=TOOL_DEFINITIONS,
                system=self.system_prompt
            )
            self.total_llm_calls += 1

            # ──────────────────────────────────────────────
            # STEP 2: CHECK STOP REASON
            # ──────────────────────────────────────────────
            if response.stop_reason == "end_turn":
                # LLM is done — extract and return the text
                final_text = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_text += block.text

                print(f"[LLM → end_turn] Final response ready.")
                # Add to message history
                messages.append({"role": "assistant", "content": final_text})
                print(f"\nAGENT: {final_text}")
                return final_text, messages

            elif response.stop_reason == "tool_use":
                # ──────────────────────────────────────────
                # STEP 3: EXECUTE TOOL(S)
                # ──────────────────────────────────────────
                # Add LLM's tool-use message to history
                messages.append({"role": "assistant", "content": response.content})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name  = block.name
                        tool_input = block.input
                        tool_id    = block.id

                        print(f"[LLM → tool_use] Calling: {tool_name}({json.dumps(tool_input)})")

                        # Execute the tool
                        if tool_name in self.tools:
                            result = self.tools[tool_name](**tool_input)
                        else:
                            result = f"Error: unknown tool '{tool_name}'"

                        self.total_tool_calls += 1
                        print(f"[Tool result]: {result}")

                        # Package the result for the next LLM call
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result
                        })

                # ──────────────────────────────────────────
                # STEP 4: ADD RESULTS TO MESSAGES AND LOOP
                # ──────────────────────────────────────────
                # The tool results go back to the LLM as a "user" message
                messages.append({"role": "user", "content": tool_results})
                print("[Looping back → LLM will now use these tool results]")
                # Continue the loop — LLM will now generate its final answer

        # If we exhaust max_iterations
        return "Max iterations reached without a final response.", messages

if __name__ == "__main__":
    print("=" * 60)
    print("THE AGENTIC LOOP — from scratch, fully mocked")
    print("=" * 60)

    system = (
        "You are a helpful assistant. Use tools when appropriate. "
        "Be concise and accurate."
    )

    llm   = MockLLM()
    agent = AgenticLoop(llm=llm, tools=TOOLS, system_prompt=system)

    # Shared conversation history across turns (demonstrates memory)
    history = []

    test_questions = [
        "What is sqrt(256) + 15 * 4?",
        "What's the weather in Tokyo?",
        "What time is it?",
        "Search for information about LangChain",
        "What is the capital of Australia?",   # no tool needed
    ]

    for question in test_questions:
        final_answer, history = agent.run(question, history)
        # Trim history to last 10 messages to avoid context overload
        history = history[-10:]

    print(f"\n\n{'='*60}")
    print("SESSION STATISTICS")
    print(f"{'='*60}")
    print(f"Total LLM calls:  {agent.total_llm_calls}")
    print(f"Total tool calls: {agent.total_tool_calls}")
    print(f"Iterations used:  {agent.total_llm_calls}")
    print(f"\nKey insight: Each tool use requires 2 LLM calls —")
    print("  1st call: LLM decides to use a tool")
    print("  2nd call: LLM generates response AFTER seeing tool result")
