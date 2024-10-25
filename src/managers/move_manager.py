from typing import List, Optional

from component.cell import Cell
from component.game import Player as P
from component.piece import Piece
from exceptions.cell_not_found_error import CellNotFoundError
from exceptions.illegal_move_error import IllegalMoveError
from state.move_state import MoveState, CaptureMove
from utils import extract_index_from_cell, get_cell_row_from_name, is_valid_cell_name, captures, generate_move, \
    get_potential_moves, index_offset


def filter_invalid_moves(
        cells: list[tuple[Cell, Cell]]
) -> list[tuple[Cell, Cell]]:
    """
    Filters out invalid moves from a list of cell pairs representing potential moves.

    Args:
        cells (list[tuple[Cell, Cell]]): A list of tuples, where each tuple contains a source cell and a target cell.

    Returns:
        list[tuple[Cell, Cell]]: A list of tuples with only valid moves, excluding any moves that violate game rules
        (e.g., moving to own piece or out of bounds).

    Usage:
        Use this function to clean up a list of possible moves before displaying or applying them in the game.

    Example:
        valid_moves = filter_invalid_moves(possible_moves)
    """
    return [
        (cell_src, cell_target) for cell_src, cell_target in cells
        if _is_valid_move(cell_src, cell_target)
    ]


def validate_move(source_cell: Cell, target_cell: Cell) -> None:
    """
    Validates the legality and in-game boundaries of a move.
    """
    _is_not_same_cell(source_cell, target_cell)
    _is_valid_distance(source_cell, target_cell)
    _is_not_same_owner(source_cell, target_cell)
    if not source_cell.is_king():
        _is_valid_move_direction(source_cell, target_cell)


def _is_valid_move(source: Cell, target: Cell) -> bool:
    """
    Utility valid move filter.
    """
    try:
        validate_move(source, target)  # Ensure it meets move rules
        return True
    except (IllegalMoveError, CellNotFoundError):
        return False


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


def can_capture_piece(source_cell: Cell, target_cell: Cell) -> bool:
    """
    Check if there is a piece on the cell and whether it is owned by the opponent.
    """
    source_owner = source_cell.get_piece_owner()
    target_owner = target_cell.get_piece_owner()

    if source_owner is None or target_owner is None:
        return False

    return source_owner != target_owner


def get_destination_cell_name_after_capture(
        source_cell: Cell, target_cell: Cell
) -> str:
    """
    Utility function for getting the final destination cell name after a capture.

    Handles normal and king movement.
    """
    row_src, col_src = extract_index_from_cell(source_cell)
    row_trg, col_trg = extract_index_from_cell(target_cell)

    row_dest = _get_row_direction_for_capture(source_cell, row_src, row_trg)
    col_dest = col_trg + 1 if col_trg > col_src else col_trg - 1

    return f"a{row_dest}{col_dest}"


def _get_row_direction_for_capture(
        source_cell: Cell, source_row: int, target_row: int
) -> int:
    """
    Get relative direction of the destination cell after capture.
    """
    if source_cell.is_king():
        # For a king, move two steps in the direction of the target
        return target_row + (target_row - source_row)

    row_direction_by_player = {
        P.P1.name: lambda row: row + 1,  # Player 1 moves down
        P.P2.name: lambda row: row - 1  # Player 2 moves up
    }

    # the destination row
    return row_direction_by_player[source_cell.get_piece_owner()](target_row)


def validate_capture_move(final_dest_cell: Cell, final_dest_cell_piece: Piece) -> None:
    """
    Validate capture logic.
    """
    validate_capture_final_destination_is_in_bounds(final_dest_cell.name)
    validate_capture_final_destination_is_available(final_dest_cell_piece)


# todo
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


def manage_adding_moves_property_to_given_cells(
        cells: List[tuple[Cell, Cell]]
) -> List[MoveState]:
    valid_moves = []
    for cell_src, cell_target in cells:
        name_src = cell_src.name
        name_target = cell_target.name
        _add_moves_property(cell_src, cell_target, name_src, name_target, valid_moves)

    return valid_moves


def _add_moves_property(
        cell_src: Cell, cell_target: Cell, name_src: str, name_target: str,
        valid_moves: List[MoveState]
) -> None:
    """Adds possible moves for the given piece in the given cell."""

    # Check if this is a capture move
    if can_capture_piece(cell_src, cell_target):
        name_dest = get_destination_cell_name_after_capture(cell_src, cell_target)
        capture_move = captures(name_target, name_dest)
        _manage_moves(name_src, name_target, valid_moves, capture_move)
    else:
        # Normal move, no capture
        _manage_moves(name_src, name_target, valid_moves)


def _manage_moves(
        name_src: str, name_target: str, valid_moves: List[MoveState],
        capture_move: Optional[CaptureMove] = None
) -> None:
    """Find or create a move for a given source and target."""

    # Try to find an existing move
    move = _find_move_state(name_src, valid_moves)
    if move:
        _update_move(move, name_target, capture_move)
    else:
        _create_move(name_src, name_target, valid_moves, capture_move)


def _find_move_state(
        name_src: str, valid_moves: List[MoveState]
) -> Optional[MoveState]:
    """Find an existing move with the given source name."""
    for move in valid_moves:
        if move.src_name == name_src:
            return move
    return None


# todo clean
def _update_move(
        move: MoveState, name_target: str, capture_move: Optional[CaptureMove] = None
) -> None:
    """Update the existing move with a new target and capture move."""
    move.target_names.append(name_target)  # Add the target name
    if capture_move:
        if move.capture_moves is None:
            move.capture_moves = []
        move.capture_moves.append(capture_move)  # Add the capture move if it exists


def _create_move(
        name_src: str, name_target: str, valid_moves: List[MoveState],
        capture_move: Optional[CaptureMove] = None
) -> None:
    """Create a new move and add it to the valid moves list."""
    if capture_move:
        new_move = generate_move(name_src, [name_target], True, [capture_move])
    else:
        new_move = generate_move(name_src, [name_target])

    valid_moves.append(new_move)


# todo
def handle_mandatory_capture(
        cells: list[tuple[Cell, Cell]], cell_map: dict[str, Cell]
) -> list[tuple[Cell, Cell]]:
    """
    Capture moves are mandatory by the game rules.
    If there are normal moves and capture moves - the normal moves are not added to the list
    """
    capture_moves = [
        (src, target) for src, target in cells
        if can_capture_piece(src, target) and _is_valid_capture(src, target, cell_map)
    ]

    filtered_cells = capture_moves if capture_moves else [
        (src, target) for src, target in cells
        if not can_capture_piece(src, target)
    ]

    return filtered_cells


# todo
#   add filter blocked from behind
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


def enforce_mandatory_capture(
        dest_cell_name: str, has_capture_moves: bool, move_dto: MoveState, target_cell: Cell
) -> None:
    """
    When a piece has capture moves and normal moves, enforce that only capture moves are allowed to execute.
    """
    if has_capture_moves:
        move_tuple = (target_cell.name, dest_cell_name)

        # check for an attempt to make a normal move when having a capture option
        if not any(
                (capture_move.name_target_cell, capture_move.name_final_cell) == move_tuple
                for capture_move in move_dto.capture_moves
        ):
            raise IllegalMoveError("Cannot make a normal move when capture is available")


def mange_chained_move(is_chained: bool, source_name: str, chaining_cell_name: str) -> None:
    if is_chained:
        name = chaining_cell_name
        if name != source_name:
            raise IllegalMoveError(f"{name} is in chain capture. Cannot move other pieces when chained.")


def format_available_moves(move_dtos: List[MoveState]) -> str:
    """
       Generate a user-friendly display of available moves.

       Returns: A string representation of the available moves to the current user.
       """
    no_moves_msg = "No available moves."
    if not move_dtos:
        return no_moves_msg

    formatted_moves = [
        f"[{idx + 1}] {description}"
        for idx, description in enumerate(
            description
            for move in move_dtos
            for description in generate_move_state_description(move).split("\n")
        )
    ]
    # todo: possible issue with testing because of the [index] but no specific order to the moves.
    return "\n".join(formatted_moves)


def generate_move_state_description(move: MoveState) -> str:
    """
    Formate available moves under game logic where capture moves are mandatory.

    When normal and capture moves are available, user must choose capture moves. Only when no capture moves available can execute normal moves.
    """
    if move.is_capture() and move.get_capture_moves():
        return format_capture_moves(move)
    else:
        return format_normal_moves(move)


def format_capture_moves(move: MoveState) -> str:
    """
    Format all capture moves for the given piece. From the source cell, capture, and final destination.

    """
    capture_moves = [
        f"{move.src_name} -> {capture.name_target_cell} -> {capture.name_final_cell}"
        for capture in move.get_capture_moves()
    ]
    return "\n".join(capture_moves)


def format_normal_moves(move: MoveState) -> str:
    """
    Format all normal( non-capture) moves for given piece.
    """
    targets = [
        f"{move.src_name} -> {target}"
        for target in move.target_names
    ]
    return "\n".join(targets)


def generate_king_moves(
        col_src: int, row_source: int
) -> list[tuple[int, int]]:
    """
        Generate possible moves for a king piece.

        A king piece can move diagonally in both forward and backward directions.
        position.
    """
    possible_rows = [-1, 1]
    possible_moves = [
        move
        for dr in possible_rows
        for move in get_potential_moves(row_source + dr, col_src)
    ]
    return possible_moves


def generate_normal_moves(
        col_src: int, owner: str, row_source: int
) -> list[tuple[int, int]]:
    """
        Generate possible moves for a normal piece.

        A normal piece can only move diagonally in the forward direction. The direction
        depends on the owner of the piece, moving "down" for player 1 and "up" for player 2.
    """
    row_target = index_offset(row_source) if owner == P.P1.name else row_source - 1
    possible_moves = get_potential_moves(row_target, col_src)
    return possible_moves
