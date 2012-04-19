def find_reactions():
    prev = ''
    now = ''
    counter = 0
    of = open('reactions.csv', 'w')
    f = open("fragment.csv", 'r')
    for i in f:
        if counter == 0:
            global MOLTYPES
            MOLTYPES = i.split(',')[1:] 
            for i in range(len(MOLTYPES)):
                MOLTYPES[i] = MOLTYPES[i].strip()           
        else:
            step = i.split(',', 1)[0]
            line = i.split(',', 1)[1]
            if len(prev) == 0:
                prev = line
            now = line
            if now != prev:
                parse_reactions(step, prev, now, of)
            prev = now
        counter += 1
    of.close()

def parse_reactions(step, prev, now, of):
    rec = []
    pro = []
    r1 = prev.strip().split(',')
    r2 = now.strip().split(',')
    for i in range(len(r1)):
        if r1[i] != r2[i]:
            n = int(r1[i])-int(r2[i])
            mol = MOLTYPES[i]
            if n > 0:
                rec.append("%d%s"%(n, mol))           
            else:
                pro.append("%d%s"%(-n, mol))
    rec.sort()
    pro.sort()
    reaction = ''
    reaction += ' + '.join(rec)        
    reaction += ' = '        
    reaction += ' + '.join(pro)        
    reaction += '\n'
    of.write(reaction)
    
find_reactions()

