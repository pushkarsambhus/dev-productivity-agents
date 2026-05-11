# Multi-agent systems have multiple AI agents working together — each with its own role.
# Think of it like a team: a researcher, a writer, and an editor all working on the same document.
# Agents can communicate, delegate tasks, and check each other's work.

# =============================================================================
# WHY MULTI-AGENT?
# =============================================================================
#
# Single agent limitations:
#   - One agent handles everything → can get confused on complex tasks
#   - Hard to specialize for very different sub-tasks
#   - A single point of failure
#
# Multi-agent benefits:
#   - Each agent specializes in one thing (research, writing, coding, reviewing)
#   - Agents can verify each other's work (reduces errors)
#   - Tasks can run in parallel
#   - Easier to scale and maintain
#
# Real-world examples:
#   - AutoGen (Microsoft): multiple agents with different roles collaborate
#   - CrewAI: "crew" of agents with defined roles and tasks
#   - Claude with sub-agents: a manager agent delegates to specialist agents

# =============================================================================
# MESSAGE PASSING: how agents communicate
# =============================================================================
# Agents communicate by passing messages. This is like email or Slack:
# one agent sends a structured message, another receives and responds.

import datetime
import random

class Message:
    """
    A message sent from one agent to another.
    Mirrors how real multi-agent frameworks pass information.
    """
    def __init__(self, sender, recipient, content, message_type="text", metadata=None):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.message_type = message_type   # "text", "task", "result", "critique"
        self.metadata = metadata or {}
        self.timestamp = datetime.datetime.now()
        self.id = f"msg_{random.randint(1000,9999)}"

    def __repr__(self):
        return f"Message({self.id}: {self.sender}→{self.recipient}: '{self.content[:40]}...')"

# =============================================================================
# BASE AGENT CLASS
# =============================================================================

class BaseAgent:
    """Base class for all agents in our multi-agent system."""

    def __init__(self, name, role, description):
        self.name = name
        self.role = role
        self.description = description
        self.inbox = []         # messages waiting to be processed
        self.message_log = []   # all messages sent and received

    def send(self, recipient_agent, content, message_type="text", metadata=None):
        """Send a message to another agent."""
        msg = Message(self.name, recipient_agent.name, content, message_type, metadata)
        recipient_agent.receive(msg)
        self.message_log.append(("sent", msg))
        print(f"\n  📤 {self.name} → {recipient_agent.name}: {content[:80]}")
        return msg

    def receive(self, message):
        """Receive a message and add it to inbox."""
        self.inbox.append(message)
        self.message_log.append(("received", message))

    def process(self):
        """Process all messages in inbox. Override in subclasses."""
        results = []
        while self.inbox:
            msg = self.inbox.pop(0)
            result = self.handle_message(msg)
            if result:
                results.append(result)
        return results

    def handle_message(self, message):
        """Handle a single message. Override in subclasses."""
        raise NotImplementedError

# =============================================================================
# SPECIALIST AGENTS
# =============================================================================

class ResearchAgent(BaseAgent):
    """Searches for information on a given topic."""

    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            role="Researcher",
            description="Finds information and gathers facts on any topic"
        )

    def handle_message(self, message):
        topic = message.content
        # In a real agent: call a search API
        # Here: return mock research
        mock_research = {
            "python":      "Python: created 1991 by Guido van Rossum. Used for web dev, data science, AI. Syntax is clean and readable.",
            "machine learning": "ML: algorithms that learn from data. Types: supervised, unsupervised, reinforcement learning.",
            "ai agents":   "AI Agents: autonomous programs that perceive, decide, and act. Can use tools, plan, and collaborate.",
        }

        result = None
        for key in mock_research:
            if key in topic.lower():
                result = mock_research[key]
                break

        if not result:
            result = f"Research on '{topic}': [Found general information — topic is broad, recommend narrowing focus]"

        print(f"  🔍 {self.name} researched: '{topic}'")
        return result

class WriterAgent(BaseAgent):
    """Writes clear, engaging content based on research."""

    def __init__(self):
        super().__init__(
            name="WriterAgent",
            role="Writer",
            description="Transforms research into well-written content"
        )

    def handle_message(self, message):
        research_text = message.content

        # In a real agent: pass research to an LLM with writing instructions
        word_count = len(research_text.split())
        draft = (
            f"[DRAFT ARTICLE]\n"
            f"Based on the research provided, here is a structured overview:\n\n"
            f"Introduction: The topic covers several important areas.\n"
            f"Key Points: {research_text}\n"
            f"Conclusion: This subject has significant implications for modern applications.\n\n"
            f"[Draft complete — {word_count} source words processed]"
        )
        print(f"  ✍️  {self.name} wrote a draft from research.")
        return draft

class ReviewerAgent(BaseAgent):
    """Critiques and improves content from the writer."""

    def __init__(self):
        super().__init__(
            name="ReviewerAgent",
            role="Editor/Reviewer",
            description="Reviews content for quality, accuracy, and clarity"
        )
        self.approval_threshold = 0.7   # 70% quality required to approve

    def handle_message(self, message):
        content = message.content

        # Simulate quality scoring
        score = min(1.0, 0.5 + len(content) / 1000)   # longer = higher score (simplified)
        approved = score >= self.approval_threshold

        feedback = {
            "score": round(score, 2),
            "approved": approved,
            "suggestions": [
                "Add more specific examples",
                "Consider breaking into shorter paragraphs",
                "Strong opening — keep this style throughout",
            ][:2],
            "verdict": "APPROVED ✓" if approved else "NEEDS REVISION ✗"
        }

        result = (
            f"[REVIEW FEEDBACK]\n"
            f"Score: {feedback['score']}/1.0\n"
            f"Verdict: {feedback['verdict']}\n"
            f"Suggestions:\n"
        )
        for s in feedback["suggestions"]:
            result += f"  • {s}\n"

        print(f"  🔎 {self.name} reviewed the draft (score: {feedback['score']})")
        return result

class OrchestratorAgent(BaseAgent):
    """
    Coordinates the other agents — acts as the 'manager'.
    Receives a goal, delegates to specialists, and assembles the final result.
    This is the 'supervisor' pattern in multi-agent systems.
    """

    def __init__(self, researcher, writer, reviewer):
        super().__init__(
            name="OrchestratorAgent",
            role="Manager/Orchestrator",
            description="Coordinates other agents to achieve a complex goal"
        )
        self.researcher = researcher
        self.writer = writer
        self.reviewer = reviewer

    def handle_message(self, message):
        pass   # orchestrator handles goals directly via run_workflow

    def run_workflow(self, goal):
        """Execute a full research → write → review workflow."""
        print(f"\n{'='*60}")
        print(f"🎯 ORCHESTRATOR: Starting workflow for goal:")
        print(f"   '{goal}'")
        print(f"{'='*60}")

        # Step 1: Ask researcher to find info
        print("\n[Step 1/3] Delegating research...")
        self.send(self.researcher, goal, message_type="task")
        research_results = self.researcher.process()
        research = research_results[0] if research_results else "No research found."

        # Step 2: Send research to writer
        print("\n[Step 2/3] Delegating writing...")
        self.send(self.writer, research, message_type="task")
        writing_results = self.writer.process()
        draft = writing_results[0] if writing_results else "No draft produced."

        # Step 3: Send draft to reviewer
        print("\n[Step 3/3] Delegating review...")
        self.send(self.reviewer, draft, message_type="task")
        review_results = self.reviewer.process()
        review = review_results[0] if review_results else "No review produced."

        # Assemble final output
        print(f"\n{'='*60}")
        print("✅ WORKFLOW COMPLETE")
        print(f"{'='*60}")
        return {"research": research, "draft": draft, "review": review}

# =============================================================================
# PEER-TO-PEER: Two agents having a conversation
# =============================================================================

class ConversationalAgent(BaseAgent):
    """An agent that engages in back-and-forth dialogue."""

    RESPONSES = {
        "question": [
            "That's a great question! Let me think... I believe the answer relates to our core task.",
            "Interesting! From my perspective, we should focus on gathering more data.",
            "Good point. I suggest we also consider the edge cases here.",
        ],
        "idea": [
            "I like that idea! Let's build on it.",
            "Hmm, that's creative. What are the potential risks?",
            "Agreed! That aligns well with our goal.",
        ],
        "result": [
            "Thanks for sharing that result. I'll incorporate it into my analysis.",
            "Excellent! That confirms my hypothesis.",
            "Noted. Should we now move on to the next step?",
        ],
        "default": [
            "Understood. Let me process that information.",
            "Interesting perspective. Let's continue.",
            "Got it. What should we tackle next?",
        ]
    }

    def handle_message(self, message):
        content_lower = message.content.lower()
        if "?" in message.content:
            responses = self.RESPONSES["question"]
        elif any(w in content_lower for w in ["idea", "suggest", "propose"]):
            responses = self.RESPONSES["idea"]
        elif any(w in content_lower for w in ["result", "found", "completed"]):
            responses = self.RESPONSES["result"]
        else:
            responses = self.RESPONSES["default"]

        return random.choice(responses)

if __name__ == "__main__":
    print("=" * 60)
    print("MULTI-AGENT SYSTEMS")
    print("=" * 60)

    # --- Demo 1: Two agents having a conversation ---
    print("\n--- Demo 1: Two agents chatting ---")
    alice = ConversationalAgent("Alice", "Analyst", "Analyzes data")
    bob   = ConversationalAgent("Bob", "Strategist", "Plans strategy")

    messages = [
        (alice, bob, "I found some interesting patterns in the data. What do you think we should do?"),
        (bob, alice, "That's a great question! I suggest we focus on the highest-value segment first."),
        (alice, bob, "I like that idea! I'll run a deeper analysis on that segment."),
        (bob, alice, "The results look promising. Should we present this to the team?"),
    ]

    for sender, receiver, text in messages:
        sender.send(receiver, text)
        responses = receiver.process()
        if responses:
            print(f"  💬 {receiver.name} thinks: {responses[0]}")

    # --- Demo 2: Orchestrated multi-agent workflow ---
    print("\n\n--- Demo 2: Orchestrated research workflow ---")
    researcher  = ResearchAgent()
    writer      = WriterAgent()
    reviewer    = ReviewerAgent()
    orchestrator = OrchestratorAgent(researcher, writer, reviewer)

    result = orchestrator.run_workflow("AI agents and multi-agent systems")

    print("\n--- Final Research ---")
    print(result["research"])
    print("\n--- Final Review ---")
    print(result["review"])

    print("\n\nKey takeaway:")
    print("  Multi-agent systems allow specialization, parallelism, and")
    print("  self-checking — making them more robust than single agents.")
