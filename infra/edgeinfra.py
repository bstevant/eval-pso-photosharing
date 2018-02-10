import json
import random

# call1: get list from MH
# call2: get photo from PH
# call3: put photo to PH
# call4: get thumb from TH

call1_medrtt = { "dsl_dsl":200, "dsl_fib":100,
                 "fib_dsl":200, "fib_fib":70}

call2_medrtt = { "dsl_dsl":800, "dsl_fib":200,
                 "fib_dsl":800, "fib_fib":100}

call3_medrtt = { "dsl_dsl":800, "dsl_fib":800,
                 "fib_dsl":200, "fib_fib":100}

call4_medrtt = { "dsl_dsl":300, "dsl_fib":150,
                 "fib_dsl":300, "fib_fib":150}


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
    def __init__(self, med_rtt, method="uni"):
        if method=="uni":
            self.rtt = self.select_dest_uni(med_rtt)
        elif method=="gaussian":
            self.rtt = self.select_dest_gaussian(med_rtt)
        elif method=="thingauss":
            self.rtt = self.select_dest_thingauss(med_rtt)
        else:
            self.rtt = med_rtt
    
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

    # Select an rtt value from a Gaussian distribution around median
    def select_dest_thingauss(self, median):
        i = random.randint(1,9)
        if i == 1:
            return random.randint(int(median*0.5),int(median*0.8))
        if (i == 2) or (i == 3):
            return random.randint(int(median*0.6),int(median*0.99))
        if (i == 4) or (i == 5) or (i == 6):
            return random.randint(int(median*0.99),int(median*1.1))
        if (i == 7) or (i == 8):
            return random.randint(int(median*1.1),int(median*1.4))
        if i == 9:
            return random.randint(int(median*1.4),int(median*2))
                
    # Select an rtt value from a uniform distribution from 0 to 1.5*median
    def select_dest_uni(self, median):
        i = random.randint(1,4)
        if i == 1:
            return random.randint(int(median*0.3),int(median*0.7))
        if i == 2:
            return random.randint(int(median*0.7), int(median))
        if i == 3:
            return random.randint(int(median), int(median*1.5))
        if i == 4:
            return random.randint(int(median*1.5), int(median*10))
    
    def __int__(self):
        return self.rtt

class Infra:

    def __init__(self, n_dsl, n_fiber, method="uni"):
        self.nodes = []
        self.clients = []
        self.call1_matrix = []
        self.call2_matrix = []
        self.call3_matrix = []
        self.call4_matrix = []
        for i in range(0, n_dsl):
            self.nodes.append(Node("dsl"))
        for i in range(0, n_fiber):
            self.nodes.append(Node("fib"))
            
        # 20% of nodes are clients
        self.clients = random.sample(range(0,len(self.nodes)), len(self.nodes)/5)
        
        self.init_matrix(self.call1_matrix, call1_medrtt, method)
        self.init_matrix(self.call2_matrix, call2_medrtt, method)
        self.init_matrix(self.call3_matrix, call3_medrtt, method)
        self.init_matrix(self.call4_matrix, call4_medrtt, method)
    
    def init_matrix(self, matrix, medrtt, method="uni"):
        for i in self.nodes:
            line = []
            for j in self.nodes:
                link_type = i.node_type + "_" + j.node_type
                l = Link(medrtt[link_type], method)
                # Define low rtt for self-calling
                if (i == j):
                    l.rtt = l.rtt / 10
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
        
    @classmethod
    def read_infra(self, file):
        with open(file) as json_data:
            data = json.load(json_data)
            nodes = data["nodes"]
            call1_matrix = data["call1_matrix"]
            call2_matrix = data["call2_matrix"]
            call3_matrix = data["call3_matrix"]
            call4_matrix = data["call4_matrix"]
            clients = data["clients"]
            return nodes, \
                    call1_matrix, \
                    call2_matrix, \
                    call3_matrix, \
                    call4_matrix, \
                    clients
    
    @classmethod
    def write_infra(self, n, c1m, c2m, c3m, c4m, c, file):
        serial = {}
        serial["nodes"] = n
        serial["clients"] = c
        serial["call1_matrix"] = c1m
        serial["call2_matrix"] = c2m
        serial["call3_matrix"] = c3m
        serial["call4_matrix"] = c4m
        s = open(file, 'w', 0)
        s.write(json.dumps(serial))
        s.close()


if __name__ == '__main__':
    infra = Infra(4,12)
    # file to store matrix
    json_file = "infra_sample.json"
    s = open(json_file, 'w', 0)
    s.write(json.dumps(infra.serialize()))
    s.close()
