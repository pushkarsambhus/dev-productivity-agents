def findMinMaxRowCol(matrix: List[List[int]]) -> dict:
    if not matrix:
        return {}
    
    m, n = len(matrix), len(matrix[0])
    result = {"rows": {}, "cols": {}}
    
    # Rows
    for i in range(m):
        result["rows"][i] = {
            "min": min(matrix[i]),
            "max": max(matrix[i])
        }
    
    # Columns
    for j in range(n):
        col = [matrix[i][j] for i in range(m)]
        result["cols"][j] = {
            "min": min(col),
            "max": max(col)
        }
    
    return result

# Example:
# Input: [[1,2,3], [4,5,6], [7,8,9]]
# Output: {"rows": {0: {min:1, max:3}, ...}, "cols": {0: {min:1, max:7}, ...}}