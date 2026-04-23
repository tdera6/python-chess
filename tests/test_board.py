from src.board import Board

def test_board_initializes_with_128_squares():
    board = Board()

    assert len(board.squares) == 128

def test_board_starts_with_white_turn():
    board = Board()

    assert board.turn == board.WHITE