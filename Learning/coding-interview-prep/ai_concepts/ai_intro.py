# Artificial Intelligence (AI) is about making computers "smart" —
# giving them the ability to learn from data and make decisions, just like humans do.

# =============================================================================
# WHAT IS AI?
# =============================================================================
#
# AI is a broad field. Think of it like a set of Russian nesting dolls:
#
#  ┌─────────────────────────────────────────────────────────┐
#  │  Artificial Intelligence (AI)                           │
#  │   — any technique that makes computers seem "smart"     │
#  │                                                         │
#  │   ┌───────────────────────────────────────────────┐     │
#  │   │  Machine Learning (ML)                        │     │
#  │   │   — computers learn from data (no hard rules) │     │
#  │   │                                               │     │
#  │   │   ┌───────────────────────────────────────┐   │     │
#  │   │   │  Deep Learning (DL)                   │   │     │
#  │   │   │   — ML using neural networks          │   │     │
#  │   │   │   — powers GPT, image recognition     │   │     │
#  │   │   └───────────────────────────────────────┘   │     │
#  │   └───────────────────────────────────────────────┘     │
#  └─────────────────────────────────────────────────────────┘

# =============================================================================
# THREE TYPES OF MACHINE LEARNING
# =============================================================================

# 1. SUPERVISED LEARNING
# -----------------------
# Analogy: A student studying with an answer key.
# You give the model labeled examples (input + correct answer).
# The model learns the pattern so it can predict answers for NEW inputs.
#
# Example tasks:
#   - Email spam detection: input = email text, label = spam or not spam
#   - House price prediction: input = size/location, label = actual price
#   - Image classification: input = photo, label = "cat" or "dog"
#
# Common algorithms:
#   - Linear Regression (predict numbers)
#   - Decision Trees
#   - Neural Networks

# 2. UNSUPERVISED LEARNING
# -------------------------
# Analogy: Sorting a pile of mixed Lego pieces without instructions.
# You give the model data WITHOUT labels — it finds patterns on its own.
#
# Example tasks:
#   - Customer segmentation: group shoppers by buying habits
#   - Anomaly detection: find unusual transactions (fraud)
#   - Dimensionality reduction: compress complex data while keeping key info
#
# Common algorithms:
#   - K-Means Clustering
#   - PCA (Principal Component Analysis)

# 3. REINFORCEMENT LEARNING
# --------------------------
# Analogy: Training a dog with treats and corrections.
# An "agent" takes actions in an environment, gets rewards for good moves,
# and penalties for bad ones. Over time, it learns the best strategy.
#
# Example tasks:
#   - Playing games (AlphaGo beat the world chess and Go champion this way)
#   - Robot navigation
#   - Optimizing ad placements
#
# Key terms:
#   - Agent: the learner/decision-maker
#   - Environment: the world it operates in
#   - Reward: positive feedback for good actions
#   - Policy: the strategy it develops

# =============================================================================
# KEY ML CONCEPTS (plain English)
# =============================================================================

# TRAINING: showing the model lots of examples so it can learn patterns
# TEST SET: data the model has NEVER seen — used to measure real performance
# OVERFITTING: model memorizes training data but fails on new data
#   Analogy: student who memorizes answers but can't solve new problems
# UNDERFITTING: model is too simple to capture the real pattern
#   Analogy: student who barely studied and gets everything wrong

# FEATURES: the input variables used to make a prediction
#   e.g. for house prices: square footage, bedrooms, location are all features
# LABEL / TARGET: the value we're trying to predict
#   e.g. for house prices: the actual sale price

# MODEL: a mathematical function that maps features → label
# PARAMETERS: the numbers inside the model that get adjusted during training
# LOSS FUNCTION: measures how wrong the model's predictions are
#   (lower loss = better model)
# GRADIENT DESCENT: the optimization method that adjusts parameters
#   to reduce the loss — like rolling a ball downhill to the lowest point

# =============================================================================
# SIMPLE DEMONSTRATION: "Supervised Learning" concept in pure Python
# =============================================================================

def simple_classifier(hours_studied):
    """
    Super-simple 'model': predict pass/fail based on hours studied.
    In real ML, the threshold 5.0 would be LEARNED from data.
    """
    threshold = 5.0   # learned threshold
    return "pass" if hours_studied >= threshold else "fail"

def show_ml_pipeline():
    """Simulate the basic steps of a supervised ML pipeline."""
    print("=== Simulated ML Pipeline ===\n")

    # Step 1: Collect data (features + labels)
    training_data = [
        # (hours_studied, result)
        (2, "fail"), (3, "fail"), (4, "fail"),
        (5, "pass"), (6, "pass"), (8, "pass"), (9, "pass"),
    ]
    print("Step 1 — Training data:")
    for hours, label in training_data:
        print(f"  {hours} hrs → {label}")

    # Step 2: "Train" our model (here: just finding the threshold manually)
    print("\nStep 2 — Training: finding the right threshold...")
    print("  (In real ML, this is done automatically by the algorithm)")

    # Step 3: Evaluate on new (unseen) test data
    test_data = [(3.5, "fail"), (5.5, "pass"), (7, "pass"), (1, "fail")]
    print("\nStep 3 — Testing on new data:")
    correct = 0
    for hours, actual in test_data:
        prediction = simple_classifier(hours)
        status = "✓" if prediction == actual else "✗"
        print(f"  {status} {hours} hrs: predicted={prediction}, actual={actual}")
        if prediction == actual:
            correct += 1

    accuracy = correct / len(test_data) * 100
    print(f"\nAccuracy: {correct}/{len(test_data)} = {accuracy:.0f}%")

if __name__ == "__main__":
    print("=" * 60)
    print("INTRODUCTION TO AI & MACHINE LEARNING")
    print("=" * 60)

    print("""
Types of Machine Learning:

1. SUPERVISED LEARNING
   → Learn from labeled examples
   → Like: spam filter, price prediction, image recognition

2. UNSUPERVISED LEARNING
   → Find hidden patterns in unlabeled data
   → Like: customer grouping, anomaly detection

3. REINFORCEMENT LEARNING
   → Learn by trial and error with rewards
   → Like: game-playing AI, robotics
""")

    show_ml_pipeline()

    print("\nKey vocabulary:")
    terms = {
        "Feature":        "An input variable (e.g. house size, email words)",
        "Label/Target":   "The value we want to predict (e.g. price, spam/not spam)",
        "Model":          "A function that maps features to a label",
        "Training":       "Fitting the model to historical data",
        "Overfitting":    "Memorizing training data — fails on new data",
        "Loss Function":  "Measures how wrong the model's predictions are",
    }
    for term, definition in terms.items():
        print(f"  {term:18}: {definition}")
