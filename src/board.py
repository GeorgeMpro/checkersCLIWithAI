from typing import Any, List

from board_display import BoardDisplay
from board_initial_configuration_dto import BoardInitialConfigurationDTO
from board_state import BoardState
from cell import Cell
from exceptions.cell_not_found_error import CellNotFoundError
from exceptions.illegal_move_error import IllegalMoveError
from game import Game
from game import Player as P
from move_handler import MoveHandler
from piece import Piece
from piece_manager import PieceManager
from utils import increment_index, is_valid_cell_name, extract_index_from_cell, get_potential_moves


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
        self.game = Game()

    def __str__(self) -> str:
        """
        Generate a string representation of the current board state.
        """
        return BoardDisplay(self.get_board_state()).construct_printable_board()

    def get_cell(self, row: int, column: int) -> Cell:
        return self.board[row][column]

    def get_cell_by_name(self, name: str) -> Cell:
        # check that cell name is of the form:
        # a_ij, i,j=1,...,8  (using an 8*8 board)
        match = is_valid_cell_name(name)

        if (not match) or (name not in self.cell_map):
            raise CellNotFoundError(f"Cell {name} not found")

        return self.cell_map[name]

    def get_board(self) -> list[list[Cell]]:
        return self.board

    def get_board_size(self) -> int:
        return self.rows * self.columns

    def get_column_size(self) -> int:
        return self.columns

    def get_row_size(self) -> int:
        return self.rows

    def set_up_piece(self, row: int, column: int, piece: Piece):
        cell = self.get_cell(row, column)
        cell.set_piece(piece)

    def get_board_state(self) -> BoardState:
        return BoardState(cells=self.board)

    def initial_setup(self) -> None:
        """
        Generate an initial board setup with 3 rows of playable pieces for each player on opposite sides.
        """
        initial_board_state = BoardInitialConfigurationDTO(
            board=self,
            rows=self.rows,
            columns=self.columns,
            game=self.game
        )

        self.manager.initial_piece_setup(initial_board_state)

    def move_piece(self, source_name: str, target_name: str) -> None:
        # validating general logic
        source_cell = self.get_cell_by_name(source_name)
        target_cell = self.get_cell_by_name(target_name)
        self.handler.validate_move(source_cell, target_cell)

        # validating gameplay logic
        # todo
        #   go over available moves
        #   if has capture move and does normal raise erro
        #   flag?
        # Get valid moves and filter capture moves
        move_list = self.get_valid_moves_for_given_cell(source_cell)
        move_dto = move_list[0]
        print(f"\n{move_list}")

        print(f"\nmove dto:{move_dto}")
        print(f"\ncapture moves:{move_dto.capture_moves}")

        # Raise error if there are capture moves but a normal move is attempted
        dest_cell_name = self.handler.get_destination_cell_name_after_capture(source_cell, target_cell)
        # if move_dto.is_capture_move and all(
        #         capture_move.name_target_cell != source_cell.name and capture_move.name_final_cell != dest_cell_name
        #         for capture_move in move_dto.capture_moves
        # ):
        #     raise IllegalMoveError("Cannot make a normal move when capture is available")
        if move_dto.is_capture_move:
            move_tuple = (target_cell.name, dest_cell_name)

            # Ensure there are capture moves and the current move matches one of the valid capture moves
            if not move_dto.capture_moves or not any(
                    (capture_move.name_target_cell, capture_move.name_final_cell) == move_tuple
                    for capture_move in move_dto.capture_moves
            ):
                raise IllegalMoveError("Cannot make a normal move when capture is available")

        # todo
        #   change to use has capture?
        if self.handler.can_capture_piece(source_cell, target_cell):
            self.capture_piece(source_cell, target_cell)
        else:
            self.manager.move_piece_to_cell(source_cell, target_cell)

        # update_turn
        self.game.toggle_whose_turn()

    def capture_piece(self, source_cell: Cell, target_cell: Cell) -> None:
        cell_dest_name = self.handler.get_destination_cell_name_after_capture(source_cell, target_cell)

        self.begin_capture_attempt(cell_dest_name, source_cell, target_cell)

    def begin_capture_attempt(self, cell_dest_name: str, source_cell: Cell, target_cell: Cell):
        # Validate cell is on board
        self.handler.is_cell_destination_after_capture_out_of_bounds(cell_dest_name)
        dest_cell = self.get_cell_by_name(cell_dest_name)
        self.handler.is_cell_available_for_capturing_piece_destination(dest_cell.get_piece())

        # execute capture
        self.handler.attempt_capture(source_cell, target_cell, dest_cell)

    def get_valid_moves_for_given_cell(self, cell: Cell) -> list[Any]:
        """
        Get valid moves for the piece on given cell under the game rules.
        """
        owner = cell.get_piece_owner()
        row_source, col_src = extract_index_from_cell(cell)

        # p1 goes up, p2 goes "down"
        row_target = increment_index(row_source) if owner == P.P1.name else row_source - 1
        possible_moves = get_potential_moves(col_src, row_target)

        return self.handle_adding_valid_moves(cell.name, possible_moves)

    def handle_adding_valid_moves(self, name_src: str, possible_moves: List[tuple[int, int]]) -> list[Any]:
        # the filtered cell list to be added
        cells = self.handler.handle_mandatory_capture(self.get_valid_cells(name_src, possible_moves))

        return self.handler.manage_adding_moves_property_to_given_cells(cells)

    def get_valid_cells(self, name_src: str, possible_moves: List[tuple[int, int]]) -> list[tuple[Cell, Cell]]:
        """
        Generate a list of moves which are in the board's boundaries.
        """
        cells = []
        for row, col in possible_moves:
            name_target = f"a{row}{col}"
            try:
                cells.append(self.validate_cell_source_and_target_names(name_src, name_target))
            except(IllegalMoveError, CellNotFoundError):
                continue
        return cells

    def validate_cell_source_and_target_names(self, name_src: str, name_target: str) -> tuple[Cell, Cell]:
        """
        Check the source and target cells are not out of bounds.
        """
        cell_src = self.get_cell_by_name(name_src)
        cell_target = self.get_cell_by_name(name_target)
        return cell_src, cell_target

    def get_current_turn(self) -> str:

        return self.game.get_turn()
