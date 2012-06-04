#!/usr/bin/env python
"""
@version: $0.1$
@author: Tao Cheng
@contact: chengtao@sjtu.edu.cn
"""

import math
TEMPERATURE = 1898
KT = 8.314*TEMPERATURE/4184
STEP = 10

def parse_out(fname, skip):
    """Output the step (step), reweighted step (step_re), potential energy
    (pe), boost energy (be) and biased potential energy (de) to out.csv
    @param fname: name of .outfile
    @param skip: number of frame to skip
    @note: The current code is exactly adaptive to the current file structure.
    """
    counter = 0
    f = open(fname, 'r')
    o = open('out.csv', 'w')
    for i in f:
        if counter < 1:
            pass
        else:
            #===================================================================
            # seperate the terms acoording to the row posistion
            #===================================================================
            tokens = i.strip().split()
            step = int(tokens[0])
            pe = float(tokens[2])
            be = float(tokens[3])
            de = float(tokens[4])
            #===================================================================
            # re-weight the step
            #===================================================================
            if counter == 1:
                step_re =  int(tokens[0])
            else:
                step_re += math.exp(de/KT)*STEP
            #===================================================================
            # Output the results to out.csv
            #===================================================================
            if (counter-1)%skip == 0:
                o.write("%-20d,"%step)
                o.write("%20d,"%step_re)
                o.write("%20.4f,"%pe)
                o.write("%20.4f,"%be)
                o.write("%20.4f,"%de)
                o.write("\n")
        counter += 1
    o.close()
    f.close()
    
parse_out('test.out', 1000)
