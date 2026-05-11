# An AI agent is a program that perceives its environment, thinks about what to do,
# and takes actions — then repeats that loop. It's like a robot with a brain:
# see something → decide what to do → do it → see what happened → repeat.

# =============================================================================
# THE AGENT LOOP
# =============================================================================
#
#  ┌──────────────────────────────────────────────────────────┐
#  │                    AGENT LOOP                            │
#  │                                                          │
#  │   1. PERCEIVE  → receive input (user message, sensor,    │
#  │                  environment state, tool result...)      │
#  │                                                          │
#  │   2. THINK     → decide what to do next                  │
#  │                  (rule-based, LLM, or learned policy)    │
#  │                                                          │
#  │   3. ACT       → take an action                          │
#  │                  (respond, call a tool, move, write...)  │
#  │                                                          │
#  │   4. OBSERVE   → see what happened as a result           │
#  │                                                          │
#  │   → Go back to step 1                                    │
#  └──────────────────────────────────────────────────────────┘
#
# Real-world analogies:
#   - A thermostat: perceives temperature → decides to heat/cool → acts
#   - A chess engine: perceives board → thinks about moves → makes move
#   - GPT with tools: reads your question → decides which tool → uses it → answers

# =============================================================================
# TYPES OF AGENTS
# =============================================================================
#
# 1. Reflex agents:      Act purely on current input (no memory of the past)
#                        Like: a thermostat, a spam filter
#
# 2. Model-based agents: Keep a model of the world (internal state)
#                        Like: a chess AI that tracks the board
#
# 3. Goal-based agents:  Have a goal and plan how to reach it
#                        Like: a GPS navigation system
#
# 4. Learning agents:    Improve over time through experience
#                        Like: AlphaGo, recommendation systems
#
# 5. LLM agents:         Use a large language model as the "brain"
#                        Like: Claude, ChatGPT with tools

# =============================================================================
# IMPLEMENTATION: Simple Rule-Based Agent
# =============================================================================

class SimpleAgent:
    """
    A basic rule-based agent that responds to user inputs.
    It has no memory — each response is based only on the current input.
    This is a "reflex agent" — the simplest kind.
    """

    def __init__(self, name="Agent"):
        self.name = name
        self.action_count = 0   # how many actions taken so far

    def perceive(self, user_input):
        """
        Step 1: PERCEIVE — receive and process the input.
        In a real agent, this might also include sensor data, API results, etc.
        """
        # Clean up the input
        return user_input.strip().lower()

    def think(self, perception):
        """
        Step 2: THINK — decide what action to take.
        This is where the agent's "intelligence" lives.
        In a rule-based agent, it's just if/else logic.
        In an LLM agent, this would be an API call to the language model.
        """
        # Route the input to the appropriate action
        if any(word in perception for word in ["hello", "hi", "hey"]):
            return "greet"
        elif any(word in perception for word in ["time", "what time", "clock"]):
            return "tell_time"
        elif any(word in perception for word in ["weather", "temperature", "forecast"]):
            return "weather"
        elif any(word in perception for word in ["help", "what can you do", "commands"]):
            return "help"
        elif any(word in perception for word in ["bye", "exit", "quit", "goodbye"]):
            return "farewell"
        elif "?" in perception:
            return "unknown_question"
        else:
            return "unknown"

    def act(self, action, original_input):
        """
        Step 3: ACT — execute the chosen action and produce a response.
        The agent "does something" based on its decision.
        """
        import datetime

        self.action_count += 1   # track how many actions we've taken

        responses = {
            "greet":           f"Hello! I'm {self.name}. How can I help you?",
            "tell_time":       f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}.",
            "weather":         "I don't have live weather data, but I can tell you it's Python weather — great for coding!",
            "help":            "I can respond to: greetings, time requests, weather, or general questions.",
            "farewell":        f"Goodbye! {self.name} signing off.",
            "unknown_question": f"That's a great question! I'm a simple agent and can't answer '{original_input}' yet.",
            "unknown":         f"I received your message but I'm not sure how to respond to: '{original_input}'",
        }
        return responses.get(action, "I'm not sure what to do.")

    def observe(self, action, response):
        """
        Step 4: OBSERVE — note what happened after acting.
        A learning agent would update its knowledge here.
        We just log it.
        """
        print(f"  [Agent observed: took action='{action}', action #{self.action_count}]")

    def run_once(self, user_input):
        """
        Execute one full perception → think → act → observe cycle.
        """
        print(f"\n{'─'*50}")
        print(f"User:  {user_input}")

        perception = self.perceive(user_input)     # Step 1
        action = self.think(perception)             # Step 2
        response = self.act(action, user_input)     # Step 3
        self.observe(action, response)              # Step 4

        print(f"Agent: {response}")
        return response

class StatefulAgent(SimpleAgent):
    """
    An upgraded agent that keeps track of conversation state.
    It knows if it's seen the user before.
    """

    def __init__(self, name="StatefulAgent"):
        super().__init__(name)
        self.has_greeted = False
        self.interaction_history = []

    def act(self, action, original_input):
        # Add to history before acting
        self.interaction_history.append(original_input)

        if action == "greet" and self.has_greeted:
            self.has_greeted = True
            return "We already said hello! What else can I help with?"
        elif action == "greet":
            self.has_greeted = True

        return super().act(action, original_input)

if __name__ == "__main__":
    print("=" * 50)
    print("AGENT BASICS — Perception → Thinking → Action")
    print("=" * 50)

    # --- Demo 1: Simple reflex agent ---
    print("\n--- Simple Reflex Agent ---")
    agent = SimpleAgent(name="Roxy")

    test_inputs = [
        "Hello there!",
        "What time is it?",
        "How's the weather today?",
        "What can you do?",
        "What is the meaning of life?",
        "Goodbye!",
    ]

    for user_input in test_inputs:
        agent.run_once(user_input)

    print(f"\n[Agent took {agent.action_count} actions total]")

    # --- Demo 2: Stateful agent ---
    print("\n\n--- Stateful Agent (remembers greeting) ---")
    stateful = StatefulAgent(name="Max")
    stateful.run_once("Hi!")
    stateful.run_once("Hey again!")
    stateful.run_once("What time is it?")
    print(f"\n[Interaction history: {stateful.interaction_history}]")
