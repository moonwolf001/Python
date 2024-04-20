import pygame
import sys

# 色のリスト
colors = [
    "snow", "ghost white", "white smoke", "gainsboro", "floral white",
    "old lace", "linen", "antique white", "papaya whip", "blanched almond",
    "bisque", "peach puff", "navajo white", "lemon chiffon", "mint cream",
    "azure", "alice blue", "lavender", "lavender blush", "misty rose",
    "ivory", "beige", "cornsilk", "seashell", "honeydew",
    "light yellow", "light goldenrod yellow", "#F7E7CE", "#FFE5B4", "wheat",
    "moccasin", "khaki", "plum", "light coral", "salmon",
    "dark salmon", "light salmon", "coral", "tomato", "orange red",
    "red", "hot pink", "deep pink", "pink", "light pink",
    "pale violet red", "maroon", "medium violet red", "violet red", "magenta",
    "violet", "plum", "orchid", "medium orchid", "dark orchid",
    "dark violet", "blue violet", "purple", "medium purple", "thistle",
    "green yellow", "chartreuse", "lawn green", "lime", "lime green",
    "pale green", "light green", "medium spring green", "spring green", "medium sea green",
    "sea green", "forest green", "green", "dark green", "yellow green",
    "olive drab", "olive", "dark olive green", "medium aquamarine", "dark sea green",
    "light sea green", "dark cyan", "teal", "aqua", "light cyan",
    "pale turquoise", "aquamarine", "turquoise", "medium turquoise", "dark turquoise",
    "cadet blue", "steel blue", "light steel blue", "powder blue", "light blue",
    "sky blue", "light sky blue", "deep sky blue", "dodger blue", "cornflower blue",
    "medium slate blue", "royal blue", "blue", "medium blue", "dark blue",
    "navy", "midnight blue", "cyan", "blue", "indigo"
]

def run():
    pygame.init()
    screen_width, screen_height = 820, 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("スクロール可能な色の一覧")

    font = pygame.font.Font(None, 24)
    color_boxes = []
    start_y = 0  # スクロールの開始位置
    total_height = 10 + 70 * ((len(colors) - 1) // 5 + 1)  # 全体の高さ

    for i, color in enumerate(colors):
        x = (i % 5) * 160 + 10
        y = (i // 5) * 70 + 10
        box_rect = pygame.Rect(x, y, 150, 60)
        text_surface = font.render(color, True, (0, 0, 0))
        text_bg_rect = pygame.Rect(x, y + 40, 150, 20)
        color_boxes.append((box_rect, text_bg_rect, color, text_surface))

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                start_y += event.y * 30
                if start_y > 0:
                    start_y = 0
                elif start_y < screen_height - total_height:
                    start_y = screen_height - total_height

        screen.fill((255, 255, 255))  # 白で画面をクリア

        for box, text_bg_rect, color, text in color_boxes:
            box_moved = box.move(0, start_y)
            text_bg_moved = text_bg_rect.move(0, start_y)
            if box_moved.top > -70 and box_moved.bottom < screen_height + 70:
                pygame.draw.rect(screen, pygame.Color(color), box_moved)
                pygame.draw.rect(screen, (255, 255, 255), text_bg_moved)  # 白背景のテキストエリア
                text_rect = text.get_rect(center=text_bg_moved.center)
                screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
