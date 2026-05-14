import pygame
import random

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
LINE_COUNT = 25  # How many "trails" to keep
SPEED = 5        # Movement speed
THICKNESS = 2    # Line thickness

class BouncingLine:
    def __init__(self, color):
        self.color = color
        # Random start positions for both ends of the line
        self.p1 = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        self.p2 = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        # Random directions for both ends
        self.v1 = [random.choice([-SPEED, SPEED]), random.choice([-SPEED, SPEED])]
        self.v2 = [random.choice([-SPEED, SPEED]), random.choice([-SPEED, SPEED])]
        # History to store trailing lines
        self.history = []

    def update(self):
        # Move both points
        self.p1[0] += self.v1[0]
        self.p1[1] += self.v1[1]
        self.p2[0] += self.v2[0]
        self.p2[1] += self.v2[1]

        # Bounce off walls
        for p, v in [(self.p1, self.v1), (self.p2, self.v2)]:
            if p[0] <= 0 or p[0] >= WIDTH: v[0] *= -1
            if p[1] <= 0 or p[1] >= HEIGHT: v[1] *= -1

        # Save current position and trim history
        self.history.append((tuple(self.p1), tuple(self.p2)))
        if len(self.history) > LINE_COUNT:
            self.history.pop(0)

    def draw(self, surface):
        for points in self.history:
            pygame.draw.line(surface, self.color, points[0], points[1], THICKNESS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("80s Retro Lines")
    clock = pygame.time.Clock()

    # Create our RGB lines
    lines = [
        BouncingLine((255, 0, 0)),   # Red
        BouncingLine((0, 255, 0)),   # Green
        BouncingLine((0, 0, 255))    # Blue
    ]

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen with black

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for line in lines:
            line.update()
            line.draw(screen)

        pygame.display.flip()
        clock.tick(30) # 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()