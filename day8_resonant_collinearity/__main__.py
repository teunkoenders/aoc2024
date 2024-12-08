import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='take_into_account_resonant_harmonics', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day8_resonant_collinearity/input.{'test' if args.test else 'prd'}") as f:
        grid = [[token for token in line.strip()] for line in f.readlines()]
    return grid

def find_antenna_locations(grid):
    antennas = {}
    for y, line in enumerate(grid):
        for x, antenna_type in enumerate(line):
            if antenna_type not in antennas:
                antennas[antenna_type] = []
            antennas[antenna_type].append((x, y))
    del antennas["."]
    return antennas

def find_potential_antinode_locations(grid, antenna_locations):
    antinode_locations = []
    max_x, max_y = len(grid[0]), len(grid)
    for location in antenna_locations:
        other_locations = antenna_locations.copy()
        other_locations.remove(location)
        for other_location in other_locations:
            offset_antinode_x = (other_location[0] - location[0])*-1
            offset_antinode_y = (other_location[1] - location[1])*-1
            antinode_x = location[0] + offset_antinode_x
            antinode_y = location[1] + offset_antinode_y
            if args.take_into_account_resonant_harmonics:
                while max_x > antinode_x >= 0 and max_y > antinode_y >= 0:
                    antinode_locations.append((antinode_x, antinode_y))
                    if grid[antinode_y][antinode_x] == ".":
                        grid[antinode_y][antinode_x] = "#"
                    antinode_x = antinode_x + offset_antinode_x
                    antinode_y = antinode_y + offset_antinode_y
            else:
                if max_x > antinode_x >= 0 and max_y > antinode_y >= 0:
                    antinode_locations.append((antinode_x, antinode_y))
                    grid[antinode_y][antinode_x] = "#"
    return antinode_locations

def solve():
    grid = read_input()
    antennas = find_antenna_locations(grid)
    antinodes = []
    for _, antenna_locations in antennas.items():
        antinodes.extend(find_potential_antinode_locations(grid, antenna_locations))
        if args.take_into_account_resonant_harmonics:
            antinodes.extend(antenna_locations)
    print(len(set(antinodes)))

if __name__ == "__main__":
    solve()