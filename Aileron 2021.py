import numpy as np
import sympy as s
import copy as c
from scipy.interpolate import interp1d
import math
import xlsxwriter as xls


m =  -0.1744186046511628
n = 0.4875
numAileronTrapezoidal = 1
numAileronReto = 1
Pretaw = 0.2
Angt = math.radians(30)
CR = 0.450
CP = 0.300
LambdaAsa = CP / CR
b = 2.150
envergReta = b * Pretaw
semienvergReta = envergReta/2
ARAsa = 4.175700090334237
S = (b ** 2) / ARAsa
Ssemiasa = S / 2
CLaw = 0.100197238
yStall = 0.20 #porcentagem da semi envergadura
y2 = 0

aileronsReta = [] #Lista de ailerons começando na parte reta
aileronsTrapezoidal = [] #Lista de ailerons começando na parte trapezoidal
aileronTemp = [] #Lista temporária para copiar ailerons para o banco de dados

#corda para fazer a integração
y = s.Symbol('y')
cordaReta = CR
cordaTrapezoidal = m*y + n


# Ranges de variáveis:
#T -> pertence ao aileron na parte trapezoidal
#R -> pertence ao aileron na parte reta
#0 -> inicial
#f -> final
y2T0 = 0.850
y2Tf = 0.960
y2R0 = 0
y2Rf = 0
y1min = (yStall + 0.10) * (b/2)
incrementoY = 0.01
eaileronT0 = 0.17
eaileronTf = 0.55
eaileronR0 = 0
eaileronRf = 0
incrementoEnvergadura = 0.015
tau0 = 0.1
tauf = 0.35
incrementoTau = 0.01
Cldeltaamin = 0.05
Cldeltaamax = 0.15
Jmin = 0.048
Jmax = 0.070
cordaAileronmin = 0.10*(m*y2 + n)
cordaAileronmax = 0.30*(m*y2 + n)


tau_grafico = [0,0.28, 0.4, 0.51,0.6 ,0.68, 0.72, 0.8]
razao_grafico = [0,0.1 ,0.2 , 0.3,0.4, 0.5,0.6 ,0.7]
propAreas = interp1d(tau_grafico,razao_grafico) #Retorna função que dá razão entre áreas a partir de tau


def aileronTrapezoidal():
    numeroAilerons = round(((y2Tf - y2T0)/incrementoY)* ((eaileronTf-eaileronT0)/incrementoEnvergadura) * ((tauf-tau0)/incrementoTau)) #Análise combinatória pra saber quantos vão ser gerados
    print('Serão gerados {} ailerons começando na parte trapezoidal da asa.'.format(numeroAilerons))
    numAileron = 0
    for y2 in np.arange(y2T0,y2Tf+incrementoY,incrementoY):
        for eaileron in np.arange(eaileronT0,eaileronTf+incrementoEnvergadura,incrementoEnvergadura):
            y1 = y2 - eaileron
            if y1 >= y1min and y1 >= semienvergReta:  # implica aileron na parte trapezoidal
                for tau in np.arange(tau0,tauf+incrementoTau,incrementoTau):
                    Cldeltaa = 57.3*((2 * CLaw * tau) /(S*b)) * s.integrate(cordaTrapezoidal*y,(y,y1,y2))
                    if Cldeltaa >= Cldeltaamin and Cldeltaa <= Cldeltaamax:
                        J = ((tau * b * Angt)/4)*(s.integrate(cordaTrapezoidal*y,(y,y1,y2)))/(s.integrate(cordaReta*(y**2),(y,0,semienvergReta)) + s.integrate(cordaTrapezoidal*(y**2),(y,semienvergReta,(b/2))) ) #pb/2V
                        if J >= Jmin and J <= Jmax:
                            razaoAreas = propAreas(tau)
                            areaAileron = Ssemiasa*razaoAreas
                            cordaAileron = areaAileron/eaileron
                            razaoEnverg = eaileron / (b/2)
                            if cordaAileron >= cordaAileronmin and cordaAileron <= cordaAileronmax and razaoEnverg <= 0.4 and razaoEnverg >=0.35:
                                print('Aileron encontrado!')
                                numAileron = numAileron + 1
                                aileronTemp.append(numAileron)
                                aileronTemp.append(y1)
                                aileronTemp.append(y2)
                                aileronTemp.append(eaileron)
                                aileronTemp.append(cordaAileron)
                                aileronTemp.append(Cldeltaa)
                                aileronTemp.append(J)
                                aileronTemp.append(tau)
                                aileronTemp.append(areaAileron)
                                aileronTemp.append(razaoAreas)
                                aileronTemp.append(razaoEnverg)
                                aileronsTrapezoidal.append(c.copy(aileronTemp))
                                aileronTemp.clear()

aileronTrapezoidal() #Função que gera ailerons na parte trapezoidal

planilhaAilerons = xls.Workbook('/Users/ruansantiago/Desktop/Ruan/BlackBird/Códigos/planilhaAilerons.xlsx') #Criando a planilha
formato_cabecalho = planilhaAilerons.add_format(
    {
        'bg_color': '#9BC2E6',
        'bold': True,
        'border': True
    }
)

formato_dados = planilhaAilerons.add_format(
    {
        'bg_color': '#BDD7EE',
        'border': True
    }
)


abaPlanilha = planilhaAilerons.add_worksheet() #Criando aba da planilha
abaPlanilha.write('A1', "Número",formato_cabecalho) #Cabeçalho da planilha
abaPlanilha.write('B1','Y1',formato_cabecalho)
abaPlanilha.write('C1','Y2',formato_cabecalho)
abaPlanilha.write('D1','Enverg',formato_cabecalho)
abaPlanilha.write('E1','Corda',formato_cabecalho)
abaPlanilha.write('F1','Cldeltaa',formato_cabecalho)
abaPlanilha.write('G1','pb/2V',formato_cabecalho)
abaPlanilha.write('H1','tau',formato_cabecalho)
abaPlanilha.write('I1','Área',formato_cabecalho)
abaPlanilha.write('J1','Razão áreas',formato_cabecalho                  )
abaPlanilha.write('K1','Razão enverg',formato_cabecalho)


#Gravar dados da matriz com os ailerons na planilha
for linha in range(len(aileronsTrapezoidal)):
    for coluna in range(11):
        abaPlanilha.write(linha+1,coluna,aileronsTrapezoidal[linha][coluna],formato_dados)
planilhaAilerons.close()

print('{} ailerons passaram no teste'.format(linha+1))

def aileronReta():
    pass







#Calculos Aileron na parte reta

#Cldeltaa = 57.3*((2 * CLaw * tau) /(S*b)) * (s.integrate(cordaReta*y,(y,y1,semienvergReta))+s.integrate(cordaTrapezoidal*y,(y,semienvergReta,y2)))
#J = (1/57.3)*((tau * b *Angt)/4) * (s.integrate(cordaReta*y,(y,y1,semienvergReta))+s.integrate(cordaTrapezoidal*y,(y,semienvergReta,y2))) / (s.integrate(cordaReta*y**2,(y,0,semienvergReta))+s.integrate(cordaTrapezoidal*y**2,(y,semienvergReta,b/2)))












