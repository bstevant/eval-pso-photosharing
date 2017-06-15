import numpy

CALL1_WEIGHT=3
CALL2_WEIGHT=2
CALL3_WEIGHT=1
CALL4_WEIGHT=3

class Score:
    def __init__(self, c, c1m, c2m, c3m, c4m):
        self.clients = c
        self.call1_matrix = c1m
        self.call2_matrix = c2m
        self.call3_matrix = c3m
        self.call4_matrix = c4m

    def score_placement(self,p):
        call1_rtt = []
        call2_rtt = []
        call3_rtt = []
        call4_rtt = []
        # Placements for each services
        p_MH  = int(p[0])
        p_PHd = int(p[1])
        p_PHu = int(p[2])
        p_TH  = int(p[3])
    
        for c in self.clients:
            call1_rtt.append(self.call1_matrix[c][p_MH])
            call2_rtt.append(self.call2_matrix[c][p_PHd])
            call3_rtt.append(self.call3_matrix[c][p_PHu])
            call4 = self.call4_matrix[c][p_TH] \
                    + self.call1_matrix[p_TH][p_MH] \
                    + self.call2_matrix[p_TH][p_PHd]
            call4_rtt.append(call4)
        call1_mean = numpy.mean(call1_rtt)
        call2_mean = numpy.mean(call2_rtt)
        call3_mean = numpy.mean(call3_rtt)
        call4_mean = numpy.mean(call4_rtt)
        score = CALL1_WEIGHT*call1_mean \
                + CALL2_WEIGHT* call2_mean \
                + CALL3_WEIGHT* call3_mean \
                + CALL4_WEIGHT* call4_mean
    
        return score
