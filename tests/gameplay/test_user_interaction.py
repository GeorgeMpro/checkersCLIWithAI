from io import StringIO

import pytest

from component.cell import Cell
from conftest import setup_board, setup_piece_on_cell_by_name_and_owner, get_cell_by_name, board_setup, p1, p2
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
            (p1, "a13"), (p1, "a33"), (p2, "a77"),
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
    assert tar_cell.name == tar_expected


def assert_initial(
        src_cell: Cell, src_expected: str, tar_cell: Cell
) -> None:
    assert src_cell.has_piece()
    assert not tar_cell.has_piece()
    assert src_cell.name == src_expected


class TestGameInteraction:
    import pytest

    @pytest.mark.parametrize("pieces, expected", [
        (
                [(p1, "a11"), (p1, "a17"),
                 (p2, "a73"), (p2, "a88")],
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
        actual = board_setup.get_available_moves()
        assert actual == expected[:2]  # Check for Player 1's expected moves

        # Toggle turn and get available moves for Player 2
        board_setup.game.toggle_player_turn()
        actual_p2 = board_setup.get_available_moves()
        assert actual_p2 == expected[2:]  # Check for Player 2's expected moves

    @pytest.mark.parametrize("pieces, expected", [
        ([(p1, "a11"), (p1, "a17")],
         [MoveState("a11", ["a22"]),  # P1 available moves
          MoveState("a17", ["a28", "a26"])]
         )])
    def test_can_present_available_moves_for_player(self, board_setup, pieces, expected):
        setup_board(board_setup, pieces)
        board_setup.game.get_turn()
        actual = board_setup.get_available_moves()

        assert actual == expected

    @pytest.mark.parametrize("pieces, expected", [
        ([(p1, "a11"), (p1, "a17"),
          (p2, "a22")],
         [MoveState("a11", ["a22"], True, [captures("a22", "a33")])]  # P1 available moves
         )])
    def test_can_present_available_moves_for_player(self, board_setup, pieces, expected):
        setup_board(board_setup, pieces)
        actual = board_setup.get_available_moves()
        actual_prompt = board_setup.get_user_moves_prompt(actual)
        expected_prompt = "[1] a11 -> a22 -> a33"

        assert actual == expected
        assert actual_prompt == expected_prompt

    @pytest.mark.parametrize("user_in, expected", [
        ("1", 1), ("2", 2), ("3", 3)
    ])
    def test_player_can_choose_action(self, monkeypatch, options, user_in, expected):
        mock_user_input(monkeypatch, user_in)

        selection, option = get_choice(options)
        assert selection == expected
        assert option == options.get(expected)

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
        assert user_expected_wrong_input_prompt in captured.out
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

    @pytest.mark.usefixtures("suppress_stdout")
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
    #   expand to different parameters?
    def test_execute_capture(self, board_setup, monkeypatch):
        pieces = [
            (p1, "a13"), (p1, "a33"), (p2, "a22"),
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
    def test_can_see_on_prompt_target_and_final_src_display(self):
        pass


class TestPresentingIllegalMoves:

    @pytest.mark.parametrize("src_name,tar_name,final_name", [
        ("a42", "a51", "a60"),
        ("a73", "a82", "a91"),
        ("a77", "a88", "a99"),
    ])
    def test_does_not_present_capture_final_out_of_bounds(
            self, board_setup, src_name, tar_name, final_name
    ):
        invalid_move_prompt = src_name + " -> " + tar_name
        setup_piece_on_cell_by_name_and_owner(board_setup, p1, src_name)
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, tar_name)

        moves = board_setup.get_available_moves()
        prompt = board_setup.get_user_moves_prompt(moves)

        assert prompt != "[1] " + src_name + " -> " + tar_name + " -> " + final_name
        assert invalid_move_prompt not in prompt

    # todo
    #   add parameters
    def test_does_not_present_blocked_capture(self, board_setup):
        setup_piece_on_cell_by_name_and_owner(board_setup, p1, "a13")
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, "a24")
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, "a35")

        moves = board_setup.get_available_moves()
        prompt = board_setup.get_user_moves_prompt(moves)

        assert prompt != "[1] a13 -> a24 -> a35"
        assert "a13 -> a24" not in prompt

    # todo !
    def test_handles_chain_capture_only_display(self, board_setup):
        """
        Assert that when a piece is in chain capture only its moves are available to user.
        """
        # the path we DO NOT take
        path_not_taken = "a17 -> a26 -> a35"
        path_take = "a11 -> a22 -> a33"

        # path 1
        setup_piece_on_cell_by_name_and_owner(board_setup, p1, "a11")
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, "a22")
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, "a42")

        # path 2
        setup_piece_on_cell_by_name_and_owner(board_setup, p1, "a17")
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, "a26")

        # all available moves
        moves = board_setup.get_available_moves()
        possible_move_prompt = board_setup.get_user_moves_prompt(moves)
        assert path_take in possible_move_prompt
        assert path_not_taken in possible_move_prompt

        # move to a chained capture
        board_setup.move_piece("a11", "a22")
        moves = board_setup.get_available_moves()
        possible_move_prompt = board_setup.get_user_moves_prompt(moves)
        path_chained = "a33 -> a42 -> a51"
        chaining_cell_name = board_setup.game.chaining_cell_name

        assert chaining_cell_name == "a33"
        assert path_chained in possible_move_prompt
        assert path_not_taken not in possible_move_prompt

        # both moves available after chain and captures
        board_setup.move_piece("a33", "a42")
        board_setup.move_piece("a17", "a26")
        moves = board_setup.get_available_moves()
        prompt = board_setup.get_user_moves_prompt(moves)
        expected_end = ["[1] a35 -> a46",
                        "[2] a35 -> a44",
                        "[3] a51 -> a62"]
        for option in expected_end:
            assert option in prompt
