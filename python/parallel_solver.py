import zmq
import subprocess
import json

CLIENTS = 8


context = zmq.Context()

sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

handles = []
for i in range(CLIENTS):
    handles.append(subprocess.Popen(["python", "parallel_worker.py"]))

syncs = 0
while syncs != CLIENTS:
    s = receiver.recv()
    if s == "sync":
        syncs += 1

print("Successfully started workers on {} cores.".format(CLIENTS))

def solve(problem, complete):
    x = {}
    x["problem"] = problem
    x["complete"] = complete
    x["slices"] = CLIENTS

    clients = 0
    for i in range(CLIENTS):
        x["slice"] = clients
        sender.send_string(json.dumps(x))
        clients += 1

    results = []
    while len(results) != CLIENTS:
        s = receiver.recv()
        results.append(s)

    solutions = []
    for res in results:
        solutions += json.loads(res)

    return solutions

def quit():
    for h in handles:
        h.terminate()

