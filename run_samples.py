from infra.edgeinfra import Infra
from placement.exhaust import ExhaustPlacement
from placement.greedy import GreedyPlacement
from placement.pso import PsoPlacement
import time
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

def print_distrib(s, a):
    p50_m = numpy.percentile(a,50)
    p25_m = numpy.percentile(a,25)
    p75_m = numpy.percentile(a,75)
    p5_m = numpy.percentile(a,5)
    p95_m = numpy.percentile(a,95)
    print(s + " Margin[p5,p25,m,p75,p95]: " + str([p5_m, p25_m, p50_m, p75_m, p95_m]))


def eval_strategies(n, nb_dsl, nb_fib):
    greedy_margins = []
    greedy_times = []
    pso_margins = []
    pso_times = []
    
    for k in range(0,n):
        infra = Infra(nb_dsl, nb_fib, method="pareto")
        
        ex = ExhaustPlacement(infra)
        popt, score_ex = ex.find_placement(verbose=False)
        
        greedy = GreedyPlacement(infra)
        t0 = time.time()
        popt, score_greedy = greedy.find_placement()
        t = time.time() - t0
        greedy_m = 100*(score_greedy-score_ex) / score_ex
        greedy_margins.append(greedy_m)
        greedy_times.append(t)
        
        pso = PsoPlacement(infra, maxiter=200)
        mm = []
        devnull = open(os.devnull, 'w')
        with RedirectStdStreams(stdout=devnull, stderr=devnull):
            t = 0.0
            for i in range(0,20):
                t0 = time.time()
                popt, score = pso.find_placement()
                t += time.time() - t0
                margin = 100*(score-score_ex) / score_ex
                mm.append(margin)
        pso_m = numpy.average(mm)
        pso_margins.append(pso_m)
        pso_times.append(t/20)
    
    greedy_avg_time = numpy.average(greedy_times)
    pso_avg_time = numpy.average(pso_times)
    #print("GREEDY (%d,%d): t: %f %s" % (nb_dsl, nb_fib, greedy_avg_time, str(greedy_margins)))
    print_distrib("GREEDY (%d,%d): t: %f" % (nb_dsl, nb_fib, greedy_avg_time), greedy_margins)
    #print("PSwarm (%d,%d): t: %f %s" % (nb_dsl, nb_fib, ps_avg_time, str(pso_margins)))
    print_distrib("PSwarm (%d,%d): t: %f" % (nb_dsl, nb_fib, pso_avg_time), pso_margins)

eval_strategies(5, 5, 5)

#for i in range(1,20):
#    print("===== %d" %i)
#    infra = Infra(6,14,method="pareto")
#    compare(infra, verbose=False)