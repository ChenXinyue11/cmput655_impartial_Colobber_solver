import TT
from clobber_1d_im import *
tt = TT.TranspositionTable()

def is_losing_ETC(s, n, depth=0):
    v = tt.lookup(Clobber_1d.to_string(s.board))
    if v != None:
        return(v==n)
    M = []
    moves = s.legalmoves_impartial()
    for m in moves:
        s.play(m)
        v = tt.lookup(Clobber_1d.to_string(s.board))
        s.undoMove()
        if v != None:
            if v == n:
                return(False)
        else:
            M.append(m)
    for i in range(n):
        if is_losing_ETC(s, i, depth+1):
            return(False)
    for m in M:
        s.play(m)
        if is_losing_ETC(s, n, depth+1):
            s.undoMove()
            return(False)
        s.undoMove()
    tt.store(Clobber_1d.to_string(s.board), n)
    return(True)

def nim_is_losing_ETC(s):
    n = 0
    while(not is_losing_ETC(s, n)):
        n += 1
    return(n)
