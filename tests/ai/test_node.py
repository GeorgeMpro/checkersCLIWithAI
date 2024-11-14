import pytest

from ai.node_generator import Node, NodeGenerator, Path
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

    def test_setup_root_node_from_data(self, board, hs):
        setup_board(board, [
            (p1, "a11"), (p1, "a13"), (p2, "a33")
        ])
        map_copy, game_copy = hs._get_cell_map_and_game_copies()
        hs._setup_board_copy_state(game_copy, map_copy)
        expected_moves = hs._generate_move_pairs(
            hs._get_available_player_moves()
        )

        node = hs.generate_root_node(game_copy)
        assert node.score == 10
        assert node.player == board.game.current_player.name

        for move, expected_move in zip(node.moves, expected_moves):
            assert move == expected_move  # Assumes equality is implemented for MoveState

    def test_generate_children_nodes(self, board, hs):
        # todo move has a11, and a13
        move_1 = [
            ("a11", "a22"), ("a13", "a22"), ("a13", "a24")
        ]
        move_2 = [("a66", "a55")]
        move_3 = [("a22", "a31"), ("a22", "a31"), ("a13", "a22"), ("a13", "a24")]
        move_4 = [("move", "4")]
        ng = NodeGenerator()
        root_node = Node(20, "p1", move_1)
        ng.root_node = root_node

        child_1 = Node(10, "p2", move_2)
        child_2 = Node(15, "p2", move_2)
        child_3 = Node(5, "p2", move_2)
        root_node.add_child(move_1[0], child_1)
        root_node.add_child(move_1[1], child_2)
        root_node.add_child(move_1[2], child_3)

        child_1_1 = Node(5, "p1", )
        child_1.add_child(move_3[0], child_1_1)

        child_2_1 = Node(7, "p1", )
        child_2.add_child(move_3[1], child_2_1)

        child_3_1 = Node(8, "p1", )
        child_3.add_child(move_3[2], child_3_1)

        print(f"\nROOT:\n{ng.root_node.moves=}\n{ng.root_node.children=}")
        path = ng.dfs_path()

        created = [
            Path(depth=0, move=None, score=20, current_player='p1',
                 moves=[('a11', 'a22'), ('a13', 'a22'), ('a13', 'a24')]),
            Path(depth=1, move=('a11', 'a22'), score=10, current_player='p2', moves=[('a66', 'a55')]),
            Path(depth=1, move=('a13', 'a22'), score=15, current_player='p2', moves=[('a66', 'a55')]),
            Path(depth=1, move=('a13', 'a24'), score=5, current_player='p2', moves=[('a66', 'a55')]),
            Path(depth=2, move=('a66', 'a55'), score=5, current_player='p1', moves=[]),
            Path(depth=2, move=('a66', 'a55'), score=7, current_player='p1', moves=[]),
            Path(depth=2, move=('a66', 'a55'), score=8, current_player='p1', moves=[])
        ]

        sorted_actual_path = sorted(path)
        sorted_expected_path = sorted(created)
        # todo del
        for p in sorted_actual_path:
            print(f"\n{p}")

        # Assert path elements individually
        for actual, expected in zip(sorted_actual_path, sorted_expected_path):
            assert actual.depth == expected.depth
            assert actual.move == expected.move
            assert actual.score == expected.score
            assert actual.current_player == expected.current_player
            assert actual.moves == expected.moves

        # Ensure correct relationships
        assert root_node.children[("a11", "a22")].score == 10
        print(f"\n{child_1.children=}")
        assert child_1.children[('a22', 'a31')].score == 5

    # todo ?
    def test_can_spot_leaf_node(self):
        pass

    # TODO
    #   can connect nodes by moves - node points at another via move pair
    #       root- children - leafs
    #   ? add move:score - get the score after making the move
    #   ? add depth?
    #   can traverse root and children nodes
    #   can generate node while exploring
    #       score, moves, player ( add something?)
    #   can traverse nodes that were generated during exploration
    #   can sum/ find most or least node per level (?)
    #   can sum a whole path leaf -> root
    #   can present sum of whole path

    # TODO begin memoization.

    # todo
    def test_can_score_on_moves(self, board):
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

    #     todo integration
    #       connect each move execution in hs to node creation
    #       check doesn't generate node when running on empty ( no more moves/win) but not max depth
    #


class TestMemoization:
    # TODO memoization
    #   hash the cell_map
    #   get the score
    #   enter a dict with cell_map hash : score
    #   before each eval - look up in the dict

    # todo
    def test_can_hash_state(self):
        pass
