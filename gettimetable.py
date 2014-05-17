"""
Reweight the boost with distribution
python gettimetable.py T(sim) T(ref) type(half or final)
"""
import math
import sys

class params():
    """
    parameters for the distribution function
    """
    def __init__(self,):
        self.y0 = 1.0
        self.x0 = 1.0
        self.A0 = 0.0
        self.t0 = 1.0
        self.y1 = 1.0
        self.A1 = 0.0
        self.t1 = 1.0
        self.r0 = 1.0

def fun(r, params):
    """
    distribution function
    """
    y0 = params.y0
    x0 = params.x0
    A0 = params.A0
    t0 = params.t0
    y1 = params.y1
    A1 = params.A1
    t1 = params.t1
    r0 = params.r0
    x = r
    if r >= r0:
        y = A0 * math.exp((x-x0)/t0) + y0
    else:
        y = A1 * math.exp((x)/t1) + y1
        if y > 20.0:
            y = 20.0
    return y

def init(T, Tref):
    """
    init parameters
    """
    scale = math.sqrt(T/Tref)
    hh = params()
    hh.y0 = 1.03747
    hh.x0 = 0.90943
    hh.A0 = 0.00389 
    hh.t0 = 0.02389 * scale
    hh.y1 = 0.96371
    hh.A1 = 5.87951e17
    hh.t1 = 0.01218 * scale
    hh.r0 = 0.75
    oo = params()
    oo.y0 = 1.03747
    oo.x0 = 0.90943
    oo.A0 = 0.00389 
    oo.t0 = 0.05189 * scale
    oo.y1 = 0.96371
    oo.A1 = 5.00000e17 
    oo.t1 = 0.01218 * scale
    oo.r0 = 1.25
    oh = params()
    oh.y0 = 1.00000
    oh.x0 = 1.00279
    oh.A0 = 0.01249
    oh.t0 = 0.04412 * scale
    oh.y1 = 1.00000
    oh.A1 = 6.99840e7
    oh.t1 = 0.03943 * scale
    oh.r0 = 0.95
    return  hh, oo, oh

def readhalf():
    f = open("half", "r")
    tokens = f.readline().strip().split()
    n1 = int(tokens[0])
    n2 = float(tokens[1])
    return n1, n2

def readfinal():
    f = open("final", "r")
    tokens = f.readline().strip().split()
    n1 = int(tokens[0])
    n2 = float(tokens[1])
    return n1, n2

def do_correct(n, hh, oo, oh):
    steps = 0.0
    counter = 0
    f = open("water.bboost", "r")
    o = open("water.timeTable", "w")
    for i in f:
        if counter == 0:
            pass
        else:
            tokens = i.strip().split()
            if len(tokens) == 10:
                step = int(tokens[0])
                r = float(tokens[5])
                bf = float(tokens[7])
                a1 = tokens[8]
                a2 = tokens[9]
                if a1 == "H" and a2 == "H":
                    par = hh
                elif a1 == "O" and a2 == "O":
                    par = oo
                else:
                    par = oh
                if bf > 1.0:
                    co = fun(r, par)
                else:
                    co = 1.0
                steps += co * bf
                o.write("%20d%50.3f\n"%(step, steps))
        if counter > n:
            break
        counter += 1
    o.close()
    return steps

def main():
    # setup the parameters
    T = float(sys.argv[1])
    Tref = float(sys.argv[2])
    simtype = sys.argv[3]
    hh, oo, oh = init(T, Tref)
    if simtype == "half":
        n, nreal = readhalf()
    elif simtype == "final":
        n, nreal = readfinal()
    else:
        pass
    steps = do_correct(n, hh, oo, oh)
    print steps, nreal, steps/nreal

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print __doc__
    else:
        main()
        
    
