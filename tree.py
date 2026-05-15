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

def new_signs():
    return random.sample(range(len(SIGNS)), 12)

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

        screen.fill(bg)
        draw_tree(screen, signs, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
