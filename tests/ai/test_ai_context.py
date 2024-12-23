import pytest

from ai.ai_context_manager import AIContextManager
from ai.heuristic_explorer import HeuristicExplorer
from conftest import board_setup
from exceptions.illegal_move_error import IllegalMoveError


class TestAIContext:

    def test_ai_context_manager(self, board_setup):
        board = board_setup

        assert not board_setup.is_ai

        with AIContextManager(board) as ai_context:
            assert ai_context.is_ai

        assert not board_setup.is_ai

    def test_ai_context_manager_error_handling(self, board_setup):
        board = board_setup
        with pytest.raises(IllegalMoveError):
            with AIContextManager(board):
                raise IllegalMoveError

        assert not board.is_ai

        with pytest.raises(Exception):
            with AIContextManager(board):
                raise Exception

        assert not board.is_ai

    def test_board_uses_ai_cell_man_in_context(self, board_setup):
        board = board_setup

        HeuristicExplorer(board)

        assert board.get_board() == board.cell_manager.get_board()

        with AIContextManager(board) as ai_context:
            assert ai_context.get_board() == board._ai_cell_manager.get_board()
