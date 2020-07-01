import os
import json
import math
import numpy as np
from numpy.linalg import inv
import math
from functools import reduce
from matplotlib import pyplot as plt

AccX = []
AccY = []
AccZ = []
AccCount = []


GyroX = []
GyroY = []
GyroZ = []

MagX = []
MagY = []
MagZ = []

Indice = []

deltat = []

tempos = []

qx = []
qy = []
qz = []
qw = []

cleanAcc = []
cleanAccX = []
cleanAccY = []
cleanAccZ = []

quaternions_count = []
velocidades = []

pasta = "C:/Users/thiag/Desktop/NAVEM/VisualStudio/imagens/9250_quaternions/"
arquivo = "Contador de Dados.json"
sense_txt = open(pasta + arquivo,"r")
sensor = json.load(sense_txt) 

class Dados:
    def obter_acc():
        for Acc in sensor["Dados"]:
            AccX.append(Acc["AccX"])
            AccY.append(Acc["AccY"])
            AccZ.append(Acc["AccZ"])
        for i in range(len(AccX)):
            AccCount.append(np.array([AccX[i],AccY[i],AccZ[i]]))
        
    def obter_gyr():
        for Gyr in sensor["Dados"]:
            GyroX.append(Gyr["GyrX"])
            GyroY.append(Gyr["GyrY"])
            GyroZ.append(Gyr["GyrZ"])

    def obter_mag():
        for mg in sensor["Dados"]:
            MagX.append(mg["MagX"])
            MagY.append(mg["MagY"])
            MagZ.append(mg["MagZ"])

            
    def obter_indice():
        for i in sensor["Dados"]:
            Indice.append(i["i"])
        

    def obter_deltat():
        for dt in sensor["Dados"]:
            deltat.append(dt["deltat"])
        

    def obter_time():
        for t in sensor["Dados"]:
            tempos.append(t["time_usec"])
        
        
    def quaternions(ax,ay,az,gx,gy,gz,mx,my,mz,deltat):
        q1,q2,q3,q4 = 1,0,0,0
        norm = 0
        hx,hy,_2bx,_2bz = 0,0,0,0
        s1,s2,s3,s4 = 0,0,0,0
        qDot1,qDot2,qDot3,qDot4 = 0,0,0,0

        GyroMeasError = math.pi * (40.0 / 180.0);
        beta = ((3.0 / 4.0)**0.5) * GyroMeasError;
                
        _2q1mx = 0
        _2q1my = 0
        _2q1mz = 0
        _2q2mx = 0
        _4bx = 0
        _4bz = 0
        _2q1 = 2.0 * q1
        _2q2 = 2.0 * q2
        _2q3 = 2.0 * q3
        _2q4 = 2.0 * q4
        _2q1q3 = 2.0 * q1 * q3
        _2q3q4 = 2.0 * q3 * q4
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q1q4 = q1 * q4
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q2q4 = q2 * q4
        q3q3 = q3 * q3
        q3q4 = q3 * q4
        q4q4 = q4 * q4
    
        norm = math.sqrt(ax * ax + ay * ay + az * az)
        
        if norm == 0.0:
            return
        norm = 1.0/norm
        ax = ax * norm
        ay = ay * norm
        az = az * norm

        norm = math.sqrt(mx * mx + my * my + mz * mz)
        if norm == 0.0:
            return
        norm = 1.0 / norm
        mx = mx * norm
        my = my * norm
        mz = mz * norm


        _2q1mx = 2.0 * q1 * mx
        _2q1my = 2.0 * q1 * my
        _2q1mz = 2.0 * q1 * mz
        _2q2mx = 2.0 * q2 * mx


        hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
        hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 - my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4
        _2bx = (hx * hx + hy * hy)**0.5
        _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4 - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4
        _4bx = 2.0 * _2bx
        _4bz = 2.0 * _2bz

        s1 = - _2q3 * (2.0 * q2q4 - _2q1q3 - ax) + _2q2 * (2.0 * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz);
        s2 = _2q4 * (2.0 * q2q4 - _2q1q3 - ax) + _2q1 * (2.0 * q1q2 + _2q3q4 - ay) - 4.0 * q2 * (1.0 - 2.0 * q2q2 - 2.0 * q3q3 - az) + _2bz * q4 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz);
        s3 = - _2q1 * (2.0 * q2q4 - _2q1q3 - ax) + _2q4 * (2.0 * q1q2 + _2q3q4 - ay) - 4.0 * q3 * (1.0 - 2.0 * q2q2 - 2.0 * q3q3 - az) + (-_4bx * q3 - _2bz * q1) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz);
        s4 = _2q2 * (2.0 * q2q4 - _2q1q3 - ax) + _2q3 * (2.0 * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
        
        norm = math.sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4)
        norm = 1.0 / norm
        s1 *= norm
        s2 *= norm
        s3 *= norm
        s4 *= norm

        qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz) - beta * s1
        qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy) - beta * s2
        qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx) - beta * s3
        qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx) - beta * s4

        q1 += qDot1 * deltat
        q2 += qDot2 * deltat
        q3 += qDot3 * deltat
        q4 += qDot4 * deltat
        
        norm = (q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4)**0.5
        norm = 1.0 / norm
        qx.append(q1 * norm)
        qy.append(q2 * norm)
        qz.append(q3 * norm)
        qw.append(q4 * norm)


    def obter_quaternions():
        for i in range(len(Indice)):
            Dados.quaternions(AccX[i],AccY[i],AccZ[i],GyroX[i],GyroY[i],GyroZ[i],MagX[i],MagY[i],MagZ[i],deltat[i])
        for i in range(len(Indice)):
            quaternions_count.append(np.array([qx[i],qy[i],qz[i],qw[i]]))

    def gravity_compensate(q, acc):
      g = [0.0, 0.0, 0.0]
          
      g[0] = 2 * (q[1] * q[3] + q[0] * q[2])
      g[1] = 2 * (q[2] * q[3] - q[0] * q[1])
      g[2] = q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]
      
      return [acc[0] - g[0], acc[1] - g[1], acc[2] - g[2]]

    def obter_cleanAccel():
        for i in range(len(AccCount)):
            cleanAcc.append(Dados.gravity_compensate(quaternions_count[i], AccCount[i]))
        for i in range(len(cleanAcc)):
            cleanAccX.append(cleanAcc[i][0])
            cleanAccY.append(cleanAcc[i][1])
            cleanAccZ.append(cleanAcc[i][2])

    def product(lista): 
        return reduce(lambda acumulado, atual: acumulado * atual, lista)

    def lagrange(x, fx):                                                              
        L = lambda num, xi: Dados.product((num - xj) / (xi - xj) for xj in x if xj != xi)
        return lambda num: sum([yi * L(num, xi) for xi, yi in zip(x, fx)])
        
    def integration_simpson(a, b, x,y , nb_ech):
        f = Dados.lagrange(x,y)
        h = (b-a)/np.double(nb_ech)
        z = np.double(f(a)+f(b))

        for i in range(1,nb_ech,2) :
            z += 4 * f(a+i*h)
        for i in range(2, nb_ech-1, 2):
            z += 4 * f(a+i*h)

        val_int =  z*(h/3)
##        val_int *= delta_t

        return val_int

    def obter_velocidade():
        for i in range(int(len(tempos)/8)):
            velocidades.append(Dados.integration_simpson(tempos[i*8], tempos[((i*8)+8)-1], cleanAccZ[i*8:(i*8)+8],tempos[i*8:(i*8)+8], 8))

            
    
Dados.obter_acc()
Dados.obter_gyr()
Dados.obter_mag()
Dados.obter_indice()
Dados.obter_deltat()
Dados.obter_time()

AccX = np.array(AccX).astype(float)
AccY = np.array(AccY).astype(float)
AccZ = np.array(AccZ).astype(float)
AccCount = np.array(AccCount).astype(float)
GyroX = np.array(AccX).astype(float)
GyroY = np.array(AccY).astype(float)
GyroZ  = np.array(AccZ).astype(float)
MagX = np.array(AccX).astype(float)
MagY = np.array(AccY).astype(float)
MagZ  = np.array(AccZ).astype(float)
Indice = np.array(Indice).astype(int)
deltat = np.array(deltat).astype(float)
tempos = np.array(tempos).astype(float)
tempos = tempos - tempos[0]
tempos = tempos/100000

Dados.obter_quaternions()
Dados.obter_cleanAccel()
Dados.obter_velocidade()



        
        
        
        
        
    
