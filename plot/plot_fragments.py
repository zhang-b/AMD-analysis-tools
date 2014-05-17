
import os
import numpy as np
import matplotlib.pyplot as plt
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

def plot_fragments(folder, fragments, labels, ax, maxline=10000, datax=0, datay=1, tag1='', tag2=''):
    """
    plot the data
    """
    ax1 = ax.twinx()
    counter = 0
    n = 0
    
    os.chdir(folder)
    for i in fragments:
        data = parse_outcsv('%s.csv'%i, maxline, datax, datay)
        # Plot Data
        if "H2O1" in i:
            ax1.plot(data[0]/4000000.0, data[1], lw=1, color="black")
        else:     
            ax.plot(data[0]/4000000.0, data[1]+12-3*counter, lw=2, label=labels[n])
            n += 1
        counter += 1

    xmin = data[0][0]/4000000.0
    xmax = data[0][-1]/4000000.0

    ax.set_xlabel(tag1, size='x-large')

    ax.set_ylabel(r"Others ( N )", size='x-large')
    ax.set_xlim(xmin,xmax)
    ax.set_xlim(0,9)
    ax.set_ylim(0,40)
    ax.legend(loc=2)
    #ax1.plot([0,20], [66,66], ls='--')
    ax1.set_ylabel(r"H$_2$O ( N )", size='x-large')
    ax.set_title(tag2, size="x-large")


def main():
    gs = gridspec.GridSpec(5, 5)
    ax1 = plt.subplot(gs[0:2, 0:4])
    ax2 = plt.subplot(gs[2:4, 0:4])
    ax3 = plt.subplot(gs[4, 0:4])
    fragments = [ "H2O2_reweight", "H1O2_reweight", "H1O1_reweight", "H1_reweight_fill", "H2O1_reweight",]
    labels = ["H$_2$O$_2$", "HO$_2$", "OH", "H", "H$_2$O"]
    plot_fragments('/temp1/inprogress/1898/a00/r03', fragments, labels, ax1, 80000, 0, 1, "BF-RMD")
    plot_fragments('/temp1/inprogress/1898/a20_all/r03', fragments, labels, ax2, 80000, 0, 1, "aARRDyn")
    plt.show()

if __name__ == "__main__":
    main()

