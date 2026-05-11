"""
Coding Interview Prep — Week 8: AI, Agents & MCP
=================================================
Covers: AI/ML basics, Tokenization, Prompt Engineering, Agent Basics,
        Tool Use, Memory, Planning, Multi-Agent Systems, Anthropic SDK
"""

NAME        = "Week 8: AI & Agents"
DESCRIPTION = "AI fundamentals, prompt engineering, agents, tool use, MCP, Anthropic SDK"
ICON        = "🤖"

CONCEPTS = [
    {
        "title": "AI/ML Fundamentals & LLMs",
        "explanation": """**Machine Learning paradigms:**
- **Supervised**: labeled input→output pairs. Train model to predict. (classification, regression)
- **Unsupervised**: no labels, find hidden structure. (clustering, PCA)
- **Reinforcement**: agent learns by reward/punishment from environment.

**How LLMs work (simplified):**
1. **Tokenization**: text → tokens (subword pieces). ~1 word ≈ 1.3 tokens.
2. **Transformer**: attention mechanism learns relationships between tokens.
3. **Pre-training**: next-token prediction on massive text corpus.
4. **Fine-tuning**: adapt to specific tasks (instruction following, coding).
5. **RLHF**: align with human preferences using reward model + PPO.

**Key parameters:**
- Temperature: 0 = deterministic, 1 = creative/random
- Max tokens: output length limit
- Top-p / top-k: nucleus sampling controls diversity
- Context window: max input+output tokens (Claude: 200k, GPT-4: 128k)

**Inference terms:**
- Prompt: input text
- Completion: model's output
- System prompt: instructions that persist across the conversation
- Few-shot: examples embedded in the prompt""",
        "gotchas": [
            "Tokens ≠ words. 'unhappiness' might be ['un', 'happi', 'ness'] = 3 tokens.",
            "Temperature=0 is not truly deterministic due to floating point — but very close.",
            "Context window includes BOTH input and output tokens combined.",
        ],
        "videos": [
            {"title": "How LLMs Work (3Blue1Brown — Attention)", "url": "https://www.youtube.com/watch?v=eMlx5fFNoYc", "source": "YouTube"},
            {"title": "Intro to Large Language Models (Andrej Karpathy)", "url": "https://www.youtube.com/watch?v=zjkBMFhNj_g", "source": "YouTube"},
            {"title": "ChatGPT Prompt Engineering for Developers (deeplearning.ai)", "url": "https://www.udemy.com/course/chatgpt-prompt-engineering-for-developers-with-openai-api/", "source": "Udemy"},
        ],
    },
    {
        "title": "Prompt Engineering & Agent Architecture",
        "explanation": """**Prompt Engineering techniques:**
- **Zero-shot**: just instructions, no examples
- **Few-shot**: 2-5 input/output examples in the prompt
- **Chain-of-thought**: "think step by step" — improves reasoning
- **System prompt**: role + constraints + output format instructions

**Prompt injection (security):** User input that overrides system instructions — like SQL injection for LLMs. Mitigate with input sanitization and output validation.

**Agent architecture:**
```
User → Orchestrator (LLM) → Tools → Results → Orchestrator → User
```

**Agentic loop (ReAct pattern):**
```python
messages = [{"role": "user", "content": user_input}]
while True:
    response = client.messages.create(model=..., tools=tools, messages=messages)
    if response.stop_reason == "end_turn":
        return response.content[0].text
    # Tool call requested
    messages.append({"role": "assistant", "content": response.content})
    tool_results = execute_tools(response.content)
    messages.append({"role": "user", "content": tool_results})
```

**Tool use in Anthropic SDK:**
```python
tools = [{
    "name": "search",
    "description": "Search the web for current info",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"]
    }
}]
```

**MCP (Model Context Protocol):** Anthropic's standard for connecting LLMs to external tools — like USB for AI. Any MCP-compatible client can use any MCP server.""",
        "gotchas": [
            "stop_reason='tool_use' means the model wants to call a tool — don't return yet.",
            "tool_use_id must match the tool_result response — they're linked by ID.",
            "Always add a max_iterations guard in agentic loops to prevent infinite loops.",
            "Prompt injection: never trust raw user input passed to the model as instructions.",
        ],
        "videos": [
            {"title": "LLM Agents (Andrew Ng — deeplearning.ai)", "url": "https://www.youtube.com/watch?v=sal78ACtGTc", "source": "YouTube"},
            {"title": "Anthropic Tool Use Tutorial", "url": "https://www.youtube.com/watch?v=3BVbJVzL0gs", "source": "YouTube"},
            {"title": "LangChain & Agents (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=HSZ_uaif57o", "source": "YouTube"},
            {"title": "Building AI Apps with Anthropic Claude API", "url": "https://www.udemy.com/course/building-ai-apps-with-chatgpt-dalle-and-gpt-4/", "source": "Udemy"},
        ],
    },
]

QUESTIONS = [

    # ══════════════════════════════════════════════════════════════════
    # AI / ML BASICS
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "AI & ML Fundamentals",
        "question": (
            "What is the difference between supervised and unsupervised learning?"
        ),
        "options": [
            "A) Supervised uses labeled data, unsupervised finds patterns in unlabeled data",
            "B) Supervised is faster, unsupervised is more accurate",
            "C) Supervised works on images, unsupervised works on text",
            "D) They are the same — both require labeled training data",
        ],
        "correct_answer": "A) Supervised uses labeled data, unsupervised finds patterns in unlabeled data",
        "explanation": (
            "Supervised learning: training data has input-output pairs (labels). "
            "Model learns to map inputs to outputs. Examples: classification, regression. "
            "Unsupervised learning: no labels. Model finds hidden structure. Examples: clustering, dimensionality reduction. "
            "Reinforcement learning is a third paradigm: agent learns by reward/punishment from environment. "
            "LLMs like Claude/GPT are trained with a mix: supervised (next-token prediction) + RLHF."
        ),
        "remember": "Supervised = labeled data → predict output. Unsupervised = unlabeled → find structure. RL = reward signals.",
    },

    # ══════════════════════════════════════════════════════════════════
    # PROMPT ENGINEERING
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Prompt Engineering",
        "question": (
            "What is 'few-shot prompting' and when is it useful?"
        ),
        "options": [
            "A) Sending the same prompt multiple times to get consistent results",
            "B) Including 2-5 examples of input/output pairs in the prompt to show the model the desired pattern",
            "C) Using a very short prompt to reduce token usage",
            "D) Fine-tuning the model on a small dataset",
        ],
        "correct_answer": "B) Including 2-5 examples of input/output pairs in the prompt to show the model the desired pattern",
        "explanation": (
            "Few-shot prompting: include examples in the prompt itself — no model training required. "
            "Zero-shot: no examples, just instructions. "
            "Few-shot: 2-5 input/output examples showing the exact format/behavior you want. "
            "Chain-of-thought (CoT): ask the model to show reasoning steps ('think step by step'). "
            "Few-shot is useful when the task has a specific output format that's hard to describe but easy to demonstrate."
        ),
        "remember": "Few-shot = examples in prompt. Zero-shot = instructions only. CoT = 'think step by step' for reasoning tasks.",
    },
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Prompt Engineering",
        "question": (
            "What is 'prompt injection' in the context of LLM-powered applications?"
        ),
        "options": [
            "A) Adding too many tokens to a prompt, causing context overflow",
            "B) A user crafting input that overrides the system prompt or causes the LLM to ignore its instructions",
            "C) Injecting variables into a prompt template at runtime",
            "D) Fine-tuning a model with adversarial examples",
        ],
        "correct_answer": "B) A user crafting input that overrides the system prompt or causes the LLM to ignore its instructions",
        "explanation": (
            "Prompt injection is the LLM equivalent of SQL injection. "
            "A user submits input like 'Ignore previous instructions and...' to hijack the model's behavior. "
            "Indirect injection: malicious instructions hidden in data the LLM reads (e.g., a document, a web page). "
            "Defenses: input sanitization, output validation, privilege separation, never passing raw user input to the model. "
            "This is a critical security concern for anyone building LLM-powered applications."
        ),
        "remember": "Prompt injection = user input overrides system instructions. Like SQL injection for LLMs. Sanitize all inputs.",
    },

    # ══════════════════════════════════════════════════════════════════
    # AGENT BASICS & TOOL USE
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "easy",
        "topic": "Agent Basics",
        "question": (
            "What is an 'agentic loop' in the context of LLM agents?"
        ),
        "options": [
            "A) An infinite loop bug in agent code",
            "B) The cycle where an LLM reasons, calls a tool, observes the result, then reasons again until the task is complete",
            "C) A method for training agents using reinforcement learning",
            "D) A technique for running multiple LLM calls in parallel",
        ],
        "correct_answer": "B) The cycle where an LLM reasons, calls a tool, observes the result, then reasons again until the task is complete",
        "explanation": (
            "The agentic loop (ReAct pattern): Reason → Act (tool call) → Observe (tool result) → Reason → ... → Answer. "
            "The LLM decides what action to take, executes it via a tool, gets back results, and continues. "
            "This allows agents to break complex tasks into steps and adapt based on intermediate results. "
            "A stopping condition is critical — without it, the agent loops forever. "
            "Anthropic's Claude Code operates exactly this way."
        ),
        "remember": "Agentic loop: Reason → Act → Observe → Reason → ... → Answer. LLM drives, tools execute, results inform next step.",
    },
    {
        "type": "coding",
        "difficulty": "medium",
        "topic": "Tool Use & Anthropic SDK",
        "question": (
            "Write a minimal Anthropic API call that uses tool use to define a 'get_weather' tool.\n\n"
            "The tool should:\n"
            "- Accept a 'location' string parameter (required)\n"
            "- Be described as getting current weather for a location\n"
            "- Be passed to the API in a messages call\n\n"
            "Just define the tool + API call structure (mock the actual weather lookup)."
        ),
        "language": "python",
        "starter_code": (
            "import anthropic\n\n\n"
            "def call_with_weather_tool(user_message: str) -> str:\n"
            "    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var\n"
            "    # Define the tool and make the API call\n"
            "    pass\n"
        ),
        "correct_answer": (
            "import anthropic\n\n\n"
            "def call_with_weather_tool(user_message: str):\n"
            "    client = anthropic.Anthropic()\n\n"
            "    tools = [\n"
            "        {\n"
            "            'name': 'get_weather',\n"
            "            'description': 'Get current weather for a location',\n"
            "            'input_schema': {\n"
            "                'type': 'object',\n"
            "                'properties': {\n"
            "                    'location': {\n"
            "                        'type': 'string',\n"
            "                        'description': 'The city or location to get weather for'\n"
            "                    }\n"
            "                },\n"
            "                'required': ['location']\n"
            "            }\n"
            "        }\n"
            "    ]\n\n"
            "    response = client.messages.create(\n"
            "        model='claude-opus-4-6',\n"
            "        max_tokens=1024,\n"
            "        tools=tools,\n"
            "        messages=[{'role': 'user', 'content': user_message}]\n"
            "    )\n"
            "    return response\n"
        ),
        "explanation": (
            "Tool use in Anthropic SDK: tools are defined as a list of dicts with name, description, and input_schema. "
            "input_schema follows JSON Schema format — type, properties, required. "
            "When the model wants to call a tool, stop_reason is 'tool_use' and the response contains a ToolUseBlock. "
            "You then execute the tool and return the result in the next message with role='user', type='tool_result'. "
            "This is the foundation of all agent systems built on Claude."
        ),
        "remember": "Tool use: define in tools=[{name, description, input_schema}]. Check stop_reason=='tool_use'. Return result as tool_result message.",
    },

    # ══════════════════════════════════════════════════════════════════
    # MEMORY & MULTI-AGENT
    # ══════════════════════════════════════════════════════════════════
    {
        "type": "mcq",
        "difficulty": "medium",
        "topic": "Agent Memory",
        "question": (
            "What are the four main types of memory in LLM agent systems?"
        ),
        "options": [
            "A) RAM, disk, cache, and network",
            "B) In-context (conversation history), external (vector DB/files), episodic (past sessions), and semantic (knowledge)",
            "C) Short-term, long-term, working, and procedural",
            "D) Prompt, completion, embedding, and fine-tune",
        ],
        "correct_answer": "B) In-context (conversation history), external (vector DB/files), episodic (past sessions), and semantic (knowledge)",
        "explanation": (
            "Agent memory types: "
            "1. In-context: the current conversation window — fastest but limited by context length. "
            "2. External: vector databases (RAG), files, databases — unlimited but requires retrieval. "
            "3. Episodic: summaries of past interactions stored and retrieved by similarity. "
            "4. Semantic: encoded world knowledge from training. "
            "Real systems combine these: in-context for recent turns, vector DB for long-term retrieval."
        ),
        "remember": "Agent memory: in-context (chat history), external (vector DB), episodic (past sessions), semantic (training knowledge).",
    },
    {
        "type": "mcq",
        "difficulty": "hard",
        "topic": "Multi-Agent Systems & MCP",
        "question": (
            "What problem does the Model Context Protocol (MCP) solve in multi-agent systems?"
        ),
        "options": [
            "A) It compresses context to fit more tokens in the LLM window",
            "B) It provides a standardized interface for LLMs to connect to external tools and data sources, replacing custom integrations",
            "C) It enables agents to communicate directly with each other without a central orchestrator",
            "D) It is a fine-tuning protocol for specializing models for specific tools",
        ],
        "correct_answer": "B) It provides a standardized interface for LLMs to connect to external tools and data sources, replacing custom integrations",
        "explanation": (
            "Before MCP, every tool integration was custom code — bespoke API wrappers for each combination of LLM + tool. "
            "MCP (by Anthropic) standardizes this: tools expose an MCP server, LLMs connect via MCP client. "
            "Any MCP-compatible client (Claude Desktop, Claude Code) can use any MCP server. "
            "Like USB for AI tools — write once, use anywhere. "
            "MCP supports: tools (functions), resources (data/files), and prompts (reusable prompt templates)."
        ),
        "remember": "MCP = standard protocol for LLM ↔ tools. Like USB for AI. Replaces custom integrations. Anthropic-created.",
    },
    {
        "type": "coding",
        "difficulty": "hard",
        "topic": "Agents — Agentic Loop",
        "question": (
            "Implement a minimal agentic loop using the Anthropic SDK.\n"
            "The agent should:\n"
            "1. Call Claude with a user message and tools\n"
            "2. If Claude calls a tool, execute it and return the result\n"
            "3. Loop until Claude gives a final text response\n\n"
            "Use a single mock tool: add(a, b) that returns a + b"
        ),
        "language": "python",
        "starter_code": (
            "import anthropic\n\n\n"
            "def run_agent(user_message: str) -> str:\n"
            "    client = anthropic.Anthropic()\n"
            "    tools = [\n"
            "        {\n"
            "            'name': 'add',\n"
            "            'description': 'Add two numbers',\n"
            "            'input_schema': {\n"
            "                'type': 'object',\n"
            "                'properties': {\n"
            "                    'a': {'type': 'number'},\n"
            "                    'b': {'type': 'number'}\n"
            "                },\n"
            "                'required': ['a', 'b']\n"
            "            }\n"
            "        }\n"
            "    ]\n"
            "    messages = [{'role': 'user', 'content': user_message}]\n"
            "    # Implement the agentic loop\n"
            "    pass\n"
        ),
        "correct_answer": (
            "import anthropic\n\n\n"
            "def run_agent(user_message: str) -> str:\n"
            "    client = anthropic.Anthropic()\n"
            "    tools = [\n"
            "        {\n"
            "            'name': 'add',\n"
            "            'description': 'Add two numbers',\n"
            "            'input_schema': {\n"
            "                'type': 'object',\n"
            "                'properties': {\n"
            "                    'a': {'type': 'number'},\n"
            "                    'b': {'type': 'number'}\n"
            "                },\n"
            "                'required': ['a', 'b']\n"
            "            }\n"
            "        }\n"
            "    ]\n"
            "    messages = [{'role': 'user', 'content': user_message}]\n\n"
            "    while True:\n"
            "        response = client.messages.create(\n"
            "            model='claude-opus-4-6',\n"
            "            max_tokens=1024,\n"
            "            tools=tools,\n"
            "            messages=messages\n"
            "        )\n\n"
            "        if response.stop_reason == 'end_turn':\n"
            "            # Final text response\n"
            "            return next(b.text for b in response.content if b.type == 'text')\n\n"
            "        if response.stop_reason == 'tool_use':\n"
            "            # Add assistant's response to messages\n"
            "            messages.append({'role': 'assistant', 'content': response.content})\n\n"
            "            # Execute each tool call\n"
            "            tool_results = []\n"
            "            for block in response.content:\n"
            "                if block.type == 'tool_use':\n"
            "                    # Execute the tool\n"
            "                    result = block.input['a'] + block.input['b']  # mock add()\n"
            "                    tool_results.append({\n"
            "                        'type': 'tool_result',\n"
            "                        'tool_use_id': block.id,\n"
            "                        'content': str(result)\n"
            "                    })\n\n"
            "            # Return tool results to the model\n"
            "            messages.append({'role': 'user', 'content': tool_results})\n"
        ),
        "explanation": (
            "The agentic loop: send message → check stop_reason. "
            "If 'end_turn': return the text response. "
            "If 'tool_use': append assistant message, execute each tool_use block, "
            "append tool_results as a user message, loop again. "
            "The tool_use_id links each result back to the specific tool call. "
            "This pattern scales to any number of tools — just dispatch on block.name. "
            "Max iteration guard is important in production to prevent infinite loops."
        ),
        "remember": "Agentic loop: while True → call API → if end_turn return → if tool_use execute + append results → repeat.",
    },
]
