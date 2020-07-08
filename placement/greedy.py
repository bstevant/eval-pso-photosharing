from infra.edgeinfra import Infra
from placement.common import Score
import numpy
#import matplotlib.pyplot as plt

GET_W = 1
POST_W = 1

class GreedyPlacement:

    def __init__(self, infra):
        self.infra = infra
        self.scoring = Score(infra)

    def constraint(self, p):
        # Test identical locations in placement
        i = len(p) - len(set(p))
        if i == 0: # No identical location
            return 0
#        elif (i == 1): # 1 identical location for PH
#            return 0
        elif (i == 1) and (p[1] == p[2]): # 1 identical location for PH
            return 0
#        elif (i == 2) and (p[1] == p[2]): # 1 identical location for PH
#            return 0
        else: # Some identical locations ... forbidden
            return -1
    
    def find_placement(self, verbose=False):
        # Find UI
        min_rp_ui = 10000000
        ui = -1
        for i in range(0, len(self.infra.nodes)):
            rp_clients = []
            for clt in self.infra.clients:
                rt = (GET_W*self.infra.ui_get_matrix[clt][i] + POST_W*self.infra.ui_post_matrix[clt][i])/(GET_W+POST_W)
                rp_clients.append(rt)
            mean_rp_clients = numpy.mean(rp_clients)
            if mean_rp_clients < min_rp_ui:
                min_rp_ui = mean_rp_clients
                ui = i
        
        # find MH
        min_rp_mh = 10000000
        mh = -1
        for i in range(0, len(self.infra.nodes)):
            if i == ui: continue
            if self.infra.mh_get_matrix[ui][i] < min_rp_mh:
                min_rp_mh = self.infra.mh_get_matrix[ui][i]
                mh = i
        
        # find TH
        min_rp_th = 10000000
        th = -1
        for i in range(0, len(self.infra.nodes)):
            if i in {ui, mh}: continue
            if self.infra.th_get_matrix[ui][i] < min_rp_th:
                min_rp_th = self.infra.th_get_matrix[ui][i]
                th = i
        
        # find PH
        min_rp_ph = 10000000
        ph = -1
        for i in range(0, len(self.infra.nodes)):
            if i in {ui, mh, th}: continue
            #rt = (GET_W*self.infra.ph_get_matrix[th][i] + POST_W*self.infra.ph_post_matrix[ui][i])/(GET_W+POST_W)
            rt = self.infra.ph_get_matrix[th][i]
            if rt < min_rp_ph:
                min_rp_ph = rt
                ph = i
        
        popt = [ui, ph, mh, th]
        score = self.scoring.score_placement(popt)
        return popt, score
