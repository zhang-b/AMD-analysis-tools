import os
o = open('test.sh', 'w')
for i in range(20):
    folder = "r%02d"%i
    os.chdir(folder)
    f = open('host.log', 'r')
    fc = f.readlines()
    node = fc[0].strip()
    rf = fc[1].strip()
    o.write("""ssh %s '
echo $HOSTNAME':' `tail %s/water.mol >> ~/1898.log`
exit'
"""%(node, rf))

    os.chdir('..')
o.close()
