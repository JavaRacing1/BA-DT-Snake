import tkinter as tk
from stackmaschine import maschine

def loop_init(widget: tk.Tk, __machine: maschine):
    __machine.stopped = False

    global root
    root = widget

    global machine
    machine = __machine

    global delay
    delay = 4000

    #Einmaliger Code hier hin

    machine.load_memory("./icons_spielfeld/test_icons.txt")

    machine.push(0)
    machine.dload8()
    machine.push(3584 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(1)
    machine.dload8()
    machine.push(3585 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(2)
    machine.dload8()
    machine.push(3586 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(3)
    machine.dload8()
    machine.push(3587 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(4)
    machine.dload8()
    machine.push(3588 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(5)
    machine.dload8()
    machine.push(3589 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(6)
    machine.dload8()
    machine.push(3590 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(7)
    machine.dload8()
    machine.push(3591 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()


    machine.push(8)
    machine.dload8()
    machine.push(3592 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(9)
    machine.dload8()
    machine.push(3593 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(10)
    machine.dload8()
    machine.push(3594 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(11)
    machine.dload8()
    machine.push(3595 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(12)
    machine.dload8()
    machine.push(3596 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(13)
    machine.dload8()
    machine.push(3597 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(14)
    machine.dload8()
    machine.push(3598 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(15)
    machine.dload8()
    machine.push(3599 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()



    #Adresse Kopf speichern
    machine.push(4352)
    machine.push(16)
    machine.dstore16()
    machine.pop()

    #Adresse Körper speichern
    machine.push(4360)
    machine.push(18)
    machine.dstore16()
    machine.pop()

    #Vertikaler Abstand zwischen 2 Blöcken
    machine.push(240)
    machine.push(48)
    machine.dstore()

    loop()

def down():
    #Kopfadresse zwischenspeichern
    machine.pop()
    machine.push(16)
    machine.dload16()
    machine.push(28)
    machine.dstore16()

    #Neue Kopfadresse berechnen
    machine.push(48)
    machine.dload8()
    machine.add()
    machine.push(16)
    machine.dstore16()
    machine.pop()

    #Ausgabe 
    machine.push(0)
    machine.dload16()
    machine.push(16)
    machine.dload16()
    machine.dstore16()
    machine.pop()

    machine.push(2)
    machine.dload16()
    machine.push(16)
    machine.dload16()
    machine.push(2)
    machine.add()
    machine.dstore16()
    machine.pop()

    machine.push(4)
    machine.dload16()
    machine.push(16)
    machine.dload16()
    machine.push(4)
    machine.add()
    machine.dstore16()
    machine.pop()

    machine.push(6)
    machine.dload16()
    machine.push(16)
    machine.dload16()
    machine.push(6)
    machine.add()
    machine.dstore16()
    machine.pop()


def loop():
    if machine.stopped:
        return
    print("--- Cycle ---")

    machine.push(1535)
    machine.dload8()

    machine.push(115) #Unten
    if (machine.jmc()):
        print("Unten")
        down()

    machine.pop()

    machine.push(119) #Oben
    if (machine.jmc()):
        print("Oben")
    machine.pop()

    machine.push(97) #Links
    if (machine.jmc()):
        print("Links")
    machine.pop()

    machine.push(100)  #Rechts
    if (machine.jmc()):
        print("Rechts")
    machine.pop()

    machine.pop()

    
    #Schleifencode hier hin
    
    root.after(delay, loop)