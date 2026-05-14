import pygame
import random

WIDTH, HEIGHT = 800, 600
TRAIL_COUNT = 20
SPEED = 2
THICKNESS = 1

COLORS = [
    (255, 50, 50),    # Red
    (50, 255, 50),    # Green
    (50, 100, 255),   # Blue
    (255, 200, 0),    # Yellow
    (255, 0, 200),    # Magenta
    (0, 220, 220),    # Cyan
    (255, 130, 0),    # Orange
    (160, 0, 255),    # Purple
]

class BouncingRect:
    def __init__(self, color):
        self.color = color
        w = random.randint(40, 160)
        h = random.randint(30, 120)
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = random.choice([-SPEED, SPEED])
        self.vy = random.choice([-SPEED, SPEED])
        self.history = []

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1

        self.history.append(self.rect.copy())
        if len(self.history) > TRAIL_COUNT:
            self.history.pop(0)

    def draw(self, surface):
        for r in self.history:
            pygame.draw.rect(surface, self.color, r, THICKNESS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Rectangles")
    clock = pygame.time.Clock()

    rects = [BouncingRect(color) for color in COLORS]

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for rect in rects:
            rect.update()
            rect.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
