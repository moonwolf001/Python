import os
import platform
import psutil

# ユーザーに確認
response = input("あなたのPCのスペックを記述したファイルを作成します。よろしいですか？ [y/N]: ").strip().lower()
if response != 'y':
    print("ファイルの作成がキャンセルされました。")
else:
    # スペック情報を収集
    specs = {
        "OS": platform.system(),
        "OSバージョン": platform.release(),
        "CPU": platform.processor(),
        "コア数": psutil.cpu_count(logical=False),
        "論理プロセッサ数": psutil.cpu_count(logical=True),
        "メモリー合計": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
    }

    # ファイル名
    filename = "pc_specs.txt"

    # スペック情報をファイルに書き込む
    with open(filename, 'w') as file:
        for key, value in specs.items():
            file.write(f"{key}: {value}\n")
    
    print(f"スペック情報が{filename}に書き込まれました。")
