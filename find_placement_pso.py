import json
from pyswarm import pso
import random
import numpy


CALL1_WEIGHT=3
CALL2_WEIGHT=2
CALL3_WEIGHT=1
CALL4_WEIGHT=3

def read_infra(file):
    with open(file) as json_data:
        d = json.load(json_data)
        return d
        
data = read_infra("infra_sample.json")
nodes = data["nodes"]
call1_matrix = data["call1_matrix"]
call2_matrix = data["call2_matrix"]
call3_matrix = data["call3_matrix"]
call4_matrix = data["call4_matrix"]
clients = data["clients"]

def score_placement(p):
    call1_rtt = []
    call2_rtt = []
    call3_rtt = []
    call4_rtt = []
    for c in clients:
        call1_rtt.append(call1_matrix[c][int(p[0])])
        call2_rtt.append(call2_matrix[c][int(p[1])])
        call3_rtt.append(call3_matrix[c][int(p[1])])
        call4 = call4_matrix[c][int(p[2])] \
                + call1_matrix[int(p[2])][int(p[0])] \
                + call2_matrix[int(p[2])][int(p[1])]
        call4_rtt.append(call4)
    call1_mean = numpy.mean(call1_rtt)
    call2_mean = numpy.mean(call2_rtt)
    call3_mean = numpy.mean(call3_rtt)
    call4_mean = numpy.mean(call4_rtt)
    score = CALL1_WEIGHT*call1_mean \
            + CALL2_WEIGHT* call2_mean \
            + CALL3_WEIGHT* call3_mean \
            + CALL4_WEIGHT* call4_mean
    #print "p:" + str(int(p[0])) + "," + str(int(p[1])) + " score:" + str(score)
    return score

# Constraint: All node in placement should be different
def constraint(p):
    pp = map(int, p)
    if len(pp) > len(set(pp)):
        return [-1]
    else:
        return [0]

lb = [0, 0, 0]
ub = [len(nodes) -1, len(nodes) -1, len(nodes) -1]

popt, score = pso(score_placement, lb, ub, f_ieqcons=constraint, maxiter=1000, minstep=0.5, minfunc=10)
print("Found placement: " + str(map(int, popt))+ " with score: " + str(score))
