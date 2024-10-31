from component.cell import Cell


def eval_player_state(
        player_cells: list[Cell],
        opponent_cells: list[Cell],
        piece_score: int = 10,
        king_modifier: int = 2,
        is_win: bool = False,
        win_score: int = 100
) -> int:
    player_score, opponent_score = _get_scores(player_cells, opponent_cells, piece_score, king_modifier)

    if is_win:
        return win_score + player_score - opponent_score

    return player_score - opponent_score


def _get_scores(player_cells: list[Cell], opponent_cells: list[Cell], piece_score: int,
                king_modifier: int) -> tuple[int, int]:
    player_score = _eval_player_pieces_score(player_cells, piece_score, king_modifier)
    opponent_score = _eval_player_pieces_score(opponent_cells, piece_score, king_modifier)

    return player_score, opponent_score


def _eval_player_pieces_score(
        player_cells: list[Cell], piece_score: int
        , king_modifier: int = 2) -> int:
    """
   Evaluate the state of a player's cells.

   Args:
       player_cells (list[Cell]): List of cells owned by the player.
       piece_score: The score associated with a normal score.
       king_modifier: Score multiplier applied to the king pieces. Defaults to 2.
   Returns:
       tuple[int, int]: Number of pieces and calculated state score.
   """
    number_of_pieces = len(player_cells)
    kings = _get_number_of_kings(player_cells)

    regular_pieces = number_of_pieces - kings

    state_score = _generate_piece_score(regular_pieces, piece_score, kings, king_modifier)

    # todo
    #   remove the number of cells?
    return state_score


def _get_number_of_kings(player_cells: list[Cell]) -> int:
    return sum(
        1 for cell in player_cells
        if cell.is_king()
    )


def _generate_piece_score(
        regular_pieces: int, piece_score: int, kings: int, king_modifier: int
) -> int:
    normal_score = regular_pieces * piece_score
    king_score = kings * piece_score * king_modifier

    return normal_score + king_score
