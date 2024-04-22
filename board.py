import pygame
from cell import Cell
import sudoku_generator


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.rows = 9
        self.cols = 9
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.difficulty_levels = {'easy': 20, 'medium': 30, 'hard': 40}
        removed_cells = self.difficulty_levels.get(self.difficulty, 20)  # Default to easy if invalid
        self.board = sudoku_generator.generate_sudoku(9, removed_cells)
        self.cells = [[Cell(self.board[i][j], i, j, self.screen) for j in range(self.cols)] for i in range(self.rows)]
        self.selected_cell = None

    def draw(self):
        # draw each cell
        for row in self.cells:
            for cell in row:
                cell.draw()
        # draw grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            self.selected_cell = (int(y), int(x))
            return int(y), int(x)
        else:
            return None

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(value)
            # clear the sketch value
            self.cells[row][col].set_sketched_value(0)

    def reset_to_original(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                cell.set_cell_value(self.board[i][j])
                cell.set_sketched_value(0)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = self.cells[i][j].value

    def check_board(self):
        if (self.board.is_valid() and self.board.valid_in_box()
                and self.board.valid_in_row() and self.board.valid_in_col()
                is True):
            return True
        return False
