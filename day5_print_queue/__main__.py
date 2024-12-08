import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--solve_incorrect_ordering', '-2', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day5_print_queue/input.{'test' if args.test else 'prd'}") as f:
        lines = [line.strip() for line in f.readlines()]

    before_map = {}
    updates = []
    for line in lines:
        if "|" in line:
            before, after = map(int, line.split("|"))
            if after not in before_map:
                before_map[after] = set()
            before_map[after].add(before)

        elif "," in line:
            updates.append(list(map(int, line.split(','))))
    
    return before_map, updates


def get_middle_number_from_update(update):
    return update[int((len(update)-1)/2)]

def assert_valid_update(rules, update):
    for index, number in enumerate(update):
        rule = rules.get(number, set())
        seen = set(update[:index])
        missed = seen.difference(rule)
        assert not missed

def fix_update(rules, update):
    tmp = []
    for number in update:
        rule = rules.get(number, set())
        where_to_set = 0
        for index, curr in enumerate(tmp, start=1):
            if curr in rule:
                where_to_set = index
        tmp.insert(where_to_set, number)
    return tmp

def solve():
    tmp = 0
    rules, updates = read_input()
    for update in updates:
        try:
            assert_valid_update(rules, update)
            tmp += get_middle_number_from_update(update)
        except AssertionError:
            pass
    print(tmp)


def solve2():
    tmp = 0
    rules, updates = read_input()
    for update in updates:
        try:
            assert_valid_update(rules, update)
        except AssertionError:
            new_update = fix_update(rules, update)
            tmp += get_middle_number_from_update(new_update)
    
    print(tmp)

if __name__ == "__main__":
    if args.solve_incorrect_ordering:
        solve2()
    else: 
        solve()