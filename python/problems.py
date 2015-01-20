import json

def convert(problem):
    points = []

    for x, line in enumerate(problem):
        ys = [ tmp for tmp in line.split("/") if len(tmp) > 0 ]
        for y, zs in enumerate(reversed(ys)):
            for z in range(len(zs)):
                if not zs[z] in [".", "0", "-"]:
                    points.append((x, y, z))

    assert len(points) == 27
    return points

def load():
    problems = []

    with open("soma.db", "r") as f:
        lines = [ l.strip() for l in f.readlines() ]

    problem = None
    for line in lines:
        if problem == None and len(line) == 0:
            continue

        if line.startswith(";"):
            continue

        if problem == None and len(line) > 0:
            problem = []
            continue

        if len(line) == 0 and len(problem) > 0:
            problems.append(convert(problem))
            problem = None
            continue

        if problem != None and len(line) > 0:
            problem.append(line)

    return problems

