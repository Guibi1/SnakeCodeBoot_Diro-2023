import ttgo as dev
import splash
import apps

# apps
import snake
import zzz


def start():
    splash.show()            # show splash screen
    dev.after(2, apps.menu)  # after 2 seconds show app menu


start()
