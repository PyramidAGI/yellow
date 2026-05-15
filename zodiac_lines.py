import pygame
import math
import random

WIDTH, HEIGHT = 1100, 600
MAIN_W = 700
SIDEBAR_W = 200
SIDEBAR1_CX = MAIN_W + SIDEBAR_W // 2
SIDEBAR2_CX = MAIN_W + SIDEBAR_W + SIDEBAR_W // 2
ITEM_SCALE = 40
ITEM_H = 90
ITEMS_PER_COL = (HEIGHT - 20) // ITEM_H
CX, CY = MAIN_W // 2, HEIGHT // 2
S = 120

COLORS = [
    (255, 80, 80), (255, 180, 0), (80, 255, 80), (0, 200, 255),
    (200, 80, 255), (255, 100, 200), (80, 255, 200), (255, 140, 40),
    (100, 100, 255), (255, 60, 120), (60, 220, 180), (180, 255, 80),
    (255, 255, 255), (180, 180, 255), (255, 220, 120), (100, 255, 180),
    (255, 160, 255), (80, 200, 255), (255, 120, 80), (200, 255, 100), (255, 200, 200),
]

# Normalized polylines: each sign is a list of polylines, each polyline is a list of (x, y) floats
SIGNS_NORM = [
    # Aries
    [(-0.6, 0.2), (-0.3, -0.4), (0, 0.1)],
    [(0, 0.1), (0.3, -0.4), (0.6, 0.2)],
    # ---
    [None],
    # Taurus
    [(-0.4, -0.5), (0, -0.8), (0.4, -0.5)],
    [(-0.5, 0), (-0.5, 0.4), (0, 0.6), (0.5, 0.4), (0.5, 0), (0.3, -0.4), (0, -0.5), (-0.3, -0.4), (-0.5, 0)],
]

# Rebuild as clean structure: list of signs, each sign = list of polylines, each polyline = list of (x,y)
SIGNS = [
    # Aries
    [[(-0.6, 0.2), (-0.3, -0.4), (0, 0.1)],
     [(0, 0.1), (0.3, -0.4), (0.6, 0.2)]],
    # Taurus
    [[(-0.4, -0.5), (0, -0.8), (0.4, -0.5)],
     [(-0.5, 0), (-0.5, 0.4), (0, 0.6), (0.5, 0.4), (0.5, 0), (0.3, -0.4), (0, -0.5), (-0.3, -0.4), (-0.5, 0)]],
    # Gemini
    [[(-0.4, -0.6), (-0.4, 0.6)],
     [(0.4, -0.6), (0.4, 0.6)],
     [(-0.4, -0.6), (0.4, -0.6)],
     [(-0.4, 0.6), (0.4, 0.6)],
     [(-0.4, 0), (0.4, 0)]],
    # Cancer
    [[(0, -0.1), (-0.3, -0.4), (-0.5, -0.1), (-0.3, 0.2), (0, 0.1), (0.3, -0.2), (0.5, 0.1), (0.3, 0.4), (0, 0.1)]],
    # Leo
    [[(0.5, 0), (0.3, -0.4), (0, -0.5), (-0.3, -0.4), (-0.5, 0), (-0.3, 0.4), (0, 0.5), (0.3, 0.4), (0.5, 0)],
     [(0.5, 0), (0.7, -0.3), (0.6, -0.6)]],
    # Virgo
    [[(-0.6, -0.4), (-0.6, 0.4), (-0.2, 0), (0.2, 0.4), (0.2, 0), (0.5, -0.3), (0.6, 0), (0.5, 0.4), (0.2, 0.5)]],
    # Libra
    [[(-0.6, 0.2), (0.6, 0.2)],
     [(-0.6, 0.5), (0.6, 0.5)],
     [(-0.3, 0.2), (-0.5, -0.2), (0, -0.5), (0.5, -0.2), (0.3, 0.2)]],
    # Scorpio
    [[(-0.6, -0.4), (-0.6, 0.3), (-0.2, 0), (0.2, 0.3), (0.2, -0.1), (0.4, 0.3), (0.6, 0.1), (0.7, 0.4)]],
    # Sagittarius
    [[(-0.6, 0.6), (0.6, -0.6)],
     [(0.6, -0.6), (0.1, -0.6)],
     [(0.6, -0.6), (0.6, -0.1)],
     [(-0.4, 0.4), (0.4, -0.4)]],
    # Capricorn
    [[(-0.6, -0.4), (-0.3, 0.5), (0, 0), (0.4, 0.4), (0.6, 0.1), (0.4, -0.2), (0.2, 0.1), (0.4, 0.4)]],
    # Aquarius
    [[(-0.6, -0.15), (-0.3, -0.4), (0, -0.15), (0.3, -0.4), (0.6, -0.15)],
     [(-0.6, 0.15), (-0.3, 0.4), (0, 0.15), (0.3, 0.4), (0.6, 0.15)]],
    # Pisces
    [[(-0.2, -0.6), (-0.5, -0.3), (-0.6, 0), (-0.5, 0.3), (-0.2, 0.6)],
     [(0.2, -0.6), (0.5, -0.3), (0.6, 0), (0.5, 0.3), (0.2, 0.6)],
     [(-0.2, 0), (0.2, 0)]],
    # Fork-up
    [[(0, 0.6), (0, -0.2)],
     [(0, -0.2), (-0.5, -0.7)],
     [(0, -0.2), (0, -0.7)],
     [(0, -0.2), (0.5, -0.7)]],
    # Fork-down
    [[(0, -0.6), (0, 0.2)],
     [(0, 0.2), (-0.5, 0.7)],
     [(0, 0.2), (0, 0.7)],
     [(0, 0.2), (0.5, 0.7)]],
    # Parallelogram
    [[(-0.6, 0.4), (-0.2, -0.4), (0.6, -0.4), (0.2, 0.4), (-0.6, 0.4)]],
    # Twin Triangles (hourglass)
    [[(-0.55, -0.65), (0.55, -0.65), (0, 0), (-0.55, -0.65)],
     [(-0.55, 0.65), (0.55, 0.65), (0, 0), (-0.55, 0.65)]],
    # Sine Cycle
    [[(-0.7 + i * 1.4 / 40, -0.5 * math.sin(i * 2 * math.pi / 40)) for i in range(41)]],
    # Circle
    [[(0.6 * math.cos(i * 2 * math.pi / 60), 0.6 * math.sin(i * 2 * math.pi / 60)) for i in range(61)]],
    # Arrow right
    [[(-0.7, 0), (0.7, 0)],
     [(0.7, 0), (0.3, -0.4)],
     [(0.7, 0), (0.3, 0.4)]],
    # Dot
    [[(0.08 * math.cos(i * 2 * math.pi / 20), 0.08 * math.sin(i * 2 * math.pi / 20)) for i in range(21)]],
    # Sentence (8x1 table)
    [[(-0.7, -0.15), (0.7, -0.15), (0.7, 0.15), (-0.7, 0.15), (-0.7, -0.15)]]
    + [[(-0.7 + i * 1.4 / 8, -0.15), (-0.7 + i * 1.4 / 8, 0.15)] for i in range(1, 8)],
]

NAMES = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces",
         "compose","decompose","causal diagram","Twin Triangles","Sine Cycle","Circle","Arrow Right","Dot","Sentence"]

def p(x, y, cx, cy, scale):
    return (cx + int(x * scale), cy + int(y * scale))

def draw_sign(surface, index, color, cx, cy, scale):
    for polyline in SIGNS[index]:
        pts = [p(x, y, cx, cy, scale) for x, y in polyline]
        if len(pts) >= 2:
            pygame.draw.lines(surface, color, False, pts, 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("fly with time - space capsule -> combine X P I T with kolmo and commonality")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 11)

    current = 0
    show = False
    sidebar = []  # list of sign indices

    SHORTCUTS = {
        pygame.K_1: 12, pygame.K_2: 13, pygame.K_3: 14,
        pygame.K_4: 15, pygame.K_5: 16, pygame.K_6: 17, pygame.K_7: 18, pygame.K_8: 19, pygame.K_9: 20,
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if show:
                        current = (current + 1) % len(SIGNS)
                    show = True
                    sidebar.append(current)
                elif event.key in SHORTCUTS:
                    current = SHORTCUTS[event.key]
                    show = True
                    sidebar.append(current)
                elif event.key == pygame.K_DELETE:
                    if sidebar:
                        sidebar.pop()
                elif event.key == pygame.K_c:
                    sidebar.clear()
                elif event.key == pygame.K_r:
                    sidebar.clear()
                    sidebar.extend(random.choices(range(len(SIGNS)), k=6))

        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (60, 60, 60), (MAIN_W, 0), (MAIN_W, HEIGHT), 1)
        pygame.draw.line(screen, (60, 60, 60), (MAIN_W + SIDEBAR_W, 0), (MAIN_W + SIDEBAR_W, HEIGHT), 1)

        if show:
            color = COLORS[current]
            draw_sign(screen, current, color, CX, CY, S)
            label = font.render(NAMES[current], True, color)
            screen.blit(label, (CX - label.get_width() // 2, CY + int(0.75 * S)))

        # Draw sidebars
        for i, idx in enumerate(sidebar):
            col = i // ITEMS_PER_COL
            if col > 1:
                break
            cx = SIDEBAR1_CX if col == 0 else SIDEBAR2_CX
            item_cy = 45 + (i % ITEMS_PER_COL) * ITEM_H
            color = COLORS[idx]
            draw_sign(screen, idx, color, cx, item_cy, ITEM_SCALE)
            lbl = small_font.render(NAMES[idx], True, color)
            screen.blit(lbl, (cx - lbl.get_width() // 2, item_cy + ITEM_SCALE + 4))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
