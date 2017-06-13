import json
import random

# call1: get list from MH
# call2: get photo from PH
# call3: put photo to PH
# call4: get thumb from TH

# file to store matrix
json_file = "infra_sample.json"



call1_medrtt = { "dsl_dsl":200, "dsl_fib":100,
                 "fib_dsl":200, "fib_fib":70}

call2_medrtt = { "dsl_dsl":800, "dsl_fib":200,
                 "fib_dsl":800, "fib_fib":150}

call3_medrtt = { "dsl_dsl":800, "dsl_fib":800,
                 "fib_dsl":200, "fib_fib":150}

call4_medrtt = { "dsl_dsl":300, "dsl_fib":200,
                 "fib_dsl":300, "fib_fib":200}


class Node:
    nb_nodes = 0
    
    def __init__(self, node_type):
        Node.nb_nodes += 1
        self.node_type = node_type
        self.name = self.gen_node_name()
    
    # Generate a name {fib,dsl}XXX
    def gen_node_name(self):
        return self.node_type + str(Node.nb_nodes)
    
    def __str__(self):
        return self.name


class Link:
    def __init__(self, med_rtt):
        #self.rtt = self.select_dest_uni(med_rtt)
        self.rtt = self.select_dest_gaussian(med_rtt)
    
    # Select an rtt value from a Gaussian distribution around median
    def select_dest_gaussian(self, median):
        i = random.randint(1,9)
        if i == 1:
            return random.randint(int(median*0.2),int(median*0.6))
        if (i == 2) or (i == 3):
            return random.randint(int(median*0.6),int(median*0.9))
        if (i == 4) or (i == 5) or (i == 6):
            return random.randint(int(median*0.9),int(median*1.1))
        if (i == 7) or (i == 8):
            return random.randint(int(median*1.1),int(median*1.4))
        if i == 9:
            return random.randint(int(median*1.4),int(median*10))
    
    # Select an rtt value from a uniform distribution from 0 to 1.5*median
    def select_dest_uni(self, median):
        i = random.randint(1,4)
        if i == 1:
            return random.randint(1,int(median*0.5))
        if i == 2:
            return random.randint(int(median*0.5), int(median))
        if i == 3:
            return random.randint(int(median), int(median*1.5))
        if i == 4:
            return random.randint(int(median*1.5), int(median*10))
    
    def __int__(self):
        return self.rtt

class Infra:
    nodes = []
    clients = []
    call1_matrix = []
    call2_matrix = []
    call3_matrix = []
    call4_matrix = []

    def __init__(self, n_dsl, n_fiber):
        for i in range(0, n_dsl):
            self.nodes.append(Node("dsl"))
        for i in range(0, n_fiber):
            self.nodes.append(Node("fib"))
            
        # 20% of nodes are clients
        self.clients = random.sample(range(0,len(self.nodes)), len(self.nodes)/5)
        
        self.init_matrix(self.call1_matrix, call1_medrtt)
        self.init_matrix(self.call2_matrix, call2_medrtt)
        self.init_matrix(self.call3_matrix, call3_medrtt)
        self.init_matrix(self.call4_matrix, call4_medrtt)
    
    def init_matrix(self, matrix, medrtt):
        for i in self.nodes:
            line = []
            for j in self.nodes:
                link_type = i.node_type + "_" + j.node_type
                l = Link(medrtt[link_type])
                # Define low rtt for self-calling
                if (i == j):
                    l.rtt = 1
                line.append(l)
            matrix.append(line)

    def serial_matrix(self, matrix):
        m = []
        for line in matrix:
            l = map(int, line)
            m.append(l)
        return m

    def serialize(self):
        serial = {}
        serial["nodes"] = map(str, self.nodes)
        serial["clients"] = self.clients
        serial["call1_matrix"] = self.serial_matrix(self.call1_matrix)
        serial["call2_matrix"] = self.serial_matrix(self.call2_matrix)
        serial["call3_matrix"] = self.serial_matrix(self.call3_matrix)
        serial["call4_matrix"] = self.serial_matrix(self.call4_matrix)
        return serial


infra = Infra(16,16)
s = open(json_file, 'w', 0)
s.write(json.dumps(infra.serialize()))
s.close()
