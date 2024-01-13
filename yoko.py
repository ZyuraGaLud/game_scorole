import pygame as pg
import sys
import random



# Pygameの初期化
pg.init()

# ゲーム画面の設定
screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("横スクロールゲーム")

# 背景の設定
background_image = pg.image.load("sky.jpg")
background_image = pg.transform.scale(background_image, (screen_width, screen_height))

# プレイヤーキャラクターの設定
player_width = 50
player_height = 50
player_x = 50
player_y = screen_height // 2 - player_height // 2
player_speed = 5

# プレイヤーキャラクターの画像を読み込む
player_image = pg.image.load("enemy.png")
player_image = pg.transform.scale(player_image, (player_width, player_height))

# 敵の設定
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# 敵の画像を読み込む
enemy_image = pg.image.load("yurei_03.png")
enemy_image = pg.transform.scale(enemy_image, (enemy_width, enemy_height))



# 時間を表示するためのフォントの設定
font = pg.font.Font(None, 36)
clock = pg.time.Clock()

# ゲームの状態を管理する変数
elapsed_time = 0
enemy_speed_increase_interval = 30  # 敵の速度を増加させる間隔（秒）
current_speed_increase_time = 0

# reset_game関数の定義
def reset_game():
    global player_x, player_y, enemies, elapsed_time
    player_x = 50
    player_y = screen_height // 2 - player_height // 2
    enemies = []
    elapsed_time = 0

# ゲームループ
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # キー入力処理
    keys = pg.key.get_pressed()
    if keys[pg.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pg.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed

    # 敵の生成
    if random.randint(0, 100) < 5:  # 5%の確率で敵を生成
        enemy_y = random.randint(0, screen_height - enemy_height)
        enemies.append({'x': screen_width, 'y': enemy_y})

    # 敵の更新
    for enemy in enemies:
        enemy['x'] -= enemy_speed

        if (
            player_x < enemy['x'] + enemy_width and
            player_x + player_width > enemy['x'] and
            player_y < enemy['y'] + enemy_height and
            player_y + player_height > enemy['y']
        ):
            reset_game()

    # 背景の描画
    screen.blit(background_image, (0, 0))

    # プレイヤーの描画
    screen.blit(player_image, (player_x, player_y))

    # 敵の描画
    for enemy in enemies:
        screen.blit(enemy_image, (enemy['x'], enemy['y']))

    elapsed_time = pg.time.get_ticks() // 1000  # ミリ秒から秒に変換

    text_surface = font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

# 敵の速度を30秒ごとに増加
    if elapsed_time > current_speed_increase_time + enemy_speed_increase_interval:
        enemy_speed += 1
        current_speed_increase_time = elapsed_time


    # ゲーム画面の更新
    pg.display.flip()

    # フレームレートの制御
    clock.tick(60)
