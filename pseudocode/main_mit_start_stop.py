
#Vorinitialierung Startwerte aus Spielfeldgenerierung

schlange_segmente_beginn = 3 # Startsegmente
anzahl_fruechte = 0 #Anzahl Körperteile abhängig durch eingesammelte Früchte
anzahl_koerper_max = 8 # maximale Länge == Sieg --> AnzahlFrüchte == 5 bedeutet auch Sieg
abstand_horizontal = 15 # von Mitte zum linken Rand --> wenn == 0 oder == 29 Niederlage
abstand_vertikal = 10  # von Mitte zum oberern Rand --> wenn == 0 oder == 19 Niederlage
zustand_spiel = 0 # für Auswertung ob Sieg bleibt ZustandSpiel gleich 0 oder ZustandSpiel wird durch einen der eintretenden Niederlagenfälle größer 0 verändert

#Speicheradressen der Früchte (5 Früchte vorplatziert, aber immer nur eine aktiv)
#aktive Frucht über AnzahlFrucht definiert (d.h. Frucht 1 wenn AnzahlFrucht = 0, Frucht 2 wenn AnzahlFrucht = 2,...)
#aktive Frucht muss immer Icon ins Spielfeld reingeladen werden, sollte die derzeit aktive Frucht erfolgreich eingesammelt werden

def load_icon(icon_addr, display_addr):
    for i in range(8):
        load(icon_addr + i)
        store(display_addr + i)

frucht1 = AdresseFrucht1 
Lade (FruchtIcon,PosiionFrucht1) #durch Spielfeldgenerierung schon vorgegeben im Spielzug 0
frucht2 = AdresseFrucht2
frucht3 = AdresseFrucht3
frucht4 = AdresseFrucht4
frucht5 = AdresseFrucht5

#Speicheradresse der Schlangenkörpersegmente
#Kopfsegmentadresse wird bei jeder erfolgreichen Bewegung an jeweils dahinter folgendendes Segment übergeben
#Bei Spielstart (noch keine Bewegung) nur Kopfsegment geladen mit Icon

schlangen_kopf = AdresseKopf
Lade (SchlangeKopfIcon,PositionSchlangeKopf) #durch Spielfeldgenerierung schon vorgegeben im Spielzug 0
schlangen_koerper1 = AdresseKörper1 # müsste durch "Bewegungsfunktion ständig erneuert werden und an die 8 Variablen für Vergleich übergeben
schlangen_koerper2 = AdresseKörper2 # bzw. wenn es möglich ist im COMPARE Microbefehl für die zwei Adressen (Kopf und jeweiliges Körpersegment) einen seperaten LOAD Befehl 
schlangen_koerper3 = AdresseKörper3 # mit reinzubauen, dann kann man sich diese 7 - 8 Variablen / extra Adressen sparen
schlangen_koerper4 = AdresseKörper4
schlangen_koerper5 = AdresseKörper5
schlangen_koerper6 = AdresseKörper6
schlangen_koerper7 = AdresseKörper7

#Spielbewegung der Schlange für Randpositionsvergeleich
#um Variablen (Adressen) AbstandHorizontal und AbstandVertikal jeweils zu incrementieren oder decrementieren zu können
#könnte vielleicht als einfache Integerzahl angegeben werden (links = 0, oben = 1, rechts = 2, unten = 3)
aktuelle_spielrichtung = AdresseSpielrichtung #Speicherort der Spielrichtung von "Bewegungs - Funktion"

#Sieg und Niederlagen Abfragen, die am Ende jedes Spielzuges abgefragt werden
#Schleifenkonstruktion kann auch mit den Befehlen für die "Bewegung" und für das "Wachstum" erweitert werden

while (anzahl_koerper_max > (schlange_segmente_beginn + anzahl_fruechte)): #Siegbedingung --> sollte dies erreicht werden nach while Schleife noch was für Sieg mit Spielfeld machen (Sieg mit den Randpixeln schreiben oder einen Smiley generieren)
    #Abfrage Niederlage durch Berühren des Randes
    if (abstand_horizontal == 0) or (abstand_horizontal == 29): #Randpositionen bei 0 (links) und 29 (rechts) 
        zustand_spiel = 1
        break
	
    if (abstand_vertikal == 0) or (abstand_vertikal == 19): #Randpositionen bei 0 (oben) und 19 (unten)
        zustand_spiel = 1
        break
	
	#Abstände an aktuelle Bewegung anpassen
    if (aktuelle_spielrichtung == 0):
        abstand_horizontal = abstand_horizontal - 1
    if (aktuelle_spielrichtung == 1):
        abstand_vertikal = abstand_vertikal - 1
    if (aktuelle_spielrichtung == 2):
        abstand_horizontal = abstand_horizontal + 1
    if (aktuelle_spielrichtung == 3):
        abstand_vertikal = abstand_vertikal + 1
    #Abfrage Niederlage durch Fressen von eigenen Körper
    #Sollte Schlange mehr als 4 Segemente haben (Kopf mitgezählt) und 3 mal hintereinander in die selbe Richtung abbiegen, dann frisst sie sich selbst --> Niederlage
    #Wenn man aber die Adressen von Kopf und den jeweilig aktiven Segmenten am Ende jedes Spielzugs mit einen COMPARE oder AND Befehl vergleichen will
    #erfordert das eine Menge Rechenzeit und extra Adressen im Speicher
    if (schlangen_kopf == schlangen_koerper1):
        zustand_spiel = 1
        break
    if (schlangen_kopf == schlangen_koerper2):
        zustand_spiel = 1
        break
    if (schlangen_kopf == schlangen_koerper3):
        zustand_spiel = 1
        break
	 
    if (schlangen_kopf == schlangen_koerper4):
        zustand_spiel = 1
        break
    if (schlangen_kopf == schlangen_koerper5):
        zustand_spiel = 1
        break
	 
    if (schlangen_kopf == schlangen_koerper6):
        zustand_spiel = 1
        break
	 
    if (schlangen_kopf == schlangen_koerper7):
        zustand_spiel = 1
        break
	 
	#Abfrage für Siegbedingung (Abschluss while Schleife) ob aktive Frucht eingesammelt wurde
	#aktive Frucht durch AnzahlFrucht bestimmt
	#nachdem eine Frucht eingesammelt wurde, AnzhalFrucht um eins erhöhen und Icon für nächste Frucht an jeweilger Position generieren
    if (schlangen_kopf == frucht1):
        anzahl_frucht = anzahl_frucht + 1
        Lade (FruchtIcon,PositionFrucht2)
	 
    if (schlangen_kopf == frucht2):
        anzahl_frucht = anzahl_frucht + 1
        Lade (FruchtIcon,PositionFrucht3)
	 
    if (schlangen_kopf == frucht3):
        anzahl_frucht = anzahl_frucht + 1
        Lade (FruchtIcon,PositionFrucht4)
	 
    if (schlangen_kopf == frucht4):
        anzahl_frucht = anzahl_frucht + 1
        Lade (FruchtIcon,PositionFrucht5)
	 
    if (schlangen_kopf == frucht5):
        anzahl_frucht = anzahl_frucht + 1
	 
 

#noch im Main Programmcode, aber im End Teil der While (loop) Schleife
#Abfrage nach Zustand des Spiels - Sieg oder Niederlage erziehlt?
if (zustand_spiel == 0):
    print('Sieg')
    #Sieg erziehlt, da alle Früchte eingesammelt und AnzhalKörperMax = 8 erreicht  #irgendwie den Spieler visuell symbolisieren
else:
    print('Niederlage')
    #Niederlage, da entweder Rand berührt oder Körpersegment gefressen  #irgendwie den Spieler visuell symbolisieren


