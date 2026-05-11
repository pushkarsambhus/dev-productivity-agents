# Memory is what makes an AI agent feel like it "knows you" across a conversation.
# Short-term memory: remembers what happened in the current conversation.
# Long-term memory: remembers information across multiple conversations (saved to disk).

# =============================================================================
# TYPES OF MEMORY IN AI AGENTS
# =============================================================================
#
# 1. SHORT-TERM (In-Context) Memory
#    → The conversation history kept in the current session
#    → Passed to the LLM as part of the prompt each turn
#    → Limited by the model's context window
#    → Forgotten when the session ends
#    → Example: "Earlier you said you liked Python..."
#
# 2. LONG-TERM (External) Memory
#    → Facts stored outside the model (database, file, vector store)
#    → Persists between sessions
#    → Must be explicitly retrieved and injected into the prompt
#    → Example: "Welcome back, Alice! Last time you were working on a Flask app."
#
# 3. EPISODIC Memory
#    → Records of specific past events/interactions
#    → "Remember last Tuesday when you asked about sorting algorithms?"
#
# 4. SEMANTIC Memory
#    → Factual knowledge about the user or world
#    → "User prefers Python over JavaScript. User is a beginner."

import json
import os
import datetime

# =============================================================================
# SHORT-TERM MEMORY: Conversation History Buffer
# =============================================================================

class ConversationMemory:
    """
    Stores the current conversation as a list of message turns.
    This mirrors exactly how LLM APIs (Claude, GPT) handle conversation history.
    """

    def __init__(self, max_turns=10):
        self.messages = []         # list of {"role": "user"/"assistant", "content": "..."}
        self.max_turns = max_turns  # limit how many turns we keep (to manage context length)

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
        self._trim()

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})
        self._trim()

    def _trim(self):
        """Keep only the most recent max_turns messages to stay within context limits."""
        if len(self.messages) > self.max_turns * 2:
            # Always keep system context; drop oldest turns
            self.messages = self.messages[-(self.max_turns * 2):]

    def get_history(self):
        return self.messages

    def format_for_display(self):
        """Format conversation history as readable text."""
        lines = []
        for msg in self.messages:
            role = "You" if msg["role"] == "user" else "Agent"
            lines.append(f"  {role}: {msg['content']}")
        return "\n".join(lines)

    def clear(self):
        self.messages = []

# =============================================================================
# LONG-TERM MEMORY: Persistent Key-Value Store (saved to file)
# =============================================================================

class LongTermMemory:
    """
    Stores facts about the user/world that persist between sessions.
    Uses a JSON file as a simple database.

    In production agents, this would typically be:
      - A vector database (Pinecone, Weaviate, Chroma) for semantic search
      - A SQL/NoSQL database for structured facts
      - Redis for fast key-value lookups
    """

    def __init__(self, filepath="/tmp/agent_long_term_memory.json"):
        self.filepath = filepath
        self.data = self._load()   # load existing memory from file

    def _load(self):
        """Load memory from disk if it exists."""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return {}   # start fresh if no file exists

    def _save(self):
        """Persist memory to disk."""
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)

    def remember(self, key, value):
        """Store a fact. Overwrites if key already exists."""
        self.data[key] = {
            "value": value,
            "stored_at": datetime.datetime.now().isoformat()
        }
        self._save()
        print(f"  [Memory saved: {key} = {value}]")

    def recall(self, key):
        """Retrieve a fact by key. Returns None if not found."""
        entry = self.data.get(key)
        if entry:
            return entry["value"]
        return None

    def recall_all(self):
        """Return all stored facts."""
        return {k: v["value"] for k, v in self.data.items()}

    def forget(self, key):
        """Delete a stored fact."""
        if key in self.data:
            del self.data[key]
            self._save()

    def clear_all(self):
        self.data = {}
        self._save()

# =============================================================================
# MEMORY-EQUIPPED AGENT
# =============================================================================

class MemoryAgent:
    """
    An agent with both short-term (conversation) and long-term (persistent) memory.

    Short-term: tracks the current conversation
    Long-term:  remembers user preferences and facts across sessions
    """

    def __init__(self, name="MemoryBot"):
        self.name = name
        self.short_term = ConversationMemory(max_turns=5)
        self.long_term = LongTermMemory()
        self.turn = 0

    def _build_context(self):
        """
        Build the 'context' that a real LLM would receive.
        This combines long-term memory facts + recent conversation history.
        """
        context_parts = []

        # Add relevant long-term memories
        memories = self.long_term.recall_all()
        if memories:
            memory_text = ", ".join(f"{k}={v}" for k, v in list(memories.items())[:3])
            context_parts.append(f"[Known about user: {memory_text}]")

        # Add recent conversation
        history = self.short_term.format_for_display()
        if history:
            context_parts.append(f"[Recent conversation:\n{history}]")

        return "\n".join(context_parts)

    def respond(self, user_input):
        """Process user input and generate a response using memory."""
        self.turn += 1
        text = user_input.lower()

        # --- Detect memory-related requests ---

        # User is telling us their name
        if "my name is" in text:
            name = user_input.lower().split("my name is", 1)[-1].strip().rstrip(".,!").title()
            self.long_term.remember("user_name", name)
            response = f"Nice to meet you, {name}! I'll remember that."

        # User is asking if we remember their name
        elif "what's my name" in text or "do you know my name" in text:
            stored_name = self.long_term.recall("user_name")
            if stored_name:
                response = f"Of course! Your name is {stored_name}."
            else:
                response = "I don't know your name yet. What is it?"

        # User is sharing a preference
        elif "i like" in text or "i love" in text or "i prefer" in text:
            for trigger in ["i like", "i love", "i prefer"]:
                if trigger in text:
                    thing = text.split(trigger, 1)[-1].strip().rstrip(".,!")
                    self.long_term.remember(f"likes_{self.turn}", thing)
                    response = f"Good to know! I'll remember that you like {thing}."
                    break

        # User is asking what we know about them
        elif "what do you know about me" in text or "what do you remember" in text:
            memories = self.long_term.recall_all()
            if memories:
                facts = "\n".join(f"  - {k}: {v}" for k, v in memories.items())
                response = f"Here's what I remember about you:\n{facts}"
            else:
                response = "I don't have any memories about you yet. Tell me something!"

        # User wants to clear memory
        elif "forget everything" in text or "clear memory" in text:
            self.long_term.clear_all()
            self.short_term.clear()
            response = "Done! I've cleared all my memories."

        # Generic response — uses conversation history for context
        else:
            context = self._build_context()
            # In a real agent, we'd pass context to an LLM here
            response = f"I hear you. [In a real agent, I'd pass this context to an LLM:\n{context or '(no context yet)'}]"

        # Store this turn in short-term memory
        self.short_term.add_user_message(user_input)
        self.short_term.add_assistant_message(response)

        return response

if __name__ == "__main__":
    print("=" * 55)
    print("MEMORY AGENT")
    print("=" * 55)

    agent = MemoryAgent("MemBot")

    conversations = [
        "Hello!",
        "My name is Alice.",
        "I like Python programming.",
        "I love hiking on weekends.",
        "What's my name?",
        "What do you know about me?",
    ]

    print("\n--- Conversation with memory ---")
    for message in conversations:
        print(f"\nUser:  {message}")
        response = agent.respond(message)
        print(f"Agent: {response}")

    print("\n\n--- Short-term memory (conversation history) ---")
    print(agent.short_term.format_for_display())

    print("\n--- Long-term memory (persisted facts) ---")
    for key, value in agent.long_term.recall_all().items():
        print(f"  {key}: {value}")

    # Demonstrate persistence: create a NEW agent — it loads the same long-term memory
    print("\n\n--- New agent session (same long-term memory) ---")
    new_agent = MemoryAgent("MemBot2")
    print("User:  What's my name?")
    print("Agent:", new_agent.respond("What's my name?"))

    # Clean up the test file
    agent.long_term.clear_all()
    print("\n[Long-term memory cleared for cleanup]")
