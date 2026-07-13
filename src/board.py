from src.move import Move


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
        self.en_passant_square = None
        self.can_white_short_castle = False
        self.can_white_long_castle = False
        self.can_black_short_castle = False
        self.can_black_long_castle = False
        self.white_king_square = 0x04
        self.black_king_square = 0x74

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
        castling_rights = fen_split[2]
        en_passant_square = fen_split[3]

        # Set castling rights
        if "K" in castling_rights:
            self.can_white_short_castle = True
        if "Q" in castling_rights:
            self.can_white_long_castle = True
        if "k" in castling_rights:
            self.can_black_short_castle = True
        if "q" in castling_rights:
            self.can_black_long_castle = True

        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if en_passant_square != "-":
            self.en_passant_square = (
                int(en_passant_square[1]) - 1
            ) * 16 + columns.index(en_passant_square[0])

        # Set player turn
        self.turn = self.WHITE if player_turn == "w" else self.BLACK

        all_rows = board_position.split("/")

        fen_pieces = {
            "P": Board.WHITE_PAWN,
            "N": Board.WHITE_KNIGHT,
            "B": Board.WHITE_BISHOP,
            "R": Board.WHITE_ROOK,
            "Q": Board.WHITE_QUEEN,
            "K": Board.WHITE_KING,
            "p": Board.BLACK_PAWN,
            "n": Board.BLACK_KNIGHT,
            "b": Board.BLACK_BISHOP,
            "r": Board.BLACK_ROOK,
            "q": Board.BLACK_QUEEN,
            "k": Board.BLACK_KING,
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

        # Find white and black kings
        self.white_king_square = self.squares.index(6)
        self.black_king_square = self.squares.index(-6)

    def make_move(self, move: Move):
        self.squares[move.from_square] = Board.EMPTY

        if move.is_promotion:
            self.squares[move.to_square] = move.promotion_to
        elif move.is_en_passant:
            self.squares[move.to_square] = move.piece_moved

            # Correctly handle en passant for white and black
            direction = 1 if self.turn == Board.WHITE else -1
            self.squares[move.to_square - 16 * direction] = Board.EMPTY
        else:
            self.squares[move.to_square] = move.piece_moved

        # Handle withdrawal of castling rights
        if abs(move.piece_moved) == Board.KING:
            if self.turn == Board.WHITE:
                self.can_white_short_castle = False
                self.can_white_long_castle = False
            else:
                self.can_black_short_castle = False
                self.can_black_long_castle = False

        if move.piece_moved == Board.WHITE_ROOK and move.from_square == 0x00:
            self.can_white_long_castle = False
        elif move.piece_moved == Board.WHITE_ROOK and move.from_square == 0x07:
            self.can_white_short_castle = False
        elif move.piece_moved == Board.BLACK_ROOK and move.from_square == 0x70:
            self.can_black_long_castle = False
        elif move.piece_moved == Board.BLACK_ROOK and move.from_square == 0x77:
            self.can_black_short_castle = False

        if move.piece_captured == Board.WHITE_ROOK and move.to_square == 0x00:
            self.can_white_long_castle = False
        elif move.piece_captured == Board.WHITE_ROOK and move.to_square == 0x07:
            self.can_white_short_castle = False
        elif move.piece_captured == Board.BLACK_ROOK and move.to_square == 0x70:
            self.can_black_long_castle = False
        elif move.piece_captured == Board.BLACK_ROOK and move.to_square == 0x77:
            self.can_black_short_castle = False

        # Handle en passant square change
        if move.is_double_pawn_move:
            direction = 1 if self.turn == Board.WHITE else -1
            self.en_passant_square = move.to_square - 16 * direction
        else:
            self.en_passant_square = None

        # Castling

        if move.is_castling:
            if move.is_short_castling:
                rook = self.squares[move.to_square + 1]
                self.squares[move.to_square + 1] = Board.EMPTY
                self.squares[move.to_square - 1] = rook

            else:  # move.is_long_castling
                rook = self.squares[move.to_square - 2]
                self.squares[move.to_square - 2] = Board.EMPTY
                self.squares[move.to_square + 1] = rook

        # Switch turn
        self.turn = Board.BLACK if self.turn == Board.WHITE else Board.WHITE

    def undo_move(self, move: Move):
        self.squares[move.from_square] = move.piece_moved

        if move.is_en_passant:
            direction = 1 if self.turn == Board.WHITE else -1
            self.squares[move.to_square + direction * 16] = move.piece_captured
            self.squares[move.to_square] = Board.EMPTY
        elif move.is_castling:
            if move.is_short_castling:
                rook = self.squares[move.to_square - 1]
                self.squares[move.to_square] = Board.EMPTY
                self.squares[move.to_square - 1] = Board.EMPTY
                self.squares[move.to_square + 1] = rook
            else:  # move.is_long_castling
                rook = self.squares[move.to_square + 1]
                self.squares[move.to_square] = Board.EMPTY
                self.squares[move.to_square + 1] = Board.EMPTY
                self.squares[move.to_square - 2] = rook
        else:
            self.squares[move.to_square] = move.piece_captured

        # Handle castling rights
        self.can_white_short_castle = move.previous_white_short_castle
        self.can_white_long_castle = move.previous_white_long_castle
        self.can_black_short_castle = move.previous_black_short_castle
        self.can_black_long_castle = move.previous_black_long_castle

        # Handle en passant square
        self.en_passant_square = move.previous_en_passant_square

        # Switch turn
        self.turn = Board.BLACK if self.turn == Board.WHITE else Board.WHITE
