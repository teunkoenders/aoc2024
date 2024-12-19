import argparse
import re
import itertools

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='test', action='store_true')
    parser.add_argument('-2', dest='fix_machine_conversion_error', action='store_true')
    return parser.parse_args()

args = parse_args()

def read_input():
    with open(f"day13_claw_contraption/input.{'test' if args.test else 'prd'}") as f:
        string = f.read().strip()
    return string

class Solution:

    def __init__(self, clawmachine: 'ClawMachine', times_a, times_b):
        self.clawmachine = clawmachine
        self.xa = times_a
        self.xb = times_b
        self._solve()

    def _solve(self):
        x = self.xa * self.clawmachine.a[0]
        y = self.xa * self.clawmachine.a[1]

        x += self.xb * self.clawmachine.b[0]
        y += self.xb * self.clawmachine.b[1]

        self.is_above_prize = (x, y) == self.clawmachine.p
        self.cost = (self.xa * 3) + (self.xb * 1)

    def is_valid_solution(self):
        return self.is_above_prize

    def is_better_solution_than(self, other_solution: 'Solution'):
        return self.cost < other_solution.cost
    
    def __repr__(self):
        return f"Solution(xa={self.xa}, xb={self.xb}, tokens={self.cost}, prize={self.clawmachine.p})"

class ClawMachine:

    def __init__(self, button_a, button_b, prize):
        self.a = button_a
        self.b = button_b
        self.p = prize
        self.solutions = []
        if True:
            self.best_solution = self._solve_using_algebra()
        else:
            self.best_solution = self._solve()

    def _solve(self):
        best_solution = None
        if not args.fix_machine_conversion_error:
            product = itertools.product(range(1, 100), repeat=2)
        for press_a, press_b in product:
            solution = Solution(self, press_a, press_b)
            if solution.is_valid_solution():
                self.solutions.append(solution)
                if not best_solution:
                    best_solution = solution
                elif solution.is_better_solution_than(best_solution):
                    best_solution = solution
        return best_solution
    
    def _solve_using_algebra(self):
        """
        Ax * Ac + Bx * Bc = Px
        Ay * Ac + By * Bc = Py

        Isolate Ac, Where Ac =

        AxByAc + BxByBc = PxBy
        AyBxAc + ByBxBc = PyBx
        ===
        AxByAc - AyBxAc = PxBy - PyBx
        ===
        Ac(AxBy - AyBx) = PxBy - PyBx
        ===
        Ac = PxBy - PyBx / AxBy - AyBx
        
        And Bc =

        AxAc + BxBc = Px
        ===
        BxBc = Px - AxAc
        ===
        Bc = (Px - AxAc) / Bx
        """
        ca = (self.p[0] * self.b[1] - self.p[1] * self.b[0]) / (self.a[0] * self.b[1] - self.a[1] * self.b[0])
        cb = (self.p[0] - self.a[0] * ca) / self.b[0]
        if ca % 1 == 0 and cb % 1 == 0:
            return Solution(self, ca, cb)

    def __repr__(self):
        return f"ClawMachine(a={self.a}, b={self.b}, prize={self.p}, solutions={len(self.solutions)})"

def parse_configurations_to_clawmachines(configurations):
    machines = []
    for ax, ay, bx, by, px, py in re.findall(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)", configurations):
        if args.fix_machine_conversion_error:
            px = int(px) + 10000000000000
            py = int(py) + 10000000000000
        
        machines.append(
            ClawMachine(
                (int(ax), int(ay)),
                (int(bx), int(by)),
                (int(px), int(py))
            )
        )
    return machines

def solve1():
    claw_machine_configurations = read_input()
    claw_machines = parse_configurations_to_clawmachines(claw_machine_configurations)
    tokens = 0
    for machine in claw_machines:
        if machine.best_solution:
            tokens += machine.best_solution.cost
    print(int(tokens))

if __name__ == "__main__":
    solve1()