import math
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

for i in range(20):

    ax = fig.add_subplot(4,5,i+1)

    data = np.loadtxt('_state_partition1_jobs_chengtao_amd_1498_r%02d_.out'%i, skiprows=1)
    data = data.transpose()

    x = data[0]
    y = data[2]
    dy = data[4]

    rx = []
    ry = []
    step = 0
    counter = 0
    for j in range(len(dy)):
        if counter < 200:
            pass
        else:
            step += math.exp(dy[j]/8.314/1498*4814)*1000
            rx.append(step)
            ry.append(y[j])
        counter += 1

    ax.plot(x[:40000]-40000, y[:40000])
    ax.plot(rx[:4000], ry[:4000])

    data = np.loadtxt('_state_partition1_jobs_chengtao_induce_1498_r%02d_.out'%i, skiprows=1)
    data = data.transpose()

    x = data[0]
    y = data[2]

    ax.plot(x[:40000], y[:40000])

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')
    ax.set_xlim(x[0], x[40000])

plt.show()
