from component.cell import Cell
from component.game import P
from exceptions.illegal_move_error import IllegalMoveError
from utils import extract_index_from_cell


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


def mandatory_capture_util(has_capture_moves, target_cell, dest_cell_name, move_dto):
    if has_capture_moves:
        move_tuple = (target_cell.name, dest_cell_name)

        # check for an attempt to make a normal move when having a capture option
        if not any(
                (capture_move.name_target_cell, capture_move.name_final_cell) == move_tuple
                for capture_move in move_dto.capture_moves
        ):
            raise IllegalMoveError("Cannot make a normal move when capture is available")
