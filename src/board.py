import re

from board_display import BoardDisplay
from board_initial_configuration_dto import BoardInitialConfigurationDTO
from board_state import BoardState
from cell import Cell
from exceptions.cell_not_found_error import CellNotFoundError
from piece_manager import PieceManager
from utils import increment_index, is_valid_cell_name
from move_handler import MoveHandler


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
        self.handler = MoveHandler()

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
        match = is_valid_cell_name(name)

        if (not match) or (name not in self.cell_map):
            raise CellNotFoundError(f"Cell {name} not found")

        return self.cell_map[name]

    def get_board_state(self) -> BoardState:
        return BoardState(cells=self.board)

    def initial_setup(self):
        initial_board_state = BoardInitialConfigurationDTO(
            board=self,
            rows=self.rows,
            columns=self.columns
        )

        self.manager.initial_piece_setup(initial_board_state)

    # todo extract to new class or simplify
    def move_piece(self, source_name, target_name):
        source_cell = self.get_cell_by_name(source_name)
        target_cell = self.get_cell_by_name(target_name)

        self.handler.validate_move(source_cell, target_cell)

        if self.handler.can_capture_piece(source_cell, target_cell):
            self.capture_piece(source_cell, target_cell)
        else:
            self.manager.move_piece_to_cell(source_cell, target_cell)

    def capture_piece(self, source_cell, target_cell):
        cell_dest_name = self.handler.get_destination_for_capture(source_cell, target_cell)
        self.handler.is_cell_after_capture_out_of_bounds(cell_dest_name)
        dest_cell = self.get_cell_by_name(cell_dest_name)
        self.handler.is_cell_available_for_capturing_piece_destination(dest_cell.get_piece())

        self.handler.attempt_capture(source_cell, target_cell, dest_cell)
