# (c)2024 MoonWolf  
#『MoonWolfと学ぶPythonシリーズ　第２巻 オブジェクト指向プログラミング 超入門編 』

# tkinterを使った、Pythonでの表示例

import tkinter as tk
from tkinter import messagebox

# ボタンがクリックされた回数を保持する変数
click_count = 0

def on_button_click():
    global click_count
    # ボタンがクリックされた回数を増やす
    click_count += 1
    # ボタンがクリックされた回数をリストボックスに追加
    listbox.insert(tk.END, f"ボタンが押されました {click_count} 回目")

# Tkinterのルートウィンドウを作成
root = tk.Tk()
root.title("Tkinter デモ")

# キャンバスウィジェットのサイズを調整し、図形とテキストのスペースを最適化
canvas = tk.Canvas(root, width=400, height=150) # キャンバスの高さを減らす
canvas.pack(pady=(10, 0)) # 上の余白を追加し、下の余白を削除

# 円、楕円、長方形、テキストをキャンバスに描画
canvas.create_oval(10, 10, 60, 60, fill="red") # サイズ調整
canvas.create_oval(80, 10, 150, 60, fill="green", outline="blue") # サイズ調整
canvas.create_rectangle(180, 10, 220, 60, fill="yellow", outline="black") # サイズ調整
canvas.create_text(300, 30, text="Python Tkinter デモ") # 位置調整

# メモ覧（リストボックス）を作成し、サイズと余白を調整
listbox = tk.Listbox(root, width=50, height=7) # heightを減らす
listbox.pack(pady=(5, 5)) # 上下の余白を設定

listbox.insert(tk.END, "Python tkinter デモンストレーション")

# ボタンウィジェットを作成し、余白を調整して配置
button = tk.Button(root, text="クリックしてね", command=on_button_click)
button.pack(pady=(0, 10)) # 上の余白を削除し、下の余白を追加

# メインループを開始
root.mainloop()
