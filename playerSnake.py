import ttgo as dev
import net
import ui
import random
import objects
import textures


def displaySnake(positions):
    def movingTo(i=-1):
        if positions[i][0] > positions[i-1][0]:
            return "R"
        elif positions[i][0] < positions[i-1][0]:
            return "L"

        if positions[i][1] > positions[i-1][1]:
            return "B"
        elif positions[i][1] < positions[i-1][1]:
            return "T"

    # Tail
    dev.draw_image(
        positions[0][0]*11 + 7, positions[0][1]*11 + 7, textures.levels["grass"]["snakeTail"][movingTo(0)])
    # Head
    dev.draw_image(
        positions[-1][0]*11 + 7, positions[-1][1]*11 + 7, textures.levels["grass"]["snakeHead"][movingTo()])
    # Body
    for i, pos in enumerate(positions[1:-1]):
        dev.draw_image(pos[0]*11 + 7, pos[1]*11 + 7,
                       textures.levels["grass"]["snakeLine"][movingTo(i)])


class PlayerSnake:
    nextX = 1
    nextY = 0
    positions = [(0, 0), (0, 1), (0, 2)]
    score = 0

    def __init__(self):
        pass

    def display(self):
        # Tail
        dev.draw_image(
            self.positions[0][0]*11 + 7, self.positions[0][1]*11 + 7, textures.levels["grass"]["snakeTail"][self.movingTo(0)])
        # Head
        dev.draw_image(
            self.positions[-1][0]*11 + 7, self.positions[-1][1]*11 + 7, textures.levels["grass"]["snakeHead"][self.movingTo()])
        # Body
        for i, pos in enumerate(self.positions[1:-1]):
            dev.draw_image(pos[0]*11 + 7, pos[1]*11 + 7,
                           textures.levels["grass"]["snakeLine"][self.movingTo(i)])

    def move(self, rallonger):
        self.positions.append(
            (self.positions[-1][0] + self.nextX, self.positions[-1][1] + self.nextY))
        if not rallonger:
            self.positions.pop(0)

    def movingTo(self, i=-1):
        if self.positions[i][0] > self.positions[i-1][0]:
            return "R"
        elif self.positions[i][0] < self.positions[i-1][0]:
            return "L"

        if self.positions[i][1] > self.positions[i-1][1]:
            return "B"
        elif self.positions[i][1] < self.positions[i-1][1]:
            return "T"

    def manger(self, pomme, blocks, tileIsSpecial):
        if pomme.sorte == "mid":
            self.score += 1

        elif pomme.sorte == "god":
            self.score += 10

        elif pomme.sorte == "block":
            bloc = objects.Blocs(self.positions[0][0], self.positions[0][-1])
            blocks.append(bloc)

        elif pomme.sorte == "smallDick":
            for i in range(5):
                pos = self.positions.pop(0)
                if tileIsSpecial[pos[0]][pos[1]]:
                    dev.draw_image(
                        pos[0]*11 + 7, pos[1]*11 + 7, textures.levels["grass"]["special"])
                else:
                    dev.draw_image(
                        pos[0]*11 + 7, pos[1]*11 + 7, textures.levels["grass"]["normal"])
