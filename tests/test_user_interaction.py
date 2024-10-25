from io import StringIO

import pytest

from display.cli import get_choice
from conftest import setup_board
from component.game import P
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


def mock_user_input(monkeypatch, user_in):
    input_string = StringIO(user_in)
    monkeypatch.setattr('sys.stdin', input_string)


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

    # todo
    @pytest.mark.parametrize("user_in, expected", [
        ("1", 1), ("2", 2), ("3", 3)
    ])
    def test_player_can_choose_action(self, monkeypatch, options, user_in, expected):
        mock_user_input(monkeypatch, user_in)

        selection, option = get_choice(options)
        assert selection == expected
        assert option == options.get(expected)

    # todo
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
        # todo update or keep?
        # user_expected_wrong_input_prompt = f"\nPlease choose a move from:\n{"\n".join(options)}\n"

        user_expected_wrong_input_prompt = f"\nPlease choose a move from:\n" + "\n".join(
            f"{k}: {v}" for k, v in options.items()) + "\n"
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

    # todo
    # @pytest.mark.skip
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
        captured = capsys.readouterr()

        assert selection == expected
        assert option == options.get(expected)

    #     todo
    def test_can_execute_user_command_on_board(self):
        pass


class TestGameState:
    # todo
    def test_can_redo_action(self):
        pass
