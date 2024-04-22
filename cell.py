import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False
        self.number_font = pygame.font.SysFont("arial", 40)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        x = self.col * 50 + 25  # centers of the cells both vertical and horizontal
        y = self.row * 50 + 25

        if self.value != 0:
            number = self.number_font.render(str(self.value), True, (0, 0, 0))
            number_rect = number.get_rect(center=(x, y))
            self.screen.blit(number, number_rect)
        elif self.sketched_value != 0:
            number = self.number_font.render(str(self.sketched_value), True, (100, 100, 100))
            number_rect = number.get_rect(center=(x, y))
            self.screen.blit(number, number_rect)
