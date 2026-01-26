class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        star_stack = []  # Track positions of '*' characters
        
        for i, c in enumerate(s):
            if c == '(':
                stack.append(i)
            elif c == '*':
                star_stack.append(i)  # Store '*' position
            elif c == ')':  # c == ')'
                if stack:
                    stack.pop()  # Match with '('
                elif star_stack:
                    star_stack.pop()  # Use '*' as '(' to match
                else:
                    return False  # No match possible
        
        # Match remaining '(' with '*' (use '*' as ')')
        while stack and star_stack:
            if stack[-1] < star_stack[-1]:  # '*' comes after '('
                stack.pop()
                star_stack.pop()
            else:
                break
        
        return len(stack) == 0
    
    def test(self, debug=False):
        """
        Test method to help debug the isValid function.
        Run: solution = Solution(); solution.test(debug=True)
        """
        test_cases = [
            ("()", True),        # Basic valid
            ("(*)", True),       # '*' as empty or matching
            ("(*))", True),      # '*' can be '('
            ("((*)", True),      # '*' can be ')'
            ("", True),          # Empty string
            ("(", False),        # Unmatched opening
            (")", False),        # Unmatched closing
            ("(*", True),        # '*' can be ')'
            ("*)", True),        # '*' can be '('
            ("())", False),      # Too many closings
            ("(((", False),      # Too many openings
            ("(()", False),      # Unmatched opening
            ("())", False),      # Unmatched closing
            ("(*))", True),      # Valid with wildcard
            ("(**", True),       # Can use '*' as closings
            ("**)", True),       # Can use '*' as openings
        ]
        
        print("\n" + "=" * 60)
        print("TESTING ValidParenthesis")
        print("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_input, expected in test_cases:
            result = self.isValid(test_input)
            if result == expected:
                passed += 1
                status = "✅ PASS"
            else:
                failed += 1
                status = "❌ FAIL"
            
            print(f"{status}: '{test_input}' -> Got: {result}, Expected: {expected}")
            
            if debug and result != expected:
                print(f"   Debugging failed case: '{test_input}'")
                print(f"   Running with detailed output...")
                # Re-run with debug if we had a failure
                self._debug_run(test_input)
        
        print("=" * 60)
        print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
        print("=" * 60 + "\n")
    
    def _debug_run(self, s: str):
        """Helper method to debug a specific input"""
        stack = []
        star_stack = []
        
        print(f"\n  🔍 Step-by-step debug for '{s}':")
        print(f"    Initial: stack={stack}, star_stack={star_stack}")
        
        for i, c in enumerate(s):
            print(f"\n    Step {i+1}: Processing '{c}' at position {i}")
            print(f"      Before: stack={stack}, star_stack={star_stack}")
            
            if c == '(':
                stack.append(i)
                print(f"      '{c}' is '(' -> added to stack at position {i}")
            elif c == '*':
                star_stack.append(i)
                print(f"      '{c}' is '*' -> added to star_stack at position {i}")
            elif c == ')':
                if stack:
                    popped = stack.pop()
                    print(f"      '{c}' is ')' -> matched with '(' at position {popped}, popped from stack")
                elif star_stack:
                    popped = star_stack.pop()
                    print(f"      '{c}' is ')' -> matched with '*' at position {popped} (used '*' as '('), popped from star_stack")
                else:
                    print(f"      '{c}' is ')' -> no match possible, returning False")
                    return False
            
            print(f"      After: stack={stack}, star_stack={star_stack}")
        
        # Match remaining '(' with '*'
        print(f"\n    Matching remaining '(' with '*' (using '*' as ')'):")
        while stack and star_stack:
            if stack[-1] < star_stack[-1]:
                stack_pos = stack.pop()
                star_pos = star_stack.pop()
                print(f"      Matched '(' at {stack_pos} with '*' at {star_pos}")
            else:
                print(f"      Cannot match: '(' at {stack[-1]} comes after '*' at {star_stack[-1]}")
                break
        
        result = len(stack) == 0
        print(f"\n    Final: stack={stack}, star_stack={star_stack}")
        print(f"    Result: len(stack) == 0 -> {result}\n")


if __name__ == "__main__":
    # Run tests when script is executed directly
    solution = Solution()
    solution.test(debug=True)
