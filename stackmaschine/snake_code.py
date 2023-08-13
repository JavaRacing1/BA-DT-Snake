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

    machine.push(512)
    machine.dload8()
    machine.push(3584 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(513)
    machine.dload8()
    machine.push(3585 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(514)
    machine.dload8()
    machine.push(3586 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(515)
    machine.dload8()
    machine.push(3587 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(516)
    machine.dload8()
    machine.push(3588 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(517)
    machine.dload8()
    machine.push(3589 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(518)
    machine.dload8()
    machine.push(3590 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(519)
    machine.dload8()
    machine.push(3591 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()


    machine.push(520)
    machine.dload8()
    machine.push(3592 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(521)
    machine.dload8()
    machine.push(3593 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(522)
    machine.dload8()
    machine.push(3594 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(523)
    machine.dload8()
    machine.push(3595 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(524)
    machine.dload8()
    machine.push(3596 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(525)
    machine.dload8()
    machine.push(3597 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(526)
    machine.dload8()
    machine.push(3598 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()

    machine.push(527)
    machine.dload8()
    machine.push(3599 + 512 + 240*3 + 8*6)
    machine.dstore()
    machine.pop()



    #Adresse Kopf speichern
    machine.push(4864)
    machine.push(528)
    machine.dstore16()
    machine.pop()

    #Adresse Körper speichern
    machine.push(4872)
    machine.push(530)
    machine.dstore16()
    machine.pop()

    #Vertikaler Abstand zwischen 2 Blöcken
    machine.push(240)
    machine.push(560)
    machine.dstore()
    machine.pop()
    #Horizontaler Abstand zwischen 2 Blöcken
    machine.push(8)
    machine.push(561)
    machine.dstore()
    machine.pop()

    machine.push(4880)
    machine.push(554)
    machine.dstore16()
    machine.pop()

    loop()


def loop():
    if machine.stopped:
        return
    print("--- Cycle ---")
    valide_eingabe = False

    #Wert der Kopfadresse in 1. Hilfsvariable speichern
    machine.push(528)
    machine.dload16()
    machine.push(552)
    machine.dstore16()
    machine.pop()

    #1. Körperteiladresse in 4. Hilfsvariable speichern
    machine.push(530)
    machine.push(558)
    machine.dstore16()
    machine.pop()

    #Eingabe laden
    machine.push(2047)
    machine.dload8()

    #Nach unten vergleichen
    machine.push(115)
    if (machine.jmc()):
        print("Unten")
        valide_eingabe = True
        unten()
    machine.pop()

    #Nach oben vergleichen
    machine.push(119)
    if (machine.jmc()):
        print("Oben")
        valide_eingabe = True
        oben()
    machine.pop()

    #Nach links vergleichen
    machine.push(97)
    if (machine.jmc()):
        print("Links")
        valide_eingabe = True
        links()
    machine.pop()

    #Nach rechts vergleichen
    machine.push(100)
    if (machine.jmc()):
        print("Rechts")
        valide_eingabe = True
        rechts()
    machine.pop()
    machine.pop()

    #Eingabe mit zwischengespeicherter Eingabe ersetzen
    machine.push(562)
    machine.dload8()
    machine.push(2047)
    machine.dstore()
    machine.pop()

    while valide_eingabe:
        #Bildschirm-Körperteiladresse aus 4. Hilfsvariable laden
        machine.push(558)
        machine.dload16()
        machine.dload16()

        #Wert in 2. Hilfsvariable speichern
        machine.push(554)
        machine.dstore16()
        machine.pop()

        #Wert der alten Körperadresse aus 1. Hilfsvariable laden
        machine.push(552)
        machine.dload16()

        #Körperelement bekommt alte Körperadresse
        machine.push(558)
        machine.dload16()
        machine.dstore16()
        machine.pop()

        #Wert der 2. Hilfsvariable laden
        machine.push(554)
        machine.dload16()

        #1. Hilfsvariable bekommt Wert der 2. Hilfsvariable
        machine.push(552)
        machine.dstore16()
        machine.pop()

        #Wert der 4. Hilfsvariable laden
        machine.push(558)
        machine.dload16()

        #Neue Körperadresse berechnen und in 4. Hilfsvariable speichern
        machine.push(2)
        machine.add()
        machine.push(558)
        machine.dstore16()
        machine.pop()

        #Prüfen, ob außerhalb des Körperteil-Speichers
        machine.push(558)
        machine.dload16()
        machine.push(550)

        if (machine.jmc()):
            machine.pop()
            machine.pop()
            break

        machine.pop()
        machine.pop()

        #Prüfen, ob neue Adresse 0 enthält
        machine.push(558)
        machine.dload16()
        machine.dload16()
        machine.push(0)

        if (machine.jmc()):
            machine.pop()
            machine.pop()
            break
        
        machine.pop()
        machine.pop()

    anzeige()

    #Schleifencode hier hin
    
    root.after(delay, loop)

def anzeige():
    #Adresse des Bitmusters spiechern
    machine.push(512)
    machine.push(556)
    machine.dstore16()
    machine.pop()

    #Adresse des Kopfes speichern
    machine.push(528)
    machine.push(558)
    machine.dstore16()
    machine.pop()

    while True:
        #Ersten Teil des Bitmusters laden
        machine.push(556)
        machine.dload16()
        machine.dload16()

        #Adresse des Körperteils laden
        machine.push(558)
        machine.dload16()
        machine.dload16()

        #Erster Teil wird in Bildschirm geladen
        machine.dstore16()
        machine.pop()

        #Bitmusteradresse wird erhöht
        machine.push(556)
        machine.dload16()
        machine.push(2)
        machine.add()

        #2. Teil des Bitmusters geladen
        machine.dload16()

        #Adresse des Körperteils laden + erhöht
        machine.push(558)
        machine.dload16()
        machine.dload16()
        machine.push(2)
        machine.add()

        #Zweiter Teil wird in Bildschirm geladen
        machine.dstore16()
        machine.pop()

        #Bitmusteradresse wird erhöht
        machine.push(556)
        machine.dload16()
        machine.push(4)
        machine.add()

        #3. Teil des Bitmusters geladen
        machine.dload16()

        #Adresse des Körperteils laden + erhöht
        machine.push(558)
        machine.dload16()
        machine.dload16()
        machine.push(4)
        machine.add()

        #Dritter Teil wird in Bildschirm geladen
        machine.dstore16()
        machine.pop()


        #Bitmusteradresse wird erhöht
        machine.push(556)
        machine.dload16()
        machine.push(6)
        machine.add()

        #4. Teil des Bitmusters geladen
        machine.dload16()

        #Adresse des Körperteils laden + erhöht
        machine.push(558)
        machine.dload16()
        machine.dload16()
        machine.push(6)
        machine.add()

        #Vierter Teil wird in Bildschirm geladen
        machine.dstore16()
        machine.pop()

        #Prüfen, ob Bitmuster noch auf Kopf ist
        machine.push(556)
        machine.dload16()
        machine.push(512)
        if (machine.jmc()):
            kopf_zu_koerper()

        machine.pop()
        machine.pop()

        #Körperadresse um 2 erhöhen -> nächstes Körperteil
        machine.push(558)
        machine.dload16()
        machine.push(2)
        machine.add()

        #Neue Körperadresse speichern
        machine.push(558)
        machine.dstore16()
        machine.pop()

        #Prüfen, ob außerhalb der Schlange
        # machine.push(2)
        # machine.push(558)
        # machine.dload16()
        # machine.sub()
        # machine.dload16()
        # machine.push(0)
        # if (machine.jmc()):
        #     machine.pop()
        #     machine.pop()
        #     machine.push(0)
        #     machine.push(2)
        #     machine.push(558)
        #     machine.dload16()
        #     machine.sub()
        #     machine.dstore16()
        #     machine.pop()

        #     break
        # machine.pop()
        # machine.pop()

        #Alten Schwanz mit Nullen füllen
        machine.push(558)
        machine.dload16()
        machine.dload16()
        machine.push(0)
        if (machine.jmc()):
            machine.pop()
            machine.pop()

            machine.push(554)
            machine.dload16() #Adresse des alten Körperteils


            machine.dup()
            machine.push(0)
            machine.swap()
            machine.dstore16()
            machine.pop()

            #Stack: 1.Duplizierter Wert -> alte adress 1. Stück
            machine.push(2)
            machine.add()
            machine.dup()
            machine.push(0)
            machine.swap()
            machine.dstore16()
            machine.pop()

            machine.push(2)
            machine.add()
            machine.dup()
            machine.push(0)
            machine.swap()
            machine.dstore16()
            machine.pop()

            machine.push(2)
            machine.add()
            machine.push(0)
            machine.swap()
            machine.dstore16()
            machine.pop()



            # machine.push(558)
            # machine.dload16()
            # machine.dstore16()
            # machine.pop()

            # machine.push(1000)
            # machine.push(556)
            # machine.dstore16()
            # machine.pop()
            break
        machine.pop()
        machine.pop()

        #Prüfen, ob außerhalb des Körperteil-Speichers
        machine.push(558)
        machine.dload16()
        machine.push(550)
        if (machine.jmc()):
            machine.pop()
            machine.pop()
            break
        machine.pop()
        machine.pop()
        
        #Prüfen, ob neue Adresse 0 enthält
        # machine.push(558)
        # machine.dload16()
        # machine.dload16()
        # machine.push(0)

        # if (machine.jmc()):
        #     machine.pop()
        #     machine.pop()
        #     break
        
        # machine.pop()
        # machine.pop()


def kopf_zu_koerper():
    #Bitmuster von Koerper zu Kopf wechseln
    machine.push(520)
    machine.push(556)
    machine.dstore16()
    machine.pop()

def unten():
    machine.pop()
    machine.pop()

    #Kopfadresse laden
    machine.push(528)
    machine.dload16()
    #Vertikale Adressänderung laden
    machine.push(560)
    machine.dload8()
    machine.add()

    #Berechneten wert speichern
    machine.push(528)
    machine.dstore16()
    machine.pop()

    #Eingabe zwischenspeichern
    machine.push(2047)
    machine.dload8()
    machine.push(562)
    machine.dstore()
    machine.pop()

def oben():
    machine.pop()
    machine.pop()

    #Vertikale Adressänderung laden
    machine.push(560)
    machine.dload8()
    #Kopfadresse laden
    machine.push(528)
    machine.dload16()
    machine.sub()

    #Berechneten wert speichern
    machine.push(528)
    machine.dstore16()
    machine.pop()

    #Eingabe zwischenspeichern
    machine.push(2047)
    machine.dload8()
    machine.push(562)
    machine.dstore()
    machine.pop()

def links():
    machine.pop()
    machine.pop()
    #Horizontrale Adressänderung laden
    machine.push(561)
    machine.dload8()
    #Kopfadresse laden
    machine.push(528)
    machine.dload16()
    machine.sub()

    #Berechneten wert speichern
    machine.push(528)
    machine.dstore16()
    machine.pop()

    #Eingabe zwischenspeichern
    machine.push(2047)
    machine.dload8()
    machine.push(562)
    machine.dstore()
    machine.pop()

def rechts():
    machine.pop()
    machine.pop()

    #Kopfadresse laden
    machine.push(528)
    machine.dload16()
    #Horizontrale Adressänderung laden
    machine.push(561)
    machine.dload8()
    machine.add()

    #Berechneten wert speichern
    machine.push(528)
    machine.dstore16()
    machine.pop()

    #Eingabe zwischenspeichern
    machine.push(2047)
    machine.dload8()
    machine.push(562)
    machine.dstore()
    machine.pop()