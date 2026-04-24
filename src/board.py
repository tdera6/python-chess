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
    
    def setup_starting_position(self):
        # Set up the initial position of pieces on the board
        self.squares[0] = self.WHITE_ROOK
        self.squares[1] = self.WHITE_KNIGHT
        self.squares[2] = self.WHITE_BISHOP
        self.squares[3] = self.WHITE_QUEEN
        self.squares[4] = self.WHITE_KING
        self.squares[5] = self.WHITE_BISHOP
        self.squares[6] = self.WHITE_KNIGHT
        self.squares[7] = self.WHITE_ROOK

        for i in range(16, 24):
            self.squares[i] = self.WHITE_PAWN

        for i in range(96, 104):
            self.squares[i] = self.BLACK_PAWN

        self.squares[112] = self.BLACK_ROOK
        self.squares[113] = self.BLACK_KNIGHT
        self.squares[114] = self.BLACK_BISHOP
        self.squares[115] = self.BLACK_QUEEN
        self.squares[116] = self.BLACK_KING
        self.squares[117] = self.BLACK_BISHOP
        self.squares[118] = self.BLACK_KNIGHT
        self.squares[119] = self.BLACK_ROOK