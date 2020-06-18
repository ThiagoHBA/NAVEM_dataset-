import os
import json
import math
import numpy as np
import math
from matplotlib import pyplot as plt

sense_txt = open("C:/Users/thiag/Desktop/NAVEM/VisualStudio/imagens/teste/Contador de Dados.json","r")

sensor = json.load(sense_txt)

GyroY = []
Indice = []

for Gy in sensor["Dados"]:
    GyroY.append(Gy["GyrY"])
for i in sensor["Dados"]:
    Indice.append(i["i"])

GyroY_float = np.array(GyroY).astype(float)

frame_inicial = 0
frame_final = 100
plt.plot(GyroY_float[frame_inicial*8 :frame_final*8])
plt.show()

