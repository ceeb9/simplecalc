from typing import Callable
import operator
import sys
import state
from collections import deque

#        todo
# resolve variables when evaluating

class Operation():
    def __init__(self, opstring: str, op_count: int, priority: int, function: Callable):
        """priority goes low -> high e.g. 1 is the lowest priority"""
        self.opstring = opstring
        self.op_count = op_count
        self.priority = priority
        self.function = function

class ExpressionEval():
    operator_list = [
        Operation("+", 2, 1, operator.add),
        Operation("-", 2, 1, operator.sub),
        Operation("*", 2, 2, operator.mul),
        Operation("/", 2, 2, operator.truediv),
        Operation("^", 2, 3, operator.pow),
    ]
    opstring_list = [x.opstring for x in operator_list]

    def opstring_to_op(self, opstring: str):
        return {x.opstring: x for x in ExpressionEval.operator_list}[opstring]
    
    def tokenize_equation_str(self, equation_str: str) -> deque:
        """takes in an infix expression and tokenizes it, putting each token as a string in a deque"""
        tokens = deque()
        token_delimiters = [x.opstring for x in ExpressionEval.operator_list] + ["(", ")"]
        cur_token = ""
    
        # go over each char
        for char in equation_str:
            # if we reach a term delimiter, add the accumulated term to the term array
            if char in token_delimiters:
                # prevents trying to add the "last term" if the first character is a bracket for example
                if cur_token != "":
                    tokens.append(cur_token)
                    cur_token = ""
    
                # add the operator
                tokens.append(char)
    
            # add char to accumulated term
            else:
                cur_token += char
    
        # add the last number to the array of terms
        if cur_token != "":
            tokens.append(cur_token)
            cur_token = ""
    
        for token in tokens: print(f"type: {type(token)} | token: {token}")
    
        return tokens
            
    def infix_to_postfix(self, tokens: deque[str]) -> deque[str]:
        """takes in a deque of tokens in infix order, left to right, and outputs a deque of tokens as a postfix queue"""
        operator_stack = deque()
        postfix_queue = deque()
        
        for item in tokens:
            if item == '(': operator_stack.append('(')
            elif item == ')':
                # do all the remaining lowest level calculations left in the brackets
                while operator_stack[-1] != '(':
                    cur_op = operator_stack.pop()
                    #print(cur_op)
                    postfix_queue.append(cur_op)
                operator_stack.pop() # remove '('
                
            elif item in ExpressionEval.opstring_list:
                # add ops to postfix until this "section" is complete (we find another equal level op)
                while len(operator_stack) > 0 and operator_stack[-1] != '(' and self.opstring_to_op(item).priority <= self.opstring_to_op(operator_stack[-1]).priority:
                    cur_op = operator_stack.pop()
                    #print(cur_op)
                    postfix_queue.append(cur_op)
                operator_stack.append(item)
    
            else:
                # add number to postfix (it hasnt been an op or a bracket)
                #print(item)
                postfix_queue.append(item)
                    
        # do all the remaining lowest level calculations left
        while len(operator_stack) != 0:
            cur = operator_stack.pop()
            #print(cur)
            postfix_queue.append(cur)
    
        return postfix_queue

    def resolve_variables(self, tokens: deque[str]) -> deque[str]:
        """takes in a deque of tokens, checks for variables and replaces them with their values, returning the same deque with replaced values"""
        for i in range(len(tokens)):
            if tokens[i] in state.user_vars:
                tokens[i] = state.user_vars[tokens[i]]
        return tokens
    
    def evaluate_postfix(self, token_queue: deque) -> float:
        """takes in a queue of tokens in postfix order, where each token is an operator, operand, or variable, and evaluates the result"""
        token_queue = self.resolve_variables(token_queue)
        stack = deque()
        while len(token_queue) > 0:
            cur_token = token_queue.popleft()
    
            # evaluate last two operands when operator is encountered
            if cur_token in ExpressionEval.opstring_list:
                if len(stack) < 1: raise ValueError("bad input, tried to pop from an empty stack when evaluating")

                a = float(stack.pop())
                b = float(stack.pop())
                #print(self.opstring_to_op(cur_token).function.__name__)
                result = self.opstring_to_op(cur_token).function(b, a)
                #print(f"eval: {b} {cur_token} {a} = {result}")
                stack.append(result)
    
            # push operand
            else:
                stack.append(cur_token)
    
        result = stack.pop()
        if len(stack) != 0:
            raise ValueError("bad input, stack still had operands in it when there were no more operators to apply")
    
        return result
    
    def solve(self, equation: str) -> float:
        return self.evaluate_postfix(self.infix_to_postfix(self.tokenize_equation_str(equation)))

def main(): 
    e = ExpressionEval()
    print(e.solve(sys.argv[1]))

if __name__ == "__main__":
    main()
