import pygame
import random
import math
from pygame.locals import *
import sys

# 画面設定
WIDTH, HEIGHT = 800, 600
SCREEN_TITLE = "Fireworks Show"

# 花火の設定
FIREWORK_RADIUS_MULTIPLIERS = [5, 4, 8]  # パーティクルの初速度係数（大きいほど広がりが大きくなる）
FIREWORK_TIMINGS = [500, 300, 600]  # 各段階の時間間隔 (ミリ秒)
FIREWORK_PARTICLE_COUNTS = [100, 150, 300]  # 各段階のパーティクル数
PARTICLE_LIFE_SPAN = 4  # パーティクルの寿命 (秒)
PARTICLE_GRAVITY = 50  # パーティクルに作用する重力
PARTICLE_FRICTION = 0.99  # パーティクルの速度減衰率

# 星の設定
STAR_COUNT = 50  # 星の数
STAR_SIZE_MIN = 1  # 星の最小サイズ
STAR_SIZE_MAX = 3  # 星の最大サイズ

# 色の設定
COLORS = {
    'Color1': ['ghostwhite', 'lightyellow', 'palevioletred', 'springgreen', 'dodgerblue'],
    'Color2': ['orangered', 'coral', 'orchid', 'lime', 'steelblue'],
    'Color3': ['greenyellow', 'seagreen', 'aqua', 'ghostwhite', 'lavender']
}

# Pygameの初期化
pygame.init()

# 画面の設定
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# 星の生成
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2), random.randint(STAR_SIZE_MIN, STAR_SIZE_MAX)) for _ in range(STAR_COUNT)]

# パーティクルクラス
class Particle:
    def __init__(self, x, y, angle, speed, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.time_alive = 0
        self.vy = 0  # 垂直方向の速度（初期値は0）

    def update(self, dt):
        # 物理演算に基づいた移動
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt + self.vy * dt
        self.vy += PARTICLE_GRAVITY * dt  # 重力を追加
        self.speed *= PARTICLE_FRICTION  # 空気抵抗で速度が減少

# 花火クラス
class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colors = [COLORS['Color1'], COLORS['Color2'], COLORS['Color3']]
        self.particles = []  # パーティクルリストの初期化
        self.stage = 0
        self.last_update = pygame.time.get_ticks()
        self.burst()

    def burst(self):
        color_list = self.colors[self.stage]
        num_particles = FIREWORK_PARTICLE_COUNTS[self.stage]
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 10) * FIREWORK_RADIUS_MULTIPLIERS[self.stage]
            color = pygame.Color(random.choice(color_list))
            self.particles.append(Particle(self.x, self.y, angle, speed, color))

    def update(self, dt):
        now = pygame.time.get_ticks()
        if now - self.last_update > FIREWORK_TIMINGS[self.stage] and self.stage < 2:
            self.stage += 1
            self.burst()
            self.last_update = now
        self.particles = [p for p in self.particles if p.time_alive < PARTICLE_LIFE_SPAN]
        for particle in self.particles:
            particle.update(dt)
            particle.time_alive += dt

# 背景描画関数
def draw_background():
    for y in range(HEIGHT):
        inter_color = pygame.Color(0, 0, 0)
        inter_color.lerp(pygame.Color('midnightblue'), y / HEIGHT)
        pygame.draw.line(screen, inter_color, (0, y), (WIDTH, y))

# 花火リストとタイマーの初期化
fireworks = []
next_firework = pygame.time.get_ticks() + random.randint(500, 1000)

# ゲームループ
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(30) / 1000
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    draw_background()
    for x, y, size in stars:
        pygame.draw.circle(screen, 'white', (x, y), size)

    if pygame.time.get_ticks() > next_firework:
        x = random.randint(0, WIDTH)
        y = random.randint(HEIGHT // 2, HEIGHT)
        fireworks.append(Firework(x, y))
        next_firework = pygame.time.get_ticks() + random.randint(1000, 2000)

    for firework in fireworks:
        firework.update(dt)
        for particle in firework.particles:
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), 3)

    pygame.display.flip()
