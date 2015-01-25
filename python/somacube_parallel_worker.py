import zmq
import time
import json

from solver import Solver

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

sender.send_string("sync")

while True:
    s = receiver.recv()

    task = json.loads(s)

    problem = []
    for point in task["problem"]:
        problem.append((point[0], point[1], point[2]))

    s = Solver(
        problem,
        complete=task["complete"],
        slices=task["slices"],
        slice=task["slice"])

    s.solve()

    sender.send_string(json.dumps(s.solutions))

