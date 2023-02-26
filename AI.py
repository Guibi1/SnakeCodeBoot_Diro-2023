from objects import *
from playerSnake import*
import snake
import playerSnake as player
import textures

name = "AI"

def comparePathLenght(snakePosition, applesPosition):
    distances = []
    
    for apple in applesPosition:
        distances.append((snakePosition[0] - apple[0] / snakePosition[1] - apple[1]))
    
    smalest = distances[0]
    for i in range(1, len(distances)):
        if distances[i] < smalest:
            smalest = distances[i]
    
    return applesPosition[distances.index(smalest)]

def pathFindingAlgorithm(apples, pSnake):
   
    if name in snake.otherSnakes:
        pass
    else:
        snake.otherSnakes[name] =[(3, 3),(3, 4)]
        
    snake.otherSnakes[name][-1] = snake.otherSnakes[name][-1]
    snakePosition = pSnake.positions[-1]
    applesPosition = []
    
    for apple in apples:
        applesPosition.append((apple.x, apple.y))
        
    theApplePosition = comparePathLenght((snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1]), applesPosition)
    
    if snake.otherSnakes[name][-1][0] == theApplePosition[0] and snake.otherSnakes[name][-1][1] != theApplePosition[1]:
        if snake.otherSnakes[name][-1][1] < theApplePosition[1]:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1]  +1)  #Go down
            
        else:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1] - 1) #Go up
            
        
    elif snake.otherSnakes[name][-1][0] != theApplePosition[0] and snake.otherSnakes[name][-1][1] == theApplePosition[1]:
        if snake.otherSnakes[name][-1][0] < theApplePosition[0]:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] + 1, snake.otherSnakes[name][-1][1]) #Go right
            
        else:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] - 1, snake.otherSnakes[name][-1][1]) #Go left
            
        
    elif snake.otherSnakes[name][-1][0] != theApplePosition[0] and snake.otherSnakes[name][-1][1] != theApplePosition[1]:
        print("TEST2")
        if snake.otherSnakes[name][-1][0] < theApplePosition[0]:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] + 1, snake.otherSnakes[name][-1][1]) #Go right
            
        else: 
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] - 1, snake.otherSnakes[name][-1][1]) #Go left
            
    elif snake.otherSnakes[name][-1][0] == theApplePosition[0] and snake.otherSnakes[name][-1][1] == theApplePosition[1]:
        print("GOT IT !!!")
            
    print(snake.otherSnakes[name])
    return