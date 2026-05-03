import tkinter as tk
import random

class BounceFixedGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Bounce Ball Fixed")
        self.root.geometry("400x500")

        self.canvas = tk.Canvas(root, width=400, height=500, bg="black")
        self.canvas.pack()

        # 🧱 koridor (tor yo‘l)
        self.left_wall = 80
        self.right_wall = 320

        self.canvas.create_line(self.left_wall, 0, self.left_wall, 500, fill="gray")
        self.canvas.create_line(self.right_wall, 0, self.right_wall, 500, fill="gray")

        # 🧺 basket (ichkarida cheklangan)
        self.basket = self.canvas.create_rectangle(170, 450, 230, 480, fill="blue")

        # ⚪ ball
        self.ball = self.canvas.create_oval(190, 100, 210, 120, fill="white")

        # physics (KUCHNI CHEKLAYMIZ)
        self.ball_x = 2
        self.ball_y = 3

        self.score = 0
        self.text = self.canvas.create_text(60, 20, text="Score: 0", fill="white")

        root.bind("<Left>", self.left)
        root.bind("<Right>", self.right)

        self.update()

    # ⬅ basket move (limit bilan)
    def left(self, event):
        x1, _, x2, _ = self.canvas.coords(self.basket)
        if x1 > self.left_wall + 5:
            self.canvas.move(self.basket, -15, 0)

    # ➡ basket move (limit bilan)
    def right(self, event):
        x1, _, x2, _ = self.canvas.coords(self.basket)
        if x2 < self.right_wall - 5:
            self.canvas.move(self.basket, 15, 0)

    # 🎮 game loop
    def update(self):
        self.canvas.move(self.ball, self.ball_x, self.ball_y)

        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

        # 🧱 devor cheklovi (katta uchib ketmasin)
        if bx1 <= self.left_wall or bx2 >= self.right_wall:
            self.ball_x *= -1  # faqat yo‘nalish o‘zgaradi

        # ⬆ yuqoriga urilib qaytadi
        if by1 <= 0:
            self.ball_y = abs(self.ball_y)

        # ⬇ pastga tushsa reset
        if by2 >= 500:
            self.reset_ball()

        # 🧺 catch
        if self.check_hit(self.canvas.coords(self.basket),
                          self.canvas.coords(self.ball)):
            self.score += 1
            self.canvas.itemconfig(self.text, text=f"Score: {self.score}")
            self.ball_y = -abs(self.ball_y)  # yumshoq bounce

        self.root.after(20, self.update)

    # 🔄 reset ball (tezlik nazorat bilan)
    def reset_ball(self):
        self.canvas.coords(self.ball,
                           random.randint(self.left_wall+10, self.right_wall-30),
                           80,
                           random.randint(self.left_wall+30, self.right_wall-10),
                           100)

        self.ball_x = random.choice([-2, 2])
        self.ball_y = 3

    # 💥 collision
    def check_hit(self, a, b):
        return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])


root = tk.Tk()
game = BounceFixedGame(root)
root.mainloop()