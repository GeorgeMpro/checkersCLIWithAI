from component.cell import Cell
from component.game import Game, P
from component.piece import Piece
from display.board_display import BoardDisplay
from managers.cell_manager import CellManager
from managers.move_handle_util import get_destination_cell_name_after_capture
from managers.move_manager import \
    mange_chained_move, format_available_moves
from managers.move_validator_util import can_capture_piece
from managers.piece_manager import PieceManager
from state.board_initial_configuration_dto import BoardInitialConfigurationDTO
from state.board_state import BoardState
from state.move_state import MoveState


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
            self.game.is_chained_move, source_name, self.game.chaining_cell_name
        )

        source_cell, target_cell = self.cell_manager.validate_cell_move_logic(source_name, target_name)

        has_chain_capture, final_name = self.handle_move(has_chain_capture, source_cell, target_cell)

        # update if turned to king
        self.check_king_promotion(final_name)
        # update chain capture
        self.update_game_state(has_chain_capture, final_name)

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
            self.game.chaining_cell_name = final_dest_name
        else:
            del self.game.chaining_cell_name

    def update_game_state(self, has_chain_capture: bool, final_name: str) -> None:
        """
        Updates game state.
        """
        self.game.is_chained_move = has_chain_capture
        if has_chain_capture:
            self.game.chaining_cell_name = final_name
        else:
            del self.game.chaining_cell_name

        self.game.toggle_player_turn()

    def capture_piece(self, source_cell: Cell, target_cell: Cell) -> str:
        cell_dest_name = get_destination_cell_name_after_capture(source_cell, target_cell)

        self.cell_manager.begin_capture_attempt(cell_dest_name, source_cell, target_cell)

        return cell_dest_name

    def get_current_player_turn(self) -> str:
        return self.game.current_player.name

    def get_available_moves(self, player: str = None) -> list[MoveState]:
        if player is None:
            player = self.game.current_player.name

        chained_name = self.game.chaining_cell_name

        return self.cell_manager.generate_available_moves_for_player(player, chained_name)

    @staticmethod
    def get_user_moves_prompt(moves: list[MoveState]) -> str:
        """
        Return a prompt to be displayed to the user with available moves and how to access them.
        """
        return format_available_moves(moves)

    def is_game_end(
            self, moves: list[MoveState], opponent_pieces: list[Piece]
    ) -> bool:
        """
        Check whether the game has reached an end and who is the winner.
        """
        # handle no more moves
        if not moves:
            self._handle_game_end_no_more_moves()
            return True

        # handle no more opponent pieces
        if not opponent_pieces:
            self.game.winner = self.game.current_player
            return True

        return False

    def _handle_game_end_no_more_moves(self):
        """
        When opponent has no more moves you win.
        """
        # set winner
        turn = self.get_current_player_turn()
        winner = P.P2 if turn == "p1" else P.P1
        self.game.winner = winner
        # set game has ended
        self.set_game_over()

    def is_game_over(self) -> bool:
        """
        Check if game reached its end.
        """

        return self.game.is_game_over

    def set_game_over(self) -> None:
        """
        Update to game end.
        """
        self.game.is_game_over = True
