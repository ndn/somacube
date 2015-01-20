import time
import sys

def output(solver):
    t1 = time.time()

    def _write():
        t2 = time.time()

        if t2 - t1 > 5:
            eta = t2 - t1
            eta *= float(solver.progress_total) / float(solver.progress_current)
            h = int(eta) / 3600
            m = (int(eta) % 3600) / 60
            s = int(eta) % 60
            eta = "{}h:{}m:{}s".format(h, m, s)
        else:
            eta = "???"

        sys.stdout.write("\r{:.4f}% -- ETA {} | {} / {} | {} solutions.".format(
            100.0 * float(solver.progress_current) / float(solver.progress_total),
            eta,
            solver.progress_current,
            solver.progress_total,
            len(solver.solutions)))
        sys.stdout.flush()

    while True:
        _write()
        time.sleep(0.25)
        if solver.done:
            _write()
            return

