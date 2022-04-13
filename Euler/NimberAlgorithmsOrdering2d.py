"""
Algorithms from Nimbers Are Inevitable

"""
#1 for win
#0 for loss

import operator, multiprocessing, TT
from clobber_2d_im import *

def A2(subgame_list, n,tt):
    position_list = subgame_list[:]
    position_list.sort(key=len)
    nimsum = n
    for i in range(len(position_list)-1):
        nimber = A3(Clobber_2d(position_list[i]),tt)
        nimsum = operator.xor(nimsum,nimber)
    outcome = A1(Clobber_2d(position_list[-1]), nimsum,tt)
    return(outcome)

def A3(position,tt):
    n = 0
    position_str = Clobber_2d.to_string(position.board)
    result = tt.lookup(position_str)
    if result != None:
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
    position_str = position.board
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
   
def A1(position, n,tt):
    position_str = Clobber_2d.to_string(position.board)
    if position.endOfGame() and n == 0:
        return(0)
    result = tt.lookup(position_str)
    if result != None:
        if result == n:
            return(0)
        else:
            return(1)
    splittable, sg_list = splittable_2d(position)
    if splittable:
        if len(sg_list) == 1:
            return(A1(Clobber_2d(sg_list[0]), n,tt))
        return(A2(sg_list, n,tt))
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

