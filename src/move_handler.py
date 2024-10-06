from cell import Cell
from exceptions.cell_not_found_error import CellNotFoundError
from piece import Piece
from utils import extract_index_from_cell, get_cell_row_from_name, is_valid_cell_name
from exceptions.illegal_move_error import IllegalMoveError


class MoveHandler:
    def __init__(self):
        pass

    @staticmethod
    def validate_move(source_cell, target_cell):
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
            "p1": lambda source, target: source > target,
            "p2": lambda source, target: source < target,
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
        if target_owner is None:
            return
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
    def get_destination_for_capture(source_cell: Cell, target_cell: Cell) -> str:
        row_src, col_src = extract_index_from_cell(source_cell)
        row_trg, col_trg = extract_index_from_cell(target_cell)

        # determine should the piece go "down" or "up" by player
        row_dest = MoveHandler.get_row_direction_for_capture(source_cell, row_trg)
        col_dest = col_trg + 1 if col_trg > col_src else col_trg - 1

        return f"a{row_dest}{col_dest}"

    @staticmethod
    def get_row_direction_for_capture(source_cell: Cell, target_row: int) -> int:
        row_direction_by_player = {
            "p1": lambda row: row + 1,
            "p2": lambda row: row - 1
        }

        # the destination row
        return row_direction_by_player[source_cell.get_piece_owner()](target_row)

    @staticmethod
    def attempt_capture(source_cell, target_cell, dest_cell):
        piece_to_move = source_cell.get_piece()

        # check where the capturing cell should go
        # todo check valid destination?
        dest_cell.set_piece(piece_to_move)

        #  clean source and target cells from pieces
        source_cell.remove_piece()
        target_cell.remove_piece()

    @staticmethod
    def validate_capture_move(cell: Cell, cell_piece: Piece):
        MoveHandler.is_cell_available_for_capturing_piece_destination(cell_piece)
        MoveHandler.is_cell_after_capture_out_of_bounds(cell)

    @staticmethod
    def is_cell_available_for_capturing_piece_destination(cell_piece: Piece):
        if cell_piece is not None:
            raise IllegalMoveError("Cannot capture if destination cell is blocked")

    @staticmethod
    def is_cell_after_capture_out_of_bounds(cell_name):
        if not is_valid_cell_name(cell_name):
            raise CellNotFoundError("Cannot capture if after target cell out of bounds")
