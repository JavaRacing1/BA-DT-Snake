from time import sleep
import threading

#Icon-Werte
head_top = (60<<24) + (66<<16) + (129<<8) + 165
head_bottom = (165<<24) + (129<<16) + (66<<8) + 60
body_top = (60<<24) + (66<<16) + (129<<8) + 129
body_bottom = (129<<24) + (129<<16) + (66<<8) + 60
fruit_top = (32<<24) + (16<<16) + (60<<8) + 126
fruit_bottom = (126<<24) + (126<<16) + (60<<8)
border_top = (126<<16) + (126<<8) + 126
border_bottom = (126<<24) + (126<<16) + (126<<8)

#Delay zwischen jeder Schlangenbewegung (in ms)
delay = 200
#Startaddresse
start_addr = 4096 + (14*8) + (9*240)
#aktuelle Position des Kopfs
head_addr = 0
#Addresse des letzten Schlangenelements
tail_addr = 0
#Richtung, in die sich die Schlange bewegt (0=Stopp, 1=Oben, 2=Rechts, 3=Unten, 4=Links)
direction = 0

#----------------------------------- Snake-Steuerung ---------------------------------------------------

#Modul initialisieren
def init(mainstorage, tk):
    global ms
    ms = mainstorage

    global app
    app = tk

    global head_addr
    head_addr = start_addr

    global direction
    direction = 0

    #Randsteine setzen
    for i in range(30):
        ms.save_word(4096+(i*8), border_top)
        ms.save_word(4100+(i*8), border_bottom)
        ms.save_word(4096+(i*8)+(19*240), border_top)
        ms.save_word(4100+(i*8)+(19*240), border_bottom)

    for i in range(1, 19):
        ms.save_word(4096+(i*240), border_top)
        ms.save_word(4100+(i*240), border_bottom)
        ms.save_word(4096+(i*240)+(29*8), border_top)
        ms.save_word(4100+(i*240)+(29*8), border_bottom)

    #Kopf an Startposition zeichnen
    draw_head()

    #Schleife starten
    loop()

#Schleife zur Fortbewegung der Schlange
def loop():
    
    #Prüfen, ob Schlange stillsteht
    if not (direction == 0):
        global head_addr

        #Addresse zwischenspeichern um Delays beim zeichnen zu vermeiden
        new_head_addr = head_addr
        
        #Kopf-Position ändern
        x = 0
        y = 0
        
        match direction:
            case 1:
                y = -1
            case 2:
                x = 1
            case 3:
                y = 1
            case 4:
                x = -1
        
        new_head_addr = calculate_move(head_addr, x, y)

        #Alten Kopf löschen und neuen zeichnen
        reset_address(head_addr)
        head_addr = new_head_addr
        draw_head()
    
    app.after(delay, loop)

#Ändert die Richtung, in die sich die Schlange bewegt
def change_direction(input):
    global direction
    match input:
        case 'w':
            new_direction = 1
        case 'd':
            new_direction = 2
        case 's':
            new_direction = 3
        case 'a':
            new_direction = 4
    
    if not is_opposite_dir(new_direction):
        direction = new_direction
            


#------------------------------------- Snake-Tools ---------------------------------------------------

#Zeichnet den Kopf der Schlange an seiner aktuellen Addresse
def draw_head():
    ms.save_word(head_addr, head_top)
    ms.save_word(head_addr+4, head_bottom)

#Leert eine Addresse im Display
def reset_address(addr):
    ms.save_word(addr, 0)
    ms.save_word(addr+4, 0)

#Berechnet eine Bewegung von einer Addresse um x-Stellen nach links/rechts und um y-Stellen nach oben/unten aus
def calculate_move(addr, x, y):
    return addr + (x*8) + (y*240)

#Prüft, ob die neue Richtung das Gegenteil der alten Richtung ist
def is_opposite_dir(new_direction):
    # 3 = senkrecht, 8 = waagerecht
    # 1 (Oben) * 3 (Unten) = 3
    # 2 (Rechts) * 4 (Links) =8
    return (new_direction*direction == 3) or (new_direction*direction == 8)