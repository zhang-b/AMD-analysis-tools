import os
import numpy as np
import matplotlib.pyplot as plt

from plot_time import parse_outcsv
from plot_time import FOLDER
from matplotlib.ticker import MultipleLocator

def parse_booste():
    bes = []
    tmp = []
    f = open('out.csv', 'r')
    counter = 0
    for i in f:
        if counter < 10000:
            if counter%1 == 0:
                tokens = i.strip().split(',')
                if len(tokens) > 4:
                    step = int(tokens[0])
                    be = float(tokens[3])
                    if be < -99999999:
                        if len(tmp) > 0:
                            bes.append(tmp)
                        tmp = []
                    else:
                        tmp.append([step, be])
        counter += 1
    return bes            

fig = plt.figure()
ax1 = fig.add_subplot(211)
bes = parse_booste()
tmp = []
energy = parse_outcsv('out.csv', 8000, 0, 2)
ax1.plot(energy[0]/4000000.0, energy[1], color='gray', alpha=1)
for i in bes:
    tmp = np.array(i)
    tmp = tmp.transpose()
    ax1.plot(tmp[0]/4000000.0, tmp[1],color='black', lw=2)
    ax1.fill_between(tmp[0]/4000000.0, tmp[1], -16500, facecolor='gray', alpha=0.4, edgecolor='')
ax1.set_xlim([0,2])
#ax1.set_ylim([-16500, -11000])
ax1.set_ylabel("Potential Energy ( kcal/mol )", size='x-large')
ax1.text(1.8, -11700, 'A', size='xx-large')

ax2 = fig.add_subplot(414)
delta = parse_outcsv('out.csv', 8000, 0, 4, 10)
ax2.plot(delta[0]/4000000.0, delta[1], color='black', alpha=0.7)
ax2.set_xlim([0,2])
ax2.yaxis.set_major_locator(MultipleLocator(15))
ax2.set_ylabel("$\Delta V$ ( kcal/mol )", size='x-large')
ax2.set_xlabel("Simulation Time ( ns )", size='x-large')
ax2.text(1.8, 18, 'C', size='xx-large')

"""
fragments = ["H1", "H1O1", "H1O2", "H3O1", "O1"]
tmp = np.array([])
counter = 0
for i in fragments:
    if counter == 0:
        tmp = parse_outcsv('%s.csv'%i, 8000, 0, 1, 10)
    else:
        tmp += parse_outcsv('%s.csv'%i, 8000, 0, 1, 10)
    counter += 1
ax3 = fig.add_subplot(413)
ax3.plot(tmp[0]/4000000.0/counter, tmp[1], color='black', alpha=0.7)
ax3.set_xlim([0,2])
ax3.set_ylabel("N", size='x-large')
ax3.yaxis.set_major_locator(MultipleLocator(2))
ax3.text(1.8, 3, 'B', size='xx-large')
"""
plt.show()
