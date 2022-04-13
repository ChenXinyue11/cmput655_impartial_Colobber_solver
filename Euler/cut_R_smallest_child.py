
from turtle import position
from clobber_1d_im import *
import random
import time
store_value = {}
endtime = 0
endcheck = 0
tttime = 0
ttcheck = 0

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

def decimalToBinary(n):
    return bin(n).replace("0b", "")

def read_database():
    global store_value
    with open('nims.txt') as text_file:
        lines = text_file.readlines()
        text_file.close()
    for line in lines:
        gamestr, value = line.split(" ")
        store_value[gamestr] = int(value[:-1])

def smallest_child(position_str,M):
    list_n2 = []
    list_0 = []
    list_n6 = []
    list_n4 = []
    list_other = []
    if len(position_str)>2:
        for m in M:
            
            #m [src, to]
            if len(position_str) == 2:
                list_n2.append(m)
            elif m[0] > m[1]:
                if m[1]  == 0 or position_str[m[1]-1] == '.':
                    '''print("m", m)
                    print("str",position_str)'''
                    if m[0]+1 == len(position_str):
                        list_n2.append(m)
                    elif position_str[m[1]] == position_str[m[0]+1]:
                        list_n4.append(m)
                    else:
                        list_n2.append(m)
                elif  m[0] == len(position_str) - 1 or position_str[m[0]+1] == '.' :
                    if position_str[m[1]] == position_str[m[1]-1]:
                        list_0.append(m)
                    elif position_str[m[1]-1] == position_str[m[0]]:
                        list_n4.append(m)
                    else:
                        list_n2.append(m)
                elif position_str[m[1]-1] == position_str[m[1]] and position_str[m[0]] == position_str[m[0]+1]:
                    list_0.append(m)
                elif position_str[m[1]-1] == position_str[m[1]] and position_str[m[1]] == position_str[m[0]+1]:
                    list_n2.append(m)
                elif position_str[m[1]-1] == position_str[m[0]] and position_str[m[0]] == position_str[m[0]+1]:  
                    list_n4.append(m)
                elif position_str[m[1]-1] == position_str[m[0]] and position_str[m[1]] == position_str[m[0]+1]:  
                    list_n6.append(m)  
                else:
                    list_other.append(m)
            else:
                if m[1] == len(position_str) - 1 or position_str[m[1]+1] == '.':
                    if m[0]-1 < 0:
                        list_n2.append(m)
                    elif position_str[m[1]] == position_str[m[0]-1]:
                        list_n4.append(m)
                    else:
                        list_n2.append(m)
                elif  m[0] == 0 or position_str[m[1]+1] == '.' :
                    if position_str[m[1]] == position_str[m[0]-1]:
                        list_0.append(m)
                    elif position_str[m[1]+1] == position_str[m[0]]:
                        list_n4.append(m)
                    else:
                        list_n2.append(m)
                elif position_str[m[1]+1] == position_str[m[1]] and position_str[m[0]] == position_str[m[0]-1]:
                    list_0.append(m)
                elif position_str[m[1]+1] == position_str[m[1]] and position_str[m[1]] == position_str[m[0]-1]:
                    list_n2.append(m)
                elif position_str[m[1]+1] == position_str[m[0]] and position_str[m[0]] == position_str[m[0]-1]:  
                    list_n4.append(m)
                elif position_str[m[1]+1] == position_str[m[0]] and position_str[m[1]] == position_str[m[0]-1]:  
                    list_n6.append(m)  
                else:
                    list_other.append(m)

        move_order =  list_0+list_other + list_n6 + list_n2 + list_n4
        M = move_order[:]
    return M
def smallest_child_v2(s,M):
    nums =[]
    for m in M:
        s.play(m)
        child_move = s.legalmoves_impartial()
        num_moves = len(child_move)
        nums.append(num_moves)
        s.undoMove()
    new_m = []
    #print(M)
    while nums != []:
        mini = min(nums)
        for i, j in enumerate(nums):
            if j == mini:
                new_m.append(M[i])
                M.pop(i)
                nums.pop(i)
    return new_m

def cut_R(s, R, tt):
    global tttime,ttcheck
    position_str = Clobber_1d.to_string(s.board)
    V = tt.lookup(position_str)
    moves = s.legalmoves_impartial()
    tttime += 1
    value = store_value.get(Clobber_1d.to_string(s.board))
    if value != None:
        ttcheck += 1
        return value
    P = []
    if V != None:
        ttcheck += 1
        if len(V) == 1:
            return(V[0])
        P = V[:]
        new_moves = smallest_child(position_str,moves)
        M = new_moves[len(new_moves)-(len(V)-1):]
    else:
        for i in range(len(moves)+1):
            P.append(i)
        new_moves = smallest_child(position_str,moves)
        M = new_moves[:]
    #new_moves = smallest_child_v2(s,M)
    exact = True
    for m in M:
        if set(P) & set(R) == set([]):
            if exact or max(P) <= max(R):
                tt.store(position_str, P)
            return(-1)
        s.play(m)
        PS = P[:]
        PS.remove(max(PS))
        full_R = []
        for i in range(max(R)+1):
            full_R.append(i)
        v = cut_R(s, list(set(PS) & set(full_R)), tt)
        s.undoMove()
        if v in P:
            P.remove(v)
        else:
            P.remove(max(P))
            if v == -1:
                exact = False
    result = P[0]
    if exact or result <= max(R):
        tt.store(position_str, P)
        return(result)
    else:
        return(-1)



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
    for poss in pos18:      
        start = time.time()
        game = Clobber_1d(poss)
        tt = TranspositionTable()
        R = nimberChoices(game)
        print("On Pruning nimber:",cut_R(game,R,tt))
        elapsed = time.time()-start
        print("time:", "{0:.4f}".format(elapsed))
        t2 += elapsed
        print("==================")
    print(t2/50)
    print(tttime/50,ttcheck/50)
    
    
    
main()
