import tkinter as tk
import math

from gamelib import Sprite, GameApp, Text
from random import randint

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5

NUM_BALLS = 5

class DotUpdateCommand:
    def __init__(self, dot):
        self.dot = dot

    def execute(self):
        self.old_state = self.dot.get_state()
        self.dot.real_update()        

    def undo(self):
        self.dot.set_state(self.old_state)

def vectlen(x,y):
    return math.sqrt(x*x + y*y)

def bounce_normal(vx,vy,nx,ny):
    nlen = vx*nx + vy*ny

    vnx = nlen * nx
    vny = nlen * ny

    vxleft = vx - vnx
    vyleft = vy - vny

    return (vnx - vxleft, vny - vyleft)


class DotBounceCommand:
    def __init__(self, dot1, dot2):
        self.dot1 = dot1
        self.dot2 = dot2

    def execute(self):
        dot1 = self.dot1
        dot2 = self.dot2
        self.old_state1 = dot1.get_state()
        self.old_state2 = dot2.get_state()

        diff_x = dot1.x - dot2.x
        diff_y = dot1.y - dot2.y

        dlen = vectlen(diff_x,diff_y)
        if dlen < 0.1:
            return

        normal_x = -diff_y / dlen
        normal_y = diff_x / dlen

        dot1.vx, dot1.vy = bounce_normal(dot1.vx, dot1.vy, normal_x, normal_y)
        dot2.vx, dot2.vy = bounce_normal(dot2.vx, dot2.vy, normal_x, normal_y)

        dot1.real_update()
        dot2.real_update()

    def undo(self):
        dot1 = self.dot1
        dot2 = self.dot2
        dot1.set_state(self.old_state1)
        dot2.set_state(self.old_state2)

class Dot(Sprite):
    def init_element(self):
        self.vx = 0
        self.vy = 0

    def random_speed(self):
        self.vx = 5 * randint(-5,5)
        while self.vx == 0:
            self.vx = 1.5 * randint(-8,8)
        self.vy = -2 * randint(1,15)

    def bounce(self):
        if (self.x > CANVAS_WIDTH) or (self.x < 0):
            self.vx = -self.vx

        if self.y > CANVAS_HEIGHT:
            self.vy = -0.85 * self.vy

    def real_update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY

        self.bounce()

    def get_update_command(self):
        return DotUpdateCommand(self)

    def get_state(self):
        return (self.x, self.y, self.vx, self.vy)

    def set_state(self, state):
        self.x, self.y, self.vx, self.vy = state

    def is_too_close(self, dot):
        dist = math.sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)
        return dist < 20

    def get_bounce_command(self, dot):
        return DotBounceCommand(self, dot)


class CommandPatternDemoApp(GameApp):
    def create_sprites(self):
        self.dots = []
        for i in range(NUM_BALLS):
            dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
            dot.random_speed()

            #dot.x += randint(-50,50)
            #dot.y += randint(-50,50)

            self.dots.append(dot)
            self.elements.append(dot)

    def init_game(self):
        self.create_sprites()

        self.commands = []
        self.is_reversed = False
        self.cmd_index = 0

    def reverse_update(self):
        current_commands = self.commands[self.cmd_index]

        for c in reversed(current_commands):
            c.undo()

        self.cmd_index -= 1
        if self.cmd_index < 0:
            self.is_reversed = False
            self.commands = []

    def create_update_commands(self):
        new_commands = []
        for dot in self.dots:
            new_commands.append(dot.get_update_command())
        return new_commands

    def create_bounce_commands(self):
        cmds = []
        num_dots = len(self.dots)
        for i in range(num_dots):
            for j in range(num_dots):
                if i < j:
                    d1 = self.dots[i]
                    d2 = self.dots[j]
                    if d1.is_too_close(d2):
                        cmds.append(d1.get_bounce_command(d2))
        return cmds

    def pre_update(self):
        if self.is_reversed:
            self.reverse_update()
            return

        new_commands = self.create_update_commands()
        for c in new_commands:
            c.execute()

        if self.cmd_index > 20:
            bounce_commands = self.create_bounce_commands()
            for c in bounce_commands:
                c.execute()
        else:
            bounce_commands = []

        self.commands.append(new_commands + bounce_commands)
        self.cmd_index = len(self.commands) - 1

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        self.is_reversed = True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = CommandPatternDemoApp(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
