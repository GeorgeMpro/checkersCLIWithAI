from board_display import BoardDisplay
from board_initial_configuration_dto import BoardInitialConfigurationDTO
from board_state import BoardState
from cell import Cell
from cell_manager import CellManager, logger
from game import Game, P
from move_manager import get_destination_cell_name_after_capture, can_capture_piece, \
    mange_chained_move, format_available_moves
from move_state import MoveState
from piece import Piece
from piece_manager import PieceManager
from utils import extract_index_from_cell


class Board:
    _rows = _columns = 8

    def __init__(self, rows=_rows, columns=_columns):
        """"
    Represents the game board for a checkers game.

    Attributes:
        columns (int): The number of columns on the board.


                """
        # todo delete
        self.rows = rows
        self.columns = columns
        # self.board = [
        #     [Cell(increment_index(y), increment_index(x)) for x in range(rows)]
        #     for y in range(columns)]
        # generate a dictionary for O(1) access
        # self.cell_map = {cell.name: cell for row in self.board for cell in row}
        self.cell_manager = CellManager(rows, columns)
        self.piece_manager = PieceManager()
        self.game = Game()

    def __str__(self) -> str:
        """
        Generate a string representation of the current board state.
        """
        return BoardDisplay(self.get_board_state()).construct_printable_board()

    def get_board(self) -> list[list[Cell]]:
        return self.cell_manager.board

    def get_board_size(self) -> int:
        return self.rows * self.columns

    def get_column_size(self) -> int:
        return self.columns

    def get_row_size(self) -> int:
        return self.rows

    def set_up_piece(
            self, row: int, column: int, piece: Piece
    ) -> None:
        """
        Place piece on the cell provided by its indexes.
        """
        cell = self.cell_manager.get_cell_by_index(row, column)
        cell.set_piece(piece)

    def get_board_state(self) -> BoardState:
        return BoardState(cells=self.get_board())

    def initial_setup(self) -> None:
        """
        Generate an initial board setup with 3 rows of playable pieces for each player on opposite sides.
        """
        initial_board_state = BoardInitialConfigurationDTO(
            board=self.get_board(),
            rows=self.rows,
            columns=self.columns,
            game=self.game
        )

        self.piece_manager.initial_piece_setup(initial_board_state)

    def move_piece(
            self, source_name: str, target_name: str
    ) -> None:
        """
        Move piece from source cell to target cell.
        Handles normal, capture, and chain captures moves.
        """
        has_chain_capture = False
        # validate that the move does not violate chain rules
        mange_chained_move(
            self.game.is_chained(), source_name, self.game.get_chaining_cell()
        )

        source_cell, target_cell = self.cell_manager.validate_cell_move_logic(source_name, target_name)

        has_chain_capture, final_name = self.handle_move(has_chain_capture, source_cell, target_cell)

        # update if turned to king
        self.check_king_promotion(final_name)
        # update chain capture
        self.update_game_state(has_chain_capture)

    def handle_move(
            self, has_chain_capture: bool, source_cell: Cell, target_cell: Cell
    ) -> tuple[bool, str]:
        """
        Handle the movement of a piece from the source cell to the target cell.

        This method determines whether the move is a capture or a regular move,
        performs the necessary actions, and updates the chain capture status if needed.
        It returns the updated chain capture flag and the final destination cell name.

        Returns:
            tuple[bool, str]: A tuple containing the updated chain capture status and the name of the final destination cell.
        """
        self.cell_manager.validate_capture_logic(source_cell, target_cell)

        if can_capture_piece(source_cell, target_cell):
            has_chain_capture, end_loc = self._handle_capture(source_cell, target_cell)
        else:
            end_loc = self._handle_regular_move(source_cell, target_cell)

        return has_chain_capture, end_loc

    def _handle_capture(
            self, source_cell: Cell, target_cell: Cell
    ) -> tuple[bool, str]:
        """
        Performs a capture move, updating the chain capture state.

        Returns:
           tuple[bool, str]: Chain capture status and final destination cell name.
        """
        end_loc = self.capture_piece(source_cell, target_cell)
        # Update chain capture flag
        has_chain_capture = self.cell_manager.handle_chain_capture(end_loc)
        self.manage_chaining_cell(end_loc, has_chain_capture)
        return has_chain_capture, end_loc

    def _handle_regular_move(
            self, source_cell: Cell, target_cell: Cell
    ) -> str:
        """
        Performs a regular move to the target cell.

        Returns:
            str: The final destination cell name.
        """
        self.piece_manager.move_piece_to_cell(source_cell, target_cell)
        return target_cell.name

    # todo check errors?
    def check_king_promotion(self, target: str) -> None:
        """
        Promote a piece to king if it reaches the last row for its player.
        """
        promotion = {
            P.P1.name: 8,
            P.P2.name: 1
        }
        final_row = int(target[1])
        tar = self.cell_manager.get_cell_by_name(target)
        player = tar.get_piece_owner()
        if final_row == promotion.get(player):
            tar.set_king()

    def manage_chaining_cell(
            self, final_dest_name: str, has_chain_capture: bool
    ) -> None:
        """
        Update the game state if there is a piece that is in chain capture.
        """
        if has_chain_capture:
            self.game.set_chaining_cell(final_dest_name)
        else:
            self.game.remove_chaining_cell()

    def update_game_state(self, has_chain_capture) -> None:
        """
        Updates game state.
        """
        self.game.set_chained_move(has_chain_capture)
        self.game.toggle_whose_turn()

    def capture_piece(self, source_cell: Cell, target_cell: Cell) -> str:
        cell_dest_name = get_destination_cell_name_after_capture(source_cell, target_cell)

        self.cell_manager.begin_capture_attempt(cell_dest_name, source_cell, target_cell)

        return cell_dest_name

    def get_current_turn(self) -> str:
        return self.game.get_turn()

    def get_available_moves(self):
        player = self.game.get_turn()

        return self.cell_manager.generate_available_moves_for_player(player)

    @staticmethod
    def get_user_moves_prompt(moves: list[MoveState]) -> str:
        return format_available_moves(moves)
