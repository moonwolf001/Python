import pygame
import random
import math
from pygame.locals import *
import sys

# 画面設定
WIDTH, HEIGHT = 800, 600
SCREEN_TITLE = "Fireworks Show"

# 花火の設定
MAX_FIREWORKS_DISPLAYED = 5  # 画面に同時に表示する花火の最大数
FIREWORK_RADIUS_MULTIPLIERS = [5, 4, 8]  # 各破裂段階の初速度係数（大きいほど広がりが大きくなる）
FIREWORK_TIMINGS = [500, 300, 600]  # 各段階の破裂タイミング (ミリ秒)
FIREWORK_PARTICLE_COUNTS = [100, 150, 300]  # 各段階のパーティクル数
PARTICLE_LIFE_SPANS = [4, 3, 5]  # 各破裂段階のパーティクル寿命 (秒)
PARTICLE_GRAVITY = 50  # パーティクルに作用する重力
PARTICLE_FRICTION = 0.99  # パーティクルの速度減衰率

# 星の設定
STAR_COUNT = 30  # 星の数
STAR_SIZE_MIN = 1  # 星の最小サイズ
STAR_SIZE_MAX = 2  # 星の最大サイズ

# 色の設定
COLORS = {
    'Color1': ['ghostwhite', 'lightyellow', 'palevioletred', 'springgreen', 'dodgerblue'],
    'Color2': ['orangered', 'coral', 'orchid', 'lime', 'steelblue'],
    'Color3': ['greenyellow', 'seagreen', 'aqua', 'ghostwhite', 'lavender']
}

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# 星の生成
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2), random.randint(STAR_SIZE_MIN, STAR_SIZE_MAX)) for _ in range(STAR_COUNT)]

# パーティクルクラス
class Particle:
    def __init__(self, x, y, angle, speed, color, lifespan):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.time_alive = 0
        self.vy = 0  # 垂直方向の速度（初期値は0）
        self.lifespan = lifespan

    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt + self.vy * dt
        self.vy += PARTICLE_GRAVITY * dt  # 重力を追加
        self.speed *= PARTICLE_FRICTION  # 空気抵抗で速度が減少
        self.time_alive += dt

    def is_alive(self):
        return self.time_alive < self.lifespan

# 花火クラス
class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stages = [COLORS['Color1'], COLORS['Color2'], COLORS['Color3']]
        self.current_stage = 0
        self.particles = []
        self.burst_stage()

    def burst_stage(self):
        color_list = self.stages[self.current_stage]
        num_particles = FIREWORK_PARTICLE_COUNTS[self.current_stage]
        lifespan = PARTICLE_LIFE_SPANS[self.current_stage]
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 10) * FIREWORK_RADIUS_MULTIPLIERS[self.current_stage]
            color = pygame.Color(random.choice(color_list))
            self.particles.append(Particle(self.x, self.y, angle, speed, color, lifespan))

    def update(self, dt):
        if not self.particles:
            self.current_stage += 1
            if self.current_stage < len(self.stages):
                self.burst_stage()
            else:
                return False  # No more stages, remove this firework
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update(dt)
        return True

# 背景描画関数
def draw_background():
    for y in range(HEIGHT):
        inter_color = pygame.Color(0, 0, 0)
        inter_color.lerp(pygame.Color('midnightblue'), y / HEIGHT)
        pygame.draw.line(screen, inter_color, (0, y), (WIDTH, y))

# 花火リストとタイマーの初期化
fireworks = []
next_firework_timing = pygame.time.get_ticks() + random.randint(500, 1000)

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
        pygame.draw.circle(screen, 'cornsilk', (x, y), size)

    if len(fireworks) < MAX_FIREWORKS_DISPLAYED and pygame.time.get_ticks() > next_firework_timing:
        x = random.randint(WIDTH // 4, 3 * WIDTH // 4)
        y = random.randint(HEIGHT // 4, HEIGHT // 3)  # 上部に花火が表示されるように調整
        fireworks.append(Firework(x, y))
        next_firework_timing = pygame.time.get_ticks() + random.randint(1000, 3000)  # 次の花火までの間隔をランダムに設定

    fireworks = [fw for fw in fireworks if fw.update(dt)]

    for firework in fireworks:
        for particle in firework.particles:
            pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), 3)

    pygame.display.flip()
