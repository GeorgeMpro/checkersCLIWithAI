from copy import deepcopy
from typing import List

from component.cell import Cell
from exceptions.cell_not_found_error import CellNotFoundError
from exceptions.illegal_move_error import IllegalMoveError
from managers.move_handle_util import get_destination_cell_name_after_capture
from managers.move_manager import validate_move, enforce_mandatory_capture, \
    validate_capture_final_destination_is_in_bounds, validate_capture_final_destination_is_available, \
    handle_mandatory_capture, manage_adding_moves_property_to_given_cells, validate_capture_move, generate_normal_moves, \
    generate_king_moves, filter_invalid_moves
from state.move_state import MoveState
from utils import index_offset, is_valid_cell_name, extract_index_from_cell, get_logger

logger = get_logger(name='cell_manager')


class CellManager:

    def __init__(self, rows, columns):
        """
        Initializes the board with specified rows and columns.

        Cell map contains only playable cells to reduce memory usage.
        """
        self.rows = rows
        self.columns = columns
        # The Cell names follow 8*8 matrix convention display a_ij, i,j=1,...,8
        #                  the +1 to start the values from 1 and not 0
        #                  [f"a{y + 1}{x + 1}" for x in range(rows)]
        self.board = [
            [Cell(index_offset(y), index_offset(x))
             for x in range(rows)]
            for y in range(columns)]

        # dictionary for O(1) access
        self.cell_map = {
            cell.name: cell
            for row in self.board
            for cell in row
            if cell.playable
        }

    def get_board(self):
        return self.board

    def get_cell_by_index(self, row: int, column: int) -> Cell:
        """
        Get cell by the i,j from its string name "a_ij".
        E.g. "a12" turns into i=1, j=2.
        """
        return self.board[row][column]

    def get_cell_map(self) -> dict[str, Cell]:
        return self.cell_map

    # todo
    def get_cell_map_copy(self) -> dict[str, Cell]:
        return deepcopy(self.cell_map)

    def get_cell_by_name(self, name: str) -> Cell | None:
        """
        Get a cell by its a_ij name.
        """
        # todo: optional: handle logging error?
        self._validate_cell_name(name)
        return self.cell_map[name]

    def _validate_cell_name(self, name: str) -> None:
        """
        Check that cell name is of the form: a_ij, i,j=1,...,8  (using an 8*8 board)
        E.g. a13 is on board, a03 is not.
        """
        match = is_valid_cell_name(name)
        if (not match) or (name not in self.cell_map):
            raise CellNotFoundError(f"Cell {name} not found.")

    def validate_cell_move_logic(
            self, source_name: str, target_name: str
    ) -> tuple[Cell, Cell]:
        source_cell = self.get_cell_by_name(source_name)
        target_cell = self.get_cell_by_name(target_name)
        validate_move(source_cell, target_cell)

        return source_cell, target_cell

    # todo
    def validate_capture_logic(self, source_cell: Cell, target_cell: Cell) -> None:
        move_list = self._get_valid_move_directions_for_cell(source_cell)
        move_dto = move_list[0]
        has_capture_moves = move_dto.is_capture_move
        # Raise error if there are capture moves but a normal move is attempted
        dest_cell_name = get_destination_cell_name_after_capture(source_cell, target_cell)
        enforce_mandatory_capture(dest_cell_name, has_capture_moves, move_dto, target_cell)

    def begin_capture_attempt(self, cell_dest_name: str, source_cell: Cell, target_cell: Cell):
        # Validate cell is on board
        validate_capture_final_destination_is_in_bounds(cell_dest_name)
        dest_cell = self.get_cell_by_name(cell_dest_name)
        validate_capture_final_destination_is_available(dest_cell.get_piece())

        # execute capture
        self.execute_capture(source_cell, target_cell, dest_cell)

    # todo, move?
    @staticmethod
    def execute_capture(source_cell: Cell, target_cell: Cell, dest_cell: Cell
                        ) -> None:
        """
        Execute capture move.
        """
        piece_to_move = source_cell.get_piece()

        dest_cell.set_piece(piece_to_move)

        #  clean source and target cells from pieces
        source_cell.remove_piece()
        target_cell.remove_piece()

    def _get_valid_move_directions_for_cell(self, cell: Cell) -> list[MoveState]:

        """
        Get valid moves for the piece on given cell under the game rules.
        """
        owner = cell.get_piece_owner()
        row_source, col_src = extract_index_from_cell(cell)
        is_king = cell.is_king()

        if is_king:
            possible_moves = generate_king_moves(col_src, row_source)
        else:
            # p1 goes up, p2 goes "down"
            possible_moves = generate_normal_moves(col_src, owner, row_source)

        return self.handle_adding_valid_moves(cell.name, possible_moves)

    def handle_adding_valid_moves(
            self, name_src: str, possible_moves: List[tuple[int, int]]
    ) -> list[MoveState]:
        """
        Filter and return valid moves.
        """

        # the filtered cell list to be added
        cells = handle_mandatory_capture(
            self._get_valid_cells(name_src, possible_moves),
            self.get_cell_map()
        )
        filtered_moves = filter_invalid_moves(cells)

        return manage_adding_moves_property_to_given_cells(filtered_moves)

    def _get_valid_cells(
            self, name_src: str, possible_moves: List[tuple[int, int]]
    ) -> list[tuple[Cell, Cell]]:
        """
        Generate a list of moves which are in the board's boundaries.
        """
        cells = []
        for row, col in possible_moves:
            name_target = f"a{row}{col}"
            try:
                cell_pair = self.validate_cell_source_and_target_names(name_src, name_target)
                if cell_pair[0] is not None and cell_pair[1]:
                    cells.append(cell_pair)
            except(IllegalMoveError, CellNotFoundError) as e:
                # todo
                # Optional, suppressed logging
                #  logger.error(f"Invalid move: {e}")
                continue
        return cells

    def validate_cell_source_and_target_names(self, name_src: str, name_target: str) -> tuple[Cell, Cell]:
        """
        Check the source and target cells are not out of bounds.
        """
        cell_src = self.get_cell_by_name(name_src)
        cell_target = self.get_cell_by_name(name_target)
        return cell_src, cell_target

    def handle_chain_capture(self, final_dest_name: str) -> bool:
        """
        Check whether a capture move will lead to more captures.
        """
        cell_final_dest = self.get_cell_by_name(final_dest_name)
        chain_moves = self._get_valid_move_directions_for_cell(cell_final_dest)
        has_valid_chain_capture = False
        for move in chain_moves:
            # Check if any move is a valid chain capture
            has_valid_chain_capture = self.check_chain_possible_moves(move) or has_valid_chain_capture

        return has_valid_chain_capture

    # todo clean
    def check_chain_possible_moves(self, move: MoveState) -> bool:

        has_valid_chain_capture = False
        for target in move.target_names:
            target_cell = self.get_cell_by_name(target)

            try:
                has_valid_chain_capture = self.validate_chain(move, target_cell)

                break
            # todo optional error message?
            except IllegalMoveError as e:
                # logger.error(f"Invalid move: {e}")
                continue
            except CellNotFoundError as e:
                # logger.error(f"Invalid move: {e}")
                continue

        return has_valid_chain_capture

    def validate_chain(self, move: MoveState, target_cell: Cell) -> bool:
        # Get the final destination cell after capture
        destination_cell_name = get_destination_cell_name_after_capture(
            self.get_cell_by_name(move.src_name), target_cell
        )

        destination_cell = self.get_cell_by_name(destination_cell_name)

        # Validate the final destination (not the target) for capture
        destination_piece = destination_cell.get_piece()
        validate_capture_move(destination_cell, destination_piece)

        # After finding a valid capture, break the loop
        return move.is_capture()

    # todo
    #   check if chain, if chain remove all
    #   maybe pass if chain from game > board > cell man?
    def generate_available_moves_for_player(
            self, player: str, chained_name: str | None
    ) -> list[MoveState]:
        """
        Generate moves for the player whose turn is to play.
        """
        cells = self.get_player_cells(player)

        return self._generate_player_move_states(cells, chained_name)

    def get_player_cells(
            self, player: str
    ) -> list[Cell]:
        """
        Get all cells owned by the given player
        """
        player_cells = [
            cell for cell in self.get_cell_map().values()
            if cell.get_piece_owner() == player
        ]

        return player_cells

    # todo consider moving to a utility class for heuristic explorer
    @staticmethod
    def get_player_cells_from_copy(
            cell_map: dict[str, Cell], player: str
    ) -> list[Cell]:
        """
        Get all cells owned by the given player.
        """
        player_cells = [
            cell for cell in cell_map.values()
            if cell.get_piece_owner() == player
        ]

        return player_cells

    def _generate_player_move_states(
            self, player_cells: List[Cell], chained_name: str | None
    ) -> List[MoveState]:
        """
        Generate move states for each of the player's pieces.
        """
        # todo
        #   check for chained moved and leave all else?
        if chained_name:
            return self.get_chained_cell_moves(chained_name)

        # First Pass:
        has_capture_moves = self._check_cells_for_capture_moves(player_cells)

        # second pass
        return self._generate_filtered_moves(has_capture_moves, player_cells)

    def get_chained_cell_moves(self, chained_name: str) -> list[MoveState]:
        """
        When executing chained capture only those piece moves are available.
        """
        return self._get_valid_move_directions_for_cell(
            self.get_cell_by_name(chained_name)
        )

    def _check_cells_for_capture_moves(
            self, cells: List[Cell]
    ) -> bool:
        """
        Check if any of the available moves are capture moves.
        """
        # todo check for final dest in bounds
        return any(
            move.is_capture_move  # condition
            for cell in cells  # outer loop
            for move in self._get_valid_move_directions_for_cell(cell)  # inner loop
        )

    def _generate_filtered_moves(self, has_capture_moves: bool, player_cells: list[Cell]):
        """
        Generate a list of valid moves for the player's pieces, filtered based on capture availability.
        """
        return [
            move  # Add the move to the list if conditions are met
            for cell in player_cells  # Iterate over each player's cell
            for move in self._get_valid_move_directions_for_cell(cell)  # Get valid moves for the cell
            if (has_capture_moves and move.is_capture_move) or not has_capture_moves  # Conditional inclusion
        ]
