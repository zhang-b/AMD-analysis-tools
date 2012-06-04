from sets import Set
import os

def parse_reactiontable(fname):
    a = Set([])
    f = open(fname, 'r')
    for i in f:
        tokens = i.strip().split()
        if len(tokens) > 4:
            reac = i.strip().split()
            reac = '_'.join([j.strip() for j in reac[:-3]])
            n = int(tokens[-1])
            if n < 0:
                a.add(reac)
    f.close()
    return a
 
def count_reactions(fname, reactions):
    f = open(fname, 'r')
    for i in f:
        for j in reactions.keys():
            line = i.strip().split()
            line = '_'.join([k.strip() for k in line[:-3]])
            if line == j:
                reactions[j] += int(i.strip().split()[-1])
    f.close()
FOLDER = """
/home/sungroup/Documents/amd/sim/rc/amd/a1498/run
/home/sungroup/Documents/amd/sim/rc/amd/a1898/run
/home/sungroup/Documents/amd/sim/rc/induce/a1498/run
/home/sungroup/Documents/amd/sim/rc/induce/a1898/run
"""

folder = [i.strip() for i in FOLDER.strip().split('\n')]

now = Set([])
prev = Set([])
common = Set([])
counter = 0

for i in folder[0:1]:
    os.chdir(i)
    for j in range(20):
        os.chdir("r%02d"%j)
        now = parse_reactiontable("H2O1_reax_table.txt")
        if counter ==0:
            prev = now
        common = prev.intersection(now)
        prev = now
        os.chdir("..")
        counter += 1

reactions = {}

for i in folder:
    os.chdir(i)
    for k in common:
            reactions[k] = 0
    for j in range(20):
        os.chdir("r%02d"%j)
        now = count_reactions("H2O1_reax_table.txt", reactions)
        os.chdir("..")
    print i
    for (l, m) in reactions.items():
        pass
        print "%-60s,%8s"%(l, m)

