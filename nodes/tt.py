import os
import time

for i in range(24843, 24863):
    os.system("qdel %d"%i)
    time.sleep(60)
