import numpy as np
import math
from scipy.interpolate import interp1d
import xlsxwriter as xls

CLaw = 0.0577 #dCL/dAlpha da asa em deg^-1
eta_ev = 0.8 #Fator de eficiência da empenagem vertical
Cl_alpha_ev = 0.1069 #dCl/dAlfa do perfil da empenagem vertical em deg^-1
ar_asa = 4.66
b = 2.050
b_ft = b * 3.28
s_asa = 2 * ((b**2)/ar_asa) #multiplicando por 2 por causa do biplano
sweep = 0
W = 35 #MTOW EM LBS (16kg)

empenagens_validas = []
lemes_validos = []


cn_beta_desejado = (0.005 * (W/b_ft**2)**(1/2)) #deg^-1
print("desejado", cn_beta_desejado)


corda_raiz_min = 0.15 #Corda na raiz da empenagem vertical
corda_raiz_max = 0.35

corda_ponta_min = 0.15 #Corda na ponta da empenagem vertical
corda_ponta_max = 0.30


enverg_ev_min = 0.25 #Envergadura da empenagem vertical
enverg_ev_max = 0.4
#enverg_ev = 0.495
'''
l_ev_min = 0 #Distância horizontal do CG ao CA da empenagem vertical
l_ev_max = 0
'''
l_ev = 0

cn_beta_min = 0.001 #dCn/dBeta da aeronave completa em deg^-1
cn_beta_max = 1.3 * cn_beta_desejado
print(f'Minimo: %.5f       Máximo: %.5f' %(cn_beta_min, cn_beta_max))

porcentagem_movel_min = 0.2 #Área leme/Area empenagem vertical
porcentagem_movel_max = 0.6

ar_ev_min = 1.5 #razão de alongamento da empenagem vertical
ar_ev_max = 3

deflexao_maxima = 30 #±15º

tau_grafico = [0,0.28, 0.4, 0.51,0.6 ,0.68, 0.72, 0.8]
razao_grafico = [0,0.1 ,0.2 , 0.3,0.4, 0.5,0.6, 0.7]
propAreas = interp1d(razao_grafico, tau_grafico) #Retorna função que tau a partir da relação entre as áreas


def perfil_para_3d(Cl_alpha_ev,ar_ev):
    CLa_ev = Cl_alpha_ev/math.sqrt(1 + (Cl_alpha_ev/(math.pi*ar_ev))**2 + Cl_alpha_ev/(math.pi * ar_ev))
    return CLa_ev


def contribuicao_asa():
    return 0    #-0.0004

def gerar_ev():
    numero = 0
    empenagem_vertical = []
    leme = []
    for corda_raiz in np.arange(corda_raiz_min, corda_raiz_max, 0.01):
        for corda_ponta in np.arange(corda_ponta_min, corda_ponta_max, 0.01):
            for enverg_ev in np.arange(enverg_ev_min, enverg_ev_max, 0.01):
                #l_ev = 0.28715 - 0.75 * corda_raiz
                #corda_ponta = corda_raiz
                l_ev = 0.4875#0.75 - 0.75 * corda_raiz
                empenagem_vertical = []
                leme = []
                s_ev = enverg_ev * ((corda_raiz + corda_ponta)/2)
                ar_ev = enverg_ev**2/s_ev
                v_ev = (l_ev* 2*s_ev)/(s_asa*b)
                lambda_ev = corda_ponta/corda_raiz
                CLa_ev = perfil_para_3d(Cl_alpha_ev, ar_ev)
                cn_beta_ev = v_ev * CLa_ev * (0.724 + 3.06 * (s_ev/s_asa)/(1 + math.cos(sweep)) + 0.009*ar_asa)
                cn_beta_aviao = cn_beta_ev + contribuicao_asa() 
                if cn_beta_aviao > 0 and ar_ev_min <= ar_ev < ar_ev_max and corda_ponta <= corda_raiz and cn_beta_min <= cn_beta_aviao <=cn_beta_max:   
                    #print(cn_beta_aviao) 
                    for porcentagem_movel in np.arange(porcentagem_movel_min, porcentagem_movel_max, 0.01):
                        s_leme = s_ev * porcentagem_movel
                        tau_leme = propAreas(porcentagem_movel)
                        cn_delta_leme = eta_ev * v_ev * CLa_ev * tau_leme * 57.3 #tá em rad^-1
                        print(cn_delta_leme)
                        if 0.1 <= cn_delta_leme <= 0.3:
                                empenagem_vertical.extend([l_ev, corda_raiz, corda_ponta, ar_ev, s_ev, v_ev, cn_beta_ev, cn_beta_aviao, porcentagem_movel,tau_leme, cn_delta_leme, enverg_ev, s_leme])
                                empenagens_validas.append(empenagem_vertical)
                                        
                                
gerar_ev()                  

planilhaEV2021 = xls.Workbook('/Users/ruansantiago/Desktop/Ruan/BlackBird/Códigos/planilhaEV2021.xlsx')

formato_cabecalho = planilhaEV2021.add_format(
    {
        'bg_color': '#9BC2E6',
        'bold': True,
        'border': True
    }
)

formato_dados = planilhaEV2021.add_format(
    {
        'bg_color': '#BDD7EE',
        'border': True
    }
)

abaPlanilha = planilhaEV2021.add_worksheet() #Criando aba da planilha
abaPlanilha.write('A1','l_ev',formato_cabecalho)
abaPlanilha.write('B1','Corda Raiz',formato_cabecalho)
abaPlanilha.write('C1','Corda Ponta',formato_cabecalho)
abaPlanilha.write('D1','AR_EV',formato_cabecalho)
abaPlanilha.write('E1','Área_EV',formato_cabecalho)
abaPlanilha.write('F1','Volume de cauda vertical',formato_cabecalho)
abaPlanilha.write('G1','Cn_beta_leme',formato_cabecalho)
abaPlanilha.write('H1','Cn_beta_avião',formato_cabecalho)
abaPlanilha.write('I1','% Móvel',formato_cabecalho)
abaPlanilha.write('J1','Tau_leme',formato_cabecalho)
abaPlanilha.write('K1','Cn_delta_leme',formato_cabecalho)
abaPlanilha.write('L1','Envergadura',formato_cabecalho)
abaPlanilha.write('M1','Área do leme',formato_cabecalho)
for linha in range(len(empenagens_validas)):
    for coluna in range(13):
        abaPlanilha.write(linha + 1, coluna, empenagens_validas[linha][coluna], formato_dados)
planilhaEV2021.close()
