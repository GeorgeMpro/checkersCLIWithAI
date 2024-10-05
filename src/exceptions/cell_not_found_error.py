class CellNotFoundError(Exception):
    def __init__(self, message="Cannot find cell name"):
        super().__init__(message)
