# (c)2024 MoonWolf / ボールバウンド・シミュレーション
# pipにより、pygameの取り込みが必要です

import pygame
import sys

# 初期設定
width, height = 800, 400  # ウィンドウのサイズ
background_color = (0, 0, 0)  # 背景色（黒）
ball_color = (255, 255, 0)  # ボールの色（黄色）
initial_velocity = 5  # 初速度
horizontal_speed = 5  # X方向の速度
gravity = 0.5  # 重力加速度
elasticity = 0.8  # 床とのバウンドの懸垂率
wall_damping = 0.8  # 壁への衝突の減衰率
floor_friction = 0.99  # 床を転がるときの摩擦抵抗

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# ボールの初期位置と速度
ball_pos = [50, 50]
ball_vel = [horizontal_speed, initial_velocity]

def move_ball():
    # 重力の影響を受ける
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # 床との衝突判定
    if ball_pos[1] >= height - 10:  # ボールの直径を考慮
        ball_vel[1] = -ball_vel[1] * elasticity
        ball_pos[1] = height - 10
        ball_vel[0] *= floor_friction  # 床に摩擦が働く

    # 壁との衝突判定
    if ball_pos[0] >= width - 10 or ball_pos[0] <= 0:
        ball_vel[0] = -ball_vel[0] * wall_damping

# ゲームのメインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_ball()
    screen.fill(background_color)
    pygame.draw.circle(screen, ball_color, [int(ball_pos[0]), int(ball_pos[1])], 10)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
