import numpy as np
import pygame
from minimax import*
from constant import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Toc Toe")
font = pygame.font.SysFont(None, 40)

board = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]



def draw_lines():
    global screen
    for i in range(BOARD_ROWS+1):
        pygame.draw.line(screen,LINE_COLOR, (0, i*40), (800, i*40), 5)
        pygame.draw.line(screen, LINE_COLOR, (i*40, 0), (i*40, 800), 5)
        
def draw_chess():
    global screen
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == O_TURN:
                pygame.draw.circle(screen, O_COLOR, (20 + column*40, row*40 + 20),radius=15,width=3)
            elif board[row][column] == X_TURN:
                pygame.draw.line(screen, X_COLOR, (column*40+5, row*40+5), (column*40+35, row*40+35), 4)
                pygame.draw.line(screen, X_COLOR, (column*40+35, row*40+5), (column*40+5, row*40+35), 4)


def draw_status_game(status_game, typechess):
    global screen
    rect = pygame.Rect(200,300,400,100)
    pygame.draw.rect(screen, STATUS_COLOR, rect)
    
    if status_game == WIN_GAME:
        text_surface1 = font.render("{} is Winner".format(typechess), True, O_COLOR)
        text_surface2 = font.render("Press Enter to play again!!!", True, O_COLOR)
        
        
    else:
        text_surface1 = font.render("Tie the Game", True, O_COLOR)
        text_surface2 = font.render("Press Enter to play again!!!", True, O_COLOR)
    text_rect1 = text_surface1.get_rect(center=(rect.centerx, rect.centery - 15))
    text_rect2 = text_surface2.get_rect(center=(rect.centerx, rect.centery + text_surface1.get_height()-5))
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)
        
    
def convert_to_position(pos: tuple[int, int]) -> tuple[int,int]:
    convert_position = tuple([pos[1]//40, pos[0]//40])
    return convert_position

def make_moves(pos: tuple[int,int], typeChess: int) -> bool:
    global board
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
    
    direct = {
        ((-1,0), (1,0)),
        ((0,-1), (0,1)),
        ((-1, -1), (1, 1)),
        ((-1, 1), (1, -1))
    }
    for direct1 , direct2 in direct:
        count = 1
        row = current_move[0] + direct1[0]
        col = current_move[1] + direct1[1]
        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and board[row][col] == typeChess:
            row += direct1[0]
            col += direct1[1]
            count += 1

        row = current_move[0] + direct2[0]
        col = current_move[1] + direct2[1]
        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLUMNS and board[row][col] == typeChess:
            row += direct2[0]
            col += direct2[1]
            count += 1
        
        if count >= TOTAL_CHESS:
            return [WIN_GAME, typeChess]

    if is_board_full():
        return [TIE_GAME, typeChess]


running = True
turn = X_TURN
status_game = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        screen.fill(BACKGROUND_COLOR)
        draw_lines()
        draw_chess()
        
        if status_game != []:
            print("Press Enter to play again!!!")
            draw_status_game(status_game[0], status_game[1])
            pygame.event.set_blocked([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
                    board = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
                    status_game = []
                    turn = X_TURN
        else:           
            if event.type == pygame.MOUSEBUTTONDOWN:            
                position_moves = pygame.mouse.get_pos()             
                if turn == X_TURN:
                    move_x = [position_moves[1], position_moves[0]]
                    if (make_moves(move_x, X_TURN)):
                        turn = O_TURN
                        check = checkStatusGame(tuple([move_x[0]//40, move_x[1]//40]), X_TURN)
                        if check != None:
                            status_game = check
                if turn == O_TURN:
                    ai = AI(board)
                    move_ai = ai.best_move()
                    # print(move_ai)
                    if (move_ai != None):
                        turn = X_TURN
                        board[move_ai[0]][move_ai[1]] = O_TURN
                        for x in board:
                            print(x)
                        check = checkStatusGame(move_ai, O_TURN)
                        if check != None:
                            status_game = check
        pygame.display.flip()
        

pygame.quit()
