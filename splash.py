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

def logo():  # draw the logo

    um = '#00F'

    dev.clear_screen(bg)

    dev.draw_image(10, 20, textures.title[0], um, bg)

def show():
    logo()
    mesg()
