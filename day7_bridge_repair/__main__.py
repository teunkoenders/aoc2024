import argparse
import itertools

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='pretty_slow_but_works_concatenation_operation', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day7_bridge_repair/input.{'test' if args.test else 'prd'}") as f:
        return f.readlines()

def parse_equation(equation):
    answer, tokens = equation.split(":")
    return int(answer.strip()), [int(nr) for nr in tokens.strip().split(" ")]

def can_create_answer(answer, tokens):
    operationstr2lambda = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y
    }
    if args.pretty_slow_but_works_concatenation_operation:
        operationstr2lambda['|'] = lambda x, y: int(f"{x}{y}")

    possible_operations = itertools.product(operationstr2lambda.keys(), repeat=(len(tokens)-1))
    for operations in possible_operations:
        tmp = tokens[0]
        for operation, next_token in zip(operations, tokens[1:]):
            tmp = operationstr2lambda[operation](tmp, next_token)
        if tmp == answer:
            return answer
    assert False


def solve():
    sum_of_correct_answers = 0
    equations = read_input()
    for equation in equations:
        answer, tokens = parse_equation(equation)
        try:
            sum_of_correct_answers += can_create_answer(answer, tokens)
        except AssertionError:
            pass

    print(sum_of_correct_answers)

if __name__ == "__main__":
    solve()