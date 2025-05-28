import GUI
from constant import *
import pygame
import sys


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro Game Menu")


WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

def draw_menu():
    button_rect_start = pygame.Rect(325, 200, 150, 50)
    button_rect_exit = pygame.Rect(325, 280, 150, 50)
    button_color_start = (0, 200, 100)
    button_color_red = (210, 92, 92)
    text_color = (255, 255, 255)
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font("fonts/Arial.ttf", 30)
    text_surface_start = font.render("Bắt đầu", True, text_color)
    text_surface_exit = font.render("Thoát", True, text_color)
    text_rect_start = text_surface_start.get_rect(center=button_rect_start.center)
    text_rect_exit = text_surface_exit.get_rect(center=button_rect_exit.center)
    pygame.draw.rect(screen, button_color_start, button_rect_start, border_radius=12)
    pygame.draw.rect(screen, button_color_red, button_rect_exit, border_radius=12)
    screen.blit(text_surface_start, text_rect_start)
    screen.blit(text_surface_exit, text_rect_exit)
    return button_rect_start, button_rect_exit

def draw_game_mode():
    font = pygame.font.Font("fonts/Arial.ttf", 30)
    title = font.render("Chế độ AI", True, WHITE)
    button_rect_normal = pygame.Rect(325, 200, 150, 50)
    button_rect_difficult = pygame.Rect(325, 280, 150, 50)
    button_color = (0, 200, 100)
    text_color = (255, 255, 255)
    screen.fill(BACKGROUND_COLOR)
    text_surface_normal = font.render("Trung bình", True, text_color)
    text_surface_difficult = font.render("Khó", True, text_color)
    text_rect_normal = text_surface_normal.get_rect(center=button_rect_normal.center)
    text_rect_difficult = text_surface_difficult.get_rect(center=button_rect_difficult.center)
    pygame.draw.rect(screen, button_color, button_rect_normal, border_radius=12)
    pygame.draw.rect(screen, button_color, button_rect_difficult, border_radius=12)
    screen.blit(title, (325, 100))
    screen.blit(text_surface_normal, text_rect_normal)
    screen.blit(text_surface_difficult, text_rect_difficult)
    return button_rect_normal, button_rect_difficult
state_menu = "menu"
if __name__ == "__main__":
    while True:
        if state_menu == "menu":
            draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state_menu == "menu":
                    start_button, exit_button = draw_menu() 
                    if start_button.collidepoint(event.pos):
                        state_menu = "game_mode"
                        normal_button, difficult_button = draw_game_mode()
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                elif state_menu == "game_mode":          
                    if normal_button.collidepoint(event.pos):
                            game = GUI.TicTacToe()
                            game.max_depth = 2
                            game.run()
                    elif difficult_button.collidepoint(event.pos):
                            game = GUI.TicTacToe()
                            game.max_depth = 3
                            game.run()
        pygame.display.flip()
    game = GUI.TicTacToe()
    game.run()