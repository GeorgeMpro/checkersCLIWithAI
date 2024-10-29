from component.cell import Cell
from component.game import P
from component.piece import Piece
from exceptions.cell_not_found_error import CellNotFoundError
from exceptions.illegal_move_error import IllegalMoveError
from managers.move_handle_util import get_destination_cell_name_after_capture
from utils import get_cell_row_from_name, extract_index_from_cell, is_valid_cell_name


def generate_filtered_moves(cells: list[tuple[Cell, Cell]]):
    """
    Filters out invalid moves from a list of cell pairs representing potential moves.
    """
    return [
        (cell_src, cell_target) for cell_src, cell_target in cells
        if _is_valid_move(cell_src, cell_target)
    ]


def validate_move_util(
        source_cell: Cell, target_cell: Cell
) -> None:
    """
    Validates the legality and in-game boundaries of a move.
    """
    _is_not_same_cell(source_cell, target_cell)
    _is_valid_distance(source_cell, target_cell)
    _is_not_same_owner(source_cell, target_cell)
    if not source_cell.is_king():
        _is_valid_move_direction(source_cell, target_cell)


def _is_not_same_cell(source_cell: Cell, target_cell: Cell) -> None:
    """
    Cannot move to the came cell you are currently on.
    """
    if source_cell == target_cell:
        raise IllegalMoveError("Cannot move to the same cell")


def _is_valid_distance(source_cell: Cell, target_cell: Cell) -> None:
    """
    Normal moves have a distance of 1 playable cell away.
    """
    # a_ij source cell
    i, j = extract_index_from_cell(source_cell)
    # a_kl target cell
    k, l = extract_index_from_cell(target_cell)
    row_distance = i - k
    col_distance = j - l
    if row_distance not in {1, -1} or col_distance not in {1, -1}:
        raise IllegalMoveError("Non capture move is a single cell distance.")


def _is_not_same_owner(source_cell: Cell, target_cell: Cell) -> None:
    """
    Cannon capture pieces your own pieces.
    """
    source_owner = source_cell.get_piece_owner()
    target_owner = target_cell.get_piece_owner()
    if source_owner == target_owner:
        raise IllegalMoveError("Cannot capture same owner")


def _is_valid_move_direction(source_cell: Cell, target_cell: Cell) -> None:
    """
    Validate the direction in which normal pieces can go on the board.
    """
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


def _is_valid_move(source: Cell, target: Cell) -> bool:
    """
    Utility valid move filter.
    """
    try:
        validate_move_util(source, target)  # Ensure it meets move rules
        return True
    except (IllegalMoveError, CellNotFoundError):
        return False


def validate_capture_final_destination_is_available(
        cell_piece: Piece
) -> None:
    if cell_piece is not None:
        raise IllegalMoveError("Cannot capture if destination cell is blocked")


def validate_capture_final_destination_is_in_bounds(
        cell_name: str
) -> None:
    if not is_valid_cell_name(cell_name):
        raise CellNotFoundError("Cannot capture if after target cell out of bounds")


def _is_valid_capture(src, target, cell_map: dict[str, Cell]) -> bool:
    try:
        name = _filter_capture_move_out_of_bounds(src, target)
        validate_capture_final_destination_is_available(cell_map.get(name).get_piece())
        return True
    except (CellNotFoundError, IllegalMoveError):
        return False


def _filter_capture_move_out_of_bounds(src: Cell, target: Cell) -> str | None:
    """
    Utility function for filtering capture moves that final destination cell is out of bounds.
    """
    final_cell_name = get_destination_cell_name_after_capture(src, target)
    validate_capture_final_destination_is_in_bounds(final_cell_name)
    return final_cell_name


def can_capture_piece(source_cell: Cell, target_cell: Cell) -> bool:
    """
    Check if there is a piece on the cell and whether it is owned by the opponent.
    """
    source_owner = source_cell.get_piece_owner()
    target_owner = target_cell.get_piece_owner()

    if source_owner is None or target_owner is None:
        return False

    return source_owner != target_owner
