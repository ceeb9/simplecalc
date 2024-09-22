from typing import Callable
import operator
import sys
import state
import math
from collections import deque

#        todo
# implement unary operators

class Operation():
    def __init__(self, opstring: str, operand_count: int, priority: int, is_function: bool, function: Callable):
        """priority goes low -> high e.g. 1 is the lowest priority"""
        self.opstring = opstring
        self.operand_count = operand_count
        self.priority = priority
        self.is_function = is_function
        self.function = function

class ExpressionEval():
    operator_list = [
        Operation("+", 2, 1, False, operator.add),
        Operation("-", 2, 1, False, operator.sub),
        Operation("*", 2, 2, False, operator.mul),
        Operation("/", 2, 2, False, operator.truediv),
        Operation("^", 2, 3, False, operator.pow),
        Operation("<", 2, 0, False, operator.lt),
        Operation(">", 2, 0, False, operator.gt),
        Operation("sqrt", 1, 0, True, math.sqrt),
    ]
    opstring_list = [x.opstring for x in operator_list]
    opstring_to_op = {x.opstring: x for x in operator_list}

    def tokenize_equation_str(self, equation_str: str) -> deque:
        """takes in an infix expression and tokenizes it, putting each token as a string in a deque. also places function names after their brackets, to make eval easier"""
        fn_reorder_stack = deque()
        tokens = deque()
        token_delimiters = [x.opstring for x in ExpressionEval.operator_list] + ["(", ")"]
        cur_token = ""
    
        # go over each char
        for char in equation_str:
            # add brackets (and function names) to the stack to allow us to know where the end of a function's brackets are
            if char == ")" and fn_reorder_stack[-1] == "(":
                fn_reorder_stack.pop()

            if char == "(" and cur_token in self.opstring_list and self.opstring_to_op[cur_token].is_function:
                fn_reorder_stack.append(cur_token)
                fn_reorder_stack.append("(")
                cur_token = ""

            elif char == "(":
                fn_reorder_stack.append("(")

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

            # if a function's brackets are over, reinsert the function name
            if len(fn_reorder_stack) > 0 and fn_reorder_stack[-1] not in "()":
                tokens.append(fn_reorder_stack.pop())
    
        # add the last number to the array of terms
        if cur_token != "":
            tokens.append(cur_token)
            cur_token = ""
    
        #for token in tokens: print(f"type: {type(token)} | token: {token}")
    
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

            elif item in ExpressionEval.opstring_list and not self.opstring_to_op[item].is_function:
                # add ops to postfix until this "section" is complete (we find another equal level op)
                while len(operator_stack) > 0 and operator_stack[-1] != '(' and self.opstring_to_op[item].priority <= self.opstring_to_op[operator_stack[-1]].priority:
                    cur_op = operator_stack.pop()
                    #print(cur_op)
                    postfix_queue.append(cur_op)
                operator_stack.append(item)
    
            else:
                # add number, function name or variable to postfix (it hasnt been an inline op or a bracket)
                #print(item)
                postfix_queue.append(item)
                    
        # do all the remaining lowest level calculations left
        while len(operator_stack) != 0:
            cur = operator_stack.pop()
            #print(cur)
            postfix_queue.append(cur)
    
        #print(postfix_queue)
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
        value_stack = deque()
        while len(token_queue) > 0:
            cur_token = token_queue.popleft()
    
            # evaluate when operator is encountered
            if cur_token in ExpressionEval.opstring_list:
                if len(value_stack) < 1: raise ValueError("bad input, tried to pop from an empty value_stack when evaluating")

                operands = deque()
                for _ in range(self.opstring_to_op[cur_token].operand_count):
                    operands.appendleft(float(value_stack.pop()))

                #print(self.opstring_to_op(cur_token).function.__name__)
                result = float(self.opstring_to_op[cur_token].function(*list(operands)))
                #print(f"operands: {operands}, operator: {cur_token}, result: {result}")
                value_stack.append(result)
    
            # push operand
            else:
                value_stack.append(cur_token)
    
        result = value_stack.pop()
        if len(value_stack) != 0:
            raise ValueError("bad input, value_stack still had operands in it when there were no more operators to apply")
    
        return result
    
    def solve(self, equation: str) -> float:
        return self.evaluate_postfix(self.infix_to_postfix(self.tokenize_equation_str(equation)))

def main(): 
    e = ExpressionEval()
    print(e.solve(sys.argv[1].strip().replace(" ", "")))

if __name__ == "__main__":
    main()
