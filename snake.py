import ttgo as dev
import net
import mate
import apps
import ui
import random

bg = '#000'  # general background color

# game state

me = None  # is 0 when non-networked, and 0 or 1 when networked

# the following global variables are useful for the networked version

networked   = False  # are we playing over the network?
random_seed = 0      # to get same random order on both nodes, set later
msg_type    = None   # type of the messages sent between the nodes, set later
ping_timer  = 0      # used to check that the mate is still with us
pong_timer  = 0

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
    ui.center(x, dev.font_height*4, 'SNAKE', '#FFF', bg)
    ui.center(x, dev.font_height*5, 'TODO!', '#FFF', bg)

tick_counter = 0

def button_handler(event, resume):
    global ping_timer, pong_timer, tick_counter
    if me is None: return  # not yet playing or no longer playing
    if event == 'cancel':
        quit()
    elif event == 'tick':
        tick_counter += 1
        ui.center(dev.screen_width//2, dev.font_height*7, str(tick_counter), '#FFF', bg)
        if networked:
            pong_timer -= 1
            if pong_timer < 0:
                leave()
                return
            ping_timer -= 1
            if ping_timer < 0:
                ping_timer = int(2 / ui.time_delta)  # send ping every 2 secs
                net.send(mate.id, [msg_type, 'ping'])
        dev.after(ui.time_delta, resume) # need to wait...
    else:
        msg = '------'
        if event == 'left_down':
            msg = 'L-DOWN'
        elif event == 'right_down':
            msg = 'R-DOWN'
        elif event == 'left_up':
            msg = ' L-UP '
        elif event == 'right_up':
            msg = ' R-UP '
        elif event == 'left_ok':
            msg = ' L-OK '
        elif event == 'right_ok':
            msg = ' R-OK '
        ui.center(dev.screen_width//2, dev.font_height*5, msg, '#FFF', bg)
        resume()

def start_game_soon(player):
    dev.after(3, lambda: start_game(player))

def start_game(player):
    global me
    me = player
    reset_mate_timeout()
    ui.track_button_presses(button_handler)  # start tracking button presses
    dev.clear_screen(bg)
    x = dev.screen_width//2
    ui.center(x, dev.font_height*10, 'QUIT =', '#FFF', bg)
    ui.center(x, dev.font_height*11, 'PUSH', '#FFF', bg)
    ui.center(x, dev.font_height*12, 'BOTH', '#FFF', bg)
    ui.center(x, dev.font_height*13, 'BUTTONS', '#FFF', bg)

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
        if me == None:
            random.seed(random_seed ^ msg[1])  # set same RNG on both nodes
            # determine if we are player 0 or 1
            start_game_soon(master() ^ random.randrange(2))
        elif msg[1] == 'quit':
            leave()
        elif msg[1] == 'ping':
            reset_mate_timeout()
        else:
            print('received', peer, msg)

def found_mate():
    global random_seed

    init_game()

    # exchange random seeds so both nodes have the same RNG
    random_seed = random.randrange(0x1000000)
    net.send(mate.id, [msg_type, random_seed])

def snake_networked():
    global msg_type
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