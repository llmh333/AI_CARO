import time
from constant import *
import os
import numpy as np
class AI:
    def __init__(self, board):
        self.board = board
        self.empty_positions = set()
        self.approved_table = {}
        self.center = (BOARD_ROWS // 2, BOARD_COLUMNS // 2)
        self.direct = [
            ((-1,0), (1,0)),
            ((0,-1), (0,1)),
            ((-1, -1), (1, 1)),
            ((-1, 1), (1, -1))
        ]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == None:
                    self.empty_positions.add((i, j))

    def make_move(self, move, typeChess):
        if move in self.empty_positions:
            self.board[move[0]][move[1]] = typeChess
            self.empty_positions.remove(move)
            return True
        return False

    def undo_move(self, move):
        if self.board[move[0]][move[1]] is not None:
            self.board[move[0]][move[1]] = None
            self.empty_positions.add(move)
            return True
        return False
    
    def is_board_full(self):
        return len(self.empty_positions) == 0
    
    def get_all_move_possible(self):
        moves = set()
        dx = [0, 0, 1, -1, -1, 1, -1, 1]
        dy = [1, -1, 0, 0, 1, 1, -1, -1]
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.board[row][col] != None:
                    for k in range(len(dx)):
                        row_new = row + dx[k]
                        col_new = col + dy[k]
                        if 0 <= row_new < BOARD_ROWS and 0 <= col_new < BOARD_COLUMNS:
                            if self.board[row_new][col_new] == None:
                                moves.add((row_new, col_new))    
        moves = list(moves)
        if not moves and self.empty_positions:
            moves = list(self.empty_positions)
        
        moves.sort(key=lambda m: abs(m[0] - self.center[0]) + abs(m[1] - self.center[1]))
        return moves
    
    def check_status_game(self, move, typeChess):
        for direct1, direct2 in self.direct:
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
        return None
    def get_board_hash(self):
        return tuple(tuple(row) for row in self.board)

    def attack_point(self, move, typeChess):
        best_point = 0
        for direct1, direct2 in self.direct:
            count = 0
            score = 0
            enemy_chess = 0
            row_new = move[0]
            col_new = move[1]
            while 0 <= row_new < BOARD_ROWS and 0 <= col_new < BOARD_COLUMNS and self.board[row_new][col_new] == typeChess:
                row_new += direct1[0]
                col_new += direct1[1]
                count += 1
                if 0 <= row_new < BOARD_ROWS and 0 <= col_new < BOARD_COLUMNS:
                    if self.board[row_new][col_new] != typeChess and self.board[row_new][col_new] != None:
                        enemy_chess += 1
            
            row_new = move[0]
            col_new = move[1]
            count -= 1
            while 0 <= row_new < BOARD_ROWS and 0 <= col_new < BOARD_COLUMNS and self.board[row_new][col_new] == typeChess:
                row_new += direct2[0]
                col_new += direct2[1]
                count += 1  
                if 0 <= row_new < BOARD_ROWS and 0 <= col_new < BOARD_COLUMNS:
                    if self.board[row_new][col_new] != typeChess and self.board[row_new][col_new] != None:
                        enemy_chess += 1    
            if count == 1:
                if enemy_chess == 2:
                    score = 5
                elif enemy_chess == 1:
                    score = 10
                elif enemy_chess == 0:
                    score = 15
            elif count == 2:
                if enemy_chess == 2:
                    score = 15
                elif enemy_chess == 1:
                    score = 20
                elif enemy_chess == 0:
                    score = 25
            elif count == 3:
                if enemy_chess == 2:
                    score = 25
                elif enemy_chess == 1:
                    score = 30
                elif enemy_chess == 0:
                    score = 35
            elif count == 4:
                if enemy_chess == 2:
                    score = 40
                elif enemy_chess == 1:
                    score = 90
                elif enemy_chess == 0:
                    score = 100
            best_point = max(best_point, score)
        return best_point  
    def defend_point(self, move, typeChess):
        best_point = 0
        for direct1, direct2 in self.direct:
            score = 0
            enemy_chess = 0 
            row_new = move[0] + direct1[0]
            col_new = move[1] + direct1[1]
            while 0 <= row_new < BOARD_ROWS and 0 <= col_new < BOARD_COLUMNS and self.board[row_new][col_new] != typeChess and self.board[row_new][col_new] != None:
                row_new += direct1[0]
                col_new += direct1[1]
                enemy_chess += 1
            
            row_new = move[0] + direct2[0]
            col_new = move[1] + direct2[1]
            while 0 <= row_new < BOARD_ROWS and 0 <= col_new < BOARD_COLUMNS and self.board[row_new][col_new] != typeChess and self.board[row_new][col_new] != None:
                row_new += direct2[0]
                col_new += direct2[1]
                enemy_chess += 1    
            if enemy_chess == 1:
                score = 5
            elif enemy_chess == 2:
                score = 10
            elif enemy_chess == 3:
                score = 80
            elif enemy_chess == 4:
                score = 100
            best_point = max(best_point, score)
        return best_point


    def minimax(self, depth, max_depth, typeChess, is_maximizing, move, alpha : float = -float('inf'), beta : float = float('inf')):

        status_game = self.check_status_game(move, typeChess)
        if status_game is not None:
            if status_game[0] == TIE_GAME:
                return 0
            if status_game[0] == WIN_GAME and status_game[1] == O_TURN:
                return -100+depth
            elif status_game[0] == WIN_GAME and status_game[1] == X_TURN:
                return 100-depth
        if depth >= max_depth:
            score_attack = self.attack_point(move, typeChess)
            score_defend = self.defend_point(move, typeChess)
            if typeChess == X_TURN:
                return max(score_attack-depth, score_defend-depth)
            else:
                return min(-score_attack+depth, -score_defend+depth)
        board_hash = self.get_board_hash()
        if board_hash in self.approved_table:
            stored_depth, stored_score = self.approved_table[board_hash]
            if stored_depth <= max_depth - depth:
                return stored_score

        move_possible = self.get_all_move_possible()
        if is_maximizing:
            best_score = -float('inf')
            for next_move in move_possible:
                self.make_move(next_move, X_TURN)
                score = self.minimax(depth+1, max_depth, X_TURN, False, next_move, alpha, beta)
                self.undo_move(next_move)

                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            
            self.approved_table[board_hash] = [max_depth - depth, best_score]
            return best_score
        else:
            best_score = float('inf')   
            for next_move in move_possible:
                self.make_move(next_move, O_TURN)
                score = self.minimax(depth+1, max_depth, O_TURN, True, next_move, alpha, beta)
                self.undo_move(next_move)
                best_score = min(score, best_score)

                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            self.approved_table[board_hash] = [max_depth - depth, best_score]
            return best_score
        
    def find_best_move(self, time_limit : float = 3.0):
        move = None
        best_score = -float('inf')
        # start_time = time.time()
        # while time.time() - start_time < time_limit:
        for next_move in self.get_all_move_possible():
            self.make_move(next_move, X_TURN)
            score_attack = self.attack_point(next_move, X_TURN)
            score_defend = self.defend_point(next_move, X_TURN)
            score = self.minimax(0, MAX_DEPTH, X_TURN, False, next_move, -float('inf'), float('inf'))
            if score < 0:  
                score_next_move = score_defend
                type_move = DEFEND_MOVE
            else:   
                score_next_move = score
                if score_attack > score_defend:
                    type_move = ATTACK_MOVE
                else:
                    type_move = DEFEND_MOVE
            self.undo_move(next_move)
            if score_next_move > best_score:
                best_score = score_next_move
                move = next_move
            elif score_next_move == best_score:
                if type_move == DEFEND_MOVE:
                    best_score = score_next_move
                    move = next_move    
        return move
    
# board = [
#     [None, None, None, None, 'X', None, None, None, None, None],
#     [None, None, None, None, 'O', None, None, None, None, None],
#     [None, None, None, None, 'O', None, None, None, None, None],
#     [None, None, None,  'O', 'O', 'O', None, 'O', None, None],
#     [None, None, 'X',   'O', 'O', 'O', 'X', None, None, None],
#     [None, None, None, None, 'X', 'X', 'X', None, None, None],
#     [None, None, None, None, None, 'X', None, None, None, None],
#     [None, None, None, None, None, 'X', None, None, None, None],
#     [None, None, None, None, None, 'X', None, None, None, None],
#     [None, None, None, None, None, 'O', None, None, None, None]]
# turn = X_TURN
# while True:
#     if turn == O_TURN:
#         for x in board:
#             print(x)
#         print("---Turn O---")
#         row = int(input("row = "))
#         col = int(input("col = "))
#         os.system("cls")
#         board[row][col] = O_TURN
#         turn = X_TURN
#     elif turn == X_TURN:
#         ai = AI(board)
#         move = ai.find_best_move()
#         print(move)
#         if (move != None):
#             board[move[0]][move[1]] = X_TURN
#             turn = O_TURN