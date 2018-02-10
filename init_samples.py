from infra import Infra
import json

def gen_sample(i,j,json_file):
    infra = Infra(i,j, "pareto")
    s = open(json_file, 'w', 0)
    s.write(json.dumps(infra.serialize()))
    s.close()
    
    
def gen_samples(nodes, pc):
    for n in nodes:
        for p in pc:
            n_fib = int(n*p/100)
            n_dsl = n - n_fib
            filename = "samples/infra_sample_" + str(n) + "n_" + str(p) + "pc"
            print("Generating " + filename)
            gen_sample(n_dsl, n_fib, filename)



gen_samples(range(5,51,5), [50])
#gen_sample(5,5,"samples/infra_sample_10n_50pc")
#gen_sample(10,10,"samples/infra_sample_20n_50pc")
#gen_sample(15,15,"samples/infra_sample_30n_50pc")
#gen_sample(20,20,"samples/infra_sample_40n_50pc")
#gen_sample(25,25,"samples/infra_sample_50n_50pc")


#gen_samples([20], range(0,101,5))
#gen_sample(40,0,"samples/infra_sample_20n_00pc")
#gen_sample(38,1,"samples/infra_sample_20n_05pc")
#gen_sample(36,2,"samples/infra_sample_20n_10pc")
#gen_sample(34,3,"samples/infra_sample_20n_15pc")
#gen_sample(32,4,"samples/infra_sample_20n_20pc")
#gen_sample(30,5,"samples/infra_sample_20n_25pc")
#gen_sample(28,6,"samples/infra_sample_20n_30pc")
#gen_sample(26,7,"samples/infra_sample_20n_35pc")
#gen_sample(12,8,"samples/infra_sample_20n_40pc")
#gen_sample(11,9,"samples/infra_sample_20n_45pc")
#gen_sample(10,10,"samples/infra_sample_20n_50pc")
#gen_sample(9,11,"samples/infra_sample_20n_55pc")
#gen_sample(8,12,"samples/infra_sample_20n_60pc")
#gen_sample(7,13,"samples/infra_sample_20n_65pc")
#gen_sample(6,14,"samples/infra_sample_20n_70pc")
#gen_sample(5,15,"samples/infra_sample_20n_75pc")
#gen_sample(4,16,"samples/infra_sample_20n_80pc")
#gen_sample(3,17,"samples/infra_sample_20n_85pc")
#gen_sample(2,18,"samples/infra_sample_20n_90pc")
#gen_sample(1,19,"samples/infra_sample_20n_95pc")
#gen_sample(0,20,"samples/infra_sample_20n_100pc")
