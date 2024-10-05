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
