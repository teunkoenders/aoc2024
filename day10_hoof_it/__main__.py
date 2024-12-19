import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='include_trail_rating', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day10_hoof_it/input.{'test' if args.test else 'prd'}") as f:
        grid = [[token for token in line.strip()] for line in f.readlines()]
    return grid

def find_trailheads(topographic_map):
    tmp = set()
    for y, line in enumerate(topographic_map):
        for x, height in enumerate(line):
            if height == "0":
                tmp.add((x,y))
    return tmp

directions = [
    # X, Y
    ( 0,-1), # UP
    ( 1, 0), # RIGHT
    ( 0, 1), # DOWN
    (-1, 0), # LEFT
]

def recurse_hike_trail(map, starting_point, current_height):
    max_y = len(map)
    max_x = len(map[0])

    if current_height == 9:
        return [starting_point]

    tmp = []
    starting_x, starting_y = starting_point
    for direction in directions:
        offset_x, offset_y = direction
        next_point = (starting_x + offset_x, starting_y + offset_y)
        next_x, next_y = next_point
        if next_x >= 0 and next_x < max_x and next_y >= 0 and next_y < max_y:
            if map[next_y][next_x] == str(current_height + 1):
                tmp.extend(recurse_hike_trail(map, next_point, current_height + 1))
    return tmp

def solve1():
    topographic_map = read_input()
    trailheads = find_trailheads(topographic_map)
    score = 0
    for trailhead in trailheads:
        if args.include_trail_rating:
            valid_trails = recurse_hike_trail(topographic_map, trailhead, 0)
        else:
            valid_trails = set(recurse_hike_trail(topographic_map, trailhead, 0))
        score += len(valid_trails)
    print(score)

if __name__ == "__main__":
    solve1()