import pytest

from ai.heuristic_explorer import HeuristicExplorer
from ai.node_generator import Node
from conftest import setup_board, p1, p2
from utils import moves


class TestNode:
    # TODO node
    #   store score, moves, and moves point to next nodes
    #   check for leaf node
    #   parent points to children nodes
    @pytest.mark.parametrize("expected_score, expected_player, expected_moves", [
        (20, p1, []),
        (20, p1, [moves("a11", ["a12"])])
    ])
    def test_node_has_score_player_moves(
            self, expected_score: int, expected_player: str, expected_moves: list):
        node = Node(expected_score, expected_player, expected_moves)

        assert node.score == expected_score
        assert node.player == expected_player
        assert node.moves == expected_moves

    def test_setup_root_node_from_data(self, board_setup):
        board = board_setup
        setup_board(board, [
            (p1, "a11"), (p1, "a13"), (p2, "a33")
        ])
        hs = HeuristicExplorer(board)
        expected_moves = board.cell_manager.generate_available_moves_for_player(
            p1, board.game.chaining_cell_name
        )
        node = hs.generate_root_node()
        assert node.score == 10
        assert node.player == board_setup.game.current_player.name

        for move, expected_move in zip(node.moves, expected_moves):
            assert move == expected_move  # Assumes equality is implemented for MoveState

    # todo
    @pytest.mark.skip
    def test_can_generate_children_nodes(self, board_setup):
        board = board_setup
        setup_board(board, [
            (p1, "a11"), (p1, "a13"), (p2, "a33")
        ])
        hs = HeuristicExplorer(board)
        node = hs.generate_root_node()
        # print(f"{node=}")

    # todo
    def test_can_score_on_moves(self, board_setup):
        # todo
        #   setup + move
        #   score player moves
        #   score opponent
        pass

    def test_can_access_child_nodes_from_parent(self):
        pass

    # todo
    def test_node_is_a_leaf(self):
        pass

    # todo
    def test_can_setup_node_from_ai_context(self):
        pass

    # todo
    def test_can_set_move_node_dict(self):
        pass


class TestMemoization:
    # TODO memoization
    #   hash the cell_map
    #   get the score
    #   enter a dict with cell_map hash : score
    #   before each eval - look up in the dict

    # todo
    def test_can_hash_state(self):
        pass
