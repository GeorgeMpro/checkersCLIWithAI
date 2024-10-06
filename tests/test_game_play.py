import pytest

import utils
from typing import List
from conftest import setup_piece_on_cell_by_name_and_owner, board_setup
from move_state import MoveState


# todo
#   print board (state?)
#   get available moves
#   present moves to player
#   get selected move from player
#   apply move
#   check win condition
#   switch turns
#   ? log move in history?


# todo invalid move does not change board
# todo alternate between p1 and p2

# todo
#    test can get player turn
#    test can switch player turn
#    test player only move its pieces during turn

# todo test get move list
#    fetch move list according to owner?
#    test blocked moves not in list
#    test out of bound moves not in list
#    test backwards not in list
# todo a way to go over piece list for each player
# todo check on piece in cell error?


# todo incremen row and attempt


def moves(src_name: str, targets: List[str], is_capture: bool = False) -> List[MoveState]:
    """
    Create a list of MoveState objects for a given source and target(s).

    :param src_name: Source cell name for the moves.
    :param targets: A list of target cell names for the moves.
    :param is_capture: Whether the moves are capture moves.
    :return: A list of MoveState objects.
    """
    return [MoveState(src_name=src_name, target_name=target, is_capture_move=is_capture) for target in targets]


class TestMoveList:

    @pytest.mark.parametrize("cell_name,piece_owner,expected_moves",
                             [("a11", "p1", moves("a11", ["a22"])),
                              ("a13", "p1", moves("a13", ["a22", "a24"])),
                              ("a82", "p2", moves("a82", ["a71", "a73"])),
                              ("a88", "p2", moves("a88", ["a77"])),
                              ])
    def test_get_move_list(self, board_setup, piece_owner, cell_name, expected_moves):
        # todo
        #    get board
        #    put piece on board
        #    check valid moves
        #    add move to tuple or something
        #    return the list

        setup_piece_on_cell_by_name_and_owner(board_setup, piece_owner, cell_name)
        # todo
        #    get piece list
        #    get valid move list
        #   ? piece has valid moves field?
        cell = board_setup.get_cell_by_name(cell_name)
        valid_moves = board_setup.get_valid_moves_list(cell)

        # todo
        #   get owner - determine direction
        #   go over possible moves?
        #   validate moves
        #   return moves

        # todo
        #   no piece in cell?

        # Note: no special meaning to the order of the moves at this point
        assert len(valid_moves) == len(expected_moves)
        valid_moves_sorted = utils.sort_moves(valid_moves)
        expected_moves_sorted = utils.sort_moves(expected_moves)

        assert valid_moves_sorted == expected_moves_sorted, f"Expected moves do not match actual moves.\nExpected: {expected_moves_sorted}\nActual: {valid_moves_sorted}"

        # for actual, expected in zip(valid_moves, expected_moves):
        #     assert actual == expected

        # todo board state?

# todo can keep possible moves
# todo can keep past move - undo opponent, undo your move
#     deque?
