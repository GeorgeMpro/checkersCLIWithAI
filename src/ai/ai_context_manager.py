from board import Board


class AIContextManager:
    """
    A context manager that enables AI-specific context within the Board,
    allowing AI classes to perform heuristic exploration and simulations
    without impacting the main game state.

    During the `with` block, `is_ai` is set to True on the provided Board
    instance, directing the Board to use AI-specific resources. Upon
    exiting the `with` block, `is_ai` is reset to False, returning
    operations to the main game context.

    This structure provides temporary AI access to necessary fields,
    ensuring that exploratory operations remain isolated from the main
    game state.
    """

    def __init__(self, board: Board):
        self.board = board

    def __enter__(self):
        self.board.is_ai = True
        return self.board

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.board.is_ai = False