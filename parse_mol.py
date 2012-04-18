#!/usr/bin/env python
"""
@version: $0.1$
@author: Tao Cheng
@contact: chengtao@sjtu.edu.cn
"""
import numpy as np
import copy
import math 

TEMPERATURE = 1898
BETA = 1/(8.314*TEMPERATURE/4184)

class Frame:
    """Basic class of frame info
    """
    def __init__(self,):
        self.nframe = 0
        """
        @ivar: frame step
        @type: int
        """
        self.energy = 0
        """
        @ivar: frame energy
        @type: real
        """
        self.de = 0
        """
        @ivar: frame amd delta energy
        @type: real
        """
        self.be = 0
        """
        @ivar: frame boost energy
        @type: real
        """
        self.df = 0
        """
        @ivar: frame force scale factor
        @type: real
        """
        self.mol = {}
        """
        @ivar: frame mol info
        @type: dict
        """
        self.mol_re = {}
        """
        @ivar: reweighted frame mol info
        @type: dict
        """
    def reweight(self,):
        """reweight the mol info according to energy
        @note: reweight should be after energy normalization
        """
        self.mol_re = copy.copy(self.mol)
        if self.de < -10*BETA:
            #print 'less ', self.nframe, self.energy
            scale = 0
        elif self.de > 7/BETA:
            scale = 1
        else:
            #print 'more ', self.nframe, self.energy
            scale = math.exp(self.de*BETA)
        for i in self.mol_re.keys():
            self.mol_re[i] = self.mol_re[i]*scale

def parse_mol(fname):
    """
    parse water.mol to plain text. The format is 'step', 'molinfo 1',
    'molinfo 2', ... 'molinfo n'.
    @param fname: file to open
    @retrun: list
    @todo: extend to a general file reading method
    """
    f = open(fname, 'r')
    flag = True
    blocks = []
    block = []

    while(flag):
        flag = False
        for i in f:
            flag = True
            if i.strip().startswith('step'):
                if len(block) == 0:
                    # append step to list as the first element
                    block.append(i.strip().split()[0][4:])
                else:
                    blocks.append(block)
                    block = []
                    # append step to list as the first element
                    block.append(i.strip().split()[0][4:])
                break
            # ignore the white lines
            elif len(i.strip()) < 1:
                pass
            else:
                block.append(i.strip())
    blocks.append(block)

    return blocks

def parse_blocks( blocks ):
    """parse the mol info in blocks to frames
    @param blocks: list generate from parse_mol
    @return: list with Class Frame element
    """
    frames = []
    for i in blocks:
        tmp = Frame()
        tmp.nframe = int(i[0])
        for j in i[1:]:
            tokens = j.split()
            mol = tokens[2]
            nmol = int(tokens[0])
            tmp.mol[mol] = nmol
        frames.append(tmp)
    return frames

def parse_out(fname, rows, row, skip):
    """parse the energy term from out file
    @param fname: input file name.
    @param rows: total rows in file
    @param row: selected term
    @param skip: step to read energy
    @return: energy list
    """
    energy = []
    counter = 0
    f = open('water.out', 'r')
    for i in f:
        tokens = i.strip().split()
        if len(tokens) == rows:
            #skip the first line
            if counter > 1:
                step = int(tokens[0])
                if step%skip==0:
                    energy.append(float(tokens[row]))
        counter += 1
    return energy

def mol_time(frames):
    """ organize the fragment info from frames to mol 
    @return: two dictionary: mol info and mol info after reweight
    """
    mol = {}
    for i in frames:
        for j in i.mol.keys():
            if j not in mol.keys():
                mol[j] = []
            mol[j].append([i.nframe, i.mol[j]])

    mol_re = {}
    for i in frames:
        for j in i.mol_re.keys():
            if j not in mol_re.keys():
                mol_re[j] = []
            mol_re[j].append([i.nframe, i.mol_re[j]])
    return mol, mol_re

def assign_de(frames, energy):
    """assign delta energy to frames
    @todo: This function should be merged with assign_energy
    @note: the length of frames and that of energy must be the same
    """
    if len(frames) == len(energy):
        for i in range(len(frames)):
            frames[i].de= energy[i]
    else:
        print "Error: inconsistent energy data %d and mol data %d"\
                %(len(energy), len(frames))

def assign_df(frames, energy):
    """assign delta force to frames
    @todo: This function should be merged with assign_energy
    @note: the length of frames and that of energy must be the same
    """
    if len(frames) == len(energy):
        for i in range(len(frames)):
            frames[i].df= energy[i]
    else:
        print "Error: inconsistent energy data %d and mol data %d"\
                %(len(energy), len(frames))

def assign_be(frames, energy):
    """assign boost energy to frames
    @todo: This function should be merged with assign_energy
    @note: the length of frames and that of energy must be the same
    """
    if len(frames) == len(energy):
        for i in range(len(frames)):
            frames[i].be= energy[i]
    else:
        print "Error: inconsistent energy data %d and mol data %d"\
                %(len(energy), len(frames))

def assign_energy(frames, energy):
    """assign delta energy to frames
    @todo: This function should be merged with assign_de
    @note: the length of frames and that of energy must be the same
    """
    if len(frames) == len(energy):
        for i in range(len(frames)):
            frames[i].energy= energy[i]
    else:
        print "Error: inconsistent energy data %d and mol data %d"\
                %(len(energy), len(frames))

def norm_de(frames):
    """normalize the delta energy in frames
    """
    maximum = -999999 
    for i in range(len(frames)):
        if maximum < frames[i].de:
            maximum = frames[i].de
        #print maximum
    for i in range(len(frames)):
        #print frames[i].nframe, frames[i].energy
        frames[i].de = frames[i].de- maximum
def output_energy(frames):
    """ Output the energy information from Frames
    @note: The default file name is ener.csv
    """
    o = open('ener.csv', 'w')
    for i in frames:
        o.write("%-10d,%20.6f\n"%(i.nframe, i.energy))
    o.close()

def output_terms(frames, oname):
    """ Output the terms selected from Frames
    @note: The default file name is ener.csv
    """
    o = open(oname, 'w')
    for i in frames:
        o.write("%-10d,%20.6f\n"%(i.nframe, i.energy))
    o.close()

def output_de(frames):
    """ Output the energy information from Frames
    @note: The default file name is ener.csv
    @todo: This function should be merged with output_energy()
    """
    o = open('de.csv', 'w')
    for i in frames:
        o.write("%-10d,%20.6f\n"%(i.nframe, i.de))
    o.close()

def write_dic(molinfo, surfix=''):
    """ output the fragment info as a function of time (dictionary) to csv file
    """
    for i in molinfo.keys():
        o = open("%s.csv"%(i+surfix), "w")
        for j in molinfo[i]:
            o.write('%-10d,%10.6f\n'%(j[0],j[1]))
        o.close()

def write_detail(molinfo, frames, surfix=''):
    """ output the detail fragment info as a function of time 
    (dictionary) to csv file, include step number delta E boost E
    @param molinfo: seperated mol infor dict
    @param frames: frames
    @param surfix: file name surfix
    """
    for i in molinfo.keys():
        o = open("%s.csv"%(i+surfix), "w")
        for j in molinfo[i]:
            n = j[0]/1000 -1
            if j[0] == frames[n].nframe:
                step = j[0]
                num = j[1]
                de = frames[n].de
                be = frames[n].be
                o.write('%-10d,%10d,%10.2f,%10.2f\n'%(step, num, de, be))
            else:
                print "warning"
        o.close()

def main():
    """
    @note: parse
    """
    blocks = parse_mol('water.mol') 
    frames = parse_blocks(blocks)
    #set skip to 100 to be consistent with information 
    #in mol file
    energy = parse_out('water.out', 12, 4, 1000)
    booste = parse_out('water.out', 12, 3, 1000)
    assign_de(frames, energy)
    output_de(frames)
    assign_be(frames, booste)
    #output detail mol information in seperated files.
    mol1, mol2 = mol_time(frames)
    write_detail(mol1, frames, surfix="_detail")
    #normalize the frames infor
    #norm_de(frames)
    for i in frames:
        i.reweight()
    mol1, mol2 = mol_time(frames)
    write_dic(mol1)
    write_dic(mol2, '_re')
    energy = parse_out('water.out', 12, 2, 1000)
    assign_energy(frames, energy)
    output_energy(frames)

    energy = parse_out('water.out', 12, 3, 1000)
    assign_energy(frames, energy)
    output_terms(frames, "booste.csv")

    energy = parse_out('water.out', 12, 5, 1000)
    assign_energy(frames, energy)
    output_terms(frames, "boostf.csv")

if __name__ == "__main__":
    main()
