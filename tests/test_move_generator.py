import pytest
from src.board import Board
from src.move_generator import MoveGenerator

@pytest.mark.parametrize("test_input, expected_number_of_moves", [
    ("8/6pp/8/2p5/2P5/8/PP1Pp3/8 w", 6),
    ("8/6pp/8/2p5/2P5/8/PP1Pp3/8 b", 5),
    ("8/8/8/8/8/pppppppp/PPPPPPPP/8 w", 0),
    ("8/8/8/8/8/pppppppp/PPPPPPPP/8 b", 0),
])
def test_generator_contains_all_basic_pawns_movements_without_capturing(test_input, expected_number_of_moves):
    board = Board()
    board.load_FEN(test_input)
    generator = MoveGenerator(board)

    assert len(generator.generate_moves()) == expected_number_of_moves