"""
reweight the fragments to real time
python reweight_fragments.py csvfile
@ note: need water.Timetable
"""
import sys

def read_csv(fname):
    data = [[], []]
    f = open(fname, "r")
    for i in f:
        tokens = i.strip().split(",")
        step = int(tokens[0])
        nmol = int(tokens[1])
        data[0].append(step)
        data[1].append(nmol)
    return data

def main():
    fname = sys.argv[1]
    output = fname[:-4] + "_reweight.csv"
    moldata = read_csv(fname)
    o = open(output, "w")
    f = open("water.timeTable", "r")
    n = 0
    for i in f:
        tokens = i.strip().split()
        tsim = int(tokens[0])
        treal = float(tokens[1])
        if n < len(moldata[0]):
            if tsim == moldata[0][n]:
                o.write("%50.4f,%10d\n"%(treal, moldata[1][n]))
                n += 1
    o.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
    else:
        main()
