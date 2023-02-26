currentLevel = "grass"


def loadAsset(name, type):
    return open(currentLevel + "-" + name + ("-" + type) if type is not None else "").read()


def loadTitle(name):
    return open(name).read()
