import sys
import numpy as np

for i in sys.argv[1:]:
    data = np.genfromtxt(i, delimiter=',')
    data = data.transpose()
    sum = data[1].sum()
    print i, sum
