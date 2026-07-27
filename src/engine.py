from src.board import Board
from src.move_generator import MoveGenerator


class ChessEngine:
    def __init__(self, board: Board):
        self.board = board
        self.current_evaluation = 0

    def evaluate_position(self, board: Board):
        generator = MoveGenerator(board)

        legal_moves = generator.generate_legal_moves()

        game_state = generator.check_game_over(legal_moves)

        if game_state == "CHECKMATE":
            if self.board.turn == Board.BLACK:
                return 1000
            else:
                return -1000

        elif game_state == "STALEMATE":
            return 0

        material_advantage = 0

        for piece in board.squares:
            if abs(piece) == 1:
                material_advantage += piece
            elif abs(piece) == 2:
                material_advantage += 3 * (1 if piece > 0 else -1)
            elif abs(piece) == 3:
                material_advantage += 3 * (1 if piece > 0 else -1)
            elif abs(piece) == 4:
                material_advantage += 5 * (1 if piece > 0 else -1)
            elif abs(piece) == 5:
                material_advantage += 9 * (1 if piece > 0 else -1)

        return material_advantage
