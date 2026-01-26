def solution(n):
    # TODO: implement the solution here
    
    result = 0
    
    while n > 0:
        digit = n % 10
        n = n // 10
        
        result = result * 10 + digit
    
    return result
    
    pass

def test_solution():
    """Test function for solution() with various test cases"""
    test_cases = [
        (123, 321),         # Basic reversal
        (100, 1),           # Ends with zeros: 100 -> 1 (leading zeros dropped)
        (0, 0),             # Zero
        (10, 1),            # 10 -> 1
        (101, 101),         # Palindrome
        (1230, 321),        # Ends with zero
    ]
    
    print("Running tests for solution() - Reverse Integer...\n")
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
    
    # Debug mode - uncomment breakpoint() to pause here
    print("\n" + "="*50)
    print("Debug mode - Set breakpoints and step through the code")
    print("="*50)
    breakpoint()  # Debugger will stop here automatically
    result = solution(12345)
    print(f"\nDebug - Reversing 12345: {result}")