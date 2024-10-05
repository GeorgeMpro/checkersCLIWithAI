import re

from board_display import BoardDisplay
from board_state import BoardState
from cell import Cell
from exceptions.cell_not_found_error import CellNotFoundError
from piece_manager import PieceManager
from utils import increment_index, get_cell_row_from_name
from board_initial_state import BoardInitialState
from move_validator import MoveValidator


class Board:
    _rows = _columns = 8

    def __init__(self, rows=_rows, columns=_columns):
        """"
    Represents the game board for a checkers game.

    Attributes:
        rows (int): The number of rows on the board.
        columns (int): The number of columns on the board.
        board (list[list[Cell]]): A 2D list representing the cells on the board.
        cell_map (dict): A dictionary mapping cell names to Cell objects for quick lookup.

                The Cell names follow 8*8 matrix convention display a_ij, i,j=1,...,8
                 the +1 to start the values from 1 and not 0
                 [f"a{y + 1}{x + 1}" for x in range(rows)]
                """
        self.rows = rows
        self.columns = columns
        self.board = [
            [Cell(increment_index(y), increment_index(x)) for x in range(rows)]
            for y in range(columns)]
        # generate a dictionary for O(1) access
        self.cell_map = {cell.name: cell for row in self.board for cell in row}
        self.manager = PieceManager()
        self.validator = MoveValidator()

    def __str__(self):
        # board_state = self.get_board_state()
        # display = BoardDisplay(board_state=board_state)
        # return display.construct_printable_board()
        return BoardDisplay(self.get_board_state()).construct_printable_board()

    def get_cell(self, row, column):
        return self.board[row][column]

    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.rows * self.columns

    def get_column_size(self):
        return self.columns

    def get_row_size(self):
        return self.rows

    def set_up_piece(self, row, column, piece):
        cell = self.get_cell(row, column)
        cell.set_piece(piece)

    def get_cell_by_name(self, name):
        # check that cell name is of the form:
        # a_ij, i,j=1,...,8  (using an 8*8 board)
        match = re.match(r'^a([1-8])([1-8])$', name)

        if (not match) or (name not in self.cell_map):
            raise CellNotFoundError(f"Cell {name} not found")

        return self.cell_map[name]

    def get_board_state(self) -> BoardState:
        return BoardState(cells=self.board)

    def initial_setup(self):
        initial_board_state = BoardInitialState(
            board=self,
            rows=self.rows,
            columns=self.columns
        )

        self.manager.initial_piece_setup(initial_board_state)

    def move_piece(self, source_name, target_name):
        source_cell = self.get_cell_by_name(source_name)
        target_cell = self.get_cell_by_name(target_name)

        self.validator.is_not_same_cell(source_cell, target_cell)
        if self.is_valid_move_direction(source_cell, target_cell):
            self.manager.move_piece_to_cell(source_cell, target_cell)

    def is_valid_move_direction(self, source_cell, target_cell):
        source_row = get_cell_row_from_name(source_cell)
        target_row = get_cell_row_from_name(target_cell)

        return self.validator.is_valid_move_direction(source_cell, source_row, target_row)
