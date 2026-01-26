from ValidParenthesis import Solution

# Create an instance of the Solution class
sol = Solution()

# Test cases
test_cases = [
    ("()", True),
    ("()[]{}", True),
    ("(]", False),
    ("([)]", False),
    ("{[]}", True),
    ("", True),  # Empty string
    ("(", False),  # Unmatched opening
    (")", False),  # Unmatched closing
    ("((", False),  # Too many openings
    ("))", False),  # Too many closings
]

print("Testing ValidParenthesis solution:\n")
for test_input, expected in test_cases:
    result = sol.isValid(test_input)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    print(f"{status}: '{test_input}' -> Got: {result}, Expected: {expected}")




