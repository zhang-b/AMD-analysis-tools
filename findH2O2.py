import math


oh = 1.47
hh = 0.77 
oo = 1.5
ot = 0

def dis(i, j):
    x = float(i[1]) - float(j[1])
    y = float(i[2]) - float(j[2])
    z = float(i[3]) - float(j[3])
    return math.sqrt(x*x + y*y + z*z)

f = open("water.trj", "r")

o = []
h = []

counter = 0
nh2o2 = 0
for i in f:
    tokens = i.strip().split()
    if counter < 2: 
        nstep = i.strip().split()[0]
    # import o
    elif counter >=2 and counter < 68:
        o.append(tokens)
    else:
    # import h
        h.append(tokens)
    counter += 1

    if counter == 200:
        nh2o2 = 0
        oopairs = []
        for i in range(len(o)):
            for j in range(i+1, len(o)):
                if dis(o[i],o[j]) < oo:
                    oopairs.append([i,j])
                #print o[i], o[j], dis(o[i], o[j])

        for i in oopairs:
            mark = 0
            o1 = o[i[0]]
            o2 = o[i[1]]
            for j in range(len(h)):
                if dis(o1, h[j]) < oh:
                    mark += 1
                    h1 = h[j]
                #print o1, h[j], dis(o1, h[j])
                if mark == 1:
                    for j in range(len(h)):
                        if dis(o2, h[j]) < oh:
                            mark += 1
                            h2 = h[j]
                    if mark == 2:
                        out = open("h2o2_%06d.xyz"%ot, 'w')
                        out.write(" 4\n test\n")
                        out.write("%s\n"%(' '.join(o1)))
                        out.write("%s\n"%(' '.join(o2)))
                        out.write("%s\n"%(' '.join(h1)))
                        out.write("%s\n"%(' '.join(h2)))
                        out.close()
                        ot += 1
                        nh2o2 += 1

        counter = 0
        h = []
        o = []
        print nstep,',', nh2o2
