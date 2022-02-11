import math
import numpy as np
import matplotlib.pyplot as plt

densidade = 1.128 #conferido
b = 2.05    #conferido
ARAsa = 4.659   #conferido
Ixx = 1.03909 #momento de inercia
Sw = (b ** 2) / ARAsa #Área da asa
Sv = 0.0777 #conferido
Sh = 0.385 #conferido
tau = 0.22 #conferido
Cldeltaa = 0.142 #conferido
Angt = 30 #conferido
Cl = Cldeltaa*math.radians(Angt) #coeficiente de momento gerado pelo aileron em máxima deflexão
Vestol = 9.141 #conferido
Vt = Vestol*1.1


Laileron = (1/2) * Vt**2 * densidade * Sw * Cl * b
Cdr = 0.7 #coeficiente de arrasto de rolamento
yd = 0.4/(b/2) #braço de momento do arrasto de rolamento
Pss = math.sqrt((2*Laileron)/(densidade*(Sw+Sh+Sv)*Cdr * math.pow(yd,3)))
theta1 = Ixx/(densidade*(pow(yd,3))* (Sw + Sh + Sv)* Cdr)* np.log(math.pow(Pss,2))
aceleracao_angular = math.pow(Pss,2)/(2*theta1)

print('PSS: {}'.format(Pss))
print('Theta1: {}'.format(theta1))
print('P`: {}'.format(aceleracao_angular))
print('L: {}'.format(Laileron))



def t_roll(bankAngle):
    t2 = math.sqrt((2*bankAngle)/aceleracao_angular)
    return t2

tempoRolamento = [0] * 1000
bankAngle_rad = np.linspace(0,math.radians(60),1000)
bankAngle_deg = [0] * 1000
for j in range(0,1000):
    bankAngle_deg[j] = math.degrees(bankAngle_rad[j])

for i in range(0,1000):
    tempoRolamento[i] = t_roll(bankAngle_rad[i])

plt.plot(bankAngle_deg,tempoRolamento)
plt.title('Tempo de rolamento em função de $\Phi$ desejado')
plt.legend(loc= 'best',frameon=False, fontsize=14);
plt.xlim(0,60)
plt.xlabel('Ângulo de rolamento(º)')
plt.ylabel('Tempo\n(s)')
plt.show()

