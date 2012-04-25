
import os
from operator import itemgetter

"""
class Reaction():
    def __init__(self):
        rec = []
        pro = []
        n = 1
"""     


def find_reactions():
    prev = ''
    now = ''
    counter = 0
    of = open('reactions.csv', 'w')
    f = open("fragment.csv", 'r')
    for i in f:
        if counter == 0:
            global MOLTYPES
            MOLTYPES = i.split(',')[1:] 
            for i in range(len(MOLTYPES)):
                MOLTYPES[i] = MOLTYPES[i].strip()           
        else:
            step = i.split(',', 1)[0]
            line = i.split(',', 1)[1]
            if len(prev) == 0:
                prev = line
            now = line
            if now != prev:
                parse_reactions(step, prev, now, of)
            prev = now
        counter += 1
    of.close()

def parse_reactions(step, prev, now, of):
    rec = []
    pro = []
    r1 = prev.strip().split(',')
    r2 = now.strip().split(',')
    for i in range(len(r1)):
        if r1[i] != r2[i]:
            n = int(r1[i])-int(r2[i])
            mol = MOLTYPES[i]
            if n > 0:
                rec.append("%d%s"%(n, mol))           
            else:
                pro.append("%d%s"%(-n, mol))
    rec.sort()
    pro.sort()
    reaction = ''
    reaction += ' + '.join(rec)        
    reaction += ' = '        
    reaction += ' + '.join(pro)        
    reaction += '\n'
    of.write(reaction)

def catalog_reactions(fragment):
    
    f = open("reactions_sort.csv", 'r')
    reactions = []
    counter = 0
    n = 0
    for i in f:
        if counter == 0:
            prev = i
            n = 0
        now = i
        if now == prev:
            n += 1
        else:
            reactions.append([prev, n])
            n = 1
        prev = now
        counter += 1
    #print now, reactions[-1][0]
    if len(reactions) > 1:
        if now == reactions[-1][0]:
            n +=1
    reactions.append([prev, n])
    #print reactions    
    f.close()
    
    o = open('reaction_types.csv', 'w')
    for i in reactions:
        o.write("%-60s,%6d\n"%(i[0].strip(), i[1]))
    o.close()
    
    n1 = 0
    n2 = 0
    forward = []
    backward = []    
    for i in reactions:
        tokens = i[0].strip().split("=")
        rec = tokens[0].split('+')
        pro = tokens[1].split('+')
        for j in rec:
            if fragment == j.strip()[1:]:
                forward.append([rec, pro, i[1]])
                n1 += int(j.strip()[0])*int(i[1])
        for k in pro:
            if fragment == k.strip()[1:]:
                backward.append([rec, pro, i[1]])
                n2 += int(k.strip()[0])*int(i[1])
    #print backward[-1]
    #print forward[-1]
    #print n1, n2, n2-n1
    o = open("%s_forward.csv"%fragment, 'w')
    for i in forward:
        line = ''
        line += '+'.join(i[0])
        line += '='
        line += '+'.join(i[1])
        o.write("%-60s,%6d\n"%(line, i[2]))
    o.close()
    
    o = open("%s_backward.csv"%fragment, 'w')
    for i in backward:
        line = ''
        line += '+'.join(i[0])
        line += '='
        line += '+'.join(i[1])
        o.write("%-60s,%6d\n"%(line, i[2]))
    o.close()

    forward = sorted(forward, key=itemgetter(2))
    backward = sorted(backward, key=itemgetter(2))
    total = []
    ignorei = []
    ignorej = []
    
    for i in forward:
        for j in backward:
            mark = 0
            if len(i[0])==len(j[1]) and len(i[1])==len(j[0]):
                for k in i[0]:
                    for l in j[1]:
                        if k.strip() == l.strip():
                            mark += 1
                for k in i[1]:
                    for l in j[0]:
                        if k.strip() == l.strip():
                            mark += 1
                if mark == (len(i[0]) + len(i[1])):
                    newn = i[-1] - j[-1]
                    total.append([i[0],i[1],i[-1], j[-1], newn])
                    #print i[0], j[1], mark
                    ignorei.append(i) 
                    ignorej.append(j) 
                    break
    
    for i in forward:
        if i in ignorei:
            pass
        else:
            total.append([i[0],i[1],i[-1], 0, i[-1]])
    
    for i in backward:
        if i in ignorej:
            pass
        else:
            total.append([i[1],i[0] ,0, i[-1], -i[-1]])
    total = sorted(total, key=itemgetter(4))
    
    o = open("%s_reax_table.txt"%fragment, 'w')
    for i in total:
        rect = ' '.join(i[0])
        pro = ' '.join(i[1])
        o.write("%70s%6d%6d%6d\n"%(rect+' = ' + pro, i[2], i[3], i[4]))
    o.write("%70s%6d%6d%6d\n"%('total', n1, n2, n1-n2))
    o.close()   
    
#from parse_mol_fun import parse_mol_fun
#parse_mol_fun('water.mol')
find_reactions()
os.system("sort reactions.csv > reactions_sort.csv")

FRAGMENTS = ['H2O1', 'H2', 'O2', 'H2O2', 'H1', 'O1', 'H1O2', 'H1O1', ]
for i in FRAGMENTS:
    catalog_reactions(i)
