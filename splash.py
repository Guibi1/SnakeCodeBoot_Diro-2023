import textures
import ttgo as dev
import ui

fg = '#FFF'  # color of text
bg = '#000'  # color of background

mesg_y = 136  # y coordinate of messsage
logo_y = -94  # y coordinate of logo


def mesg():  # draw the message

    x = dev.screen_width//2

    ui.center(x, mesg_y+dev.font_height*2, 'HACK', fg, bg)
    ui.center(x, mesg_y+dev.font_height*3, 'A', fg, bg)
    ui.center(x-24, mesg_y+dev.font_height*3, '\x10', fg, bg)
    ui.center(x+24, mesg_y+dev.font_height*3, '\x11', fg, bg)
    ui.center(x, mesg_y+dev.font_height*4, 'THON', fg, bg)
    ui.center(x, mesg_y+dev.font_height*5, '2023', fg, bg)


def show():
    dev.clear_screen(bg)

    def animate(i):
        if i == len(textures.titleAnimation) - 1:
            return
        dev.draw_image(15, 20, textures.titleAnimation[i])
        dev.after(0.2, lambda: animate(i + 1))

    animate(0)
    mesg()
