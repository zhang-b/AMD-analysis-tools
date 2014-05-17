"""
Fill the reweighted fragment files with same interval
python fill.py fname t_start t_end t_interval [fill value]
"""

import sys
import argparse

def read_input(input):
    """
    Read the input file.
    """
    x = []
    y = []

    f = open(input, 'r')
    for i in f:
        tokens = i.strip().split(',')
        if len(tokens) == 2:
            x.append(int(float(tokens[0])))
            y.append(int(float(tokens[1])))
    f.close()
    return x, y

def main():
    
    input = sys.argv[1]
    output = input[:-4] + "_filled.csv"
    t0 = int(sys.argv[2])
    t1 = int(sys.argv[3])
    dt = int(sys.argv[4])

    
    x2 = []
    y2 = []

    c1 = 0
    n = 0
    for i in range(t0, t1, dt):
        if len(x) > c1:
            x2.append(i)
            if len(sys.argv) > 5:
                if n == 0:
                    y2.append(y[c1])
                else:
                    y2.append(int(sys.argv[5]))
            elif len(sys.argv) == 5:
                y2.append(y[c1])
            n += 1
            while (x[c1] <= i):
                print x[c1], i
                c1 += 1
                n = 0

    o = open(output, "w")

    for i in range(len(x2)):
        o.write("%50d,%50d\n"%(x2[i], y2[i]))
    o.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print __doc__
    else: 
        main()
