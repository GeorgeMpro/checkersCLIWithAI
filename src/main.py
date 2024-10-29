from board import Board
from component.game import P
from display.cli import moves_dto_to_dict, extract_move_chosen_by_user
from managers.cell_manager import logger


class GamePlay:
    def __init__(self):
        self._board = Board()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    def init_game(self):
        self.board.initial_setup()

    def game_loop(self):
        while True:
            print(self.board)
            player_moves = self.board.get_available_moves()
            opponent = P.P1.name if self.board.game.current_player == "p1" else P.P2.name
            opponent_pieces = self.board.cell_manager.get_player_cells(opponent)

            if self.board.is_game_end(player_moves, opponent_pieces):
                winner = self.board.game.winner
                player_symbol = winner.symbol
                print(f"\nPlayer {player_symbol} wins!")
                break

            moves_dict = moves_dto_to_dict(player_moves)
            print(self.board.get_user_moves_prompt(player_moves))

            src, tar = extract_move_chosen_by_user(moves_dict)
            if src == "q":
                break
            self.board.move_piece(src, tar)


if __name__ == '__main__':
    game = GamePlay()
    game.init_game()
    game.game_loop()
