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
from Imagens import Imagens
from Sensores import Dados

acc_linear = False
vetor_lateral = False
giro_corpo = False
acc_linear_Z = False
eixo_invertidoX = False
vel = False
vel_per_frame = False
gravityForce = 9.80665

'''----------------------------------------------------------------------------------------------------------------'''

##imagem = "./camera+captura/NOVOS_EXPS_NEWMPU/"+exp+"/frames.json"
##pasta = "./camera+captura/NOVOS_EXPS_NEWMPU/"+exp+"/"
##arquivo = "accelerations.json"

pasta = "./camera+captura/Exps_28.06.2021/Exp2/"
imagem = pasta + "frames.json"
arquivo = "accelerations.json"

sense_txt = open(pasta + arquivo,"r")
sensor = json.load(sense_txt)

##acc_linear = True
vel = True
##vel_per_frame = True

'''----------------------------------------------------------------------------------------------------------------'''

Dados.obter_acc(sensor)
Dados.obter_time(sensor)
Imagens.abrirCam(imagem)

AccX_MPU = Dados.AccX_MPU
AccY_MPU = Dados.AccY_MPU
AccZ_MPU = Dados.AccZ_MPU
AccCount = Dados.AccCount
roll_MPU = Dados.roll_MPU
pitch_MPU = Dados.pitch_MPU
yaw_MPU = Dados.yaw_MPU
tempos = Dados.tempos
diffTempos = Dados.diffTempos

timeIniArray = Imagens.timeIniArray
timeFimArray = Imagens.timeFimArray
timeFimIniArray = Imagens.timeFimIniArray

timeIniArray = np.array(timeIniArray).astype(float)
timeFimArray = np.array(timeFimArray).astype(float)
timeFimIniArray = np.array(timeFimIniArray).astype(float)

AccX_MPU = np.array(AccX_MPU).astype(float)
AccY_MPU = np.array(AccY_MPU).astype(float)
AccZ_MPU = np.array(AccZ_MPU).astype(float)

##AccY_MPU *= -1

AccX_MPU = (AccX_MPU / 16384) * gravityForce;
AccY_MPU = (AccY_MPU / 16384) * gravityForce;
AccZ_MPU = (AccZ_MPU / 16384) * gravityForce;

AccCount = np.array(AccCount).astype(float)

roll_MPU = np.array(roll_MPU).astype(float)
pitch_MPU = np.array(pitch_MPU).astype(float)
yaw_MPU  = np.array(yaw_MPU).astype(float)

tempos = np.array(tempos).astype(float)
tempos = tempos - tempos[0]
tempos = tempos/1000000
timeFimIniArray = timeFimIniArray/1000000

#=====================================================================

####Aceleração e velocidade graficos.
if acc_linear:
    fig, axs = plt.subplots(3)
    
    axs[0].plot(tempos,AccX_MPU) #marker = "o"
    axs[0].set_title("AccX_MPU", loc = 'left')

    axs[1].plot(tempos,AccY_MPU) #marker = "o"
    axs[1].set_title("AccY_MPU", loc = 'left')

    axs[2].plot(tempos,AccZ_MPU) #marker = "o"
    axs[2].set_title("AccZ_MPU", loc = 'left')
    

elif vel:
    Vel_MPU_X = Dados.obter_velocidade_geral(AccX_MPU, tempos, 0, len(tempos)-1)
    Vel_MPU_Y = Dados.obter_velocidade_geral(AccY_MPU, tempos, 0, len(tempos)-1)
    Vel_MPU_Z = Dados.obter_velocidade_geral(AccZ_MPU, tempos, 0, len(tempos)-1)
    
    fig, axs = plt.subplots(3)
    
    axs[0].plot(Vel_MPU_X)
    axs[0].set_title("Vel MPU X ",loc = 'left')

    axs[1].plot(Vel_MPU_Y)
    axs[1].set_title("Vel MPU Y ",loc = 'left')
    
    axs[2].plot(Vel_MPU_Z)
    axs[2].set_title("Vel MPU Z ",loc = 'left')
    

elif vel_per_frame:
    fig, axs = plt.subplots(3)
    
    axs[0].plot(medias_velX)
    axs[0].set_title("Vel MPU Per frame X ",loc = 'left')

    axs[1].plot(medias_velY)
    axs[1].set_title("Vel MPU Per frame Y ",loc = 'left')
    
    axs[2].plot(medias_velZ)
    axs[2].set_title("Vel MPU Per frame Z ",loc = 'left')
    
    
plt.show()


#=====================================================================

#Sepração por arquivos

indexPrimeiroDado = 4

for i in range(indexPrimeiroDado,len(tempos), 1):
    diffTempos.append(tempos[i] - tempos[i-1])
    
inicio = 0
contadorDeDados = 0
dadosPorFrame = []

medias_velX = []
medias_velY = []
medias_velZ = []

for i in range(1,len(timeFimIniArray),1):
    arquivo = open(str(pasta) + "/frame" + str(i) + ".txt", "w")
    print("="*100)
    print("FRAME: ", i)
    print('~'*30)
    
    soma = 0
    arquivoDados = []
    dados = []
    contadorDeDados = 0
    
    accXPerFrame = []
    accYPerFrame = []
    accZPerFrame = []
    
    for j in range(inicio,len(diffTempos),1):
        soma += diffTempos[j]
        
        if(soma >= timeFimIniArray[i]):
            Vel_MPU_X = Dados.obter_velocidade_geral(accXPerFrame, tempos[inicio : inicio + contadorDeDados], 0, contadorDeDados)
            Vel_MPU_Y = Dados.obter_velocidade_geral(accYPerFrame, tempos[inicio : inicio + contadorDeDados], 0, contadorDeDados)
            Vel_MPU_Z = Dados.obter_velocidade_geral(accZPerFrame, tempos[inicio : inicio + contadorDeDados], 0, contadorDeDados)
            
            velMediaX = np.mean(Vel_MPU_X)
            velMediaY = np.mean(Vel_MPU_Y)
            velMediaZ = np.mean(Vel_MPU_Z)
            
            arquivoDados.append("Vel. Media X: " + str(velMediaX) + "\n")
            arquivoDados.append("Vel. Media Y: " + str(velMediaY) + "\n")
            arquivoDados.append("Vel. Media Z: " + str(velMediaZ))
            
            arquivo.writelines(arquivoDados)
            
            print("Velocidade média X: ", velMediaX)
            print("Velocidade média Y: ", velMediaY)
            print("Velocidade média Z: ", velMediaZ)
            
            print('~'*30)
            print("Estão dentro do intervalo de: ", timeFimIniArray[i])
            
            medias_velX.append(velMediaX)
            medias_velY.append(velMediaY)
            medias_velZ.append(velMediaZ)
            
            dadosPorFrame.append(contadorDeDados)
            
            accXPerFrame = []
            accYPerFrame = []
            accZPerFrame = []
            
            break

        indiceAtual = inicio + (indexPrimeiroDado - 1)

        accXPerFrame.append(AccX_MPU[indiceAtual])
        accYPerFrame.append(AccY_MPU[indiceAtual])
        accZPerFrame.append(AccZ_MPU[indiceAtual])
        
        print("Dados AccX: ", AccX_MPU[indiceAtual])
        print("Dados AccY: ", AccY_MPU[indiceAtual])
        print("Dados AccZ: ", AccZ_MPU[indiceAtual])

        dados.append(AccX_MPU[indiceAtual])
        dados.append(AccY_MPU[indiceAtual])
        dados.append(AccZ_MPU[indiceAtual])
        
        arquivoDados.append("AccX: " + str(AccX_MPU[indiceAtual]) + "\n")
        arquivoDados.append("AccY: " + str(AccY_MPU[indiceAtual]) + "\n")
        arquivoDados.append("AccZ: " + str(AccZ_MPU[indiceAtual]) + "\n")
        arquivoDados.append("\n")
        
        contadorDeDados += 1
        inicio += 1
        
        print("DiffTempos: ", diffTempos[j], "Soma: ", soma)

print("Média de dados por frame: ", np.mean(dadosPorFrame))
    
for i in range(len(dadosPorFrame)):
    if(dadosPorFrame[i] < 3):
        print("O frame de número ", i+1, "Possui apenas ", dadosPorFrame[i], "dados.")
    




        
        
        
        
        
    
