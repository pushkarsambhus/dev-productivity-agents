# Pandas is the go-to library for working with tabular data (like spreadsheets).
# The main objects are: DataFrame (a table with rows and columns) and Series (a single column).

import pandas as pd
import io

# --- Creating a DataFrame from a dictionary ---
# Each key is a column name; each list is the column's values
data = {
    "name":   ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "age":    [25, 32, 28, 45, 31],
    "city":   ["New York", "London", "New York", "Paris", "London"],
    "salary": [70000, 85000, 72000, 95000, 68000]
}
df = pd.DataFrame(data)

# --- Simulating reading a CSV (normally: pd.read_csv("file.csv")) ---
csv_text = """product,price,quantity
Apple,1.20,100
Banana,0.50,200
Cherry,3.00,50
Date,5.00,30
"""
products_df = pd.read_csv(io.StringIO(csv_text))   # StringIO lets us treat text like a file

# --- Accessing data ---
names_col = df["name"]             # get a single column (returns a Series)
first_row = df.iloc[0]             # get first row by position
alice_row = df.loc[df["name"] == "Alice"]  # get row(s) where name is "Alice"

# --- Summary info ---
# df.head()    → first 5 rows
# df.info()    → column names, types, non-null counts
# df.describe() → stats: count, mean, min, max, etc.

# --- Filtering rows: keep only rows that match a condition ---
ny_people = df[df["city"] == "New York"]         # only people in New York
high_earners = df[df["salary"] > 75000]          # only people earning over $75k
young_ny = df[(df["city"] == "New York") & (df["age"] < 30)]  # combine conditions with &

# --- Adding a new column ---
df["salary_k"] = df["salary"] / 1000             # salary in thousands

# --- Sorting ---
by_age = df.sort_values("age")                   # ascending by age
by_salary_desc = df.sort_values("salary", ascending=False)  # highest salary first

# --- GroupBy: split data into groups and aggregate ---
avg_salary_by_city = df.groupby("city")["salary"].mean()  # average salary per city
count_by_city = df.groupby("city")["name"].count()        # how many people per city

# --- Basic stats on a column ---
mean_age = df["age"].mean()
max_salary = df["salary"].max()

if __name__ == "__main__":
    print("=== Full DataFrame ===")
    print(df)

    print("\n=== First 3 rows ===")
    print(df.head(3))

    print("\n=== DataFrame Info ===")
    print(df.dtypes)

    print("\n=== People in New York ===")
    print(ny_people)

    print("\n=== High Earners (>$75k) ===")
    print(high_earners[["name", "city", "salary"]])

    print("\n=== Sorted by Salary (desc) ===")
    print(by_salary_desc[["name", "salary"]])

    print("\n=== Average Salary by City ===")
    print(avg_salary_by_city.round(0))

    print("\n=== Count per City ===")
    print(count_by_city)

    print(f"\nMean age: {mean_age:.1f}")
    print(f"Max salary: ${max_salary:,}")

    print("\n=== Products CSV (loaded) ===")
    print(products_df)
    print("Total inventory value:")
    products_df["total_value"] = products_df["price"] * products_df["quantity"]
    print(products_df)
