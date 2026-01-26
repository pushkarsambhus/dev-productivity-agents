class setMatrixZeroes:
    def setMatrixZeroes(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])

        zero_rows = set()
        zero_cols = set()

        # Find zeros
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        # Set zeros
        for row in zero_rows:
            for j in range(cols):
                matrix[row][j] = 0

        for col in zero_cols:
            for i in range(rows):
                matrix[i][col] = 0

        return matrix


if __name__ == "__main__":
    sol = setMatrixZeroes()

    # Test 1: Single zero in middle
    matrix1 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    print("Test 1 - Single zero in middle:")
    print("Input:", matrix1)
    result1 = sol.setMatrixZeroes(matrix1)
    print("Output:", result1)
    print("Expected: [[1, 0, 1], [0, 0, 0], [1, 0, 1]]")
    print()

    # Test 2: Multiple zeros
    matrix2 = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    print("Test 2 - Multiple zeros:")
    print("Input:", matrix2)
    result2 = sol.setMatrixZeroes(matrix2)
    print("Output:", result2)
    print("Expected: [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]")
    print()

    # Test 3: No zeros
    matrix3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("Test 3 - No zeros:")
    print("Input:", matrix3)
    result3 = sol.setMatrixZeroes(matrix3)
    print("Output:", result3)
    print("Expected: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]")
    print()

    # Test 4: Entire row is zero
    matrix4 = [[1, 2, 3], [0, 0, 0], [7, 8, 9]]
    print("Test 4 - Entire row is zero:")
    print("Input:", matrix4)
    result4 = sol.setMatrixZeroes(matrix4)
    print("Output:", result4)
    print("Expected: [[0, 2, 3], [0, 0, 0], [0, 8, 9]]")
    print()

    # Test 5: Entire column is zero
    matrix5 = [[1, 0, 3], [4, 0, 6], [7, 0, 9]]
    print("Test 5 - Entire column is zero:")
    print("Input:", matrix5)
    result5 = sol.setMatrixZeroes(matrix5)
    print("Output:", result5)
    print("Expected: [[0, 0, 0], [0, 0, 0], [0, 0, 0]]")
    print()

    # Test 6: Single element (zero)
    matrix6 = [[0]]
    print("Test 6 - Single element (zero):")
    print("Input:", matrix6)
    result6 = sol.setMatrixZeroes(matrix6)
    print("Output:", result6)
    print("Expected: [[0]]")
    print()

    # Test 7: Single element (non-zero)
    matrix7 = [[5]]
    print("Test 7 - Single element (non-zero):")
    print("Input:", matrix7)
    result7 = sol.setMatrixZeroes(matrix7)
    print("Output:", result7)
    print("Expected: [[5]]")
    print()

    # Test 8: Zero in corner
    matrix8 = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    print("Test 8 - Zero in corner:")
    print("Input:", matrix8)
    result8 = sol.setMatrixZeroes(matrix8)
    print("Output:", result8)
    print("Expected: [[0, 0, 0], [0, 4, 5], [0, 7, 8]]")