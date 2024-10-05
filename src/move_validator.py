from cell import Cell

from exceptions.illegal_move_error import IllegalMoveError


class MoveValidator:
    def __init__(self):
        pass

    @staticmethod
    def is_valid_move_direction(source_cell: Cell, source_row: int, target_row: int) -> bool:
        owner = source_cell.get_piece_owner()
        # p1 cannot move "down"; p2 cannot move "up"
        rules = {
            "p1": lambda source, target: source > target,
            "p2": lambda source, target: source < target,
        }
        # check if players is attempting to move backwards
        if owner in rules and rules[owner](source_row, target_row):
            return False
        return True

    @staticmethod
    def is_not_same_cell(source_cell, target_cell):
        if source_cell == target_cell:
            raise IllegalMoveError("Cannot move to the same cell")
