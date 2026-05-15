import pygame
import math
import random
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from zodiac_lines import SIGNS, NAMES, COLORS, draw_sign

WIDTH, HEIGHT = 1000, 680
SCALE = 45
LINE_COLOR = (80, 80, 80)

# Tree layout: (parent_index, x, y)
# 1 root + 3 branches + 8 leaves = 12 total
CHILDREN = {0: [1, 2, 3], 1: [4, 5, 6], 2: [7, 8, 9], 3: [10, 11]}

TREE_LAYOUT = [
    (None, 500,  90),   # 0  root
    (0,    200, 280),   # 1  branch 1
    (0,    500, 280),   # 2  branch 2
    (0,    800, 280),   # 3  branch 3
    (1,     80, 510),   # 4
    (1,    200, 510),   # 5
    (1,    320, 510),   # 6
    (2,    380, 510),   # 7
    (2,    500, 510),   # 8
    (2,    620, 510),   # 9
    (3,    720, 510),   # 10
    (3,    880, 510),   # 11
]

def random_path():
    path = [0]
    node = 0
    while node in CHILDREN:
        node = random.choice(CHILDREN[node])
        path.append(node)
    return path

def new_signs():
    return random.choices(range(12, min(21, len(SIGNS))), k=12)

def draw_tree(surface, sign_indices, font):
    for i, (parent, x, y) in enumerate(TREE_LAYOUT):
        if parent is not None:
            _, px, py = TREE_LAYOUT[parent]
            pygame.draw.line(surface, LINE_COLOR, (px, py), (x, y), 1)

    for i, (parent, x, y) in enumerate(TREE_LAYOUT):
        idx = sign_indices[i]
        color = COLORS[idx % len(COLORS)]
        draw_sign(surface, idx, color, x, y, SCALE)
        lbl = font.render(NAMES[idx], True, color)
        surface.blit(lbl, (x - lbl.get_width() // 2, y + SCALE + 3))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sign Tree")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 11)

    signs = new_signs()
    bg = (0, 0, 0)
    nav_path = None
    nav_t = 0.0
    NAV_SPEED = 0.04

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    signs = new_signs()
                elif event.key == pygame.K_b:
                    bg = (255, 255, 255) if bg == (0, 0, 0) else (0, 0, 0)
                elif event.key == pygame.K_n:
                    nav_path = random_path()
                    nav_t = 0.0

        screen.fill(bg)
        draw_tree(screen, signs, font)

        if nav_path:
            nav_t += NAV_SPEED
            seg = int(nav_t)
            if seg >= len(nav_path) - 1:
                nav_path = None
            else:
                frac = nav_t - seg
                _, x0, y0 = TREE_LAYOUT[nav_path[seg]]
                _, x1, y1 = TREE_LAYOUT[nav_path[seg + 1]]
                bx = int(x0 + (x1 - x0) * frac)
                by = int(y0 + (y1 - y0) * frac)
                pygame.draw.circle(screen, (255, 220, 50), (bx, by), 5)

        caption = font.render("fly with time-space capsule. combine X P I T with quarks, kolmo and commonality.", True, (120, 120, 120))
        screen.blit(caption, (WIDTH // 2 - caption.get_width() // 2, HEIGHT - 22))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
