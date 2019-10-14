# -*- coding: utf-8 -*-

### Darstellung des Merkurorbits mit VPython


# ----------------------------------
## Laden des Grafikmoduls
# ----------------------------------

# Da es unglaublich viel Zeit kostet ein Programm für 3-dimensionale grafische
# Darstellung selber zu schreiben, lassen wir uns die Arbeit von "Vpython"
# abnehmen. Doch dazu müssen wir zunächst dieses Modul bereitstellen. Das
# erreicht man mit Hilfe des Befehls "import" oder "from .. import".

from vpython import *

# Schreibt man
#   "from visual import *"
# bedeutet dies: "Lade alles aus Vpython"

# Eine Dokumentation von Modulen lässt sich durch den Befehl
# "help(modul_name)" aufrufen.
#
# Tipp: Will man eine Eingabe unterdrücken, so lässt sich dies auch mit "#" tun.
# Der darauf folgende Text wird dabei von Python überlesen.

# help(visual)


# ----------------------------------
## Aufgabe 1: Merkurorbit)
# ----------------------------------

# Funktionen werden in Python wie folgt definiert:
# def func(x):
#     .... Rechnung und Anderes ....
#
# Diese wollen wir nun nutzen. Um die Umlaufbahn des Merkurs darzustellen, ist
# es sinvoll die Aufgabe in zwei Abschnitte zu Teilen:
# (a) Berchnung des Orbits
# (b) Zeichnung des Orbits
# Für beide Abschnitte werden wir Funktionen nutzen.


# ----------------------------------
## Parameter
# ----------------------------------

# Für Merkur Parameter siehe
#     http://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html
# Für Sonnen Parameter siehe
#     http://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html

# Alle Größen sind in einem angepassten Einheitensystem gegeben:
#  - Längen in Einheiten von R0 = 1e10 m
#  - Zeiten in Einheiten von T0 = 1 d = 60*60*24 s
#  - Massen in Einheiten von M0 = m_sonne = 1.989e30 kg

# Massen von Sonne und Merkur
m_sonne = 1
m_merkur = 1.66e-7

# Anfangsposition und -geschwindigkeit des Merkur (im Perihel)
r_merkur_0 = vector(0, 4.6, 0)
v_merkur_0 = vector(0.51, 0, 0)
# Anfangsposition und -geschwindigkeit der Sonne
r_sonne_0 = vector(0, 0, 0)
v_sonne_0 = -v_merkur_0 * m_merkur / m_sonne # Impulserhaltung

# Gravitationskonstante berechnet als G' * M0 * T0**2 / R0**3
# mit G' = 6.6738e-11 m**3 / kg / s**2
G = 0.99

# Scharzschildradius der Sonne
rS = 2.95e-7
# Spezifischer Drehimpuls
rL2 = 8.19e-7

# Dauer der Simulation in Erdentagen
T = 88 * 5
# Zeitschritt der Simulation in Erdentagen
dt = 2 * v_merkur_0.mag / G / 100


# ----------------------------------
## (a) Berechnung des Orbits
# ----------------------------------

# Die Berechnung des Orbits läuft wie folgt ab.
# Man übergibt der Funktion "merkur_zeit_schritt"  die aktuelle Position und
# Geschwindigkeit des Merkurs und der Sonne. Das Ergebnis der Rechnung soll die
# jeweils neue Position und Geschwindigkeit nach einem Zeitintervall "dt" sein.

def merkur_zeit_schritt(r_merkur_alt, v_merkur_alt, r_sonne_alt, v_sonne_alt,
                        alpha, beta):
    # Berechne den Vektor der von der Sonne zum Merkur zeigt
    r_sm = r_merkur_alt - r_sonne_alt

    # Berechne die Kraft der Sonne auf den Merkur mit Newtonscher Gravitation
    F_m = -G * m_sonne * m_merkur / r_sm.mag**2 * (r_sm / r_sm.mag)
    # Multipliziere mit Korrekturfaktor
    F_m = F_m * (1 + alpha * rS / r_sm.mag + beta * rL2 / r_sm.mag**2)
    # Kraft des Merkurs auf die Sonne
    F_s = -F_m

    # Berechne die daraus resultierenden Geschwindigkeiten
    v_sonne_neu = v_sonne_alt + F_s / m_sonne * dt
    v_merkur_neu = v_merkur_alt + F_m / m_merkur * dt
    # Und letztendlich die neuen Positionen
    r_sonne_neu = r_sonne_alt + v_sonne_neu * dt
    r_merkur_neu = r_merkur_alt + v_merkur_neu * dt

    # Rückgabe der eben ermittelten Vektoren
    return r_merkur_neu, v_merkur_neu, r_sonne_neu, v_sonne_neu


# ----------------------------------
## (b) Zeichnung des Orbits
# ----------------------------------

def zeichne_orbit(alpha, beta):
    # Erstelle Kugeln für Merkur und Sonne
    merkur = sphere(pos=r_merkur_0, radius=0.2, color=color.red)
    sonne = sphere(pos=r_sonne_0, radius=0.8, color=color.yellow)
    # Weise den Planeten ihre Anfangsgeschwindigkeiten zu
    merkur.velocity = v_merkur_0
    sonne.velocity = v_sonne_0

    # Erstelle die Bahnkurve für Merkur
    merkur.bahn = curve(color=color.white)

    # Starte die Animation
    t = 0
    while t < T:
        # Bildaktualisierungsrate
        rate(100)

        # Füge akltuelle Position zur Bahnkurve hinzu
        merkur.bahn.append(pos=merkur.pos)
        # Berechne die neuen Positionen
        merkur.pos, merkur.velocity, sonne.pos, sonne.velocity = merkur_zeit_schritt(
            merkur.pos, merkur.velocity, sonne.pos, sonne.velocity,
            alpha, beta
        )

        # Ändere die Zeit.
        t += dt

    return


# ----------------------------------
## Ausführen der Funktionen
# ----------------------------------

zeichne_orbit(5e6, 0)
