##########################################################################
# (c)2024 MoonWolf（むーんうるふ） 
# pygame レトロ横スクロール 2D Game, Version 001  
# ゲーム操作：マウスで自分を動かす、スペースキーで弾を撃つ
# 本プログラムには、pip pygame　が必要
# 書籍 MoonWolfと学ぶPythonシリーズ 第4巻 レトロゲーム編
# 上記書籍によりプログラムの詳細を説明
# MoonWolf著作：https://www.amazon.co.jp/stores/MoonWolf/author/B0CD3151FX
# このコメントを残す限り、本プログラムを自由に使うことを許可します
# ご意見等、ツイッター（X）でのDM歓迎。https://twitter.com/MoonWolf_001
##########################################################################

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
font = pygame.font.Font(None, 74)  # ゲームオーバーテキスト用のフォント
small_font = pygame.font.Font(None, 36)  # スコア表示用の小さいフォント

# スコア
score = 0

# 自機設定
PLAYER_SIZE = 20
PLAYER_OUTER_COLOR = (255, 255, 255)
PLAYER_INNER_COLOR = (0, 0, 255)
PLAYER_BORDER_WIDTH = 8

# ミサイル設定
MISSILE_WIDTH = 4
MISSILE_LENGTH = 20
MISSILE_SPEED = 12
MISSILE_COLOR = (255, 0, 0)
MISSILE_FIRE_RATE = 5  # ミサイル発射間隔

# ゲーム設定
ENEMY_START_X_MIN = 380
ENEMY_START_X_MAX = 400
ENEMY_START_Y_MIN = -300
ENEMY_START_Y_MAX = 300
PYRAMID_SIZE_MIN = 15
PYRAMID_SIZE_MAX = 35
CUBOID_SIZE_MIN = 15
CUBOID_SIZE_MAX = 35
ROTATION_SPEED_MIN = 0.01
ROTATION_SPEED_MAX = 0.1
PYRAMID_MOVEMENT_SPEED_MIN = 1
PYRAMID_MOVEMENT_SPEED_MAX = 5
CUBOID_MOVEMENT_SPEED_MIN = 2
CUBOID_MOVEMENT_SPEED_MAX = 7
PYRAMID_COUNT = 10
CUBOID_COUNT = 10

# 衝突判定の調整定数
PYRAMID_COLLISION_FACTOR = 1.0
CUBOID_COLLISION_FACTOR = 1.3

# 星の設定
star_color = (0, 200, 200)  # 星の色（シアン）
star_count = 500  # 画面上の星の数
min_star_speed = 1  # 星の最小速度
max_star_speed = 2  # 星の最大速度
stars = []

def create_star():
    radius = random.randint(1, 2)
    x = random.randint(0, width)
    y = random.randint(0, height)
    speed = random.randint(min_star_speed, max_star_speed)
    return {'radius': radius, 'x': x, 'y': y, 'speed': speed}

stars = [create_star() for _ in range(star_count)]

def move_stars():
    global stars
    for star in stars:
        star['x'] -= star['speed']
    stars = [star for star in stars if star['x'] > -star['radius']]
    while len(stars) < star_count:
        stars.append(create_star())

def rotate(points, angle_x, angle_y, angle_z):
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
    return [(int(x + width / 2), int(y + height / 2)) for x, y, z in points]

def check_collision(missile, enemy):
    missile_center = (missile.rect.centerx, missile.rect.centery)
    enemy_center = (enemy.position[0] + width / 2, enemy.position[1] + height / 2)
    distance = math.sqrt((missile_center[0] - enemy_center[0]) ** 2 + (missile_center[1] - enemy_center[1]) ** 2)
    if enemy.type == 'Pyramid':
        collision_distance = enemy.size * PYRAMID_COLLISION_FACTOR
    else:
        collision_distance = enemy.size * CUBOID_COLLISION_FACTOR
    return distance < collision_distance

def check_player_collision(player, enemy):
    player_center_x, player_center_y = player.rect.center
    enemy_center_x, enemy_center_y = enemy.position[0] + width // 2, enemy.position[1] + height // 2
    distance = math.sqrt((player_center_x - enemy_center_x) ** 2 + (player_center_y - enemy_center_y) ** 2)
    collision_radius = PLAYER_SIZE + enemy.size * (PYRAMID_COLLISION_FACTOR if enemy.type == 'Pyramid' else CUBOID_COLLISION_FACTOR)
    return distance < collision_radius

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
        self.color = (255, 255, 0) if type == 'Pyramid' else (159, 200, 255)
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

player = Player()
missiles = pygame.sprite.Group()
shoot_timer = 0  # ミサイル発射タイマーの初期化

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

game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                if shoot_timer <= 0:
                    for _ in range(5):  # 5連射のミサイル
                        missiles.add(Missile(player.rect.midright))
                    shoot_timer = MISSILE_FIRE_RATE

    move_stars()  # 星を移動させる
    screen.fill(background_color)

    # 星を描画
    for star in stars:
        pygame.draw.circle(screen, star_color, (star['x'], star['y']), star['radius'])

    # スコア表示
    score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

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

    # ミサイルと敵の当たり判定
    for missile in list(missiles):
        for enemy in list(enemies):
            if check_collision(missile, enemy):
                missile.kill()
                enemy.kill()
                score += 10  # スコア加算
                # 敵の再生成ロジック（ランダムに1機または2機追加）
                rand_value = random.randint(1, 1300)
                if rand_value <= 1000:
                    enemies.add(Enemy(enemy.type, random.randint(PYRAMID_SIZE_MIN, PYRAMID_SIZE_MAX),
                                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                                      random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                                      random.uniform(PYRAMID_MOVEMENT_SPEED_MIN, PYRAMID_MOVEMENT_SPEED_MAX)))
                elif 1001 <= rand_value <= 1300:
                    for _ in range(2):
                        enemies.add(Enemy(enemy.type, random.randint(PYRAMID_SIZE_MIN, PYRAMID_SIZE_MAX),
                                          random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                                          random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                                          random.uniform(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX),
                                          random.uniform(PYRAMID_MOVEMENT_SPEED_MIN, PYRAMID_MOVEMENT_SPEED_MAX)))

    # 自機と敵の当たり判定
    for enemy in enemies:
        if check_player_collision(player, enemy):
            game_over = True
            text = font.render('Game Over', True, (255, 0, 0))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
            score_display = font.render(f'Your Score: {score}', True, (255, 255, 255))
            score_rect = score_display.get_rect(center=(width // 2, height // 2 + 50))
            screen.blit(score_display, score_rect)
            break

    pygame.display.flip()
    clock.tick(60)

    if game_over:
        # ゲームオーバー後の処理
        text_restart = font.render('Hit Return Key to Restart', True, (255, 255, 255))
        text_restart_rect = text_restart.get_rect(center=(width // 2, height // 2 + 100))
        screen.blit(text_restart, text_restart_rect)
        pygame.display.flip()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # ゲーム再開
                        game_over = False
                        score = 0  # スコアリセット
                        #player.position = [80, height // 2]  # 自機の位置を画面左端にリセット
                        player = Player()
                        for enemy in list(enemies):
                            enemy.kill()
                        player = Player()
                        missiles = pygame.sprite.Group()
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
                        waiting_for_input = False
                    elif event.key == pygame.K_ESCAPE:
                        # ゲーム終了
                        running = False
                        waiting_for_input = False

pygame.quit()
sys.exit()
