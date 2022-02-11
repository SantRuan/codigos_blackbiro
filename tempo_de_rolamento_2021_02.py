import matplotlib.pyplot as plt
import numpy as np
import scipy
import math
rho = 1.225
s_w = 2* 0.902
cma = 0.4405
Cl_delta = 0.142 / 57.3
Ixx = 1

v = 12
Phi = np.linspace(0, 60, 100)
delta = 30
cl = Cl_delta * delta
l = 0.5*cl*rho*s_w*cma*v**2
t = (2*Ixx* Phi/l)**(1/2)


titulo = "Tempo por ângulo de rolamento"
xlabel = "Ângulo de rolamento (º)"
ylabel = "tempo\n(s)"
font = {'fontname': 'Roboto'}
laranja = '#EF7911FF'
fundo = (0.25,0.25,0.25)

fig = plt.figure()
fig.patch.set_facecolor(fundo)
ax = fig.add_subplot(1,1,1)
ax.plot(Phi, t, color=laranja)
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