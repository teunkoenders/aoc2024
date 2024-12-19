import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='resize_warehouse', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day15_warehouse_woes/input.{'test' if args.test else 'prd'}") as f:
        content = f.read()
        grid, instructions = content.split('\n\n')

        grid = [[token for token in line.strip()] for line in grid.split('\n')]
        instructions = [token for line in instructions.split('\n') for token in line]
    return grid, instructions

class Position:

    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
    
    @property
    def position(self):
        return self.x, self.y
    
    def move(self, direction):
        pass

    def try_to_move(self, direction):
        pass

    def __repr__(self):
        return f"{self.TOKEN}"
    
class Free(Position):
    TOKEN = "."

class Wall(Position):
    TOKEN = "#"
    def move(self, direction):
        assert False, "Cannot move wall"
    def try_to_move(self, direction):
        assert False, "Cannot move wall"

class MovableObject(Position):
    def try_to_move(self, direction):
        ox, oy = direction
        self.grid[self.y + oy][self.x + ox].try_to_move(direction)
        
    def move(self, direction):
        ox, oy = direction
        self.grid[self.y + oy][self.x + ox].move(direction)
        px = self.x
        py = self.y
        self.x = self.x + ox
        self.y = self.y + oy
        self.grid[self.y][self.x] = self
        self.grid[py][px] = Free(px, py, self.grid)

class Box(MovableObject):
    TOKEN = "O"

    def gps_coordinates(self):
        return self.y * 100 + self.x

    
class LeftHalfBox(MovableObject):
    TOKEN = "["

    def gps_coordinates(self):
        return self.y * 100 + self.x
    
    def try_to_move(self, direction, flag_to_prevent_recursion=False):
        if not flag_to_prevent_recursion and direction in ((0, -1), (0, +1)):
            self.grid[self.y][self.x + 1].try_to_move(direction, flag_to_prevent_recursion=True)
        return super().try_to_move(direction)

    def move(self, direction, flag_to_prevent_recursion=False):
        if not flag_to_prevent_recursion and direction in ((0, -1), (0, +1)):
            self.grid[self.y][self.x + 1].move(direction, flag_to_prevent_recursion=True)
        return super().move(direction)
    
class RightHalfBox(MovableObject):
    TOKEN = "]"

    def try_to_move(self, direction, flag_to_prevent_recursion=False):
        if not flag_to_prevent_recursion and direction in ((0, -1), (0, +1)):
            self.grid[self.y][self.x - 1].try_to_move(direction, flag_to_prevent_recursion=True)
        return super().try_to_move(direction)
    
    def move(self, direction, flag_to_prevent_recursion=False):
        if not flag_to_prevent_recursion and direction in ((0, -1), (0, +1)):
            self.grid[self.y][self.x - 1].move(direction, flag_to_prevent_recursion=True)
        return super().move(direction)
    
class Robot(MovableObject):
    TOKEN = "@"

    def move(self, direction):
        instruction_to_direction_mapping = {
            "^": ( 0,-1),
            ">": (+1, 0),
            "v": ( 0,+1),
            "<": (-1, 0),
        }
        try:
            super().try_to_move(instruction_to_direction_mapping[direction])
            super().move(instruction_to_direction_mapping[direction])
        except AssertionError:
            pass


def parse_grid_and_find_robot(grid):
    robot = None
    tmp = []
    for y, line in enumerate(grid):
        horizontal = []
        for x, token in enumerate(line):
            token2object_mapping = {
                Wall.TOKEN: Wall,
                Box.TOKEN: Box,
                Free.TOKEN: Free,
                Robot.TOKEN: Robot
            }
            obj = token2object_mapping[token](x, y, tmp)
            horizontal.append(obj)
            if token == Robot.TOKEN:
                robot = obj
        tmp.append(horizontal)
    return robot

def parse_fat_grid_and_find_robot(grid):
    robot = None
    tmp = []
    for y, line in enumerate(grid):
        horizontal = []
        for x, token in enumerate(line):
            token2object_mapping = {
                Wall.TOKEN: [Wall, Wall],
                Box.TOKEN: [LeftHalfBox, RightHalfBox],
                Free.TOKEN: [Free, Free],
                Robot.TOKEN: [Robot, Free]
            }
            cls1, cls2 = token2object_mapping[token]
            obj1 = cls1(x*2, y, tmp)
            obj2 = cls2(x*2+1, y, tmp)
            horizontal.extend([obj1, obj2])
            if token == Robot.TOKEN:
                robot = obj1
        tmp.append(horizontal)
    return robot

def solve1():
    grid, instructions = read_input()
    robot: Robot = parse_grid_and_find_robot(grid)

    for instruction in instructions:
        robot.move(instruction)

    gps_sum = 0
    for line in robot.grid:
        for object in line:
            if isinstance(object, Box):
                gps_sum += object.gps_coordinates()

    print(gps_sum)

def solve2():
    grid, instructions = read_input()
    robot: Robot = parse_fat_grid_and_find_robot(grid)

    for index, instruction in enumerate(instructions):
        robot.move(instruction)

    gps_sum = 0
    for line in robot.grid:
        for object in line:
            if isinstance(object, LeftHalfBox):
                gps_sum += object.gps_coordinates()

    for line in robot.grid:
        for object in line:
            print(object.TOKEN, end="")
        print()
    print(gps_sum)

if __name__ == "__main__":
    if args.resize_warehouse:
        solve2()
    else:
        solve1()