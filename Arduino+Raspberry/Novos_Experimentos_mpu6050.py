import numpy as np
import json
import os
import re

accx = []
accy = []
accz = []
yaw = []
pitch = []
roll = []
times = []
imu_json = []

def array_sensores(txt,AccX,AccY,AccZ,Yaw,Pitch,Roll,tempos):
    arquivo = open(txt, 'r')
    lista_dados = arquivo.readlines()

    for i in range(len(lista_dados)):
        linha_amostras = str(lista_dados[i])
        dados_split = linha_amostras.split(":",6)
        
        AccX.append(dados_split[0])
        AccY.append(dados_split[1])
        AccZ.append(dados_split[2])
        Yaw.append(dados_split[3])
        Pitch.append(dados_split[4])
        Roll.append(dados_split[5])
        tempos.append(dados_split[6][:-1])

        
    arquivo.close()

    
def escrever_json(lista):
    arquivo = 'Experimento_4.json'
    pasta = os.path.dirname(os.path.abspath(__file__))
    with open(pasta+'/'+arquivo, 'w') as f:
      json.dump(lista, f, indent = 4)
      

def preparar_json(a,b,c,d,e,f,g):
    for i in range(len(a)):
      dados = {
        'AccX': a[i],
        'AccY': b[i],
        'AccZ': c[i],
        'Roll': d[i],
        'Pitch': e[i],
        'Yaw': f[i],
        'tempos': g[i]
      }
      imu_json.append(dados)


array_sensores('Exp5.txt',accx,accy,accz,yaw,pitch,roll,times)
preparar_json(accx,accy,accz,roll,pitch,yaw,times)
escrever_json(imu_json)
