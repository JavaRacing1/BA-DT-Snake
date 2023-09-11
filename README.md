# Snake
Dieses Projekt ist eine Implementierung von Snake in der Oktopus-Maschine.

## Funktion der Dateien
- oktopus_machinep3.py -> Die Oktopus-Maschine
- requirements.txt -> Beinhaltet alle benötigten Python-Pakete
- out.mic -> Enthält alle Mikroprogramme
- snake_memory.txt -> Programmcode von Snake im Format der Oktopus-Maschine
- snake.txt -> Programmcode von Snake mit Kommentaren und uncodierten Befehlen
- stackmaschine.py -> Die eigensprogrammierte Stackmaschine zum Testen von Mikroprogrammcode außerhalb der Oktopus-Maschine
- snake_code.py -> Vereinfachte Implementation von Snake für die Stackmaschine
- stachmaschine.txt -> Speicher, der beim Start der Stackmaschine geladen wird

## Anforderungen
- Python 3.11

## Installation
1. Ein venv von Python mit ```python -m venv venv``` erstellen
2. Das venv aktivieren ```.\venv\Scripts\activate```
3. Alle benötigten Pakete mit ```pip install -r ".\requirements.txt"``` installieren

## Start
1. Das venv aktivieren ```.\venv\Scripts\activate```
2. Die Oktopus-Maschine starten mit ```python .\oktopus_machinep3.py"```
3. Die Mikroprogramme über "Load Microprogramm" aus der **out.mic**-Datei laden
4. Eine Konsole über "Console" öffnen
5. Den Speicher über "Load Memory" mit der **snake_memory.txt** befüllen
6. Einen Takt von min. 25 auswählen, empfohlen wird ein Takt von 1000
7. Den Start-Knopf betätigen. Danach kann die Schlange mit WASD gesteuert werden (dauert etwas)