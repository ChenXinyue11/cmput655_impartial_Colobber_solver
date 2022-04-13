# Cmput 655 sample code
# 1xn Clobber game board, rules, and a random game simulator
# Includes the code() method to compute a "hash code" for 
# use in a transposition table (This is actually a perfect code, 
# not a hash code, since the state space is so small)
# Written by Martin Mueller
# Modified by Xinyue

import code
import random
from game_basics import EMPTY, BLACK, WHITE, isEmptyBlackWhite, opponent

class Clobber_2d(object):
# Board is stored in 1-d array of EMPTY, BLACK, WHITE

    @classmethod
    def standard_board(cls, size):
        pairs = (size+1) // 2
        board_line_1 = [BLACK, WHITE] * pairs
        board_line_2 = [WHITE, BLACK] * pairs
        return [board_line_1,board_line_2]
            
    @classmethod
    def custom_board(cls, start_position): # str of B, W, E or .
        color_map = { 'B': BLACK, 'W': WHITE, 'E': EMPTY, '.': EMPTY }
        board = []
        board_line =[]
        for c in start_position:
            if c == "/":
                board.append(board_line)
                board_line = []
            else:
                board_line.append(color_map[c])
        board.append(board_line)
        return board
    
    @classmethod
    def to_string(cls, board):
        #todo
        char_map = { BLACK: 'B', WHITE: 'W', EMPTY: '.'}
        s = ""
        for p in board[0]:
            s += char_map[p]
        s += "/"
        for p in board[1]:
            s += char_map[p]
        return s
        
    def __init__(self, start_position, first_player = WHITE): 
    # we take either a board size for standard "BWBW...", 
    # or a custom start string such as "BWEEWWB"
        if type(start_position) == int:
            self.init_board = Clobber_2d.standard_board(start_position)
        else:
            assert type(start_position) == str
            self.init_board = Clobber_2d.custom_board(start_position)
        #self.zobTable = [[[random.randint(1,2**64 - 1) for i in range(3)]for j in range(2)]for k in range(len(self.init_board))]
        self.resetGame(first_player)
        #self.boardcode = self.computeHash()

    def resetGame(self, first_player):
        self.board = self.init_board
        self.toPlay = first_player
        self.first_player = first_player
        self.pre_moves = []
        #self.pr_code = []
    def computeHash(self):
        h = 0
        for j in range(len(self.board)):
            for k in range(len(self.board[j])):
                if self.board[j] != EMPTY:
                    piece = self.board[j]
                    h ^= self.zobTable[j][k][piece]
        return h

    def opp_color(self):
        return opponent(self.toPlay)
        
    def switchToPlay(self):
        self.toPlay = self.opp_color()

    def play(self, move):
        #modified by xy
        src, to = move
        src_color = self.board[src[0]][src[1]]
        to_color = self.board[to[0]][to[1]]
        #assert self.board[src] == self.toPlay
        #assert self.board[to] == self.opp_color()
        #self.pr_code.append(self.boardcode)
        self.board[src[0]][src[1]] = EMPTY
        self.board[to[0]][to[1]] = src_color
        #need to change
        #self.boardcode ^= self.zobTable[to[0]][to[1]][src_color]
        #self.boardcode ^= self.zobTable[src[0]][src[1]][EMPTY]
        self.pre_moves.append(move)
        self.switchToPlay()
        

    def undoMove(self):
        #modified by xy
        self.switchToPlay()
        src, to = self.pre_moves.pop()
        #self.boardcode = self.pr_code.pop()
        #assert self.board[src] == EMPTY
        #assert self.board[to] == self.toPlay
        self.board[src[0]][src[1]] = self.board[to[0]][to[1]]
        self.board[to[0]][to[1]] = 3 - self.board[src[0]][src[1]]
        
    
    def winner(self):
        if self.endOfGame():
            return self.opp_color()
        else:
            return EMPTY

    def staticallyEvaluateForToPlay(self):
        winColor = self.winner()
        return winColor == self.toPlay
    

    def endOfGame(self):
        return len(self.legalmoves_impartial()) == 0

    def legalMoves(self):
        # To do: this is super slow. Should keep track of moves
        moves = []
        opp = self.opp_color()
        last = len(self.board) - 1
        for i, p in enumerate(self.board):
            if p == self.toPlay:
                if i > 0 and self.board[i-1] == opp:
                    moves.append((i, i-1))
                if i < last and self.board[i+1] == opp:
                    moves.append((i, i+1))
        return moves
    def legalmoves_impartial(self):
        #modified by xy
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1):
                if self.board[i][j] + self.board[i][j+1] == 3:
                    moves.append(((i,j),(i,j+1)))
                    moves.append(((i,j+1),(i,j)))
        for i in range(len(self.board[0])):
            if self.board[0][i] + self.board[1][i] == 3:
                moves.append(((0,i),(1,i)))
                moves.append(((1,i),(0,i)))
        return moves

    def code(self):
        # To do: this is super slow. Should keep track of code
        c = 0
        for color in self.board:
            c = 3*c + color
        return 2*c + self.toPlay - 1 # BLACK = 1, WHITE = 2

    # simulate one game from the current state until the end
    def simulate(self):
        assert False # todo: this is for Tic Tac Toe, needs fixing for Clobber
        i = 0
        if not self.endOfGame():
            allMoves = self.legalMoves()
            random.shuffle(allMoves)
            while not self.endOfGame():
                self.play(allMoves[i])
                i += 1
        return self.winner(), i

    def print(self):
        print(Clobber_2d.to_string(self.board))
