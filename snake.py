import ttgo as dev
import net
import mate
import apps
import ui
import playerSnake as player
import objects
import textures
import AI
import classement

bg = '#000'  # general background color
currentLevel = "grass"  # grass sand space
width = 11
height = 18

# game state
me = None  # is 0 when non-networked, and 0 or 1 when networked

# the following global variables are useful for the networked version

ai = False
networked = False  # are we playing over the network?
msg_type = "SNAKENET"   # type of the messages sent between the nodes, set later
ping_timer = 0      # used to check that the mate is still with us
pong_timer = 0


def reset_mate_timeout():
    global pong_timer
    pong_timer = int(5 / ui.time_delta)  # reset peer timeout to 5 seconds


def quit():  # called to quit the game
    if networked:
        for id in mate.ids:
            net.send(id, [msg_type, 'quit'])
    leave()


def leave():
    global me
    me = None  # no longer playing
    if networked:
        net.pop_handler()  # remove message_handler
    apps.menu()  # go back to app menu


def init_game():
    global me, tick_counter, playerSnake, otherSnakes, pommes, blocks, tileIsSpecial
    me = None
    tick_counter = 1
    playerSnake = player.PlayerSnake(
        int(net.id[-1]) if net.id is not None else 5)
    otherSnakes = {}
    pommes = []

    setCurrentLevel(currentLevel)

    dev.clear_screen(bg)
    dev.draw_image(17, 30, textures.readySetSnake1)

    def next():
        dev.draw_image(20, 90, textures.readySetSnake2)
        dev.after(1, lambda: dev.draw_image(
            15, 160, textures.readySetSnake3))
    dev.after(1, next)


def gameOver():
    global me
    me = None
    quitWhenButtonOk()
    classement.addHighScore(playerSnake.score)

    dev.clear_screen(bg)

    dev.draw_image(17, 10, textures.gameOverText)

    dev.draw_image(30, 120, textures.scoreText)
    ui.center(dev.screen_width//2, 180,
              str(playerSnake.score), apps.fg, bg)

    ui.center(dev.screen_width//2, 220, " Quit ", bg, apps.accent)


def setCurrentLevel(level):
    global currentLevel, tileIsSpecial, blocks

    currentLevel = level
    textures.currentLevel = level

    if currentLevel == "grass":
        blocks = [(2,6),(3, 6),                      (7, 6), (8,6),
                  (2,7),                                    (8, 7),
                  (2,8),                                    (8, 8),


                  (2,11),                                   (8,11),
                  (2,12),                                   (8,12),
                  (2,13),(3,13),                      (7,13),(8,13)
                  ]
    elif currentLevel == "sand":
        blocks = [(3, 8), (2, 9), (7, 2), (9, 4),
                  (1, 17), (10, 5), (8, 9), (10, 15)]
    else:
        blocks = [  (1,10) , (3,10) , (5,10) , (7,10) , (9,10)  ,

                    (1,13) , (3,13) , (5,13) , (7,13) , (9,13)


                                     ,(5,17)]

    tileIsSpecial = []
    for _ in range(width):
        row = []
        tileIsSpecial.append(row)
        for _ in range(height):
            row.append(random() > (0.99 if currentLevel == "sand" else 0.9))


tick_counter = 1
playerSnake = player.PlayerSnake(int(net.id[-1]) if net.id is not None else 5)
player.displaySnake(playerSnake.positions)
otherSnakes = {}
pommes = []
pommeTimer = 0
blocks = []
tileIsSpecial = []
timeSlowDownRatio = 5


def button_handler(event, resume):
    global ping_timer, pong_timer, tick_counter, pommes, blocks
    if me is None:
        return  # not yet playing or no longer playing

    if event == 'cancel':
        quit()
    elif event == 'tick':
        tick_counter += 1

        ui.center(dev.screen_width//2, dev.screen_height -
                  16, "Score " + str(playerSnake.score), '#FFF', bg)

        if tick_counter % timeSlowDownRatio != 0:
            dev.after(ui.time_delta, resume)  # need to wait...
            return

        rallonger = False
        if len(pommes) == 0:
            if not networked or master():
                addRandomPomme()
                for pomme in pommes:
                    pomme.display()

                if networked:
                    for id in mate.ids:
                        net.send(id, [msg_type, "newPomme",
                                      pomme.sorte, pomme.x, pomme.y])
       # pas sur

        for pomme in pommes:
            if playerSnake.positions[-1] == pomme.getPosition():
                manger(pomme)
                pommes = []
                rallonger = True
                for id in mate.ids:
                    net.send(id, [msg_type, "eatPomme", pommes.index(pomme)])

        if not rallonger:
            if tileIsSpecial[playerSnake.positions[0][0]][playerSnake.positions[0][1]]:
                dev.draw_image(
                    playerSnake.positions[0][0]*11 + 7, playerSnake.positions[0][1]*11 + 7, textures.getLevel()["special"])
            else:
                dev.draw_image(
                    playerSnake.positions[0][0]*11 + 7, playerSnake.positions[0][1]*11 + 7, textures.getLevel()["normal"])

        if ai:
            AI.pathFindingAlgorithm([pomme], playerSnake, blocks)
            print(otherSnakes[AI.name])
            player.displaySnake(otherSnakes[AI.name])

        playerSnake.move(rallonger)
        if networked:
            for id in mate.ids:
                net.send(id, [msg_type, "snakePositions",
                              playerSnake.positions])
        player.displaySnake(playerSnake.positions)

        for block in blocks:
            if playerSnake.positions[-1] == block:
                gameOver()

        if playerSnake.positions[-1][0] < 0 or playerSnake.positions[-1][0] >= width:
            gameOver()

        elif playerSnake.positions[-1][1] < 0 or playerSnake.positions[-1][1] >= height:
            gameOver()

        for position in playerSnake.positions[:-1]:
            if playerSnake.positions[-1] == position:
                gameOver()

        for ennemy in otherSnakes:
            for position in ennemy:
                if playerSnake.positions[-1] == position:
                    gameOver()

        if networked:
            pong_timer -= 1
            if pong_timer < 0:
                leave()
                return
            ping_timer -= 1
            if ping_timer < 0:
                ping_timer = int(2 / ui.time_delta)  # send ping every 2 secs
                for id in mate.ids:
                    net.send(id, [msg_type, 'ping'])

        dev.after(ui.time_delta, resume)  # need to wait...
    else:
        to = playerSnake.movingTo()
        if event == 'left_down':
            if to == "L":
                playerSnake.nextY = 1
                playerSnake.nextX = 0
            elif to == "R":
                playerSnake.nextY = -1
                playerSnake.nextX = 0
            elif to == "T":
                playerSnake.nextX = -1
                playerSnake.nextY = 0
            elif to == "B":
                playerSnake.nextX = 1
                playerSnake.nextY = 0
        elif event == 'right_down':
            if to == "L":
                playerSnake.nextY = -1
                playerSnake.nextX = 0
            elif to == "R":
                playerSnake.nextY = 1
                playerSnake.nextX = 0
            elif to == "T":
                playerSnake.nextX = 1
                playerSnake.nextY = 0
            elif to == "B":
                playerSnake.nextX = -1
                playerSnake.nextY = 0
        resume()


def displayBlocks():
    for block in blocks:
        dev.draw_image(7 + 11 * block[0], 7 + 11 *
                       block[1], textures.getLevel()["block"])


def getRandomPos():
    x = int(random()*width)
    y = int(random()*height)
    return (x, y)


def addRandomPomme():
    global pommeTimer, pommes

    nbRandom = int(random()*120+1)

    pos = None
    posValid = False
    while not posValid:
        pos = getRandomPos()
        posValid = True
        for p in playerSnake.positions:
            if p == pos:
                posValid = False

    if nbRandom > 110:
        addRandomPomme()
        return
    elif nbRandom > 100:
        pos2 = None
        posValid = False
        while not posValid:
            pos2 = getRandomPos()
            posValid = True
            for p in playerSnake.positions:
                if p == pos2:
                    posValid = False
        p = objects.Apple("portal", pos[0], pos[1])
        d = objects.Apple("portal", pos2[0], pos2[1])
        pommeTimer = dev.after(10, lambda: manger(p))
        pommeTimer = dev.after(10, lambda: manger(d))
        pommes.append(p)
        pommes.append(d)
        return
    elif nbRandom > 90:
        p = objects.Apple("poison", pos[0], pos[1])
        pommeTimer = dev.after(10, lambda: manger(p))
        pommes.append(p)
        return
    elif nbRandom > 80:
        p = objects.Apple("chrono", pos[0], pos[1])
        pommeTimer = dev.after(10, lambda: manger(p))
        pommes.append(p)
        return
    elif nbRandom > 70:
        p = objects.Apple("block", pos[0], pos[1])
        pommes.append(p)
        return
    elif nbRandom > 60:
        p = objects.Apple("speed", pos[0], pos[1])
        pommes.append(p)
        return
    elif nbRandom > 50:
        p = objects.Apple("god", pos[0], pos[1])
        pommes.append(p)
        return
    elif nbRandom > 40:
        p = objects.Apple("small", pos[0], pos[1])
        return
    pommes.append(objects.Apple("mid", pos[0], pos[1]))


def manger(pom):
    global pommes, pommeTimer, timeSlowDownRatio
    if not playerSnake.positions[-1] == pom.getPosition():
        if pom.sorte == "chrono":
            if playerSnake.score - 5 < 0:
                playerSnake.score = 0
            else:
                playerSnake.score -= 5
        for pomme in pommes:
            if tileIsSpecial[pomme.x][pomme.y]:
                dev.draw_image(
                    pomme.x*11 + 7, pomme.y*11 + 7, textures.getLevel()["special"])
            else:
                dev.draw_image(
                    pomme.x*11 + 7, pomme.y*11 + 7, textures.getLevel()["normal"])

        pommes = []

        for id in mate.ids:
            net.send(id, [msg_type, "eatPomme", pommes.index(pom)])
        return

    if pom.sorte == "mid":
        playerSnake.score += 1

    elif pom.sorte == "god":
        playerSnake.score += 10

    elif pom.sorte == "block":
        blocks.append((
            playerSnake.positions[1][0], playerSnake.positions[1][-1]))
        displayBlocks()
        if networked:
            for id in mate.ids:
                net.send(id, [msg_type, 'setBlocks', blocks])

    elif pom.sorte == "small":
        ranTemp = int((random() * (len(playerSnake.positions)/5))+1)
        for i in range(ranTemp):
            pos = playerSnake.positions.pop(0)
            if tileIsSpecial[pos[0]][pos[1]]:
                dev.draw_image(
                    pos[0]*11 + 7, pos[1]*11 + 7, textures.getLevel()["special"])
            else:
                dev.draw_image(
                    pos[0]*11 + 7, pos[1]*11 + 7, textures.getLevel()["normal"])

    elif pom.sorte == "poison":
        gameOver()

    elif pom.sorte == "portal":
        for pomme in pommes:
            if pomme.sorte == "portal" and not playerSnake.positions[-1] == pomme.getPosition():
                playerSnake.tpTo = pomme.getPosition()
    elif pom.sorte == "speed":
        timeSlowDownRatio = 3

        def l():
            global timeSlowDownRatio
            timeSlowDownRatio = 5

        dev.after(3, l)

    if (pommeTimer > 0):
        dev.stopAfter(pommeTimer)
        pommeTimer = 0


def start_game_soon(player):
    dev.after(3, lambda: start_game(player))


def start_game(player):
    global me
    me = player
    reset_mate_timeout()
    ui.track_button_presses(button_handler)  # start tracking button presses
    dev.clear_screen(bg)

    for y in range(height):
        for x in range(width):
            if (tileIsSpecial[x][y]):
                dev.draw_image(7 + x * 11, 7 + y * 11,
                               textures.getLevel()["special"])
            else:
                dev.draw_image(7 + x * 11, 7 + y * 11,
                               textures.getLevel()["normal"])
    displayBlocks()


def snake_non_networked():
    init_game()
    start_game_soon(0)

# The following functions are used when playing the game over the network


def master():  # the master is the node with the smallest id
    for id in mate.ids:
        if net.id > id:
            return False
    return True


def message_handler(peer, msg):
    global pong_timer, otherSnakes, pommes, currentLevel, blocks
    if peer is None:
        if msg == 'start':
            networkStart()
        else:
            print('system message', msg)  # ignore other messages from system
    elif type(msg) is list and msg[0] == msg_type:
        if msg[1] == 'quit':
            leave()
        elif msg[1] == 'ping':
            reset_mate_timeout()
        elif msg[1] == 'snakePositions':
            if otherSnakes.get(peer, None) != None:
                if tileIsSpecial[otherSnakes[peer][0][0]][otherSnakes[peer][0][1]]:
                    dev.draw_image(
                        otherSnakes[peer][0][0]*11 + 7, otherSnakes[peer][0][1]*11 + 7, textures.getLevel()["special"])
                else:
                    dev.draw_image(
                        otherSnakes[peer][0][0]*11 + 7, otherSnakes[peer][0][1]*11 + 7, textures.getLevel()["normal"])
            otherSnakes[peer] = msg[2]
            player.displaySnake(otherSnakes[peer])
        elif msg[1] == 'newPomme':
            pomme = objects.Apple(msg[2], msg[3], msg[4])
            pomme.display()
            pommes.append(pomme)
        elif msg[1] == 'eatPomme':
            pommes.pop(msg[2])
        elif msg[1] == 'setLevel':
            setCurrentLevel(msg[2])
        elif msg[1] == 'setBlocks':
            blocks = msg[2]
            displayBlocks()
        elif me == None:
            start_game_soon(master() ^ int(random() * 2))
        else:
            print('received', peer, msg)


def networkStart():
    init_game()
    for id in mate.ids:
        net.send(id, [msg_type, ""])


def snake(n, hasAi):
    global networked, ai
    networked = n
    ai = hasAi

    if networked:
        mate.find(msg_type, message_handler,
                  lambda m, s: askMap(lambda: start(m, s)))

        def start(start_msg, mateStart):
            for id in mate.ids:
                net.send(id, start_msg)
                net.send(id, [msg_type, "setLevel", currentLevel])
            mateStart()
    else:
        askMap(snake_non_networked)


def askMap(then):
    def menu_handler(level, cont):
        if level is None:
            cont()
        elif level is False:
            quit()
        else:
            setCurrentLevel(level.lower())
            then()

    dev.clear_screen(bg)
    dev.draw_image(15, 30, textures.mapSelection)
    ui.menu(4, 111, 8, 7, 2, [apps.accent, '#000'], lambda: [
        "Sand", "Grass", "Space"], "Grass", menu_handler)


def showScore():
    quitWhenButtonOk()

    dev.clear_screen(bg)

    dev.draw_image(27, 10, textures.scoreText)
    ui.center(dev.screen_width//2, 220, " Quit ", bg, apps.accent)

    if len(classement.highscore) == 0:
        ui.center(dev.screen_width//2, 100, "No", apps.fg, bg)
        ui.center(dev.screen_width//2, 120, "scores", apps.fg, bg)
        ui.center(dev.screen_width//2, 140, "yet", apps.fg, bg)

    for i, score in enumerate(classement.highscore):
        ui.center(dev.screen_width//2, 100 + 20 * i, "#" +
                  str(i + 1) + " " + str(score), apps.fg, bg)


def quitWhenButtonOk():
    def handle(event, resume):
        if event == 'left_ok' or event == 'right_ok':
            quit()
        else:
            dev.after(0.1, resume)

    ui.track_button_presses(handle)


apps.register('SNAKE', lambda: snake(False, False), False)
apps.register('SNAKENET', lambda: snake(True, False), True)
apps.register('SCORE', lambda: showScore(), False)
apps.register('SNAKEAI', lambda: snake(False, True), False)
