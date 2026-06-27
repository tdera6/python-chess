import pygame
from pathlib import Path

WIDTH = 1000
HEIGHT = 1000

SQUARE_SIZE = WIDTH / 8

BASE_DIR = Path(__file__).parent.parent.absolute()


class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.piece_images = []

        for color in ["white", "black"]:
            for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
                img = pygame.image.load(f"{BASE_DIR}/assets/images/{color}-{piece}.png")
                scaled_img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                converted_alpha_img = pygame.Surface.convert_alpha(scaled_img)
                self.piece_images.append(converted_alpha_img)

    def main_loop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill("green")

            for i in range(8):
                for j in range(8):
                    square_color = "white" if (i + j) % 2 == 0 else "black"
                    pygame.draw.rect(
                        self.screen,
                        square_color,
                        pygame.Rect(
                            i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                        ),
                    )

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
