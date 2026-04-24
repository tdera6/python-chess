from src.board import Board

def test_board_initializes_with_128_squares():
    board = Board()

    assert len(board.squares) == 128

def test_board_starts_with_white_turn():
    board = Board()

    assert board.turn == board.WHITE

def test_board_pieces_constants():
    assert Board.WHITE_PAWN == 1
    assert Board.BLACK_BISHOP == -3
    assert Board.WHITE_KING == 6
    assert Board.BLACK_QUEEN == -5

def test_board_setup_starting_position():
    board = Board()
    board.setup_starting_position()

    # Check some key squares for white pieces
    assert board.squares[0] == Board.WHITE_ROOK
    assert board.squares[1] == Board.WHITE_KNIGHT
    assert board.squares[4] == Board.WHITE_KING
    assert board.squares[16] == Board.WHITE_PAWN

    # Check some key squares for black pieces
    assert board.squares[112] == Board.BLACK_ROOK
    assert board.squares[113] == Board.BLACK_KNIGHT
    assert board.squares[116] == Board.BLACK_KING
    assert board.squares[96] == Board.BLACK_PAWN