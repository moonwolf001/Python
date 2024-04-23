# (c)2024 MoonWolf // tkinter RGBカラーパレット

import tkinter as tk

def generate_colors():
    """RGBの各成分で色を生成する"""
    colors = []
    intervals = [i for i in range(0, 256, 55)]  # 0から252まで16進数の55刻みとする
    for r in intervals:
        for g in intervals:
            for b in intervals:
                if len(colors) >= 120:  # 最初の120色のみを取得
                    return colors
                rgb_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
                colors.append(rgb_hex)
    return colors


def main():
    root = tk.Tk()
    root.title("Python Tkinter RGBカラー　by MoonWolf")

    # ウィンドウのサイズを800x1600ピクセルに設定
    root.geometry("800x1600")

    # スクロールバー付きのキャンバスを設定
    canvas = tk.Canvas(root, borderwidth=0, background="white")
    frame = tk.Frame(canvas, background="white")
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw", tags="frame")

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    # 色を生成
    colors = generate_colors()

    # 色を表示
    row = 0
    col = 0
    for color in colors:
        border_frame = tk.Frame(frame, borderwidth=1, relief="solid", width=150, height=80)
        border_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        border_frame.grid_propagate(False)

        color_label = tk.Label(border_frame, bg=color, height=2, width=20)
        color_label.pack(expand=True, fill="both")
        rgb_label = tk.Label(border_frame, text=color, bg="white", fg="black", height=1, width=20)
        rgb_label.pack(fill="both")

        col += 1
        if col >= 5:
            col = 0
            row += 1

    root.mainloop()


if __name__ == "__main__":
    main()
