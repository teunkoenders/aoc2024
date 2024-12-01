from day1_historian_hysteria.lib import read_input

def solve(left, right):
    total_distance = 0
    for l, r in zip(left, right):
        total_distance += abs(l - r) 
    return total_distance

def main():
    left, right = read_input()

    left = sorted(left)
    right = sorted(right)

    solution = solve(left, right)
    print(solution)

if __name__ == "__main__":
    main()