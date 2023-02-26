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
    tailDirection = "R" if positions[0][0] >= positions[1][0] else (
        "T" if positions[0][0] <= positions[1][0] else ("L" if positions[0][1] >= positions[1][1] else "R"))
    dev.draw_image(
        positions[0][0]*11 + 7, positions[0][1]*11 + 7, textures.getLevel()["snakeTail"][tailDirection])
    # Head
    dev.draw_image(
        positions[-1][0]*11 + 7, positions[-1][1]*11 + 7, textures.getLevel()["snakeHead"][movingTo()])
    # Body
    for i, pos in enumerate(positions[1:-1]):
        dev.draw_image(pos[0]*11 + 7, pos[1]*11 + 7,
                       textures.getLevel()["snakeLine"][movingTo(i)])


class PlayerSnake:
    tpTo = None
    nextX = 1
    nextY = 0
    positions = [(0, 0), (0, 1), (0, 2)]
    score = 0

    def __init__(self):
        pass

    def display(self):
        # Tail
        dev.draw_image(
            self.positions[0][0]*11 + 7, self.positions[0][1]*11 + 7, textures.getLevel()["snakeTail"][self.movingTo(0)])
        # Head
        dev.draw_image(
            self.positions[-1][0]*11 + 7, self.positions[-1][1]*11 + 7, textures.getLevel()["snakeHead"][self.movingTo()])
        # Body
        for i, pos in enumerate(self.positions[1:-1]):
            dev.draw_image(pos[0]*11 + 7, pos[1]*11 + 7,
                           textures.getLevel()["snakeLine"][self.movingTo(i)])

    def move(self, rallonger):
        if self.tpTo is not None:
            self.positions.append(self.tpTo)
            self.tpTo = None
            return

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
