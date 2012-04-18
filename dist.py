"""
@version: $0.1$
@author: Tao Cheng
@contact: chengtao@sjtu.edu.cn
"""

from parse_mol import parse_out
import matplotlib.pyplot as plt
import os

def find_max(elist):
    """
    return the max number in a list
    @param elist: a list
    @note: default lowest level is -99999999
    """
    max = -9999999999
    n = 0
    for i in range(len(elist)):
        if max < elist[i]:
            max = elist[i]
            n = i
    return max, n

def find_min(elist):
    """
    return the min number in a list
    @param elist: a list
    @note: default highest level is 99999999
    """
    min = 9999999999
    n = 0
    for i in range(len(elist)):
        if min > elist[i]:
            min = elist[i]
            n = i
    return min, n

def ener_dist(elist, nslice):
    """generate the energy distribution with n slice
    @var elist: input energy list
    @type elist: list
    @var nslice: n slice
    """

    emax, p = find_max(elist)
    emin, p = find_min(elist)
    step = (emax-emin)/nslice
    edist = [[0]*nslice, [0]*nslice]

    for i in range(nslice):
        edist[0][i] = emin + i*step
    
    counter = 0
    for i in elist:
        n = int((i-emin)/step)
        if n >= nslice:
            n = nslice - 1
        edist[1][n] += 1
        counter += 1
    for i in range(len(edist[1])):
        edist[1][i] = edist[1][i]*1.0/counter

    return edist

def ener_dist_with_other(elist, olist, nslice):
    """generate the energy distribution with n slice,
    and sort olist according to elist.
    @var elist: input energy list
    @type elist: list
    @var nslice: n slice
    """

    if len(elist) != len(olist):
        print "Warning"

    emax, p = find_max(elist)
    emin, p = find_min(elist)
    step = (emax-emin)/nslice
    edist = [[0]*nslice, [0]*nslice, [0]*nslice]

    print "sort the energy from %.2f to %.2f with %.2f"%(emin, emax, step)

    for i in range(nslice):
        edist[0][i] = emin + i*step
    
    counter = 0
    for i in range(len(elist)):
        n = int((elist[i]-emin)/step)
        if n >= nslice:
            n = nslice - 1
        edist[1][n] += 1
        if olist[i] > 0.9:
            edist[2][n] = 0.0045
        counter += 1

    for i in range(len(edist[1])):
        edist[1][i] = edist[1][i]*1.0/counter

    return edist

def main2():
    """
    specify for pes analysis
    """
    epath = "/home/sungroup/Documents/amd/sim/pes/r1298"
    for i in range(34):
        folder = os.path.join(epath, "mix%02d"%(i*2))
        os.chdir(folder)
        elist = parse_out("water.out", 11, 2,1)
        edist = ener_dist(elist, 500)
        if i == 3:
            pass
        else:
            plt.plot(edist[0], edist[1])
            v, p = find_max(edist[1])
            print i, v, edist[0][p] 
            plt.annotate("%d"%(i*2), xy=(edist[0][p], v+0.0005),\
                xycoords='data')
    plt.xlabel("Potential Energy")
    plt.ylabel("possibility")
    plt.show()

def main():
    elist = parse_out("water.out", 12, 2,1)
    edist = ener_dist(elist, 5000)
    o = open("ener_dist.txt", "w")
    for i in range(len(edist[0])):
        o.write("%8.3f%8.5f\n"%(edist[0][i], edist[1][i]))
    o.close()
    plt.plot(edist[0], edist[1])
    plt.show()

def main3():
    elist = parse_out("water.out", 12, 2,1)
    flist = parse_out("water.out", 12, 5,1)
    edist = ener_dist_with_other(elist, flist, 5000)
    o = open("ener_dist.txt", "w")
    for i in range(len(edist[0])):
        o.write("%8.3f%8.5f%8.3f\n"%(edist[0][i], edist[1][i], edist[2][i]))
    o.close()
    #plt.plot(edist[0], edist[1])
    #plt.plot(edist[0], edist[2])
    #plt.show()

if __name__ == "__main__":
    main3()


