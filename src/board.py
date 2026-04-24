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

    WHITE_PAWN = PAWN * WHITE
    BLACK_PAWN = PAWN * BLACK
    WHITE_KNIGHT = KNIGHT * WHITE
    BLACK_KNIGHT = KNIGHT * BLACK
    WHITE_BISHOP = BISHOP * WHITE
    BLACK_BISHOP = BISHOP * BLACK
    WHITE_ROOK = ROOK * WHITE
    BLACK_ROOK = ROOK * BLACK
    WHITE_QUEEN = QUEEN * WHITE
    BLACK_QUEEN = QUEEN * BLACK
    WHITE_KING = KING * WHITE
    BLACK_KING = KING * BLACK

    def __init__(self):
        self.squares = [self.EMPTY] * 128

        self.turn = self.WHITE
    