# Prompt engineering is the art of crafting instructions for AI models to get the best results.
# Just like asking a question clearly gets a better answer from a person,
# well-structured prompts get dramatically better responses from LLMs.

# =============================================================================
# WHAT IS PROMPT ENGINEERING?
# =============================================================================
#
# When you send text to an LLM (like Claude or GPT), that text is called a "prompt".
# The quality of your prompt directly determines the quality of the response.
#
# Prompt engineering = learning HOW to write effective prompts.
# It's part skill, part experimentation, and part knowing how LLMs work.

# =============================================================================
# KEY PRINCIPLES
# =============================================================================
#
# 1. BE SPECIFIC — vague prompts give vague answers
# 2. GIVE CONTEXT — tell the model who/what/why
# 3. SPECIFY FORMAT — tell it how to structure the response
# 4. USE EXAMPLES — show it what good output looks like (few-shot)
# 5. SET A ROLE — "You are an expert in X..."
# 6. BREAK IT DOWN — complex tasks → step-by-step instructions

# =============================================================================
# EXAMPLES: BAD vs. GOOD PROMPTS
# =============================================================================

bad_prompts = [
    {
        "task": "Code help",
        "bad":  "Fix my code.",
        "why_bad": "No code provided, no context, no explanation of the problem.",
        "good": (
            "Here is my Python function that calculates the average of a list:\n"
            "\n"
            "def average(numbers):\n"
            "    return sum(numbers) / len(numbers)\n"
            "\n"
            "It crashes when the list is empty with a ZeroDivisionError. "
            "Please fix it and add a docstring explaining what it does."
        ),
    },
    {
        "task": "Writing",
        "bad":  "Write something about AI.",
        "why_bad": "Too vague. What audience? What format? How long? What angle?",
        "good": (
            "Write a 3-paragraph blog post introduction for non-technical readers "
            "explaining what AI is and why it matters in everyday life. "
            "Use simple analogies and an engaging, friendly tone."
        ),
    },
    {
        "task": "Analysis",
        "bad":  "Tell me about this data.",
        "why_bad": "No data provided, no question, no desired output format.",
        "good": (
            "Here is monthly sales data for 2024:\n"
            "Jan: $12,000, Feb: $15,000, Mar: $11,000, Apr: $18,000\n"
            "\n"
            "Please: (1) identify the highest and lowest months, "
            "(2) calculate the average, and (3) note any obvious trends. "
            "Format the response as a bulleted list."
        ),
    },
    {
        "task": "Summarization",
        "bad":  "Summarize this.",
        "why_bad": "No text, no length guidance, no audience specified.",
        "good": (
            "Summarize the following article in 3 bullet points, "
            "each 1 sentence long. Target audience: busy executives "
            "who need the key takeaways quickly.\n\n[article text here]"
        ),
    },
]

# =============================================================================
# FEW-SHOT PROMPTING
# =============================================================================
#
# Few-shot prompting = giving the model 2-5 examples of input → output pairs
# before asking your real question. This "shows" the model exactly what you want.
#
# Why it works: LLMs are very good at pattern matching. Seeing examples
# helps them understand the format, tone, and style you're looking for.

few_shot_example = """
TASK: Classify customer reviews as POSITIVE, NEGATIVE, or NEUTRAL.

Example 1:
Review: "This product is amazing! Best purchase I've made all year."
Sentiment: POSITIVE

Example 2:
Review: "It arrived broken and customer service was unhelpful."
Sentiment: NEGATIVE

Example 3:
Review: "The package arrived on time. It's okay I guess."
Sentiment: NEUTRAL

Now classify this review:
Review: "Works exactly as described. Shipping was fast."
Sentiment: ???
"""

# The model will see the pattern and respond: POSITIVE

# =============================================================================
# CHAIN-OF-THOUGHT PROMPTING
# =============================================================================
#
# For complex reasoning tasks, ask the model to "think step by step".
# This dramatically improves accuracy on math, logic, and multi-step problems.
#
# Without CoT: "What is 15% of 240?"
#   → Model might guess: "36"  (wrong)
#
# With CoT:    "What is 15% of 240? Let's think step by step."
#   → "15% means 15/100 = 0.15
#      0.15 × 240 = ?
#      0.15 × 200 = 30
#      0.15 × 40 = 6
#      Total: 30 + 6 = 36"  ✓

# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

def build_prompt(task, context, format_instructions, examples=None):
    """
    A reusable function for building well-structured prompts.
    This pattern is commonly used in production AI applications.
    """
    prompt = f"TASK: {task}\n\n"

    if context:
        prompt += f"CONTEXT: {context}\n\n"

    if examples:
        prompt += "EXAMPLES:\n"
        for i, (inp, out) in enumerate(examples, 1):
            prompt += f"  Example {i}:\n"
            prompt += f"    Input:  {inp}\n"
            prompt += f"    Output: {out}\n"
        prompt += "\n"

    prompt += f"FORMAT: {format_instructions}\n\n"
    prompt += "Now complete the task above."
    return prompt

if __name__ == "__main__":
    print("=" * 65)
    print("PROMPT ENGINEERING — Key Concepts & Examples")
    print("=" * 65)

    print("\n=== BAD vs. GOOD PROMPTS ===")
    for ex in bad_prompts:
        print(f"\n  Task: {ex['task']}")
        print(f"  ✗ Bad:  \"{ex['bad']}\"")
        print(f"    Why:  {ex['why_bad']}")
        print(f"  ✓ Good: \"{ex['good'][:100]}...\"" if len(ex['good']) > 100 else f"  ✓ Good: \"{ex['good']}\"")

    print("\n" + "=" * 65)
    print("FEW-SHOT PROMPTING EXAMPLE")
    print("=" * 65)
    print(few_shot_example)
    print("→ Expected model output: POSITIVE")
    print("→ The model learned from the 3 examples, not from explicit rules!")

    print("\n" + "=" * 65)
    print("PROMPT TEMPLATE DEMO")
    print("=" * 65)
    prompt = build_prompt(
        task="Extract key action items from a meeting transcript",
        context="You are a professional assistant helping a project manager",
        format_instructions="Return a numbered list. Each item: [Owner] - [Action] - [Deadline]",
        examples=[
            ("Alice said she'll send the report by Friday.",
             "1. [Alice] - Send report - Friday"),
            ("Bob needs to schedule the client call for next week.",
             "2. [Bob] - Schedule client call - Next week"),
        ]
    )
    print(prompt)

    print("\n" + "=" * 65)
    print("QUICK REFERENCE: Prompt Engineering Cheatsheet")
    print("=" * 65)
    tips = [
        ("Be specific",        "Bad: 'Explain AI'  Good: 'Explain AI to a 10-year-old in 2 sentences'"),
        ("Give context",       "Add: who you are, what you're building, who the audience is"),
        ("Set a role",         "'You are a senior Python developer with 10 years of experience...'"),
        ("Specify format",     "'Respond in JSON', 'Use bullet points', 'Max 100 words'"),
        ("Few-shot examples",  "Show 2-3 input/output pairs before your real question"),
        ("Chain of thought",   "Add 'Think step by step' for math/logic problems"),
        ("Iterate",            "Treat prompting like code — test, observe, refine"),
        ("Negative examples",  "Tell it what NOT to do: 'Do not use jargon'"),
    ]
    for tip, detail in tips:
        print(f"\n  {tip}:")
        print(f"    {detail}")
