import sys
import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (245, 245, 245)  # Light grey background
LINE_COLOR = (25, 35, 45)  # Dark text color
BUTTON_COLOR = (15, 165, 145)  # Teal buttons
BUTTON_HOVER_COLOR = (5, 155, 135)  # Slightly darker teal on hover
FONT_SIZE_LARGE = 100
FONT_SIZE_MEDIUM = 85
FONT_SIZE_SMALL = 70

# Load Fonts
button_font = pygame.font.Font('Helvetica.ttf', FONT_SIZE_SMALL)  # Example with a custom font

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku Game')

def vertical_gradient(surface, rect, start_color, end_color):
    """Draws a vertical gradient filling the entire rect with a start and end color."""
    height = rect.height
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color
    for i in range(height):
        r = start_r + (end_r - start_r) * i / height
        g = start_g + (end_g - start_g) * i / height
        b = start_b + (end_b - start_b) * i / height
        pygame.draw.line(surface, (int(r), int(g), int(b)), (rect.left, rect.top + i), (rect.right, rect.top + i))

def create_button(text, font, center, color=BUTTON_COLOR, padding=20):
    """Creates a button with text and returns the surface and rect for the button."""
    text_surface = font.render(text, True, (255, 255, 255))
    button_surface = pygame.Surface((text_surface.get_width() + padding, text_surface.get_height() + padding)).convert_alpha()
    button_surface.fill((0, 0, 0, 0))  # Transparent

    rect = pygame.Rect(0, 0, text_surface.get_width() + padding, text_surface.get_height() + padding)
    vertical_gradient(button_surface, rect, color, (color[0]-30, color[1]-30, color[2]-30))

    button_surface.blit(text_surface, (padding // 2, padding // 2))
    button_rect = button_surface.get_rect(center=center)
    return button_surface, button_rect

def draw_game_start(screen):
    """Draws the game start menu and handles button interactions."""
    start_title_font = pygame.font.Font('Helvetica.ttf', FONT_SIZE_LARGE)
    game_mode_font = pygame.font.Font('Helvetica.ttf', FONT_SIZE_MEDIUM)

    screen.fill(BG_COLOR)

    # Draw Title
    title_surface = start_title_font.render("Welcome to Sudoku", True, LINE_COLOR)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rect)

    # Draw Game Mode Text
    mode_surface = game_mode_font.render("Select Game Mode:", True, LINE_COLOR)
    mode_rect = mode_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
    screen.blit(mode_surface, mode_rect)

    # Draw Buttons
    easy_surface, easy_rect = create_button("EASY", button_font, (WIDTH // 2 - 150, HEIGHT // 2 + 120))
    med_surface, med_rect = create_button("MEDIUM", button_font, (WIDTH // 2, HEIGHT // 2 + 120))
    hard_surface, hard_rect = create_button("HARD", button_font, (WIDTH // 2 + 150, HEIGHT // 2 + 120))

    buttons = [(easy_surface, easy_rect), (med_surface, med_rect), (hard_surface, hard_rect)]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for _, rect in buttons:
                    if rect.collidepoint(event.pos):
                        return  # Exit the menu on button click

        # Handle button hover effects
        for surface, rect in buttons:
            if rect.collidepoint(mouse_pos):
                inflated_rect = rect.inflate(20, 20)
                screen.blit(surface, inflated_rect)
            else:
                screen.blit(surface, rect)

        pygame.display.update()

draw_game_start(screen)