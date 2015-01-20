#!/usr/bin/python

import sys
import argparse
import functools, operator
from threading import Thread

from shapes import shapes
import rotation
import problems
import verbose

problems = problems.load()

def move(shape, position, orientation):
    """
    Rotate a shape into an orientation, then move it to a position. Return the
    new shape.
    """
    placed_shape = []

    for point in shape:
        rotated_point = orientation.rotate(point)
        placed_shape.append((rotated_point[0] + position[0], rotated_point[1] + position[1], rotated_point[2] + position[2]))

    return placed_shape


def check(shape, problem):
    """
    Check if all points of the shape are contained in problem.
    """
    return all([ point in problem for point in shape ])


def add(shape, solution):
    """
    Adds all points of the shape to the solution if they are not already
    contained.

    Returns True if all points could be added or False otherwise
    """
    if any([ point in solution for point in shape ]):
        return False

    for point in shape:
        solution.append(point)

    return True


def remove(shape, solution):
    """
    Removes all points of the shape from the solution.
    """
    for point in shape:
        solution.remove(point)


def place_shapes(problem):
    """
    Permutates all shapes into all orientations and moves them to all positions
    of the problem.

    Then it checks whether the resulting shape is even in the solution (to make
    things easier later).
    """
    placed_shapes = []

    orientations = rotation.get_all_orientations()
    positions = problem

    for shape_index in range(len(shapes)):

        placed_shapes.append([])

        for orientation in orientations:
            for position in positions:

                shape = move(shapes[shape_index], position, orientation)
                shape.sort()

                if shape in placed_shapes[shape_index]:
                    continue

                if check(shape, problem):
                    placed_shapes[shape_index].append(shape)

    return placed_shapes


def optimize_placed_shapes(placed_shapes):
    """
    Optimizes how the placed shapes are ordered.
    """

    """
    The solving algorithm skips variations of placed shapes as soon as
    collisions appear.

    Therefore it is beneficial to maximise the number of permutations that will
    be skipped.

    This is done by sorting the shapes in ascending order based on how many
    valid placements in the solution exist.
    """
    placed_shapes.sort(key = lambda x: len(x))

    """
    To sort the placed / oriented variations of a shape more efficiently, try
    to divine which one is most probably placed correctly.

    The following metric is used:
    - Find out which points of the problem are covered by how many placed shapes.
    - Prefer shapes that contain rare points (on average).
    """
    heat_map = {}
    for i in range(len(placed_shapes)):
        for shape in placed_shapes[i]:
            for point in shape:
                if not point in heat_map.keys():
                    heat_map[point] = 1
                else:
                    heat_map[point] += 1

    for i in range(len(placed_shapes)):
        placed_shapes[i].sort(key = lambda shape: float(sum([ heat_map[point] for point in shape ])) / float(len(shape)))


class Solver:
    def __init__(self, problem, complete=False, slices=1, slice=0):
        self.problem = problem
        self.verbose = verbose
        self.complete = complete
        self.done = False

        self.problem.sort()
        assert len(problem) == sum([ len(shape) for shape in shapes ]), "Invalid problem length."

        self.solutions = []

        self.placed_shapes = place_shapes(problem)
        optimize_placed_shapes(self.placed_shapes)

        self.placed_shapes[0] = [ x for i, x in enumerate(self.placed_shapes[0]) if i % slices == slice ]

        self.progress_current = 0
        self.progress_total = functools.reduce(operator.mul, [ len(p) for p in self.placed_shapes ], 1)

        # First will stay 0 because it can never fail
        self.progress_offset = [ 0, 0, 0, 0, 0, 0, 0 ]
        for i in range(1, len(self.placed_shapes) - 1):
            self.progress_offset[i] = functools.reduce(operator.mul, [ len(p) for p in self.placed_shapes[i+1:] ], 1)
        self.progress_offset[-1] = 1


    def solve(self):
        self._solve(0, [], [])
        self.done = True


    def _solve(self, shape_index, solution, parts):
        if shape_index == len(self.placed_shapes):
            solution.sort()
            assert len(self.problem) == len(solution)
            assert solution == self.problem
            self.solutions.append(parts)
            return not self.complete

        for shape in self.placed_shapes[shape_index]:
            if not add(shape, solution):
                self.progress_current += self.progress_offset[shape_index]
                continue

            if shape_index == 6:
                self.progress_current += 1

            parts.append(shape)

            if self._solve(shape_index + 1, solution, parts):
                return True
            else:
                parts.remove(shape)
                remove(shape, solution)

        return False



if __name__ != "__main__":
    sys.exit()

parser = argparse.ArgumentParser(description="Kloetze algorithm.")
parser.add_argument("-p", "--problem")
parser.add_argument("-a", "--all", action="store_true", help="Solve all problems starting with the given one.")
parser.add_argument("-c", "--complete", action="store_true", help="Find all solutions.")
parser.add_argument("-l", "--list", action="store_true", help="List problems.")
parser.add_argument("-v", "--verbose", action="store_true", help="Show progress (slower).")
parser.add_argument("-j", "--javascript", action="store_true", help="Generate java script arrays for solutions")

args = parser.parse_args()

if args.list:
    for i, p in enumerate(problems):
        s = Solver(p)
        print("{}:    {}".format(i, s.progress_total))
    sys.exit()

if args.problem == None:
    print("Specify problem to work on. (0-{})".format(len(problems) - 1))
    sys.exit()

problem = int(args.problem)

assert problem >= 0 and problem < len(problems), "-p or --problem out of range"

if args.all:
    problem_range = range(problem, len(problems))
else:
    problem_range = range(problem, problem + 1)

solvers = []
for p in problem_range:
    solvers.append(Solver(problems[p], complete = args.complete))

for p, solver in enumerate(solvers):
    if args.verbose and len(problem_range) > 1:
        print("Problem {}".format(p))

    try:
        if args.verbose and args.complete:
            t = Thread(target = verbose.output, args = (solver, ))
            t.start()

        solver.solve()

        if args.verbose and args.complete:
            t.join()

    except KeyboardInterrupt:
        if args.verbose and args.complete:
            solver.done = True
            t.join()
        print("")
        sys.exit()

    if args.verbose and args.complete:
        print("")

if args.javascript:
    import json
    with open("../js/solutions.js", "w") as f:
        solutions = [ s.solutions[0] for s in solvers ]
        f.write("solutions =")
        f.write(json.dumps(solutions))
        f.write(";")

    with open("../js/problems.js", "w") as f:
        f.write("problems =")
        f.write(json.dumps(problems))
        f.write(";")

