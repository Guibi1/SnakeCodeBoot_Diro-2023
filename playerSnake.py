import ttgo as dev
import net
import ui
import random
import objects
import textures


class PlayerSnake:
    nextX = 1
    nextY = 0
    positions = [(0, 0), (0, 1)]
    score = 0

    def __init__(self):
        pass

    def display(self):
        for pos in self.positions:
            dev.draw_image(pos[0]*11 + 7, pos[1]*11 + 7, textures.snakeHead)

    def move(self, rallonger):
        self.positions.append(
            (self.positions[-1][0] + self.nextX, self.positions[-1][1] + self.nextY))
        if not rallonger:
            self.positions.pop(0)

    def movingTo(self):
        if self.positions[-1][0] > self.positions[-2][0]:
            return "R"
        elif self.positions[-1][0] < self.positions[-2][0]:
            return "L"

        if self.positions[-1][1] > self.positions[-2][1]:
            return "B"
        elif self.positions[-1][1] < self.positions[-2][1]:
            return "T"
    
    def manger(self,pomme, blocks):
        if isinstance(pomme,objects.PommeNormale):
            self.score+=1
            
        elif isinstance(pomme,objects.Pomme10):
            self.score+=10
            
        elif isinstance(pomme,objects.PommeBloc):
            bloc=objects.Blocs(self.positions[0][0], self.positions[0][-1])
            blocks.append(bloc)
       
 
