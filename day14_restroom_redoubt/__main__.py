import argparse
import re
import math

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='find_easter_egg', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day14_restroom_redoubt/input.{'test' if args.test else 'prd'}") as f:
        lines = [f.strip() for f in f.readlines()]
    return lines

class Robot:

    def __init__(self, config, grid):
        x, y, vx, vy = re.findall(r"-?\d+", config)
        self.x = int(x)
        self.y = int(y)
        self.vx = int(vx)
        self.vy = int(vy)
        self.grid = grid
        self.mx = len(grid[0])
        self.my = len(grid)

    def poll(self):
        self.x = (self.x + self.vx) % self.mx
        self.y = (self.y + self.vy) % self.my

    def check_quadrant(self):
        tx = self.mx//2
        ty = self.my//2
        if 0 <= self.x < tx and 0 <= self.y < ty:
            return "topleft"
        elif tx < self.x and 0 <= self.y < ty:
            return "topright"
        elif 0 <= self.x < tx and ty < self.y:
            return "botleft"
        elif tx < self.x and ty < self.y:
            return "botright"
        else:
            return None
        
    def __repr__(self):
        return f"Robot(position=({self.x}, {self.y}), q={self.check_quadrant()}, velocity({self.vx}, {self.vy}))"
    
def print_grid(grid, robots):
    for y, line in enumerate(grid):
        for x, _ in enumerate(line):
            if any((robot.x, robot.y) == (x, y) for robot in robots):
                print("X", end='')
            else:
                print(" ", end='')
        print()

def potentially_has_top_of_christmas_tree(robots):
    """
    top of christmas tree would probably look like:
        .
       ...
      .....
      
    somewhere in the grid
    """
    robot_positions = [
        (robot.x, robot.y) for robot in robots
    ]
    for robot in robots:
        if (
            (robot.x - 1, robot.y + 1) in robot_positions and
            (robot.x + 0, robot.y + 1) in robot_positions and
            (robot.x + 1, robot.y + 1) in robot_positions and
            (robot.x - 2, robot.y + 2) in robot_positions and
            (robot.x - 1, robot.y + 2) in robot_positions and 
            (robot.x + 0, robot.y + 2) in robot_positions and
            (robot.x + 1, robot.y + 2) in robot_positions and
            (robot.x + 2, robot.y + 2) in robot_positions
        ):
            return True
    return False

def solve2():
    robots = read_input()
    if args.test:
        grid = [list(range(11)) for _ in range(7)]
    else:
        grid = [list(range(101)) for _ in range(103)]
    robots = [Robot(r, grid) for r in robots]
    second = 0
    while True:
        second += 1
        for robot in robots:
            robot.poll()
        if potentially_has_top_of_christmas_tree(robots):
            print_grid(grid, robots)
            print(second)
            if "y" in input("[y/n] do you see a christmas tree? :)").lower():
                print(second)
                exit()

def solve1():
    robots = read_input()
    if args.test:
        grid = [list(range(11)) for _ in range(7)]
    else:
        grid = [list(range(101)) for _ in range(103)]
    robots = [Robot(r, grid) for r in robots]
    for second in range(100):
        for robot in robots:
            robot.poll()
    
    quadrants = {}
    for robot in robots:
        quadrant = robot.check_quadrant()
        if quadrant not in quadrants:
            quadrants[quadrant] = 0
        quadrants[quadrant] += 1
    del quadrants[None]
    print(math.prod(quadrants.values()))
        

if __name__ == "__main__":
    if args.find_easter_egg:
        solve2()
    else:
        solve1()