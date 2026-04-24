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