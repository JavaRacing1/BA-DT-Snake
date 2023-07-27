import tkinter as tk
import stackmaschine

def loop_init(widget: tk.Tk, __machine: stackmaschine.maschine):
    __machine.stopped = False

    global root
    root = widget

    global machine
    machine = __machine

    global delay
    delay = 2000

    #Einmaliger Code hier hin

    loop()


def loop():
    if machine.stopped:
        return
    
    #Schleifencode hier hin
    
    root.after(delay, loop)