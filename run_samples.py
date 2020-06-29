from infra.edgeinfra import Infra
from placement.exhaust import ExhaustPlacement
from placement.greedy import GreedyPlacement
from placement.pso import PsoPlacement
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

greedy_win = 0
pso_win = 0
def compare(infra, verbose=False):
    global greedy_win
    global pso_win
    
    ex = ExhaustPlacement(infra)
    popt, score_ex = ex.find_placement(verbose=verbose)
    #print("Found placement (exh): " + str(popt)+ " with score: " + str(score_ex))
    
    greedy = GreedyPlacement(infra)
    popt, score_greedy = greedy.find_placement()
    greedy_m = 100*(score_greedy-score_ex) / score_ex
    #print("Found placement (greedy): " + str(popt)+ " with score: " + str(score_greedy) + " Margin: " + str(int(margin)) + "%")
    
    pso = PsoPlacement(infra)
    mm = []
    devnull = open(os.devnull, 'w')
    with RedirectStdStreams(stdout=devnull, stderr=devnull):
        for i in range(1,50):
            popt, score = pso.find_placement()
            margin = 100*(score-score_ex) / score_ex
            mm.append(margin)
    mean_m = numpy.mean(mm)
    pso_m = numpy.average(mm)
    
    #print("PSO found placements with mean margin: " + str(int(mean_m)) + "%")
    p50_m = numpy.percentile(mm,50)
    p25_m = numpy.percentile(mm,25)
    p75_m = numpy.percentile(mm,75)
    p5_m = numpy.percentile(mm,5)
    p95_m = numpy.percentile(mm,95)
    if verbose:
        print("Margin distribution [p5,p25,m,p75,p95]: " + str([p5_m, p25_m, p50_m, p75_m, p95_m]))
    
    if greedy_m < pso_m:
        greedy_win += 1
    else:
        pso_win += 1
    
    print("Min score: %f - Greedy: %f - PSO: %f - Battle: %d/%d" \
            % (score_ex, greedy_m, pso_m, greedy_win, pso_win) )

def run_compare(nodes,pc, verbose=False):
    for n in nodes:
        for p in pc:
            filename = "samples/infra_sample_" + str(n) + "n_" + str(p) + "pc"
            infra = Infra(0,0,file=filename)
            print("===== " + filename)
            compare(filename, verbose)

#run_compare(range(5,51,5), [50], verbose=True)
#run_compare([10, 20, 30, 40, 50], [10], verbose=True)
#run_compare([10, 20, 30], [20], verbose=True)

for i in range(1,20):
    print("===== %d" %i)
    infra = Infra(20,10,method="pareto")
    compare(infra, verbose=False)