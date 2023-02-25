import ttgo as dev
import net

time_delta = 0.05  # time increment for polling buttons, etc
long_press = 0.5   # after 0.5 seconds button press is "long"

def pad(text, width):  # pad text with spaces at end
    return text + ' ' * (width - len(text))

def center(x, y, text, fg, bg):
    dev.draw_text(x-len(text)*dev.font_width//2, y-dev.font_height//2, text, fg, bg)

def draw_status(lines, direction, fg, bg):
    x = dev.screen_width//2
    y = dev.font_height//2
    h = dev.font_height*len(lines)
    if direction < 0:
        y += dev.screen_height - dev.font_height
        dev.fill_rect(0, dev.screen_height-h, dev.screen_width, h, bg)
    else:
        dev.fill_rect(0, 0, dev.screen_width, h, bg)
    for i in range(len(lines)):
        center(x, y + dev.font_height*direction*i, lines[i], fg, bg)

def when_buttons_released(done):  # call done when both buttons not pressed
    if dev.button(0) or dev.button(1):
        dev.after(time_delta, lambda: when_buttons_released(done))
    else:
        done()

def track_button_presses(handler):  # call handler according to button presses

    def main_loop():
        track_button_presses(handler)

    def main_loop_when_released():
        if dev.button(0) or dev.button(1):
            handle('tick', main_loop_when_released)
        else:
            main_loop()

    def handle(event, cont):
        dev.after(0, lambda: handler(event, cont))

    b0 = dev.button(0)  # read state of buttons
    b1 = dev.button(1)

    if not b0 and not b1:  # no buttons pressed?
        handle('tick', main_loop)
    else:

        # determine if it is a long press and generate event for handler

        timer = int(long_press / time_delta)
        pressed = 0 if b0 else 1
        cancelled = False

        def inner_loop():
            nonlocal timer, cancelled
            if dev.button(1-pressed):  # both buttons pressed?
                cancelled = True
            if not dev.button(pressed):  # button was released
                if cancelled:
                    handle('tick', main_loop)  # ignore button press
                else:
                    # short press of one button: generate "up" event
                    handle('left_up' if b0 else 'right_up', main_loop)
            elif timer <= 0:  # long press?
                if cancelled:
                    if dev.button(1-pressed):
                        # long press of both buttons: generate "cancel" event
                        handle('cancel', main_loop_when_released)
                    else:
                        handle('tick', main_loop)  # ignore button press
                else:
                    # long press of one button: generate "ok" event
                    handle('left_ok' if b0 else 'right_ok', main_loop_when_released)
            else:
                timer -= 1
                handle('tick', inner_loop)  # check again soon

        # indicate start of button press
        handle('left_down' if b0 else 'right_down', inner_loop)

def menu(x, y, width, height, linespacing, colors, get_choices, selection, handler):

    cursor = height//2
    cursor_y = y + cursor*(dev.font_height+linespacing)
    selected = 0
    timer = 0
    start_selection = ''

    def handle(event, cont):
        dev.after(0, lambda: handler(event, cont))

    def get_choices_sorted():
        return sort(list(get_choices()))

    choices = get_choices_sorted()
        
    def get_selected(default):
        return choices[selected] if selected < len(choices) else default

    def set_selected(selection):
        nonlocal selected
        selected = 0
        if selection:
            while selected < len(choices)-1:
                if selection <= choices[selected]:
                    break
                selected += 1

    def draw_menu():
        nonlocal selection
        for i in range(height):
            j = i - cursor + selected
            yy = y + i*(dev.font_height+linespacing)
            fg = colors[i == cursor]
            bg = colors[i != cursor]
            if j >= 0 and j < len(choices):
                text = choices[j]
            else:
                text = ''
            dev.draw_text(x, yy, pad(text, width), fg, bg)
        selection = get_selected('')

    def refresh():
        nonlocal timer, choices
        timer = int(1 / time_delta) # refresh every second
        new_choices = get_choices_sorted()
        if new_choices != choices:
            choices = new_choices
            set_selected(selection)
            draw_menu()

    def invalid_choice():
        dev.draw_text(x, cursor_y, pad('invalid', width), '#000', '#F00')
        when_buttons_released(refresh_and_start)

    def button_handler(event, resume):
        nonlocal selected, timer, selection, start_selection
        if event == 'left_down' or event == 'right_down':
            start_selection = selection
            resume()
        elif event == 'left_up':
            if selected > 0:
                selected -= 1
                draw_menu()
            resume()
        elif event == 'right_up':
            if selected < len(choices)-1:
                selected += 1
                draw_menu()
            resume()
        elif event == 'left_ok' or event == 'right_ok':
            result = get_selected(None)
            if result is None:
                refresh_and_start()
            elif result == start_selection:
                dev.draw_text(x, cursor_y, pad(selection, width), '#000', '#FF0')
                handle(result, invalid_choice)
            else:
                when_buttons_released(refresh_and_start)
        elif event == 'cancel':
            handle(False, refresh_and_start)
        elif event == 'tick':
            timer -= 1
            if timer < 0:
                refresh()
            handle(None, resume) # need to wait... event is continuation

    def refresh_and_start():
        refresh()
        start()

    def start():
        draw_menu()
        track_button_presses(button_handler)

    set_selected(selection)
    when_buttons_released(start)

def sort(lst):
    lst = lst[:]
    hi = len(lst)-1
    while hi > 0:
        lo = hi-1
        while lo >= 0:
            if lst[lo] > lst[hi]:
                t = lst[lo]
                lst[lo] = lst[hi]
                lst[hi] = t
            lo -= 1
        hi -= 1
    return lst
