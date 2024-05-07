# (c)2024 MoonWolf / よこスクロールゲーム背景
# 上カーソルで速度アップ、下カーソールで速度ダウン

import pygame
import sys
import random

# 初期設定
width, height = 800, 600  # ウィンドウのサイズ
background_color = (0, 0, 0)  # 背景色（黒）
star_color = (0, 200, 200)  # 星の色（シアン）
star_count = 500  # 画面上の星の数
min_star_speed = 0.1  # 星の最小速度
max_star_speed = 0.5  # 星の最大速度

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# 星を生成する関数
def create_star():
    radius = random.randint(1, 2)
    x = random.randint(0, width)
    y = random.randint(0, height)
    speed = random.uniform(min_star_speed, max_star_speed) * radius
    return {'radius': radius, 'x': x, 'y': y, 'speed': speed}

# 星のリストを初期化
stars = [create_star() for _ in range(star_count)]

# 星を移動させる関数
def move_stars():
    global stars
    for star in stars:
        star['x'] -= star['speed']
    # 画面外に出た星をフィルターしてリストから削除
    stars = [star for star in stars if star['x'] > -star['radius']]
    # 画面上に星の数が規定数より少なければ追加
    while len(stars) < star_count:
        stars.append(create_star())

# 速度の調整を行う関数
def adjust_star_speed(new_min_speed, new_max_speed):
    global min_star_speed, max_star_speed
    min_star_speed = new_min_speed
    max_star_speed = new_max_speed
    for star in stars:
        star['speed'] = random.uniform(min_star_speed, max_star_speed) * star['radius']

# ゲームのメインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                adjust_star_speed(min_star_speed + 0.1, max_star_speed + 0.1)
            elif event.key == pygame.K_DOWN:
                adjust_star_speed(max(0, min_star_speed - 0.1), max(0, max_star_speed - 0.1))

    move_stars()
    screen.fill(background_color)
    for star in stars:
        pygame.draw.circle(screen, star_color, (star['x'], star['y']), star['radius'])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
