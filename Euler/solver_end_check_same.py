
from clobber_1d_im import *
from cut import *
import time, random
from cut_ETC import *
from cut_R import *

store_value = {}


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

def endgame():
    to = 4
    tt = TranspositionTable()
    for i in range(1,to):
        length = i
        a = int('1'*length,2)
        string = "0"+str(length)+"b"
        for i in range(0,a+1):
            two_base = format(i,string)
            #print(str(two_base))
            string_code = str(two_base)
            acode = ""
            for i in range(len(string_code)):
                if string_code[i] == "0":
                    acode += "W"
                else:
                    acode += "B"
            game = Clobber_1d(acode)
            nim = A3(game, tt)
            with open("nims.txt", "a") as text_file:
                text_file.write(acode + " "+str(nim) + "\n")
            text_file.close()
def read_database():
    global store_value
    with open('nims.txt') as text_file:
        lines = text_file.readlines()
        text_file.close()
    for line in lines:
        gamestr, value = line.split(" ")
        store_value[gamestr] = int(value[:-1])

def main():
    read_database()
    position = "BW"*10
    game = Clobber_1d(position)
    tt = TranspositionTable()
    start = time.time()
    sg_list = ["BW", "BWBW", "BWBWBW"]
    nim = A3(game, tt)
    print(nim)
    elapsed = time.time()-start
    print("time:", elapsed)




def A2(subgame_list, n,tt):
    position_list = subgame_list[:]
    position_list.sort(key=len)
    nimsum = n
    after_remove_list = []
    for i in range(0,len(position_list)):
        sym = ''
        for char in position_list[i]:
            if char == 'W':
                sym += 'B'
            elif char == 'B':
                sym += 'W'
            else:
                sym += char
        if position_list[i] in after_remove_list:
            after_remove_list.remove(position_list[i])
        elif sym in after_remove_list:
            after_remove_list.remove(sym)
        else:
            after_remove_list.append(position_list[i])
    if after_remove_list == []:
        return n != 0
    for i in range(len(after_remove_list)-1):
        nimber = A3(Clobber_1d(after_remove_list[i]),tt)
        nimsum = operator.xor(nimsum,nimber)
    outcome = A1(Clobber_1d(after_remove_list[-1]), nimsum,tt)
    return(outcome)

def args_list(args1, tt):
    result = []
    for i in range(len(args1)):
        result.append([Clobber_1d(args1[i]), tt])
    return(result)

def A3(position,tt):
    #print("A3 position:", Clobber_1d.to_string(position.board))
    n = 0
    position_str = Clobber_1d.to_string(position.board)
    result = tt.lookup(position_str)
    if result != None:
        return result
    value = store_value.get(position_str)
    if value != None:
        #print("inend")
        return value
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
    value = store_value.get(position_str)
    if value != None:
        if value == n:
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



main()
