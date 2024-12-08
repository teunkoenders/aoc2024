import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--parse_conditional_statements', '-2', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day3_mull_it_over/input.{'test' if args.test else 'prd'}") as f:
        return f.read()
    
MULTIPLICATION_REGEX = r"mul\((\d{1,3}),(\d{1,3})\)"
    
def find_multiplications(memory):
    return re.findall(MULTIPLICATION_REGEX, memory)

def find_conditional_multiplications(memory):
    do_instruction = r"do\(\)"
    dont_instruction = r"don't\(\)"
    matches = list(re.finditer(rf"{do_instruction}|{dont_instruction}|{MULTIPLICATION_REGEX}", memory))

    tmp = []
    instructions_enabled = True
    for match in matches:
        if match.group() == "do()":
            instructions_enabled = True
        elif match.group() == "don't()":
            instructions_enabled = False
        elif instructions_enabled:
            tmp.append((match.group(1), match.group(2)))
    return tmp

def solve():
    corrupted_memory = read_input()
    if args.parse_conditional_statements:
        unjumbled_instructions = find_conditional_multiplications(corrupted_memory)
    else:
        unjumbled_instructions = find_multiplications(corrupted_memory)
    tmp = 0
    for digit1, digit2 in unjumbled_instructions:
        tmp += (int(digit1) * int(digit2))
    
    print(tmp)

if __name__ == "__main__":
    solve()