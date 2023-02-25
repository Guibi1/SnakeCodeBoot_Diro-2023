import ttgo as dev
import net
import ui
import random

class PlayerSnake:
    
    
    def __init__(self):
        self.y = 5
        self.x = 6
        self.nextX = 0
        self.nextY = 0
        self.position = [(0,0), (0, 1)]
    def display(self):
        for pos in self.position:
            dev.fill_rect(pos[0]*11 + 7, pos[1]*11 + 7, 11, 11, "#f00")

    def move(self):
        positions.append((self.positions[-1][0] + self.nextX, self.positions[-1][1] + self.nextY))

    def movingTo(self):
        if self.positions[-1][0] > self.positions[-2][0]:
            return "R"
        elif self.positions[-1][0] < self.positions[-2][0]:
            return "L"

        if self.positions[-1][1] > self.positions[-2][1]:
            return "B"
        elif self.positions[-1][1] < self.positions[-2][1]:
            return "T"
 
        