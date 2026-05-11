# Linear Regression finds the "best fit" straight line through a set of data points.
# It's one of the simplest ML algorithms — great for predicting numbers (like house prices).
# We'll build it from scratch using just math, no libraries needed.

# =============================================================================
# THE IDEA
# =============================================================================
#
# We want to predict y from x using a straight line:
#
#     y = m * x + b
#
#   where:
#     x = input (feature), e.g. hours studied
#     y = output (label), e.g. exam score
#     m = slope — how much y changes per unit of x
#     b = intercept — where the line crosses the y-axis
#
# "Training" means finding the best values of m and b so the line
# fits the data as closely as possible.
#
# We measure "closeness" using Mean Squared Error (MSE):
#   MSE = average of (actual_y - predicted_y)²
#   → lower MSE = better fit

# =============================================================================
# MATH FORMULAS (closed-form solution — exact answer, no iteration needed)
# =============================================================================
#
#   m = Σ[(xi - x_mean)(yi - y_mean)] / Σ[(xi - x_mean)²]
#   b = y_mean - m * x_mean
#
#   This is called the "Ordinary Least Squares" formula.

def mean(values):
    """Calculate the average of a list of numbers."""
    return sum(values) / len(values)

def train_linear_regression(x_data, y_data):
    """
    Find the best slope (m) and intercept (b) for the data.
    Returns (m, b) — the parameters of our model.
    """
    n = len(x_data)
    x_avg = mean(x_data)
    y_avg = mean(y_data)

    # Calculate numerator and denominator for the slope formula
    numerator = sum((x_data[i] - x_avg) * (y_data[i] - y_avg) for i in range(n))
    denominator = sum((x_data[i] - x_avg) ** 2 for i in range(n))

    slope = numerator / denominator          # m
    intercept = y_avg - slope * x_avg        # b

    return slope, intercept

def predict(x, slope, intercept):
    """Use our trained model to predict y for a given x."""
    return slope * x + intercept

def mean_squared_error(y_actual, y_predicted):
    """
    Measure how wrong our predictions are on average.
    Lower = better. Zero = perfect.
    """
    n = len(y_actual)
    return sum((y_actual[i] - y_predicted[i]) ** 2 for i in range(n)) / n

def r_squared(y_actual, y_predicted):
    """
    R² (R-squared): how well the line explains the data.
    1.0 = perfect fit, 0.0 = no better than just using the mean.
    """
    y_avg = mean(y_actual)
    ss_total = sum((y - y_avg) ** 2 for y in y_actual)       # total variance
    ss_residual = sum((y_actual[i] - y_predicted[i]) ** 2 for i in range(len(y_actual)))
    return 1 - (ss_residual / ss_total)

if __name__ == "__main__":
    # --- Dataset: hours studied vs exam score ---
    hours_studied = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    exam_scores   = [52, 55, 58, 65, 68, 72, 75, 82, 87, 90]
    # There's a clear upward trend: more studying → higher score

    print("=== Linear Regression From Scratch ===\n")
    print("Training data:")
    for h, s in zip(hours_studied, exam_scores):
        print(f"  {h} hrs → {s} points")

    # Step 1: Train the model (find m and b)
    m, b = train_linear_regression(hours_studied, exam_scores)
    print(f"\nTrained model: score = {m:.2f} × hours + {b:.2f}")
    print(f"  Interpretation: each extra hour of study → +{m:.1f} points")

    # Step 2: Make predictions
    predictions = [predict(h, m, b) for h in hours_studied]

    print("\nPredictions vs Actual:")
    print(f"{'Hours':>6} | {'Actual':>8} | {'Predicted':>10} | {'Error':>7}")
    print("-" * 38)
    for h, actual, pred in zip(hours_studied, exam_scores, predictions):
        error = actual - pred
        print(f"{h:>6} | {actual:>8} | {pred:>10.1f} | {error:>+7.1f}")

    # Step 3: Evaluate the model
    mse = mean_squared_error(exam_scores, predictions)
    r2  = r_squared(exam_scores, predictions)
    print(f"\nMean Squared Error: {mse:.2f}  (lower is better)")
    print(f"R² Score:           {r2:.4f}  (1.0 = perfect, 0.0 = random guessing)")

    # Step 4: Predict for new, unseen values
    print("\nPredictions for new students:")
    for new_hours in [3.5, 6.5, 11]:
        score = predict(new_hours, m, b)
        print(f"  {new_hours} hours → predicted score: {score:.1f}")
