# Разработать игру.
#
# Примеры игр:
#
# пинг-понг
# змейка
# тетрис
# игра на выживание с постоянным передвижением, где на поле постоянно появляются “враги”, которых нельзя касаться

import pygame
import random

# 1. Инициализация Pygame и настройка поля
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тетрис")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Формы тетромино
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # J
    [[1, 1, 1], [0, 0, 1]],  # L
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, BLUE, ORANGE, GREEN, RED]

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

clock = pygame.time.Clock()
FPS = 60
current_piece = None
next_piece = None
score = 0
game_over = False


# 2. Функция создания новой фигуры
def new_piece():
    shape = random.choice(SHAPES)
    color = SHAPE_COLORS[SHAPES.index(shape)]
    piece = {
        "shape": shape,
        "color": color,
        "x": GRID_WIDTH // 2 - len(shape[0]) // 2,
        "y": 0
    }
    return piece


current_piece = new_piece()
next_piece = new_piece()


# 3. Проверка столкновений
def check_collision(piece, grid, dx=0, dy=0):
    for y, row in enumerate(piece["shape"]):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece["x"] + x + dx
                new_y = piece["y"] + y + dy
                if (new_x < 0 or new_x >= GRID_WIDTH or
                        new_y >= GRID_HEIGHT or
                        (new_y >= 0 and grid[new_y][new_x])):
                    return True
    return False


# 4. Поворот фигуры
def rotate_piece(piece, grid):
    rotated = [list(row) for row in zip(*piece["shape"][::-1])]
    old_shape = piece["shape"]
    piece["shape"] = rotated
    if check_collision(piece, grid):
        piece["shape"] = old_shape


# 5. Очистка линий
def clear_lines(grid):
    lines_cleared = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            lines_cleared += 1
            for y2 in range(y, 0, -1):
                grid[y2] = grid[y2 - 1][:]
            grid[0] = [0] * GRID_WIDTH
    return lines_cleared


# 6. Основной игровой цикл
fall_time = 0
fall_speed = 0.5

running = True
while running:
    dt = clock.tick(FPS) / 1000
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(current_piece, grid, dx=-1):
                current_piece["x"] -= 1
            if event.key == pygame.K_RIGHT and not check_collision(current_piece, grid, dx=1):
                current_piece["x"] += 1
            if event.key == pygame.K_DOWN and not check_collision(current_piece, grid, dy=1):
                current_piece["y"] += 1
            if event.key == pygame.K_UP:
                rotate_piece(current_piece, grid)

    if fall_time >= fall_speed:
        fall_time = 0
        if not check_collision(current_piece, grid, dy=1):
            current_piece["y"] += 1
        else:
            for y, row in enumerate(current_piece["shape"]):
                for x, cell in enumerate(row):
                    if cell and current_piece["y"] + y >= 0:
                        grid[current_piece["y"] + y][current_piece["x"] + x] = current_piece["color"]

            lines = clear_lines(grid)
            score += lines * 100

            current_piece = next_piece
            next_piece = new_piece()
            if check_collision(current_piece, grid):
                game_over = True

    screen.fill(BLACK)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                                 (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    for y, row in enumerate(current_piece["shape"]):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_piece["color"],
                                 ((current_piece["x"] + x) * GRID_SIZE,
                                  (current_piece["y"] + y) * GRID_SIZE,
                                  GRID_SIZE - 1, GRID_SIZE - 1))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    screen.blit(score_text, (GRID_WIDTH * GRID_SIZE + 20, 20))

    pygame.display.flip()

pygame.quit()