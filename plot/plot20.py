import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

for i in range(20):

    ax = fig.add_subplot(4,5,i+1)

    data = np.loadtxt('_state_partition1_jobs_chengtao_amd_1898_r%02d_.out'%i, skiprows=1)
    data = data.transpose()

    x = data[0]
    y = data[2]

    ax.plot(x[:44000], y[:44000])

    data = np.loadtxt('_state_partition1_jobs_chengtao_induce_1898_r%02d_.out'%i, skiprows=1)
    data = data.transpose()

    x = data[0]
    y = data[2]

    ax.plot(x[:44000], y[:44000])

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')

plt.show()
