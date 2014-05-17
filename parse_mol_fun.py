#!/usr/bin/env python
"""
@version: $0.1$
@author: Tao Cheng
@contact: chengtao@sjtu.edu.cn
"""

import operator

def parse_mol_fun(fname):
    """
    parse water.mol to plain text. The format is 'step', 'molinfo 1',
    'molinfo 2', ... 'molinfo n'.
    - read fragments information from water.mol
    - generate the fragments distribution and obtain all the fragment types
    - parse the blocks and count the fragment numbers in each time step
    - output the fragments information to fragment.csv
    @param fname: file to open
    @return: list
    @todo: extend to a general file reading method
    """
    f = open(fname, 'r')
    flag = True
    block = []
#===============================================================================
# - Generate the fragment distributions and obtain a dictionary of {fragment : n}
# - Sort the dictionary and obtain an ascending sequence nst
# - Output the head of fragment.csv
#===============================================================================
    fragments = gen_distribute(fname)
    nst = sort_fragments(fragments, len(fragments))
    fragments_output = open("fragment.csv", 'w')
    fragments_output.write("%-20s,"%'step')
    for i in nst:
        fragments_output.write("%5s,"%i)
    fragments_output.write('\n')

#===============================================================================
# parse the blocks according to 'step' flag and blank flag
#===============================================================================
    while(flag):
        flag = False
        for i in f:
            flag = True
            if i.strip().startswith('step'):
                if len(block) == 0:
                    # append step to list as the first element
                    block.append(i.strip().split()[0][4:])
                else:
                    output_fragment(fragments_output, block, nst)
                    block = []
                    # append step to list as the first element
                    block.append(i.strip().split()[0][4:])
                break
            # ignore the white lines
            elif len(i.strip()) < 1:
                pass
            else:
                block.append(i.strip())
    output_fragment(fragments_output, block, nst)
    fragments_output.close()

def output_fragment(of, block, fragments):
    fragment_block = {}
    for i in fragments:
        fragment_block[i] = 0
    for i in block[1:]:
        tokens = i.split()
        frag = tokens[-1]
        n = int(tokens[0])
        fragment_block[frag] = n
    step = int(block[0])
    of.write("%-20d,"%step)
    for i in fragments:
        #print fragment_block[i]
        of.write("%5d,"%int(fragment_block[i]))
    of.write('\n')
        
        
    
def gen_distribute(fname):
    """
    Generate a distribution of fragment
    @param fname: file to open
    @retrun: dictionary
    @todo: extend to a general file reading method
    """
    fragments = {}
    f = open(fname, 'r')
    for i in f:
        if len(i.strip()) < 1:
            pass
        elif i.strip().startswith('step'):
            pass
        else:
            tokens = i.strip().split()
            frag = tokens[2]
            n = int(tokens[0])
            if frag in fragments.keys():
                fragments[frag] += n
            else:
                fragments[frag] = n
    f.close()
    o = open('distribute.csv', 'w')
    for (i,j) in fragments.items():
        o.write("%-8s,%20d\n"%(i,j))
    o.close()
    
    return fragments

def sort_fragments(fragments, n):
    """
    sort the fragments (dictionary) according to the number of n
    @param fragments: fragments dictionary
    @param n: only output the first n fragments
    @return: a list nst
    """
    nst = []
    sorted_fragments = sorted(fragments.iteritems(), key=operator.itemgetter(1))
    if n > len(sorted_fragments):
        print "Error: "
    else:
        for i in range(len(sorted_fragments)-n, len(sorted_fragments)):
            nst.append(sorted_fragments[i][0])
    return nst

def parse_fragment(fragment, skip):
    f = open('fragment.csv', 'r')
    o = open('%s.csv'%fragment, 'w')
    counter = 0
    for i in f:
        if counter == 0:
            header = [j.strip() for j in i.strip().split(',')]
            n = header.index(fragment)
            print header
        else:
            tokens = i.strip().split(',')
            if (counter-1)%skip == 0:
                o.write("%-12d,%12d\n"%(int(tokens[0]), int(tokens[n])))
        counter += 1
    o.close()
    f.close()
                    
parse_mol_fun('water.mol')

FRAGMENTS = ['H2O1', 'H2', 'O2', 'H2O2', 'H1', 'O1', 'H1O2', 'H1O1', ]
#FRAGMENTS = ['H3O1']
#FRAGMENTS = ["C3H6O3"]
#FRAGMENTS = ['C1026H102', 'C3H9N4', 'C1026H102N2', 'C2H6N4', 'C1H3N4', 'C1024H96', 'C1025H99', 'C2H6', 'C1025H99N2', 'C3H9N2', 'N2', 'C1H3N2', 'C2H6N2', 'C1H3']
#FRAGMENTS = ['O2', "O1"]
for i in FRAGMENTS:
    parse_fragment(i, 1)

