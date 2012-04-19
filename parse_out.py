#!/usr/bin/env python
"""
@version: $0.1$
@author: Tao Cheng
@contact: chengtao@sjtu.edu.cn
"""

import math
TEMPERATURE = 1898
KT = 8.314*TEMPERATURE/4184
STEP = 100

def parse_out(fname, skip):
    counter = 0
    f = open(fname, 'r')
    o = open('out.csv', 'w')
    for i in f:
        if counter < 1:
            pass
        else:
            tokens = i.strip().split()
            if counter == 1:
                step_re =  int(tokens[0])
            step_re += math.exp(float(tokens[4])/KT)*STEP
            if (counter-1)%skip == 0:
                step = int(tokens[0])
                pe = float(tokens[2])
                be = float(tokens[3])
                de = float(tokens[4])
                o.write("%-20d,"%step)
                o.write("%20d,"%step_re)
                o.write("%20.4f,"%pe)
                o.write("%20.4f,"%be)
                o.write("%20.4f,"%de)
                o.write("\n")
        counter += 1
    o.close()
    f.close()
    
parse_out('water.out', 1000)
    