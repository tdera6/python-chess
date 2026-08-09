from src.board import Board
from src.move import Move
from src.move_generator import MoveGenerator


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
            return self.evaluate_position(self.board)

        legal_moves = MoveGenerator(self.board).generate_legal_moves()

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
