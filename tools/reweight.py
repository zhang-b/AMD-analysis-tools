import os
import math
BETA = 4184/1898/8.124
print BETA
f = open('water.out', 'r')
reweight = {}
realstep = 0
counter = 0

for i in f:
    if counter > 0:
        tokens = i.strip().split()
        step = int(tokens[0])
        if step%1000 == 0:
            reweight[step] = []
            de = float(tokens[4])
            if de > 2 and de < 22:
                reweight[step].append(realstep)
                realstep += int(math.exp(de*BETA))*1000
            else:
                realstep += 1000
            reweight[step].append(realstep)
    counter += 1
print realstep
f.close()



flist = [
'H2O1',
'H3O1',
'H1O1',
'H1O2',
'H2O2',
'H1',
]

def handle(fname):
    f = open("%s.csv"%fname, 'r')
    o = open("%s_time.csv"%fname, 'w')
    for i in f:
        tokens = i.strip().split(',')
        step = int(tokens[0])
        num = int(float(tokens[1]))
        start = reweight[step][0]
        o.write("%14d,%6d\n"%(start, num))
        if len(reweight[step]) == 2:
            end = reweight[step][1]
            for j in range(start+1000, end, 1000):
                o.write("%14d,%6d\n"%(j, num))

    f.close()
    o.close()
    

for i in flist:
    handle(i)
    os.system("python fill.py %s_time.csv"%i)
    os.system("cp fill.csv %s_time_f.csv"%i)

