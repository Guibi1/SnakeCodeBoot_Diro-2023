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
    tailDirection = "R" if positions[0][0] > positions[1][0] else (
        "L" if positions[0][0] < positions[1][0] else ("B" if positions[0][1] > positions[1][1] else "T"))
    dev.draw_image(
        positions[0][0]*11 + 7, positions[0][1]*11 + 7, textures.getLevel()["snakeTail"][tailDirection])
    # Head
    dev.draw_image(
        positions[-1][0]*11 + 7, positions[-1][1]*11 + 7, textures.getLevel()["snakeHead"][movingTo()])
    # Body
    for i, pos in enumerate(positions[1:-1]):
        next = positions[i + 2]
        last = positions[i]
        type = "snakeLine"
        direction = "L" if pos[0] > next[0] else (
            "R" if pos[0] < next[0] else ("T" if pos[1] > next[1] else "B"))

        if (pos[1] == last[1] and pos[1] - next[1] == last[0] - pos[0]) or (pos[0] == last[0] and next[0] - pos[0] == last[1] - pos[1]):
            type = "snakeCorner"
            direction = "R" if pos[0] > next[0] else (
                "L" if pos[0] < next[0] else ("B" if pos[1] > next[1] else "T"))
        elif next[0] != last[0] and next[1] != last[1]:
            type = "snakeCorner"
            direction = "T" if pos[0] > next[0] else (
                "B" if pos[0] < next[0] else ("R" if pos[1] > next[1] else "L"))

        dev.draw_image(pos[0]*11 + 7, pos[1]*11 + 7,
                       textures.getLevel()[type][direction])


class PlayerSnake:
    tpTo = None
    nextX = 1
    nextY = 0
    positions = [(0, 0), (0, 1), (0, 2)]
    score = 0

    def __init__(self):
        pass

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
