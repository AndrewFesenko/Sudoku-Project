#Final Menu Screen

import pygame sys
from board import Board

def draw_game_start(screen):
    #title font
    start_title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 70)

    #Color Background
    screen.fill(BG_COLOR)

    #Inittialize and draw title
    title_surface = start_title_font.render("Welcome to Sudoku", 0, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rectangle)

    #Initialize buttons
    #Initialize text first
    easy_text = button_font.render("Easy", 0, (255, 255, 255))
    med_text = button_font.render("Medium", 0, (255, 255, 255))
    hard_text = button_font.render("Hard", 0, (255, 255, 255))

    #Initialize button background and text
    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill(LINE_COLOR)
    easy_surface.blit
