# A planning agent breaks a big goal into a sequence of smaller steps, executes them,
# and uses the results to decide what to do next.
# It follows a Plan → Act → Observe loop (sometimes called ReAct: Reason + Act).

# =============================================================================
# THE PLAN → ACT → OBSERVE LOOP
# =============================================================================
#
#  ┌────────────────────────────────────────────────────────────┐
#  │                 Planning Agent Loop                        │
#  │                                                            │
#  │   GOAL received: "Research Python and write a summary"     │
#  │                                                            │
#  │   ┌─────────────────────────────────────────────────┐      │
#  │   │  PLAN: break goal into steps                    │      │
#  │   │    1. Search for Python info                    │      │
#  │   │    2. Extract key facts                         │      │
#  │   │    3. Write summary                             │      │
#  │   │    4. Review and finalize                       │      │
#  │   └────────────────┬────────────────────────────────┘      │
#  │                    ↓                                        │
#  │   ┌─────────────────────────────────────────────────┐      │
#  │   │  ACT: execute step 1 (call search tool)         │      │
#  │   └────────────────┬────────────────────────────────┘      │
#  │                    ↓                                        │
#  │   ┌─────────────────────────────────────────────────┐      │
#  │   │  OBSERVE: "Python is a high-level language..."  │      │
#  │   └────────────────┬────────────────────────────────┘      │
#  │                    ↓                                        │
#  │         Move to step 2... repeat until done.               │
#  └────────────────────────────────────────────────────────────┘

import time
import datetime

# =============================================================================
# PLAN REPRESENTATION
# =============================================================================

class Step:
    """A single step in a plan."""

    def __init__(self, step_id, description, tool=None, args=None, depends_on=None):
        self.step_id = step_id
        self.description = description   # human-readable description
        self.tool = tool                 # which tool to call (None = no tool)
        self.args = args or {}           # arguments for the tool
        self.depends_on = depends_on     # step_id this step must wait for
        self.status = "pending"          # pending → running → done / failed
        self.result = None               # what the step produced
        self.started_at = None
        self.finished_at = None

    def __repr__(self):
        return f"Step({self.step_id}: {self.description} [{self.status}])"

class Plan:
    """A sequence of steps to achieve a goal."""

    def __init__(self, goal, steps):
        self.goal = goal
        self.steps = steps
        self.created_at = datetime.datetime.now()

    def get_next_step(self):
        """Return the next step that's ready to run (all dependencies satisfied)."""
        done_ids = {s.step_id for s in self.steps if s.status == "done"}
        for step in self.steps:
            if step.status == "pending":
                # Check if dependency is satisfied
                if step.depends_on is None or step.depends_on in done_ids:
                    return step
        return None   # all done or blocked

    def all_done(self):
        return all(s.status in ("done", "failed") for s in self.steps)

    def summary(self):
        total = len(self.steps)
        done = sum(1 for s in self.steps if s.status == "done")
        failed = sum(1 for s in self.steps if s.status == "failed")
        return f"{done}/{total} steps done, {failed} failed"

# =============================================================================
# MOCK TOOLS (same idea as tool_use_agent.py)
# =============================================================================

def mock_search(query):
    results = {
        "python programming language": "Python is a high-level, interpreted language created by Guido van Rossum in 1991. Known for readability and simplicity.",
        "python use cases":            "Python is used for web dev (Django, Flask), data science, AI/ML, automation, and scripting.",
        "python popularity":           "Python is consistently ranked #1 or #2 in most language popularity indices (TIOBE, Stack Overflow).",
    }
    for key, val in results.items():
        if any(word in query.lower() for word in key.split()):
            return val
    return f"Search result for '{query}': [mock result — no real data]"

def mock_extract_facts(text):
    """Pretend to extract bullet points from a body of text."""
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 10]
    facts = [f"• {s}." for s in sentences[:3]]
    return "\n".join(facts) if facts else "• No facts extracted."

def mock_write_summary(facts):
    """Pretend to write a final summary paragraph."""
    return (
        "SUMMARY: Python is a versatile, beginner-friendly programming language "
        "widely used in web development, data science, and AI. "
        f"Key facts include: {facts[:80]}..."
    )

def mock_review(text):
    """Pretend to review and approve content."""
    word_count = len(text.split())
    return f"Review complete. Content looks good! Word count: {word_count}. Approved ✓"

TOOLS = {
    "search":        mock_search,
    "extract_facts": mock_extract_facts,
    "write_summary": mock_write_summary,
    "review":        mock_review,
}

# =============================================================================
# THE PLANNING AGENT
# =============================================================================

class PlanningAgent:
    """
    An agent that creates a plan for a goal, then executes it step by step.
    After each step, it observes the result before moving on.

    This mirrors how LLM agents like AutoGPT and LangChain agents work:
    they plan first, then execute, using tool results to inform next actions.
    """

    def __init__(self, name="Planner"):
        self.name = name
        self.tools = TOOLS
        self.plans_completed = 0

    def plan(self, goal):
        """
        Create a plan for the given goal.
        In a real LLM agent, this would be generated by the language model.
        Here we use predefined plan templates.
        """
        print(f"\n[PLANNING] Goal: '{goal}'")

        if "research" in goal.lower() and "python" in goal.lower():
            steps = [
                Step(1, "Search for general Python info",  tool="search",        args={"query": "python programming language"}),
                Step(2, "Search for Python use cases",     tool="search",        args={"query": "python use cases"}),
                Step(3, "Extract key facts from results",  tool="extract_facts", args={}, depends_on=2),
                Step(4, "Write a summary",                 tool="write_summary", args={}, depends_on=3),
                Step(5, "Review the summary",              tool="review",        args={}, depends_on=4),
            ]
        else:
            # Generic fallback plan
            steps = [
                Step(1, f"Search for information about: {goal}", tool="search", args={"query": goal}),
                Step(2, "Extract key facts", tool="extract_facts", args={}, depends_on=1),
                Step(3, "Write a summary",   tool="write_summary", args={}, depends_on=2),
            ]

        plan = Plan(goal=goal, steps=steps)
        print(f"[PLAN CREATED] {len(steps)} steps:")
        for step in steps:
            dep = f" (after step {step.depends_on})" if step.depends_on else ""
            print(f"  Step {step.step_id}: {step.description}{dep}")

        return plan

    def execute_step(self, step, previous_result=None):
        """
        ACT: execute a single step using the appropriate tool.
        """
        step.status = "running"
        step.started_at = datetime.datetime.now()

        print(f"\n  [ACT] Step {step.step_id}: {step.description}")

        try:
            if step.tool is None:
                # No tool needed — just a logical step
                result = f"Completed: {step.description}"
            else:
                tool_fn = self.tools[step.tool]
                # For steps that need the PREVIOUS result as input
                if step.tool in ("extract_facts", "write_summary", "review"):
                    result = tool_fn(previous_result or "")
                else:
                    result = tool_fn(**step.args)

            step.status = "done"
            step.result = result
        except Exception as e:
            step.status = "failed"
            step.result = f"ERROR: {e}"

        step.finished_at = datetime.datetime.now()
        return step.result

    def observe(self, step):
        """
        OBSERVE: review the result of the last action.
        A learning agent could use this to adjust future steps.
        """
        print(f"  [OBSERVE] Result: {str(step.result)[:120]}...")
        print(f"  [STATUS] Step {step.step_id}: {step.status.upper()}")

    def run(self, goal):
        """
        Full planning agent loop:
        Plan the goal → Execute step by step → Observe each result
        """
        print("\n" + "=" * 60)
        print(f"PLANNING AGENT: '{goal}'")
        print("=" * 60)

        plan = self.plan(goal)
        last_result = None

        print("\n[EXECUTING PLAN...]")
        while not plan.all_done():
            step = plan.get_next_step()
            if step is None:
                print("[BLOCKED] No steps are ready to run.")
                break

            result = self.execute_step(step, previous_result=last_result)
            self.observe(step)
            last_result = result

        self.plans_completed += 1
        print(f"\n[PLAN COMPLETE] {plan.summary()}")
        print(f"[FINAL OUTPUT]\n{last_result}")
        return last_result

if __name__ == "__main__":
    agent = PlanningAgent()

    # Run a research and summarize task
    agent.run("Research Python programming language and write a summary")

    print("\n\n" + "=" * 60)
    print("AGENT STATS")
    print("=" * 60)
    print(f"Plans completed: {agent.plans_completed}")
