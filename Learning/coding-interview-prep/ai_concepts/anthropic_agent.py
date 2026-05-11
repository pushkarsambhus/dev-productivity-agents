# This file shows how to build a real AI agent using the Anthropic Python SDK.
# Claude supports "tool use" — you define tools as JSON schemas, and Claude decides
# when and how to call them. This is how production AI agents are built.

# =============================================================================
# SETUP
# =============================================================================
# Install the Anthropic SDK:
#   pip install anthropic
#
# Get an API key:
#   1. Go to https://console.anthropic.com
#   2. Create an account and generate an API key
#   3. Set it as an environment variable:
#      export ANTHROPIC_API_KEY="sk-ant-..."
#
# Then run this file:
#   python anthropic_agent.py

# =============================================================================
# HOW ANTHROPIC TOOL USE WORKS
# =============================================================================
#
#  You send Claude:
#    - A system prompt (agent's instructions/persona)
#    - A list of tool definitions (JSON schemas describing what tools exist)
#    - The conversation messages
#
#  Claude responds with EITHER:
#    a) A text response (if no tool is needed), OR
#    b) A tool_use block: {"name": "tool_name", "input": {...}}
#
#  If Claude wants to use a tool:
#    - You execute the tool yourself (in Python)
#    - You send Claude the result as a "tool_result" message
#    - Claude then generates the final response
#
#  This back-and-forth continues until Claude gives a final text response.

import os
import json
import math
import datetime

# =============================================================================
# TOOL IMPLEMENTATIONS (the actual Python functions that do the work)
# =============================================================================

def calculator(expression: str) -> str:
    """Evaluate a math expression safely."""
    try:
        allowed = {"sqrt": math.sqrt, "pi": math.pi, "abs": abs, "round": round}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_weather(city: str) -> str:
    """Get current weather (mocked)."""
    weather_db = {
        "london": "Partly cloudy, 15°C, humidity 75%",
        "paris":  "Sunny, 22°C, humidity 55%",
        "tokyo":  "Rainy, 18°C, humidity 88%",
    }
    return weather_db.get(city.lower(), f"Weather data unavailable for {city}")

def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Map tool names to Python functions
TOOL_FUNCTIONS = {
    "calculator":    calculator,
    "get_weather":   get_weather,
    "get_current_time": get_current_time,
}

# =============================================================================
# TOOL DEFINITIONS (JSON schemas sent to Claude)
# =============================================================================
# Claude uses these schemas to understand:
#   - What tools are available
#   - What each tool does
#   - What parameters each tool expects
#
# The format follows the Anthropic tool use specification.

TOOL_DEFINITIONS = [
    {
        "name": "calculator",
        "description": "Evaluate a mathematical expression. Supports +, -, *, /, **, sqrt, pi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate, e.g. '2 * (3 + 4)' or 'sqrt(144)'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get the current weather conditions for a given city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city, e.g. 'London', 'Paris', 'Tokyo'"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Get the current date and time.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

# =============================================================================
# THE AGENT CLASS
# =============================================================================

class AnthropicAgent:
    """
    A production-style agent using the Anthropic Python SDK.

    The agent:
    1. Sends user messages to Claude
    2. Checks if Claude wants to use a tool
    3. If yes: runs the tool and sends the result back to Claude
    4. Repeats until Claude gives a final text response
    """

    def __init__(self, api_key: str = None):
        # Get API key from argument or environment variable
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

        if not self.api_key:
            print("⚠️  No API key found. Set ANTHROPIC_API_KEY environment variable.")
            print("   Running in DEMO MODE — showing code structure only.\n")
            self.client = None
        else:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                print("✓ Anthropic client initialized")
            except ImportError:
                print("⚠️  anthropic package not installed. Run: pip install anthropic")
                self.client = None

        self.model = "claude-opus-4-6"          # which Claude model to use
        self.system_prompt = (
            "You are a helpful assistant with access to tools for math, weather, and time. "
            "Use tools when they would help answer the user's question more accurately. "
            "Always be concise and friendly."
        )
        self.conversation_history = []          # tracks the full conversation

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """
        Run the requested tool and return the result as a string.
        This is YOUR code — Claude doesn't run the tool, you do.
        """
        print(f"  [Tool called: {tool_name}({tool_input})]")

        if tool_name not in TOOL_FUNCTIONS:
            return f"Error: Unknown tool '{tool_name}'"

        tool_fn = TOOL_FUNCTIONS[tool_name]
        result = tool_fn(**tool_input)

        print(f"  [Tool result: {result}]")
        return str(result)

    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response, handling tool calls automatically.
        This is the main agent loop.
        """
        print(f"\n{'─'*55}")
        print(f"User: {user_message}")

        if self.client is None:
            return self._demo_response(user_message)

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Agent loop: keep going until Claude gives a final text response
        max_iterations = 5   # prevent infinite loops
        for iteration in range(max_iterations):

            # Call the Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system_prompt,
                tools=TOOL_DEFINITIONS,           # give Claude the tool schemas
                messages=self.conversation_history
            )

            # Check what Claude wants to do
            if response.stop_reason == "tool_use":
                # Claude wants to use one or more tools
                tool_results = []

                for content_block in response.content:
                    if content_block.type == "tool_use":
                        # Execute the tool
                        tool_result = self._execute_tool(
                            content_block.name,
                            content_block.input
                        )
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": tool_result
                        })

                # Add Claude's tool-use message to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                # Add tool results to history so Claude can see them
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                # Loop again — Claude will now generate the final response

            elif response.stop_reason == "end_turn":
                # Claude is done — extract the text response
                final_text = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_text += block.text

                # Add to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_text
                })

                print(f"Agent: {final_text}")
                return final_text

        return "Max iterations reached."

    def _demo_response(self, user_message: str) -> str:
        """
        Demo mode: simulate what would happen without a real API key.
        This lets you understand the code structure without spending API credits.
        """
        text = user_message.lower()

        if any(w in text for w in ["calculate", "math", "+", "*", "sqrt"]):
            import re
            exprs = re.findall(r"[\d\s\+\-\*\/\.\(\)]+", user_message)
            expr = max(exprs, key=len).strip() if exprs else "2+2"
            tool_result = calculator(expr)
            return f"[DEMO] Claude would call calculator('{expr}') → {tool_result}. Final answer: The result is {tool_result}."

        elif any(w in text for w in ["weather", "temperature"]):
            city = "London"
            tool_result = get_weather(city)
            return f"[DEMO] Claude would call get_weather('{city}') → '{tool_result}'. Final answer: {tool_result}."

        elif "time" in text:
            tool_result = get_current_time()
            return f"[DEMO] Claude would call get_current_time() → '{tool_result}'. Final answer: The current time is {tool_result}."

        else:
            return "[DEMO] Claude would respond directly without tools: 'That's an interesting question! Let me help you with that...'"

if __name__ == "__main__":
    print("=" * 55)
    print("ANTHROPIC AGENT WITH TOOL USE")
    print("=" * 55)
    print("Model: claude-opus-4-6")
    print("Tools:", [t["name"] for t in TOOL_DEFINITIONS])

    # Create the agent
    # It will use ANTHROPIC_API_KEY from environment, or fall back to demo mode
    agent = AnthropicAgent()

    # Test questions
    test_questions = [
        "What is 25 * 48 + sqrt(144)?",
        "What's the weather like in Tokyo?",
        "What time is it right now?",
        "Can you tell me a fun fact about Python?",
    ]

    for question in test_questions:
        agent.chat(question)

    print(f"\n\nConversation had {len(agent.conversation_history)} messages total.")
    print("\nTo use with a real API key:")
    print("  export ANTHROPIC_API_KEY='sk-ant-...'")
    print("  python anthropic_agent.py")
