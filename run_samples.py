from placement import ExhaustPlacement
from placement import PsoPlacement
import numpy
import os
import sys

class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


def compare(file):
    ex = ExhaustPlacement(file)
    popt, score_ex = ex.find_placement()
    print("Found placement (exh): " + str(popt)+ " with score: " + str(score_ex))
    pso = PsoPlacement(file)
    mm = []
    devnull = open(os.devnull, 'w')
    with RedirectStdStreams(stdout=devnull, stderr=devnull):
        for i in range(1,50):
            popt, score = pso.find_placement()
            margin = 100*(score-score_ex) / score_ex
            mm.append(margin)
        #print("Found placement (pso): " + str(popt)+ " with score: " + str(score)) + "margin: " + str(int(margin)) + "%"
    mean_m = numpy.mean(mm)
    print "PSO found placements with mean margin: " + str(int(mean_m)) + "%"

def run_compare(nodes,pc):
    for n in nodes:
        for p in pc:
            filename = "samples/infra_sample_" + str(n) + "n_" + str(p) + "pc"
            print("===== " + filename)
            compare(filename)

run_compare([64], range(0,101,5))