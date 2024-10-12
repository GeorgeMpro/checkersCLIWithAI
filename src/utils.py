import logging
import re
from typing import List, Optional

from cell import Cell
from move_state import MoveState, CaptureMove



def get_logger(name: str):
    """
    Returns a logger configured for the project, logging to the console (DEBUG level).
    Args:
        name (str): The name of the logger, typically the module name.

    Returns:
        logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        log_format = '%(levelname)s - %(message)s'
        level = logging.DEBUG
        logging.basicConfig(level=level, format=log_format)
    return logger


def is_even(i: int, j: int) -> bool:
    return (i + j) % 2 == 0


def index_offset(index: int) -> int:
    """
    Increment the given index.
    """
    tmp = index + 1
    return tmp


def get_cell_row_from_name(source_cell: Cell) -> Optional[Cell]:
    source_row = source_cell.name[1:]
    return source_row


def extract_index_from_cell(source_cell: Cell) -> tuple[int, int]:
    """
    Extract the i,j values from cell a_ij.
    """
    source_index = re.match(r'a(\d)(\d)', source_cell.name)
    i, j = int(source_index[1]), int(source_index[2])
    return i, j


def is_valid_cell_name(name: str) -> bool:
    """
    Check if cell name is board bounds.
    """
    try:
        return bool(re.match(r'^a([1-8])([1-8])$', name))
    except TypeError:
        return False


def moves(
        src_name: str, targets: List[str], is_capture: bool = False,
        capture_moves: Optional[List[CaptureMove]] = None
) -> List[MoveState]:
    """
    Create a list of MoveState objects for a given source and target(s).

    :param src_name: Source cell name for the moves.
    :param targets: A list of target cell names for the moves.
    :param is_capture: Whether the moves are capture moves.
    :param capture_moves: List of capture moves, corresponding to the target cells.
    :return: A list of MoveState objects.
    """
    if capture_moves is None:
        # If no capture moves, return a single MoveState with all targets
        return [
            generate_move(src_name, targets, is_capture)
        ]
    # Otherwise, return a single MoveState with all targets and capture moves together
    return [
        generate_move(src_name, targets, is_capture, capture_moves)
    ]


def captures(name_target: str, name_final: str) -> CaptureMove:
    """
    Generate capture moves for a given target name and final destination.
    E.g. a11->a22->a33, a11 targets opponent on a22 and finally lands on a33.
    """
    return CaptureMove(name_target, name_final)


def get_potential_moves(row_target: int, col_src: int) -> List[tuple[int, int]]:
    """
    Generate moves that can be done by the piece in the cell.
    :return: move indexes
    """
    possible_moves = [
        (row_target, col_src + 1),
        (row_target, col_src - 1)
    ]
    return possible_moves


def generate_move(
        name_src: str, target_name: List[str], is_capture_move: bool = False,
        capture_moves: Optional[List[CaptureMove]] = None
) -> MoveState:
    return MoveState(
        src_name=name_src,
        target_names=target_name,
        is_capture_move=is_capture_move,
        capture_moves=capture_moves
    )
