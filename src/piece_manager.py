from cell import Cell
from piece import Piece
from utils import increment_index, is_even


class PieceManager:
    def __init__(self):
        pass

    @staticmethod
    def put_piece_on_cell_by_name(cell: Cell, piece_owner):
        piece = Piece(piece_owner)
        cell.set_piece(piece)

    @staticmethod
    def move_piece_to_cell(source_cell: Cell, target_cell: Cell):
        piece = source_cell.piece
        target_cell.set_piece(piece)
        source_cell.remove_piece_reference()

    def initial_piece_setup(self, state):
        """
            Sets up the initial positions for players one and two.

            Player one occupies the cells in rows 1 to 3, and player two occupies the cells in rows 6 to 8.
            Pieces are placed on dark squares starting at a11 in a checkers pattern.
            :param state:
            """

        initial_cells = self.generate_initial_setup_cells_and_piece_owners(state)

        for cell_name, piece_owner in initial_cells:
            cell = state.cell_map[cell_name]
            self.put_piece_on_cell_by_name(cell, piece_owner)

    @staticmethod
    def generate_initial_setup_cells_and_piece_owners(state) -> list[tuple[str, str]]:
        """
        Generates a list of initial setup cells and their respective owners.

        Args:
            state: An instance of InitialBoardState containing board setup information.

        Returns:
            A list of tuples, where each tuple contains the cell name (e.g., "a11")
            and the owner of the piece ("p1" or "p2").
        """
        initial_rows_to_fill = 3
        number_of_rows = increment_index(state.rows)
        player_two_row_start_index = increment_index(state.rows) - initial_rows_to_fill

        # Generate initial cells for player one and player two
        initial_cells = [
                            (f"a{i}{j}", "p1") for i in range(1, initial_rows_to_fill + 1)
                            for j in range(1, number_of_rows) if is_even(i, j)
                        ] + [
                            (f"a{i}{j}", "p2") for i in range(player_two_row_start_index, number_of_rows)
                            for j in range(1, number_of_rows) if is_even(i, j)
                        ]

        return initial_cells
