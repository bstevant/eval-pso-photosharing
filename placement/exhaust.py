from infra import Infra
from . import Score
#import matplotlib.pyplot as plt

class ExhaustPlacement:

    def __init__(self, file):
        self.nodes, c1m, c2m, c3m, c4m, c = Infra.read_infra(file)
        self.scoring = Score(c, c1m, c2m, c3m, c4m)

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

    def find_placement(self):
        score = 100000
        ss= []
        s = 0
        popt = []
        for i in range(0, len(self.nodes)):
            for j in range(0, len(self.nodes)):
                for k in range(0, len(self.nodes)):
                    for l in range(0, len(self.nodes)):
                        p = [i,j,k,l]
                        if self.constraint(p) == 0:
                            s = self.scoring.score_placement(p)
                            ss.append(s)
                            if (s < score):
                                popt = [i,j,k,l]
                                score = s
        return popt, score

#print("Found placement: " + str(popt)+ " with score: " + str(score))
#mean_ss = numpy.mean(ss)
#p25_ss = numpy.percentile(ss,25)
#p75_ss = numpy.percentile(ss,75)
#p5_ss = numpy.percentile(ss,5)
#p95_ss = numpy.percentile(ss,95)
#print("Score distribution [p5,p25,m,p75,p95]: " + str([p5_ss, p25_ss, mean_ss, p75_ss, p95_ss]))

#h, b = numpy.histogram(ss, 100)
#h2 = numpy.cumsum(h)
#h3 = numpy.array([], numpy.float)
#for i in numpy.nditer(h2):
#    j = float(i) / len(data)
#    h3 = numpy.append(h3,[j])
#b2 = b[1:]
#plt.plot(b2, h2, "r")
#plt.show()