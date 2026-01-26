class Solution:
    def isValid(self, s: str) -> bool:
        stack =[]
        closeToOpenMap = {")" :"(" , "}" : "{", "]" : "["}

        for c in s:
            if c in closeToOpenMap:
                if stack and stack[-1] == closeToOpenMap[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        
        return not stack
    
    def test(self, debug=False):
        """
        Test method to help debug the isValid function.
        Run: solution = Solution(); solution.test(debug=True)
        """
        test_cases = [
            ("()", True),
            ("()[]{}", True),
            ("(]", False),
            ("([)]", False),
            ("{[]}", True),
            ("", True),
            ("(", False),
            (")", False),
            ("((", False),
            ("))", False),
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
        closeToOpenMap = {")": "(", "}": "{", "]": "["}
        
        print(f"\n  🔍 Step-by-step debug for '{s}':")
        for i, c in enumerate(s):
            print(f"    Step {i+1}: Processing '{c}'")
            print(f"      Stack before: {stack}")
            
            if c in closeToOpenMap:
                print(f"      '{c}' is a closing bracket, looking for '{closeToOpenMap[c]}'")
                if stack and stack[-1] == closeToOpenMap[c]:
                    popped = stack.pop()
                    print(f"      ✅ Match! Popped '{popped}'")
                else:
                    if not stack:
                        print(f"      ❌ Stack is empty - no match possible")
                    else:
                        print(f"      ❌ Top is '{stack[-1]}', expected '{closeToOpenMap[c]}'")
                    print(f"      Returning False")
                    return False
            else:
                stack.append(c)
                print(f"      '{c}' is opening bracket, added to stack")
            
            print(f"      Stack after: {stack}")
        
        result = True if not stack else False
        print(f"    Final stack: {stack}")
        print(f"    Returning: {result}\n")


if __name__ == "__main__":
    # Run tests when script is executed directly
    solution = Solution()
    solution.test(debug=True)
