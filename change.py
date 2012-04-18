import math
from operator import itemgetter, attrgetter

BETA = 4184/1898/8.124

# obtain the change of fragment
f = open("fill.csv", "r")

increase = []
decrease = []

his = 0
for i in f:
    tokens = i.strip().split(',')
    if len(tokens) == 2:
        now = int(tokens[1])
        step = int(tokens[0])
        if now == his:
            pass
        else:
            if now > his:
                increase.append([his, now, step])
            elif now < his:
                decrease.append([his, now, step])
            else:
                pass
            his = int(tokens[1])
f.close()
# parse energy info
f = open("water.out", "r")
ener = []
for i in f:
    tokens = i.strip().split()
    if i.strip().startswith("step"):
        pass
    elif len(tokens) == 12:
        step = int(tokens[0])
        en = float(tokens[2])
        booste = float(tokens[4])
        force = float(tokens[5])
        ener.append([step, en, booste,force])
f.close()
    
for i in range(len(increase)):
    s = increase[i][2]/100
    en = ener[s][1]
    enprev = ener[s-1][1]
    de = en - enprev
    boostep = ener[s-1][2]
    boosten = ener[s][2]
    force = ener[s-1][3]
    increase[i].append(en)
    increase[i].append(enprev)
    increase[i].append(de)
    increase[i].append(boostep)
    increase[i].append(boosten)
    increase[i].append(force)

#parse the framgment info
import sys
sys.path.append("/home/sungroup/Documents/amd/py")
from parse_mol import parse_mol

def compare(l1, l2):
    react = {}
    pro = {}
    react2 = {}
    pro2 = {}
    for i in l1:
        tokens = i.strip().split()
        if i in l2:
            pass
        else:
            react[tokens[2]] = int(tokens[0])
    for i in l2:
        tokens = i.strip().split()
        if i in l1:
            pass
        else:
            pro[tokens[2]] = int(tokens[0])
    for i in react.keys():
        if i in pro.keys():
            if react[i] > pro[i]:
                react2[i] = react[i] - pro[i] 
            else:
                pass
        else:
            react2[i] = react[i]

    for i in pro.keys():
        if i in react.keys():
            if pro[i] > react[i]:
                pro2[i] = pro[i] - react[i] 
            else:
                pass
        else:
            pro2[i] = pro[i]
    info = ''
    for i in react2.keys():
        info += "%d%s "%(react2[i], i)
    info += " = "
    for i in pro2.keys():
        info += "%d%s "%(pro2[i], i)
        
    return info

molinfo = parse_mol("water.mol")

for i in range(len(increase)):
    s = increase[i][2]/1000 -1
    react = molinfo[s-1][1:]
    pro = molinfo[s][1:]
    info = compare(react, pro)
    increase[i].append(info)


#output

lines = []

o = open("ana.txt", "w")
for i in increase:
    line = ''
    line += "%3d"%i[0]
    line += "%3d"%i[1]
    line += "%10d"%i[2]
    #line += o.write("%11.2f"%i[3])
    #line += o.write("%11.2f"%i[4])
    line += "%8.2f"%i[5]
    line += "%8.2f"%i[6]
    line += "%8.2f"%i[7]
    line += "  %s"%i[9]
    line += "\n"
    lines.append("%s+%s"%(i[9], line))
    o.write(line)
o.close()

lines.sort()
o = open("ana_sort.txt", "w")
for i in lines:
    o.write("%s"%(i.split('+')[-1]))
o.close()


pre  = ''
counter = 0
o = open("ana_total.txt", "w")
for i in lines:
    now = i.split('+')[0]
    boostep = float(i.split('+')[1].split()[4])
    boosten = float(i.split('+')[1].split()[5])
    if boostep < 0.01 or boosten < 0.01:
        boostr = 0
    else:
        boostr = abs(boostep - boosten)
        boostr = 0
    if now == pre:
        counter += 1/math.exp(boostr*BETA)
    else:
        if pre:
            o.write("%10.2f\n"%counter)
        o.write("%40s"%now)
        counter = 0
        counter += 1/math.exp(boostr*BETA)
        pre = now
o.write("%10.2f\n"%counter)
o.close()

#output back

for i in range(len(decrease)):
    s = decrease[i][2]/100
    en = ener[s][1]
    enprev = ener[s-1][1]
    de = en - enprev
    boostep = ener[s-1][2]
    boosten = ener[s][2]
    force = ener[s][3]
    decrease[i].append(en)
    decrease[i].append(enprev)
    decrease[i].append(de)
    decrease[i].append(boostep)
    decrease[i].append(boosten)
    decrease[i].append(force)

for i in range(len(decrease)):
    s = decrease[i][2]/1000 -1
    react = molinfo[s-1][1:]
    pro = molinfo[s][1:]
    info = compare(react, pro)
    decrease[i].append(info)

lines = []

o = open("ana_back.txt", "w")
for i in decrease:
    line = ''
    line += "%3d"%i[0]
    line += "%3d"%i[1]
    line += "%10d"%i[2]
    #line += o.write("%11.2f"%i[3])
    #line += o.write("%11.2f"%i[4])
    line += "%8.2f"%i[5]
    line += "%8.2f"%i[6]
    line += "%8.2f"%i[7]
    line += "  %s"%i[9]
    line += "\n"
    lines.append("%s+%s"%(i[9], line))
    o.write(line)
o.close()

lines.sort()
o = open("ana_sort_back.txt", "w")
for i in lines:
    o.write("%s"%(i.split('+')[-1]))
o.close()


pre  = ''
counter = 1
o = open("ana_total_back.txt", "w")
for i in lines:
    now = i.split('+')[0]
    boostep = float(i.split('+')[1].split()[4])
    boosten = float(i.split('+')[1].split()[5])
    if boostep < 0.01 or boosten < 0.01:
        boostr = 0
    else:
        boostr = abs(boostep - boosten)
        boostr = 0
    if now == pre:
        counter += 1/math.exp(boostr*BETA)
    else:
        if pre:
            o.write("%10.2f\n"%counter)
        o.write("%40s"%now)
        counter = 0
        counter += 1/math.exp(boostr*BETA)
        pre = now
o.write("%10.2f\n"%counter)
o.close()

# forward and backward

f = open("ana_total.txt", 'r')

forward = []
for i in f:
    reax = [[],[],0]
    rec = i.rsplit(' ', 1)[0].split('=')[0].strip().split()
    pro = i.rsplit(' ', 1)[0].split('=')[1].strip().split()
    reax[0] = rec
    reax[1] = pro
    reax[2] = float(i.split()[-1])
    forward.append(reax)
f.close()

f = open("ana_total_back.txt", 'r')

backward = []
for i in f:
    reax = [[],[],0]
    rec = i.rsplit(' ', 1)[0].split('=')[0].strip().split()
    pro = i.rsplit(' ', 1)[0].split('=')[1].strip().split()
    reax[0] = rec
    reax[1] = pro
    reax[2] = float(i.split()[-1])
    backward.append(reax)
f.close()

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
                    if k == l:
                        #print k, l, '-------',
                        mark += 1
            for k in i[1]:
                for l in j[0]:
                    if k == l:
                        #print k, l
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
        total.append([i[1],i[0],0, i[-1], -i[-1]])

sorted(total, key=itemgetter(4))
o = open("reax_table.txt", 'w')
for i in total:
    rect = ' '.join(i[0])
    pro = ' '.join(i[1])
    o.write("%45s%6.2f%6.2f%6.2f\n"%(rect+' = ' + pro, i[2], i[3], i[4]))
o.close()
