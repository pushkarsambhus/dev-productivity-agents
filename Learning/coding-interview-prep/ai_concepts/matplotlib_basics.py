# Matplotlib is Python's most popular library for creating charts and graphs.
# Think of it as your code-powered graphing tool — like Excel charts, but in Python.

import matplotlib
matplotlib.use("Agg")        # use non-interactive backend (saves to file instead of screen)
import matplotlib.pyplot as plt
import numpy as np

# --- Line Plot: great for showing trends over time ---
def line_plot():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = [1200, 1500, 1350, 1800, 2100, 1950]

    plt.figure(figsize=(8, 4))             # set the figure size (width, height in inches)
    plt.plot(months, sales, marker="o", color="blue", linewidth=2, label="Sales")
    plt.title("Monthly Sales")             # chart title
    plt.xlabel("Month")                    # x-axis label
    plt.ylabel("Sales ($)")               # y-axis label
    plt.legend()                           # shows the label box
    plt.grid(True, alpha=0.3)             # light grid lines
    plt.tight_layout()
    plt.savefig("/tmp/line_plot.png")      # save to file
    plt.close()
    print("Saved: /tmp/line_plot.png")

# --- Bar Chart: great for comparing categories ---
def bar_chart():
    fruits = ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"]
    counts = [45, 72, 30, 18, 55]
    colors = ["red", "yellow", "darkred", "brown", "purple"]

    plt.figure(figsize=(8, 4))
    plt.bar(fruits, counts, color=colors, edgecolor="black")
    plt.title("Fruit Sales This Week")
    plt.xlabel("Fruit")
    plt.ylabel("Units Sold")
    plt.tight_layout()
    plt.savefig("/tmp/bar_chart.png")
    plt.close()
    print("Saved: /tmp/bar_chart.png")

# --- Scatter Plot: great for showing relationships between two variables ---
def scatter_plot():
    np.random.seed(42)   # set seed so we get the same "random" numbers every time
    study_hours = np.random.uniform(1, 10, 50)             # 50 random study times (1-10 hrs)
    test_scores = study_hours * 7 + np.random.normal(0, 5, 50)  # score ≈ hours × 7, plus noise
    test_scores = np.clip(test_scores, 0, 100)             # cap scores between 0 and 100

    plt.figure(figsize=(7, 5))
    plt.scatter(study_hours, test_scores, color="green", alpha=0.6, edgecolors="darkgreen")
    plt.title("Study Hours vs Test Score")
    plt.xlabel("Hours Studied")
    plt.ylabel("Test Score")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("/tmp/scatter_plot.png")
    plt.close()
    print("Saved: /tmp/scatter_plot.png")

# --- Multi-panel figure: show multiple charts in one image ---
def combined_figure():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))   # 1 row, 3 columns

    # Panel 1: Line plot
    x = np.linspace(0, 2 * np.pi, 100)   # 100 points from 0 to 2π
    axes[0].plot(x, np.sin(x), color="blue", label="sin(x)")
    axes[0].plot(x, np.cos(x), color="red", label="cos(x)")
    axes[0].set_title("Sine & Cosine Waves")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Panel 2: Bar chart
    categories = ["A", "B", "C", "D"]
    values = [23, 45, 12, 67]
    axes[1].bar(categories, values, color="steelblue")
    axes[1].set_title("Category Comparison")

    # Panel 3: Histogram — shows how data is distributed
    data = np.random.normal(50, 10, 500)   # 500 numbers centered around 50
    axes[2].hist(data, bins=20, color="orange", edgecolor="black")
    axes[2].set_title("Score Distribution")
    axes[2].set_xlabel("Score")

    plt.suptitle("Combined Chart Example", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("/tmp/combined_charts.png")
    plt.close()
    print("Saved: /tmp/combined_charts.png")

if __name__ == "__main__":
    line_plot()
    bar_chart()
    scatter_plot()
    combined_figure()
    print("\nAll charts saved to /tmp/")
    print("Tip: Change savefig() paths to save wherever you like.")
    print("Tip: Replace plt.savefig() with plt.show() to display charts interactively.")
