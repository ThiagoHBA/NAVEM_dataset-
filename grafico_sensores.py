import os
import json
import math
import numpy as np
from numpy.linalg import inv
import math
from matplotlib import pyplot as plt

pasta = "C:/Users/thiag/Desktop/NAVEM/VisualStudio/imagens/9250_quaternions/"
arquivo = "CleanSense.json"
sense_json = open(pasta + arquivo,"r")

sensor = json.load(sense_json)

AccX = []
AccY = []
AccZ = []

GyroX = []
GyroY = []
GyroZ = []


for Acc in sensor:
    AccX.append(Acc["AccX"])
    AccY.append(Acc["AccY"])
    AccZ.append(Acc["AccZ"])

for Gyr in sensor:
    GyroX.append(Gyr["GyrX"])
    GyroY.append(Gyr["GyrY"])
    GyroZ.append(Gyr["GyrZ"])   
        
frame_inicial = 0
frame_final = 100
plt.plot(AccX[frame_inicial*8 :frame_final*8], color = "blue", label = "AccX")
plt.plot(AccY[frame_inicial*8 :frame_final*8], color = "black", label = "AccY")
plt.plot(AccZ[frame_inicial*8 :frame_final*8], color = "red", label = "AccZ")
plt.legend()
plt.show()
