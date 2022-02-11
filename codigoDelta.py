import sympy as s
import math
import numpy as np
import matplotlib.pyplot as plt



v = 7 #velocidade do vento
Clbeta = -0.0218166735093509 
Cl_delta_aileron = 0.142 
v_min = 9 # Velocidade  maxima e mínima foram retiradas dos inputs de estabilidade como envolope de voo
v_max = 25
V = np.arange(v_min,v_max,0.1) #velocidade do aviao u
length = len(V)
delta = np.empty(length)
i=0

for velocidadeAviao in V:
    if velocidadeAviao < v:
        break
    else:
        delta[i] = -Clbeta * np.arctan( v / velocidadeAviao) / Cl_delta_aileron  * 57.3
        i = i+1
        print('A velocidade do aviao eh : ', velocidadeAviao)
        print('O valor de Delta eh', delta)





titulo = "Variação de $\delta_a$ em função da velocidade do avião"
xlabel = r'V''(m/s)'
ylabel = r'$\delta_a$' '($\degree$)'
font = {'fontname': 'Roboto'}
laranja = '#EF7911FF'
fundo = (0.25,0.25,0.25)

fig = plt.figure()
fig.patch.set_facecolor(fundo)
ax = fig.add_subplot(1,1,1)
ax.plot(V,delta, color=laranja)
ax.set_facecolor(fundo)
ax.set_title(titulo, color=laranja, **font, fontsize=16)
ax.set_xlabel(xlabel, color=laranja, **font, fontsize = 14)
ax.set_ylabel(ylabel, color=laranja, **font, fontsize =14)
ax.grid(color = laranja, linestyle='dotted')


ax.spines['bottom'].set_color(laranja)
ax.spines['top'].set_color(laranja)
ax.spines['right'].set_color(laranja)
ax.spines['left'].set_color(laranja)
ax.tick_params(axis='x', colors=laranja)
ax.tick_params(axis='y', colors=laranja)
plt.show()