import readline
import math
from enum import Enum

from expression_eval import ExpressionEval

class Action(Enum):
    QUIT = 1
    SET = 2

def is_expression_string(input_string: str):
    result = True
    first_word = input_string.split(' ')[0]
    action_names = [x.name.lower() for x in list(Action)]

    if first_word in action_names:
        result = False

    return result

def create_prompt_string(line_count: int, prev_result: str):
    pre_linecount_string = " "*(2 - math.floor(math.log(line_count, 10)))
    return f"{pre_linecount_string}{line_count}> {prev_result}"

def main():
    exp_eval = ExpressionEval()
    line_count = 1
    cur_input = ""
    result_string = ""

    while 1:
        prompt_string = create_prompt_string(line_count, result_string)
        cur_input = input(prompt_string).strip()

        # special actions etc.
        # future work, not concerned with for now.
        if not is_expression_string(cur_input):
            cur_input_args = cur_input.split(' ')
            command = Action[cur_input_args[0].upper()]

            if command == Action.QUIT:
                break

        # if the current input is a normal mathematical expression to evaluate
        else:
            result = exp_eval.solve(cur_input)
            result_string = str(result)
            print(result)

        line_count += 1

if __name__ == "__main__":
    main()
