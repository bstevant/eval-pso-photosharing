import json
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
    print score
    return score

score = 100000
for i in range(0, len(nodes)):
    for j in range(0, len(nodes)):
        for k in range(0, len(nodes)):
            p = [i,j,k]
            if (len(p) == len(set(p))):
                s = score_placement(p)
                if (s < score):
                    popt = [i,j,k]
                    score = s

print("Found placement: " + str(map(int, popt))+ " with score: " + str(score))
