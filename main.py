import os
import AtmelCom
import time
import numpy as np
import utils


th = 900 # threshold de corriente de pulsacion, default 700
tm = 1 # tiempo entre cada ciclo
m = AtmelCom.Atmel()


freq = [262, 294, 330, 349, 392]
dbi = [20, 40, 60]

mc = 0
cb = 0
cf = -1
cdbi = 0

duracionplay = 3

psi = False
pno = False
repr = False

# freq, intensidad
results = []

print("Mantenga presionado dos unidades de tiempo el boton del asistente para cambiar de modo!")

print("Ciclo principal iniciado...")
while True:
    lc = m.analogRead([0, 1, 2])

    if np.max(lc) >= th:
        btn = np.argmax(lc)
        print(btn)

        if btn == 0:
            cb += 1
            print("."*cb)
        elif btn == 1:
            if repr:
                print(f"Si ha escuchado la frecuencia {freq[cf]} Hz, intensidad de {dbi[cdbi]} dB, duracion de {duracionplay}")
                repr = False
                utils.insert(freq[cf], duracionplay, dbi[cdbi], 1)
        elif btn == 2:
            if repr:
                print(f"No ha escuchado la frecuencia {freq[cf]} Hz, intensidad de {dbi[cdbi]} dB, duracion de {duracionplay}")
                repr = False
                utils.insert(freq[cf], duracionplay, dbi[cdbi], 0)
    else:
        if cb == 1:
            if mc == 0:
                cf += 1
                if cf >= len(freq): cf = 0
                print(f"La frecuencia elegida es: {freq[cf]}")
            elif mc == 1:
                cdbi += 1
                if cdbi >= len(dbi): cdbi = 0
                print(f"Decibeles elegidos: {dbi[cdbi]}")
        elif cb >= 2:
            if mc == 0:
                print("Modo de eleccion de decibeles activado!")
                mc = 1
            elif mc == 1:
                print("Reproduccion iniciada!")
                play_frequency(freq[cf], duracionplay, dbi[cdbi])
                repr = True
                mc = 0
        cb = 0

    time.sleep(tm)

