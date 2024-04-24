#Final Menu Screen
import sys
import pygame sys
from board import Board

def draw_game_start(screen):
    #title font
    start_title_font = pygame.font.Font(None, 100)
    game_mode_font = pygame.font.Font(None, 85)
    button_font = pygame.font.Font(None, 70)

    #Color Background
    screen.fill(BG_COLOR)

    #Inittialize and draw title
    title_surface = start_title_font.render("Welcome to Sudoku", 0, LINE_COLOR)
    title_rectangle = title_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rectangle)
    mode_surface = game_mode_font.render("Select Game Mode:", 0, LINE_COLOR)
    mode_rectangle = mode_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 10))
    screen.blit(mode_surface, mode_rectangle)

    #Initialize buttons
    #Initialize text first
    easy_text = button_font.render("Easy", 0, (255, 255, 255))
    med_text = button_font.render("Medium", 0, (255, 255, 255))
    hard_text = button_font.render("Hard", 0, (255, 255, 255))

    #Initialize button background and text
    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill(LINE_COLOR)
    easy_surface.blit(easy_text, (10, 10))
    med_surface = pygame.Surface((med_text.get_size()[0] + 20, med_text.get_size()[1] + 20))
    med_surface.fill(LINE_COLOR)
    med_surface.blit(med_text, (10, 10))
    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill(LINE_COLOR)
    hard_surface.blit(hard_text, (10, 10))

    #Initialize button rectangle
    easy_rectangle = easy_surface.get_rect(
        center=(WIDTH // 2 - 150, HEIGHT // 2 + 120))
    med_rectangle = med_surface.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 120))
    hard_rectangle = hard_surface.get_rect(
        center=(WIDTH // 2 + 150, HEIGHT // 2 + 120))

    #Draw buttons
    screen.blit(easy_surface, easy_rectangle)
    screen.blit(med_surface, med_rectangle)
    screen.blit(hard_surface, hard_rectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #FIX RETURN FOR THESE THREE IFS
                if easy_rectangle.collidepoint(event.pos):
                    #Checks if mouse is on easy button
                    return # if mouse on easy, we can return to main
                elif med_rectangle.collidepoint(event.pos):
                    #Checks if mouse is on easy button
                    return # if mouse on easy, we can return to main
                elif hard_rectangle.collidepoint(event.pos):
                    #Checks if mouse is on easy button
                    return # if mouse on easy, we can return to main
        pygame.display.update()


def draw_game_over():
    game_over_font = pygame.font.Font(None, 70)
    screen.fill(BG_COLOR)

    game_over_surf = game_over_font.render("Game Over :(", 0, LINE_COLOR)
    game_over_rectangle = game_over_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(game_over_surf, game_over_rectangle)

def draw_game_won():
    game_won_font = pygame.font.Font(None, 70)
    screen.fill(BG_COLOR)

    game_won_surf = game_won_font.render("Game Won!", 0, LINE_COLOR)
    game_won_rectangle = game_won_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(game_won_surf, game_won_rectangle)
