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

aaWorldX = []
aaWorldY = []
aaWorldZ = []


tempos = []
roll = []
pitch = []
yaw = []

gravityForce = 9.80665
sensibilidade = 8192

pi = 3.141592653589793238462643

past_vel = []
media_acc = 0
quaternions_count = []
velocidades = []

pasta = "C:/Users/thiag/Desktop/NAVEM/Arduino+Raspberry/"
arquivo = "Experimento_4.json"
sense_txt = open(pasta + arquivo,"r")
sensor = json.load(sense_txt) 

class Dados:
    def obter_acc():
        for Acc in sensor:
            AccX.append(Acc["AccX"])
            AccY.append(Acc["AccY"])
            AccZ.append(Acc["AccZ"])
        for i in range(len(AccX)):
            AccCount.append(np.array([AccX[i],AccY[i],AccZ[i]]))
        
    def obter_gyr():
        for Gyr in sensor:
            GyroX.append(Gyr["GyrX"])
            GyroY.append(Gyr["GyrY"])
            GyroZ.append(Gyr["GyrZ"])

    def obter_rpy():
        for rpy in sensor:
            roll.append(rpy["Roll"])
            pitch.append(rpy["Pitch"])
            yaw.append(rpy["Yaw"])

    def obter_aaWorld():
        for aaW in sensor["dados"]:
            aaWorldX.append(aaW["aaWorldX"])
            aaWorldY.append(aaW["aaWorldY"])
            aaWorldZ.append(aaW["aaWorldZ"])
        

    def obter_time():
        for t in sensor:
            tempos.append(t["tempos"])
    
            
    def product(lista): 
        return reduce(lambda acumulado, atual: acumulado * atual, lista)

    def lagrange(x, fx):                                                              
        L = lambda num, xi: Dados.product((num - xj) / (xi - xj) for xj in x if xj != xi)
        return lambda num: sum([yi * L(num, xi) for xi, yi in zip(x, fx)])
        
    def integration_simpson(a, b, f, delta_t, nb_ech):
        h = (b-a)/np.double(nb_ech)
        z = np.double(f(a)+f(b))

        for i in range(1,nb_ech,2) :
            z += 4 * f(a+(i*h))
        for i in range(2, nb_ech-1, 2):
            z += 2 * f(a+(i*h))

        val_int =  z*(h/3)
        val_int *= delta_t

        return val_int


    def integration_trapeze(a, b, f, delta_t):
        f_a = a
        f_b = b
        val_int = (f_a+f_b)/2.
        val_int *= delta_t

        return val_int

    def obter_velocidade():
##        velocidades.append(0)
##        velocidade_inst = 0
##        for j in range(0,len(tempos)-1, 1):
##            f = Dados.lagrange(tempos[j:j+2], AccX[j:j+2])
##            delta_t = tempos[j+1] - tempos[j]
##            velocidade_inst = Dados.integration_trapeze(AccX[j+1],AccX[j], f, delta_t)
##            velocidades.append(velocidade_inst + (AccX[j] * delta_t))
##
        '''outro teste'''
        
        velocidades.append(0)
        velocidade_inst = 0
        contador = 0
        delta_t = tempos[1] - tempos[0]
        f = Dados.lagrange(tempos[4:5], AccX[3:4])
        velocidade_inst = Dados.integration_trapeze(AccX[0],AccX[1],f,delta_t)
        velocidades.append(velocidade_inst)
        for j in range(1,len(tempos)-2, 1):
            f = Dados.lagrange(tempos[j:j+2], AccX[j:j+2])
            delta_t = tempos[j+2] - tempos[j+1]
            velocidade_inst = Dados.integration_trapeze(AccX[j],AccX[j+1],f,delta_t)
            velocidades.append(velocidades[j-1] + velocidade_inst)


#----------------------------------------------------------------------------------------------------------------

    
Dados.obter_acc()
##Dados.obter_gyr()
Dados.obter_rpy()
##Dados.obter_aaWorld()
Dados.obter_time()

AccX = np.array(AccX).astype(float)
AccY = np.array(AccY).astype(float)
AccZ = np.array(AccZ).astype(float)
AccCount = np.array(AccCount).astype(float)

GyroX = np.array(GyroX).astype(float)
GyroY = np.array(GyroY).astype(float)
GyroZ  = np.array(GyroZ).astype(float)

roll = np.array(roll).astype(float)
pitch = np.array(pitch).astype(float)
yaw  = np.array(yaw).astype(float)

roll = roll*(180/pi)
pitch = pitch*(180/pi)
yaw = yaw*(180/pi)

AccX = (AccX/sensibilidade)*gravityForce
AccY = (AccY/sensibilidade)*gravityForce
AccZ = (AccZ/sensibilidade)*gravityForce

tempos = np.array(tempos).astype(float)

tempos = tempos/1000

tempos = tempos - tempos[0]
##AccZ = AccZ * -1


##aaWorldX = np.array(aaWorldX).astype(float)
##aaWorldY = np.array(aaWorldY).astype(float)
##aaWorldZ = np.array(aaWorldZ).astype(float)

##AccX = AccX + 1.26263646392785567


Dados.obter_velocidade()
##print(velocidades)
##print(sum(velocidades))
##print("Velocidade média: ",np.mean(velocidades))
##plt.plot(yaw)
##plt.plot(tempos,AccX, color = "black")
##plt.plot(velocidades)
##plt.plot(tempos,yaw, color = "red")
##plt.plot(velocidades)
##plt.plot(tempos,AccY, color = "red")
fig, axs = plt.subplots(2)
axs[0].plot(tempos,AccZ, marker = "o")
axs[1].plot(velocidades, marker = "o")
##plt.plot(tempos[55:65],AccX[55:65], color = "red")
##plt.plot(tempos[10:14], AccX[10:14], color = "black", marker = "o")
##plt.plot(tempos[28:32],AccX[28:32], color = "black", marker = "o")
##plt.plot(tempos[43:48],AccX[43:48], color = "black", marker = "o")
##plt.plot(tempos[60:65],AccX[60:65], color = "black", marker = "o")

plt.show()



        
        
        
        
        
    
