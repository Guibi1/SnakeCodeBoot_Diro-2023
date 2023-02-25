import ttgo as dev
import net
import mate
import apps
import ui
import playerSnake as player
import objects
import textures

bg = '#000'  # general background color
currentLevel = "grass"
width = 11
height = 18

# game state

me = None  # is 0 when non-networked, and 0 or 1 when networked

# the following global variables are useful for the networked version

networked = False  # are we playing over the network?
random_seed = 0      # to get same random order on both nodes, set later
msg_type = None   # type of the messages sent between the nodes, set later
ping_timer = 0      # used to check that the mate is still with us
pong_timer = 0


def reset_mate_timeout():
    global pong_timer
    pong_timer = int(5 / ui.time_delta)  # reset peer timeout to 5 seconds


def quit():  # called to quit the game
    if networked:
        net.send(mate.id, [msg_type, 'quit'])
    leave()


def leave():
    global me
    me = None  # no longer playing
    if networked:
        net.pop_handler()  # remove message_handler
    apps.menu()  # go back to app menu


def init_game():
    global me

    me = None

    dev.clear_screen(bg)

    x = dev.screen_width//2
    dev.fill_rect(10, 10, 12, 12, "#F00")

    ui.center(x, dev.font_height*4, 'SNAKE', '#FFF', bg)
    ui.center(x, dev.font_height*5, 'TODO!', '#FFF', bg)


tileIsSpecial = []
for x in range(width):
    row = []
    tileIsSpecial.append(row)
    for y in range(height):
        row.append(random() > 0.9)

tick_counter = 1
playerSnake = player.PlayerSnake()
playerSnake.display()
pomme = None
blocks = []


def button_handler(event, resume):
    global ping_timer, pong_timer, tick_counter, pomme, blocks
    if me is None:
        return  # not yet playing or no longer playing
    if event == 'cancel':
        quit()
    elif event == 'tick':
        tick_counter += 1

        ui.center(dev.screen_width//2, dev.screen_height -
                  16, "Score " + str(playerSnake.score), '#FFF', bg)

        if tick_counter % 5 != 0:
            dev.after(ui.time_delta, resume)  # need to wait...
            return

        rallonger = False
        if pomme is None:
            pomme = objects.getRandomPomme()
            pomme.display()
        elif playerSnake.positions[-1] == pomme.getPosition():
            playerSnake.manger(pomme, blocks)
            pomme = None
            rallonger = True

        if not rallonger:
            if tileIsSpecial[playerSnake.positions[0][0]][playerSnake.positions[0][1]]:
                dev.draw_image(
                    playerSnake.positions[0][0]*11 + 7, playerSnake.positions[0][1]*11 + 7, textures.levels[currentLevel]["special"])
            else:
                dev.draw_image(
                    playerSnake.positions[0][0]*11 + 7, playerSnake.positions[0][1]*11 + 7, textures.levels[currentLevel]["normal"])

        playerSnake.move(rallonger)
        playerSnake.display()

        if networked:
            pong_timer -= 1
            if pong_timer < 0:
                leave()
                return
            ping_timer -= 1
            if ping_timer < 0:
                ping_timer = int(2 / ui.time_delta)  # send ping every 2 secs
                net.send(mate.id, [msg_type, 'ping'])
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
        elif event == 'left_up':
            pass
        elif event == 'right_up':
            pass
        elif event == 'left_ok':
            pass
        elif event == 'right_ok':
            pass
        resume()


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
                               textures.levels[currentLevel]["special"])
            else:
                dev.draw_image(7 + x * 11, 7 + y * 11,
                               textures.levels[currentLevel]["normal"])


def snake_non_networked():
    init_game()
    start_game_soon(0)

# The following functions are used when playing the game over the network


def master():  # the master is the node with the smallest id
    return net.id < mate.id


def message_handler(peer, msg):
    global pong_timer
    if peer is None:
        if msg == 'found_mate':
            found_mate()
        else:
            print('system message', msg)  # ignore other messages from system
    elif type(msg) is list and msg[0] == msg_type:
        if msg[1] == 'quit':
            leave()
        elif msg[1] == 'ping':
            reset_mate_timeout()
        elif me == None:
            random.seed(random_seed ^ msg[1])  # set same RNG on both nodes
            # determine if we are player 0 or 1
            start_game_soon(master() ^ random.randrange(2))
        else:
            print('received', peer, msg)


def found_mate():
    init_game()
    net.send(mate.id, [msg_type, random_seed])


def snake_networked():
    global msg_type, random_seed
    # exchange random seeds so both nodes have the same RNG
    random_seed = random.randrange(0x1000000)
    msg_type = 'SNAKENET'
    mate.find(msg_type, message_handler)


def snake(n):
    global networked
    networked = n
    if networked:
        snake_networked()
    else:
        snake_non_networked()


apps.register('SNAKE', lambda: snake(False), False)
apps.register('SNAKENET', lambda: snake(True), True)
