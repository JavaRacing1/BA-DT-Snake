#Temporäre Startwerte ----------------------------------------------
AdresseIconKopf = 0
AdresseIconKoerper = 0
AdresseKopf = 0
Eingabe = 0

#------------------------------------------------------------------

icon_kopf = AdresseIconKopf
icon_koerper = AdresseIconKoerper

pos_kopf = AdresseKopf
pos_koerper1 = 0
pos_koerper2 = 0
pos_koerper3 = 0
pos_koerper4 = 0
pos_koerper5 = 0
pos_koerper6 = 0
pos_koerper7 = 0

eingabe = Eingabe 
addr_eingabe = 4096

schrittweite_horizontal = 8
schrittweite_vertikal = 240


def load(addr, name):
  print('Loaded ' + addr + ' to ' + name)
  


while True:
    load(addr_eingabe, 'Eingabe')

    if (eingabe == 119): #w
        print()
    if (eingabe == 97): #a
        print()
    if (eingabe == 115): #s
        print()
    if (eingabe == 100): #d
        print()

