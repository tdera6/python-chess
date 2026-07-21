import pygame
from pathlib import Path
from src.board import Board
from src.move_generator import MoveGenerator
from src.move import Move

WIDTH = 1000
HEIGHT = 1000

SQUARE_SIZE = WIDTH / 8

BASE_DIR = Path(__file__).parent.parent.absolute()

PIECES = [
    "white-pawn",
    "white-knight",
    "white-bishop",
    "white-rook",
    "white-queen",
    "white-king",
    "black-king",
    "black-queen",
    "black-rook",
    "black-bishop",
    "black-knight",
    "black-pawn",
]


class GUI:
    def __init__(self, board: Board):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.piece_images = [None]
        self.dot_image = None
        self.circle_image = None
        self.board = board
        self.load_images()
        self.clicked_squares = []
        self.possible_moves = MoveGenerator(self.board).generate_legal_moves()
        self.game_state = None
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 64)
        self.promotion_flag = False

    def load_images(self):
        for piece in PIECES:
            img = pygame.image.load(f"{BASE_DIR}/assets/images/{piece}.png")
            scaled_img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            converted_alpha_img = pygame.Surface.convert_alpha(scaled_img)
            self.piece_images.append(converted_alpha_img)

        img = pygame.image.load(f"{BASE_DIR}/assets/images/dot.png")
        scaled_img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        converted_alpha_img = scaled_img.convert_alpha()
        converted_alpha_img.set_alpha(64)
        self.dot_image = converted_alpha_img

        img = pygame.image.load(f"{BASE_DIR}/assets/images/circle.png")
        scaled_img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        converted_alpha_img = scaled_img.convert_alpha()
        converted_alpha_img.set_alpha(64)
        self.circle_image = converted_alpha_img

    def display_pieces(self):
        for row in range(8):
            for column in range(8):
                piece = self.board.squares[row * 16 + column]
                if piece != 0:
                    self.screen.blit(
                        self.piece_images[piece],
                        (
                            (column * SQUARE_SIZE),
                            (HEIGHT - (row + 1) * SQUARE_SIZE),
                        ),
                    )

    def handle_click_detection(self, event):

        if self.promotion_flag:
            return

        clicked_square = self.square_click_detection(event)

        if clicked_square == -1:
            self.clicked_squares.clear()
            return

        if len(self.clicked_squares) == 0 and self.board.squares[clicked_square] == 0:
            return

        if clicked_square in self.clicked_squares:
            self.clicked_squares.clear()
            return

        if (
            len(self.clicked_squares) == 1
            and self.board.squares[clicked_square] * self.board.turn > 0
        ):
            self.clicked_squares.clear()

        self.clicked_squares.append(clicked_square)

        if len(self.clicked_squares) == 2:
            for move in self.possible_moves:
                if (
                    move.from_square == self.clicked_squares[0]
                    and move.to_square == self.clicked_squares[1]
                ):
                    self.board.make_move(move)
                    generator = MoveGenerator(self.board)
                    self.possible_moves = generator.generate_legal_moves()
                    self.game_state = generator.check_game_over(self.possible_moves)
                    break

            self.clicked_squares.clear()

    def square_click_detection(self, event) -> int:
        if event.button != 1:
            return -1

        x, y = event.pos
        column = x // SQUARE_SIZE

        # prevent row = 8 if player clicks on 0 px
        row = min((HEIGHT - y) // SQUARE_SIZE, 7)

        return int(row * 16 + column)

    def display_game_over_screen(self):
        game_over_surface = pygame.Surface((5 * SQUARE_SIZE, 4 * SQUARE_SIZE))
        game_over_surface.fill("white")
        game_over_surface.set_alpha(230)

        if self.game_state == "CHECKMATE":
            text = f"{'WHITE' if self.board.turn == Board.BLACK else 'BLACK'} WIN!"
        elif self.game_state == "STALEMATE":
            text = "DRAW!"
        else:
            text = ""

        text_surface = self.font.render(text, False, (0, 0, 0))
        text_button = self.font.render("Click 'R' to play again", False, (0, 0, 0))

        button = pygame.Surface((3 * SQUARE_SIZE, SQUARE_SIZE))
        button.fill("white")
        button.set_alpha(255)
        button.blit(
            text_button,
            (
                (button.get_width() - text_button.get_width()) // 2,
                (button.get_height() - text_button.get_height()) // 2,
            ),
        )

        game_over_surface.blit(
            text_surface,
            (
                (game_over_surface.get_width() - text_surface.get_width()) // 2,
                (game_over_surface.get_height() - text_surface.get_height()) // 2
                - SQUARE_SIZE,
            ),
        )

        game_over_surface.blit(
            button,
            (
                (game_over_surface.get_width() - button.get_width()) // 2,
                (game_over_surface.get_height() - button.get_height()) // 2
                + SQUARE_SIZE,
            ),
        )

        self.screen.blit(
            game_over_surface,
            (
                (WIDTH - game_over_surface.get_width()) // 2,
                (HEIGHT - game_over_surface.get_height()) // 2,
            ),
        )

    def display_piece_promotion_screen(self):
        piece_promotion_screen = pygame.Surface((5 * SQUARE_SIZE, 4 * SQUARE_SIZE))
        piece_promotion_screen.fill("white")
        piece_promotion_screen.set_alpha(230)

        color = self.board.turn

        title_text = self.big_font.render("PROMOTION", False, (0, 0, 0))
        cancel_text = self.font.render("To cancel click ESC", False, (0, 0, 0))
        knight_letter_text = self.big_font.render("A", False, (0, 0, 0))
        bishop_letter_text = self.big_font.render("S", False, (0, 0, 0))
        rook_letter_text = self.big_font.render("D", False, (0, 0, 0))
        queen_letter_text = self.big_font.render("F", False, (0, 0, 0))

        knight_box = pygame.Surface((SQUARE_SIZE, 2 * SQUARE_SIZE))
        knight_box.fill("white")
        knight_box.blit(self.piece_images[Board.KNIGHT * color], (0, 0))
        knight_box.blit(
            knight_letter_text,
            (
                (knight_box.get_width() - knight_letter_text.get_width()) // 2,
                SQUARE_SIZE * 1.2,
            ),
        )

        bishop_box = pygame.Surface((SQUARE_SIZE, 2 * SQUARE_SIZE))
        bishop_box.fill("white")
        bishop_box.blit(self.piece_images[Board.BISHOP * color], (0, 0))
        bishop_box.blit(
            bishop_letter_text,
            (
                (bishop_box.get_width() - bishop_letter_text.get_width()) // 2,
                SQUARE_SIZE * 1.2,
            ),
        )

        rook_box = pygame.Surface((SQUARE_SIZE, 2 * SQUARE_SIZE))
        rook_box.fill("white")
        rook_box.blit(self.piece_images[Board.ROOK * color], (0, 0))
        rook_box.blit(
            rook_letter_text,
            (
                (rook_box.get_width() - rook_letter_text.get_width()) // 2,
                SQUARE_SIZE * 1.2,
            ),
        )

        queen_box = pygame.Surface((SQUARE_SIZE, 2 * SQUARE_SIZE))
        queen_box.fill("white")
        queen_box.blit(self.piece_images[Board.QUEEN * color], (0, 0))
        queen_box.blit(
            queen_letter_text,
            (
                (queen_box.get_width() - queen_letter_text.get_width()) // 2,
                SQUARE_SIZE * 1.2,
            ),
        )

        piece_promotion_screen.blit(
            title_text,
            (
                (piece_promotion_screen.get_width() - title_text.get_width()) // 2,
                SQUARE_SIZE * 0.2,
            ),
        )

        piece_promotion_screen.blit(
            knight_box,
            (
                0.5 * SQUARE_SIZE,
                (piece_promotion_screen.get_height() - knight_box.get_height()) // 2,
            ),
        )

        piece_promotion_screen.blit(
            bishop_box,
            (
                1.5 * SQUARE_SIZE,
                (piece_promotion_screen.get_height() - bishop_box.get_height()) // 2,
            ),
        )

        piece_promotion_screen.blit(
            rook_box,
            (
                2.5 * SQUARE_SIZE,
                (piece_promotion_screen.get_height() - rook_box.get_height()) // 2,
            ),
        )

        piece_promotion_screen.blit(
            queen_box,
            (
                3.5 * SQUARE_SIZE,
                (piece_promotion_screen.get_height() - queen_box.get_height()) // 2,
            ),
        )

        piece_promotion_screen.blit(
            cancel_text,
            (
                (piece_promotion_screen.get_width() - cancel_text.get_width()) // 2,
                piece_promotion_screen.get_height() - SQUARE_SIZE * 0.6,
            ),
        )

        self.screen.blit(
            piece_promotion_screen,
            (
                (WIDTH - piece_promotion_screen.get_width()) // 2,
                (HEIGHT - piece_promotion_screen.get_height()) // 2,
            ),
        )

    def restart_game(self):
        self.board = Board()
        self.board.load_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.clicked_squares = []
        self.game_state = None
        self.possible_moves = MoveGenerator(self.board).generate_legal_moves()

    def main_loop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click_detection(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_state is not None:
                        self.restart_game()

            self.screen.fill("green")

            for i in range(8):
                for j in range(8):
                    square_color = "#eeeed2" if (i + j) % 2 == 0 else "#769656"
                    square_number_gui = (7 - j) * 16 + i

                    piece_on_square = self.board.squares[square_number_gui]
                    current_turn = self.board.turn

                    pygame.draw.rect(
                        self.screen,
                        square_color,
                        pygame.Rect(
                            i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                        ),
                    )

                    if (
                        square_number_gui in self.clicked_squares
                        and piece_on_square != 0
                        and piece_on_square * current_turn > 0
                        and any(
                            move.from_square == square_number_gui
                            for move in self.possible_moves
                        )
                    ):
                        highlighted_square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                        highlighted_square.set_alpha(128)
                        highlighted_square.fill("#a0c322")
                        self.screen.blit(
                            highlighted_square, (i * SQUARE_SIZE, j * SQUARE_SIZE)
                        )

                    if len(self.clicked_squares) == 1:
                        for move in self.possible_moves:
                            if (
                                move.from_square == self.clicked_squares[0]
                                and move.to_square == square_number_gui
                            ):
                                if move.piece_captured == 0:
                                    self.screen.blit(
                                        self.dot_image,
                                        (i * SQUARE_SIZE, j * SQUARE_SIZE),
                                    )
                                else:
                                    self.screen.blit(
                                        self.circle_image,
                                        (i * SQUARE_SIZE, j * SQUARE_SIZE),
                                    )

            self.display_pieces()

            if self.game_state is not None:
                self.display_game_over_screen()

            if self.promotion_flag:
                self.display_piece_promotion_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
