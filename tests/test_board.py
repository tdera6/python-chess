import pytest
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

@pytest.mark.parametrize("test_input, expected_turn", [
    ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", Board.BLACK),
    ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", Board.BLACK),
    ("4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1", Board.WHITE)
])
def test_board_load_fen_check_if_turn_is_correct(test_input: str, expected_turn: int):
    board = Board()
    board.load_FEN(test_input)

    assert board.turn == expected_turn


@pytest.mark.parametrize("test_input, square, expected_piece", [
    ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", 0x00, Board.EMPTY),
    ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", 0x20, Board.WHITE_PAWN),
    ("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", 0x65, Board.BLACK_KING),
    ("4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1", 0x66, Board.BLACK_ROOK),
    ("4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1", 0x13, Board.WHITE_ROOK),
    ("1r2k1r1/pbppnp1p/1b3P2/8/Q7/B1PB1q2/P4PPP/3R2K1 w - - 0 21", 0x30, Board.WHITE_QUEEN),
    ("1r2k1r1/pbppnp1p/1b3P2/8/Q7/B1PB1q2/P4PPP/3R2K1 w - - 0 21", 0x25, Board.BLACK_QUEEN),
])
def test_board_load_fen_check_if_pieces_are_correct(test_input: str, square: int, expected_piece: int):
    board = Board()
    board.load_FEN(test_input)

    assert board.squares[square] == expected_piece