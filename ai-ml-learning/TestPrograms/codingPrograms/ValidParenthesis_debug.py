class Solution:
    def isValid(self, s: str, debug=False) -> bool:
        stack = []
        closeToOpenMap = {")": "(", "}": "{", "]": "["}
        
        if debug:
            print(f"\n🔍 Debugging: '{s}'")
            print("=" * 50)

        for i, c in enumerate(s):
            if debug:
                print(f"\nStep {i+1}: Processing character '{c}'")
                print(f"  Current stack: {stack}")
            
            if c in closeToOpenMap:
                if debug:
                    print(f"  '{c}' is a closing bracket")
                    print(f"  Looking for opening: {closeToOpenMap[c]}")
                
                if stack and stack[-1] == closeToOpenMap[c]:
                    popped = stack.pop()
                    if debug:
                        print(f"  ✅ Match found! Popped '{popped}' from stack")
                        print(f"  New stack: {stack}")
                else:
                    if debug:
                        if not stack:
                            print(f"  ❌ Stack is empty - no match possible")
                        else:
                            print(f"  ❌ Top of stack is '{stack[-1]}', expected '{closeToOpenMap[c]}'")
                    return False
            else:
                stack.append(c)
                if debug:
                    print(f"  '{c}' is an opening bracket, added to stack")
                    print(f"  New stack: {stack}")
        
        result = True if not stack else False
        if debug:
            print(f"\n{'=' * 50}")
            if result:
                print(f"✅ Final result: True (all brackets matched)")
            else:
                print(f"❌ Final result: False (stack still has: {stack})")
        
        return result


# Test with debug mode
if __name__ == "__main__":
    sol = Solution()
    
    # Test cases with debug output
    test_cases = [
        "()",
        "([)]",
        "{[]}",
        "(((",
    ]
    
    for test in test_cases:
        sol.isValid(test, debug=True)
        print("\n")




