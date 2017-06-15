from infra import Infra
from . import Score
from pyswarm import pso

class PsoPlacement:

    def __init__(self, file):
        self.nodes, c1m, c2m, c3m, c4m, c = Infra.read_infra(file)
        self.scoring = Score(c, c1m, c2m, c3m, c4m)

    # Constraint: All node in placement should be different
    def constraint(self,p):
        pp = map(int, p)
        # Test identical locations in placement
        i = len(pp) - len(set(pp))
        if i == 0: # No identical location
            return [0]
#        elif (i == 1): # 1 identical location for PH
#            return [0]
        elif (i == 1) and (pp[1] == pp[2]): # 1 ident. location for PH
            return [0]
#        elif (i == 2) and (pp[1] == pp[2]): # 1 ident. location for PH
#            return [0]
        else: # Some identical locations ... forbidden
            return [-1]

    def find_placement(self):
        # MH, PHd, PHu, TH
        lb = [0, 0, 0, 0]
        ub = [len(self.nodes) -1, len(self.nodes) -1, len(self.nodes) -1, len(self.nodes) -1]
        
        popt, score = pso(self.scoring.score_placement, lb, ub, f_ieqcons=self.constraint, maxiter=100)
        return map(int, popt), score
