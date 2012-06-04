import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('out.csv', delimiter=',')
data = data.transpose()

plt.plot(data[0][:400], data[2][:400])
plt.show()
