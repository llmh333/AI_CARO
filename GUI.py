import numpy as np
import pygame
from ai import*
from constant import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Toc Toe")
font = pygame.font.SysFont(None, 40)

board = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def draw_score_table(score_o: int, score_x: int):
    global screen
    pygame.draw.rect(screen, BACKGROUND_COLOR, (WIDTH-200, 0, 200, HEIGHT), 0)
    pygame.draw.rect(screen, LINE_COLOR, (WIDTH-200, 0, 200, HEIGHT), 5)

    font = pygame.font.SysFont(None, 50)

    text_chess_o = font.render(f"O".format(score_o), True, O_COLOR)
    text_chess_x = font.render(f"X".format(score_x), True, X_COLOR)

    text_score_o = font.render(f" - {score_o}".format(score_o), True, (255,255,255))  
    text_score_x = font.render(f" - {score_x}".format(score_x), True, (255,255,255))

    screen.blit(text_chess_o, (WIDTH-150, 30))       
    screen.blit(text_score_o, (WIDTH-110, 30))       
    screen.blit(text_chess_x, (WIDTH-150, 80))       
    screen.blit(text_score_x, (WIDTH-110, 80))       

def draw_button_restart():
    global screen
    button_rect = pygame.Rect(620, 200, 160, 50)
    button_color = (0, 200, 100)
    text_color = (255, 255, 255)
    font = pygame.font.Font("fonts/Arial.ttf", 30)
    text_surface = font.render("Chơi lại", True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)

    pygame.draw.rect(screen, button_color, button_rect, border_radius=12)
    screen.blit(text_surface, text_rect)

    return button_rect

def draw_lines():
    global screen
    for i in range(BOARD_ROWS+1):
        pygame.draw.line(screen,LINE_COLOR, (0, i*40), (WIDTH-200, i*40), 5)
        pygame.draw.line(screen, LINE_COLOR, (i*40, 0), (i*40, HEIGHT), 5)
        
def draw_chess():
    global screen
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == O_TURN:
                pygame.draw.circle(screen, O_COLOR, (20 + column*40, row*40 + 20),radius=15,width=3)
            elif board[row][column] == X_TURN:
                pygame.draw.line(screen, X_COLOR, (column*40+5, row*40+5), (column*40+35, row*40+35), 4)
                pygame.draw.line(screen, X_COLOR, (column*40+35, row*40+5), (column*40+5, row*40+35), 4)


def draw_status_game(winning_cells):
    global screen
    if not winning_cells or len(winning_cells) < TOTAL_CHESS:
        return
    
    winning_cells.sort()
    
    start_cell = winning_cells[0]
    end_cell = winning_cells[-1]
    
    start_point = (start_cell[1] * 40 + 20, start_cell[0] * 40 + 20) 
    end_point = (end_cell[1] * 40 + 20, end_cell[0] * 40 + 20)
    
    pygame.draw.line(screen, LINE_STATUS_COLOR, start_point, end_point, 5)

def draw_current_move(current_move: tuple[int,int]):
    global screen
    if current_move == None:
        return
    highlight_rect = pygame.Rect(current_move[1]*40, current_move[0]*40, 40, 40)
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 3)

def convert_to_position(pos: tuple[int, int]) -> tuple[int,int]:
    convert_position = tuple([pos[1]//40, pos[0]//40])
    return convert_position

def make_moves(pos: tuple[int,int], typeChess: int) -> bool:
    global board
    global screen
    row = pos[0]//40
    column = pos[1]//40
    try:
        if (board[row][column] == None):
            if (typeChess == X_TURN):
                board[row][column] = X_TURN
            elif (typeChess == O_TURN):
                board[row][column] = O_TURN
            return True
        return False
    except:
        return False

def convert_move_ai(move_ai: tuple[int,int]) -> tuple[int,int]:
    return tuple([move_ai[0]*40, move_ai[1]*40])
  
def is_board_full():
    for x in board:
        if None in x:
            return False
    return True
        
def checkStatusGame(current_move: tuple[int, int], typeChess: int) -> tuple[int,int]:
    global board
    
    start_position = end_position = None

    direct = {
        ((-1,0), (1,0)),
        ((0,-1), (0,1)),
        ((-1, -1), (1, 1)),
        ((-1, 1), (1, -1))
    }
    for direct1 , direct2 in direct:
        count = 1
        winning_cells = [current_move]
        row = current_move[0] + direct1[0]
        col = current_move[1] + direct1[1]
        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and board[row][col] == typeChess:
            winning_cells.append((row, col))
            row += direct1[0]
            col += direct1[1]
            count += 1

        row = current_move[0] + direct2[0]
        col = current_move[1] + direct2[1]
        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and board[row][col] == typeChess:
            winning_cells.append((row, col))
            row += direct2[0]
            col += direct2[1]
            count += 1
        if count >= TOTAL_CHESS:
            return [WIN_GAME, typeChess, winning_cells]

    if is_board_full():
        return [TIE_GAME, typeChess, []]


running = True
turn = O_TURN
status_game = []
current_move = None
score_o = score_x = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        screen.fill(BACKGROUND_COLOR)
        draw_score_table(score_o, score_x)
        draw_lines()
        draw_chess()

        if current_move != None:
            draw_current_move(current_move)
        
        if status_game != []:
            draw_status_game(status_game[2])
            restart_button = draw_button_restart()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    board = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
                    status_game = []
                    turn = O_TURN
                    current_move = None
                    continue
            pygame.display.flip()
            
        else:               
            if event.type == pygame.MOUSEBUTTONDOWN:     
                position_moves = pygame.mouse.get_pos()             
                if turn == O_TURN:
                    move_o = [position_moves[1], position_moves[0]]
                    if (make_moves(move_o, O_TURN)):
                        current_move = tuple([move_o[0]//40, move_o[1]//40])
                        turn = X_TURN
                        check = checkStatusGame(current_move, O_TURN)
                        if check != None:
                            if check[0] == WIN_GAME:
                                score_o += 1
                            status_game = check
                            continue
            if turn == X_TURN:
                ai = AI(board=board)
                move_ai = ai.find_best_move()
                current_move = move_ai
                if (move_ai != None):
                    turn = O_TURN
                    board[move_ai[0]][move_ai[1]] = X_TURN
                    check = checkStatusGame(move_ai, X_TURN)
                    if check != None:
                        if check[0] == WIN_GAME:
                            score_x += 1
                        status_game = check
                        continue
        pygame.display.flip()
        

pygame.quit()
