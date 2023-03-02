import ttgo as dev
import textures


class Objects():
    tex = "#0f0"
    x = 0
    y = 0

    def getPosition(self):
        return (self.x, self.y)

    def display(self):
        dev.draw_image(self.x * 11 + 7, self.y * 11 + 7, self.tex)


class Apple(Objects):
    sorte = ""

    def __init__(self, sorte, x, y):
        self.sorte = sorte
        self.x = x
        self.y = y

    def display(self):
        dev.draw_image(self.x * 11 + 7, self.y * 11 + 7,
                       textures.getLevel()["apples"][self.sorte])
