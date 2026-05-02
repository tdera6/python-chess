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

    
    def load_FEN(self, fen: str):

        # Clear board
        self.squares = [0] * 128

        fen_split = fen.split(" ")
        
        board_position = fen_split[0]
        player_turn = fen_split[1]

        # Set player turn
        self.turn = self.WHITE if player_turn == 'w' else self.BLACK

        all_rows = board_position.split('/')

        fen_pieces = {
            'P': Board.WHITE_PAWN,
            'N': Board.WHITE_KNIGHT,
            'B': Board.WHITE_BISHOP,
            'R': Board.WHITE_ROOK,
            'Q': Board.WHITE_QUEEN,
            'K': Board.WHITE_KING,
            'p': Board.BLACK_PAWN,
            'n': Board.BLACK_KNIGHT,
            'b': Board.BLACK_BISHOP,
            'r': Board.BLACK_ROOK,
            'q': Board.BLACK_QUEEN,
            'k': Board.BLACK_KING
        }

        # Load pieces

        row = 7
        for row_str in all_rows:
            column = 0
            for sign in row_str:
                if sign.isdigit():
                    column += int(sign)
                else:
                    square = 16 * row + column
                    piece = fen_pieces[sign]
                    self.squares[square] = piece
                    column += 1
            row -= 1