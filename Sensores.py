import os
import json
import math
import numpy as np
from numpy.linalg import inv
import math
from functools import reduce
from matplotlib import pyplot as plt
import scipy.integrate as integrate
import statistics


class Dados:
    AccX_MPU = []
    AccY_MPU = []
    AccZ_MPU = []

    AccCount = []

    GyroX_MPU = []
    GyroY_MPU = []
    GyroZ_MPU = []

    aaWorldX = []
    aaWorldY = []
    aaWorldZ = []

    tempos = []
    diffTempos = []

    roll_MPU = []
    pitch_MPU = []
    yaw_MPU = []

    gravityForce = 9.80665
    
    past_vel = []
    media_acc = 0
    quaternions_count = []
    velocidades = []

    def obter_acc(sensor):
        for Acc in sensor["dados"]:
            Dados.AccX_MPU.append(Acc["AccX"])
            Dados.AccY_MPU.append(Acc["AccY"])
            Dados.AccZ_MPU.append(Acc["AccZ"])
            
        for i in range(len(Dados.AccX_MPU)):  
            Dados.AccCount.append(np.array([Dados.AccX_MPU[i],Dados.AccY_MPU[i],Dados.AccZ_MPU[i]]))
            
        
    def obter_gyr(sensor):
        for Gyr in sensor["dados"]:
            Dados.GyroX.append(Gyr["GyrX"])
            Dados.GyroY.append(Gyr["GyrY"])
            Dados.GyroZ.append(Gyr["GyrZ"])
    
    def obter_rpy(sensor):
        for rpy in sensor["dados"]:
            Dados.roll_MPU.append(rpy["Roll"])
            Dados.pitch_MPU.append(rpy["Pitch"])
            Dados.yaw_MPU.append(rpy["Yaw"])

    def obter_aaWorld(sensor):
        for aaW in sensor["dados"]:
            Dados.aaWorldX.append(aaW["aaWorldX"])
            Dados.aaWorldY.append(aaW["aaWorldY"])
            Dados.aaWorldZ.append(aaW["aaWorldZ"])
        

    def obter_time(sensor):
        for t in sensor["dados"]:
            Dados.tempos.append(t["time_sec"])
    
            
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
        val_int = (f_a+f_b)/2.
        val_int *= delta_t

        return val_int

    def obter_velocidade():
        velocidades.append(0)
        velocidade_inst = 0
        delta_t = tempos[1] - tempos[0]        
        velocidades.append(velocidade_inst + (AccX[0] * delta_t))
        velocidade_inst = Dados.integration_trapeze(AccX[1],AccX[0], delta_t)
        
        for j in range(1,len(tempos)-1, 1):
            delta_t = tempos[j] - tempos[j-1]        
            velocidades.append(velocidade_inst + (AccX[j] * delta_t))
            velocidade_inst = Dados.integration_trapeze(AccX[j],AccX[j-1], delta_t)

    def obter_velocidade_geral(acc, t, ini, fim):
        vel = []
        vel.append(0)
        contador = 0

        for j in range(ini,len(t) - 1, 1):
            delta_t = t[j+1] - t[j]
            velocidade_inst = Dados.integration_trapeze(acc[j],acc[j+1], delta_t)
            vel.append(vel[j] + velocidade_inst)
            contador += 1
        return vel
    
