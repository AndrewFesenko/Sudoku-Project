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
        self.difficulty_levels = {'easy': 30, 'medium': 40, 'hard': 50}
        removed_cells = self.difficulty_levels.get(self.difficulty, 20)  # Default to easy if invalid
        self.board = sudoku_generator.generate_sudoku(9, removed_cells)
        self.cells = [[Cell(self.board[i][j], i, j, self.screen) for j in range(self.cols)] for i in range(self.rows)]
        self.selected_cell = None
        self.initial_board = [[cell.value for cell in row] for row in self.cells]

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
            # Unselect all cells
            for row in self.cells:
                for cell in row:
                    cell.selected = False
            # Select the clicked cell
            self.cells[int(y)][int(x)].selected = True
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

    def save_initial_state(self):
        # Save the initial state of the board
        self.initial_state = [[cell.value for cell in row] for row in self.cells]

    def reset_to_original(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].value = self.initial_board[i][j]
                self.cells[i][j].sketched_value = 0

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
    
    def select(self, row, col):
        # Unselect the currently selected cell
        if self.selected_cell is not None:
            self.cells[self.selected_cell[0]][self.selected_cell[1]].selected = False
        self.selected_cell = (row, col)
        self.cells[row][col].selected = True

    def move_selection(self, d_row, d_col):
        if self.selected_cell is not None:
            row, col = self.selected_cell
            self.select((row + d_row) % 9, (col + d_col) % 9)

    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].value == 0 or not self.is_valid(row, col, self.cells[row][col].value):
                    return False
        return True
    
    def is_valid(self, row, col, num):
        # Check row
        for i in range(9):
            if self.cells[row][i].value == num and col != i:
                return False

        # Check column
        for i in range(9):
            if self.cells[i][col].value == num and row != i:
                return False

        # Check box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.cells[i][j].value == num and (i, j) != (row, col):
                    return False

        return True
    
    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(0)