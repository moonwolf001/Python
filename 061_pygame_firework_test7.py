# (c)2024 MoonWolf（むーんうるふ） // Python pygameにて花火大会 Part1
# pip により、外部ライブラリー　pygame　の取り込みが必要

import pygame
import random
import math
from pygame.locals import *
import sys
import time

# 画面設定
WIDTH, HEIGHT = 800, 600
SCREEN_TITLE = "Fireworks Show by MoonWolf, 2024"

# 乱数のシードを現在の時刻（ミリ秒）に設定
random.seed(time.time())

# 花火の破裂位置設定
FIREWORK_X_RANGE = (80, WIDTH - 80)  # X座標の破裂範囲
FIREWORK_Y_RANGE = (80, HEIGHT // 2 - 100)  # Y座標の破裂範囲（画面の上半分）

# 花火の表示数のシーケンス設定
FIREWORK_SEQUENCE = [(0, 1), (7000, 2), (14000, 3), (20000, 7),(30000, 20), (40000,0)]  # (開始時間ms, 表示最大数)

# 花火の設定
FIREWORK_RADIUS_MULTIPLIERS = [5, 6, 12]  # 各破裂段階の初速度係数
FIREWORK_TIMINGS = [500, 300, 600]  # 各段階の破裂タイミング (ミリ秒)
FIREWORK_PARTICLE_COUNTS = [100, 150, 400]  # 各段階のパーティクル数
PARTICLE_LIFE_SPANS = [4, 5, 7]  # 各破裂段階のパーティクル寿命 (秒)
PARTICLE_GRAVITY = 40  # パーティクルに作用する重力
PARTICLE_FRICTION = 0.992  # パーティクルの速度減衰率

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
            self.particles[i] = [p for p in self.particles[i] if p.is_alive()]  # Corrected syntax here

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


    def draw_background():
        top_color = pygame.Color('black')  # 画面上部の色
        bottom_color = pygame.Color('midnightblue')  # 画面下部の色
        for y in range(HEIGHT):
            # 画面の高さに応じて色を補間
            lerp_factor = y / HEIGHT
            blended_color = top_color.lerp(bottom_color, lerp_factor)
            pygame.draw.line(screen, blended_color, (0, y), (WIDTH, y))


    # ゲームループ内で背景を描画
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(30) / 1000
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        draw_background()  # 背景を描画
        for x, y, size in stars:
            pygame.draw.circle(screen, 'ivory', (x, y), size)

        current_time = pygame.time.get_ticks()
        max_fireworks_displayed = 1
        for time_threshold, count in sorted(FIREWORK_SEQUENCE, reverse=True):
            if current_time >= time_threshold:
                max_fireworks_displayed = count
                break

        if len(fireworks) < max_fireworks_displayed and current_time > next_firework_timing:
            x = random.randint(FIREWORK_X_RANGE[0], FIREWORK_X_RANGE[1])
            y = random.randint(FIREWORK_Y_RANGE[0], FIREWORK_Y_RANGE[1])
            fireworks.append(Firework(x, y))
            next_firework_timing = current_time + random.randint(300, 700)

        fireworks = [fw for fw in fireworks if fw.update(dt)]
        for firework in fireworks:
            for stage_particles in firework.particles:
                for particle in stage_particles:
                    pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), 3)

        pygame.display.flip()
