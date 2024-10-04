from board_display import BoardDisplay
from board_state import BoardState
from cell import Cell
from piece import Piece


class Board:
    _rows = _columns = 8

    def __init__(self, rows=_rows, columns=_columns):
        """"
    Represents the game board for a checkers game.

    Attributes:
        rows (int): The number of rows on the board.
        columns (int): The number of columns on the board.
        board (list[list[Cell]]): A 2D list representing the cells on the board.
        cell_map (dict): A dictionary mapping cell names to Cell objects for quick lookup.

                The Cell names follow 8*8 matrix convention display a_ij, i,j=1,...,8
                 the +1 to start the values from 1 and not 0
                 [f"a{y + 1}{x + 1}" for x in range(rows)]
                """
        self.rows = rows
        self.columns = columns
        self.board = [
            [Cell(self.increment_index(y), self.increment_index(x)) for x in range(rows)]
            for y in range(columns)]
        # generate a dictionary for O(1) access
        self.cell_map = {cell.name: cell for row in self.board for cell in row}

    def get_cell(self, row, column):
        return self.board[row][column]

    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.rows * self.columns

    def get_column_size(self):
        return self.columns

    def get_row_size(self):
        return self.rows

    def set_up_piece(self, row, column, piece):
        cell = self.get_cell(row, column)
        cell.set_piece(piece)

    def get_cell_by_name(self, name):
        return self.cell_map[name]

    def get_board_state(self) -> BoardState:
        return BoardState(cells=self.board)

    # todo del when done
    # def __str__(self):
    #     board_str = ""
    #     for row in self.board:
    #         board_str += " ".join([cell.name for cell in row]) + "\n"
    #         board_str += " ".join([cell.display() for cell in row]) + "\n"
    # return board_str

    def __str__(self):
        board_state = self.get_board_state()
        display = BoardDisplay(board_state=board_state)
        return display.print_board_to_player()

    def initial_setup(self):
        """
            Sets up the initial positions for players one and two.

            Player one occupies the cells in rows 1 to 3, and player two occupies the cells in rows 6 to 8.
            Pieces are placed on dark squares starting at a11 in a checkers pattern.
            """

        # get the cells and pieces to initialize
        initial_cells = self.generate_initial_setup_cells_and_piece_owners()

        for cell_name, piece_owner in initial_cells:
            self.put_piece_on_cell_by_name(cell_name, Piece(piece_owner))

    def generate_initial_setup_cells_and_piece_owners(self) -> list[tuple[str, str]]:
        """
            Generates a list of initial setup cells and their respective owners.

            Returns:
                A list of tuples, where each tuple contains the cell name (e.g., "a11")
                and the owner of the piece ("p1" or "p2").
            """
        initial_rows_to_fill = 3
        number_of_rows_in_cell_representation = number_of_columns_in_cell_representation = self.increment_index(
            self._rows)
        player_two_row_start_index = number_of_rows_in_cell_representation - initial_rows_to_fill

        initial_cells = [
                            (f"a{i}{j}", "p1") for i in range(1, initial_rows_to_fill + 1) for j in
                            range(1, number_of_columns_in_cell_representation) if
                            self.is_even(i, j)
                        ] + [
                            (f"a{i}{j}", "p2") for i in
                            range(player_two_row_start_index,
                                  number_of_rows_in_cell_representation) for j
                            in
                            range(1, number_of_columns_in_cell_representation) if
                            self.is_even(i, j)
                        ]
        return initial_cells

    @staticmethod
    def is_even(i, j):
        return (i + j) % 2 == 0

    def put_piece_on_cell_by_name(self, cell_name, piece_owner):
        cell = self.get_cell_by_name(cell_name)
        cell.set_piece(piece_owner)

    @staticmethod
    def increment_index(index):
        """
        update index to start at 1 in the name of the cell
        """
        tmp = index + 1
        return tmp
