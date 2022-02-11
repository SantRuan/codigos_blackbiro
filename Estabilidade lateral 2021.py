import sympy as s
import math
import numpy as np
import matplotlib.pyplot as plt

#Alo git hub

m =  -0.1744186046511628 #Função corda da parte trapezoidal da asa
n = 0.4875
Pretaw = 0.6
CR = 0.450
CP = 0.400
LambdaAsa = CP / CR
b = 2.05
envergReta = b * Pretaw
semienvergReta = envergReta/2
ARAsa = 4.659 #Conferido
S = ((b ** 2) / ARAsa) * 2
Ssemiasa = S / 2
CLaw = math.degrees(0.0577)
sweep = math.radians(0) #ângulo de enflexamento
T = math.radians(0)     #Diedro
configAsa = 1
Cl_delta_aileron = 0.100197238
Nv = 0.9
Sv = 0.0777 #conferido
Zv = 0.349
CLav = math.degrees(0.0577)
y = s.Symbol('y')
cordaTrapezoidal = m*y + n


def analiseEstabilidadeLateral():

    ybarra = (2/S) * (s.integrate(CR*y, (y, 0, semienvergReta)) + s.integrate(cordaTrapezoidal*y, (y, semienvergReta, b/2)))

    CL = 1.122967 #CL em velocidade de cruzeiro e alpha = 3º
    Clbetasweep = -CL * ybarra/b * math.sin(2*sweep)
    print('Contribuição do ângulo de enflechamento: {}'.format(Clbetasweep))

    ClbetaT = -T * CLaw * ybarra/b
    print('Contribuição do ângulo de diedro: {}'.format(ClbetaT))

    ClbetaV = - Nv * (Sv/S) * (Zv/b) * CLav
    print('Contribuição da empenagem vertical: {}'.format(ClbetaV))

    if configAsa == 0:
        Clbetafus = 0.0006
    elif configAsa == 1:
        Clbetafus = 0
    elif configAsa == 2:
        Clbetafus = -0.0006
    print('Contribuição da fuselagem: {}'.format(Clbetafus))

    Clbeta = Clbetasweep + ClbetaT + ClbetaV + Clbetafus
    print('dCl/dBeta {}\n'.format(Clbeta))
    if Clbeta == 0:
        print('Aeronave com estabilidade lateral estática neutra!')
    elif Clbeta < 0:
        print('Aeronave lateralmente estável!')
    elif Clbeta > 0:
        print('Aeronave lateralmente instável')

    beta = np.linspace(-15,15,1000)
    Cl = beta * Clbeta * (math.pi/180)

    print('',)
    plt.plot(beta,Cl,label = 'C_{n} x Delta')
    plt.title('Coeficiente de momento de guinada versus deflexao dos lemes',fontsize='13', y = 1.029)
    plt.ylim([-0.015,0.015])
    plt.xlim([-15,15])
    plt.xlabel(r'$\delta$',fontsize = '14')
    plt.ylabel('$C_{n}$',fontsize = '14')
    plt.show()

analiseEstabilidadeLateral()













