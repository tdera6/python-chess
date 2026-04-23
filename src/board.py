class Board:
    
    # Colors
    WHITE = 1
    BLACK = -1

    # Basic pieces
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    def __init__(self):
        self.squares = [self.EMPTY] * 128

        self.turn = self.WHITE
    