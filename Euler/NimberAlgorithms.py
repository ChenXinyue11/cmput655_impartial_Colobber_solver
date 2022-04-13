"""
Algorithms from Nimbers Are Inevitable

"""

#1 for win
#0 for loss

import operator
from clobber_1d_im import *

def A2(subgame_list, n,tt):
    position_list = subgame_list[:]
    position_list.sort(key=len)
    nimsum = n
    for i in range(len(position_list)-1):
        nimber = A3(Clobber_1d(position_list[i]),tt)
        nimsum = operator.xor(nimsum,nimber)
    outcome = A1(Clobber_1d(position_list[-1]), nimsum,tt)
    return(outcome)

def A3(position,tt):
    n = 0
    position_str = Clobber_1d.to_string(position.board)
    result = tt.lookup(position_str)
    if result != None:
        #print("in 3")
        return result
    while (A1(position, n,tt)) == 1:
        n += 1
    tt.store(position_str, n)
    return(n)

def moves_nimber(nimber):
    moves = []
    for i in range(nimber):
        moves.append(i)
    return(moves)

def splittable(position):
    if "." in Clobber_1d.to_string(position.board):
        return(True)
    return(False)
   
def A1(position, n,tt):
    position_str = Clobber_1d.to_string(position.board)
    if position.endOfGame() and n == 0:
        return(0)
    result = tt.lookup(position_str)
    if result != None:
        #print("in 1")
        if result == n:
            return(0)
        else:
            return(1)
    if splittable(position):
        position_list = list(filter(None, position_str.split(".")))
        if len(position_list) == 1:
            return(A1(Clobber_1d(position_list[0]), n,tt))
        return(A2(position_list, n,tt))
    else:
        moves = position.legalmoves_impartial()
        center_moves = [moves[(len(moves) + (~i, i)[i%2]) // 2] for i in range(len(moves))]
        for move in center_moves:
            #new_position = result_position(position, move)
            position.play(move)
            result = A1(position, n,tt)
            position.undoMove()
            
            if result == 0:
                return(1)
        for move in moves_nimber(n):
            if A1(position, move,tt) == 0:
                return(1)
        return(0)
