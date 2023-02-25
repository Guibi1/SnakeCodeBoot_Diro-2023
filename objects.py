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


class Blocs(Objects):
    tex = textures.fence

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Apple(Objects):
    sorte = ""

    def __init__(self, sorte, x, y):
        self.sorte = sorte
        self.x = x
        self.y = y

    def display(self):
        dev.draw_image(self.x * 11 + 7, self.y * 11 + 7,
                       textures.levels["grass"]["apples"][self.sorte])


def getRandomPomme():
    nbRandom = int(random()*120+1)
    x = int(random()*11)
    y = int(random()*11)

    if nbRandom > 110:
        return Apple("multi", x, y)
    elif nbRandom > 100:
        return Apple("portal", x, y)
    elif nbRandom > 90:
        return Apple("poison", x, y)
    elif nbRandom > 80:
        return Apple("chrono", x, y)
    elif nbRandom > 70:
        return Apple("bloc", x, y)
    elif nbRandom > 60:
        return Apple("speed", x, y)
    elif nbRandom > 50:
        return Apple("god", x, y)
    elif nbRandom > 40:
        return Apple("smallDick", x, y)
    return Apple("mid", x, y)
