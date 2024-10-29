from typing import Optional

from component.cell import Cell
from component.game import P
from exceptions.illegal_move_error import IllegalMoveError
from managers.move_handle_util import get_destination_cell_name_after_capture
from managers.move_validator_util import can_capture_piece, _is_valid_capture
from state.move_state import CaptureMove, MoveState
from utils import captures, generate_move, index_offset, get_potential_moves


def format_moves_util(move_dtos: list[MoveState]) -> str:
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


def adding_moves_property_util(
        cells: list[tuple[Cell, Cell]]
) -> list[MoveState]:
    valid_moves = []
    for cell_src, cell_target in cells:
        name_src = cell_src.name
        name_target = cell_target.name
        _add_moves_property(cell_src, cell_target, name_src, name_target, valid_moves)
    return valid_moves


def _add_moves_property(
        cell_src: Cell, cell_target: Cell, name_src: str, name_target: str,
        valid_moves: list[MoveState]
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
        name_src: str, name_target: str, valid_moves: list[MoveState],
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
        name_src: str, valid_moves: list[MoveState]
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
        name_src: str, name_target: str, valid_moves: list[MoveState],
        capture_move: Optional[CaptureMove] = None
) -> None:
    """Create a new move and add it to the valid moves list."""
    if capture_move:
        new_move = generate_move(name_src, [name_target], True, [capture_move])
    else:
        new_move = generate_move(name_src, [name_target])

    valid_moves.append(new_move)


def generate_king_moves_util(col_src, row_source):
    possible_rows = [-1, 1]
    possible_moves = [
        move
        for dr in possible_rows
        for move in get_potential_moves(row_source + dr, col_src)
    ]
    return possible_moves


def generate_normal_moves_util(col_src, owner, row_source):
    row_target = index_offset(row_source) if owner == P.P1.name else row_source - 1
    possible_moves = get_potential_moves(row_target, col_src)
    return possible_moves


def handle_chain_util(is_chained: bool, source_name: str, chaining_cell_name: str):
    if is_chained:
        name = chaining_cell_name
        if name != source_name:
            raise IllegalMoveError(f"{name} is in chain capture. Cannot move other pieces when chained.")


def filter_mandatory_capture(
        cells: list[tuple[Cell, Cell]], cell_map: dict[str, Cell]
) -> list[tuple[Cell, Cell]]:
    capture_moves = [
        (src, target) for src, target in cells
        if can_capture_piece(src, target) and _is_valid_capture(src, target, cell_map)
    ]
    filtered_cells = capture_moves if capture_moves else [
        (src, target) for src, target in cells
        if not can_capture_piece(src, target)
    ]
    return filtered_cells
