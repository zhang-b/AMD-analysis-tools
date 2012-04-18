import sys

x = []
y = []
input = sys.argv[1]
f = open(input, 'r')
for i in f:
    tokens = i.strip().split(',')
    if len(tokens) == 2:
        x.append(int(tokens[0]))
        y.append(int(float(tokens[1])))
f.close()
x2 = []
y2 = []

c1 = 0
for i in range(0, 80001000, 1000):
    if len(x) > c1:
        if  x[c1] > i:
            x2.append(i)
            y2.append(0)
        else:
            x2.append(x[c1])
            y2.append(y[c1])
            c1 += 1
    else:
        x2.append(i)
        y2.append(0)

o = open("fill.csv", "w")

for i in range(len(x2)):
    o.write("%d,%d\n"%(x2[i], y2[i]))
o.close()


