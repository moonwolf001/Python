#(c)2024 MoonWolf / 敵が右から流れてくる
#回転する敵の表現が未熟

import pygame
import sys
import random
from pygame.math import Vector2

# 初期設定
width, height = 800, 600
background_color = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# 敵の設定
enemy_counts = {'Pyramid': 5, 'Sphere': 5, 'Cuboid': 5, 'Octahedron': 5}
enemy_colors = {'Pyramid': (255, 255, 0), 'Sphere': (192, 192, 192), 'Cuboid': (0, 128, 0), 'Octahedron': (0, 0, 255)}


# 敵クラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.color = enemy_colors[type]
        self.rotation_speed = random.uniform(0.1, 0.5) * random.choice([-1, 1])
        self.speed = random.uniform(1, 4)
        self.position = Vector2(width, random.uniform(0, height))
        self.angle = 0
        self.scale = random.uniform(0.5, 3)

    def update(self):
        self.angle += self.rotation_speed
        self.position.x -= self.speed
        if self.position.x < -50:  # 画面外に出たらリセット
            self.position = Vector2(width, random.uniform(0, height))

    def draw(self):
        if self.type == 'Sphere':
            center = (int(self.position.x), int(self.position.y))
            radius = int(20 * self.scale)
            pygame.draw.circle(screen, self.color, center, radius)
            # 回転が分かるデザインを追加
            offset = Vector2(radius, 0).rotate(-self.angle)
            pygame.draw.circle(screen, (255, 0, 0), center + offset, 5)
        elif self.type == 'Pyramid':
            points = [Vector2(0, -20 * self.scale), Vector2(-15 * self.scale, 15 * self.scale),
                      Vector2(15 * self.scale, 15 * self.scale)]
            rotated_points = [Vector2(p).rotate(self.angle) + self.position for p in points]
            pygame.draw.polygon(screen, self.color, rotated_points)
        elif self.type == 'Cuboid':
            points = [Vector2(-20 * self.scale, -10 * self.scale), Vector2(20 * self.scale, -10 * self.scale),
                      Vector2(20 * self.scale, 10 * self.scale), Vector2(-20 * self.scale, 10 * self.scale)]
            rotated_points = [Vector2(p).rotate(self.angle) + self.position for p in points]
            pygame.draw.polygon(screen, self.color, rotated_points)
        elif self.type == 'Octahedron':
            points = [Vector2(0, -20 * self.scale), Vector2(-15 * self.scale, 0), Vector2(0, 20 * self.scale),
                      Vector2(15 * self.scale, 0)]
            rotated_points = [Vector2(p).rotate(self.angle) + self.position for p in points]
            pygame.draw.polygon(screen, self.color, rotated_points)


# 敵の生成
enemies = pygame.sprite.Group()
for type in enemy_counts:
    for _ in range(enemy_counts[type]):
        enemies.add(Enemy(type))

# ゲームのメインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    enemies.update()  # 敵の更新
    for enemy in enemies:
        enemy.draw()  # 敵の描画
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
