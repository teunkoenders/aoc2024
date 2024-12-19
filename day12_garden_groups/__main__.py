import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='apply_bulk_discount', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day12_garden_groups/input.{'test' if args.test else 'prd'}") as f:
        string = [[token for token in line.strip()] for line in f.readlines()]
    return string

directions = [
    # X, Y
    ( 0,-1), # UP
    ( 1, 0), # RIGHT
    ( 0, 1), # DOWN
    (-1, 0), # LEFT
]

all_directions = [
    (-1,  0), 
    (-1,  1),
    ( 0,  1),
    ( 1,  1),
    ( 1,  0),
    ( 1, -1),
    ( 0, -1),
    (-1, -1),
]

clockwise_directions_mapping = {
    (0,-1): (1,0),
    (1,0):(0,1),
    (0,1):(-1,0),
    (-1,0):(0,-1)
}

other_fence_directions = {
    (0,-1): [(0,0,(1,0)), (1,-1, (-1,0))],
    (1,0):  [(0,0,(0,1)), (1,1,(0,-1))],
    (0,1):  [(0,0,(-1,0)),(-1,1,(1,0))],
    (-1,0): [(0,0,(0,-1)),(-1,-1,(0,1))]
}

class Plot:

    def __init__(self, plant, starting_plant_position):
        self.plant = plant
        self.plant_positions = [starting_plant_position]
        self.processed_fences = []
        self.all_fences = []
        self.sides = 0

    def expand(self, garden, starting_position=None):
        max_y = len(garden)
        max_x = len(garden[0])
        x, y = starting_position or self.plant_positions[0]
        for offset_x, offset_y in directions:
            new_plant_x = x + offset_x
            new_plant_y = y + offset_y
            out_of_garden = new_plant_x < 0 or new_plant_x >= max_x or new_plant_y < 0 or new_plant_y >= max_y
            if not out_of_garden and garden[new_plant_y][new_plant_x] == self.plant and (new_plant_x, new_plant_y) not in self.plant_positions:
                self.plant_positions.append((new_plant_x, new_plant_y))
                self.expand(garden, (new_plant_x, new_plant_y))

    def is_same_plant_type(self, plant):
        return plant == self.plant

    def fence(self, garden):
        max_y = len(garden)
        max_x = len(garden[0])
        fences = []
        for plant in self.plant_positions:
            plantx, planty = plant
            for direction in directions:
                offsetx, offsety = direction
                fencex = plantx + offsetx
                fencey = planty + offsety

                fence_out_of_garden = fencex < 0 or fencex >= max_x or fencey < 0 or fencey >= max_y
                fence_not_at_plant_spot = (fencex, fencey) not in self.plant_positions
                if fence_out_of_garden or fence_not_at_plant_spot and (fencex, fencey, direction) not in fences:
                    fences.append((plantx, planty, direction))
        self.all_fences = fences
        return fences

    @property
    def area(self):
        return len(set(self.plant_positions))
    
    def is_plant_in_plot(self, x, y, plant):
        return self.is_same_plant_type(plant) and (x, y) in self.plant_positions
    
    def __repr__(self):
        return f"Plot('{self.plant}', plants={len(self.plant_positions)})"
    
    def count_sides(self, fence, fences):
        if fence in self.processed_fences:
            if len(self.processed_fences) != len(self.all_fences):
                inner_fences = list(set(fences).difference(set(self.processed_fences)))
                return self.count_sides(inner_fences[0], inner_fences)
            else:
                return self.sides
        self.processed_fences.append(fence)
        fence_x, fence_y = fence[:2]
        fence_direction = fence[2]
        offset_x, offset_y = clockwise_directions_mapping[fence_direction]
        next_fence_x, next_fence_y = (fence_x + offset_x, fence_y + offset_y)
        if (next_fence_x, next_fence_y, fence_direction) in fences:
            self.sides += 0
            return self.count_sides((next_fence_x, next_fence_y, fence_direction), fences)
        else:
            for change_side_x, change_side_y, change_side_dir in other_fence_directions[fence_direction]:
                next_fence = (fence_x + change_side_x, fence_y + change_side_y, change_side_dir)
                if next_fence in fences:
                    self.sides += 1
                    return self.count_sides(next_fence, fences)
  
def is_plant_in_any_plot(plots: list[Plot], x, y, plant):
    for plot in plots:
        if plot.is_plant_in_plot(x, y, plant):
            return True
    return False

def parse_garden_to_plots(garden):
    plots: list[Plot] = []

    for y, line in enumerate(garden):
        for x, plant in enumerate(line):
            if not is_plant_in_any_plot(plots, x, y, plant):
                new_plot = Plot(plant, (x, y))
                new_plot.expand(garden)
                plots.append(new_plot)

    return plots


def solve1():
    garden = read_input()
    plots = parse_garden_to_plots(garden)
    cost = 0
    for plot in plots:
        cost += len(plot.fence(garden)) * plot.area
    
    print(cost)

def solve2():
    garden = read_input()
    plots = parse_garden_to_plots(garden)
    cost = 0
    for plot in plots:
        fences = plot.fence(garden)
        cost += plot.count_sides(fences[0], fences) * plot.area
    
    print(cost)


if __name__ == "__main__":
    if args.apply_bulk_discount:
        solve2()
    else: 
        solve1()