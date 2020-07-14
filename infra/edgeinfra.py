import json
import random
import numpy


# call1: get gallery from UI
ui_get_minrtt = { "dsl_dsl":4000, "dsl_fib":1000,
                 "fib_dsl":4000, "fib_fib":200}

ui_get_medrtt = { "dsl_dsl":8000, "dsl_fib":4000,
                 "fib_dsl":8000, "fib_fib":500}

# call1: post photo to UI
ui_post_minrtt = { "dsl_dsl":20000, "dsl_fib":20000,
                 "fib_dsl":5000, "fib_fib":500}

ui_post_medrtt = { "dsl_dsl":40000, "dsl_fib":40000,
                 "fib_dsl":20000, "fib_fib":2000}

# call1: get list from MH
mh_get_minrtt = { "dsl_dsl":130, "dsl_fib":110,
                 "fib_dsl":110, "fib_fib":90}

mh_get_medrtt = { "dsl_dsl":180, "dsl_fib":150,
                 "fib_dsl":150, "fib_fib":100}

# call2: get photo from PH
ph_get_minrtt = { "dsl_dsl":20000, "dsl_fib":5000,
                 "fib_dsl":20000, "fib_fib":500}

ph_get_medrtt = { "dsl_dsl":40000, "dsl_fib":20000,
                 "fib_dsl":40000, "fib_fib":2000}

# call3: put photo to PH
ph_post_minrtt = { "dsl_dsl":20000, "dsl_fib":20000,
                 "fib_dsl":5000, "fib_fib":500}

ph_post_medrtt = { "dsl_dsl":40000, "dsl_fib":40000,
                 "fib_dsl":20000, "fib_fib":2000}

# call4: get thumb from TH
th_get_minrtt = { "dsl_dsl":1400, "dsl_fib":800,
                 "fib_dsl":1400, "fib_fib":600}

th_get_medrtt = { "dsl_dsl":2200, "dsl_fib":1400,
                 "fib_dsl":2200, "fib_fib":650}

# call4: get thumb from TH (a=2)
th_get2_minrtt = { "dsl_dsl":1000, "dsl_fib":500,
                 "fib_dsl":1000, "fib_fib":300}

th_get2_medrtt = { "dsl_dsl":2000, "dsl_fib":1000,
                 "fib_dsl":2000, "fib_fib":400}

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
        elif method=="pareto":
            self.rtt = self.select_pareto(med_rtt)
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
    
    def select_pareto(self, distri):
        return int(numpy.random.choice(distri))

    def __int__(self):
        return int(self.rtt)

class Infra:

    def __init__(self, n_dsl, n_fiber, method="uni", file=None):
        self.nodes = []
        self.clients = []
        self.a2 = []
        self.ui_get_matrix  = []
        self.ui_post_matrix = []
        self.ph_get_matrix  = []
        self.ph_post_matrix = []
        self.mh_get_matrix  = []
        self.th_get_matrix  = []
        
        if file != None:
            self.read_file(file)
        else:
            self.init_infra(n_dsl, n_fiber, method)

    def init_infra(self, n_dsl, n_fiber, method):
        for i in range(0, n_dsl):
                self.nodes.append(Node("dsl"))
        for i in range(0, n_fiber):
            self.nodes.append(Node("fib"))
            
        # 20% of nodes are clients
        self.clients = random.sample(range(0,len(self.nodes)), int(len(self.nodes)/5))
        # 20% of nodes have a_factor = 2
        self.a2 = random.sample(self.nodes, int(len(self.nodes)/5))
        
        self.init_matrix(self.ui_get_matrix,  ui_get_minrtt, ui_get_medrtt, method)
        self.init_matrix(self.ui_post_matrix, ui_post_minrtt, ui_post_medrtt, method)
        self.init_matrix(self.ph_get_matrix,  ph_get_minrtt, ph_get_medrtt, method)
        self.init_matrix(self.ph_post_matrix, ph_post_minrtt, ph_post_medrtt, method)
        self.init_matrix(self.mh_get_matrix,  mh_get_minrtt, mh_get_medrtt, method)
        self.init_matrix(self.th_get_matrix,  th_get_minrtt, th_get_medrtt, method)
        self.updt_matrix(self.th_get_matrix,  self.a2, th2_get_minrtt, th2_get_medrtt, method)
    
    def init_matrix(self, matrix, minrtt, medrtt, method="uni"):
        m = {}
        if method == "pareto":
            m["dsl_dsl"] = self.gen_pareto(minrtt["dsl_dsl"], medrtt["dsl_dsl"], len(self.nodes)**2)
            m["dsl_fib"] = self.gen_pareto(minrtt["dsl_fib"], medrtt["dsl_fib"], len(self.nodes)**2)
            m["fib_dsl"] = self.gen_pareto(minrtt["fib_dsl"], medrtt["fib_dsl"], len(self.nodes)**2)
            m["fib_fib"] = self.gen_pareto(minrtt["fib_fib"], medrtt["fib_fib"], len(self.nodes)**2)
        for i in self.nodes:
            line = []
            for j in self.nodes:
                link_type = i.node_type + "_" + j.node_type
                if method == "pareto":
                    v = m[link_type]
                else:
                    v = medrtt[link_type]
                l = Link(v, method)
                # Define low rtt for self-calling
                if (i == j):
                    l.rtt = l.rtt / 10
                line.append(int(l))
            matrix.append(line)

    def updt_matrix(self, matrix, nodes, minrtt, medrtt, method="uni"):
        m = {}
        if method == "pareto":
            m["dsl_dsl"] = self.gen_pareto(minrtt["dsl_dsl"], medrtt["dsl_dsl"], len(self.nodes)**2)
            m["dsl_fib"] = self.gen_pareto(minrtt["dsl_fib"], medrtt["dsl_fib"], len(self.nodes)**2)
            m["fib_dsl"] = self.gen_pareto(minrtt["fib_dsl"], medrtt["fib_dsl"], len(self.nodes)**2)
            m["fib_fib"] = self.gen_pareto(minrtt["fib_fib"], medrtt["fib_fib"], len(self.nodes)**2)
        for i in self.nodes:
            line = []
            for j in nodes:
                link_type = i.node_type + "_" + j.node_type
                if method == "pareto":
                    v = m[link_type]
                else:
                    v = medrtt[link_type]
                l = Link(v, method)
                # Define low rtt for self-calling
                if (i == j):
                    l.rtt = l.rtt / 10
                line.append(int(l))
            matrix[i] = line
    
    def serial_matrix(self, matrix):
        m = []
        for line in matrix:
            l = list(map(int, line))
            m.append(l)
        return m
        

    def gen_pareto(self, minrtt, medrtt, n):
        # Pareto params:
        # a = shape
        # min = scale
        a = float(medrtt) / float(medrtt - minrtt) 
        return (numpy.random.pareto(a, n) + 1) * minrtt
        
    def serialize(self):
        serial = {}
        serial["nodes"] = list(map(str, self.nodes))
        serial["clients"] = list(self.clients)
        serial["ui_get_matrix"]  = self.serial_matrix(self.ui_get_matrix)
        serial["ui_post_matrix"] = self.serial_matrix(self.ui_post_matrix)
        serial["ph_get_matrix"]  = self.serial_matrix(self.ph_get_matrix)
        serial["ph_post_matrix"] = self.serial_matrix(self.ph_post_matrix)
        serial["mh_get_matrix"]  = self.serial_matrix(self.mh_get_matrix)
        serial["th_get_matrix"]  = self.serial_matrix(self.th_get_matrix)
        return serial
        
    def read_file(self, file):
        with open(file) as json_data:
            data = json.load(json_data)
            self.nodes = data["nodes"]
            self.ui_get_matrix  = data["ui_get_matrix"] 
            self.ui_post_matrix = data["ui_post_matrix"]
            self.ph_get_matrix  = data["ph_get_matrix"] 
            self.ph_post_matrix = data["ph_post_matrix"]
            self.mh_get_matrix  = data["mh_get_matrix"] 
            self.th_get_matrix  = data["th_get_matrix"] 
            self.clients = data["clients"]

    @classmethod
    def read_infra(self, file):
        with open(file) as json_data:
            data = json.load(json_data)
            nodes = data["nodes"]
            ui_get_matrix  = data["ui_get_matrix"] 
            ui_post_matrix = data["ui_post_matrix"]
            ph_get_matrix  = data["ph_get_matrix"] 
            ph_post_matrix = data["ph_post_matrix"]
            mh_get_matrix  = data["mh_get_matrix"] 
            th_get_matrix  = data["th_get_matrix"] 
            clients = data["clients"]
            return nodes, \
                    ui_get_matrix , \
                    ui_post_matrix, \
                    ph_get_matrix , \
                    ph_post_matrix, \
                    mh_get_matrix , \
                    th_get_matrix , \
                    clients
    
    @classmethod
    def write_infra(self, n, uig, uip, phg, php, mhg, thg, c, file):
        serial = {}
        serial["nodes"] = n
        serial["clients"] = c
        serial["ui_get_matrix"]  = uig
        serial["ui_post_matrix"] = uip
        serial["ph_get_matrix"]  = phg
        serial["ph_post_matrix"] = php
        serial["mh_get_matrix"]  = mhg
        serial["th_get_matrix"]  = thg
        with open(file, 'w') as s:
            s.write(json.dumps(serial))
            #s.close()


if __name__ == '__main__':
    infra = Infra(4,12)
    # file to store matrix
    json_file = "infra_sample.json"
    with open(json_file, 'w', 0) as s:
        s.write(json.dumps(infra.serialize()))
