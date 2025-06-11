import numpy as np
import pygame
from ai import *
from constant import *

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Toc Toe")
        self.font = pygame.font.SysFont(None, 40)
        self.board = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
        self.running = True
        self.turn = O_TURN
        self.status_game = []
        self.current_move = None
        self.score_o = 0
        self.score_x = 0
        self.max_depth = GAME_MODE_NORMAL

    def draw_score_table(self):
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (WIDTH-200, 0, 200, HEIGHT), 0)
        pygame.draw.rect(self.screen, LINE_COLOR, (WIDTH-200, 0, 200, HEIGHT), 5)
        font = pygame.font.SysFont(None, 50)
        text_chess_o = font.render(f"O", True, O_COLOR)
        text_chess_x = font.render(f"X", True, X_COLOR)
        text_score_o = font.render(f" - {self.score_o}", True, (255,255,255))  
        text_score_x = font.render(f" - {self.score_x}", True, (255,255,255))
        self.screen.blit(text_chess_o, (WIDTH-150, 30))       
        self.screen.blit(text_score_o, (WIDTH-110, 30))       
        self.screen.blit(text_chess_x, (WIDTH-150, 80))       
        self.screen.blit(text_score_x, (WIDTH-110, 80))

    def draw_button_restart(self):
        button_rect = pygame.Rect(620, 200, 160, 50)
        button_color = (0, 200, 100)
        text_color = (255, 255, 255)
        font = pygame.font.Font("fonts/Arial.ttf", 30)
        text_surface = font.render("Chơi lại", True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=12)
        self.screen.blit(text_surface, text_rect)
        return button_rect

    def draw_lines(self):
        for i in range(BOARD_ROWS+1):
            pygame.draw.line(self.screen, LINE_COLOR, (0, i*40), (WIDTH-200, i*40), 5)
            pygame.draw.line(self.screen, LINE_COLOR, (i*40, 0), (i*40, HEIGHT), 5)
            
    def draw_chess(self):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if self.board[row][column] == O_TURN:
                    pygame.draw.circle(self.screen, O_COLOR, (20 + column*40, row*40 + 20), radius=15, width=3)
                elif self.board[row][column] == X_TURN:
                    pygame.draw.line(self.screen, X_COLOR, (column*40+5, row*40+5), (column*40+35, row*40+35), 4)
                    pygame.draw.line(self.screen, X_COLOR, (column*40+35, row*40+5), (column*40+5, row*40+35), 4)

    def draw_status_turn(self, typeChess):
        font = pygame.font.Font("fonts/Arial.ttf", 20)
        if (typeChess == X_TURN):
            title = font.render("AI đang suy nghĩ", True, WHITE_COLOR)
        elif (typeChess == O_TURN):
            title = font.render("Lượt người chơi", True, WHITE_COLOR)
        self.screen.blit(title, (610,120))
        
        
    def draw_status_game(self, winning_cells):
        if not winning_cells or len(winning_cells) < TOTAL_CHESS:
            return
        
        winning_cells.sort()
        
        start_cell = winning_cells[0]
        end_cell = winning_cells[-1]
        
        start_point = (start_cell[1] * 40 + 20, start_cell[0] * 40 + 20) 
        end_point = (end_cell[1] * 40 + 20, end_cell[0] * 40 + 20)
        
        pygame.draw.line(self.screen, LINE_STATUS_COLOR, start_point, end_point, 5)

    def draw_current_move(self):
        if self.current_move == None:
            return
        highlight_rect = pygame.Rect(self.current_move[1]*40, self.current_move[0]*40, 40, 40)
        pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, highlight_rect, 3)

    def convert_to_position(self, pos):
        convert_position = tuple([pos[1]//40, pos[0]//40])
        return convert_position

    def make_moves(self, pos, typeChess):
        row = pos[0]//40
        column = pos[1]//40
        try:
            if (self.board[row][column] == None):
                if (typeChess == X_TURN):
                    self.board[row][column] = X_TURN
                elif (typeChess == O_TURN):
                    self.board[row][column] = O_TURN
                return True
            return False
        except:
            return False

    def convert_move_ai(self, move_ai):
        return tuple([move_ai[0]*40, move_ai[1]*40])
      
    def is_board_full(self):
        for x in self.board:
            if None in x:
                return False
        return True
            
    def check_status_game(self, current_move, typeChess):
        direct = {
            ((-1,0), (1,0)),
            ((0,-1), (0,1)),
            ((-1, -1), (1, 1)),
            ((-1, 1), (1, -1))
        }
        for direct1, direct2 in direct:
            count = 1
            winning_cells = [current_move]
            row = current_move[0] + direct1[0]
            col = current_move[1] + direct1[1]
            while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] == typeChess:
                winning_cells.append((row, col))
                row += direct1[0]
                col += direct1[1]
                count += 1
            row = current_move[0] + direct2[0]
            col = current_move[1] + direct2[1]
            while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and self.board[row][col] == typeChess:
                winning_cells.append((row, col))
                row += direct2[0]
                col += direct2[1]
                count += 1
            if count >= TOTAL_CHESS:
                return [WIN_GAME, typeChess, winning_cells]
        if self.is_board_full():
            return [TIE_GAME, typeChess, []]
        return None

    def reset_game(self):
        self.board = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
        self.status_game = []
        self.turn = O_TURN
        self.current_move = None        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.status_game:
                restart_button = self.draw_button_restart()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.reset_game()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:     
                    position_moves = pygame.mouse.get_pos()             
                    if self.turn == O_TURN:
                        move_o = [position_moves[1], position_moves[0]]
                        if (self.make_moves(move_o, O_TURN)):
                            self.current_move = tuple([move_o[0]//40, move_o[1]//40])
                            self.draw()
                            pygame.display.flip()
                            self.turn = X_TURN
                            check = self.check_status_game(self.current_move, O_TURN)
                            if check != None:
                                if check[0] == WIN_GAME:
                                    self.score_o += 1
                                self.status_game = check

    def ai_move(self):
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        if self.turn == X_TURN and not self.status_game:
            ai = AI(board=self.board)
            move_ai = ai.find_best_move(self.max_depth)
            self.current_move = move_ai
            if (move_ai != None):
                self.turn = O_TURN
                self.board[move_ai[0]][move_ai[1]] = X_TURN
                check = self.check_status_game(move_ai, X_TURN)
                if check != None:
                    if check[0] == WIN_GAME:
                        self.score_x += 1
                    self.status_game = check
        pygame.event.set_allowed([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])




    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_score_table()
        self.draw_lines()
        self.draw_chess()
        
        if self.current_move != None:
            self.draw_current_move()

        if self.status_game:
            self.draw_status_game(self.status_game[2])
            self.draw_button_restart()

    def run(self):
        while self.running:
            self.draw()
            if self.turn == O_TURN:
                self.draw_status_turn(O_TURN)
                self.handle_events()
            pygame.display.flip()
            if self.turn == X_TURN:
                self.draw_status_turn(X_TURN)
                pygame.display.flip()
                self.ai_move()
        pygame.quit()