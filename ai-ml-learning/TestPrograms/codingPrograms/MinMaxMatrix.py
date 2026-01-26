class MinMaxMatrix:
    def maxInRowsAndColumns(self, matrix):
        """
        Find max element in each row and each column
        """
        if not matrix or not matrix[0]:
            return None

        rows = len(matrix)
        cols = len(matrix[0])

        # Max in each row
        row_maxes = []
        for i in range(rows):
            row_max = max(matrix[i])
            row_maxes.append(row_max)
            print(f"Row {i}: max = {row_max}")

        # Max in each column
        col_maxes = []
        for j in range(cols):
            col_max = max(matrix[i][j] for i in range(rows))
            col_maxes.append(col_max)
            print(f"Column {j}: max = {col_max}")

        return row_maxes, col_maxes

    def setMatrixZeroes(self, matrix):
        """
        If matrix[i][j] = 0, set entire row i and column j to 0
        """
        if not matrix or not matrix[0]:
            return

        rows = len(matrix)
        cols = len(matrix[0])

        # Track which rows and columns need to be zeroed
        zero_rows = set()
        zero_cols = set()

        # First pass: find all zeros
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        # Second pass: set rows to zero
        for row in zero_rows:
            for j in range(cols):
                matrix[row][j] = 0

        # Third pass: set columns to zero
        for col in zero_cols:
            for i in range(rows):
                matrix[i][col] = 0

        return matrix


if __name__ == "__main__":
    sol = MinMaxMatrix()

    # Max in rows and columns
    matrix1 = [[1, 5, 3], [4, 2, 6], [7, 8, 9]]
    print(sol.maxInRowsAndColumns(matrix1))
    # Row maxes: [5, 6, 9]
    # Col maxes: [7, 8, 9]

    # Set matrix zeroes
    matrix2 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    sol.setMatrixZeroes(matrix2)
    print(matrix2)
    # [[1, 0, 1], [0, 0, 0], [1, 0, 1]]