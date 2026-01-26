class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        closeToOpenMap  = {")":"(", "}" : "{", "]" : "[" }

        for c in s:
            if c in closeToOpenMap:
                if stack and stack[-1] == closeToOpenMap[c] :
                    stack.pop()
                else :
                    return false
            else :
                stack.append(c)
        
        return not stack 

if __name__ == "__main__":
    solution = Solution()
    
    # Add your test cases here
    result = solution.isValid("()[]{}")
    print(f"Result: {result}")