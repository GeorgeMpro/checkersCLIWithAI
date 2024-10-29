import pytest

from component.game import P
from conftest import setup_piece_on_cell_by_name_and_owner, p1, p2
from main import GamePlay
from test_user_interaction import mock_user_input


@pytest.fixture
def game_instance(board=None):
    game = GamePlay()
    if board is not None:
        game.board = board
    return game


class TestGameState:
    # todo

    def test_can_undo_action(self):
        pass

    def test_game_exit(self, monkeypatch, game_instance, capsys):
        game_quit_msg = "Quitting the game."
        mock_user_input(monkeypatch, "q")
        game_instance.init_game()
        game_instance.game_loop()
        captured = capsys.readouterr()

        assert game_quit_msg in captured.out

    # todo clean and add p2
    def test_when_opponent_cannot_move_is_a_win(self, board_setup):
        p1 = P.P1.name
        p2 = P.P2.name
        p1_src = "a11"
        p2_src = "a22"
        p2_src_also = "a33"

        setup_piece_on_cell_by_name_and_owner(board_setup, p1, p1_src)
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, p2_src)
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, p2_src_also)
        moves = board_setup.get_available_moves()
        board_setup.is_game_end(moves, None)

        assert moves == []
        assert board_setup.is_game_over()
        assert board_setup.game.winner == P.P2

    # todo
    def test_when_no_moves_game_loop_end(self, board_setup, capsys, game_instance):
        setup_piece_on_cell_by_name_and_owner(board_setup, p1, "a11")
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, "a22")
        setup_piece_on_cell_by_name_and_owner(board_setup, p2, "a33")
        possible_moves = board_setup.get_available_moves()
        game_instance.board = board_setup
        game_instance.game_loop()

        assert possible_moves == []
        assert board_setup.game.winner == P.P2
        end_message = "Player O wins!"
        assert end_message in capsys.readouterr().out
        pass

    # todo
    def test_opponent_no_pieces_is_game_end_and_win(self, board_setup, game_instance, capsys):
        end_message = "Player X wins!"
        setup_piece_on_cell_by_name_and_owner(board_setup, p1, "a11")
        possible_moves = board_setup.get_available_moves()
        game_instance.board = board_setup
        game_instance.game_loop()

        assert possible_moves
        assert board_setup.game.winner == P.P1
        assert end_message in capsys.readouterr().out

        pass

    # todo
    def test_can_keep_track_of_turns(self):
        pass

    # todo
    def test_can_undo_player_turn(self):
        pass
