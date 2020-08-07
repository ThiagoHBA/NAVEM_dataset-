import os
import json
import time
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

pasta = "./caminhada_30/Exp1/"
arquivo = "sensores.json"
sense_txt = open(pasta + arquivo,"r")
sensor = json.load(sense_txt) 
def calculo_integral():
    delta_t = time[j] - time[j-1]
    velocidade_inst = Dados.integration_trapeze(acc[j-1],acc[j],delta_t)
    velocidades.append(velocidades[j-1] + velocidade_inst)

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
            roll.append(rpy["Roll"])
            pitch.append(rpy["Pitch"])
            yaw.append(rpy["Yaw"])

    def obter_aaWorld():
        for aaW in sensor["dados"]:
            aaWorldX.append(aaW["aaWorldX"])
            aaWorldY.append(aaW["aaWorldY"])
            aaWorldZ.append(aaW["aaWorldZ"])
        

    def obter_time():
        for t in sensor["dados"]:
            tempos.append(t["time_sec"])
    
            
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


    def integration_trapeze(a, b, delta_t):
        f_a = a
        f_b = b
        val_int = (f_a+f_b)*delta_t
        val_int = val_int/2

        return val_int

    def obter_velocidade(acc,time,velocidades):
        contador = 0
        desconto = 0
        
        contador_estado = 0
        contador_estado3 = 0.005
        
        limite_superior = 0.1
        limite_inferior = -0.5
        limite_estado = 30
        limite_estado3 = 23
        
    
        ''''''
        estado = 0
        
        velocidades.append(0)
        velocidade_inst = 0
            
        for j in range(1,len(time), 1):

            if(estado == 0):
                velocidades.append(0)
                if(acc[j] >= limite_superior or acc[j] <= limite_inferior):
                    estado = 1
                    
            elif(estado == 1):
       
                delta_t = time[j] - time[j-1]
                velocidade_inst = Dados.integration_trapeze(acc[j-1],acc[j],delta_t)
                velocidades.append(velocidades[j-1] + velocidade_inst)

                if(acc[j] <= limite_superior and acc[j] >= limite_inferior):
                    estado = 2
                    contador_estado = 0
                
            elif(estado == 2):
                
                delta_t = time[j] - time[j-1]
                velocidade_inst = Dados.integration_trapeze(acc[j-1],acc[j],delta_t)
                velocidades.append(velocidades[j-1] + velocidade_inst)

                contador_estado += 1

                if(acc[j] >= limite_superior or acc[j] <= limite_inferior):
                    estado = 1
                    contador_estado = 0
                    
                elif(contador_estado >= limite_estado):
                    estado = 3

            elif(estado == 3):
                
                if(contador_estado3 >= limite_estado3):
                    delta_t = time[j] - time[j-1]
                    velocidade_inst = Dados.integration_trapeze(acc[j-1],acc[j],delta_t)
                    velocidades.append(velocidades[j-1] + velocidade_inst)
                    
                    estado = 0
                    
                elif(acc[j] <= limite_superior and acc[j] >= limite_inferior):
                    delta_t = time[j] - time[j-1]
                    velocidade_inst = Dados.integration_trapeze(acc[j-1],acc[j],delta_t)
                    velocidades.append((velocidades[j-1] + velocidade_inst) - desconto)

                    desconto += 0.005
                    contador_estado3 += 1
                    
                elif(acc[j] >= limite_superior or acc[j] <= limite_inferior):
                    delta_t = time[j] - time[j-1]
                    velocidade_inst = Dados.integration_trapeze(acc[j-1],acc[j],delta_t)
                    velocidades.append(velocidades[j-1] + velocidade_inst)
                    
                    estado = 1
                    contador_estado = 0

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

##aaWorldX = np.array(aaWorldX).astype(float)
##aaWorldY = np.array(aaWorldY).astype(float)
##aaWorldZ = np.array(aaWorldZ).astype(float)

GyroX = np.array(GyroX).astype(float)
GyroY = np.array(GyroY).astype(float)
GyroZ  = np.array(GyroZ).astype(float)

roll = np.array(roll).astype(float)
pitch = np.array(pitch).astype(float)
yaw  = np.array(yaw).astype(float)

tempos = np.array(tempos).astype(float)

tempos = tempos[1:]
AccX = AccX[1:]
AccY = AccY[1:]
AccZ = AccZ[1:]
yaw = yaw[1:]


intervalo_ini = 0
intervalo_fim = 100
Dados.obter_velocidade(AccX,tempos,velocidades)

##plt.plot(AccX)
##print(velocidades)
##print(sum(velocidades))
print("Velocidade média: ",np.mean(velocidades))
##plt.plot(yaw)
##plt.plot(tempos,AccX, color = "black")
##plt.plot(velocidades)
##plt.plot(tempos,yaw, color = "red")
##plt.plot(velocidades)
##plt.plot(tempos,AccY, color = "red")
##print(np.mean(velocidades))
##plt.plot(tempos,velocidades)

fig, axs = plt.subplots(2)
axs[0].plot(tempos,AccX, marker = "o")
axs[0].set_title('AccX')
##axs[1].plot(tempos,yaw, marker = "o")
##axs[1].set_title('Yaw')
axs[1].plot(tempos,velocidades, marker = "o")
axs[1].set_title('Velocidade X')

plt.show()



        
        
        
        
        
    
