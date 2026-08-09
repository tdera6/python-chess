from src.board import Board
from src.move import Move
from src.move_generator import MoveGenerator

PIECE_VALUES = {
    0: 0,
    1: 1,
    2: 3,
    3: 3,
    4: 5,
    5: 9,
    6: 0,
    -1: -1,
    -2: -3,
    -3: -3,
    -4: -5,
    -5: -9,
    -6: 0,
}


class ChessEngine:
    LOWEST_SCORE = -100000
    HIGHEST_SCORE = 100000
    DEFAULT_DEPTH = 3

    def __init__(self, board: Board):
        self.board = board
        self.current_evaluation = 0

    def alpha_beta(
        self, depth: int, is_maximizing: bool, alpha: int, beta: int
    ) -> Move:

        if depth == 0:
            color = self.board.turn
            if color == Board.WHITE:
                king_square = self.board.white_king_square
                enemy_color = Board.BLACK
            else:
                king_square = self.board.black_king_square
                enemy_color = Board.WHITE

            move_generator = MoveGenerator(self.board)

            if move_generator.is_square_under_atack(king_square, enemy_color):
                legal_moves = move_generator.generate_legal_moves()
                game_state = move_generator.check_game_over(legal_moves)

                if game_state == "CHECKMATE":
                    if self.board.turn == Board.BLACK:
                        return 1000
                    else:
                        return -1000

                elif game_state == "STALEMATE":
                    return 0

            return self.evaluate_position(self.board)

        legal_moves = MoveGenerator(self.board).generate_legal_moves()

        game_state = MoveGenerator(self.board).check_game_over(legal_moves)

        if game_state == "CHECKMATE":
            if self.board.turn == Board.BLACK:
                return 1000
            else:
                return -1000

        elif game_state == "STALEMATE":
            return 0

        if is_maximizing:
            best_value = ChessEngine.LOWEST_SCORE

            for move in legal_moves:
                self.board.make_move(move)
                evaluation = self.alpha_beta(depth - 1, not is_maximizing, alpha, beta)
                best_value = max(best_value, evaluation)
                alpha = max(best_value, alpha)

                self.board.undo_move(move)

                if alpha >= beta:
                    break

            return best_value

        else:  # is_maximizing == False
            best_value = ChessEngine.HIGHEST_SCORE

            for move in legal_moves:
                self.board.make_move(move)
                evaluation = self.alpha_beta(depth - 1, not is_maximizing, alpha, beta)
                best_value = min(best_value, evaluation)
                beta = min(best_value, beta)

                self.board.undo_move(move)

                if alpha >= beta:
                    break

            return best_value

    def find_best_move(self) -> Move:
        legal_moves = MoveGenerator(self.board).generate_legal_moves()

        alpha = ChessEngine.LOWEST_SCORE
        beta = ChessEngine.HIGHEST_SCORE

        is_maximizing = self.board.turn == Board.WHITE

        if is_maximizing:
            best_score = ChessEngine.LOWEST_SCORE
            best_move = None
            for move in legal_moves:
                self.board.make_move(move)
                score = self.alpha_beta(
                    ChessEngine.DEFAULT_DEPTH, not is_maximizing, alpha, beta
                )

                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, best_score)

                self.board.undo_move(move)

                if alpha >= beta:
                    break

            return best_move

        else:  # is_maximizing == False
            best_score = ChessEngine.HIGHEST_SCORE
            best_move = None
            for move in legal_moves:
                self.board.make_move(move)
                score = self.alpha_beta(
                    ChessEngine.DEFAULT_DEPTH, not is_maximizing, alpha, beta
                )

                if score < best_score:
                    best_score = score
                    best_move = move

                beta = min(beta, best_score)

                self.board.undo_move(move)

                if alpha >= beta:
                    break

            return best_move

    def evaluate_position(self, board: Board):
        material_advantage = 0

        for piece in board.squares:
            material_advantage += PIECE_VALUES[piece]

        return material_advantage
