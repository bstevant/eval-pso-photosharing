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

print "========= Infra 10n 50pc"
compare("samples/infra_sample_10n_50pc")
print "========= Infra 20n 50pc"
compare("samples/infra_sample_20n_50pc")
print "========= Infra 30n 50pc"
compare("samples/infra_sample_30n_50pc")
print "========= Infra 40n 50pc"
compare("samples/infra_sample_40n_50pc")
print "========= Infra 50n 50pc"
compare("samples/infra_sample_50n_50pc")