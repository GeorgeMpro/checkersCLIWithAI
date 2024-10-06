class IllegalMoveError(Exception):
    def __init__(self, message="Illegal move"):
        super().__init__(message)
