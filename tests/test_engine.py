import pytest
from src.engine import ChessEngine
from src.move_generator import MoveGenerator
from src.board import Board


@pytest.mark.parametrize(
    "fen, expected_eval",
    [
        ("3k4/8/8/8/8/8/7p/3K2R1 w - - 0 0", 4),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0", 0),
        ("r1bqkbnr/1ppp1Qpp/p1n5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 0", 1000),
        ("7k/5Q2/8/8/8/8/8/3K4 b - - 0 0", 0),
        ("7k/5Q2/8/8/8/8/q7/q2K4 w - - 0 0", -1000),
        ("4k3/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0 0", 39),
        ("rnbqkbnr/pppppppp/8/8/8/8/8/4K3 w kq - 0 0", -39),
    ],
)
def test_correct_board_evaluation(fen: str, expected_eval: int):
    board = Board()
    board.load_FEN(fen)

    engine = ChessEngine(board)

    assert engine.evaluate_position(engine.board) == expected_eval
