import re

from cell import Cell
from move_state import MoveState


def is_even(i, j):
    return (i + j) % 2 == 0


def increment_index(index):
    """
    update index to start at 1 in the name of the cell
    """
    tmp = index + 1
    return tmp


def get_cell_row_from_name(source_cell):
    source_row = source_cell.name[1:]
    return source_row


def extract_index_from_cell(source_cell: Cell) -> tuple[int, int]:
    source_index = re.match(r'a(\d)(\d)', source_cell.name)
    i, j = int(source_index[1]), int(source_index[2])
    return i, j


def is_valid_cell_name(name):
    try:
        return bool(re.match(r'^a([1-8])([1-8])$', name))
    except TypeError:
        return False


def sort_moves(move_list: list[MoveState]) -> list[MoveState]:
    """
    Sort a list of MoveState objects based on their attributes for consistent ordering.

    :param move_list: A list of MoveState objects representing possible moves.
    :return: A list of MoveState objects sorted by src_name, target_name, is_capture_move, and final_dest_name.
    """
    valid_moves_sorted = sorted(move_list, key=lambda move: (
        move.src_name, move.target_name, move.is_capture_move, move.final_dest_name))
    return valid_moves_sorted
