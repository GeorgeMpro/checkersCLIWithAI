from io import StringIO

import pytest

from component.cell import Cell
from component.game import P
from conftest import setup_board, setup_piece_on_cell_by_name_and_owner, get_cell_by_name, board_setup
from display.cli import get_choice, moves_dto_to_dict, parse_prompt, extract_src_target_names, \
    extract_move_chosen_by_user
from state.move_state import MoveState
from utils import captures


@pytest.fixture
def options() -> dict:
    return {
        1: "[1] a11 -> a22",
        2: "[2] a11 -> a33",
        3: "[3] a22 -> a33",
        'q': "quit"
    }


def mock_user_input(monkeypatch, user_in: str) -> None:
    """
    Helper function to mock user input from stdin.
    """
    input_string = StringIO(user_in)
    monkeypatch.setattr('sys.stdin', input_string)


def get_moves_and_prompt(
        board_setup, pieces: list[tuple[str, str]] = None
) -> tuple[list[MoveState], str]:
    if pieces is None:
        pieces = [
            (P.P1.name, "a13"), (P.P1.name, "a33"), (P.P2.name, "a77"),
        ]

    setup_board(board_setup, pieces)
    moves = board_setup.get_available_moves()
    prompt = board_setup.get_user_moves_prompt(moves)
    return moves, prompt


def assert_final_state(
        src_cell: Cell, tar_cell: Cell, tar_expected: str
) -> None:
    assert not src_cell.has_piece()
    assert tar_cell.has_piece()
    assert tar_cell.get_name() == tar_expected


def assert_initial(
        src_cell: Cell, src_expected: str, tar_cell: Cell
) -> None:
    assert src_cell.has_piece()
    assert not tar_cell.has_piece()
    assert src_cell.get_name() == src_expected


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

    @pytest.mark.parametrize("src_name,tar_name,final_name", [
        ("a42", "a51", "a60"),
        ("a73", "a82", "a91"),
        ("a77", "a88", "a99"),
    ])
    def test_does_not_present_capture_final_out_of_bounds(
            self, board_setup, src_name, tar_name, final_name
    ):
        invalid_move_prompt = src_name + " -> " + tar_name
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, src_name)
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P2.name, tar_name)

        moves = board_setup.get_available_moves()
        prompt = board_setup.get_user_moves_prompt(moves)

        assert prompt != "[1] " + src_name + " -> " + tar_name + " -> " + final_name
        assert invalid_move_prompt not in prompt

    # todo
    def test_does_not_present_blocked_capture(self, board_setup):
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, "a13")
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P2.name, "a24")
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P2.name, "a35")

        moves = board_setup.get_available_moves()
        prompt = board_setup.get_user_moves_prompt(moves)

        assert prompt != "[1] a13 -> a24 -> a35"
        assert "a13 -> a24" not in prompt

    @pytest.mark.parametrize("user_in, expected", [
        ("1", 1), ("2", 2), ("3", 3)
    ])
    def test_player_can_choose_action(self, monkeypatch, options, user_in, expected):
        mock_user_input(monkeypatch, user_in)

        selection, option = get_choice(options)
        assert selection == expected
        assert option == options.get(expected)

    # todo update test to fit project
    #   removed the while loop in get choice
    @pytest.mark.skip
    @pytest.mark.parametrize("user_in, expected", [
        ('10\n1\n', 1), ('-1\n2\n', 2), ('0\n3\n', 3)
    ])
    def test_handle_player_input_not_an_option(self, monkeypatch, capsys, options, user_in, expected):
        # setup
        mock_user_input(monkeypatch, user_in)
        selection, option = get_choice(options)
        # Capture the output
        captured = capsys.readouterr()

        # Notice: the \n at the end of the capture is due to the user entering the input.
        user_expected_wrong_input_prompt = (f"\nPlease choose a move from:\n"
                                            + "\n".join(
                    f"{k}: {v}" for k, v in options.items()
                ) + "\n")

        # assert
        assert captured.out == user_expected_wrong_input_prompt
        assert selection == expected
        assert option == options.get(expected)

    @pytest.mark.parametrize("user_in, expected", [
        ("q", 'q'),
        ("1213\n0\nq\n", 'q')
    ])
    def test_user_can_end_choosing_moves(self, monkeypatch, options, capsys, user_in, expected):
        # setup
        mock_user_input(monkeypatch, user_in)
        selection, option = get_choice(options)
        captured = capsys.readouterr()

        assert selection == expected
        assert option == options.get(expected)
        assert "Quitting the game." in captured.out

    @pytest.mark.parametrize("user_in, expected", [
        ("\nq", 'q'),
        ("~\n1213\n0\nq\n", 'q'),
        ("abc\n1", 1),
        ("1 1\n2", 2),
    ])
    def test_handle_invalid_user_input(self, monkeypatch, capsys, options, user_in, expected):
        # setup
        mock_user_input(monkeypatch, user_in)
        selection, option = get_choice(options)

        assert selection == expected
        assert option == options.get(expected)

    def test_cli_generates_correct_dict_from_moves(self, board_setup):
        moves, prompt = get_moves_and_prompt(board_setup)

        parsed = parse_prompt(prompt)
        moves_to_dict = moves_dto_to_dict(moves)

        assert parsed == moves_to_dict

    # todo
    @pytest.mark.parametrize("user_in, src_expected,tar_expected", [
        ("1", "a13", "a24"),
        ("2", "a13", "a22"),
        ("3", "a33", "a44"),
        ("4", "a33", "a42")
    ])
    def test_board_interprets_move_dto_from_user_choice(
            self, board_setup, monkeypatch, capsys, user_in, src_expected,
            tar_expected):
        """
        Test that the board accurately interprets user-selected moves by verifying
        the source and target cells for each choice.

        This test ensures that:
        - The chosen move (obtained from `get_choice`) matches the user-selected option.
        - The parsed prompt data accurately reflects the initial move list.
        - The source and target cells extracted from the move match expected values.
        """
        # Arrange
        moves, prompt = get_moves_and_prompt(board_setup)
        parsed = parse_prompt(prompt)
        moves_to_dict = moves_dto_to_dict(moves)

        # Act
        mock_user_input(monkeypatch, user_in)
        selection, option = get_choice(moves_to_dict)
        chosen_move = moves_to_dict.get(selection)
        src_actual, tar_actual = extract_src_target_names(chosen_move)

        # Assert
        # Ensures user-selected move is correct
        assert chosen_move == option
        # Ensures prompt parsing is accurate
        assert chosen_move == parsed.get(selection)
        assert (src_actual, tar_actual) == (src_expected, tar_expected)

    @pytest.mark.parametrize("user_in, src_expected,tar_expected", [
        ("1", "a13", "a24"),
        ("2", "a13", "a22"),
        ("3", "a33", "a44"),
        ("4", "a33", "a42")
    ])
    def test_board_executes_selected_move_correctly(
            self, board_setup, monkeypatch, capsys, user_in, src_expected,
            tar_expected):
        """
        Tests that the board correctly executes a move selected by the user,
        moving a piece from the source cell to the target cell.
        """
        # Arrange
        moves, prompt = get_moves_and_prompt(board_setup)
        moves_to_dict = moves_dto_to_dict(moves)
        mock_user_input(monkeypatch, user_in)
        src_actual, tar_actual = extract_move_chosen_by_user(moves_to_dict)

        src_cell = get_cell_by_name(board_setup, src_actual)
        tar_cell = get_cell_by_name(board_setup, tar_actual)

        # assert initial piece placement from the user prompt and board
        assert_initial(src_cell, src_expected, tar_cell)

        # Act: execute move on board from user's move selection
        board_setup.move_piece(src_actual, tar_actual)

        # assert piece placement after move execution
        assert_final_state(src_cell, tar_cell, tar_expected)

    # todo
    # @pytest.mark.parametrize("user_in, src_expected,tar_expected", [
    #     ("1", "a13", "a24"),
    #     ("2", "a13", "a22"),
    #     ("3", "a33", "a44"),
    #     ("4", "a33", "a42")
    # ])
    # todo
    def test_execute_capture(self, board_setup, monkeypatch):
        pieces = [
            (P.P1.name, "a13"), (P.P1.name, "a33"), (P.P2.name, "a22"),
        ]
        moves, prompt = get_moves_and_prompt(board_setup, pieces)


        moves_to_dict = moves_dto_to_dict(moves)
        user_in = "1"
        mock_user_input(monkeypatch, user_in)
        src, tar = extract_move_chosen_by_user(moves_to_dict)
        src_cell = get_cell_by_name(board_setup, src)
        tar_cell = get_cell_by_name(board_setup, tar)
        final_cell = get_cell_by_name(board_setup, "a31")
        assert src_cell.has_piece()
        assert tar_cell.has_piece()

        board_setup.move_piece(src, tar)
        assert not src_cell.has_piece()
        assert not tar_cell.has_piece()
        assert final_cell.has_piece()
        # todo
        #       setup board
        #       set capture moves
        #   see that it gets executed?

        pass

    # todo
    @pytest.mark.skip
    def test_board_can_get_chosen_move_by_user(self, board_setup, monkeypatch):
        # todo
        #   setup board
        #   setup mock user choice
        #   get user input
        #   fine the move state to choose
        #   execute somehow?

        # setup
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, "a13")
        setup_piece_on_cell_by_name_and_owner(board_setup, P.P1.name, "a33")
        mock_user_input(monkeypatch, "1")
        moves = board_setup.get_available_moves()
        prompt = board_setup.get_user_moves_prompt(moves)
        moves_to_dict = moves_dto_to_dict(moves)

        selection, option = get_choice(moves_to_dict)
        # todo del
        print("#$$#*#*#*#\nmoves: ", moves)
        print(prompt)
        print("to dict", moves_to_dict)
        print("selection, options", selection, option)
        pass

    # todo
    def test_user_can_quit_the_game(self):
        pass

    # todo
    def test_user_move_execution(self):
        pass

    # todo
    def test_user_capture_move_execution(self):
        pass

    # todo
    def test_can_see_on_prompt_target_and_final_src_display(self):
        pass

    # todo
    def test_user_can_view_available_options_from_board(self):
        pass


class TestGameState:
    # todo
    def test_can_undo_action(self):
        pass

    # todo
    def test_game_start_and_exit(self):
        pass

    # todo
    def test_when_opponent_cannot_move_its_a_win(self):
        pass

    # todo
    #       when oppent has no moves its a win
    def test_game_end_when_no_moves_possible(self):
        pass
