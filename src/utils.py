import re

from cell import Cell


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


def extract_index_from_cell_name(source_cell: Cell) -> tuple[int, int]:
    source_index = re.match(r'a(\d)(\d)', source_cell.name)
    i, j = int(source_index[1]), int(source_index[2])
    return i, j


def is_valid_cell_name(name):
    try:
        return bool(re.match(r'^a([1-8])([1-8])$', name))
    except TypeError:
        return False
