import readline
import math
import state
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

def create_prompt_string(line_count: int):
    pre_linecount_string = " "*(2 - math.floor(math.log(line_count, 10)))
    return f"{pre_linecount_string}{line_count}> "

def main():
    print("   | The last result can be accessed with the variable 'r'.\n   | Type 'quit' to exit the program.")
    exp_eval = ExpressionEval()
    line_count = 1
    cur_input = ""

    while 1:
        prompt_string = create_prompt_string(line_count)
        cur_input = input(prompt_string).strip()
        cur_input = cur_input.replace(" ", "")

        # special actions etc.
        # future work, not concerned with for now.
        if not is_expression_string(cur_input):
            cur_input_args = cur_input.split(' ')
            command = Action[cur_input_args[0].upper()]

            if command == Action.QUIT:
                break

        # if the current input is a normal mathematical expression to evaluate
        else:
            var_to_write_to = "r"
            if "=" in cur_input:
                temp = cur_input.split("=")
                var_to_write_to = temp[0]
                cur_input = temp[1]

            result = exp_eval.solve(cur_input)
            state.result_history.append(result)
            state.user_vars[var_to_write_to] = str(result)
            print(f"   | {result}")

        line_count += 1

if __name__ == "__main__":
    main()
