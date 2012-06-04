"""
@version: $0.1$
@author: Tao Cheng
@contact: chengtao@sjtu.edu.cn
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import os

from matplotlib.ticker import MultipleLocator
import matplotlib.gridspec as gridspec



def parse_outcsv(fname, nmax=10000, x=0, y=1, skip=1):
    """
    parse the out.csv
    @param fname: input filename
    @return: list
    """
    data = [[],[]]
    f = open(fname, 'r')
    counter = 0
    for i in f:
        if counter < nmax:
            if counter % skip == 0:
                tokens = [j.strip() for j in i.strip().split(',')]
                if len(tokens) >= y+1:
                    data[0].append(int(tokens[x]))
                    data[1].append(float(tokens[y]))
        counter += 1
    data = np.array(data)
    return data

FOLDER = """
/home/sungroup/Documents/amd/sim/rc/amd/a1498/run
/home/sungroup/Documents/amd/sim/rc/induce/a1498/run
/home/sungroup/Documents/amd/sim/rc/amd/a1898/run
/home/sungroup/Documents/amd/sim/rc/induce/a1898/run
"""
def plot_time():
    """
    plot the real simulation time (reweighted simulation time) as a function of MD simulation time
    """
    folder = [i.strip() for i in FOLDER.strip().split('\n')]
    fig = plt.figure()
    
    gs = gridspec.GridSpec(4,5)
    gs.update(wspace=0.50, hspace=0.50)
    
    for i in folder[2:3]:
        os.chdir(i)
        for j in range(20):
            ax = fig.add_subplot(gs[j])
            os.chdir("r%02d"%j)
            data = parse_outcsv("out.csv", 10000, 0, 1, 10)
            ax.loglog(data[0]/4000000.0, data[1]/4000000.0, color='black')
            ax.loglog([0.01,5], [0.01,5], color='black', ls=':')
            ax.set_xlim(data[0][0]/4000000.0, data[0][-1]/4000000.0)
            ax.set_ylim(data[1][0]/4000000.0, data[1][-1]/4000000.0)
            x = data[0][int(len(data[0])/100)]/4000000.0
            y = data[1][int(len(data[1]) - len(data[1])/1.2)]/4000000.0
            #print x, y
            ax.annotate(chr(65+j), xy=(x, y), xycoords='data')
            os.chdir("..")
    #plt.tight_layout()
    plt.show()

def plot_fragments(fragment):
    """
    plot the fragment as a function of time, and compare the result of AMD and MD 
    """
    folder = [i.strip() for i in FOLDER.strip().split('\n')]
    fig = plt.figure()
    gs = gridspec.GridSpec(4,5)
    gs.update(wspace=0.30, hspace=0.30)
    for i in range(20):
        ax = fig.add_subplot(gs[i])
        for j in folder[2:4]:
            os.chdir(j)
            os.chdir("r%02d"%i)
            #print os.getcwd()
            data = parse_outcsv("%s.csv"%fragment, 10000)
            if 'induce' in j:
                ax.plot(data[0]/4000000.0, data[1], color='black', ls=':')
            else:
                ax.plot(data[0]/4000000.0, data[1], color='black')
            os.chdir("..")
        ax.set_xlim(0, 2.5)
        ax.set_ylim(-10, 70)
        ax.annotate(chr(65+i), xy=(2, 10), xycoords='data')
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(20))
            
    #plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    #plot_time() 
    plot_fragments('H2O1')   
    