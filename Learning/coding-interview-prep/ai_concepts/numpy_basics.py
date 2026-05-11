# NumPy (Numerical Python) gives us fast, powerful arrays for math and data.
# Think of a NumPy array like a super-powered list designed for numbers and math operations.

import numpy as np

# --- Creating arrays ---
simple_array = np.array([1, 2, 3, 4, 5])              # 1D array (like a row of numbers)
two_d_array = np.array([[1, 2, 3], [4, 5, 6]])        # 2D array (like a table/grid)

zeros = np.zeros((3, 3))       # 3x3 grid of zeros
ones = np.ones((2, 4))         # 2x4 grid of ones
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8] — like range() but for arrays
linspace = np.linspace(0, 1, 5)  # 5 evenly spaced values between 0 and 1

# --- Array properties ---
# .shape tells you the dimensions (rows, columns)
# .dtype tells you what type of numbers are stored

# --- Math operations: applied to every element at once ---
a = np.array([10, 20, 30, 40])
doubled = a * 2           # [20, 40, 60, 80] — no loop needed!
shifted = a + 5           # [15, 25, 35, 45]
squared = a ** 2          # [100, 400, 900, 1600]

# --- Matrix operations ---
matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])

element_multiply = matrix_a * matrix_b   # multiplies each matching element
dot_product = np.dot(matrix_a, matrix_b) # real matrix multiplication (rows × columns)

# --- Aggregation: summarizing data ---
data = np.array([4, 7, 2, 9, 1, 5, 8, 3, 6])
mean = np.mean(data)       # average
median = np.median(data)   # middle value
std = np.std(data)         # how spread out the values are
total = np.sum(data)

# --- Slicing (same idea as Python lists) ---
row = two_d_array[0]         # first row: [1, 2, 3]
col = two_d_array[:, 1]      # second column: [2, 5]
subset = two_d_array[0, 1:3] # row 0, columns 1 and 2: [2, 3]

# --- Boolean indexing: filter values using a condition ---
big_values = data[data > 5]   # returns only values greater than 5

if __name__ == "__main__":
    print("Simple array:", simple_array)
    print("2D array:\n", two_d_array)
    print("Zeros:\n", zeros)
    print("Range array:", range_arr)
    print("Linspace:", linspace)
    print("\nArray shape:", two_d_array.shape)
    print("Data type:", simple_array.dtype)

    print("\nMath on array a =", a)
    print("  Doubled:", doubled)
    print("  Shifted:", shifted)
    print("  Squared:", squared)

    print("\nMatrix A:\n", matrix_a)
    print("Matrix B:\n", matrix_b)
    print("Element-wise multiply:\n", element_multiply)
    print("Dot product (matrix multiply):\n", dot_product)

    print("\nData:", data)
    print("  Mean:", mean)
    print("  Median:", median)
    print("  Std dev:", round(std, 2))
    print("  Sum:", total)

    print("\nFirst row:", row)
    print("Second column:", col)
    print("Values > 5:", big_values)
