from objects import *
from playerSnake import*
import snake
import playerSnake as player
import textures

name = "AI"
score = 0

def comparePathLenght(snakePosition, applesPosition):
    distances = []
    
    for apple in applesPosition:
        if(snakePosition[1] == apple[1]):
            distances.append(0)
        else:
            distances.append((snakePosition[0] - apple[0] / snakePosition[1] - apple[1]))
    
    smalest = distances[0]
    for i in range(1, len(distances)):
        if distances[i] < smalest:
            smalest = distances[i]
    
    return distances.index(smalest)

def pathFindingAlgorithm(apples, pSnake, blocs):
   
    if name in snake.otherSnakes:
        pass
    else:
        snake.otherSnakes[name] =[(3, 3),(3, 4)]
        
    snake.otherSnakes[name][-1] = snake.otherSnakes[name][-1]
    snakePosition = pSnake.positions[-1]
    applesPosition = []
  
    try:
        for apple in apples:
            if apple.sorte == "poison":
                pass
            else:
                applesPosition.append((apple.x, apple.y))
    except:
         walkArround(snake.otherSnakes[name])
            
    if len(applesPosition) == 0:
        walkArround(snake.otherSnakes[name])
        return
    
    posOfSmalest = comparePathLenght((snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1]), applesPosition)    
    theApplePosition = applesPosition[posOfSmalest]
    
    
    
    if snake.otherSnakes[name][-1][0] == theApplePosition[0] and snake.otherSnakes[name][-1][1] != theApplePosition[1]:
        if snake.otherSnakes[name][-1][1] < theApplePosition[1] and isItSafe(apples, blocs, pSnake, (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1]  +1)):
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1]  +1)  #Go down
            
        if snake.otherSnakes[name][-1][1] > theApplePosition[1] and isItSafe(apples, blocs, pSnake, (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1]  +1)):
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1] - 1) #Go up
            
        
    elif snake.otherSnakes[name][-1][0] != theApplePosition[0] and snake.otherSnakes[name][-1][1] == theApplePosition[1]:
        if snake.otherSnakes[name][-1][0] < theApplePosition[0]:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] + 1, snake.otherSnakes[name][-1][1]) #Go right
            
        else:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] - 1, snake.otherSnakes[name][-1][1]) #Go left
            
        
    elif snake.otherSnakes[name][-1][0] != theApplePosition[0] and snake.otherSnakes[name][-1][1] != theApplePosition[1]:
        if snake.otherSnakes[name][-1][0] < theApplePosition[0]:
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] + 1, snake.otherSnakes[name][-1][1]) #Go right
            
        else: 
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] - 1, snake.otherSnakes[name][-1][1]) #Go left
            
    elif snake.otherSnakes[name][-1][0] == theApplePosition[0] and snake.otherSnakes[name][-1][1] == theApplePosition[1]:
            manger(apples[posOfSmalest])
            snake.pomme = None
    return
        
def manger(pomme):
    global score
    oSnake = snake.otherSnakes[name]
    if oSnake[-1] != pomme.getPosition():
        if pomme.sorte == "chrono":
            score -= 5
        snake.pomme = snake.getRandomPomme()
    if pomme.sorte == "mid":
        score += 1

    elif pomme.sorte == "god":
        score += 10

    elif pomme.sorte == "block":
        snake.blocks.append((
            oSnake[0][0], oSnake[0][-1]))
        snake.displayBlocks()

    elif pomme.sorte == "small":
        ranTemp = -1
        for i in range(ranTemp):
            pos = oSnake[0].pop(0)
            if tileIsSpecial[pos[0]][pos[1]]:
                dev.draw_image(
                    pos[0]*11 + 7, pos[1]*11 + 7, textures.getLevel()["special"])
            else:
                dev.draw_image(
                    pos[0]*11 + 7, pos[1]*11 + 7, textures.getLevel()["normal"])

    elif pomme.sorte == "poison":
        snake.gameOver()

    elif pomme.sorte == "portal":
        snake.otherSnakes[name][-1] = (5, 3)
        
def walkArround(oSnake):
    for i in range(len(oSnake)):
        if oSnake[-1] != (oSnake[i][0] + 1, oSnake[i][1]):
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] + 1, snake.otherSnakes[name][-1][1])
        elif oSnake[-1] != (oSnake[i][0] - 1, oSnake[i][1]):
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0] - 1, snake.otherSnakes[name][-1][1])
        elif oSnake[-1] != (oSnake[i][0], oSnake[i][1] + 1):
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1] + 1) 
        elif oSnake[-1] != (oSnake[i][0], oSnake[i][1] - 1):
            snake.otherSnakes[name][-1] = (snake.otherSnakes[name][-1][0], snake.otherSnakes[name][-1][1] - 1) 
        else:
            print("I'm not supposed to see this")
            
def isItSafe(apples, blocs, pSnake, request):
    unsafePlaces = []
    
    for apple in apples:
        if(apple.sorte == "poison"):
            unsafePlaces.append((apple.getPosition()))
    
    for bloc in blocs:
        unsafePlaces.append(bloc)
        
    for pPos in pSnake.positions:
        unsafePlaces.append(pPos)
        
    for oPos in snake.otherSnakes[name]:
        unsafePlaces.append(oPos)
        
    print (unsafePlaces)
    for threat in unsafePlaces:
        if request == threat:
            return False
    return True