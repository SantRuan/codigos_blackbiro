import numpy as np
import math
from scipy.interpolate import interp1d
import xlsxwriter as xls

tau_grafico = [0,0.28, 0.4, 0.51,0.6 ,0.68, 0.72, 0.8]
razao_grafico = [0,0.1 ,0.2 , 0.3,0.4, 0.5,0.6 ,0.7]
propAreas = interp1d(razao_grafico, tau_grafico) #Retorna função que dá tau a partir da relação entre as áreas

s_eh = 0.385
CLa_eh = 0.0573
eta_eh = 0.9
vh = 0.39

deflexao_maxima = math.radians(40)

porc_movel_min = 0.35
porc_movel_max = 0.45

cm_delta_profundor_min = -1
cm_delta_profundor_max = -0.5


def gerar_profundor():
    for porcentagem_movel in np.arange(porc_movel_min, porc_movel_max, 0.01):
        s_profundor = porcentagem_movel * s_eh
        tau = propAreas(porcentagem_movel)
        cm_delta_profundor = (-vh) * eta_eh * CLa_eh * tau *57.3 #ISSO AQUI TÁ EM RAD^-1 
        if cm_delta_profundor_min <= cm_delta_profundor <= cm_delta_profundor_max:
            print(porcentagem_movel*100,'%', cm_delta_profundor, s_profundor)

gerar_profundor()

