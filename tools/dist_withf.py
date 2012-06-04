def run_single(n):
    f = open("water.out", 'r')

    #n = 0
    emin = 999999
    emax = -999999
    e = -11700
    de = 65.12
    elist = []
    for i in f:
        etag = "%.2f"%(e-n*de)
        tokens = i.strip().split()
        if tokens[3] == etag:
            ener = float(tokens[2])
            acc = float(tokens[5])
            elist.append([ener, acc])

            if emin > ener:
                emin = ener
            if emax < ener:
                emax = ener

    step = 0.89
    nslice = int((emax - emin)/step) + 1
    edist = [0]*nslice
    adist = [0]*nslice
    steps = [0]*nslice

    for i in range(nslice):
        steps[i] = emin + i*step

    print emin, emax, int((emax-emin)/step+1)

    for i in range(len(elist)):
        ns = int((elist[i][0] - emin)/step)
        edist[ns] += 1
        adist[ns] += elist[i][1]

    for i in range(len(edist)):
        if edist[i]*0.98 > adist[i]:
            adist[i] = edist[i]
        else:
            adist[i] = 0
    #for i in range(len(edist)):
    #    if edist[i] > 0:
    #        adist[i] = adist[i]/edist[i]

    o = open("out_%02d.txt"%n, 'w')
    for i in range(len(edist)):
        o.write("%8d%8d%8.2f\n"%(steps[i],edist[i], adist[i]))
    o.close()

def run_all():
    f = open("water.out", 'r')

    #n = 0
    emin = 999999
    emax = -999999
    e = -11700
    de = 65.12
    counter = 0
    elist = []
    for i in f:
        if counter == 0:
            pass
        else:
            tokens = i.strip().split()
            ener = float(tokens[2])
            acc = float(tokens[5])
            elist.append([ener, acc])

            if emin > ener:
                emin = ener
            if emax < ener:
                emax = ener
        counter += 1

    step = 0.89
    nslice = int((emax - emin)/step) + 1
    edist = [0]*nslice
    adist = [0]*nslice
    steps = [0]*nslice

    for i in range(nslice):
        steps[i] = emin + i*step

    print emin, emax, int((emax-emin)/step+1)

    for i in range(len(elist)):
        ns = int((elist[i][0] - emin)/step)
        edist[ns] += 1
        adist[ns] += elist[i][1]

    for i in range(len(edist)):
        if edist[i]*0.98 > adist[i]:
            adist[i] = edist[i]
        else:
            adist[i] = 0
    #for i in range(len(edist)):
    #    if edist[i] > 0:
    #        adist[i] = adist[i]/edist[i]

    o = open("out.txt", 'w')
    for i in range(len(edist)):
        o.write("%8d%8d%8.2f\n"%(steps[i],edist[i], adist[i]))
    o.close()
for i in range(67):
    run_single(i)
run_all()


    
