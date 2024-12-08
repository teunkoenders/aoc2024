import argparse
import copy

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--add_obstacles', '-2', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day6_guard_gallivant/input.{'test' if args.test else 'prd'}") as f:
        grid = [[token for token in line.strip()] for line in f.readlines()]
    return grid

def find_guard_starting_location(grid):
    for y, line in enumerate(grid):
        for x, token in enumerate(line):
            if token == "^":
                return (x, y)

def will_walk_into_obstacle(grid, x, y, direction): 
    offset_x, offset_y = direction
    if not (y + offset_y >= 0 and x + offset_x >= 0):
        raise IndexError()
    return grid[y + offset_y][x + offset_x] == "#" # will raise IndexError if at end of protocol

UP =    (0, -1)
RIGHT = (+1, 0)
DOWN =  (0, +1)
LEFT =  (-1, 0)

directions = [
    UP, RIGHT, DOWN, LEFT
]

def execute_lab_guard_1518_walk_protocol(x, y, grid):
    seen_positions = set()
    seen_positions_with_direction = set()
    current_direction = 0
    try:
        while True:
            seen_positions.add((x, y))
            direction = directions[current_direction % len(directions)]
            offset_x, offset_y = direction
            seen_positions_with_direction.add((x, y, direction))

            if will_walk_into_obstacle(grid, x, y, direction):
                current_direction += 1
            else:
                x = x + offset_x
                y = y + offset_y
                assert (x, y, direction) not in seen_positions_with_direction
    except IndexError:
        return seen_positions

def solve():
    grid = read_input()
    starting_position = find_guard_starting_location(grid)
    x, y = starting_position
    positions = execute_lab_guard_1518_walk_protocol(x, y, grid)
    print(len(positions))

def horribly_slow_bruteforce_solution2():
    amount_of_loops_found = 0
    grid = read_input()
    starting_position = find_guard_starting_location(grid)
    x, y = starting_position
    positions = execute_lab_guard_1518_walk_protocol(x, y, grid)
    positions.remove((x, y))

    for potential_obstacle_x, potential_obstacle_y in positions:
        new_grid = copy.deepcopy(grid)
        new_grid[potential_obstacle_y][potential_obstacle_x] = "#"
        try:
            execute_lab_guard_1518_walk_protocol(x, y, new_grid)
        except AssertionError:
            amount_of_loops_found += 1
    
    print(amount_of_loops_found)

if __name__ == "__main__":
    if args.add_obstacles:
        horribly_slow_bruteforce_solution2()
    else: 
        solve()