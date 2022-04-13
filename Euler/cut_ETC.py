
from clobber_1d_im import *

def cut_etc(s,R,tt):
    #s is a move or positon
    #R are possible nimbers list
    #R must in order
    global tttime,ttcheck
    position_str = Clobber_1d.to_string(s.board)
    result = tt.lookup(position_str)
    tttime += 1
    if result != None:
        #print("in 1")
        ttcheck += 1
        return result
    value = store_value.get(position_str)
    if value != None:
        ttcheck += 1
        return value
    moves = s.legalmoves_impartial()
    center_moves = [moves[(len(moves) + (~i, i)[i%2]) // 2] for i in range(len(moves))]
    P = []
    for i in range(len(moves)+1):
        P.append(i)
    M = []
    for m in moves:
        s.play(m)
        position_str1 = Clobber_1d.to_string(s.board)
        result1 = tt.lookup(position_str1)
        value1 = store_value.get(position_str)
        s.undoMove()
        tttime += 1
        if result1 != None:
            if result1 in P:
                ttcheck += 1
                P.remove(result1)
            else:
                P.remove(P[-1])
        elif value1 != None:
            if value1 in P:
                ttcheck += 1
                P.remove(result1)
            else:
                P.remove(P[-1])
        else:
            M.append(m) 
    exact = True
    for m in M:
        if list(set(R) & set(P)) == []:
            return -1
        s.play(m)
        full_R = []
        for i in range(R[-1]+1):
            full_R.append(i)
        v = cut_etc(s, list(set(P[:-1]) & set(full_R)),tt)
        s.undoMove()
        if v in P:
            P.remove(v)
        else:
            P.remove(P[-1])
            if v == -1:
                exact = False
        #if len(P) == 1:
        #    break
    nim = P[0]
    if exact or nim <= R[-1]:
        tt.store(position_str, nim)
        return nim
    else:
        return -1


import operator
from clobber_1d_im import *
store_value = {}
import time
endtime = 0
endcheck = 0
tttime = 0
ttcheck = 0
def nimberChoices(s):
    R = []
    for i in range(len(s.legalmoves_impartial())+1):
        R.append(i)
    return(R)


class TranspositionTable(object):


    # Empty dictionary
    def __init__(self):
        
        self.table = {}

    # Used to print the whole table with print(tt)
    def __repr__(self):
        return self.table.__repr__()
        
    def store(self, code, score):
        #print(code)
        sym = ''
        for char in code:
            if char == 'W':
                sym += 'B'
            elif char == 'B':
                sym += 'W'
            else:
                sym += char
        self.table[code] = score
        self.table[sym] = score
    
    # Python dictionary returns 'None' if key not found by get()
    def lookup(self, code):
        #print("geting")
        return self.table.get(code)
def cut(s,R,tt):
    #s is a move or positon
    #R are possible nimbers list
    #R must in order
    global tttime,ttcheck
    position_str = Clobber_1d.to_string(s.board)
    result = tt.lookup(position_str)
    tttime += 1
    if result != None:
        #print("in 1")
        ttcheck += 1
        return result
    value = store_value.get(position_str)
    if value != None:
        ttcheck += 1
        return value
    moves = s.legalmoves_impartial()
    center_moves = [moves[(len(moves) + (~i, i)[i%2]) // 2] for i in range(len(moves))]
    P = []
    for i in range(len(moves)+1):
        P.append(i)
    exact = True
    for m in center_moves:
        if list(set(R) & set(P)) == []:
            return -1
        s.play(m)
        full_R = []
        for i in range(R[-1]+1):
            full_R.append(i)
        v = cut(s, list(set(P[:-1]) & set(full_R)),tt)
        s.undoMove()
        if v in P:
            ttcheck += 1
            P.remove(v)
        else:
            P.remove(P[-1])
            if v == -1:
                exact = False
        #if len(P) == 1:
        #    break
    nim = P[0]
    if exact or nim <= R[-1]:
        tt.store(position_str, nim)
        return nim
    else:
        return -1
"""
def cut_R(s, R):
    result = tt.lookup(s)
    if result != None:
        
        
"""
def read_database():
    global store_value
    with open('nims.txt') as text_file:
        lines = text_file.readlines()
        text_file.close()
    for line in lines:
        gamestr, value = line.split(" ")
        store_value[gamestr] = int(value[:-1])
def main():

    pos20 = ['.W.WW...WBBW.BBBBWBW', '..BWW.B.WBBB.WBBW..B', '.WWBB.BBB..WBWW.WBBB', 'WW.WW.WB.WWWBBBBBB..', '..WB..WWB.WBWBWBWW.B', 'BBB.W.WWWWW....B.BBB', '.WB.B..WWWB.BB.WBBWW', 'W..WBB.WBW..BWB.W.BW', '.BB.W.B.BW.WW.B..BB.', '.....W...BWW....WWW.', '.BWB.W.WB.W.BW..B.B.', 'WBBB.WB..WBBW....BBW', 'B...BBWB.WBWWBBBWBWB', 'BBWW.BW.W..WBW.W...B', 'W...WWB.WBWBWW.BB.BW', 'WBWBBBB..BW.W..BBB.B', 'WWWBWBB..WWW..WB..BB', '..BB.WBBB....WWWB.WW', 'W.BBWBBWBBWW...W.W.W', 'BB..BWBWWWW..B.B.BW.', 'WBWBWW...WBW.B....BW', '.W.WBBWBB...W.WW.W.B', 'B.W.WBBBB..BBBBW.BBB', 'BB.B.BBWBWBBW.WBWW..', 'W.WBB.W.B.WWBBBW.BW.', 'WWBB.BW.BWB.W..W.WWB', 'W..W.BBB.BW.BWBW.W.B', 'B.B..W..WBBW.WBW..BW', '.BBBBWW.BWBB.WWWBBWB', '...BB..BWBWWWWBBB.W.', 'BWW.WBBB.B.BWW.BB..W', 'WBW.BB..WBWBWWWW.W.B', 'BWWWWB.WWBWWW...BW..', 'WB...WWW.W.BBWWBBWWB', 'BW..BBW.WB.W.WW.WBWB', '.B.B..WBW..BWWWWW...', 'B.WB.W.W.WW.W.B..WWB', 'W...B.BBWWWB..BBWBW.', 'WBBW.W.BWW.....W.BBB', 'WWBB...WBBB..BBBB..W', 'B.WWWBBWWBB..W.WW.WW', 'WWWW.WBWBBBB.BB.WW.W', '.BB..WW.W.WW..W.WBB.', '.BWB.B..WW.BB.BBWBWW', 'W..W...BW.BBWB.WBBW.', '.WW.BWB...BB..WWW..B', 'BB.WBW.BW.WWWWB.WBBB', 'W..BW...WWB.BW.B.B..', 'W.W.B.W....WW.WWW...', 'BB.WWWWWBW..WWBBWWBW'] 
    pos30 = ['W.BB..WWWB...BBBWWBBBBWWWB.B.W', 'WB.W.BBWWBB.BWB.WW..BW..WB.B..', 'BBWWW..BWWBB.BBBBWWBWBBWW..WW.', 'W.WB..WB.BW...B..BBBWWWBWBBBWB', 'W...WW...B.WBBWWW..WW.WBW.W.WB', '.WBW.WW.W.WBBWWBWBBW.BWW.WBW.W', 'WB...BWBWWWWBWB...W.W..W.WW..B', 'WB..B.W.BW.W..WBW.WW.WWW.BBW.B', 'WBBBWB.WBBBBBBWWW..BWB.BBBB.BB', 'B.BBW.WB..WWW.WBB..W..B.B..BWW', 'BB..WWB..WW..WW.BBB.WBW...WBBW', 'WBW.WWB...BWW.BBWB.B.WBBW.W.B.', '.BBB.BBBWB..W..WW....BWWBW...B', 'BB.B....BBB..W.WB..W..BWBBB.W.', 'BBB.WWBB.WBBWWBB....WBBW.B..W.', '.WW.B.BBBBW.B.W.B..BWWW..B.WWW', 'B..BB.WW..B..B..BBWW.WWBB.BB..', '..BW...BBB.....BWWWWBBWBWWW.WB', '.WWWWW..B.WWBBWBWBBB..BW..B.WW', '.WW.W.B.W.BWWBW...WWBWW..W.WW.', '..BW.B.BW.WWWWBW.B..WBB.W.BW.B', 'WB.WBBB..B.WB..BWBBBW.WBW.BBWB', '.BWBWBB.W.W..WWW.W.B....W..WBB', '.WWB.W.WB.BBB....BBWW.W.W.B..W', 'W....W.WBW.WWWB..BBW...BWW.BB.', '..W.BWBWWWBWWBWBWB.W..W.WBWW..', 'BWWWBW.B.W..BWB...BWWBWW.....B', 'WW.W.WWWWBWBWB.WBW.W.WW.WB.BBW', 'BWWWBW.WBB..W..BB..W.W.WW.B..W', 'BBB.WWWB..BBBWW..WBBW..BBB..W.', 'WWB.WB.B..WWB.W..WWBW.WWB..BBW', '..WBBWB.W.WBB.BB.WBWBBW.WWB...', 'W.WBW.WWWB.WW..BWB.B......BB.W', 'BWB.B...B.BWB..BWBBWW..BB..BBW', 'BBWB.B.BBB.W.WBWBB.B.W.BBW.WBW', 'BW..WW.W.BB...B.W.BWBB.WBBW.BB', 'W..W.W.B..BB..WBWB.WB..WW.W..B', '.WB.BB.WBBWW.B.BWWW..BW.B.WBW.', 'W.BBW.BBBWW.WB.W...WB..W.BB.W.', 'W.WWBW.B...BB.WWW.BBBBB.BW...B', 'B..BWWW.WBW.BW.B.BBW.W.....WWB', 'WWW.BBWWWW.W..B.B.WB.WWB.B.BB.', '.W.W.B.B.WB.W.W.BWW.BWB..BBW..', '..WBWW.BWW..W.WW.BWBW..W.WWWBB', 'WWW.B..W.WB.WWWWBWB..BBBWB.W.B', 'BBB..B.BBW..B...WWBW.WWBB.WWBB', '.WB.W....W....BB.WWBBWBW.WWWWB', '.B.WWW.WBB.W....W...WBB..WW.WW', '.WWW..BBBW.WWWWWBBBW..WB.WBWBB', 'W.BWW....BBBBWBBBWWBWBBW.WBWBW']
    
    pos18 = ['BBBBWBBBWWWWBBBBBW', 'WBBWWBWWBWWBBBBBWB', 'WBBWBWWWBBBWBWWWBB', 'BWBWBBBBWBWWWWWBBB', 'BBWBWBWBWBWWBWWBBB', 'WBBWWBWWWWWBBBWBBW', 'BBWWBWBWBBBBWWBWWB', 'BWWBBBBWWBWBWBBBWB', 'WBWBBWBBWWWWBWBWWB', 'BBWWWBWWWBWBWWBBWW', 'WBWWBBWWWWBWBBBBWW', 'BWBWWBWBBWWWWWWBBB', 'WWBBWWBBBWWBBBWBWW', 'WWWWWWBWBWWBWWBWWB', 'BBWWWBBWWBBWBBBBBW', 'WBBBWBBWWWWBWWBWWB', 'BBWBBWWWBWBWWBWBWB', 'WBBWBBBWWBBBWBWBBB', 'BWWBBWBWBWWBBBWBBB', 'WWBBBWBWBWWBBBBWBW', 'WBWBWWBWBBBBBBBWBW', 'BWWBWBBBBBWWBWWWBB', 'WBBBBBBWWBBWBWWBBW', 'WBWWWBWWWBBWBWBWWW', 'WWBWWBBBBBBBBBBWWB', 'BWBBBWWBBBBWWWBBWW', 'BWBBWBBWBWWWBWWBWW', 'WBWBWWBWBBWBWBWWWW', 'BBWBWWWBWWWBBBBBWW', 'BBWWWBWBWWBBBBWBBW', 'BWWWWWBBWWBBWBBBBW', 'WBBWBWWWWBWWBBWBBB', 'BBBBWWWWBBWWWWWBWB', 'BWWBBWWWBBBWWBWWBW', 'WBWWWWWBBBBBWBBWWW', 'WBWWWBWWWBWBWWWBBW', 'BBBWBBBBWBWWBWBBBW', 'BWWBBBWBWWBWWBWBWW', 'BWBWBWWWWWBBBWBBBW', 'WWWWBWBBWBBBBWWBWW', 'WBWBBBBBWWBBBWBBWB', 'WWWWBBWBBBWBWWWBWW', 'BBWWWWWBBBBBBBBBBW', 'BBWWBWBWBWWBWWWBWB', 'WWWBBBWWBBBBBWBWBW', 'WBWWBWWBWBBBWWBWWW', 'BBWWBBBBBWBWBBWBBB', 'WWWWWBWBBBBBWBWWWB', 'BBBBWBBWBWBWWWWBWW', 'WWWWWWBBWWWBBBBBBB']
    pos40 = ['B..W.WBB.B.B..W...WBBWWW..BWWBBBBBBB..BB', 'W.W..WWBWBBB.B.BBBB.W.BBWW....BBWWBWWB.B', '..WWB.BW.WWBBWBWB..B..BWB.BWBBBWW..WB..B', 'WBBWBW.BB.BWB.BW..W...W.WBWWBBB.BBB.WB.W', 'BBW..B.BBWWB..B.WB..B.BBWB.WWB.W.W..BB.B', 'B.B.B.B.....WBBWWBW.WWW.BB...WBB.BWW.WBW', '.WWWBBWWBWBBBB.WWBW.WBWBBBWB..BB.BWW.BWB', 'BWBBBBW.WW.W..WWW.WB.WB.W.WB.WWBWBB..BBW', 'WB.BWB.BWB..BW.BWWB.BWWBW.W.WBW.WBBB.BBW', 'WB..BB.B.WB...B.W.B.BBBWBWWB.BW....WBBW.', 'BB.W.BBWWWBBB.BWWBBWWB...B.WWBWBBWWWWWW.', '.W.B.BWBWBWBB..BWW.BBWWB..B..WBB.BBWW...', 'BBWWBWBB.B.B..WBBW..W.BWW.WWBWWB..W.WW.W', '.B.W.WB..W.WW.B..W.BWWBWB.BWBWB.WB.W..BW', 'BWBB.WWB.WWWW.BBW..B.BBBBW.BW....WBBWW.B', 'WB..WW..B.BBW..WWWBWWWBW.W.WBW..B.WBWWBB', '.BB.BBBWB.W.WBBB...BW.W..BWBWBBBBBBB.B.W', '.B.WWB.W.WB.BBB..BBBWWBBBWWBBW.WWWB.WB.B', 'WB..W....W.WBBW.BBBBBBBB..WWB.BBB...BW.W', '.WBWWWB.BB...WB.BB.BWWWBB.WB.B.BWBW....B', '.WWBB.WBW.WWBBBW.WWBWWBWBBBW.BWBW.WWW.B.', 'BWBWB.W...WBWB.BWW.BW..WB.WB..BB..WB..BB', '.B..B.B.BWW...WB..B...WBBBWB..WB..B..WB.', 'B...B...BW.WWW.WB.WBW.W...W..B.WWW..W.WW', 'WWBWWB.....WWWWB.WW.WBWW.B.W.B.W...WBWW.', '.B..WBW...WWWW....BW.WWB.BWW.WWB.WBB....', 'BB.WBW.B.B.WWW.W...W.W.BWWBBBW..W.BWWBW.', 'B.WBWB.BBBW.W..WW.BBW.BBB.WB..BBBW.B.W..', 'WWBWBWWB.WWBB..BB.W.B.BW..B.B...W.WWB.WB', '..WB...W.WBBB.WW.WW.BBB...WWWBWWBBBBWWW.', 'WBBW.BB.W..W.WWW.BWB..W..B.WW.WBW...B...', '.BBB.BWWWBW.WBBWWB.W.BWBB.WWBWWB..WWB.B.', '.B.BBBWBWB.BBBBBBW..WWB.BW..B...WBWBB.BW', '.WWBWWWBWB.W.BBBBWBWBWWB.W.BWB...WW.W.BW', 'B.BBWBWW...B.WWWBWBB..BWWW.WBWBB.W.B.WW.', 'B.W.B...B.B.WWWWWWW..WW..B..WBW...WW.B.B', 'WBBBWWWW.B.W.W.BWW.B.BBW.WB....WB.W.BBWW', 'BBW..WWBBBWW.WW..WBWB..WBWW.BBWBWWB..BWB', 'W.WW...BB.WW.W....B.W.BW.W..BBB..W.WB.WB', 'WWWBBB.WWBB.WBW..WWWWBBBWWB.WBWBBWBBBB.W', '.BWB.BBBB.WBB.WB..BB.B.WBB...BW.B.WW.W..', '.WBWBWBWBWB.B.WWBWBWBW..B..B.BB.BB..B.WB', 'WW.W..WWBB.WBW..W..BB.WBW..BB...W.B.W.W.', 'WW.WB.BBWWWWWWWWWBBBB.BBWWWBBBB.B...B.BB', 'WBW....BW..W.W.BBWB.WW.WBWWBB..W.B..B.WW', 'B.BBWW.B.WB.BBW.WBWWBBWBBBWWB.B.WBBWBWBB', 'WBWBBB.BBBWBB.B.W..BWB.B.BWBBW.B.BBWB..W', 'WBBWBBB.WWW.B.WBBB..WWB.WWBBBBB..W.BW.B.', 'BBWBB.BB.B.WB.BWWWWBWBBW.BWWB.W.BW.BBWBB', '.WWW.B...WWBB.B...W....WWBBBW....W..WB.W']
    pos16 = ['BWBBWBBBBWWWBWBB', 'WWBWWWBBBWWWWBBB', 'WWBBBBWBBWWWWBWW', 'BWBWWWBWBWBWWBBB', 'BWBBWWBBBWWBWBBW', 'WBBWWWWWBWBWBWBW', 'BWBBWWBWBBWBBBWB', 'WWWWWBWWBWWWBWBW', 'WBBWBWWWBBBWBBBB', 'WWBWWWWWBWBBWWBB', 'WWWWWWWBWBWWBWBB', 'BBBBBWWWBBBWWWBW', 'BBBBBWBWBBBBBWBB', 'BBWWBWBWWBBWBBBB', 'BBWBWBWWWBWBBBBW', 'WBWWBBWBBWWWBBWW', 'WWWWWBBBBBWWWBBB', 'BWWBWBBBWWWWWWWB', 'BWWWBWWBBWWWWBBB', 'BBBBWWBBBBWBBBBW', 'WWWWBBWBBWBWBBBB', 'WWWBBWWWWBWBBWBB', 'WWWBBWBBBWBWWBBB', 'WWBBWBBWWBBWWBBW', 'BBWWBWBWWWBWWWWB', 'BWWBBWWWWWWWBBWB', 'BBWWBWWWBWBWWWBW', 'WBWBWBWWWBBBWBBW', 'WBBBWBWBWWWWBBBW', 'BWBWWBWBBWBBWBBW', 'BBBBBWBBWWBBBWWW', 'BBBWBBWBWBWWBBWB', 'WWBBWBBWWWBWBBWW', 'BWWWWWWBBBWBWBBW', 'BWWBBBWBBBWWWWBB', 'BBWWBWBBBBBBWWBW', 'WWWBBBWWWWBWWWWB', 'WWBBWBBWBWBWWBWW', 'BBBWBWWBBWWWWBWB', 'WBWWWBBWBWWBWBWW', 'WBBWBBBWWWWWWBBB', 'BBBBWWBBWWBWBBWB', 'WBWBWBBBWBWWWWWB', 'WWBBWBBWWBBBWBBW', 'WBWWBWWBBWWBWWWW', 'WBBBBBWBWWBWBWBW', 'WBBBWBBWBWBWWBWW', 'BBWWWWBWWBBBWWBW', 'WBWBBWWBBBBWBBWB', 'WBBWWBBWWBWWWBWB']  
    pos201 = ['BBWWBWWBWWBWWWWBBWWW', 'BBWWWWWBWWBBWBWBWWWB', 'WBBWWBBWWWBWBBWBWBWB', 'BBWWBBBBWWWWWBWBWBWW', 'WBBBBBBWWWBWWBWBWBWB', 'WBWWWWWWWWWBBWBWWBBB', 'BBBBBBBBBWBBBBWBBBWB', 'WWWBWBWBBBBWBBBBBWWW', 'BWBBBBBBWBBWBWWWWWWB', 'BWWBWWBBWBWWBBWWBBWW', 'BWBWWWWWBBWBBWWBBWBW', 'BWBWBBBBBWBWBBBBWWBB', 'WBBWBWWWBWWBBBBWBWBB', 'WWBWWBWWWBWWWWWWWBBB', 'WBWWWWWWWBWBWBBWBWWB', 'BWWWBBBWBWWBWWWWWWBB', 'BWWBWBBWBBBBBWWWWBWW', 'BBBBBWBWWWBBWWWWBBWW', 'WBWBWWWBBWWBWWWWBBBW', 'WBWWWBBWBWBWBBWBWBWB', 'WWBWBWBWBBBBWWWWBBWW', 'BBWWBWBBWBBBBBBBWBBW', 'WBWBWBBWBBBWWWBWWBBB', 'WBWBWWWBBBBBBWBBWBWW', 'BWWBWWBBBWBBWWWBWWBB', 'BBWBWWWBBWWWWWWWWWWW', 'WWWBBWWBWBWWWBBWWBBW', 'WBWBWWBBWWBWWWBBBWWB', 'BWBBBWWBBBBBWBBBBWBB', 'WWBWBWWBWWWWWBWWWBWW', 'BWWBWBWWBWBWWBBWWWBB', 'BWBWBWBWWWBWWBBBBWWW', 'WWWWWBWWWBWWWWWWWWWB', 'WBWWWWWWBWBWBWBWWWBB', 'WWBBWWBWBWWBWBWWWBWW', 'WBWBWWBBBBWBWWBWBWBB', 'WWBWBWBWBBWWBWBWWWBW', 'WWWWBWBBBWWBBWWBBWBW', 'BBWWBBWBBWBBBBWBBWWW', 'WWBWBWBBBWBWWWBWBBBB', 'BWBWBBBWWBBWBBWWWWBB', 'WWBWWBBWBBWWWWBBBWWB', 'BWBWBWBBBWWWBWBBWBWW', 'WBWBBWBWBWWBWWBWBWWB', 'WBBWBWBBWBWBWBWBBBBW', 'BWBWWWWBBWBBWWWBWWBW', 'BBWWWWWBWWWBBWWWWWBW', 'BWBBBBWBWWWBBWBBWWWB', 'BBWWWWBWWBBWBWBWBWWB', 'WBBWBBBBBBWBBBWWWBBB']  
    t1 =0
    t2 = 0
    start = time.time()
    read_database()
    elapsed = time.time()-start
    print("database loading time:", "{0:.4f}".format(elapsed))
    for poss in pos201:      
        start = time.time()
        game = Clobber_1d(poss)
        tt = TranspositionTable()
        R = nimberChoices(game)
        print("On Pruning nimber:",cut_etc(game,R,tt))
        elapsed = time.time()-start
        print("time:", "{0:.4f}".format(elapsed))
        t2 += elapsed
        print("==================")
    print(t2/50)
    print(tttime/50,ttcheck/50)
    
    
    
main()