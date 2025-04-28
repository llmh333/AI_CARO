from constant import *
import numpy as np
import os

class AI:
    def __init__(self, board):
        self.board = board
        self.move = None
    def make_move(self, move : tuple([int, int]), typeChess):
        if (self.board[move[0]][move[1]] == None):
            self.board[move[0]][move[1]] = typeChess
            return True
        return False

    def remake_move(self, move: tuple([int, int])):
        if (self.board[move[0]][move[1]] != None):
            self.board[move[0]][move[1]] = None
            return True
        return False

    def is_board_full(self):
        for x in self.board:
            if None in x:
                return False
        return True

    def get_all_move_possible(self):
        dx = [-1, 1, 0, 0, -1, 1, -1, -1]
        dy = [0, 0, -1, 1, 1, 1, -1, 1]
        moves = set()
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if (self.board[row][col] != None):
                    for i in range(8):
                        row_new = row + dx[i]
                        col_new = col + dy[i]
                        if row_new >= 0 and row_new < BOARD_ROWS and col_new >= 0 and col_new < BOARD_COLUMNS:
                            if (self.board[row_new][col_new] == None) and (not(row_new,col_new) in moves):
                                moves.add((row_new,col_new))
        moves = list(moves)
        center = (BOARD_ROWS // 2, BOARD_COLUMNS // 2)
        moves.sort(key=lambda m: abs(m[0] - center[0]) + abs(m[1] - center[1]))
        return list(moves)

    def check_status_game(self, move, typeChess):
        direct = [
            ((-1,0), (1,0)),
            ((0,-1), (0,1)),
            ((-1, -1), (1, 1)),
            ((-1, 1), (1, -1))
        ]
        for direct1, direct2 in direct:
            count = 1
            row = move[0] + direct1[0]
            col = move[1] + direct1[1]
            while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] == typeChess:
                row += direct1[0]
                col += direct1[1]
                count += 1

            row = move[0] + direct2[0]
            col = move[1] + direct2[1]
            while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] == typeChess:
                row += direct2[0]
                col += direct2[1]
                count += 1        
            if count >= TOTAL_CHESS:   
                return [WIN_GAME, typeChess]
        if self.is_board_full():
            return [TIE_GAME, typeChess]          

    
    def minimax(self, depth, is_maximizing, move: tuple([int, int]), type_chess, alpha : float = -float('inf'), beta : float = float('inf')):
        check_status = self.check_status_game(move, type_chess)
        if check_status != None:
            if check_status[0] == WIN_GAME and check_status[1] == X_TURN:
                return -10+depth
            elif check_status[0] == WIN_GAME and check_status[1] == O_TURN:
                return 10-depth
            elif check_status[0] == TIE_GAME:
                return 0
        if depth == 5:
            return 0
        moves = self.get_all_move_possible()
        if not moves:
            return self.evaluate_board(self.board, O_TURN)
        if is_maximizing:
            best_score = float('-inf')
            for move in moves:
                self.make_move(move, O_TURN)
                score = self.minimax(depth+1, False, move, O_TURN, alpha, beta)
                self.remake_move(move)
                best_score = max(score,best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in moves:
                self.make_move(move, X_TURN)
                score = self.minimax(depth+1, True, move, X_TURN, alpha, beta)
                self.remake_move(move)
                best_score = min(score,best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score


    def best_move(self):
        best_score = -float('inf')
        move = None
        moves = self.get_all_move_possible()
        if not moves:
            return None
        
        for move_possible in moves:
            self.make_move(move_possible,O_TURN)
            score = self.minimax(0, False, move_possible, O_TURN, -float('inf'), float('inf'))
            self.remake_move(move_possible)
            if score > best_score:
                best_score = score
                move = move_possible
        return move

# board = np.full((BOARD_COLUMNS,BOARD_ROWS), None, dtype=object)
# board[0][0] = O_TURN
# board[0][2] = O_TURN
# board[1][0] = O_TURN
# board[1][1] = X_TURN
# board[1][2] = X_TURN
# board[2][2] = X_TURN
# turn = X_TURN

# while True:
#     if turn == X_TURN:
#         for x in board:
#             print(x)
#         row = int(input("row = "))
#         col = int(input("col = "))
#         os.system("cls")
#         board[row][col] = X_TURN
#         turn = O_TURN
#     elif turn == O_TURN:
#         ai = AI(board)
#         move = ai.best_move()
#         print(move)
#         if (move != None):
#             board[move[0]][move[1]] = O_TURN
#             turn = X_TURN
        