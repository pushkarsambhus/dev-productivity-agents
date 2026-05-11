# scikit-learn (sklearn) is Python's most popular Machine Learning library.
# It gives you ready-made ML algorithms so you don't have to build them from scratch.
# This file shows the standard sklearn workflow: split data → train → predict → evaluate.

# =============================================================================
# INSTALLATION (run this in your terminal first)
# =============================================================================
#   pip install scikit-learn

# =============================================================================
# THE SKLEARN WORKFLOW
# =============================================================================
#
#  1. Load / prepare data
#  2. Split into TRAINING set and TEST set
#  3. Choose a model and train it on the training set
#  4. Make predictions on the test set
#  5. Evaluate: how close were the predictions?
#
# The training/test split is crucial:
#   - Training set: the model learns from this (e.g. 80% of data)
#   - Test set: we check real performance on this — model has NEVER seen it (20%)

try:
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("scikit-learn is not installed.")
    print("Install it with: pip install scikit-learn")
    print("\nShowing code walkthrough instead...\n")

import numpy as np

# --- Generate a synthetic dataset ---
# We'll create fake "house" data: size → price
np.random.seed(42)
house_sizes  = np.random.uniform(500, 3500, 100)          # 100 house sizes (sq ft)
house_prices = 150 * house_sizes + np.random.normal(0, 20000, 100)  # price ≈ $150/sq ft + noise

# Reshape to 2D array — sklearn expects features as a 2D array (rows=samples, cols=features)
X = house_sizes.reshape(-1, 1)   # shape: (100, 1)
y = house_prices                  # shape: (100,)

def run_with_sklearn():
    """Full sklearn workflow."""
    print("=== scikit-learn Linear Regression ===\n")

    # Step 1: Split data — 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples:     {len(X_test)}")

    # Step 2: Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)   # "fit" = train the model on training data

    # Step 3: Inspect the learned parameters
    slope     = model.coef_[0]       # price per sq ft
    intercept = model.intercept_     # base price
    print(f"\nLearned: price = ${slope:.2f} × size + ${intercept:,.0f}")

    # Step 4: Predict on the test set
    y_pred = model.predict(X_test)

    # Step 5: Evaluate
    mse  = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2   = r2_score(y_test, y_pred)

    print(f"\nModel Performance on Test Set:")
    print(f"  RMSE (Root Mean Sq Error): ${rmse:,.0f}")
    print(f"  R² Score:                  {r2:.4f}  (1.0 = perfect)")

    # Step 6: Predict for new houses
    print("\nPredictions for new houses:")
    new_sizes = np.array([[800], [1500], [2500], [3000]])
    new_prices = model.predict(new_sizes)
    for size, price in zip(new_sizes.flatten(), new_prices):
        print(f"  {size:,} sq ft → predicted price: ${price:,.0f}")

def show_code_walkthrough():
    """Print the code steps as a reference even without sklearn installed."""
    steps = [
        ("Import",    "from sklearn.model_selection import train_test_split"),
        ("Import",    "from sklearn.linear_model import LinearRegression"),
        ("Import",    "from sklearn.metrics import mean_squared_error, r2_score"),
        ("Split",     "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)"),
        ("Train",     "model = LinearRegression()"),
        ("Train",     "model.fit(X_train, y_train)"),
        ("Predict",   "y_pred = model.predict(X_test)"),
        ("Evaluate",  "mse = mean_squared_error(y_test, y_pred)"),
        ("Evaluate",  "r2  = r2_score(y_test, y_pred)"),
    ]
    print("=== sklearn Workflow (code walkthrough) ===\n")
    for step, code in steps:
        print(f"  [{step:8}]  {code}")

    print("""
Key concepts:
  train_test_split  → randomly splits data into training and test portions
  model.fit()       → trains the model (adjusts internal parameters)
  model.predict()   → uses the trained model to make predictions
  mean_squared_error → how far off predictions are on average
  r2_score          → 1.0 means perfect; 0.0 means no better than a flat line
""")

if __name__ == "__main__":
    if SKLEARN_AVAILABLE:
        run_with_sklearn()
    else:
        show_code_walkthrough()
