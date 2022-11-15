
from text_game.game_data import *
import random

# Spielfeld erzeugen (Länge, Breite, Schatz-Position X, Schatz-Position Y)
feld = Feld(10, 10, 9, 8)

# Player erzeugen (Position X, Position Y, hp, Waffe, Waffenstärke)
spieler = Spieler(1, 1, 100, "Knüppel", 10)

# Legende ausgeben
def info():
    print(
        '***** Fortbewegung *****\n'
        '"w" : geradeaus gehen\n'
        '"a" : nach links gehen\n'
        '"s" : zurückgehen\n'
        '"d" : nach rechts gehen\n'        
        '"f" : kämpfen\n'
        '"z" : Spiel beenden'
    )

# Game Loop
def spiel():
    while True:
        print('Was wirst du tun? ("i" für Info eingeben)')
        eingabe = input()

        # Player über das Spielfeld bewegen, solange Spielfeld-Ende nicht erreicht
        if eingabe == "w" or eingabe == "s" or eingabe == "d" or eingabe == "a":
            bewegen(eingabe)
        elif eingabe == "i":
            info()
        # Spiel beenden, wenn abgebrochen werden soll
        elif eingabe == "z":
            print("Spiel beendet")
            exit()
        else:
            print("Ungültige Eingabe")

def bewegen(eingabe):

    # Player über das Spielfeld bewegen, solange Spielfeld-Ende nicht erreicht
    if eingabe == "w" and spieler.y_pos < feld.hoehe:
        spieler.y_pos += 1
    elif eingabe == "s" and spieler.y_pos > 1:
        spieler.y_pos -= 1
    elif eingabe == "d" and spieler.x_pos < feld.breite:
        spieler.x_pos += 1
    elif eingabe == "a" and spieler.x_pos > 1:
        spieler.x_pos -= 1
    else:
        print("Du kommst hier nicht weiter.")
        spiel()

    print(f"Deine aktuelle Position:    X:{spieler.x_pos} | Y:{spieler.y_pos}")

    if spieler.x_pos == feld.schatz_position_x and spieler.y_pos == feld.schatz_position_y:
        print("Du hast den Schatz gefunden!")
        exit()
    else:
        ereignis()

def ereignis():

    # Unterfunktion fight() (Funktion in der Funktion ereignis())
    def kaempfen():

        ereignis_wahrscheinlichkeit = random.randint(1, 3)

        # Gegner ist ein Goblin (Wahrscheinlichkeit 2/3)
        if ereignis_wahrscheinlichkeit == 1 or ereignis_wahrscheinlichkeit == 2:
            gegner = Goblin()

        # Gegner ist ein Zwerg (Wahrscheinlichkeit 1/3)
        else:
            gegner = Zwerg()

        def spieler_lebt():
            # Spiel beenden, wenn Player gestorben
            if spieler.hp < 1:
                print("Du hast den Kampf nicht überlebt!")
                exit()
            else:
                return True

        print(f"Mist! Ein {gegner.name} stellt sich mir in den Weg!")
        while True:
            print("Kämpfst du oder läufst du weg? (Wahrscheinlichkeit, fliehen zu können: 1/3)")
            print(f'Drücke "f" für kämpfen, etwas anderes für flüchten. Deine aktuelle Gesundheit: {spieler.hp}')
            if input() == "f":
                gegner.hp -= spieler.staerke

                if gegner.hp < 1:
                    print(f"Du hast den {gegner.name} getötet!")
                    del gegner
                    break
                else:
                    print("Dein Gegner ist noch nicht tot.")
                    spieler.hp -= gegner.staerke
                    if spieler_lebt():
                        continue
            else:
                ereignis_wahrscheinlichkeit = random.randint(1, 3)
                if ereignis_wahrscheinlichkeit == 1:
                    print("Deine Flucht war erfolgreich!")
                    break
                else:
                    print("Du wirst angegriffen!")
                    spieler.hp -= gegner.staerke
                    if spieler_lebt():
                        continue
        spiel()


    # Unterfunktion weapon() (Funktion in der Funktion ereignis())
    def waffe_gefunden():
        print("Du hast eine neue Waffe gefunden.")
        waffen_index = random.randint(0, len(waffen) - 1)
        gefundene_waffe = list(waffen.keys())[waffen_index]
        print(f"Die neue Waffe: {gefundene_waffe}")
        if spieler.staerke >= list(waffen.values())[waffen_index]:
            print("So ein Mist! Die Waffe ist schwächer als meine bisherige.")
        else:
            print("Die Waffe wird mir gute Dienste leisten...")
            spieler.waffe = gefundene_waffe
            spieler.staerke = list(waffen.values())[waffen_index]

    # zufällige Ereignisse steuern
    ereignis_wahrscheinlichkeit = random.randint(1, 10)

    # 1. Gegner taucht auf (Wahrscheinlichkeit 1/5)
    if ereignis_wahrscheinlichkeit == 1 or ereignis_wahrscheinlichkeit == 2:
        kaempfen()

    # 2. Waffe wird gefunden (Wahrscheinlichkeit 1/10)
    elif ereignis_wahrscheinlichkeit == 3:
        waffe_gefunden()
