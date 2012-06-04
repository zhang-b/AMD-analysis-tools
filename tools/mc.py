import math

BETA = 1 /(8.314 * 798 / 4184)

def parse_accept(filename):
    frames = []
    f = open(filename, 'r')
    for i in f:
        tokens = i.strip().split()
        if len(tokens) == 15:
            if tokens[-1] == 'accept':
                frames.append([int(tokens[1]), float(tokens[-2])])
    f.close()
    return frames

def find_max(frames):
    max = 0
    for i in frames:
        if i[1] > max:
            max = i[1]
    return max

def parse_trj(filename):
    coords = []
    f = open(filename, 'r')
    frame = []
    counter = 0
    for i in f:
        tokens = i.strip().split()
        if i.strip().startswith('198') and len(i.split()) == 1:
            if len(frame) > 0:
                coords.append(frame)
            frame = []
            counter = 0
        if counter > 1:
            frame.append(tokens)
        counter += 1
    coords.append(frame)
    f.close()
    return coords

def ave_coords(frames, demean, coords):
    avec = []
    sumall = 0
    for i in range(len(coords[0])):
        avec.append([0, 0, 0, coords[0][i][0]]) 
    for i in frames:
        for j in range(len(coords[0])):
#            print j, i[0], i[1]
#            print len(coords)
#            print coords[i[0]][j][0]
#            print i[1], demean, i[1]-demean
            avec[j][0] += float(coords[i[0]][j][1]) * math.exp(BETA *(i[1]-demean))
            avec[j][1] += float(coords[i[0]][j][2]) * math.exp(BETA *(i[1]-demean))
            avec[j][2] += float(coords[i[0]][j][3]) * math.exp(BETA *(i[1]-demean))
        sumall += math.exp(BETA *(i[1]-demean))
    for i in range(len(avec)):
        avec[i][0] = avec[i][0] / sumall
        avec[i][1] = avec[i][1] / sumall
        avec[i][2] = avec[i][2] / sumall
    return avec

def output_xyz(coords):
    o = open('out.xyz', 'w')
    for i in coords:
        o.write('%10.4f%10.4f%10.4f\n'%(i[0], i[1], i[2]))
    o.close()

def output_pdb(coords):
    o = open('../md/ave', 'w')
    o.write('CRYST1   25.000   25.000   25.000  90.00  90.00  90.00              0\n')
    'ATOM      1    O REX     1       3.282  15.582  16.944  1.00  0.00      0    O'
    counter = 1
    for i in coords:
        o.write('ATOM%7d%5s REX     1'%(counter, i[-1]))
        o.write('%12.3f%8.3f%8.3f'%(i[0], i[1], i[2]))
        o.write('  1.00  0.00      0%5s\n'%i[-1])
        counter += 1
    o.close()

def main():
    afs = parse_accept('accept.log')
    demax = find_max(afs)
    coords = parse_trj('water.trj')
#    print coords[198][-1]
    avec = ave_coords(afs, demax - 1000, coords)
    output_xyz(avec)
    output_pdb(avec)

def test():
    for i in range(10000):
        print i
        math.exp(BETA * i)

if __name__ == '__main__':
    main()
