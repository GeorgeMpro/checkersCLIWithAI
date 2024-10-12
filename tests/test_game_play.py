import pytest

from conftest import setup_piece_on_cell_by_name_and_owner, board_setup, assert_player_turn_after_move, setup_board, \
    get_cell_by_name, get_valid_moves_for_given_cell
from exceptions.illegal_move_error import IllegalMoveError
from game import Player as P
from move_state import MoveState
from utils import moves, captures


class TestMoveList:

    @pytest.mark.parametrize("cell_name,piece_owner,expected_moves",
                             [("a11", P.P1.name, moves("a11", ["a22"])),
                              ("a13", P.P1.name, moves("a13", ["a22", "a24"])),
                              ("a82", P.P2.name, moves("a82", ["a71", "a73"])),
                              ("a88", P.P2.name, moves("a88", ["a77"])),
                              ])
    def test_get_move_list(
            self, board_setup, piece_owner, cell_name, expected_moves
    ):
        setup_piece_on_cell_by_name_and_owner(board_setup, piece_owner, cell_name)
        cell = get_cell_by_name(board_setup, cell_name)
        actual_moves = get_valid_moves_for_given_cell(board_setup, cell)

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
        cell = get_cell_by_name(board_setup, cell_src)
        actual_moves = get_valid_moves_for_given_cell(board_setup, cell)

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
        cell = get_cell_by_name(board_setup, cell_src)
        actual_moves = get_valid_moves_for_given_cell(board_setup, cell)

        assert actual_moves == expected_moves

        # todo

    def test_cannot_move_to_normal_cell_if_has_capture(self, board_setup):
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, "a13")
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P2.name, "a24")

        actual_moves = get_valid_moves_for_given_cell(board_setup, get_cell_by_name(board_setup, "a13"))
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
        board_setup.initial_setup()
        assert board_setup.get_current_turn() == P.P1.name
        assert_player_turn_after_move(board_setup, "a33", "a44", P.P2.name)
        assert_player_turn_after_move(board_setup, "a62", "a53", P.P1.name)
        assert_player_turn_after_move(board_setup, "a44", "a53", P.P2.name)
        assert_player_turn_after_move(board_setup, "a71", "a62", P.P1.name)

    @pytest.mark.parametrize("pieces, moves_sequence", [
        ([(P.P1.name, "a13"), (P.P1.name, "a73"), (P.P2.name, "a24"), (P.P2.name, "a44"),
          (P.P2.name, "a64"), (P.P2.name, "a82")],
         [("a13", "a24", P.P1.name),  # First capture by P1
          ("a35", "a44", P.P1.name),  # Continue capture by P1
          ("a53", "a64", P.P2.name),  # No more captures, turn to P2
          ("a82", "a73", P.P1.name)]
         )
    ])
    def test_chained_move_keeps_player_turn(self, board_setup, pieces, moves_sequence):
        # Set up the board with the given pieces
        setup_board(board_setup, pieces)

        # chained capture p1
        # a33-> a24 -> a35
        # keep turn
        # a35-> a44 -> a53
        # keep turn
        # a53-> a64 -> a75
        # done p1 begin normal p2 capture
        # p2 done back to p1
        for (src, target, expected_turn) in moves_sequence:
            assert_player_turn_after_move(board_setup, src, target, expected_turn)

    @pytest.mark.parametrize("pieces", [
        [(P.P1.name, "a11"), (P.P1.name, "a17"),
         (P.P2.name, "a22"), (P.P2.name, "a42")]
    ])
    def test_cannot_move_other_pieces_when_chained_capture(self, board_setup, pieces):
        setup_board(board_setup, pieces)

        assert_player_turn_after_move(board_setup, "a11", "a22", P.P1.name)
        with pytest.raises(IllegalMoveError, match=f"a33 is in chain capture. Cannot move other pieces when chained."):
            board_setup.move_piece("a17", "a28")

    # todo when getting all available moves is complete
    def test_when_chain_capture_has_only_the_chaining_cell_move_list(self, board_setup):
        pass

    # todo
    def test_can_keep_track_of_turns(self):
        pass

    #   todo
    #       stack for only undo
    #       deque for undo and redo
    #       https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks
    def can_undo_turn(self):
        pass


# todo move
def assert_stays_king(board_setup, source_name, target_name):
    board_setup.move_piece(source_name, target_name)
    assert board_setup.cell_manager.get_cell_by_name(target_name).is_king()


def set_king_by_cell_name(
        board_setup, cell_name: str
) -> None:
    board_setup.cell_manager.get_cell_by_name(cell_name).set_king()


class TestKing:
    king_moves = [
        ("a31", "a22"), ("a22", "a13"), ("a13", "a24")
    ]

    @pytest.mark.parametrize("king_moves",
                             [king_moves])
    def test_king_can_move_backwards(self, board_setup, king_moves):
        initial_cell = king_moves[0][0]
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, initial_cell)
        king = board_setup.cell_manager.get_cell_by_name(initial_cell)
        king.set_king()
        assert king.is_king()
        for src, target in king_moves:
            assert_stays_king(board_setup, src, target)

    @pytest.mark.parametrize("src,p_name, targets",
                             [("a22", P.P1.name, ["a11", "a13", "a33", "a31"]),
                              ("a73", P.P2.name, ["a62", "a64", "a82", "a84"])])
    def test_king_move_state(self, board_setup, src, p_name, targets):
        # setup
        setup_piece_on_cell_by_name_and_owner(board_setup, p_name, src)

        # setup king and turn
        set_king_by_cell_name(board_setup, src)
        extract_player = board_setup.cell_manager.get_cell_by_name(src).get_piece_owner()
        board_setup.game.set_player(extract_player)

        actual = board_setup.get_available_moves()
        expected = moves(src, targets)
        assert actual == expected

    # todo
    def test_can_have_king_move_list_prompt(self, board_setup):
        src_name = "a22"
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, src_name)
        set_king_by_cell_name(board_setup, src_name)
        actual = board_setup.get_available_moves()
        actual_prompt = board_setup.get_user_moves_prompt(actual)
        expected_prompt = "[1] a22 -> a13\n[2] a22 -> a11\n[3] a22 -> a33\n[4] a22 -> a31"

        assert actual_prompt == expected_prompt

    # todo
    @pytest.mark.parametrize("king,p_king, sacrifice, p_sac",
                             [
                                 ("a33", P.P1.name, "a22", P.P2.name),
                                 ("a66", P.P2.name, "a77", P.P1.name)
                             ])
    def test_king_can_capture_backwards(self, board_setup, king, p_king, sacrifice, p_sac):
        # setup king and sacrifice
        setup_piece_on_cell_by_name_and_owner(board_setup, p_king, king)
        setup_piece_on_cell_by_name_and_owner(board_setup, p_sac, sacrifice)
        set_king_by_cell_name(board_setup, king)

        assert get_cell_by_name(board_setup, king).get_piece_owner() == p_king
        # capture backwards
        board_setup.move_piece(king, sacrifice)
        assert get_cell_by_name(board_setup, sacrifice).get_piece_owner() is None

    @pytest.mark.parametrize("src,owner,dest",
                             [
                                 ("a77", P.P1.name, "a86"),
                                 ("a77", P.P1.name, "a88"),
                                 ("a22", P.P2.name, "a13"),
                                 ("a22", P.P2.name, "a11")
                             ])
    def test_piece_can_become_king(self, board_setup, src, owner, dest):
        setup_piece_on_cell_by_name_and_owner(board_setup, owner, src)
        assert not board_setup.cell_manager.get_cell_by_name(src).is_king()

        board_setup.move_piece(src, dest)
        assert board_setup.cell_manager.get_cell_by_name(dest).is_king()


class TestWinCondition:
    # todo
    def test_can_advance_game_turn(self):
        pass

    #     todo
    def test_win_when_no_opponent_pieces(self):
        pass

    # todo
    def test_win_when_no_moves_and_one_has_more_pieces(self):
        pass

    # todo
    def test_draw_when_no_moves_and_same_pieces(self):
        pass


class TestGameInteraction:
    import pytest

    @pytest.mark.parametrize("pieces, expected", [
        (
                [(P.P1.name, "a11"), (P.P1.name, "a17"),
                 (P.P2.name, "a73"), (P.P2.name, "a88")],
                [
                    MoveState("a11", ["a22"]),  # P1 available moves
                    MoveState("a17", ["a28", "a26"]),
                    MoveState("a73", ["a62", "a64"]),  # P2 available moves
                    MoveState("a88", ["a77"])
                ]
        )
    ])
    def test_can_get_available_moves_for_player(self, board_setup, pieces, expected):
        setup_board(board_setup, pieces)

        # Get available moves for Player 1
        board_setup.game.get_turn()
        actual = board_setup.get_available_moves()
        assert actual == expected[:2]  # Check for Player 1's expected moves

        # Toggle turn and get available moves for Player 2
        board_setup.game.toggle_whose_turn()
        actual_p2 = board_setup.get_available_moves()
        assert actual_p2 == expected[2:]  # Check for Player 2's expected moves

    # todo
    @pytest.mark.parametrize("pieces, expected", [
        ([(P.P1.name, "a11"), (P.P1.name, "a17")],
         [MoveState("a11", ["a22"]),  # P1 available moves
          MoveState("a17", ["a28", "a26"])]
         )])
    def test_can_present_available_moves_for_player(self, board_setup, pieces, expected):
        setup_board(board_setup, pieces)
        board_setup.game.get_turn()
        actual = board_setup.get_available_moves()
        assert actual == expected

    @pytest.mark.parametrize("pieces, expected", [
        ([(P.P1.name, "a11"), (P.P1.name, "a17"),
          (P.P2.name, "a22")],
         [MoveState("a11", ["a22"], True, [captures("a22", "a33")])]  # P1 available moves
         )])
    def test_can_present_available_moves_for_player(self, board_setup, pieces, expected):
        setup_board(board_setup, pieces)
        board_setup.game.get_turn()
        actual = board_setup.get_available_moves()
        actual_prompt = board_setup.get_user_moves_prompt(actual)
        expected_prompt = "[1] a11 -> a22 -> a33"
        assert actual == expected
        assert actual_prompt == expected_prompt

    # todo
    def test_player_can_choose_action(self):
        pass

    # todo
    def test_can_redo_action(self):
        pass
