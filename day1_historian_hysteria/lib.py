def read_input():
    FILE = "day1_historian_hysteria/input"
    with open(FILE) as f: 
        lines = [line.split(maxsplit=1) for line in f.readlines()]
    left, right = zip(*lines)
    return map(int, left), map(int, right)