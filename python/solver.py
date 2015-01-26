
from shapes import shapes
import rotation

def _move(shape, position, orientation):
    """
    Rotate a shape into an orientation, then move it to a position. Return the
    new shape.
    """
    placed_shape = []

    for point in shape:
        rotated_point = orientation.rotate(point)
        placed_shape.append((rotated_point[0] + position[0], rotated_point[1] + position[1], rotated_point[2] + position[2]))

    return placed_shape


def _check(shape, problem):
    """
    Check if all points of the shape are contained in problem.
    """
    return all([ point in problem for point in shape ])


def _add(shape, solution):
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


def _remove(shape, solution):
    """
    Removes all points of the shape from the solution.
    """
    for point in shape:
        solution.remove(point)


def _place_shapes(problem):
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

                shape = _move(shapes[shape_index], position, orientation)

                # This sort is essential (otherwise a lot of symmertries are
                # not found).
                shape.sort()

                if shape in placed_shapes[shape_index]:
                    continue

                if _check(shape, problem):
                    placed_shapes[shape_index].append(shape)

    return placed_shapes


def _optimize_placed_shapes(placed_shapes):
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
        self.complete = complete

        self.problem.sort()
        assert len(problem) == sum([ len(shape) for shape in shapes ]), "Invalid problem length."

        self.solutions = []

        self.placed_shapes = _place_shapes(problem)
        _optimize_placed_shapes(self.placed_shapes)

        self.placed_shapes[0] = [ x for i, x in enumerate(self.placed_shapes[0]) if i % slices == slice ]


    def solve(self):
        self._solve(0, [], [])


    def _solve(self, shape_index, solution, parts):
        if shape_index == len(self.placed_shapes):
            solution.sort()
            assert len(self.problem) == len(solution)
            assert solution == self.problem
            self.solutions.append(parts)
            return not self.complete

        for shape in self.placed_shapes[shape_index]:
            if not _add(shape, solution):
                continue

            parts.append(shape)

            if self._solve(shape_index + 1, solution, parts):
                return True
            else:
                parts.remove(shape)
                _remove(shape, solution)

        return False

