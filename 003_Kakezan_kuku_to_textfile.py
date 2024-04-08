import os

def create_kuku_file():
    # ファイル名のベースとなる部分
    base_filename = "9_9_result"
    extension = ".txt"
    counter = 1
    filename = f"{base_filename}{extension}"

    # 既存のファイル名と重複しないように調整
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_filename}({counter}){extension}"

    # 九九の結果をファイルに書き込む
    with open(filename, 'w') as file:
        for i in range(1, 10):
            for j in range(1, 10):
                file.write(f"{i} x {j} = {i*j}\n")

    # 完全なファイルパスを返す
    return os.path.abspath(filename)

# ユーザーに確認
response = input("カレントディレクトリーにかけ算九九のテキストファイルを作成しても良いですか？ [y/N]: ").strip().lower()
if response == 'y':
    file_path = create_kuku_file()
    print(f"ファイルが作成されました: {file_path}")
else:
    print("ファイルの作成がキャンセルされました。")
