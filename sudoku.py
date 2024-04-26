import pygame
import sys
from board import Board

# Constants for screen dimensions and colors
WIDTH, HEIGHT = 450, 450
BG_COLOR = (250, 248, 239)  # Light gray background
LINE_COLOR = (0, 0, 0)  # Black lines


def draw_game_start(screen):
    start_title_font = pygame.font.Font(None, 60)  # Reduced size for better fit
    game_mode_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 30)

    screen.fill(BG_COLOR)
    title_surface = start_title_font.render("Welcome to Sudoku", True, LINE_COLOR)
    title_rectangle = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Centered at a quarter of the height
    screen.blit(title_surface, title_rectangle)

    mode_surface = game_mode_font.render("Select Game Mode:", True, LINE_COLOR)
    mode_rectangle = mode_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))  # Placed below the title
    screen.blit(mode_surface, mode_rectangle)

    # Button setup
    button_width = 100  # Uniform width for all buttons
    button_height = 50  # Uniform height for all buttons
    button_gap = 30  # Space between buttons
    total_button_width = 3 * button_width + 2 * button_gap
    start_x = (WIDTH - total_button_width) // 2  # Starting X coordinate to center buttons

    buttons = {}
    levels = ['EASY', 'MEDIUM', 'HARD']

    for index, level in enumerate(levels):
        text_surf = button_font.render(level, True, (255, 255, 255))
        button_surf = pygame.Surface((button_width, button_height))
        button_surf.fill(LINE_COLOR)
        # Get the text rectangle and center it within the button
        text_rect = text_surf.get_rect(center=(button_width // 2, button_height // 2))
        button_surf.blit(text_surf, text_rect)
        x_pos = start_x + index * (button_width + button_gap)
        button_rect = button_surf.get_rect(topleft=(x_pos, HEIGHT // 2))
        buttons[level] = (button_surf, button_rect)
        screen.blit(button_surf, button_rect)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for level, (surf, rect) in buttons.items():
                    if rect.collidepoint(event.pos):
                        return level  # Return the selected difficulty level


def draw_game_won(screen):
    win_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    win_screen.fill(BG_COLOR)
    win_text = "Congratulations! You've won!"
    win_surf = pygame.font.Font(None, 50).render(win_text, True, pygame.Color('green'))
    win_rect = win_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win_screen.blit(win_surf, win_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return  # Return to the caller to handle the next step


def draw_game_over(screen):
    over_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    over_screen.fill(BG_COLOR)
    over_text = "Game Over. Try again!"
    over_surf = pygame.font.Font(None, 50).render(over_text, True, pygame.Color('red'))
    over_rect = over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    over_screen.blit(over_surf, over_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return  # Return to the caller to handle the next step


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Add space for buttons
    pygame.display.set_caption("Sudoku")

    difficulty = draw_game_start(screen)  # Get difficulty from the menu
    board = Board(WIDTH, HEIGHT, screen, difficulty.lower())  # Initialize board with selected difficulty
    initial_board = [row[:] for row in board.board]  # Save the initial state of the board

    button_font = pygame.font.Font(None, 30)
    buttons = {
        'reset': {'text': 'Reset', 'rect': pygame.Rect(50, HEIGHT + 20, 100, 50), 'color': LINE_COLOR},
        'restart': {'text': 'Restart', 'rect': pygame.Rect(WIDTH // 2 - 50, HEIGHT + 20, 100, 50), 'color': LINE_COLOR},
        'exit': {'text': 'Exit', 'rect': pygame.Rect(WIDTH - 150, HEIGHT + 20, 100, 50), 'color': LINE_COLOR},
    }

    def draw_buttons():
        for button_key, button in buttons.items():
            pygame.draw.rect(screen, button['color'], button['rect'])  # Draw button background
            text_color = (255, 255, 255) if button['color'] == LINE_COLOR else (0, 0, 0)
            text_surf = button_font.render(button['text'], True, text_color)
            text_rect = text_surf.get_rect(center=button['rect'].center)
            screen.blit(text_surf, text_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if buttons['reset']['rect'].collidepoint(pos):
                    board.reset_to_original()
                elif buttons['restart']['rect'].collidepoint(pos):
                    main()  # Recursive call to restart the game
                    return  # Exit the current invocation of main
                elif buttons['exit']['rect'].collidepoint(pos):
                    running = False
                board.click(pos)  # Handle board click events
            elif event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_1, pygame.K_9 + 1):
                    board.sketch(event.key - pygame.K_0)
                elif event.key == pygame.K_RETURN:
                    board.place_number(board.cells[board.selected_cell[0]][board.selected_cell[1]].sketched_value)
                elif event.key == pygame.K_DELETE:
                    board.clear()  # Clear the selected cell

        if board.is_full():
            if board.check_win():
                draw_game_won(screen)
                running = False
            else:
                draw_game_over(screen)
                running = False

        screen.fill(BG_COLOR)
        board.draw()
        draw_buttons()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
