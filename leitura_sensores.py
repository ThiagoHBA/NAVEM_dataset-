import os
import json
import math
import numpy as np
from numpy.linalg import inv
import math
from matplotlib import pyplot as plt

def mult_3x3_3x1(a,b):
  soma = 0
  mult = []
  newMatrix = []
  
  for i in range(3):
    for j in range(3):
      mult.append(a[i][j] * b[j]);      
    for k in range(3):
      soma += mult[k];
  
    newMatrix.append(soma);
    soma = 0;
  return newMatrix

def gravity_compensate(q, acc):
  g = [0.0, 0.0, 0.0]
      
  g[0] = 2 * (q[1] * q[3] + q[0] * q[2])
  g[1] = 2 * (q[2] * q[3] - q[0] * q[1])
  g[2] = q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]
  
  return [acc[0] - g[0], acc[1] - g[1], acc[2] - g[2]]



def matriz_rotação(quats):
  q = []
  q.append(quats[0])
  q.append(quats[1])
  q.append(quats[2])
  q.append(quats[3])
  
  RotationMat = [[],[],[]]
  
  m = [[-2*(q[2]**2) - 2*(q[3]**2), 2*(q[1]*q[2]) - 2*(q[3]*q[0]),  2*(q[1]*q[3])+ 2*(q[2]*q[0])],
  
  [2*(q[1]*q[2]) + 2*(q[3]*q[0]),  -2*(q[1]**2) - 2*(q[3]**2), 2*(q[2]*q[3]) - 2*(q[1]*q[0])],

   [2*(q[1]*q[3]) - 2*(q[2]*q[0]), 2*(q[2]*q[3]) + 2*(q[1]*q[0]),  2*(q[1]**2) - 2*(q[2]**2)]]
  
  return m


pasta = "C:/Users/thiag/Desktop/NAVEM/VisualStudio/imagens/9250_quaternions/"
arquivo = "Contador de Dados.json"
sense_txt = open(pasta + arquivo,"r")

sensor = json.load(sense_txt)

AccX = []
AccY = []
AccZ = []
AccCount = []

for Acc in sensor["Dados"]:
    AccX.append(Acc["AccX"])
    AccY.append(Acc["AccY"])
    AccZ.append(Acc["AccZ"])
    AccCount.append(Acc["AccX"])
    AccCount.append(Acc["AccY"])
    AccCount.append(Acc["AccZ"])

GyroX = []
GyroY = []
GyroZ = []

for Gyr in sensor["Dados"]:
    GyroX.append(Gyr["GyrX"])
    GyroY.append(Gyr["GyrY"])
    GyroZ.append(Gyr["GyrZ"])

Indice = []

for i in sensor["Dados"]:
    Indice.append(i["i"])

quat0 = []
quat1 = []
quat2 = []
quat3 = []
    
for q0 in sensor["Dados"]:
    quat0.append(q0["q0"])
for q1 in sensor["Dados"]:
    quat1.append(q1["q1"])
for q2 in sensor["Dados"]:
    quat2.append(q2["q2"])
for q3 in sensor["Dados"]:
    quat3.append(q3["q3"])


AccX = np.array(AccX).astype(float)
AccY = np.array(AccY).astype(float)
AccZ = np.array(AccZ).astype(float)

GyroX = np.array(GyroX).astype(float)
GyroY = np.array(GyroY).astype(float)
GyroZ = np.array(GyroZ).astype(float)

#--------------------------------------
Quat0_float = np.array(quat0).astype(float)
Quat1_float = np.array(quat1).astype(float)
Quat2_float = np.array(quat2).astype(float)
Quat3_float = np.array(quat3).astype(float)
#--------------------------------------

cleanAccX = []

quaternions = []

for i in range(len(Quat0_float)):
    quaternions.append(Quat0_float[i])
    quaternions.append(Quat1_float[i])
    quaternions.append(Quat2_float[i])
    quaternions.append(Quat3_float[i])
    
Accs = []

for i in range(0,len(AccCount),3):
    Accs.append(AccCount[i:i+3])
    
Accs = np.array(Accs).astype(float)

quats = []

for i in range(0,len(quaternions),4):
    quats.append(quaternions[i:i+4])

cleanAcc = []

for i in range(0,len(Accs),1):
    cleanAcc.append(gravity_compensate(quats[i], Accs[i]))

cleanAccX = []
cleanAccY = []
cleanAccZ = []

for i in range(len(cleanAcc)):
    cleanAccX.append(cleanAcc[i][0])
    cleanAccY.append(cleanAcc[i][1])
    cleanAccZ.append(cleanAcc[i][2])

inv_matriz_rotação = []
rotation_matrix = []

for i in range(len(quats)):
  rotation_matrix.append(matriz_rotação(quats[i]))
  try:
    inv_matriz_rotação.append(inv(rotation_matrix[i]))
  except:
    inv_matriz_rotação.append(rotation_matrix[i])

imu_json = []
for i in range(len(cleanAccX)):
  dados = {
    'AccX': cleanAccX[i],
    'AccY': cleanAccY[i],
    'AccZ': cleanAccZ[i],
    'GyrX': GyroX[i],
    'GyrY': GyroY[i],
    'GyrZ': GyroZ[i]
  }
  imu_json.append(dados)

def escrever_json(lista):
    arquivo = 'CleanSense.json'
    with open(pasta+arquivo, 'w') as f:
      json.dump(lista, f, indent = 4)

escrever_json(imu_json)

#PARA PLOTAR O GRÁFICO:
      
##frame_inicial = 0
##frame_final = 100
##plt.plot(AccX[frame_inicial*8 :frame_final*8], color = "blue", label = "AccX")
##plt.plot(AccY[frame_inicial*8 :frame_final*8], color = "black", label = "AccY")
##plt.plot(AccZ[frame_inicial*8 :frame_final*8], color = "red", label = "AccZ")
##plt.legend()
##plt.show()
