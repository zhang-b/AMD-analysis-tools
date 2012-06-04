def find_max(data):
    max = -999999999
    for i in data:
        if max < i:
            max = i
    return max

def find_min(data):
    min = 999999999
    for i in data:
        if min > i:
            min = i
    return min

def gen_dist(data,min,max,step):
    sep = (max-min)/step
    dist = [0]*step
    xcoord = []

    for i in range(step):
        xcoord.append(min+sep*i)
    
    for i in data:
        n = int((i-min)/sep)
        if n > (step-1):
            n = step-1
        dist[n] += 1
    return xcoord, dist

import numpy as nm
import sys

org = nm.genfromtxt(sys.argv[1], delimiter=',')
#data = org[2975:]
data = org.transpose()
min = find_min(data[1])
max = find_max(data[1])

print "-----------------------"
print "min", min, "max", max
print "-----------------------"

x,y = gen_dist(data[1],min,max,200)

o = open('dist.dat', 'w')
for i in range(len(x)):
    o.write('%10.4f%10.4f\n'%(x[i], y[i]))

o.close()
