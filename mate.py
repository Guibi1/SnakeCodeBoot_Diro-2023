import ttgo as dev
import net
import ui
import apps
import textures

network_id = 'TEAM11'

wifi_ssid = 'eero'      # the wifi's SSID and password
wifi_pwd = 'wifiwifi'

ids = []  # id of the peer we mated with

reply_timeout = 2  # wait 2 seconds for mating proposal reply

wifi_started = False


def connect_to_net():
    global wifi_started
    if not wifi_started:
        wifi_started = True
        net.set_wifi(wifi_ssid, wifi_pwd)
        connect_to_network_id()


def connect_to_network_id():
    dev.after(2, connect_to_network_id_loop)


def connect_to_network_id_loop():
    if not net.connected:
        net.connect(network_id, lambda peer, msg: None)
        connect_to_network_id()


connect_to_net()


def peers():
    if len(ids) > 0:
        return list(net.peers()) + ["Start"]
    return list(net.peers())


def peers_menu(activity, menu_handler):
    dev.clear_screen(apps.bg)

    dev.draw_image(40, 20, textures.ffaText)

    ui.center(dev.screen_width//2, 38, net.id, apps.accent, apps.bg)

    bg = '#666'

    dev.fill_rect(0, 58, dev.screen_width, 50, bg)
    ui.center(dev.screen_width//2, 70, 'choose', apps.fg, bg)
    ui.center(dev.screen_width//2, 86, 'mate', apps.fg, bg)

    ui.menu(4, 111, 8, 7, 2, [apps.accent, apps.bg],
            peers, "Start", menu_handler)


def find(activity, message_handler, startHandle):  # message_handler called when mate is found
    global ids

    ids = []          # no mate found yet
    proposing = None   # peer that we are proposing to mate with

    # message sent to peer to propose and accept to mate for this activity
    mating_msg = [None, activity]
    start_msg = ["START", activity]
    starting = False

    def start():
        nonlocal starting
        starting = True
        net.pop_handler()  # stop calling mate_message_handler
        message_handler(None, 'start')

    def mate_message_handler(peer, msg):
        global ids
        nonlocal proposing

        if msg == mating_msg:  # mating reply proposal or acceptance?
            if (proposing is None or proposing == peer) and peer not in ids:
                net.send(peer, mating_msg)  # accept mating proposal
                proposing = None
                ids.append(peer)
        elif msg == start_msg:
            start()
        else:
            return True  # allow previous handler to handle message

    def menu_handler(peer, cont):
        nonlocal proposing

        if starting:
            return
        elif peer is None:  # menu is asking to wait?
            dev.after(ui.time_delta, cont)
        elif peer is False:  # cancel?
            net.pop_handler()  # stop calling mate_message_handler
            net.pop_handler()  # stop calling app's handler
            apps.menu()
        elif peer == "Start":  # Start
            startHandle(start_msg, start)
        else:  # a peer was selected by the menu
            # limit how long to listen for the reply to the mating proposal
            timer = int(reply_timeout / ui.time_delta)

            def listen():
                nonlocal proposing, timer
                timer -= 1
                if timer < 0:  # mating offer timed out?
                    proposing = None
                    cont()  # continue menu navigation
                else:  # check again for a reply soon
                    dev.after(ui.time_delta, listen)

            proposing = peer            # start proposing to the peer
            net.send(peer, mating_msg)  # send mating proposal to the peer
            listen()                    # listen for the reply

    def wait_until_connected():
        if net.connected:
            net.push_handler(message_handler)  # install app's handler
            net.push_handler(mate_message_handler)  # intercept mating messages
            peers_menu(activity, menu_handler)
        else:
            dev.after(1, wait_until_connected)

    wait_until_connected()
