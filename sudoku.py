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
    button_font = pygame.font.Font(None, 50)

    screen.fill(BG_COLOR)
    title_surface = start_title_font.render("Welcome to Sudoku", True, LINE_COLOR)
    title_rectangle = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Centered at a quarter of the height
    screen.blit(title_surface, title_rectangle)

    mode_surface = game_mode_font.render("Select Game Mode:", True, LINE_COLOR)
    mode_rectangle = mode_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))  # Placed below the title
    screen.blit(mode_surface, mode_rectangle)

    # Button setup
    button_width = 138  # Uniform width for all buttons
    button_height = 50  # Uniform height for all buttons
    button_gap = 12  # Space between buttons
    total_button_width = 3 * button_width + 2*button_gap
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


def draw_game_won(screen, width):
    pygame.init()
    # Clear the screen with a background color (e.g., black)
    screen.fill(BG_COLOR)  # Fill screen with black

    # Define the message and settings
    win_text = "Congratulations!\n You've won!"
    font_size = 50
    font = pygame.font.Font(None, font_size)
    text_color = pygame.Color('green')
    lines = win_text.split('\n')

    # Calculate the height to start drawing the text to center it vertically
    total_height = len(lines) * font_size
    start_y = (screen.get_height() - total_height) // 2

    # Render each line
    for i, line in enumerate(lines):
        # Check the width
        line_surf = font.render(line, True, text_color)
        line_width = line_surf.get_width()
        if line_width > width:
            # Split the line into words
            words = line.split()
            accumulated_line = ""
            for word in words:
                # Check width
                test_line = accumulated_line + word + " "
                test_surf = font.render(test_line, True, text_color)
                test_width = test_surf.get_width()
                if test_width < width:
                    accumulated_line = test_line
                else:
                    # Render the accumulated line
                    temp_surf = font.render(accumulated_line, True, text_color)
                    screen.blit(temp_surf, ((width - temp_surf.get_width()) // 2, start_y))
                    start_y += font_size
                    accumulated_line = word + " "
            # Render the last accumulated line
            temp_surf = font.render(accumilated_line, True, text_color)
            screen.blit(temp_surf, ((width - temp_surf.get_width()) // 2, start_y))
            start_y += font_size
        else:
            # If the line is within the width, render it directly
            screen.blit(line_surf, ((width - line_width) // 2, start_y))
            start_y += font_size

    # Update the display
    pygame.display.flip()


def draw_game_over(screen):
    # Clear the screen or draw a game over message over the board
    background_color = (BG_COLOR)  # Red, green, blue (RGB)

    # Fill the screen with the background color
    screen.fill(background_color)
    over_text = "Game Over. Try again!"
    over_surf = pygame.font.Font(None, 50).render(over_text, True, pygame.Color('red'))
    screen.blit(over_surf, (50, HEIGHT // 2))  # Adjust position as needed
    pygame.display.flip()

    # Update the display to show the new color
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Add space for buttons
    pygame.display.set_caption("Sudoku")

    difficulty = draw_game_start(screen)  # Get difficulty from the menu
    board = Board(WIDTH, HEIGHT, screen, difficulty.lower())  # Initialize board with selected difficulty
    initial_board = [row[:] for row in board.board]  # Save the initial state of the board

    button_font = pygame.font.Font(None, 40)
    buttons = {
        'reset': {'text': 'Reset', 'rect': pygame.Rect(50, HEIGHT + 20, 100, 50), 'color': LINE_COLOR},
        'restart': {'text': 'Restart', 'rect': pygame.Rect(WIDTH // 2 - 50, HEIGHT + 20, 100, 50), 'color': LINE_COLOR},
        'exit': {'text': 'Exit', 'rect': pygame.Rect(WIDTH - 150, HEIGHT + 20, 100, 50), 'color': LINE_COLOR},
    }

    def draw_buttons():
        for button_key, button in buttons.items():
            pygame.draw.rect(screen, button['color'], button['rect'])  # Draw button background
            # Choose a text color that contrasts with the button color
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
                if event.key == pygame.K_LEFT:
                    board.move_selection(0, -1)
                elif event.key == pygame.K_RIGHT:
                    board.move_selection(0, 1)
                elif event.key == pygame.K_UP:
                    board.move_selection(-1, 0)
                elif event.key == pygame.K_DOWN:
                    board.move_selection(1, 0)
                elif event.key == pygame.K_1:
                    board.sketch(1)
                elif event.key == pygame.K_2:
                    board.sketch(2)
                elif event.key == pygame.K_3:
                    board.sketch(3)
                elif event.key == pygame.K_4:
                    board.sketch(4)
                elif event.key == pygame.K_5:
                    board.sketch(5)
                elif event.key == pygame.K_6:
                    board.sketch(6)
                elif event.key == pygame.K_7:
                    board.sketch(7)
                elif event.key == pygame.K_8:
                    board.sketch(8)
                elif event.key == pygame.K_9:
                    board.sketch(9)
                elif event.key == pygame.K_RETURN:
                    board.place_number(board.cells[board.selected_cell[0]][board.selected_cell[1]].sketched_value)
                elif event.key == pygame.K_DELETE:
                    board.clear()  # This should clear the selected cell

        # Check for game over or win condition
        if board.is_full():
            if board.check_win():
                draw_game_won(screen, 450)  # Define this function to show the win screen
                pygame.display.update()
                pygame.time.wait(5000)  # Wait for 5 seconds
                running = False
            else:
                draw_game_over(screen)  # Define this function to show the game over screen
                pygame.display.update()
                pygame.time.wait(5000)  # Wait for 5 seconds
                running = False

        screen.fill(BG_COLOR)
        board.draw()
        draw_buttons()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
