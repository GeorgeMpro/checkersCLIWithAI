import pytest

from ai.educated_guess_heuristic import _eval_player_pieces_score, eval_player_state
from ai.heuristic_move_explorer import get_number_of_moves, extract_in_order_all_move_src_target, \
    calculate_copy_state_score
from board import Board
from component.game import P
from conftest import board_setup, setup_board, get_cell_by_name, setup_and_get_both_cells

# names values for the players
p1 = P.P1.name
p2 = P.P2.name


def set_kings_by_name(
        board_setup: Board, king_cells: list[str]
) -> None:
    for king_name in king_cells:
        cell = get_cell_by_name(board_setup, king_name)
        cell.set_king()




class TestHeuristic:
    """
    Evaluate current and immediate game state.

    """

    def test_empty_board_score(self, board_setup):
        player_cells = board_setup.cell_manager.get_player_cells(p1)
        number_of_pieces = len(player_cells)
        state_score = _eval_player_pieces_score(player_cells, 10)

        assert number_of_pieces == 0
        assert state_score == 0

    @pytest.mark.parametrize("cells, expected_number_of_pieces, expected_state_score", [
        ([(p1, "a13"), (p2, "a46")], 1, 10),
        ([(p1, "a13"), (p1, "a11"), (p2, "a46")], 2, 20)
    ])
    def test_can_evaluate_pieces(
            self, board_setup: Board, cells: list[tuple[str, str]], expected_number_of_pieces: int,
            expected_state_score: int
    ):
        setup_board(board_setup, cells)
        player_cells = board_setup.cell_manager.get_player_cells(p1)
        number_of_pieces = len(player_cells)
        state_score = _eval_player_pieces_score(player_cells, 10)

        assert number_of_pieces == expected_number_of_pieces
        assert state_score == expected_state_score

    @pytest.mark.parametrize("cells, king_cells, expected_number_of_pieces, expected_state_score", [
        ([(p1, "a13"), (p2, "a46")], ["a13"], 1, 20),
        ([(p1, "a13"), (p1, "a11"), (p2, "a46")], ["a13"], 2, 30),
        ([(p1, "a13"), (p1, "a11"), (p1, "a33"), (p2, "a46")], ["a13", "a33"], 3, 50)
    ])
    def test_can_eval_king_piece(
            self, board_setup: Board, cells: list[tuple[str, str]],
            king_cells: list[str], expected_number_of_pieces: int,
            expected_state_score: int
    ):
        setup_board(board_setup, cells)
        player_cells = board_setup.cell_manager.get_player_cells(p1)
        set_kings_by_name(board_setup, king_cells)
        number_of_pieces = len(player_cells)
        state_score = _eval_player_pieces_score(player_cells, 10, 2)

        assert number_of_pieces == expected_number_of_pieces
        assert state_score == expected_state_score

    @pytest.mark.parametrize("cells, king_cells, expected_number_of_pieces, expected_state_score", [
        ([(p1, "a13"), (p2, "a46")], ["a13"], 1, 10),
        ([(p1, "a13"), (p1, "a11"), (p2, "a46")], ["a13"], 2, 20),
        ([(p1, "a13"), (p1, "a11"), (p1, "a33"), (p2, "a46")], ["a13", "a33"], 3, 40),
        # notice: opponent has king
        ([(p1, "a13"), (p1, "a11"), (p1, "a33"), (p2, "a46")], ["a13", "a33", "a46"], 3, 30)
    ])
    def test_can_eval_current_game_state(
            self, board_setup: Board, cells: list[tuple[str, str]], king_cells: list[str],
            expected_number_of_pieces: int, expected_state_score: int):
        player_cells, opponent_cells = setup_and_get_both_cells(board_setup, cells)
        set_kings_by_name(board_setup, king_cells)
        number_of_pieces = len(player_cells)
        state_score = eval_player_state(player_cells, opponent_cells, piece_score=10, king_modifier=2, )

        assert number_of_pieces == expected_number_of_pieces
        assert state_score == expected_state_score

    # todo
    #   notice: DOES NOT CHECK THE GAME ENDED! need to check separate and pass
    def test_win_score(self, board_setup):
        player_cells = board_setup.cell_manager.get_player_cells(p1)
        opponent_cells = board_setup.cell_manager.get_player_cells(p2)
        is_win = True
        state_score = eval_player_state(player_cells, opponent_cells, 10, 2, is_win)
        expected_score = 100

        assert state_score == expected_score

    # todo
    def test_score_compare_to_opponent(self):
        pass

    # todo
    def test_lose_score(self, board_setup):
        pass

    # todo
    def test_win_lose_with_pieces_score(self, board_setup):
        pass


class TestCumulativeHeuristic:

    @pytest.mark.parametrize("pieces, expected_number_of_moves", [
        ([], 0),
        ([(p1, "a11"), (p2, "a33")], 1),
        ([(p1, "a11"), (p1, "a13"), (p2, "a33")], 3),
        # Notice: mandatory capture move:
        ([(p1, "a11"), (p1, "a22"), (p2, "a33")], 1),
        ([(p1, "a24"), (p1, "a22"), (p2, "a33")], 2)
    ])
    def test_can_verify_number_of_moves(self, board_setup, pieces, expected_number_of_moves):
        setup_board(board_setup, pieces)
        available_moves = board_setup.get_available_moves(p1)
        actual_number_of_moves = get_number_of_moves(available_moves)

        assert actual_number_of_moves == expected_number_of_moves

    @pytest.mark.parametrize("pieces, expected_moves,expected_number_of_moves", [
        ([(p1, "a11"), (p2, "a33")], [("a11", "a22")], 1),
        ([(p1, "a13")], [("a13", "a22"), ("a13", "a24")], 2),
        ([(p1, "a11"), (p1, "a13")], [("a11", "a22"), ("a13", "a22"), ("a13", "a24")], 3),
    ])
    def test_can_extract_all_available_moves(
            self, board_setup: Board, pieces: list[tuple[str, str]], expected_moves: list[tuple[str, str]],
            expected_number_of_moves: int
    ):
        """
        Test that the function extract all src and target names.

        The return value is sorted for easier testing, notice in test parameters.
        """
        setup_board(board_setup, pieces)
        available_moves = board_setup.get_available_moves(p1)
        actual_moves = extract_in_order_all_move_src_target(available_moves)
        actual_number_of_moves = get_number_of_moves(available_moves)

        assert actual_number_of_moves == expected_number_of_moves
        assert actual_moves == expected_moves

    @pytest.mark.parametrize("player,opponent, pieces,expected_copy_score", [
        (p1, p2, [(p1, "a11"), (p1, "a13"), (p2, "a33")], 10),
        (p2, p1, [(p1, "a11"), (p1, "a13"), (p2, "a33")], -10),

    ])
    def test_can_get_score_from_copy(
            self, board_setup: Board, player: str, opponent: str, pieces: list[tuple[str, str]],
            expected_copy_score: int
    ):
        setup_board(board_setup, pieces)
        map_copy = board_setup.cell_manager.get_cell_map_copy()

        actual_copy_score = calculate_copy_state_score(map_copy, player, opponent)

        assert actual_copy_score == expected_copy_score



    # todo
    @pytest.mark.skip
    def test_can_move_on_copy(self, board_setup):
        pieces = [(p1, "a11"), (p1, "a13"), (p2, "a33")]
        setup_board(board_setup, pieces)
        map_copy = board_setup.cell_manager.get_cell_map_copy()

        pass

    # todo
    def test_can_generate_copy_for_each_move_and_execute_move(self):
        pass
    # todo
    #   can update game state copy for a win/lose/chain



    # todo
    def test_can_get_score_after_move_on_copy(self, board_setup):
        pass

    # todo
    def test_keep_score_on_multiple_moves(self, board_setup):
        pass

    # todo
    def test_keep_score_for_several_depths(self, board_setup):
        pass

    # TODO!
    #   wrong test, need to check i can move forward in moves
    #   check getting cells and moving forward on board
    #   assumption -> the moves provided are CORRECT
    #   pass move piece from board?
    #   The moves are correct and filtered -> create slim utilty/helper:
    #   get cell maps, execute move.
    #   that's it.
    def test_can_get_state_score_after_move(self, board_setup):
        # TODO!
        # "Note: This utility class assumes that all move inputs are pre-validated by the Board class. No additional checks for move validity are performed here."
        # todo
        #   get copy of board
        #   move on copy
        #   get score for state
        #   then
        #   get moves
        #   go over each move and perform it
        #   get score for each state after move

        pass

    # todo
    @pytest.mark.skip
    def test_get_score_from_all_available_moves(self, board_setup):
        setup_board(board_setup, [(p1, "a11"), (p1, "a13"), (p2, "a33")])
        available_moves = board_setup.get_available_moves(p1)
        actual_moves = extract_in_order_all_move_src_target(available_moves)

        pass

    def test_no_more_moves_game_end(self):
        pass

    # todo
    def test_return_board_score_after_turn(self, board_setup):
        # todo
        #   setup: normal, normal,

        pass

    # todo
    def test_can_score_possible_moves(self):
        pass

    # todo
    def test_select_best_move_for_given_scenario(self):
        pass

    # todo
    def test_piece_has_no_score_after_being_captured(self):
        pass

    def test_can_eval_being_captured(self):
        pass

    # todo
    def test_score_on_capturing_a_king(self):
        pass

    # todo
    def test_score_on_losing_a_king(self):
        pass

    # todo
    def test_evaluate_board_symmetry_identical_scores(self):
        pass

    # todo
    def test_win_and_lose_states_score(self):
        pass

    # todo ?
    def test_draw(self):
        pass

    # todo
    def test_scoring_being_captured_after_capturing(self):
        pass

    # todo
    def test_score_for_opponent_sacrificing_piece_for_multi_capture(self):
        """
        Check for "trap" moves by the opponent.
        """

    # todo
    def test_score_on_promoting_piece_to_king(self):
        pass

    # todo
    def test_chain_capture_score(self):
        pass

    # todo
    def test_evaluate_incomplete_board(self):
        """
        Test for irregular game states like player having only one piece and scoring accordingly.

        """

    # todo
    def test_can_evaluate_piece_loss_after_capture_next_move(self):
        # todo
        #   can calculate that the move lead to a capture by total state
        pass

    # todo
    def test_eval_move_reduce_opponent_piece_count(self):
        pass

    # todo
    def test_no_more_moves_stops_eval(self):
        pass


class TestMoveSelection:
    # todo
    def test_can_return_highest_scored_move(self):
        pass

    # TODO move to hasher?
    def test_hash_state_key_has_score_value(self):
        pass
