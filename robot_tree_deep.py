import pygame
import math
import random
import os
import csv

CSV_FILE = os.path.join(os.path.dirname(__file__), "robot_tree_deep1.csv")
BINARY_FILE = os.path.join(os.path.dirname(__file__), "binary_tree.csv")

WIDTH, HEIGHT = 1000, 680
SCALE = 20
LINE_COLOR = (80, 80, 80)

# 4 levels: 1 root + 3 branches + 8 sub-branches + 16 leaves = 28 nodes
CHILDREN = {
    0: [1, 2, 3],
    1: [4, 5, 6],   2: [7, 8, 9],    3: [10, 11],
    4: [12, 13],    5: [14, 15],     6: [16, 17],
    7: [18, 19],    8: [20, 21],     9: [22, 23],
    10: [24, 25],   11: [26, 27],
}

TREE_LAYOUT = [
    (None, 500,  55),   # 0  root
    (0,    190, 180),   # 1  branch 1
    (0,    562, 180),   # 2  branch 2
    (0,    872, 180),   # 3  branch 3
    (1,     66, 330),   # 4
    (1,    190, 330),   # 5
    (1,    314, 330),   # 6
    (2,    438, 330),   # 7
    (2,    562, 330),   # 8
    (2,    686, 330),   # 9
    (3,    810, 330),   # 10
    (3,    934, 330),   # 11
    (4,     35, 510),   # 12
    (4,     97, 510),   # 13
    (5,    159, 510),   # 14
    (5,    221, 510),   # 15
    (6,    283, 510),   # 16
    (6,    345, 510),   # 17
    (7,    407, 510),   # 18
    (7,    469, 510),   # 19
    (8,    531, 510),   # 20
    (8,    593, 510),   # 21
    (9,    655, 510),   # 22
    (9,    717, 510),   # 23
    (10,   779, 510),   # 24
    (10,   841, 510),   # 25
    (11,   903, 510),   # 26
    (11,   965, 510),   # 27
]

ROBOT_PARTS = [
    ("grasper", [
        [(-0.3, 0.5), (-0.3, 0.0), (-0.15, -0.5)],
        [(0.3, 0.5), (0.3, 0.0), (0.15, -0.5)],
        [(-0.3, 0.0), (0.3, 0.0)],
    ]),
    ("arm", [
        [(-0.5, 0.6), (-0.5, 0.0), (0.5, 0.0), (0.5, -0.6)],
    ]),
    ("leg", [
        [(0.0, -0.6), (0.0, 0.4), (0.5, 0.6)],
    ]),
    ("body", [
        [(-0.5, -0.6), (0.5, -0.6), (0.5, 0.6), (-0.5, 0.6), (-0.5, -0.6)],
    ]),
    ("camera", [
        [(-0.5, -0.3), (0.5, -0.3), (0.5, 0.3), (-0.5, 0.3), (-0.5, -0.3)],
        [(0.25 * math.cos(i * 2 * math.pi / 20), 0.25 * math.sin(i * 2 * math.pi / 20)) for i in range(21)],
    ]),
    ("electromotor", [
        [(0.35 * math.cos(i * 2 * math.pi / 30), 0.35 * math.sin(i * 2 * math.pi / 30)) for i in range(31)],
        [(-0.7, 0.0), (-0.35, 0.0)],
        [(0.35, 0.0), (0.7, 0.0)],
    ]),
    ("servomotor", [
        [(-0.4, -0.2), (0.4, -0.2), (0.4, 0.4), (-0.4, 0.4), (-0.4, -0.2)],
        [(0.0, -0.2), (0.0, -0.6)],
        [(-0.2, -0.6), (0.2, -0.6)],
    ]),
    ("brain", [
        [(0.5 * math.cos(t) * (1 + 0.15 * math.cos(6 * t)),
          0.4 * math.sin(t) * (1 + 0.1 * math.cos(6 * t)))
         for t in (i * 2 * math.pi / 60 for i in range(61))],
    ]),
    ("dot", [
        [(0.08 * math.cos(i * 2 * math.pi / 20), 0.08 * math.sin(i * 2 * math.pi / 20)) for i in range(21)],
    ]),
]

COLORS = [
    (255, 80, 80), (255, 180, 0), (80, 255, 80), (0, 200, 255),
    (200, 80, 255), (255, 100, 200), (80, 255, 200), (255, 140, 40),
]

def p(x, y, cx, cy, scale):
    return (cx + int(x * scale), cy + int(y * scale))

def draw_part(surface, index, color, cx, cy, scale):
    for polyline in ROBOT_PARTS[index][1]:
        pts = [p(x, y, cx, cy, scale) for x, y in polyline]
        if len(pts) >= 2:
            pygame.draw.lines(surface, color, False, pts, 1)

def draw_tree(surface, part_indices, font, binary=None):
    for i, (parent, x, y) in enumerate(TREE_LAYOUT):
        if parent is not None:
            _, px, py = TREE_LAYOUT[parent]
            pygame.draw.line(surface, LINE_COLOR, (px, py), (x, y), 1)
    for i, (parent, x, y) in enumerate(TREE_LAYOUT):
        idx = part_indices[i]
        color = COLORS[idx % len(COLORS)]
        draw_part(surface, idx, color, x, y, SCALE)
        lbl = font.render(ROBOT_PARTS[idx][0], True, color)
        surface.blit(lbl, (x - lbl.get_width() // 2, y + SCALE + 2))
        bin_lbl = font.render(str(binary[i]) if binary else "", True, color)
        surface.blit(bin_lbl, (x - bin_lbl.get_width() // 2, y - SCALE - 10))

def new_parts():
    return random.choices(range(len(ROBOT_PARTS)), k=len(TREE_LAYOUT))

def all_paths():
    paths = []
    def dfs(node, current):
        current = current + [node]
        if node not in CHILDREN:
            paths.append(current)
        else:
            for child in CHILDREN[node]:
                dfs(child, current)
    dfs(0, [])
    return paths

def random_path():
    path = [0]
    node = 0
    while node in CHILDREN:
        node = random.choice(CHILDREN[node])
        path.append(node)
    return path

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Robot Tree (deep)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 9)

    parts = new_parts()
    binary = [1] * len(TREE_LAYOUT)
    if os.path.exists(BINARY_FILE):
        with open(BINARY_FILE, newline="") as f:
            binary = [int(x) for x in next(csv.reader(f))]
    bg = (0, 0, 0)
    nav_path = None
    nav_t = 0.0
    NAV_SPEED = 0.04
    seq_paths = []
    seq_idx = 0
    cmd_word = ""
    cmd_timer = 0
    mouse_pos = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                mouse_pos = None
                for i, (_, nx, ny) in enumerate(TREE_LAYOUT):
                    if math.hypot(mx - nx, my - ny) <= SCALE:
                        binary[i] = 1 - binary[i]
                        with open(BINARY_FILE, "w", newline="") as f:
                            csv.writer(f).writerow(binary)
                        mouse_pos = f"{ROBOT_PARTS[parts[i]][0]} ({mx}, {my})"
                        break
                if mouse_pos is None:
                    mouse_pos = f"({mx}, {my})"
            if event.type == pygame.KEYDOWN:
                cmd_map = {
                    pygame.K_r: "randomize", pygame.K_b: "toggle",
                    pygame.K_n: "navigate", pygame.K_s: "save",
                    pygame.K_t: "traverse", pygame.K_l: "load",
                    pygame.K_1: "load 1", pygame.K_2: "load 2", pygame.K_3: "load 3",
                    pygame.K_4: "load 4", pygame.K_5: "load 5", pygame.K_6: "load 6",
                }
                if event.key in cmd_map:
                    cmd_word = cmd_map[event.key]
                    cmd_timer = pygame.time.get_ticks()
                if event.key == pygame.K_r:
                    parts = new_parts()
                elif event.key == pygame.K_b:
                    bg = (255, 255, 255) if bg == (0, 0, 0) else (0, 0, 0)
                elif event.key == pygame.K_n:
                    nav_path = random_path()
                    nav_t = 0.0
                elif event.key == pygame.K_s:
                    with open(CSV_FILE, "w", newline="") as f:
                        csv.writer(f).writerow(parts)
                elif event.key == pygame.K_t:
                    if not seq_paths or seq_idx >= len(seq_paths):
                        seq_paths = all_paths()
                        seq_idx = 0
                    nav_path = seq_paths[seq_idx]
                    nav_t = 0.0
                elif event.key == pygame.K_l:
                    if os.path.exists(CSV_FILE):
                        with open(CSV_FILE, newline="") as f:
                            parts = [int(x) for x in next(csv.reader(f))]
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                    n = event.key - pygame.K_0
                    path = os.path.join(os.path.dirname(__file__), f"robot_tree_deep{n}.csv")
                    if os.path.exists(path):
                        with open(path, newline="") as f:
                            parts = [int(x) for x in next(csv.reader(f))]

        screen.fill(bg)
        draw_tree(screen, parts, font, binary)

        if nav_path:
            nav_t += NAV_SPEED
            seg = int(nav_t)
            if seg >= len(nav_path) - 1:
                seq_idx += 1
                nav_path = None
            else:
                frac = nav_t - seg
                _, x0, y0 = TREE_LAYOUT[nav_path[seg]]
                _, x1, y1 = TREE_LAYOUT[nav_path[seg + 1]]
                bx = int(x0 + (x1 - x0) * frac)
                by = int(y0 + (y1 - y0) * frac)
                pygame.draw.circle(screen, (255, 220, 50), (bx, by), 5)

        if mouse_pos:
            coord_lbl = font.render(mouse_pos, True, (200, 200, 200))
            screen.blit(coord_lbl, (10, 25))

        if cmd_word and pygame.time.get_ticks() - cmd_timer < 500:
            cmd_lbl = font.render(cmd_word, True, (200, 200, 200))
            screen.blit(cmd_lbl, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
