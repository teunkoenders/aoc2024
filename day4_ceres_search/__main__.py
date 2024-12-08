import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t', action='store_true')
    parser.add_argument('--cross_mas', '-2', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day4_ceres_search/input.{'test' if args.test else 'prd'}") as f:
        grid = [[token for token in line.strip()] for line in f.readlines()]
    return grid

UP =    ( 0, -1)
RIGHT = (+1,  0)
DOWN =  ( 0, +1)
LEFT =  (-1,  0)

all_directions = [
    (UP,),
    (UP, RIGHT,),
    (RIGHT,),
    (DOWN, RIGHT),
    (DOWN,),
    (DOWN, LEFT),
    (LEFT,),
    (UP, LEFT),
]

all_cross_mas_directions = [
    (UP, RIGHT,),
    (DOWN, RIGHT),
    (DOWN, LEFT),
    (UP, LEFT),
]

def search_word_in_grid_in_direction(grid, start_x, start_y, word, direction):
    offset_x, offset_y = direction
    try: 
        assert start_x >= 0 and start_y >= 0
        assert grid[start_y][start_x] == word[0]
        if word[1:]:
            return search_word_in_grid_in_direction(grid, start_x+offset_x, start_y+offset_y, word[1:], direction)
        else: 
            return True
    except (AssertionError, IndexError):
        return False

def solve():
    total_xmasses = 0
    grid = read_input()
    
    for y, line in enumerate(grid):
        for x, token in enumerate(line):
            if token == "X":
                for directions in all_directions:
                    direction = tuple(sum(ax) for ax in zip(*directions))
                    total_xmasses += 1 if search_word_in_grid_in_direction(grid, x, y, list("XMAS"), direction) else 0

    print(total_xmasses)


def solve2():
    total_crossmasses = 0
    grid = read_input()
    
    for y, line in enumerate(grid):
        for x, token in enumerate(line):
            if token == "M":
                for directions in all_cross_mas_directions:
                    direction = tuple(sum(ax) for ax in zip(*directions))
                    offset_x, offset_y = direction
                    first_mas_found = search_word_in_grid_in_direction(grid, x, y, list("MAS"), direction)
                    second_mas_found = search_word_in_grid_in_direction(grid, x + (offset_x*2), y, list("MAS"), (offset_x*-1, offset_y))
                    reverse_second_mas_found = search_word_in_grid_in_direction(grid, x, y + (offset_y*2), list("MAS"), (offset_x, offset_y*-1))
                    total_crossmasses += 1 if first_mas_found and (second_mas_found or reverse_second_mas_found) else 0

    print(total_crossmasses/2)

if __name__ == "__main__":
    if args.cross_mas:
        solve2()
    else:
        solve()