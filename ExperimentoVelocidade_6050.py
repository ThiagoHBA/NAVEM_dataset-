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

gravityForce = 9.80665

quaternions_count = []
velocidades = []

pasta = "C:/Users/thiag/Desktop/Velocidade exps/MPU6050/Experimentos_delay_baixo/Experimentos_aaWorld/"
arquivo = "Experimento 5.txt"
sense_txt = open(pasta + arquivo,"r")
sensor = json.load(sense_txt) 

class Dados:
    def obter_acc():
        for Acc in sensor["Dados"]:
            AccX.append(abs(Acc["AccX"]))
##            AccY.append(Acc["AccY"])
##            AccZ.append(Acc["AccZ"])
##        for i in range(len(AccX)):
##            AccCount.append(np.array([AccX[i],AccY[i],AccZ[i]]))
        
    def obter_gyr():
        for Gyr in sensor["Dados"]:
            GyroX.append(Gyr["GyrX"])
            GyroY.append(Gyr["GyrY"])
            GyroZ.append(Gyr["GyrZ"])
        

    def obter_time():
        for t in sensor["Dados"]:
            tempos.append(t["time_usec"])
    
            
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


    def obter_velocidade():
        for i in range(0,len(tempos),5):
            f = Dados.lagrange(tempos[i : i+5], AccX[i : i+5])
            for j in range(4, 0, -1):
                velocidades.append(Dados.integration_simpson(tempos[i], tempos[i+j], f, 100))
            
##        velocidades.append(Dados.integration_simpson(tempos[0], tempos[5], f, 100))
##        velocidades.append(Dados.integration_simpson(tempos[0], tempos[4], f, 100))
##        velocidades.append(Dados.integration_simpson(tempos[0], tempos[3], f, 100))
##        velocidades.append(Dados.integration_simpson(tempos[0], tempos[2], f, 100))
##        velocidades.append(Dados.integration_simpson(tempos[0], tempos[1], f, 100))
##        f1 = Dados.lagrange(tempos[60 : 66], AccX[60 : 66])
##        velocidades.append(Dados.integration_simpson(tempos[60], tempos[65], f1, 100))
##        velocidades.append(Dados.integration_simpson(tempos[60], tempos[64], f1, 100))
##        velocidades.append(Dados.integration_simpson(tempos[60], tempos[63], f1, 100))
##        velocidades.append(Dados.integration_simpson(tempos[60], tempos[62], f1, 100))
##        velocidades.append(Dados.integration_simpson(tempos[60], tempos[61], f1, 100))
##        f2 = Dados.lagrange(tempos[120 : 125], AccX[120 : 125])
##        velocidades.append(Dados.integration_simpson(tempos[120], tempos[124], f2, 100))
##        velocidades.append(Dados.integration_simpson(tempos[120], tempos[123], f2, 100))
##        velocidades.append(Dados.integration_simpson(tempos[120], tempos[122], f2, 100))
##        velocidades.append(Dados.integration_simpson(tempos[120], tempos[121], f2, 100))
            
##   [0.009276723563242089, 0.0069568121411608405, 0.0064906208558603, 0.004998603914599093]
Dados.obter_acc()
##Dados.obter_gyr()
Dados.obter_time()

AccX = np.array(AccX).astype(float)
##AccY = np.array(AccY).astype(float)
##AccZ = np.array(AccZ).astype(float)
##AccCount = np.array(AccCount).astype(float)

##GyroX = np.array(AccX).astype(float)
##GyroY = np.array(AccY).astype(float)
##GyroZ  = np.array(AccZ).astype(float)

tempos = np.array(tempos).astype(float)

Dados.obter_velocidade()

##print("Velocidade media: ", np.mean(velocidades))
print("Velocidade média: ",np.mean(velocidades))

plt.plot(tempos[1:125],AccX[1:125])
plt.show()



        
        
        
        
        
    
