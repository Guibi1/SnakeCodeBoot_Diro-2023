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

    dev.draw_text(49,154+logo_y, '\xDB', um, bg)
    dev.draw_text(71,154+logo_y, '\xDB', um, bg)
    dev.draw_text(44, 96+logo_y, '\xDB \xDB', um, bg)
    dev.draw_text(44,112+logo_y, '\xDB \xDB', um, bg)
    dev.draw_text(44,128+logo_y, '\xDB \xDB', um, bg)
    dev.draw_text(44,144+logo_y, '\xDB \xDB', um, bg)
    dev.draw_text(22,170+logo_y, '\xDB', um, bg)
    dev.draw_text(31,170+logo_y, '\xDB', um, bg)
    dev.draw_text(55,170+logo_y, '\xDB', um, bg)
    dev.draw_text(66,170+logo_y, '\xDB', um, bg)
    dev.draw_text(89,170+logo_y, '\xDB', um, bg)
    dev.draw_text(98,170+logo_y, '\xDB', um, bg)
    dev.draw_text(12,184+logo_y, '\xDB \xDB \xDB \xDB', um, bg)
    dev.draw_text(12,200+logo_y, '\xDB \xDB \xDB \xDB', um, bg)
    dev.draw_text(12,210+logo_y, '\xDB \xDB \xDB \xDB', um, bg)

def show():
    logo()
    mesg()
