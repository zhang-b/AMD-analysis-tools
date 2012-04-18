f = open("H1_detail.csv", 'r')
o = open("test.csv", 'w')

for i in f:
    if len(i.strip()) > 0:
        tokens = i.split(',')
        step = int(tokens[0])
        num = int(tokens[1])
        de = float(tokens[2])
        if de > 0:
            pass
        else:
            o.write("%10d,%10d\n"%(step, num))
o.close()
f.close()
