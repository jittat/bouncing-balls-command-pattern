import tkinter as tk

from gamelib import Sprite, GameApp, Text
from random import randint

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5

NUM_BALLS = 10

class Dot(Sprite):
    def init_element(self):
        self.vx = 0
        self.vy = 0

    def random_speed(self):
        self.vx = 5 * randint(-5,5)
        self.vy = -5 * randint(1,10)

    def bounce(self):
        if (self.x > CANVAS_WIDTH) or (self.x < 0):
            self.vx = -self.vx

        if self.y > CANVAS_HEIGHT:
            self.vy = -0.85 * self.vy

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY

        self.bounce()


class FlappyGame(GameApp):
    def create_sprites(self):
        for i in range(NUM_BALLS):
            dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
            dot.random_speed()

            self.elements.append(dot)

    def init_game(self):
        self.create_sprites()

    def pre_update(self):
        pass

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
