"""
@version: $0.1$
@author: Tao Cheng
@contact: chengtao@sjtu.edu.cn
"""

import matplotlib.pyplot as plt

class Outcsv():
    def __init__(self, fname='out.csv', skip=1):
        self.step = []
        self.step_re = []
        self.pe = []
        self.be = []
        self.de = []
        self.name = fname
        self.skip = skip
    def parse_csv(self):
        counter = 0
        f = open(self.name, 'r')
        for i in f:
            if counter%self.skip == 0:
                tokens = i.strip().split(',')
                self.step.append(int(tokens[0]))
                self.step_re.append(int(tokens[1]))
                self.pe.append(float(tokens[2]))
                self.be.append(float(tokens[3]))
                self.de.append(float(tokens[4]))
    
        