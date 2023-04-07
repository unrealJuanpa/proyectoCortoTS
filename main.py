import os
import AtmelCom
import time


m = AtmelCom.Atmel()

while True:
    print(m.analogRead([0]))
    time.sleep(1)

