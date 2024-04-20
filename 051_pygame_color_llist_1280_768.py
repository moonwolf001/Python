#(c)2024 MoonWolf // Python pygame 1280 x 768 color list
#解像度 1280x768 にて一画面で、100色程度の色と英語でのその呼び名を知ることができます
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
    screen_width, screen_height = 1280, 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Python pygame color list for 1280x768")

    font = pygame.font.Font(None, 24)
    color_boxes = []
    box_width, box_height = 160, 42  # ボックスの幅と新しい高さ
    boxes_per_row = screen_width // box_width

    for i, color in enumerate(colors):
        x = (i % boxes_per_row) * box_width
        y = (i // boxes_per_row) * box_height
        box_rect = pygame.Rect(x, y, box_width, box_height)
        text_surface = font.render(color, True, (0, 0, 0), (255, 255, 255))
        color_boxes.append((box_rect, color, text_surface))

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # 白で画面をクリア

        for box, color, text in color_boxes:
            pygame.draw.rect(screen, pygame.Color(color), box)  # 色でボックスを塗る
            text_bg_rect = pygame.Rect(box.x, box.y + box.height - 20, box.width, 20)  # テキスト背景
            pygame.draw.rect(screen, (255, 255, 255), text_bg_rect)  # 白背景
            text_rect = text.get_rect(center=(text_bg_rect.x + text_bg_rect.width // 2, text_bg_rect.y + text_bg_rect.height // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
