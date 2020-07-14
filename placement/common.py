import numpy

GET_W=1
POST_W=1

class Score:
    def __init__(self, infra):
        self.clients = infra.clients
        self.uig = infra.ui_get_matrix 
        self.uip = infra.ui_post_matrix
        self.phg = infra.ph_get_matrix 
        self.php = infra.ph_post_matrix
        self.mhg = infra.mh_get_matrix 
        self.thg = infra.th_get_matrix 

    def score_placement(self,p):
        clients_rt = []

        # Placements for each services
        p_UI = int(p[0])
        p_PH = int(p[1])
        p_MH = int(p[2])
        p_TH = int(p[3])
    
        for c in self.clients:
            rt_get = int(self.uig[c][p_UI]) \
                   + int(self.mhg[p_UI][p_MH]) \
                   + 5*(int(self.thg[p_UI][p_TH]) \
                      + int(self.phg[p_TH][p_PH]) \
                      + int(self.mhg[p_TH][p_MH]))
            rt_post = int(self.uip[c][p_UI]) + int(self.mhg[p_UI][p_MH]) + int(self.php[p_UI][p_PH])
            rt = (GET_W*rt_get + POST_W*rt_post) / (GET_W + POST_W)
            clients_rt.append(rt)
        
        rt_app = numpy.average(clients_rt)        
    
        return rt_app
