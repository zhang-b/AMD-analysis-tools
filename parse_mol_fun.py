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
    fragments = gen_distribute('water.mol')
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
        
parse_mol_fun('water.mol')





