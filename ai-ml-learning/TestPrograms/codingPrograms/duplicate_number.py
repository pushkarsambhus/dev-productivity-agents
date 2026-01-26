def solution(n):
    # TODO: Implement the solution
    
    # Handle edge case: if n is 0, return 0
    if n == 0:
        return 0
    
    # Store duplicated digits in a list to preserve order and trailing zeros
    duplicated_digits = []
    
    # Process digits from right to left (least significant first)
    while n > 0:
        digit = n % 10
        duplicated_digit = digit * 10 + digit  # e.g., 3 becomes 33
        duplicated_digits.append(duplicated_digit)
        n = n // 10
    
    # Build result from left to right (most significant first)
    # Reverse the list since we processed digits right-to-left
    result = 0
    for duplicated_digit in reversed(duplicated_digits):
        result = result * 100 + duplicated_digit
    
    return result
    pass

def test_solution():
    """Test function for solution() - Duplicate each digit in the number"""
    test_cases = [
        (100, 110000),      # 100 -> 110000 (zeros duplicated)
        (45, 4455),         # 45 -> 4455
        (1, 11),            # Single digit: 1 -> 11
        (0, 0),             # Zero: 0 -> 0
        (12, 1122),         # 12 -> 1122
        (987, 998877),      # 987 -> 998877
        (1234, 11223344),   # 1234 -> 11223344
        (5, 55),            # Single digit: 5 -> 55
        (999, 999999),      # All same digits
    ]
    
    print("Running tests for solution() - Duplicate Number...\n")
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
        if result != expected:
            # Show what the input looks like for debugging
            input_str = str(input_val)
            expected_str = ''.join([d + d for d in input_str])
            print(f"      Hint: '{input_str}' should become '{expected_str}' = {int(expected_str) if expected_str else 0}")
    
    print(f"\n{'='*50}")
    print(f"Total: {len(test_cases)} tests | Passed: {passed} | Failed: {failed}")
    print(f"{'='*50}")
    
    return failed == 0


# Test the function
if __name__ == "__main__":
    # Run comprehensive tests
    test_solution()
    
    # Debug mode - uncomment breakpoint() to pause here
    print("\n" + "="*50)
    print("Debug mode - Set breakpoints and step through the code")
    print("="*50)
    breakpoint()  # Debugger will stop here automatically
    result = solution(123)
    print(f"\nDebug - Duplicating 123: {result} (expected 112233)")