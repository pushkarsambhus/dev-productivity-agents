"""
Simple Agent System - Tool Calling and Decision Making
======================================================

WHAT IS AN AGENT?
An agent is a system that can:
1. Understand a user's request
2. Decide which tool(s) to use
3. Execute the tool
4. Return a formatted response

DIFFERENCE FROM A REGULAR API:
- Regular API: User calls specific endpoint (deterministic)
- Agent: User describes what they want; agent figures out how to do it (dynamic)

REAL-WORLD EXAMPLES:
- ChatGPT with function calling
- GitHub Copilot suggesting code
- Virtual assistants (Alexa, Siri)
- AutoGPT, LangChain agents

INTERVIEW TIP: Modern agents use LLMs (Large Language Models) to:
- Parse natural language
- Reason about which tools to use
- Generate human-friendly responses

This simplified version uses pattern matching instead of an LLM to demonstrate
the core concept without requiring API keys.
"""

import re
from typing import Dict, Any, List, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class Tool:
    """
    A tool is a function the agent can call.

    CONCEPT: Tools are the agent's "hands" - how it interacts with the world.

    In production systems:
    - Tools have descriptions that help the AI decide when to use them
    - Tools validate their inputs
    - Tools handle errors gracefully
    """

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters or []

    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        try:
            return self.function(**kwargs)
        except Exception as e:
            logger.error(f"Tool {self.name} failed: {str(e)}")
            return f"Error executing {self.name}: {str(e)}"


class SimpleAgent:
    """
    A simple agent that demonstrates tool calling.

    ARCHITECTURE:
    1. Tool Registry: Stores available tools
    2. Intent Recognition: Determines what the user wants
    3. Tool Selection: Picks the right tool
    4. Execution: Runs the tool and formats the response

    INTERVIEW TIP: In production, you'd use an LLM for steps 2-3:
    - OpenAI's function calling
    - Anthropic's tool use
    - Open-source models with function calling
    """

    def __init__(self):
        """Initialize the agent with a set of tools."""
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """
        Register default tools available to the agent.

        CONCEPT: Tool registration - making capabilities available to the agent.

        In production:
        - Tools can be dynamically loaded from plugins
        - Tools can require authentication/permissions
        - Tools can have usage limits or costs
        """
        # Tool 1: Calculate math expressions
        self.register_tool(
            name="calculator",
            description="Performs mathematical calculations",
            function=self._calculate,
            parameters=["expression"]
        )

        # Tool 2: Get weather information
        self.register_tool(
            name="weather",
            description="Gets weather information for a location",
            function=self._get_weather,
            parameters=["location"]
        )

        # Tool 3: Search for information
        self.register_tool(
            name="search",
            description="Searches for information on a topic",
            function=self._search,
            parameters=["query"]
        )

        # Tool 4: Get current time
        self.register_tool(
            name="time",
            description="Gets the current time",
            function=self._get_time,
            parameters=[]
        )

    def register_tool(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[List[str]] = None
    ):
        """
        Register a new tool with the agent.

        INTERVIEW TIP: This pattern (plugin/registry) is common in:
        - WordPress (plugins)
        - VS Code (extensions)
        - Kubernetes (custom resources)
        """
        tool = Tool(name, description, function, parameters)
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools with their descriptions."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools.values()
        ]

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main agent execution loop.

        CONCEPT: Agent workflow
        1. Parse the task to understand intent
        2. Select appropriate tool
        3. Extract parameters from the task
        4. Execute the tool
        5. Format and return the response

        REAL-WORLD: In production agents (LangChain, AutoGPT):
        - LLM analyzes the task
        - LLM decides which tool(s) to use
        - LLM extracts parameters
        - Tools execute
        - LLM formats the final response

        WHY USE AN AGENT?
        - Flexibility: Handle varied user requests without coding each one
        - Natural language: Users don't need to know exact API endpoints
        - Multi-step tasks: Agent can chain tools together
        - Adaptability: Add new tools without changing the interface
        """
        logger.info(f"Agent processing task: {task}")

        # Step 1: Intent recognition (simplified pattern matching)
        # In production: Use an LLM to understand intent
        task_lower = task.lower()

        # Step 2: Tool selection based on keywords
        # In production: LLM chooses based on tool descriptions
        selected_tool = None
        params = {}

        if any(word in task_lower for word in ["calculate", "compute", "math", "+"]):
            selected_tool = "calculator"
            # Extract mathematical expression
            # Simple pattern: look for numbers and operators
            match = re.search(r'[\d\s\+\-\*/\(\)\.]+', task)
            if match:
                params["expression"] = match.group().strip()
            else:
                return {
                    "result": "I couldn't find a mathematical expression to calculate.",
                    "tool_used": None
                }

        elif any(word in task_lower for word in ["weather", "temperature", "forecast"]):
            selected_tool = "weather"
            # Extract location
            # Look for "in [location]" or "at [location]"
            match = re.search(r'(?:in|at|for)\s+([a-zA-Z\s]+?)(?:\?|$)', task)
            if match:
                params["location"] = match.group(1).strip()
            else:
                params["location"] = "unknown"

        elif any(word in task_lower for word in ["search", "find", "look up", "what is"]):
            selected_tool = "search"
            # Extract search query (everything after trigger word)
            for trigger in ["search for", "find", "look up", "what is"]:
                if trigger in task_lower:
                    params["query"] = task_lower.split(trigger, 1)[1].strip().rstrip("?")
                    break
            if not params.get("query"):
                params["query"] = task

        elif any(word in task_lower for word in ["time", "clock", "what time"]):
            selected_tool = "time"
            # No parameters needed

        else:
            # Default to search if no specific tool matches
            selected_tool = "search"
            params["query"] = task

        # Step 3: Execute the selected tool
        if selected_tool and selected_tool in self.tools:
            tool = self.tools[selected_tool]
            logger.info(f"Executing tool: {selected_tool} with params: {params}")
            result = tool.execute(**params)

            return {
                "result": result,
                "tool_used": selected_tool
            }
        else:
            return {
                "result": "I'm not sure how to help with that task.",
                "tool_used": None
            }

    # ============================================================================
    # TOOL IMPLEMENTATIONS
    # ============================================================================
    # These are the actual functions the agent can call.
    # In a real system, these might call external APIs, databases, etc.

    def _calculate(self, expression: str) -> str:
        """
        Calculator tool - evaluates mathematical expressions.

        SECURITY NOTE: Using eval() is dangerous in production!
        - Users could execute arbitrary code
        - Use a safe math parser instead (e.g., py-expression-eval)

        INTERVIEW TIP: Always discuss security implications:
        - Input validation
        - Sandboxing
        - Rate limiting
        """
        try:
            # WARNING: eval() is unsafe - only for demonstration
            # In production, use a safe expression evaluator
            result = eval(expression, {"__builtins__": {}}, {})
            return f"The result is: {result}"
        except Exception as e:
            return f"I couldn't calculate that: {str(e)}"

    def _get_weather(self, location: str) -> str:
        """
        Weather tool - gets weather information.

        REAL-WORLD: Would call an external API like:
        - OpenWeatherMap
        - Weather.gov
        - AccuWeather

        INTERVIEW TIP: When integrating external APIs:
        - Cache responses to reduce API calls
        - Handle rate limits
        - Implement retry logic with exponential backoff
        - Monitor API costs
        """
        # Mock response (in production, call actual weather API)
        weather_data = {
            "san francisco": "Sunny, 68°F",
            "new york": "Cloudy, 45°F",
            "london": "Rainy, 52°F",
            "tokyo": "Clear, 72°F"
        }

        location_key = location.lower().strip()
        weather = weather_data.get(location_key, "I don't have weather data for that location")

        return f"The weather in {location} is: {weather}"

    def _search(self, query: str) -> str:
        """
        Search tool - finds information.

        REAL-WORLD: Would integrate with:
        - Google Custom Search API
        - Elasticsearch
        - Vector databases (Pinecone, Weaviate)
        - Internal knowledge bases

        INTERVIEW TIP: Modern AI agents use vector search:
        - Convert query to embeddings
        - Find similar documents in vector DB
        - Use as context for LLM response
        """
        # Mock knowledge base
        knowledge = {
            "kubernetes": "Kubernetes (K8s) is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.",
            "docker": "Docker is a platform for developing, shipping, and running applications in containers. Containers package code and dependencies together.",
            "redis": "Redis is an in-memory data structure store used as a database, cache, and message broker. It's extremely fast because data lives in RAM.",
            "fastapi": "FastAPI is a modern, fast web framework for building APIs with Python. It uses type hints for automatic validation and documentation.",
            "rest api": "REST (Representational State Transfer) is an architectural style for designing networked applications using HTTP methods and stateless communication."
        }

        # Simple keyword matching
        query_lower = query.lower()
        for key, value in knowledge.items():
            if key in query_lower:
                return value

        return f"I searched for '{query}' but couldn't find specific information. In a real system, this would search a knowledge base or the internet."

    def _get_time(self) -> str:
        """
        Time tool - gets current time.

        REAL-WORLD: Might also handle:
        - Timezones
        - Time format preferences
        - Scheduling/reminders
        """
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p on %B %d, %Y")
        return f"The current time is: {current_time}"


# ============================================================================
# INTERVIEW TALKING POINTS - AGENT SYSTEMS
# ============================================================================
"""
KEY CONCEPTS TO EXPLAIN:

1. What is an Agent?
   - Software that acts autonomously to achieve goals
   - Makes decisions about which actions to take
   - Different from traditional APIs that follow fixed logic

2. Agent Architecture (Modern AI Agents):
   - LLM Brain: Language model that reasons and makes decisions
   - Tools/Functions: Capabilities the agent can use
   - Memory: Context from previous interactions (optional)
   - Planning: Breaking down complex tasks into steps

3. Tool Calling Pattern:
   - Agent receives a task
   - Agent analyzes task and available tools
   - Agent selects appropriate tool(s)
   - Agent executes tool(s)
   - Agent formats response

4. Why Use Agents?
   - Natural language interface (user-friendly)
   - Flexibility (handle varied requests)
   - Composability (combine tools in novel ways)
   - Adaptability (add new tools without changing code)

5. Challenges with Agents:
   - Reliability: LLMs can make mistakes
   - Latency: Multiple steps = slower responses
   - Cost: LLM API calls can be expensive
   - Security: Need to sandbox tool execution
   - Debugging: Hard to trace agent reasoning

6. Real-World Examples:
   - ChatGPT Plugins: Agent calls external tools
   - GitHub Copilot: Suggests code based on context
   - Customer Service Bots: Route queries, lookup info
   - Trading Bots: Analyze markets, execute trades

7. Production Considerations:
   - Rate limiting (prevent abuse)
   - Tool permissions (not all users get all tools)
   - Audit logging (track what agents do)
   - Fallback strategies (what if agent fails?)
   - Human in the loop (for high-stakes decisions)

8. Agent Frameworks in Industry:
   - LangChain: Popular Python framework
   - AutoGPT: Autonomous goal-driven agents
   - BabyAGI: Task-driven autonomous agent
   - Semantic Kernel: Microsoft's agent framework
   - Anthropic's Claude with tool use

9. How This Scales:
   - Simple version: Pattern matching (what we built)
   - Production version: LLM-powered decision making
   - Enterprise version: Multi-agent systems, orchestration
"""
