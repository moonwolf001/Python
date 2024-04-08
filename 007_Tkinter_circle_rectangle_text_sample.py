import tkinter as tk

# ウィンドウの作成
root = tk.Tk()
root.title("Tkinter Shapes and Text Example")
canvas = tk.Canvas(root, width=800, height=600, bg='white')
canvas.pack()

# 青色の塗りつぶされた円と枠だけの円
canvas.create_oval(100, 50, 200, 150, fill='blue')
canvas.create_oval(250, 50, 350, 150, outline='blue', width=2)

# 緑色の塗りつぶされた楕円と枠だけの楕円
canvas.create_oval(400, 50, 550, 150, fill='green')
canvas.create_oval(600, 50, 750, 150, outline='green', width=2)

# 黄色の塗りつぶされた長方形と枠だけの長方形
canvas.create_rectangle(100, 200, 250, 300, fill='yellow')
canvas.create_rectangle(300, 200, 450, 300, outline='yellow', width=2)

# テキストの表示（フォント名とサイズを含む）
font_name = "Helvetica"
font_size = 16
text = f"フォント名: {font_name}, サイズ: {font_size}"
canvas.create_text(400, 350, text=text, font=(font_name, font_size), fill="blue")

root.mainloop()
