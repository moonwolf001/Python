# (c)2024 MoonWolf / pygame 2D Game 敵と自分だけ。
# 弾はスペースキー。当たり判定はこれから実装。

import pygame
import sys
import random
import math

# 初期設定
width, height = 800, 600
background_color = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# 自機設定
PLAYER_SIZE = 20
PLAYER_OUTER_COLOR = (255, 255, 255)
PLAYER_INNER_COLOR = (0, 0, 255)
PLAYER_BORDER_WIDTH = 8

# ミサイル設定
MISSILE_WIDTH = 4
MISSILE_LENGTH = 20
MISSILE_SPEED = 10
MISSILE_COLOR = (255, 0, 0)
MISSILE_FIRE_RATE = 5  # Frames between missiles

# ゲーム設定
ENEMY_START_X_MIN = 380
ENEMY_START_X_MAX = 400
ENEMY_START_Y_MIN = -300
ENEMY_START_Y_MAX = 399
PYRAMID_SIZE_MIN = 8
PYRAMID_SIZE_MAX = 30
CUBOID_SIZE_MIN = 8
CUBOID_SIZE_MAX = 30
ROTATION_SPEED_MIN = 0.01
ROTATION_SPEED_MAX = 0.1
PYRAMID_MOVEMENT_SPEED_MIN = 1
PYRAMID_MOVEMENT_SPEED_MAX = 2
CUBOID_MOVEMENT_SPEED_MIN = 2
CUBOID_MOVEMENT_SPEED_MAX = 4
PYRAMID_COUNT = 10
CUBOID_COUNT = 10

def rotate(points, angle_x, angle_y, angle_z):
    """ Rotate points in 3D space """
    angle_x, angle_y, angle_z = math.radians(angle_x), math.radians(angle_y), math.radians(angle_z)
    sin_x, cos_x = math.sin(angle_x), math.cos(angle_x)
    sin_y, cos_y = math.sin(angle_y), math.cos(angle_y)
    sin_z, cos_z = math.sin(angle_z), math.cos(angle_z)

    rotated = []
    for x, y, z in points:
        x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
        x, z = x * cos_y + z * sin_y, z * cos_y - x * sin_y
        y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
        rotated.append((x, y, z))
    return rotated

def project(points):
    """ Convert 3D points to 2D projection """
    return [(int(x + width / 2), int(y + height / 2)) for x, y, z in points]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = [width - 50, height // 2]
        self.image = pygame.Surface((2 * PLAYER_SIZE, 2 * PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_OUTER_COLOR, (PLAYER_SIZE, PLAYER_SIZE), PLAYER_SIZE, PLAYER_BORDER_WIDTH)
        pygame.draw.circle(self.image, PLAYER_INNER_COLOR, (PLAYER_SIZE, PLAYER_SIZE), PLAYER_SIZE - PLAYER_BORDER_WIDTH)
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.position[0], self.position[1] = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(center=self.position)

class Missile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((MISSILE_LENGTH, MISSILE_WIDTH))
        self.image.fill(MISSILE_COLOR)
        self.rect = self.image.get_rect(midleft=pos)

    def update(self):
        self.rect.x += MISSILE_SPEED
        if self.rect.x > width:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, size, rotation_speed_x, rotation_speed_y, rotation_speed_z, movement_speed):
        super().__init__()
        self.type = type
        self.size = size
        self.rotation_speed = (rotation_speed_x, rotation_speed_y, rotation_speed_z)
        self.movement_speed = movement_speed
        self.position = (random.uniform(ENEMY_START_X_MIN, ENEMY_START_X_MAX), random.uniform(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.color = (255, 255, 0) if type == 'Pyramid' else (0, 128, 0)

        if self.type == 'Pyramid':
            self.points = [
                (0, -size, 0),  # Apex
                (-size, size, -size),  # Base vertices
                (size, size, -size),
                (size, size, size),
                (-size, size, size),
            ]
        elif self.type == 'Cuboid':
            h = size
            self.points = [
                (-h, -h, -h), (h, -h, -h), (h, -h, h), (-h, -h, h),
                (-h, h, -h), (h, h, -h), (h, h, h), (-h, h, h)
            ]

    def update(self):
        self.angle_x += self.rotation_speed[0]
        self.angle_y += self.rotation_speed[1]
        self.angle_z += self.rotation_speed[2]
        self.position = (self.position[0] - self.movement_speed, self.position[1])
        if self.position[0] < -400:
            self.position = (random.uniform(ENEMY_START_X_MIN, ENEMY_START_X_MAX), random.uniform(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))

    def draw(self):
        rotated = rotate(self.points, self.angle_x, self.angle_y, self.angle_z)
        projected = project([(x + self.position[0], y + self.position[1], z) for x, y, z in rotated])
        edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                 (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)] if self.type == 'Cuboid' else [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)]
        for start, end in edges:
            pygame.draw.line(screen, self.color, projected[start], projected[end], 2)

# 自機とミサイルの初期化
player = Player()
missiles = pygame.sprite.Group()
shoot_timer = 0

# 敵の生成
enemies = pygame.sprite.Group()
for _ in range(PYRAMID_COUNT):
    enemies.add(Enemy('Pyramid', random.randint(PYRAMID_SIZE_MIN, PYRAMID_SIZE_MAX),
                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                      random.uniform(PYRAMID_MOVEMENT_SPEED_MIN, PYRAMID_MOVEMENT_SPEED_MAX)))
for _ in range(CUBOID_COUNT):
    enemies.add(Enemy('Cuboid', random.randint(CUBOID_SIZE_MIN, CUBOID_SIZE_MAX),
                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                      random.uniform(CUBOID_MOVEMENT_SPEED_MIN, CUBOID_MOVEMENT_SPEED_MAX)))

# ゲームのメインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if shoot_timer <= 0:
                for _ in range(5):  # 5連射のミサイル
                    missiles.add(Missile(player.rect.midright))
                shoot_timer = MISSILE_FIRE_RATE

    screen.fill(background_color)

    # 自機とミサイルの更新
    player.update()
    screen.blit(player.image, player.rect)

    if shoot_timer > 0:
        shoot_timer -= 1

    missiles.update()
    missiles.draw(screen)

    # 敵の更新
    for enemy in enemies:
        enemy.update()
        enemy.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
