# (c)2024 MoonWolf / Python Tkinterでの色一覧とその色の名称
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("スクロール可能な色の一覧")

    # ウィンドウのサイズを820x500に設定
    root.geometry("820x500")

    # スクロールバー付きのキャンバスを設定
    canvas = tk.Canvas(root, borderwidth=0, background="white")
    frame = tk.Frame(canvas, background="white")
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw", tags="frame")

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

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

    # グリッド内に色と色名を表示（5列で配置）
    for i, color in enumerate(colors):
        row = i // 5
        col = i % 5
        border_frame = tk.Frame(frame, borderwidth=1, relief="solid", width=120, height=60)
        border_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        border_frame.grid_propagate(False)  # 固定サイズを保持するため

        color_label = tk.Label(border_frame, bg=color, height=2, width=20)
        color_label.pack(expand=True, fill="both")
        name_label = tk.Label(border_frame, text=color, bg="white", fg="black", height=1, width=20)
        name_label.pack(fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
