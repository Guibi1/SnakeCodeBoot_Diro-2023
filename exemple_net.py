import ttgo as dev
import net, mate

# Note : exécutez ce programme sur deux ordinateurs ou fenêtres de navigateur.

def handler(origine, msg):  # sera appellée à chaque message recu
    print(origine, "a envoyé", repr(msg))
    if origine is None and msg == "found_mate": message1()

# messages à envoyer en séquence :
def message1(): net.send(mate.id, [1, 2, 3]); dev.after(2, message2)
def message2(): net.send(mate.id, "hello");   dev.after(2, message3)
def message3(): net.send(mate.id, "world!")

mate.find("TEST", handler)  # chercher un partenaire