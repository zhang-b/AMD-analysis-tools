import os
import numpy as np
import matplotlib.pyplot as plt

FRAGMENTS = [
"H2O2",
"H1O2",
"H3O1",
"H1O1",
"H1",
"H2O1",
]

from plot_time import parse_outcsv
from plot_time import FOLDER

def plot_fragments(nfolder, sample, fig, ax, maxline=10000, datax=0, datay=1, tag=''):
    folders = [i.strip() for i in FOLDER.strip().split('\n')]
    folder = os.path.join(folders[nfolder], sample)
    ax1 = ax.twinx()
    counter = 0
    
    os.chdir(folder)
    for i in FRAGMENTS:
        data = parse_outcsv('%s.csv'%i, maxline, datax, datay)
        # Plot Data
        if i == "H2O1":
            ax1.plot(data[0]/4000000.0, data[1], color='gray', lw=3)
        else:     
            ax.plot(data[0]/4000000.0, data[1]+15-3*counter, color='black')
        counter += 1

    xmin = data[0][0]/4000000.0
    xmax = data[0][-1]/4000000.0

    ax.set_xlabel(r"Time ( ns)", size='xx-large')
    ax.set_ylabel(r"Others ( N )", size='xx-large')
    ANNOTATE = ['$H_1$', '$H_1O_1$', '$H_3O_1$', '$H_1O_2$','$H_2O_2$' ]
    for j in range(len(ANNOTATE)):
        x = 0.7*(xmax - xmin)
        y = 4.2 + j*3.0
        ax.annotate(ANNOTATE[j], xy=(x, y), xycoords='data', size='large', style='italic')
    #ax.annotate(r'MD', xy=(0.15*(xmax-xmin), 35.0), xycoords='data', size='xx-large', )
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(0,40)
    ax1.plot([0,20], [66,66], color='black', ls='--')
    ax1.set_ylabel(r"$H_2O$ ( N )", size='xx-large')

fig = plt.figure()
ax2 = fig.add_subplot(211)
plot_fragments(3, 'r04', fig, ax2, 80000, 0, 1)
ax1 = fig.add_subplot(212)
plot_fragments(2, 'r04', fig, ax1,10000, 0, 1)
plt.show()