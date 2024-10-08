from typing import List, Optional

from cell import Cell
from exceptions.cell_not_found_error import CellNotFoundError
from exceptions.illegal_move_error import IllegalMoveError
from game import Player as P
from move_state import MoveState, CaptureMove
from piece import Piece
from utils import extract_index_from_cell, get_cell_row_from_name, is_valid_cell_name, captures, generate_move


class MoveHandler:
    def __init__(self):
        pass

    @staticmethod
    def validate_move(source_cell: Cell, target_cell: Cell):
        MoveHandler.is_not_same_cell(source_cell, target_cell)
        MoveHandler.is_valid_distance(source_cell, target_cell)
        MoveHandler.is_not_same_owner(source_cell, target_cell)
        MoveHandler.is_valid_move_direction(source_cell, target_cell)

    @staticmethod
    def is_valid_move_direction(source_cell: Cell, target_cell: Cell):
        source_row = get_cell_row_from_name(source_cell)
        target_row = get_cell_row_from_name(target_cell)
        owner = source_cell.get_piece_owner()
        # p1 cannot move "down"; p2 cannot move "up"
        rules = {
            P.P1.name: lambda source, target: source > target,
            P.P2.name: lambda source, target: source < target,
        }
        # check if players is attempting to move backwards
        if owner in rules and rules[owner](source_row, target_row):
            raise IllegalMoveError("Normal piece cannot move in opposite direction")

    @staticmethod
    def is_not_same_cell(source_cell: Cell, target_cell: Cell):
        if source_cell == target_cell:
            raise IllegalMoveError("Cannot move to the same cell")

    @staticmethod
    def is_valid_distance(source_cell: Cell, target_cell: Cell):
        # a_ij source cell
        i, j = extract_index_from_cell(source_cell)
        # a_kl target cell
        k, l = extract_index_from_cell(target_cell)
        row_distance = i - k
        col_distance = j - l
        if row_distance not in {1, -1} or col_distance not in {1, -1}:
            raise IllegalMoveError("Non capture move is a single cell distance.")

    @staticmethod
    def is_not_same_owner(source_cell: Cell, target_cell: Cell):
        source_owner = source_cell.get_piece_owner()
        target_owner = target_cell.get_piece_owner()
        if source_owner == target_owner:
            raise IllegalMoveError("Cannot capture same owner")

    @staticmethod
    def can_capture_piece(source_cell: Cell, target_cell: Cell) -> bool:
        source_owner = source_cell.get_piece_owner()
        target_owner = target_cell.get_piece_owner()

        if source_owner is None or target_owner is None:
            return False

        return source_owner != target_owner

    @staticmethod
    def get_destination_cell_name_after_capture(source_cell: Cell, target_cell: Cell) -> str:
        row_src, col_src = extract_index_from_cell(source_cell)
        row_trg, col_trg = extract_index_from_cell(target_cell)

        # determine should the piece go "down" or "up" by player
        row_dest = MoveHandler.get_row_direction_for_capture(source_cell, row_trg)
        col_dest = col_trg + 1 if col_trg > col_src else col_trg - 1

        return f"a{row_dest}{col_dest}"

    @staticmethod
    def get_row_direction_for_capture(source_cell: Cell, target_row: int) -> int:
        row_direction_by_player = {
            P.P1.name: lambda row: row + 1,
            P.P2.name: lambda row: row - 1
        }

        # the destination row
        return row_direction_by_player[source_cell.get_piece_owner()](target_row)

    @staticmethod
    def attempt_capture(source_cell: Cell, target_cell: Cell, dest_cell: Cell):
        piece_to_move = source_cell.get_piece()

        dest_cell.set_piece(piece_to_move)

        #  clean source and target cells from pieces
        source_cell.remove_piece()
        target_cell.remove_piece()

    @staticmethod
    def validate_capture_move(cell: Cell, cell_piece: Piece):
        MoveHandler.is_cell_available_for_capturing_piece_destination(cell_piece)
        MoveHandler.is_cell_destination_after_capture_out_of_bounds(cell.name)

    @staticmethod
    def is_cell_available_for_capturing_piece_destination(cell_piece: Piece):
        if cell_piece is not None:
            raise IllegalMoveError("Cannot capture if destination cell is blocked")

    @staticmethod
    def is_cell_destination_after_capture_out_of_bounds(cell_name: str):
        if not is_valid_cell_name(cell_name):
            raise CellNotFoundError("Cannot capture if after target cell out of bounds")

    @staticmethod
    def manage_adding_moves_property_to_given_cells(cells):
        valid_moves = []
        for cell_src, cell_target in cells:
            name_src = cell_src.name
            name_target = cell_target.name
            MoveHandler.add_moves_property(cell_src, cell_target, name_src, name_target, valid_moves)

        return valid_moves

    @staticmethod
    def add_moves_property(cell_src: Cell, cell_target: Cell, name_src: str, name_target: str,
                           valid_moves: List[MoveState]) -> None:
        """Adds possible moves for the given piece in the given cell."""

        # Check if this is a capture move
        if MoveHandler.can_capture_piece(cell_src, cell_target):
            name_dest = MoveHandler.get_destination_cell_name_after_capture(cell_src, cell_target)
            capture_move = captures(name_target, name_dest)
            MoveHandler.manage_moves(name_src, name_target, valid_moves, capture_move)
        else:
            # Normal move, no capture
            MoveHandler.manage_moves(name_src, name_target, valid_moves)

    @staticmethod
    def manage_moves(name_src: str, name_target: str, valid_moves: List[MoveState],
                     capture_move: Optional[CaptureMove] = None) -> None:
        """Find or create a move for a given source and target."""

        # Try to find an existing move
        move = MoveHandler.find_move_state(name_src, valid_moves)
        if move:
            MoveHandler.update_move(move, name_target, capture_move)
        else:
            MoveHandler.create_move(name_src, name_target, valid_moves, capture_move)

    @staticmethod
    def find_move_state(name_src: str, valid_moves: List[MoveState]) -> Optional[MoveState]:
        """Find an existing move with the given source name."""
        for move in valid_moves:
            if move.src_name == name_src:
                return move
        return None

    @staticmethod
    def update_move(move: MoveState, name_target: str, capture_move: Optional[CaptureMove] = None) -> None:
        """Update the existing move with a new target and capture move."""
        move.target_names.append(name_target)  # Add the target name
        if capture_move:
            move.capture_moves.append(capture_move)  # Add the capture move if it exists

    @staticmethod
    def create_move(name_src: str, name_target: str, valid_moves: List[MoveState],
                    capture_move: Optional[CaptureMove] = None) -> None:
        """Create a new move and add it to the valid moves list."""
        if capture_move:
            new_move = generate_move(name_src, [name_target], True, [capture_move])
        else:
            new_move = generate_move(name_src, [name_target])

        valid_moves.append(new_move)

    # todo?
    @staticmethod
    def has_capture_moves(cells: list[Cell]) -> bool:
        return any(MoveHandler.can_capture_piece(move.src, move.target) for move in cells)

    @staticmethod
    def handle_mandatory_capture(cells: list[tuple[Cell, Cell]]) -> list[tuple[Cell, Cell]]:
        """
        Capture moves are mandatory by the game rules.
        If there are normal moves and capture moves - the normal moves are not added to the list
        """
        capture_moves = [(src, target) for src, target in cells if MoveHandler.can_capture_piece(src, target)]

        return capture_moves if capture_moves else cells  # Return capture moves or all moves if no captures
