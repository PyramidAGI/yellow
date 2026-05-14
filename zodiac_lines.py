import pygame
import math

WIDTH, HEIGHT = 800, 600
CX, CY = WIDTH // 2, HEIGHT // 2
S = 120  # scale

COLORS = [
    (255, 80, 80), (255, 180, 0), (80, 255, 80), (0, 200, 255),
    (200, 80, 255), (255, 100, 200), (80, 255, 200), (255, 140, 40),
    (100, 100, 255), (255, 60, 120), (60, 220, 180), (180, 255, 80),
    (255, 255, 255), (180, 180, 255), (255, 220, 120), (100, 255, 180), (255, 160, 255),
]

def s(x, y):
    return (CX + int(x * S), CY + int(y * S))

# Each sign is a list of polylines (list of list of points)
SIGNS = [
    # Aries - two curved horns as lines
    [[(s(-0.6, 0.2), s(-0.3, -0.4), s(0, 0.1)), (s(0, 0.1), s(0.3, -0.4), s(0.6, 0.2))]],
    # Taurus - circle with horns
    [[s(-0.4, -0.5), s(0, -0.8), s(0.4, -0.5)],
     [s(-0.5, 0), s(-0.5, 0.4), s(0, 0.6), s(0.5, 0.4), s(0.5, 0), s(0.3, -0.4), s(0, -0.5), s(-0.3, -0.4), s(-0.5, 0)]],
    # Gemini - two vertical bars with connectors
    [[s(-0.4, -0.6), s(-0.4, 0.6)],
     [s(0.4, -0.6), s(0.4, 0.6)],
     [s(-0.4, -0.6), s(0.4, -0.6)],
     [s(-0.4, 0.6), s(0.4, 0.6)],
     [s(-0.4, 0), s(0.4, 0)]],
    # Cancer - two spirals
    [[s(0, -0.1), s(-0.3, -0.4), s(-0.5, -0.1), s(-0.3, 0.2), s(0, 0.1), s(0.3, -0.2), s(0.5, 0.1), s(0.3, 0.4), s(0, 0.1)]],
    # Leo - circle with tail
    [[s(0.5, 0), s(0.3, -0.4), s(0, -0.5), s(-0.3, -0.4), s(-0.5, 0), s(-0.3, 0.4), s(0, 0.5), s(0.3, 0.4), s(0.5, 0)],
     [s(0.5, 0), s(0.7, -0.3), s(0.6, -0.6)]],
    # Virgo - m shape with curl
    [[s(-0.6, -0.4), s(-0.6, 0.4), s(-0.2, 0), s(0.2, 0.4), s(0.2, 0), s(0.5, -0.3), s(0.6, 0), s(0.5, 0.4), s(0.2, 0.5)]],
    # Libra - line with bump above
    [[s(-0.6, 0.2), s(0.6, 0.2)],
     [s(-0.6, 0.5), s(0.6, 0.5)],
     [s(-0.3, 0.2), s(-0.5, -0.2), s(0, -0.5), s(0.5, -0.2), s(0.3, 0.2)]],
    # Scorpio - m with stinger
    [[s(-0.6, -0.4), s(-0.6, 0.3), s(-0.2, 0), s(0.2, 0.3), s(0.2, -0.1), s(0.4, 0.3), s(0.6, 0.1), s(0.7, 0.4)]],
    # Sagittarius - arrow diagonal
    [[s(-0.6, 0.6), s(0.6, -0.6)],
     [s(0.6, -0.6), s(0.1, -0.6)],
     [s(0.6, -0.6), s(0.6, -0.1)],
     [s(-0.4, 0.4), s(0.4, -0.4)]],
    # Capricorn - v with loop
    [[s(-0.6, -0.4), s(-0.3, 0.5), s(0, 0), s(0.4, 0.4), s(0.6, 0.1), s(0.4, -0.2), s(0.2, 0.1), s(0.4, 0.4)]],
    # Aquarius - two waves
    [[s(-0.6, -0.15), s(-0.3, -0.4), s(0, -0.15), s(0.3, -0.4), s(0.6, -0.15)],
     [s(-0.6, 0.15), s(-0.3, 0.4), s(0, 0.15), s(0.3, 0.4), s(0.6, 0.15)]],
    # Pisces - two arcs with crossbar
    [[s(-0.2, -0.6), s(-0.5, -0.3), s(-0.6, 0), s(-0.5, 0.3), s(-0.2, 0.6)],
     [s(0.2, -0.6), s(0.5, -0.3), s(0.6, 0), s(0.5, 0.3), s(0.2, 0.6)],
     [s(-0.2, 0), s(0.2, 0)]],
    # Fork-up - stem down, three prongs pointing up
    [[s(0, 0.6), s(0, -0.2)],
     [s(0, -0.2), s(-0.5, -0.7)],
     [s(0, -0.2), s(0, -0.7)],
     [s(0, -0.2), s(0.5, -0.7)]],
    # Fork-down - stem up, three prongs pointing down
    [[s(0, -0.6), s(0, 0.2)],
     [s(0, 0.2), s(-0.5, 0.7)],
     [s(0, 0.2), s(0, 0.7)],
     [s(0, 0.2), s(0.5, 0.7)]],
    # Parallelogram
    [[s(-0.6, 0.4), s(-0.2, -0.4), s(0.6, -0.4), s(0.2, 0.4), s(-0.6, 0.4)]],
    # Two opposing triangles meeting at center point (hourglass)
    [[s(-0.55, -0.65), s(0.55, -0.65), s(0, 0), s(-0.55, -0.65)],
     [s(-0.55, 0.65), s(0.55, 0.65), s(0, 0), s(-0.55, 0.65)]],
    # Sine cycle
    [[s(-0.7 + i * 1.4 / 40, -0.5 * math.sin(i * 2 * math.pi / 40)) for i in range(41)]],
]

NAMES = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces",
         "Fork-Up","Fork-Down","Parallelogram","Twin Triangles","Sine Cycle"]

def draw_sign(surface, index, color):
    for polyline in SIGNS[index]:
        if polyline and isinstance(polyline[0], tuple) and isinstance(polyline[0][0], tuple):
            # list of polylines (Aries case)
            for sub in polyline:
                if len(sub) >= 2:
                    pygame.draw.lines(surface, color, False, sub, 1)
        else:
            if len(polyline) >= 2:
                pygame.draw.lines(surface, color, False, polyline, 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zodiac Lines")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28)

    current = 0
    show = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if show:
                        current = (current + 1) % 17
                    show = True
                elif event.key == pygame.K_1:
                    current, show = 12, True
                elif event.key == pygame.K_2:
                    current, show = 13, True
                elif event.key == pygame.K_3:
                    current, show = 14, True
                elif event.key == pygame.K_4:
                    current, show = 15, True
                elif event.key == pygame.K_5:
                    current, show = 16, True

        screen.fill((0, 0, 0))

        if show:
            color = COLORS[current]
            draw_sign(screen, current, color)
            label = font.render(NAMES[current], True, color)
            screen.blit(label, (CX - label.get_width() // 2, CY + int(0.75 * S)))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
