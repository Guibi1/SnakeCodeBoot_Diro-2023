import ttgo as dev
import ui
import net
import splash
import textures

last_app = None  # last app used

apps = {}

fg = "#FFF"
bg = "#000"
accent = "#9E5"


def register(name, handler, networked):
    apps[name] = [handler, networked]


def menu():  # pick an app with a menu and call its handler
    stop = False

    def items():
        result = []
        for app in apps:
            if not apps[app][1] or net.connected:
                result.append(app)
        return result

    def menu_handler(item, cont):
        nonlocal stop
        global last_app
        if item is None or item is False:  # menu is asking to wait?
            dev.after(ui.time_delta, cont)
        else:  # an item was selected by the menu
            stop = True
            handler = apps[item][0]
            if handler:
                last_app = item
                handler()

    def animate(i):
        if stop:
            return
        if i == len(textures.titleAnimationIdle) - 1:
            animate(0)
            return
        dev.draw_image(15, 20, textures.titleAnimationIdle[i])
        dev.after(0.2, lambda: animate(i + 1))

    dev.clear_screen(bg)
    animate(0)

    ui.center(dev.screen_width//2, splash.mesg_y +
              dev.font_height//2, '\x1F\x1FAPPS\x1F\x1F', fg, bg)
    ui.menu(4, splash.mesg_y+16, 8, 5, 2,
            [accent, bg], items, last_app, menu_handler)
