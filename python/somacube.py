#!/usr/bin/python

import sys
import argparse
from threading import Thread

import problems
from solver import Solver

if __name__ != "__main__":
    sys.exit()

parser = argparse.ArgumentParser(description="Kloetze algorithm.")
parser.add_argument("-p", "--problem")
parser.add_argument("-a", "--all", action="store_true", help="Solve all problems starting with the given one.")
parser.add_argument("-c", "--complete", action="store_true", help="Find all solutions.")
parser.add_argument("-j", "--javascript", action="store_true", help="Generate java script arrays for solutions")
parser.add_argument("-m", "--multicore", action="store_true", help="Use parallel execution on all cores.")

args = parser.parse_args()

problems = problems.load()

if args.problem == None:
    print("Specify problem to work on. (0-{})".format(len(problems) - 1))
    sys.exit()

problem = int(args.problem)

assert problem >= 0 and problem < len(problems), "-p or --problem out of range"

if args.all:
    problem_range = range(problem, len(problems))
else:
    problem_range = range(problem, problem + 1)

solutions = []

if args.multicore:
    # TODO: See what happens on systems where zmq is not installed.
    import parallel_solver

try:
    for p in problem_range:
        print("Solving problem {}".format(p))

        if not args.multicore:
            solver = Solver(problems[p], complete=args.complete)
            solutions.append(solver.solve())
        else:
            solutions.append(parallel_solver.solve(problems[p], args.complete))

except:
    raise

finally:
    if args.multicore:
        parallel_solver.quit()

print("")

if args.javascript:
    import json
    with open("../js/solutions.js", "w") as f:
        f.write("solutions =")
        f.write(json.dumps(solutions))
        f.write(";")

    with open("../js/problems.js", "w") as f:
        f.write("problems =")
        f.write(json.dumps(problems))
        f.write(";")

