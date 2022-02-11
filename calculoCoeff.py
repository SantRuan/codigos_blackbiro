import numpy as np
import math
import sympy as s
from scipy.interpolate import interp1d
import xlsxwriter as xls
import matplotlib.pyplot as plt



cl = [1.50, 1.73]
alfa = [4,7]
AR = 6.7 # AR = alongamento. Define a razão entre a envergadura e a corda do perfil  b / c 
e = 0.98 # e  é um fator estimado por um parâmetro sigma de arrasto 1 / 1+ sigma
c_med = 0.37 #corda media aerodinâmica
hcg = 0.1587 #distancia do bordo de ataque ao centro de gravidade
hac = 0.1225 #distância do bordo de ataque ao centro aerodinâmico

#Curva cl vs Alfa
plt.plot(cl,alfa, label='Gráfico cl vs Alfa')
plt.show()

#Calculo do coeficiente angular da reta cl vs alfa
a0 = (cl[0]- cl[1]) / (alfa[0] - alfa[1] )
print(a0)

#Calculo de a para asa finita

a = a0 / (1 +(57.3*a0 /(math.pi*e*AR)))
print(a)

# Considerando um angulo de ataque para sustenção nula de -10 o coeficiente de sustentação será
alfa0 = -10
Cl0 = a * (0 - alfa0)
print(Cl0)


# Pela leitura do Gráfico, o coeficiente para alfaw =0 é obtido pela leitura do gráfico
# cm vs alfa que é -0.24

Cmac = -0.24
Cm0w = Cmac + Cl0 * ( (hcg - hac)/c_med )
print(Cm0w)

#Coeficiente angular da curva dos momentos é calculado por
Cm_alfa_w = a*( (hcg - hac)/c_med )
print(Cm_alfa_w)

# A equação que define a variação do coeficiente do momento em função do angulo de ataque é
x = s.Symbol('x')

Cm_CG_w = Cm0w + Cm_alfa_w * x


print(x)
