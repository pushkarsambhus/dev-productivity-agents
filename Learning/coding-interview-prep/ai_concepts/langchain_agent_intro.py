# LangChain is a popular framework for building applications powered by language models.
# It provides ready-made components: chains, agents, tools, and memory — so you don't
# have to build everything from scratch like we did in the other files.

# =============================================================================
# INSTALLATION
# =============================================================================
#   pip install langchain langchain-anthropic langchain-openai

# =============================================================================
# CORE LANGCHAIN CONCEPTS
# =============================================================================
#
# 1. MODEL (LLM)
#    The language model at the center of everything.
#    LangChain wraps models from OpenAI, Anthropic, Cohere, etc.
#    in a standard interface.
#
# 2. PROMPT TEMPLATE
#    A reusable template for building prompts with dynamic content.
#    Like an f-string, but with LangChain's extras.
#
# 3. CHAIN
#    A sequence of steps: PromptTemplate → LLM → OutputParser
#    The "chain" connects these components into a pipeline.
#    "LCEL" (LangChain Expression Language) uses | to connect them:
#      chain = prompt | llm | output_parser
#
# 4. TOOL
#    A function the agent can call. Same concept as Anthropic tool use.
#    Decorated with @tool to register it.
#
# 5. AGENT
#    An LLM that reasons about which tools to use and when.
#    The AgentExecutor handles the think → act → observe loop.
#
# 6. MEMORY
#    ConversationBufferMemory, ConversationSummaryMemory, etc.
#    Automatically manages conversation history for you.
#
# 7. RETRIEVER / RAG
#    Retrieval-Augmented Generation: fetch relevant documents
#    from a vector store and inject them into the prompt.
#    This is how "chat with your documents" products work.

# =============================================================================
# ARCHITECTURE DIAGRAM
# =============================================================================
#
#  User Input
#       │
#       ▼
#  ┌──────────────┐
#  │PromptTemplate│  ← fills in variables
#  └──────┬───────┘
#         │
#         ▼
#  ┌──────────────┐
#  │  LLM (Claude │  ← generates text
#  │   or GPT)    │
#  └──────┬───────┘
#         │
#         ▼
#  ┌──────────────┐
#  │OutputParser  │  ← extracts structured data from response
#  └──────┬───────┘
#         │
#         ▼
#  Final Output (string, JSON, Python object...)

# =============================================================================
# SKELETON CODE — shows structure even without installation
# =============================================================================

# This is what a LangChain agent looks like.
# Comments explain each component.

LANGCHAIN_AGENT_SKELETON = '''
# ============================================================
# LangChain Agent — Full Skeleton (requires langchain installed)
# ============================================================

from langchain_anthropic import ChatAnthropic       # LLM wrapper
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
import os

# --- Step 1: Define tools using the @tool decorator ---

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Use for any math question."""
    import math
    allowed = {"sqrt": math.sqrt, "pi": math.pi, "abs": abs}
    return str(eval(expression, {"__builtins__": {}}, allowed))

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city. Call this for weather questions."""
    # In reality: call a weather API
    return f"Weather in {city}: Sunny, 22°C"

tools = [calculator, get_weather]   # list of all available tools

# --- Step 2: Set up the LLM ---
llm = ChatAnthropic(
    model="claude-opus-4-6",
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

# --- Step 3: Create the prompt template ---
# MessagesPlaceholder("chat_history") = where conversation history goes
# MessagesPlaceholder("agent_scratchpad") = where tool calls/results go

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    MessagesPlaceholder("chat_history"),          # conversation history
    ("human", "{input}"),                         # user's message
    MessagesPlaceholder("agent_scratchpad"),       # tool use scratch space
])

# --- Step 4: Create short-term memory ---
memory = ConversationBufferMemory(
    memory_key="chat_history",     # must match MessagesPlaceholder key
    return_messages=True
)

# --- Step 5: Create the agent and executor ---
agent = create_tool_calling_agent(llm, tools, prompt)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,       # prints each thought/action step (great for learning)
    max_iterations=5,
)

# --- Step 6: Run the agent ---
result1 = executor.invoke({"input": "What is 42 * 17?"})
print(result1["output"])

result2 = executor.invoke({"input": "What's the weather in Paris?"})
print(result2["output"])

# Memory means the agent remembers previous turns:
result3 = executor.invoke({"input": "What did I just ask about?"})
print(result3["output"])   # Should mention the weather question
'''

# =============================================================================
# COMPARISON: Raw Anthropic SDK vs LangChain
# =============================================================================

COMPARISON = {
    "Task": [
        "Define a tool",
        "Set up memory",
        "Handle tool calls",
        "Multi-step chains",
        "Structured output",
        "RAG / document retrieval",
        "Switch between models",
    ],
    "Raw Anthropic SDK": [
        "Write JSON schema manually",
        "Manage list manually",
        "Write loop manually",
        "Write each step manually",
        "Parse response manually",
        "Build from scratch",
        "Change API call",
    ],
    "LangChain": [
        "@tool decorator",
        "ConversationBufferMemory()",
        "AgentExecutor handles it",
        "chain = prompt | llm | parser",
        "PydanticOutputParser",
        "VectorStore + Retriever",
        "Swap ChatAnthropic for ChatOpenAI",
    ]
}

# =============================================================================
# LCEL (LangChain Expression Language) — pipe-based chains
# =============================================================================

LCEL_EXAMPLES = """
# LCEL chains connect components with the | operator (like Unix pipes)

# Simple chain: prompt → LLM → string output
from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain.schema.output_parser import StrOutputParser

prompt = ChatPromptTemplate.from_template("Tell me a fact about {topic}")
llm    = ChatAnthropic(model="claude-haiku-4-5-20251001")   # faster/cheaper model
parser = StrOutputParser()

chain = prompt | llm | parser      # this IS the chain

result = chain.invoke({"topic": "penguins"})   # runs the whole pipeline
print(result)

# More complex: add a second LLM call to translate the result
translate_prompt = ChatPromptTemplate.from_template("Translate to French: {text}")
translate_chain = {"text": chain} | translate_prompt | llm | parser

french_result = translate_chain.invoke({"topic": "penguins"})
print(french_result)
"""

if __name__ == "__main__":
    print("=" * 60)
    print("LANGCHAIN AGENT CONCEPTS")
    print("=" * 60)

    print("""
LangChain provides building blocks for LLM apps:

  Model      → wraps LLMs (Claude, GPT, Llama, etc.)
  Prompt     → reusable templates with variables
  Chain      → connects prompt → LLM → parser
  Tool       → function the agent can call
  Agent      → LLM that reasons about tool use
  Memory     → manages conversation history
  Retriever  → fetches documents from a knowledge base

Install:  pip install langchain langchain-anthropic
API key:  export ANTHROPIC_API_KEY="sk-ant-..."
""")

    print("=== SKELETON CODE ===")
    print(LANGCHAIN_AGENT_SKELETON)

    print("\n=== RAW SDK vs LANGCHAIN COMPARISON ===")
    col_w = 32
    print(f"{'Task':<25} | {'Raw SDK':<{col_w}} | {'LangChain':<{col_w}}")
    print("-" * (25 + col_w * 2 + 6))
    for task, raw, lc in zip(COMPARISON["Task"], COMPARISON["Raw Anthropic SDK"], COMPARISON["LangChain"]):
        print(f"{task:<25} | {raw:<{col_w}} | {lc:<{col_w}}")

    print("\n=== LCEL (LangChain Expression Language) ===")
    print(LCEL_EXAMPLES)

    print("\nWhen to use LangChain:")
    print("  ✓ Rapid prototyping")
    print("  ✓ Multi-step pipelines")
    print("  ✓ RAG / document Q&A")
    print("  ✓ Switching between LLM providers")
    print("\nWhen to use raw SDK:")
    print("  ✓ Full control over API calls")
    print("  ✓ Simple single-model applications")
    print("  ✓ Minimizing dependencies")
    print("  ✓ Understanding what's happening under the hood")
