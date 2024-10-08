import pytest

from utils import moves, captures
from conftest import setup_piece_on_cell_by_name_and_owner, board_setup
from game import Player as P


def assert_player_turn_after_move(board_setup, src: str, target: str, expected_player_turn: str):
    board_setup.move_piece(src, target)
    assert board_setup.get_current_turn() == expected_player_turn


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

class TestMoveList:

    @pytest.mark.parametrize("cell_name,piece_owner,expected_moves",
                             [("a11", P.P1.name, moves("a11", ["a22"])),
                              ("a13", P.P1.name, moves("a13", ["a22", "a24"])),
                              ("a82", P.P2.name, moves("a82", ["a71", "a73"])),
                              ("a88", P.P2.name, moves("a88", ["a77"])),
                              ])
    def test_get_move_list(self, board_setup, piece_owner, cell_name, expected_moves):
        setup_piece_on_cell_by_name_and_owner(board_setup, piece_owner, cell_name)
        cell = board_setup.get_cell_by_name(cell_name)
        actual_moves = board_setup.get_valid_moves_for_given_cell(cell)

        assert len(actual_moves) == len(expected_moves)
        assert actual_moves == expected_moves, f"Expected moves do not match actual moves.\nExpected: {expected_moves}\nActual: {actual_moves}"

    @pytest.mark.parametrize("cell_src,owner_src,cell_target, owner_target,expected_moves",
                             [
                                 ("a11", P.P1.name, "a22", P.P2.name,
                                  moves("a11", ["a22"], True, [captures("a22", "a33")])),

                             ])
    def test_move_list_with_capture(self, board_setup, cell_src, owner_src, cell_target, owner_target, expected_moves):
        setup_piece_on_cell_by_name_and_owner(board_setup, owner_src, cell_src)
        setup_piece_on_cell_by_name_and_owner(board_setup, owner_target, cell_target)
        cell = board_setup.get_cell_by_name(cell_src)
        actual_moves = board_setup.get_valid_moves_for_given_cell(cell)

        assert len(actual_moves) == len(expected_moves)
        assert actual_moves == expected_moves

    # todo
    @pytest.mark.parametrize("cell_src,owner_src,cells_target, owner_target,expected_moves",
                             [("a13", P.P1.name, ["a22", "a24"], P.P2.name,
                               moves("a13", ["a22", "a24"], True, [captures("a22", "a31"), captures("a24", "a35")]),
                               )])
    # todo
    def test_move_list_with_multiple_capture_paths(self, board_setup, cell_src, owner_src, cells_target, owner_target,
                                                   expected_moves):
        setup_piece_on_cell_by_name_and_owner(board_setup, owner_src, cell_src)
        for cell_target in cells_target:
            setup_piece_on_cell_by_name_and_owner(board_setup, owner_target, cell_target)
        cell = board_setup.get_cell_by_name(cell_src)
        actual_moves = board_setup.get_valid_moves_for_given_cell(cell)

        assert actual_moves == expected_moves

        # todo

    def test_cannot_move_to_normal_cell_if_has_capture(self, board_setup):
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, "a13")
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P2.name, "a24")

        actual_moves = board_setup.get_valid_moves_for_given_cell(board_setup.get_cell_by_name("a13"))
        expected_moves = moves("a13", ["a24"], True, [captures("a24", "a35")])

        assert actual_moves == expected_moves

    # todo
    def test_when_piece_has_capture_moves_removes_non_capture_moves_from_move_list(self, board_setup):
        pass

    # todo
    def test_when_pieces_have_capture_moves_non_captures_moves_are_not_in_list(self):
        pass

    # todo
    #   a two pass solution to make pieces that can capture

    # todo
    def test_move_list_with_chained_capture(self):
        pass


class TestGamePlay:

    def test_has_player_turn(self, board_setup):
        assert board_setup.get_current_turn() == P.P1.name

    def test_player_turn_updates_after_playing(self, board_setup):
        # setup board
        board_setup.initial_setup()

        assert board_setup.get_current_turn() == P.P1.name
        assert_player_turn_after_move(board_setup, "a33", "a44", P.P2.name)
        assert_player_turn_after_move(board_setup, "a62", "a53", P.P1.name)
        assert_player_turn_after_move(board_setup, "a44", "a53", P.P2.name)
        assert_player_turn_after_move(board_setup, "a73", "a62", P.P1.name)

    # todo
    @pytest.mark.skip
    def test_chained_move_keeps_player_turn(self, board_setup):
        # setup board pieces
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, "a13")
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P2.name, "a24")
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P2.name, "a44")

        # todo
        print(f"\n{board_setup}")
        # chained capture
        # a33-> a24 -> a35
        # keep turn
        # a35-> a44 -> a53
        assert_player_turn_after_move(board_setup, "a13", "a24", P.P1.name)
        assert_player_turn_after_move(board_setup, "a35", "a44", P.P2.name)

        # todo
        print(f"\n{board_setup}")

    # todo
    def test_if_normal_move_after_chain_change_player(self):
        pass

    # todo
    #   get game state thingy
    #     change initial setup to turn 1
    # update after move

    # todo

    def test_can_keep_track_of_turns(self):
        pass

    # todo
    def test_chained_move_has_one_src_cell_from(self):
        # todo get moves for only one?
        pass

    # todo
    def test_can_advance_game_turn(self):
        pass

    #   todo
    def can_undo_turn(self):
        pass

    # todo

    #   go over possible moves?
    #   validate moves
    #   return moves

    # todo
    #   no piece in cell?

    # todo board state?

    # todo can keep possible moves
    # todo can keep past move - undo opponent, undo your move
    #     deque?

    # todo
    #   add chained capture moves
    #   chained stop if blocked but have to go...
    #   choose chain if multi?

    # todo
    #   chained move ->
    #   game state {player, is_chained, piece_capturing (optional none)}
    #   when is capture = false done
