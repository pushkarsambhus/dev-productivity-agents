# A tool-using agent is an agent that can call external functions ("tools") to get information
# or take actions it couldn't do alone. Think of it like a person with a smartphone:
# the person decides what to do, but uses apps (tools) to actually do it.

# =============================================================================
# HOW TOOL USE WORKS IN REAL LLM AGENTS
# =============================================================================
#
#  1. User asks: "What's the weather in Paris and convert 25°C to °F?"
#
#  2. Agent THINKS: "I need two tools:
#       - weather_lookup(city="Paris")
#       - convert_temperature(value=25, from="C", to="F")"
#
#  3. Agent CALLS the tools (one or more times)
#
#  4. Tools RETURN results:
#       - weather → "Sunny, 25°C"
#       - convert → 77.0°F
#
#  5. Agent COMPOSES final answer using tool results
#
# This is exactly how Claude, GPT-4, and other LLMs work with tools.

import math
import datetime
import json

# =============================================================================
# STEP 1: DEFINE TOOLS (just regular Python functions)
# =============================================================================

def calculator(expression: str) -> str:
    """
    Tool: evaluate a math expression safely.
    Supports: +, -, *, /, **, sqrt, and basic functions.
    """
    try:
        # Only allow safe math operations (no exec/eval of arbitrary code)
        allowed = {
            "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
            "abs": abs, "round": round, "pow": pow,
            "sin": math.sin, "cos": math.cos, "log": math.log,
        }
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as ex:
        return f"Error: {ex}"

def weather_lookup(city: str) -> str:
    """
    Tool: look up (mock) weather for a city.
    In a real agent, this would call a weather API like OpenWeatherMap.
    """
    # Mocked weather data — in reality you'd call an API here
    mock_data = {
        "london":   "Cloudy, 14°C, humidity 80%",
        "paris":    "Sunny, 22°C, humidity 55%",
        "new york": "Partly cloudy, 18°C, humidity 65%",
        "tokyo":    "Rainy, 19°C, humidity 90%",
        "sydney":   "Clear, 25°C, humidity 45%",
    }
    city_key = city.lower().strip()
    weather = mock_data.get(city_key, f"No weather data for '{city}' (this is a mock tool)")
    return f"Weather in {city}: {weather}"

def web_search(query: str) -> str:
    """
    Tool: perform a (mock) web search.
    In a real agent, this would call Google Search API, SerpAPI, Tavily, etc.
    """
    # Mocked search results
    mock_results = {
        "python":         "Python is a high-level programming language known for readability.",
        "machine learning": "Machine learning is a subset of AI that learns from data.",
        "openai":         "OpenAI is an AI research company founded in 2015.",
        "anthropic":      "Anthropic is an AI safety company that created Claude.",
        "langchain":      "LangChain is a framework for building LLM-powered applications.",
    }
    for key, result in mock_results.items():
        if key in query.lower():
            return f"Search results for '{query}': {result}"
    return f"Search results for '{query}': No mock data available (this is a simulated search)"

def get_current_time(timezone: str = "UTC") -> str:
    """
    Tool: get the current date and time.
    """
    now = datetime.datetime.utcnow()
    return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"

def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """
    Tool: convert between common units.
    """
    conversions = {
        ("km", "miles"):   lambda v: v * 0.621371,
        ("miles", "km"):   lambda v: v * 1.60934,
        ("kg", "lbs"):     lambda v: v * 2.20462,
        ("lbs", "kg"):     lambda v: v * 0.453592,
        ("celsius", "fahrenheit"): lambda v: v * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5/9,
        ("meters", "feet"):   lambda v: v * 3.28084,
        ("feet", "meters"):   lambda v: v * 0.3048,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {result:.4f} {to_unit}"
    return f"Conversion from {from_unit} to {to_unit} not supported."

# =============================================================================
# STEP 2: TOOL REGISTRY — a dictionary mapping tool names to functions
# =============================================================================
# This is how real agent frameworks (LangChain, Claude API) register tools.
# The agent looks up tools by name and calls them with arguments.

TOOLS = {
    "calculator":    calculator,
    "weather":       weather_lookup,
    "search":        web_search,
    "time":          get_current_time,
    "convert_units": unit_converter,
}

# =============================================================================
# STEP 3: THE TOOL-USING AGENT
# =============================================================================

class ToolUsingAgent:
    """
    An agent that selects and uses tools to answer user questions.

    In a real LLM agent, the "think" step is done by the language model.
    Here we use keyword matching to simulate that decision.
    """

    def __init__(self):
        self.tools = TOOLS
        self.call_log = []   # keeps track of every tool call made

    def think(self, user_input):
        """
        Decide which tool(s) to use and with what arguments.
        Returns a list of (tool_name, kwargs) tuples.

        In a real LLM agent: the model returns structured JSON like:
          {"tool": "weather", "args": {"city": "Paris"}}
        Here we simulate that with keyword detection.
        """
        text = user_input.lower()
        tool_calls = []

        # Detect weather request
        if any(w in text for w in ["weather", "temperature", "forecast"]):
            # Extract city name (simplified: take the word after "in" or "for")
            words = text.split()
            city = "London"   # default
            for i, word in enumerate(words):
                if word in ["in", "for"] and i + 1 < len(words):
                    city = words[i + 1].rstrip("?.,!")
                    break
            tool_calls.append(("weather", {"city": city}))

        # Detect math/calculation request
        if any(w in text for w in ["calculate", "what is", "compute", "math", "+", "*", "/"]):
            # Extract the expression (simplified)
            import re
            expr = re.findall(r"[\d\s\+\-\*\/\.\(\)]+", user_input)
            if expr:
                clean = max(expr, key=len).strip()
                if clean:
                    tool_calls.append(("calculator", {"expression": clean}))

        # Detect unit conversion request
        if any(w in text for w in ["convert", "in miles", "in km", "in fahrenheit", "in celsius", "in lbs"]):
            import re
            nums = re.findall(r'\d+\.?\d*', text)
            value = float(nums[0]) if nums else 100

            if "celsius" in text or "fahrenheit" in text:
                if "celsius" in text:
                    tool_calls.append(("convert_units", {"value": value, "from_unit": "celsius", "to_unit": "fahrenheit"}))
                else:
                    tool_calls.append(("convert_units", {"value": value, "from_unit": "fahrenheit", "to_unit": "celsius"}))
            elif "km" in text or "miles" in text:
                if "km" in text and "miles" in text:
                    tool_calls.append(("convert_units", {"value": value, "from_unit": "km", "to_unit": "miles"}))

        # Detect time request
        if any(w in text for w in ["time", "date", "what day", "current time"]):
            tool_calls.append(("time", {}))

        # Detect search request (fallback)
        if any(w in text for w in ["search", "find", "look up", "who is", "what is"]) and not tool_calls:
            # Use everything after "search for" or "what is" as query
            for trigger in ["search for", "look up", "who is", "what is", "find"]:
                if trigger in text:
                    query = text.split(trigger, 1)[-1].strip().rstrip("?")
                    tool_calls.append(("search", {"query": query}))
                    break

        # If nothing matched, just say so
        if not tool_calls:
            tool_calls.append(None)

        return tool_calls

    def use_tool(self, tool_name, kwargs):
        """
        Call a tool by name with the given arguments.
        Logs the call for transparency.
        """
        if tool_name not in self.tools:
            return f"Unknown tool: {tool_name}"

        tool_fn = self.tools[tool_name]
        result = tool_fn(**kwargs)                          # call the function

        # Log the tool call
        self.call_log.append({"tool": tool_name, "args": kwargs, "result": result})
        return result

    def respond(self, user_input):
        """
        Full agent turn: think → call tools → compose response.
        """
        print(f"\n{'─'*55}")
        print(f"User:  {user_input}")

        tool_calls = self.think(user_input)         # decide what to do

        if tool_calls == [None]:
            print("Agent: I'm not sure which tool to use for that. Try asking about weather, math, conversions, time, or web search.")
            return

        results = []
        for call in tool_calls:
            if call is None:
                continue
            tool_name, kwargs = call
            print(f"  [→ Calling tool: {tool_name}({kwargs})]")
            result = self.use_tool(tool_name, kwargs)  # call the tool
            print(f"  [← Tool result: {result}]")
            results.append(result)

        # Compose the final response from tool results
        if len(results) == 1:
            print(f"Agent: {results[0]}")
        else:
            print(f"Agent: Here are the results:")
            for r in results:
                print(f"  • {r}")

if __name__ == "__main__":
    print("=" * 55)
    print("TOOL-USING AGENT")
    print("=" * 55)

    agent = ToolUsingAgent()

    # Show all available tools
    print("\nAvailable tools:", list(agent.tools.keys()))

    # Run test interactions
    test_queries = [
        "What's the weather in Tokyo?",
        "Calculate 15 * 24 + 100",
        "What time is it?",
        "Convert 25 celsius to fahrenheit",
        "What is machine learning?",
        "Can you dance?",
    ]

    for query in test_queries:
        agent.respond(query)

    print(f"\n\n[Total tool calls made: {len(agent.call_log)}]")
    print("[Tool call log (last 3):]")
    for entry in agent.call_log[-3:]:
        print(f"  {entry['tool']}({entry['args']}) → {entry['result'][:60]}...")
