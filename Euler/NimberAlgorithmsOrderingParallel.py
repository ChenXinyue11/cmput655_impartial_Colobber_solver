"""
Algorithms from Nimbers Are Inevitable

"""

import operator, multiprocessing, TT
from clobber_1d_im import *

ifparallel = False
tt = TT.TranspositionTable()

def A2(subgame_list, n):
    global ifparallel
    nimsum = n
    if ifparallel:
        print("ifparallel:", ifparallel)
        ifparallel = False
        pool = multiprocessing.Pool(4)
        results = pool.map(A3, subgame_list[:-1])
        pool.close()
        for i in results:
            nimsum = nimsum^i
        pool.terminate()
        return(A1(subgame_list[-1], nimsum))
    else:
        for i in range(len(subgame_list)-1):
            nimber = A3(subgame_list[i])
            nimsum = operator.xor(nimsum,nimber)
        outcome = A1(subgame_list[-1], nimsum)
    return(outcome)

def A3(position_str, parallel=False):
    global ifparallel, tt
    if splittable(position_str) and parallel:
        ifparallel = parallel
    n = 0
    result = tt.lookup(position_str)
    if result != None:
        return result
    while (A1(position_str, n)) == 1:
        n += 1
    tt.store(position_str, n)
    return(n)

def moves_nimber(nimber):
    moves = []
    for i in range(nimber):
        moves.append(i)
    return(moves)

def splittable(position):
    if "." in position:
        return(True)
    return(False)
   
def A1(position, n):
    if Clobber_1d(position).endOfGame() and n == 0:
        return(0)
    result = tt.lookup(position)
    if result != None:
        #print("in 1")
        if result == n:
            return(0)
        else:
            return(1)
    if splittable(position):
        position_list = list(filter(None, position.split(".")))
        if len(position_list) == 1:
            return(A1(position_list[0], n))
        return(A2(position_list, n))
    else:
        moves = Clobber_1d(position).legalmoves_impartial()
        center_moves = [moves[(len(moves) + (~i, i)[i%2]) // 2] for i in range(len(moves))]
        for move in center_moves:
            #new_position = result_position(position, move)
            game = Clobber_1d(position)
            game.play(move)
            game_str = Clobber_1d.to_string(game.board)
            result = A1(game_str, n)
            #position.undoMove()
            
            if result == 0:
                return(1)
        for move in moves_nimber(n):
            if A1(position, move) == 0:
                return(1)
        return(0)

