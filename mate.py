import ttgo as dev
import net
import ui
import apps
import splash

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

    color = '#4CF'

    fg = '#FFF'
    bg = '#A00'

    dev.clear_screen(splash.bg)

    dev.fill_rect(0, 0, dev.screen_width, 58, bg)
    ui.center(dev.screen_width//2, 10, activity, fg, bg)

    ui.center(dev.screen_width//2, 38, net.id, color, bg)

    fg = '#FFF'
    bg = '#666'

    dev.fill_rect(0, 58, dev.screen_width, 50, bg)
    ui.center(dev.screen_width//2, 70, 'choose', fg, bg)
    ui.center(dev.screen_width//2, 86, 'mate', fg, bg)

    ui.menu(4, 111, 8, 7, 2, [color, '#000'], peers, "Start", menu_handler)


def find(activity, message_handler):  # message_handler called when mate is found
    global ids

    ids = []          # no mate found yet
    proposing = None   # peer that we are proposing to mate with

    # message sent to peer to propose and accept to mate for this activity
    mating_msg = [None, activity]
    start_msg = ["START", activity]

    def mate_message_handler(peer, msg):
        global ids
        nonlocal proposing

        if msg == mating_msg:  # mating reply proposal or acceptance?
            if (proposing is None or proposing == peer) and peer not in ids:
                print("MATE " + peer)
                net.send(peer, mating_msg)  # accept mating proposal
                proposing = None
                ids.append(peer)
        elif msg == start_msg:
            start()
        else:
            return True  # allow previous handler to handle message

    def start():
        net.pop_handler()  # stop calling mate_message_handler
        message_handler(None, 'start')

    def menu_handler(peer, cont):
        nonlocal proposing

        if peer is None:  # menu is asking to wait?
            dev.after(ui.time_delta, cont)
        elif peer is False:  # cancel?
            net.pop_handler()  # stop calling mate_message_handler
            net.pop_handler()  # stop calling app's handler
            apps.menu()
        elif peer == "Start":  # Start
            for id in ids:
                net.send(id, start_msg)
            start()
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
