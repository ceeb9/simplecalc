import math
from enum import Enum

class Action(Enum):
    QUIT = 1
    SET = 2

def expand_aliases(input_string: str) -> str:
    aliases = [
        ("^", "**"),
        ("pi", "math.pi"),
        ("sin", "math.sin"),
        ("cos", "math.cos"),
        ("tan", "math.tan"),
    ]
    for f, r in aliases: input_string = input_string.replace(f, r)
    return input_string

def parse_expression_string(input_string: str) -> str:
    return expand_aliases(input_string)

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
    line_count = 1
    cur_input = ""
    result_string = ""

    while 1:
        cur_input = input(create_prompt_string(line_count, result_string)).strip()
        if not is_expression_string(cur_input):
            cur_input_args = cur_input.split(' ')
            command = Action[cur_input_args[0].upper()]

            if command == Action.QUIT:
                break
        else:
            cur_input = parse_expression_string(result_string + cur_input)
            result = eval(cur_input)
            result_string = str(result)
            print(result)

        line_count += 1

if __name__ == "__main__":
    main()
