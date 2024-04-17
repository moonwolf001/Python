# (c)2024 MoonWolf / ボールバウンド・シミュレーション

import tkinter as tk

class BallSimulation:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack()
        self.ball_radius = 10  # ボールの半径
        self.reset_ball()  # ボールの初期設定を行う関数
        self.gravity = 0.5  # 重力加速度
        self.elasticity = 0.95  # 床からの反発係数
        self.min_velocity = 1.0  # 最小反発速度（これ以下になったらリセット）
        self.update()

    def reset_ball(self):
        """ ボールの位置と速度を初期状態にリセットする """
        self.x_velocity = 8  # x方向の初速度
        self.y_velocity = 0  # y方向の初速度
        self.canvas.delete("ball")  # 既存のボールを削除
        self.ball = self.canvas.create_oval(10, 90, 10 + 2 * self.ball_radius, 90 + 2 * self.ball_radius, fill='red', tags="ball")

    def update(self):
        self.canvas.move(self.ball, self.x_velocity, self.y_velocity)  # ボールを動かす
        pos = self.canvas.coords(self.ball)
        # 右または左の壁に衝突
        if pos[2] >= 500 or pos[0] <= 0:
            self.x_velocity = -self.x_velocity
        # 床に衝突
        if pos[3] >= 400:
            if abs(self.y_velocity) < self.min_velocity:
                self.reset_ball()  # バウンドが小さい場合はリセット
            else:
                self.y_velocity = -self.y_velocity * self.elasticity
        else:
            self.y_velocity += self.gravity  # 重力による加速

        self.root.after(50, self.update)  # 50ミリ秒後に再度updateメソッドを呼び出し

def main():
    root = tk.Tk()
    app = BallSimulation(root)
    root.mainloop()

if __name__ == "__main__":
    main()
