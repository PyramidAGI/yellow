import pygame
import random

WIDTH, HEIGHT = 800, 600

SIGNS = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]

COLORS = [
    (255, 80, 80), (255, 180, 0), (80, 255, 80), (0, 200, 255),
    (200, 80, 255), (255, 100, 200), (80, 255, 200), (255, 140, 40),
    (100, 100, 255), (255, 60, 120), (60, 220, 180), (180, 255, 80),
]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zodiac")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeuisymbol", 300)

    current = None
    index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current = index % len(SIGNS)
                index += 1

        screen.fill((0, 0, 0))

        if current is not None:
            text = font.render(SIGNS[current], True, COLORS[current])
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
