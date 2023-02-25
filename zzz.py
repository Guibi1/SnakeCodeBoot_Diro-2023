import ttgo as dev
import splash
import apps

def zzz():
    splash.show()
    dev.stop()  # put device to sleep

apps.register('ZZZ', zzz, False)
