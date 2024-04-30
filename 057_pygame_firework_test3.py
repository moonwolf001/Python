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
FIREWORK_RADIUS_MULTIPLIERS = [5, 4, 8]  # 各破裂段階の初速度係数
FIREWORK_TIMINGS = [500, 300, 600]  # 各段階の破裂タイミング (ミリ秒)
FIREWORK_PARTICLE_COUNTS = [100, 150, 300]  # 各段階のパーティクル数
PARTICLE_LIFE_SPANS = [4, 3, 5]  # 各破裂段階のパーティクル寿命 (秒)
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
        self.particles = [[] for _ in range(3)]
        self.current_stage = 0
        self.last_update = pygame.time.get_ticks()
        self.burst_stage(0)  # 初期破裂

    def burst_stage(self, stage):
        color_list = self.stages[stage]
        num_particles = FIREWORK_PARTICLE_COUNTS[stage]
        lifespan = PARTICLE_LIFE_SPANS[stage]
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 10) * FIREWORK_RADIUS_MULTIPLIERS[stage]
            color = pygame.Color(random.choice(color_list))
            self.particles[stage].append(Particle(self.x, self.y, angle, speed, color, lifespan))

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if self.current_stage < 2 and (current_time - self.last_update > FIREWORK_TIMINGS[self.current_stage]):
            self.current_stage += 1
            self.burst_stage(self.current_stage)
            self.last_update = current_time
        
        for stage_particles in self.particles:
            for particle in stage_particles:
                particle.update(dt)

        for i in range(len(self.particles)):
            self.particles[i] = [p for p in self.particles[i] if p.is_alive()]

        if all(len(stage) == 0 for stage in self.particles):
            return False
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
        pygame.draw.circle(screen, 'white', (x, y), size)

    current_time = pygame.time.get_ticks()
    if len(fireworks) < MAX_FIREWORKS_DISPLAYED and current_time > next_firework_timing:
        x = random.randint(WIDTH // 4, 3 * WIDTH // 4)
        y = random.randint(HEIGHT // 4, HEIGHT // 3)
        fireworks.append(Firework(x, y))
        next_firework_timing = current_time + random.randint(500, 1500)  # Reduce the interval for more frequent fireworks

    fireworks = [fw for fw in fireworks if fw.update(dt)]
    for firework in fireworks:
        for stage_particles in firework.particles:
            for particle in stage_particles:
                pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), 3)

    pygame.display.flip()