import sys

flist = [
'.out',
#'.mol',
]

out_sub = sys.argv[1].replace('/', '_')
counter = 0

for i in flist:
    outf = out_sub+i
    o = open(outf, 'w')
    f = open(sys.argv[1]+'water'+i, 'r')
    print sys.argv[1]+i
    for i in f:
        if counter > 0:
            if (counter-1)%100 == 0:
                o.write(i)
        else:
            o.write(i)
        counter += 1
    f.close()
    o.close()
