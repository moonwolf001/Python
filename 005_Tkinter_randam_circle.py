import tkinter as tk
import random

# ウィンドウの作成
root = tk.Tk()
root.title("Simple Drawing with Tkinter")
canvas_width = 600
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

def draw_circle():
    # 円の大きさと位置をランダムに設定
    radius = random.randint(20, 100)  # 半径
    x = random.randint(0, canvas_width)
    y = random.randint(0, canvas_height)

    # 円を描画（枠のみ）
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius)

# ボタンをクリックすると円を描画
button = tk.Button(root, text="Draw Circle", command=draw_circle)
button.pack()

root.mainloop() 
