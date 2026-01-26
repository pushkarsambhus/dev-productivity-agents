class evalRPN:
    def evalRPN(self, tokens):
        stack = []
        operators = ["+", "-", "*", "/"]
        result = 0

        for token in tokens:
            if token in operators:
                first_pop = stack.pop()
                second_pop = stack.pop()

                if token == '+':
                    result = second_pop + first_pop
                elif token == '-':
                    result = second_pop - first_pop
                elif token == '*':
                    result = second_pop * first_pop
                elif token == '/':
                    result = second_pop // first_pop

                stack.append(int(result))
            else:
                stack.append(int(token))

        return stack[-1]

if __name__ == "__main__":
    sol = evalRPN()

    print(sol.evalRPN(["2", "1", "+", "3", "*"]))  # 9
    print(sol.evalRPN(["4", "13", "5", "/", "+"]))  # 6
    print(sol.evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]))  # 22