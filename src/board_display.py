from board_state import BoardState  # Import the BoardState DTO


class BoardDisplay:
    def __init__(self, board_state: BoardState):
        self.board_state = board_state

    def construct_printable_board(self) -> str:
        """
        Generate a visual representation of the current board state as a string.

        The output includes column headers, row numbers, and borders for each cell.

        Returns:
            str: A formatted string representing the current state of the board.
        """
        cells = self.board_state.cells
        columns = len(cells[0])

        # Construct the entire board representation
        return self.generate_board_representation(cells, columns)

    def generate_board_representation(
            self, cells: list, columns: int
    ) -> str:
        """
        Generate the entire board representation, including headers, rows, and borders.

        Args:
            cells (list): A 2D list representing the board cells.
            columns (int): The number of columns in the board.

        Returns:
            str: A formatted string representing the current state of the board.
        """
        # Construct column headers and top border
        column_headers = self.generate_column_headers(columns)
        top_border = self.generate_border(columns) + "\n"

        # Generate board rows
        board_rows = self.construct_board_rows(cells)

        # Append the bottom border
        bottom_border = self.generate_border(columns)

        # Combine all parts of the board
        return column_headers + top_border + board_rows + bottom_border

    @staticmethod
    def generate_column_headers(columns: int) -> str:
        """
        Generate the column headers for the board.

        Args:
            columns (int): The number of columns.

        Returns:
            str: A formatted string representing the column headers.
        """
        return "   " + " ".join(f" {chr(ord('a') + i)} " for i in range(columns)) + "\n"

    @staticmethod
    def generate_border(columns: int) -> str:
        """
        Generate a border for the board.

        Args:
            columns (int): The number of columns.

        Returns:
            str: A formatted string representing a border.
        """
        return "  +" + "---+" * columns

    @staticmethod
    def construct_board_rows(cells: list) -> str:
        """
        Construct the rows of the board.

        Args:
            cells (list): A 2D list representing the board cells.

        Returns:
            str: A formatted string representing the rows of the board.
        """
        rows_list = []
        columns = len(cells[0])

        for i, row in enumerate(cells):
            # Construct the row string (e.g., "1 | X | O | ...")
            current_row_str = f"{i + 1} |" + "".join(f" {cell.display()} |" for cell in row)
            rows_list.append(current_row_str)

            # Append horizontal separator, except after the last row
            if i < len(cells) - 1:
                rows_list.append(BoardDisplay.generate_border(columns))

        # Join all parts of the rows into a single string
        return "\n".join(rows_list) + "\n"
