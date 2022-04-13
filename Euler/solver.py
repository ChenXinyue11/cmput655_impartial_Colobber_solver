#import NimberAlgorithms
from NimberAlgorithmsOrdering2d import *
#from NimberAlgorithmsOrderingParallel import *
from clobber_1d_im import *
from clobber_2d_im import *
from cut import *
import time, random, TT

def negamaxBoolean(state):
    if state.endOfGame():
        return False
    for m in state.legalmoves_impartial():
        state.play(m)
        success = negamaxBoolean(state)
        state.undoMove()
        if not success:
            return True
    return False

def nimberChoices(s):
    R = []
    for i in range(len(s.legalmoves_impartial())+1):
        R.append(i)
    return(R)

def randomPosition3(l):
    position = ""
    for i in range(l):
        random_num = random.randint(0, 2)
        if random_num == 0:
            position = position + "B"
        elif random_num == 1:
            position = position + "W"
        else:
            position = position + "."
    return(position)

def randomPositions(n, l):
    positions = []
    for i in range(n):
        positions.append(randomPosition3(l))
    return(positions)

if __name__ == "__main__":
    tt = TT.TranspositionTable()
    for i in range(20):
        p = randomPosition3(7) + "/" + randomPosition3(7)#row 0,1 in same length
        s = Clobber_2d(p)
        
        print(Clobber_2d.to_string(s.board))
        start = time.time()
        print("Nimber:", A3(s, tt))
        elapsed = time.time()-start
        print("time:", "{0:.4f}".format(elapsed))
        print("=====================")
    """
        start = time.time()
        print()
        elapsed = time.time()-start
        print("time:", "{0:.4f}".format(elapsed))
        t1 += elapsed
        print()

        start = time.time()
        print()
        elapsed = time.time()-start
        print("time:", "{0:.4f}".format(elapsed))
        t2 += elapsed
        print("==================")
    """
    #print("avg. sort:", t1/n)
    #print("avg. not sort:", t2/n)

