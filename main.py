import ttgo as dev
import splash
import apps
import snake

def start():
    splash.show()
    dev.after(2, apps.menu)

start()
