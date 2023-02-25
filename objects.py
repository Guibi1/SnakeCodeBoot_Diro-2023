import ttgo as dev


class Objects():
    tex = ""
    x = 0
    y = 0

    def getPosition(self):
        return (self.x, self.y)

    def display(self):
        for pos in self.positions:
            dev.fill_rect(self.x*11 + 7, self.y*11 + 7, 11, 11, "#0f0")


class Blocs(Objects):
    tex = ""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Pommes(Objects):
    tex = ""
    score = 0

    def __init__(self):
        self.x = int(random()*11)
        self.y = int(random()*11)


class PommeBloc(Pommes):
    # position doit etre apres la queue du serpent
    tex = ""

    pass


class PommeNormale(Pommes):
    tex = ""
    score = 1


class Pomme10(Pommes):
    tex = ""
    score = 10


class PommePoison(Pommes):
    tex = ""


class PommeChrono(Pommes):
    tex = ""


class PommeMulti(Pommes):
    tex = ""

    def __init__(self):
        pommemulti1 = PommeNormale()
        pommemulti2 = PommeNormale()
        pommemulti3 = PommeNormale()


class PommePortail(Pommes):
    tex = ""


class PommeVitesse(Pommes):
    tex = ""


obj1 = PommeNormale()
obj2 = Pomme10()
obj3 = PommePoison()
obj4 = PommeChrono()
obj5 = PommeMulti()
obj6 = PommeVitesse()
obj7 = PommeBloc()
obj8 = Blocs(10, 10)
obj9 = PommePortail()


def getRandomPomme():
    nbRandom = int(random()*120+1)
    if nbRandom > 110:
        return PommeMulti()
    if nbRandom > 100:
        return PommePortail()
    if nbRandom > 90:
        return PommePoison()
    if nbRandom > 80:
        return PommeChrono()
    if nbRandom > 70:
        return PommeBloc()
    if nbRandom > 60:
        return PommeVitesse()
    if nbRandom > 50:
        return Pomme10()
    if nbRandom > 40:
        return PommeNormale()
