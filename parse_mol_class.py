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

class Frames:
    """
    Containor of Frame (class)
    """
    def __init__(self,):
        self.molfile = ''
        """
        @ivar: file name of mol file
        @type: text
        """
        self.outfile = ''
        """
        @ivar: file name of mol file
        @type: text
        """
        self.frames = []
        """
        @ivar: list of Frame
        @type: list of Frame
        """
        self.nframes = 0
        """
        @ivar: total number of frames in simulation
        @type: int
        """        
        self.steps = []
        """
        @ivar: list of boost energy parameters
        @type: list of float
        """
        self.blocks = []
        """
        @ivar: list of brute mol information
        @type: list of text
        """
        self.energy = []
        """
        @ivar: list of potential energy
        @type: list of float
        """
        self.de = []
        """
        @ivar: list of biased energy
        @type: list of float
        """
        self.df = []
        """
        @ivar: list of biased force scale parameters
        @type: list of float
        """
        self.be = []
        """
        @ivar: list of boost energy parameters
        @type: list of float
        """
    def init_frames(self,):
        self.steps = self.parse_out(12, 0, 1)
        for i in range(len(self.steps)):
            tmp = Frame()
            tmp.nframe = self.steps[i]
            self.frames.append(tmp)
        self.nframes = i + 1

    def parse_mol(self,):
        """
        parse water.mol to plain text. The format is 'step', 'molinfo 1',
        'molinfo 2', ... 'molinfo n'.
        @param fname: file to open
        @retrun: list
        @todo: extend to a general file reading method
        """
        f = open(self.molfile, 'r')
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
       
    def parse_blocks(self, ):
        """parse the mol info in blocks to frames
        @param blocks: list generate from parse_mol
        @return: list with Class Frame element
        """
        blocks = self.parse_mol()
        for i in range(len(blocks)):
            for j in blocks[i][1:]:
                tokens = j.split()
                mol = tokens[2]
                nmol = int(tokens[0])
                self.frames[i].mol[mol] = nmol

    def parse_out(self, rows, row, skip):
        """parse the energy term from out file
        @param fname: input file name.
        @param rows: total rows in file
        @param row: selected term
        @param skip: step to read energy
        @return: energy list
        """
        data = []
        counter = 0
        f = open(self.outfile, 'r')
        for i in f:
            tokens = i.strip().split()
            if len(tokens) == rows:
                #skip the first line
                if counter > 1:
                    step = int(tokens[0])
                    if step%skip==0:
                        data.append(float(tokens[row]))
            counter += 1
        return data
    
    def assign_terms(self, key):
        """assign energy and force terms to frames
        @todo: This function should be merged with assign_energy
        @note: the length of frames and that of energy must be the same
        """
        if key == 'potential energy':
            n = 2
        elif key == 'boost energy':
            n = 3
        elif key == 'biased energy':
            n = 4
        elif key == 'force scale factor':
            n = 5
        else:
            print "warning: No terms selected"
        data = self.parse_out(12, n, 1)
        if len(self.frames) == len(data):
            for i in range(len(self.frames)):
                if n == 2:
                    self.frames[i].energy = data[i]
                elif n == 3:
                    self.frames[i].be = data[i]
                elif n == 4:
                    self.frames[i].de = data[i]
                elif n == 5:
                    self.frames[i].df = data[i]
                else:
                    print "Error: inconsistent energy data %d and mol data %d"
        
    def output_terms(self, key):
        """ Output the energy information from Frames
        @note: The default file name is ener.csv
        """
        if key == 'potential energy':
            fname = 'potential_energy.csv'
        elif key == 'boost energy':
            fname = 'boost_energy.csv'
        elif key == 'biased energy':
            fname = 'biased_energy.csv'
        elif key == 'force scale factor':
            fname = 'force_scale_factor.csv'
        else:
            print "warning: no selected terms"
            
        o = open(fname, 'w')
        for i in self.frames:
            if key == 'potential energy':
                val = i.energy
            elif key == 'boost energy':
                val = i.be
            elif key == 'biased energy':
                val = i.de
            elif key == 'force scale factor':
                val = i.df
            o.write("%-10d,%20.6f\n"%(i.nframe, val))
        o.close()
        
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
    simFrames = Frames()
    simFrames.outfile = 'water.out'
    simFrames.init_frames()
    #simFrames.assign_terms("potential energy")
    #simFrames.output_terms("potential energy")
    #simFrames.assign_terms("boost energy")
    #simFrames.output_terms("boost energy")
    #simFrames.assign_terms("biased energy")
    #simFrames.output_terms("biased energy")
    #simFrames.assign_terms("force scale factor")
    #simFrames.output_terms("force scale factor")
    simFrames.molfile = 'water.mol'
    simFrames.parse_blocks()
    
def main2():
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
