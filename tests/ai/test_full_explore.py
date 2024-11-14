import pytest

from ai.ai_context_manager import AIContextManager
from ai.heuristic_explorer import HeuristicExplorer
from board import Board
from component.game import P
from component.piece import Piece
from conftest import p1, p2, setup_board


def assert_game_state(board, player, name_src, available_moves, targets):
    assert board.game.current_player == player
    moves_prompt = board.get_user_moves_prompt(board.get_available_moves(p1))
    for src in name_src:
        assert board.cell_manager.get_cell_by_name(src).piece
    for target in targets:
        assert not board.cell_manager.get_cell_by_name(target).piece
    for move in available_moves:
        assert move in moves_prompt


def assert_state_after_ai(
        ai_context, name_src, next_moves, origin_moves, targets
):
    assert ai_context.game.current_player == P.P2

    p1_moves_prompt = ai_context.get_user_moves_prompt(ai_context.get_available_moves(p1))

    # assert that one of the sources is empty ( when multiple source options)
    assert any(
        ai_context.cell_manager.get_cell_by_name(src).piece is None for src in name_src
    )
    # does not look at specific move that was executed but that one of them was executed

    # todo
    assert any(
        ai_context.cell_manager.get_cell_by_name(target).piece for target in targets
    )

    # least one of the original moves is not in the prompt
    assert any(move not in p1_moves_prompt for move in origin_moves)

    assert any(
        move in p1_moves_prompt for move in next_moves
    )


def get_piece_by_name(
        board: Board, name: str
) -> Piece:
    return board.cell_manager.get_cell_by_name(name).piece


class TestFullExplore:
    # todo
    #   Notice: board display does not work correctly on ai board

    def test_separate_copy_generation(self, board, hs):
        assert board.game is not board._ai_game
        assert board._ai_cell_manager is not board.cell_manager

        map_copy, game_copy = hs._get_cell_map_and_game_copies()
        assert board.game is not game_copy
        assert board.cell_manager.cell_map is not map_copy

    @pytest.mark.parametrize(
        "pieces, expected_move_count",
        [
            # Example cases with pieces and the expected number of moves
            ([(p1, "a11"), (p2, "a88")], 1),
            ([(p1, "a17"), (p2, "a88")], 2),
            ([(p1, "a17"), (p2, "a88")], 3),
        ]
    )
    def test_generate_correct_number_of_unique_copies(self, board, pieces, expected_move_count):
        # setup
        setup_board(board, pieces)
        hs = HeuristicExplorer(board)

        copies_created = hs._generate_state_copies(expected_move_count)

        assert all(
            game_copy is not board.game and map_copy is not board.cell_manager.cell_map
            for game_copy, map_copy in copies_created
        ), "Each copy should be distinct from the main game and cell map"

        assert all(
            game1 is not game2 and map1 is not map2
            for (game1, map1), (game2, map2) in zip(copies_created, copies_created[1:])
        ), "Each game and map copy should be unique from each other"

    @pytest.mark.parametrize(
        "pieces,sources, targets,origin_moves,next_moves",
        [
            # one source and 1 moves
            ([(p1, "a11"), (p2, "a88")],
             ["a11"],
             ["a22"],
             ["a11 -> a22"],
             ["a22 -> a31", "a22 -> a33"]),
            # one source and 2 move
            ([(p1, "a17"), (p2, "a88")],
             ["a17"], ["a26", "a28"],
             ["a17 -> a26", "a17 -> a28"],
             ["a26 -> a35", "a26 -> a37"]),
            # two sources and 3 move
            ([(p1, "a11"), (p1, "a17"), (p2, "a88")],
             ["a11", "a17"], ["a22", "a26", "a28"],
             ["a11 -> a22", "a17 -> a26", "a17 -> a28"],
             ["a26 -> a35", "a26 -> a37", "a22 -> a31", "a22 -> a33"]),
        ])
    def test_can_execute_moves_on_copy(
            self, board: Board, hs: HeuristicExplorer, pieces: list[tuple[str, str]], sources: list[str],
            targets: list[str],
            origin_moves: list[str], next_moves: list[str]
    ):
        setup_board(board, pieces)

        # Action
        hs.ai_execute_available_moves()

        # Assertions after moving on copy
        # assert main stayed the same
        assert board.game is not board._ai_game
        assert_game_state(
            board, P.P1, sources, origin_moves, targets
        )

        # assert copy has performed action
        with AIContextManager(board) as ai_context:
            assert_state_after_ai(
                ai_context, sources, next_moves, origin_moves, targets
            )

    # todo
    def test_can_execute_several_moves_on_copy(
            self, board, hs
    ):
        # setup
        p1_src = "a11"
        p1_tar = "a22"
        p2_src = "a88"
        p2_tar = "a77"
        pieces = [(p1, p1_src), (p2, p2_src)]
        setup_board(board, pieces)
        hs.ai_execute_available_moves(0, 2)

        assert board.game is not board._ai_game
        assert board.cell_manager.cell_map is not board._ai_cell_manager.cell_map
        # main state
        assert get_piece_by_name(board, p1_src)
        assert get_piece_by_name(board, p2_src)
        # ai state
        with AIContextManager(board) as ai_context:
            assert ai_context.cell_manager.cell_map is board._ai_cell_manager.cell_map
            assert ai_context.game is board._ai_game

            # assert the first move on copy
            assert not get_piece_by_name(ai_context, p1_src)
            assert get_piece_by_name(ai_context, p1_tar)

            # assert second move on copy
            assert not get_piece_by_name(ai_context, p2_src)
            assert get_piece_by_name(ai_context, p2_tar)
            # assert correct game state
            assert ai_context.game.current_player == P.P1
            assert ai_context.game.turn_counter == 2

        #     todo del
        hs.ai_execute_available_moves(0, )
        # todo

    # todo, check nothing?
    @pytest.mark.skip
    def test_explore_stops_at_game_end(self, board, hs):
        setup_board(board, [
            (p1, "a11"), (p2, "a22")
        ])
        hs.ai_execute_available_moves(0, 100)
        with AIContextManager(board) as ai_context:
            print(f"player: {ai_context.game.current_player}")
            print(f"turn: {ai_context.game.turn_counter}")
            print(f"is win: {ai_context.game.is_game_over}")
            cells = ai_context.cell_manager.cell_map
            ai_context.game.is_game_over = True
            for cell in cells.values():
                if pp := cell.piece:
                    print(f"piece: {cell.name} {pp}")

    def test_stop_on_depth_limit(self):
        # todo - check game counter
        pass

    # todo
    def test_can_verify_which_player_moves(self):
        pass

        # todo
        #   get all moves
        #   generate all moves
        #   get game and cell map copy
        #   exectue each move on copy
        #   get stuff for node
        #   generate node
        #   connect root to children

        pass
