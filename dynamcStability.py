import numpy as np
import scipy.signal as sig
from scipy.integrate import odeint
import matplotlib.pyplot as plt 
## Stability coefficients
 ## Input list
g = 32.2
m= 85.4
Iy = 3000
S = 184
p = 0.002378
u_0 = 176
Q = 0.5 *  p * u_0**2
C_du = 0
C_d0 = 0.05
C_lu = 0
C_l0 = 0.41
C_da = 0.33

C_la = 4.44
corda =5.7
Cmu = 0
C_ma = -0.683
C_za_dot = 0
C_ma_dot = -4.36
C_mq = -9.96
C_zq = 0

## Logitudinal  derivatives from table 4.9 of Nelson

### for u
X_u = -(C_du + 2 * C_d0) * Q * S / (m * u_0)
Z_u = -(C_lu + 2 * C_l0) * Q * S / (m * u_0)
M_u =  Cmu *(Q*S * corda) / (u_0 * Iy)

## W derivatives

X_w = -(C_da -  C_l0) * Q * S / (m * u_0)
Z_w = -(C_la +  C_d0) * Q * S / (m * u_0)
M_w = C_ma * Q * S * corda / (Iy * u_0)

## W_DOT derivatives

Zw_dot = C_za_dot * corda * Q * S / ((m * u_0) * 2 * u_0)
Mw_dot = C_ma_dot * corda * Q * S * corda / ((2 * u_0) *( Iy * u_0))


## q derivatives

Z_q = C_zq * corda  * Q * S / (m * 2 * u_0)
X_q = 0
M_q = C_mq * corda * S * Q * corda /( 2 * u_0 * Iy)


### Matrix     

A = np.array([[X_u , X_w ,0, -g], 
     [Z_u, Z_w, u_0, 0], 
     [M_u + Mw_dot * Z_u , M_w + Mw_dot * Z_w , M_q + Mw_dot * u_0, 0],
     [0 , 0, 1 ,0]])


print(A)

autovalores = np.linalg.eigvals(A)
nil1 = abs((autovalores[0]+ autovalores[1])/ 2)
nil2 = abs((autovalores[2]+ autovalores[3])/ 2)
w1 = abs((autovalores[0] -autovalores[1])/ 2)
w2 = abs((autovalores[2] - autovalores[3])/ 2)

print(w1)
print(w2)
                #Calculo do período da função senoidal

t_Periodo = 2 * np.pi / w1
N_ciclos = 0.101 * nil1 / w1
print(nil1)
print(N_ciclos)
print(t_Periodo)
t = 0.693/nil1  # Calculo do Tempo de meia vida de oscilação
