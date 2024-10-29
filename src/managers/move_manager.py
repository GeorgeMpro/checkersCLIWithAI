from component.cell import Cell
from component.piece import Piece
from managers.move_generation_util import adding_moves_property_util, generate_normal_moves_util, \
    generate_king_moves_util, format_moves_util, handle_chain_util, filter_mandatory_capture
from managers.move_handle_util import mandatory_capture_util
from managers.move_validator_util import validate_move_util, generate_filtered_moves, \
    validate_capture_final_destination_is_available, validate_capture_final_destination_is_in_bounds
from state.move_state import MoveState


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
    return generate_filtered_moves(cells)


def validate_move(source_cell: Cell, target_cell: Cell) -> None:
    """
    Validates the legality and in-game boundaries of a move.
    """
    validate_move_util(source_cell, target_cell)


def validate_capture_move(final_dest_cell: Cell, final_dest_cell_piece: Piece) -> None:
    """
    Validate capture logic.
    """
    validate_capture_final_destination_is_in_bounds(final_dest_cell.name)
    validate_capture_final_destination_is_available(final_dest_cell_piece)


def manage_adding_moves_property_to_given_cells(
        cells: list[tuple[Cell, Cell]]
) -> list[MoveState]:
    return adding_moves_property_util(cells)


def handle_mandatory_capture(
        cells: list[tuple[Cell, Cell]], cell_map: dict[str, Cell]
) -> list[tuple[Cell, Cell]]:
    """
    Capture moves are mandatory by the game rules.
    If there are normal moves and capture moves - the normal moves are not added to the list
    """
    return filter_mandatory_capture(cells, cell_map)


def enforce_mandatory_capture(
        dest_cell_name: str, has_capture_moves: bool, move_dto: MoveState, target_cell: Cell
) -> None:
    """
    When a piece has capture moves and normal moves, enforce that only capture moves are allowed to execute.
    """
    mandatory_capture_util(has_capture_moves, target_cell, dest_cell_name, move_dto)


def mange_chained_move(
        is_chained: bool, source_name: str, chaining_cell_name: str
) -> None:
    handle_chain_util(is_chained, source_name, chaining_cell_name)


def format_available_moves(move_dtos: list[MoveState]) -> str:
    """
       Generate a user-friendly display of available moves.

       Returns: A string representation of the available moves to the current user.
       """
    return format_moves_util(move_dtos)


def generate_king_moves(
        col_src: int, row_source: int
) -> list[tuple[int, int]]:
    """
        Generate possible moves for a king piece.

        A king piece can move diagonally in both forward and backward directions.
        position.
    """
    return generate_king_moves_util(col_src, row_source)


def generate_normal_moves(
        col_src: int, owner: str, row_source: int
) -> list[tuple[int, int]]:
    """
        Generate possible moves for a normal piece.

        A normal piece can only move diagonally in the forward direction. The direction
        depends on the owner of the piece, moving "down" for player 1 and "up" for player 2.
    """
    return generate_normal_moves_util(col_src, owner, row_source)
