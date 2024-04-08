import tkinter as tk
import random

def draw_shapes():
    canvas_width = 600
    canvas_height = 400

    root = tk.Tk()
    root.title("Random Shapes")
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # 描画の継続を制御するフラグ
    continue_drawing = True

    def random_shape():
        if not continue_drawing:
            return  # 描画を停止

        shapes = ['circle', 'oval', 'rectangle', 'square']
        shape = random.choice(shapes)
        color = "#" + ''.join(random.choices('0123456789ABCDEF', k=6))

        x1 = random.randint(0, canvas_width - 100)
        y1 = random.randint(0, canvas_height - 100)
        x2 = x1 + random.randint(50, 100)
        y2 = y1 + random.randint(50, 100)

        if shape == 'circle' or shape == 'oval':
            canvas.create_oval(x1, y1, x2, y2, outline=color, fill=color)
        elif shape == 'rectangle':
            canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=color)
        elif shape == 'square':
            side = min(x2 - x1, y2 - y1)
            canvas.create_rectangle(x1, y1, x1 + side, y1 + side, outline=color, fill=color)

        root.after(30, random_shape)

    def stop_drawing(event):
        nonlocal continue_drawing
        continue_drawing = False

    # スペースキーを押すと描画を停止するイベントハンドラーを設定
    root.bind("<space>", stop_drawing)

    random_shape()
    root.mainloop()

draw_shapes()
