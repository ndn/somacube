import zmq
import subprocess
import sys
import json

import problems

CLIENTS = 8

problems = problems.load()

x = {}
x["problem"] = problems[0]
x["complete"] = False
x["slices"] = CLIENTS

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
        print("sync {}".format(syncs + 1))
        syncs += 1

clients = 0
for i in range(CLIENTS):
    x["slice"] = clients
    sender.send_string(json.dumps(x))
    clients += 1

results = []
while len(results) != CLIENTS:
    s = receiver.recv()
    results.append(s)

for res in results:
    x = json.loads(res)
    print(len(x))

for h in handles:
    h.terminate()

