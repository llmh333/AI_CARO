import time
from constant import *
import os
import numpy as np

class AI:
    def __init__(self, board):
        self.board = board
        self.empty_positions = set()
        self.transposition_table = {}
        self.center = (BOARD_ROWS // 2, BOARD_COLUMNS // 2)
        self.directions = [
            ((-1,0), (1,0)),   
            ((0,-1), (0,1)),   
            ((-1, -1), (1, 1)),
            ((-1, 1), (1, -1)) 
        ]
        
        self.move_deltas = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
        
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
    
    def quick_attack_score(self, move, typeChess):
        max_score = 0
        for dir1, dir2 in self.directions:
            count = 1 
            blocked = 0
            
            row, col = move[0] + dir1[0], move[1] + dir1[1]
            while (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] == typeChess):
                count += 1
                row += dir1[0]
                col += dir1[1]
            if (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] is not None):
                blocked += 1
                
            row, col = move[0] + dir2[0], move[1] + dir2[1]
            while (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] == typeChess):
                count += 1
                row += dir2[0]
                col += dir2[1]
            if (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] is not None):
                blocked += 1

            if count >= 5:
                return 10000
            elif count == 4:
                score = 1000 if blocked == 0 else (500 if blocked == 1 else 50)
            elif count == 3:
                score = 100 if blocked == 0 else (50 if blocked == 1 else 10)
            elif count == 2:
                score = 10 if blocked == 0 else (5 if blocked == 1 else 1)
            else:
                score = 1
                
            max_score = max(max_score, score)
        return max_score
    
    def quick_defend_score(self, move, my_type):
        enemy_type = O_TURN if my_type == X_TURN else X_TURN
        return self.quick_attack_score(move, enemy_type)
    
    def get_all_move_possible(self, limit=20):
        moves = set()
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.board[row][col] is not None:
                    for dx, dy in self.move_deltas:
                        new_row, new_col = row + dx, col + dy
                        if (0 <= new_row < BOARD_ROWS and 0 <= new_col < BOARD_COLUMNS and self.board[new_row][new_col] is None):
                            moves.add((new_row, new_col))
        
        moves = list(moves)
        
        if not moves and self.empty_positions:
            center_moves = [(row, col) for row, col in self.empty_positions 
                           if abs(row - self.center[0]) <= 2 and abs(col - self.center[1]) <= 2]
            moves = center_moves if center_moves else list(self.empty_positions)
        
        move_scores = []
        for move in moves:
            attack_score = self.quick_attack_score(move, X_TURN)
            defend_score = self.quick_defend_score(move, X_TURN)
            distance_penalty = abs(move[0] - self.center[0]) + abs(move[1] - self.center[1])
            total_score = attack_score + defend_score - distance_penalty * 0.1
            move_scores.append((total_score, move))
        
        move_scores.sort(reverse=True)
        return [move for _, move in move_scores[:limit]]
    
    
    
    def check_status_game(self, move, typeChess):
        for direct1, direct2 in self.directions:
            count = 1
            
            row, col = move[0] + direct1[0], move[1] + direct1[1]
            while (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and 
                   self.board[row][col] == typeChess):
                count += 1
                row += direct1[0]
                col += direct1[1]

            row, col = move[0] + direct2[0], move[1] + direct2[1]
            while (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and 
                   self.board[row][col] == typeChess):
                count += 1
                row += direct2[0]   
                col += direct2[1]
                
            if count >= TOTAL_CHESS:
                return [WIN_GAME, typeChess]
                
        if self.is_board_full():
            return [TIE_GAME, typeChess]    
        return None
    
    def get_board_hash(self):
        return hash(tuple(tuple(row) for row in self.board))

    def evaluate_position(self, last_move, player):

        status = self.check_status_game(last_move, player)
        if status:
            if status[0] == WIN_GAME:
                return 10000 if status[1] == X_TURN else -10000
            return 0 
        
        my_score = self.position_score(X_TURN)
        enemy_score = self.position_score(O_TURN)
        return my_score - enemy_score
    
    def position_score(self, player):
        total_score = 0
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                if self.board[row][col] == player:
                    total_score += self.quick_attack_score((row, col), player)
        return total_score

    def minimax(self, depth, max_depth, typeChess, is_maximizing, last_move, alpha=float('-inf'), beta=float('inf')):
        
        if last_move:
            evaluation = self.evaluate_position(last_move, typeChess)
            if abs(evaluation) >= 10000:  # Game over
                return evaluation + (depth if evaluation < 0 else -depth)
        
        if depth >= max_depth:
            return self.evaluate_position(last_move, typeChess) if last_move else 0
        
        board_hash = self.get_board_hash()
        if board_hash in self.transposition_table:
            stored_depth, stored_score, stored_type = self.transposition_table[board_hash]
            if stored_depth >= max_depth - depth:
                if stored_type == 'exact':
                    return stored_score
                elif stored_type == 'alpha' and stored_score <= alpha:
                    return stored_score
                elif stored_type == 'beta' and stored_score >= beta:
                    return stored_score

        moves = self.get_all_move_possible(limit=15)
        
        if is_maximizing:
            best_score = float('-inf')
            hash_type = 'alpha'
            
            for move in moves:
                self.make_move(move, X_TURN)
                score = self.minimax(depth + 1, max_depth, X_TURN, False, move, alpha, beta)
                self.undo_move(move)

                if score > best_score:
                    best_score = score
                    
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    hash_type = 'beta'
                    break
                    
        else:
            best_score = float('inf')
            hash_type = 'alpha'
            
            for move in moves:
                self.make_move(move, O_TURN)
                score = self.minimax(depth + 1, max_depth, O_TURN, True, move, alpha, beta)
                self.undo_move(move)

                if score < best_score:
                    best_score = score
                    
                beta = min(beta, best_score)
                if beta <= alpha:
                    hash_type = 'beta'
                    break
        
        if abs(best_score) < 9000: 
            self.transposition_table[board_hash] = (max_depth - depth, best_score, hash_type)
        
        return best_score
        
    def find_best_move(self, max_depth):
        start_time = time.time()
        total_time = None
        best_move = None
        
        for current_depth in range(2, max_depth + 1):
            if time.time() - start_time > 5.0:
                total_time = time.time() - start_time
                break
             
            temp_best_move = None
            best_score = float('-inf')
            
            moves = self.get_all_move_possible(limit=15)
            
            for move in moves:
                self.make_move(move, X_TURN)
                
                if self.check_status_game(move, X_TURN):
                    self.undo_move(move)
                    return move
                
                score = self.minimax(1, current_depth, X_TURN, False, move)
                self.undo_move(move)
                
                if score > best_score:
                    best_score = score
                    temp_best_move = move
            
            if temp_best_move:
                best_move = temp_best_move
        if total_time == None:
            total_time = time.time() - start_time   
        print(total_time)
        return best_move
