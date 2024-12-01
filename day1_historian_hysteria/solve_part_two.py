from day1_historian_hysteria.lib import read_input

def solve(left, right):
    similarity_score = 0
    for l in left:
        similarity_score += (l * right.count(l))
    return similarity_score

def main():
    left, right = read_input()

    left = sorted(left)
    right = sorted(right)
    solution = solve(left, right)
    print(solution)

if __name__ == "__main__":
    main()