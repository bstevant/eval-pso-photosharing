from infra.edgeinfra import Infra
from placement.common import Score
from pyswarm import pso
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

class PsoPlacement:

    def __init__(self, infra, maxiter=100):
        self.infra = infra
        self.scoring = Score(infra)
        self.maxiter = maxiter

    # Constraint: All node in placement should be different
    def constraint(self,p):
        pp = list(map(int, p))
        # Test identical locations in placement
        i = len(pp) - len(set(pp))
        if i == 0: # No identical location
            return [0]
#        elif (i == 1): # 1 identical location for PH
#            return [0]
#        elif (i == 1) and (pp[1] == pp[2]): # 1 ident. location for PH
#            return [0]
#        elif (i == 2) and (pp[1] == pp[2]): # 1 ident. location for PH
#            return [0]
        else: # Some identical locations ... forbidden
            return [-1]

    def find_placement(self):
        # MH, PHd, PHu, TH
        lb = [0, 0, 0, 0]
        n = len(self.infra.nodes) -1
        ub = [n, n, n, n]
        devnull = open(os.devnull, 'w')
        with RedirectStdStreams(stdout=devnull, stderr=devnull):
            popt, score = pso(self.scoring.score_placement, lb, ub, f_ieqcons=self.constraint, maxiter=self.maxiter)
        return list(map(int, popt)), score
