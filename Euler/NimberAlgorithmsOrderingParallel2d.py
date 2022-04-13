"""
Algorithms from Nimbers Are Inevitable

"""

import operator, multiprocessing, TT
from clobber_2d_im import *

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
    s = Clobber_2d(position_str)
    if splittable_2d(s.board)[0] and parallel:
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

def balance_rows(break_point_diff, row0, row1):
    if break_point_diff > 0:
        row0_new = [0]*break_point_diff + row0
        row1_new = row1
    else:
        row0_new = row0
        row1_new = [0]*(-break_point_diff) + row1
    len_diff = len(row0_new) - len(row1_new)
    if len_diff > 0 :
        row1_new = row1_new + [0]*len_diff
    else:
        row0_new = row0_new + [0]*(-len_diff)
    return(Clobber_2d.to_string([row0_new, row1_new]))

def splittable_2d(position):
    position_str = position
    if len(position_str[0]) <= 2:
        return(False, None)
    sg_list = []
    break_point_row0 = 0
    break_point_row1 = 0
    for i in range(1, len(position_str[0])-1):
        sg = []
        if position_str[0][i] == 0:
            if position_str[1][i-1] == 0:
                break_point_diff = break_point_row0 - break_point_row1
                sg = balance_rows(break_point_diff, \
                                  position_str[0][break_point_row0:i], position_str[1][break_point_row1:i-1])
                break_point_row0 = i + 1
                break_point_row1 = i
                sg_list.append(sg)
            elif position_str[1][i] == 0:
                break_point_diff = break_point_row0 - break_point_row1
                sg = balance_rows(break_point_diff, \
                                  position_str[0][break_point_row0:i], position_str[1][break_point_row1:i])
                break_point_row0 = i + 1
                break_point_row1 = i + 1
                sg_list.append(sg)
            elif position_str[1][i+1] == 0:
                break_point_diff = break_point_row0 - break_point_row1
                sg = balance_rows(break_point_diff, \
                                  position_str[0][break_point_row0:i], position_str[1][break_point_row1:i+1])
                break_point_row0 = i + 1
                break_point_row1 = i + 2
                sg_list.append(sg)
    if len(sg_list) != 0:
        row0 = position_str[0][break_point_row0:]
        row1 = position_str[1][break_point_row1:]
        sg_list.append(balance_rows(break_point_row0 - break_point_row1, row0, row1))
        return(True, sg_list)
    return(False, None)
   
def A1(position, n):
    s = Clobber_2d(position)
    if s.endOfGame() and n == 0:
        return(0)
    result = tt.lookup(position)
    if result != None:
        #print("in 1")
        if result == n:
            return(0)
        else:
            return(1)
    splittable, sg_list = splittable_2d(s.board)
    if splittable:
        if len(sg_list) == 1:
            return(A1(sg_list[0], n))
        return(A2(sg_list, n))
    else:
        moves = s.legalmoves_impartial()
        center_moves = [moves[(len(moves) + (~i, i)[i%2]) // 2] for i in range(len(moves))]
        for move in center_moves:
            game = Clobber_2d(position)
            game.play(move)
            game_str = Clobber_2d.to_string(game.board)
            result = A1(game_str, n)
            if result == 0:
                return(1)
        for move in moves_nimber(n):
            if A1(position, move) == 0:
                return(1)
        return(0)

