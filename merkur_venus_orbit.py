# -*- coding: utf-8 -*-

### Darstellung der Merkur- und Venusorbits mit VPython


from vpython import *


# ----------------------------------
## Parameter
# ----------------------------------

# Für Merkur Parameter siehe
#     http://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html
# Für Venus Parameter siehe
#     http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
# Für Sonnen Parameter siehe
#     http://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html

# Alle Größen sind in einem angepassten Einheitensystem gegeben:
#  - Längen in Einheiten von R0 = 1e10 m
#  - Zeiten in Einheiten von T0 = 1 d = 60*60*24 s
#  - Massen in Einheiten von M0 = m_sonne = 1.989e30 kg

# Massen von Sonne und Merkur
m_sonne = 1
m_merkur = 1.66e-7
m_venus = 2.448e-6

# Anfangsposition und -geschwindigkeit des Merkur (im Perihel)
r_merkur_0 = vector(0, 4.6, 0)
v_merkur_0 = vector(0.51, 0, 0)
# Anfangsposition und -geschwindigkeit des Merkur (im Perihel)
r_venus_0 = vector(0, 10.7, 0)
v_venus_0 = vector(0.30, 0, 0)
# Anfangsposition und -geschwindigkeit der Sonne
r_sonne_0 = vector(0, 0, 0)
v_sonne_0 = -v_merkur_0*m_merkur/m_sonne - v_venus_0*m_venus/m_sonne  # Impulserhaltung


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

def zeit_schritt(r_merkur_alt, v_merkur_alt,
                 r_venus_alt, v_venus_alt,
                 r_sonne_alt, v_sonne_alt,
                 alpha, beta):
    # Berechne die Abstandsvektoren
    r_sm = r_merkur_alt - r_sonne_alt
    r_sv = r_venus_alt - r_sonne_alt
    r_vm = r_merkur_alt - r_venus_alt

    # Kraft auf Merkur
    c_sm = 1 + alpha * rS / r_sm.mag + beta * rL2 / r_sm.mag**2
    F_m = -G * m_sonne * m_merkur * c_sm / r_sm.mag**2 * (r_sm / r_sm.mag) \
        - G * m_venus * m_merkur / r_vm.mag**2 * (r_vm / r_vm.mag)
    # Kraft auf Venus
    c_sv = 1 + alpha * rS / r_sv.mag + beta * rL2 / r_sv.mag**2
    F_v = -G * m_sonne * m_venus * c_sv / r_sv.mag**2 * (r_sv / r_sv.mag) \
        + G * m_merkur * m_venus / r_vm.mag**2 * (r_vm / r_vm.mag)
    # Kraft auf Sonne
    F_s = G * m_merkur * m_sonne / r_sm.mag**2 * (r_sm / r_sm.mag) \
        + G * m_venus * m_sonne / r_sv.mag**2 * (r_sv / r_sv.mag)

    # Berechne die daraus resultierenden Geschwindigkeiten
    v_sonne_neu = v_sonne_alt + F_s / m_sonne * dt
    v_merkur_neu = v_merkur_alt + F_m / m_merkur * dt
    v_venus_neu = v_venus_alt + F_v / m_venus * dt
    # Und die neuen Positionen
    r_sonne_neu = r_sonne_alt + v_sonne_neu * dt
    r_merkur_neu = r_merkur_alt + v_merkur_neu * dt
    r_venus_neu = r_venus_alt + v_venus_neu * dt

    # Rückgabe der eben ermittelten Vektoren
    return r_merkur_neu, v_merkur_neu, \
        r_venus_neu, v_venus_neu, \
        r_sonne_neu, v_sonne_neu


# ----------------------------------
## (b) Zeichnung des Orbits
# ----------------------------------

def zeichne_orbit(alpha, beta):
    # Erstelle Kugeln für Merkur, Venus und Sonne
    merkur = sphere(pos=r_merkur_0, radius=0.2, color=color.red)
    venus = sphere(pos=r_venus_0, radius=0.25, color=color.orange)
    sonne = sphere(pos=r_sonne_0, radius=0.8, color=color.yellow)
    # Weise den Planeten ihre Anfangsgeschwindigkeiten zu
    merkur.velocity = v_merkur_0
    venus.velocity = v_venus_0
    sonne.velocity = v_sonne_0

    # Erstelle die Bahnkurven für Merkur und Venus
    merkur.bahn = curve(color=color.white)
    venus.bahn = curve(color=color.white)

    # Starte die Animation
    t = 0
    while t < T:
        # Bildaktualisierungsrate
        rate(500)

        # Füge akltuelle Position zur Bahnkurve hinzu
        merkur.bahn.append(pos=merkur.pos)
        venus.bahn.append(pos=venus.pos)
        # Berechne die neuen Positionen
        merkur.pos, merkur.velocity, \
            venus.pos, venus.velocity, \
            sonne.pos, sonne.velocity = zeit_schritt(
                merkur.pos, merkur.velocity,
                venus.pos, venus.velocity,
                sonne.pos, sonne.velocity,
                alpha, beta
            )

        # Ändere die Zeit.
        t += dt

    return


# ----------------------------------
## Ausführen der Funktionen
# ----------------------------------

zeichne_orbit(0, 0)
