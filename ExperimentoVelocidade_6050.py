import os
import json
import math
import numpy as np
from numpy.linalg import inv
import math
from functools import reduce
from matplotlib import pyplot as plt
import scipy.integrate as integrate

AccX = []
AccY = []
AccZ = []
AccCount = []

GyroX = []
GyroY = []
GyroZ = []

tempos = []
roll = []
pitch = []
yaw = []

gravityForce = 9.80665
past_vel = []
media_acc = 0
quaternions_count = []
velocidades = []

pasta = "C:/Users/thiag/Desktop/Experimentos/Experimentos_acc_linear/Exp1/"
arquivo = "sensores.json"
sense_txt = open(pasta + arquivo,"r")
sensor = json.load(sense_txt) 

class Dados:
    def obter_acc():
        for Acc in sensor["dados"]:
            AccX.append(Acc["AccX"])
            AccY.append(Acc["AccY"])
            AccZ.append(Acc["AccZ"])
        for i in range(len(AccX)):
            AccCount.append(np.array([AccX[i],AccY[i],AccZ[i]]))
        
    def obter_gyr():
        for Gyr in sensor["dados"]:
            GyroX.append(Gyr["GyrX"])
            GyroY.append(Gyr["GyrY"])
            GyroZ.append(Gyr["GyrZ"])

    def obter_rpy():
        for rpy in sensor["dados"]:
            roll.append(rpy["Row"])
            pitch.append(rpy["Pitch"])
            yaw.append(rpy["Yaw"])
        

    def obter_time():
        for t in sensor["dados"]:
            tempos.append(t["time_sec"])
    
            
    def product(lista): 
        return reduce(lambda acumulado, atual: acumulado * atual, lista)

    def lagrange(x, fx):                                                              
        L = lambda num, xi: Dados.product((num - xj) / (xi - xj) for xj in x if xj != xi)
        return lambda num: sum([yi * L(num, xi) for xi, yi in zip(x, fx)])
        
    def integration_simpson(a, b, f, nb_ech):
        h = (b-a)/np.double(nb_ech)
        z = np.double(f(a)+f(b))

        for i in range(1,nb_ech,2) :
            z += 4 * f(a+(i*h))
        for i in range(2, nb_ech-1, 2):
            z += 2 * f(a+(i*h))

        val_int =  z*(h/3)
##        val_int *= delta_t

        return val_int


    def integration_trapeze(a, b, f, delta_t):
##        f_a = f(a)
##        f_b = f(b)
        f_a = a
        f_b = b
        val_int = (f_a+f_b)/2.
        val_int *= delta_t

        return val_int

    def obter_velocidade():
##        f = Dados.lagrange(tempos[8:16],AccX[8:16])
##        for i in range(7):
##            delta_t = tempos[(8+1)+i] - tempos[8+i]
##            velocidades.append(Dados.integration_trapeze(tempos[(8+1)+i], tempos[8+i], f, delta_t))
        for j in range(0,len(tempos[306:411]), 1):
            f = Dados.lagrange(tempos[j:j+2], AccX[j:j+2])
            delta_t = tempos[306+j+1] - tempos[306+j] #calculo o intervalo de tempo ( altura do trapézio ).
            velocidades.append(Dados.integration_trapeze(AccX[306+j],AccX[306+j+1], f, delta_t)) #calcula a área de um trapézio e joga no array.


'''
EXP5:

Pico 1: [7:12]
vale 1: [12:24]
Pico 2: [24:30]
vale 2: [30:38]
Pico 3: [38:46]
Vale 3: [46:56]
Pico 4: [56:62]
Vale 4: [62:72]
Pico 5: [72:81]
Vale 5: [81:89]
Pico 6: [89:98]
'''

Dados.obter_acc()
Dados.obter_gyr()
Dados.obter_rpy()
Dados.obter_time()

AccX = np.array(AccX).astype(float)
AccY = np.array(AccY).astype(float)
AccZ = np.array(AccZ).astype(float)
AccCount = np.array(AccCount).astype(float)

GyroX = np.array(AccX).astype(float)
GyroY = np.array(AccY).astype(float)
GyroZ  = np.array(AccZ).astype(float)

roll = np.array(roll).astype(float)
pitch = np.array(pitch).astype(float)
yaw  = np.array(yaw).astype(float)

tempos = np.array(tempos).astype(float)

Dados.obter_velocidade()
print(velocidades)
print(sum(velocidades))
##print("Velocidade média: ",sum(velocidades))

plt.plot(tempos,AccX, marker = "o")
##plt.plot(tempos,AccY, color = "red")
##fig, axs = plt.subplots(2)
##axs[0].plot(tempos,AccX, marker = "o")
##axs[1].plot(velocidades, marker = "o")
##plt.plot(tempos[55:65],AccX[55:65], color = "red")
##plt.plot(tempos[10:14], AccX[10:14], color = "black", marker = "o")
##plt.plot(tempos[28:32],AccX[28:32], color = "black", marker = "o")
##plt.plot(tempos[43:48],AccX[43:48], color = "black", marker = "o")
##plt.plot(tempos[60:65],AccX[60:65], color = "black", marker = "o")

plt.show()



        
        
        
        
        
    
