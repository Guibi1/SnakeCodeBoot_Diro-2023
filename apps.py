import ttgo as dev
import ui
import net
import splash

last_app = None  # last app used

apps = {}

def register(name, handler, networked):
    apps[name] = [handler, networked]

def menu():  # pick an app with a menu and call its handler

    fg = '#4CF'
    bg = splash.bg

    def items():
        result = []
        for app in apps:
            if not apps[app][1] or net.connected:
                result.append(app)
        return result

    def menu_handler(item, cont):
        global last_app
        if item is None or item is False:  # menu is asking to wait?
            dev.after(ui.time_delta, cont)
        else:  # an item was selected by the menu
            handler = apps[item][0]
            if handler:
                last_app = item
                handler()

    splash.logo()
    ui.center(dev.screen_width//2, splash.mesg_y+dev.font_height//2, '\x1F\x1FAPPS\x1F\x1F', fg, bg)
    ui.menu(4, splash.mesg_y+16, 8, 5, 2, [fg, bg], items, last_app, menu_handler)
