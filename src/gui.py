import pygame

WIDTH = 1000
HEIGHT = 1000

SQUARE_SIZE = WIDTH / 8


class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

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
