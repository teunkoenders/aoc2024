import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='this_will_take_a_long_time_if_i_do_slow_blink', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day11_plutonian_pebbles/input.{'test' if args.test else 'prd'}") as f:
        pebbles = f.read().strip().split(" ")
    return pebbles

def blink(pebbles: list):
    tmp = []
    while pebble := pebbles.pop(0):
        if pebble == "0":
            tmp.append("1")
        else:
            quotient, remainder = divmod(len(pebble), 2)
            if remainder == 0:
                tmp.append(pebble[:quotient].lstrip("0") or "0")
                tmp.append(pebble[quotient:].lstrip("0") or "0")
            else:
                tmp.append(f"{int(pebble) * 2024}")
    
        if not pebbles:
            return tmp

def solve1():
    pebbles = read_input()
    unique_pebbles = set()

    for index in range(25):
        print(f"start blink #{index}")
        before = time.time()
        before_count = len(pebbles)
        pebbles = blink(pebbles)
        unique_pebbles.update(set(pebbles))
        print(len(unique_pebbles))
        print(f"current amount of pebbles ({len(pebbles)}, ({len(pebbles) / before_count}))")
        print(f"blinking took {time.time() - before:.2f}s")
    
    print(len(pebbles))

pebbles_found = {}

def smarter_blink(pebble, times):
    if times == 0:
        return 1

    if (pebble, times) in pebbles_found:
        return pebbles_found[(pebble, times)]

    if pebble == "0":
        size = smarter_blink("1", times - 1)
    else:
        quotient, remainder = divmod(len(pebble), 2)
        if remainder == 0:
            left = pebble[:quotient].lstrip("0") or "0"
            right = pebble[quotient:].lstrip("0") or "0"
            size = smarter_blink(left, times - 1) + smarter_blink(right, times - 1)
        else:
            size = smarter_blink(f"{int(pebble) * 2024}", times - 1)

    if (pebble, times) not in pebbles_found:
        pebbles_found[(pebble, times)] = size

    return size

def solve2():
    pebbles = read_input()
    count = 0
    for pebble in pebbles: 
        count += smarter_blink(pebble, 75)
    print(count)

if __name__ == "__main__":
    if  args.this_will_take_a_long_time_if_i_do_slow_blink:
        solve2()
    else:
        solve1()