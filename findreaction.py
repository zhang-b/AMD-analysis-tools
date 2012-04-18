
#----------------read-mol-fractions---------------------#
mol = {}

f = open('water.mol')
# step4277 fragments

state = 'True'
while( state == 'True'):
    state = 'False'
    for i in f:
        state = 'True'
        if "fragments" in i:
            step = int(i.split()[0][4:])
            mol[step] = []
        elif len(i.strip()) == 0:
            #sort the data according mol name
            for tmp in range(len(mol[step])):
                tokens = mol[step][tmp].split()
                mol[step][tmp] = "%s %s"%(tokens[2], tokens[0])
            mol[step].sort()
            break
        else:
            mol[step].append(i.strip())

f.close()

#--------------read-energy------------------------------#
ener = {}
f = open('accept.log', 'r')
for i in f:
    if len(i.strip()) > 0:
        if i.strip().endswith('accept'):
            ener[int(i.split()[1])] = [i.split()[3], i.split()[5]]
f.close()
#-------------summary-----------------------------------#
lines = []
for i in mol.keys():
    # if > 2 reaction if == 2 no reaction
    if len(mol[i]) == 2:
        line = ''
        if i in ener.keys():
            for j in range(len(mol[i])):
                line +="%s "%mol[i][j]
            line += " && "
            line += "%d %s %s\n"%(i, ener[i][0], ener[i][1],)
        lines.append(line)
#lines.sort()
print len(lines)
#--------------split reaction----------------------------#
reac = ''
counter = 0

o = open('test.log', 'w')
for i in lines:
    o.write(i)

for i in lines:
    if len(i.strip()) > 0:
        tokens = i.split('&&')
        if reac == tokens[0]:
            print "I am right!!"
            o.write(i)
        else:
            reac = tokens[0]
            o.close()
            o = open('%s.log'%reac.strip().replace(' ', '_'), 'w')
o.close()

