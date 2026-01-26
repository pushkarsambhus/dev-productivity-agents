def solution(n):
    # TODO: implement
    digit_product = 1
    even_count = 0
    original_length = len(str(n))
    while n > 0:
        digit = n % 10
        
        if digit % 2 != 0:
           digit_product *= digit
        else:
            even_count +=1
        
        n = n // 10

    if(even_count == original_length):
        digit_product = 0

    return digit_product
    pass

def test_solution():
    """Test function for solution() with various test cases"""
    test_cases = [
        (135, 15),      # All odd digits: 1 * 3 * 5 = 15
        (2468, 0),      # All even digits: should return 0
        (12345, 15),    # Mixed: 1 * 3 * 5 = 15 (ignores 2 and 4)
        (246, 0),       # All even: should return 0
        (1357, 105),    # All odd: 1 * 3 * 5 * 7 = 105
        (1234, 3),      # Mixed: 1 * 3 = 3 (ignores 2 and 4)
        (1, 1),         # Single odd digit
        (2, 0),         # Single even digit
        (0, 0),         # Zero
        (135246, 15),   # Mixed with odd first: 1 * 3 * 5 = 15
    ]
    
    print("Running tests for solution()...\n")
    passed = 0
    failed = 0
    
    for input_val, expected in test_cases:
        result = solution(input_val)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status}: solution({input_val}) = {result} (expected {expected})")
    
    print(f"\n{'='*50}")
    print(f"Total: {len(test_cases)} tests | Passed: {passed} | Failed: {failed}")
    print(f"{'='*50}")
    
    return failed == 0


# Test the function
if __name__ == "__main__":
    # Run comprehensive tests
    test_solution()
    
    # Optional: Uncomment for debugging
    # breakpoint()
    # result = solution(2468)
    # print(f"\nDebug - Result: {result}")