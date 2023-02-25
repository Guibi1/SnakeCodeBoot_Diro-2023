import pixels
import js
import _ffi

screen_width  = 135  # screen size
screen_height = 240

cb = document.querySelector('.cb-vm')
if cb.hasAttribute('data-cb-floating') or cb.hasAttribute('data-cb-hidden'):
    pixels.setScreenMode(screen_width, screen_height, 3)  # scale up
else:
    pixels.setScreenMode(screen_width, screen_height)

def clear_screen(color):
    fill_rect(0, 0, screen_width, screen_height, color)

def set_pixel(x, y, color):
    pixels.setPixel(x, y, color)

def fill_rect(x, y, w, h, color):
    pixels.fillRectangle(x, y, w, h, color)

def draw_image(x, y, image):
    pixels.drawImage(x, y, image)

def draw_text(x, y, text, fg, bg):
    pixels.drawText(x, y, text, fg, bg)

font_width  = 16  # font size
font_height = 16

def button(index):
    if index == 0:
        return host_eval('rte.vm.cb.keyboard.shiftLeft')
    else:
        return host_eval('rte.vm.cb.keyboard.shiftRight')

def after(delay, callback):
    js.setTimeout(callback, delay*1000)

def stop():
    return host_eval('rte.vm.processEvent("stop")')