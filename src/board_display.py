from board_state import BoardState  # Import the BoardState DTO


class BoardDisplay:
    def __init__(self, board_state: BoardState):
        self.board_state = board_state

    def print_board_to_player(self) -> str:
        """
            Generate a visual representation of the current board state as a string.

            The output includes column headers, row numbers, and borders for each cell.

            Returns:
                str: A formatted string representing the current state of the board.
        """
        cells = self.board_state.cells
        columns = len(cells[0])

        # Construct column headers (e.g. "a b c..."
        column_headers = "   " + " ".join(f" {chr(ord('a') + i)} " for i in range(columns)) + "\n"

        # Construct top border
        top_border = "  +" + "---+" * columns + "\n"

        # stage: board with headers and top border
        board_str = column_headers + top_border

        # Construct rows of the board
        for i, row in enumerate(cells):
            # Row number on the left
            row_str = f"{i + 1} |"
            for cell in row:
                cell_display = cell.display()
                row_str += f" {cell_display} |"

            board_str += row_str + "\n"

            # Append horizontal separator, except after the last row
            if i < len(cells) - 1:
                board_str += "  +" + "---+" * columns + "\n"

        bottom_border = "  +" + "---+" * columns + "\n"
        board_str += bottom_border

        return board_str
