import pygame
from pathlib import Path
from src.board import Board
from src.move_generator import MoveGenerator

WIDTH = 1000
HEIGHT = 1000

SQUARE_SIZE = WIDTH / 8

BASE_DIR = Path(__file__).parent.parent.absolute()

PIECES = [
    None,
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
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.piece_images = [None]
        self.board = board
        self.load_images()
        self.clicked_squares = []

    def load_images(self):
        for piece in PIECES:
            if piece is not None:
                img = pygame.image.load(f"{BASE_DIR}/assets/images/{piece}.png")
                scaled_img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                converted_alpha_img = pygame.Surface.convert_alpha(scaled_img)
                self.piece_images.append(converted_alpha_img)

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
        clicked_square = self.square_click_detection(event)

        if clicked_square == -1:
            self.clicked_squares.clear()

        self.clicked_squares.append(clicked_square)

        if len(self.clicked_squares) == 2:
            generator = MoveGenerator(self.board)
            legal_moves = generator.generate_legal_moves()

            for move in legal_moves:
                if (
                    move.from_square == self.clicked_squares[0]
                    and move.to_square == self.clicked_squares[1]
                ):
                    self.board.make_move(move)
                    break

            self.clicked_squares.clear()

    def square_click_detection(self, event) -> int:
        if event.button != 1:
            return -1

        x, y = event.pos
        column = x // SQUARE_SIZE
        row = (HEIGHT - y) // SQUARE_SIZE

        return row * 16 + column

    def main_loop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click_detection(event)

            self.screen.fill("green")

            for i in range(8):
                for j in range(8):
                    square_color = "#eeeed2" if (i + j) % 2 == 0 else "#769656"
                    pygame.draw.rect(
                        self.screen,
                        square_color,
                        pygame.Rect(
                            i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                        ),
                    )

            self.display_pieces()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
