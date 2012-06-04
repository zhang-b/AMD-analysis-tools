import sys
fname = sys.argv[1]
skip = int(sys.argv[2])

f = open(fname, 'r')
o = open("out.csv", 'w')
counter = 0

for i in f:
    if counter%skip == 0:
        o.write(i)
    else:
        pass
    counter += 1
o.close()
f.close()
