"""
@todo : error analysis
@log :

Mon Dec  2 16:59:53 PST 2013
- Error analysis
"""
import numpy as np
from sets import Set
import os

def parse_reactiontable(fname):
    """
    Parse the reactions
    """
    a = Set([])
    b = Set([])
    f = open(fname, 'r')
    for i in f:
        tokens = i.strip().split()
        if len(tokens) > 4:
            reac = i.strip().split()
            reac = '_'.join([j.strip() for j in reac[:-3]])
            n = int(tokens[-1])
            # forward
            if n < 0:
                a.add(reac)
            # backward
            if n > 0:
                b.add(reac)
    f.close()
    # return a, if we need a forward reaction, otherwise return b
    return a
 
def count_reactions(fname, reactions, std):
    """
    count the reactions
    """
    f = open(fname, 'r')
    for i in f:
        for j in reactions.keys():
            line = i.strip().split()
            line = '_'.join([k.strip() for k in line[:-3]])
            if line == j:
                n = int(i.strip().split()[-1])
                reactions[j] += n
                std[j].append(n)
    f.close()

def get_reaction_types(folder):

    now = Set([])
    prev = Set([])
    common = Set([])
    all = Set([])

    counter = 0
    for i in folder[0:1]:
        os.chdir(i)
        for j in range(1,20):
            if j == 12 or j == 10:
                pass
            else:
                print i, j
                os.chdir("r%02d"%j)
                now = parse_reactiontable("H2O2_reax_table.txt")
                if counter ==0:
                    prev = now
                common = prev.intersection(now)
                all = all.union(now)
                prev = now
                os.chdir("..")
                counter += 1
    return common, all

def main():
    FOLDER = """
    /home/sungroup/Documents/amd/sim/rc/amd/a1498/run
    /home/sungroup/Documents/amd/sim/rc/amd/a1898/run
    /home/sungroup/Documents/amd/sim/rc/induce/a1498/run
    /home/sungroup/Documents/amd/sim/rc/induce/a1898/run
    """

    FOLDER = """
    /temp1/inprogress/1898/a00/
    /temp1/inprogress/1898/a20_all/
    /temp1/inprogress/1898/a30_all/
    /temp1/inprogress/1898/a40_all/
    """
    
    FOLDER = """
    /net/hulk/home6/chengtao/PUREMD/bboost15
    /net/hulk/home6/chengtao/PUREMD/bboost21
    /net/hulk/home6/chengtao/PUREMD/bboost22
    /net/hulk/home6/chengtao/PUREMD/bboost23
    """

    folder = [i.strip() for i in FOLDER.strip().split('\n')]
    
    #------------------------------------------#
    #          get reaction types              #
    #------------------------------------------#
    common, all = get_reaction_types(folder )
    
    reactions = {}
    std = {}
    
    #------------------------------------------#
    #          get reaction types              #
    #------------------------------------------#
    for i in folder:
        os.chdir(i)
        for k in all:
                reactions[k] = 0
                std[k] = []
        for j in range(1,20):
            if j == 12 or j == 10:
                pass
            else:
                os.chdir("r%02d"%j)
                now = count_reactions("H2O2_reax_table.txt", reactions, std)
                os.chdir("..")
        print i
        for (l, m) in reactions.items():
            for i in range(19 - len(std[l])):
                std[l].append(0)
            data = np.array(std[l])
            print "%-60s,%8s, %8.2f"%(l, m, np.std(data)*20)

if __name__ == "__main__":
    main()
