    
""" Código con el factor de onda longitudinal"""

import numpy as np
import pandas as pd
import cmath

# Parámetros del sistema
voltajes = np.arange(1, 5, 1)
diametros_bobina = np.arange(0.05, 0.20, 0.05)
Z_load_values = np.arange(100, 5001, 100)  # Impedancia de carga en ohmios
frecuencia = 4.011e6  # Frecuencia en Hz
R1 = 367  # Impedancia de la antena generadora en ohmios
tiempo = 1  # Tiempo en segundos
n_receptores = 2  # Cantidad de receptores
phi = np.deg2rad(95)  # Ángulo de fase en radianes

# Coeficiente de reflexión
def coeficiente_reflexion(Z_load, Z_antena):
    return (Z_load - Z_antena) / (Z_load + Z_antena)

def onda_longitudinal_factor(phi, P_con_carga, P_sin_carga):
    if P_sin_carga == 0:
        return 0
    return (1 + np.sin(phi)**2) * P_con_carga / P_sin_carga

def calcular_potencial_escalar(voltaje, Z_load, R1, frecuencia, phi):
    # Constante de proporcionalidad
    c = 299792458  # Velocidad de la luz en m/s
    k = 2 * np.pi * frecuencia / c
    
    # Longitud del dipolo eléctrico
    l = 0.5 * c / frecuencia
    
    # Corriente que circula por la antena
    Z_antena = np.sqrt(R1 * Z_load)
    I = voltaje / Z_antena
    
    # Distancia al punto arbitrario
    r = 1  # En unidades arbitrarias
    
    # Potencial escalar en el punto arbitrario
    V = -k * I * l * np.cos(phi) / r
    
    return V

def calcular_potencias(voltaje, Z_load, R1, frecuencia, n_receptores, phi):
    # Coeficiente de reflexión
    gamma = coeficiente_reflexion(Z_load, R1)

    # Potencia sin carga (corregido)
    P_sin_carga = (1 - np.abs(gamma)**2)

    # Potencia con carga (corregido) teniendo en cuenta el ángulo phi
    P_con_carga = ((1 - np.abs(gamma)**2) / (1 + np.abs(gamma)**2)) * n_receptores * np.cos(phi)**2

    # Energía consumida por las resistencias sin carga
    energia_sin_carga = P_sin_carga * tiempo

    # Corriente que circula por las resistencias sin carga
    I_sin_carga = np.sqrt(P_sin_carga / R1)

    # Energía consumida por las resistencias con carga
    energia_con_carga = P_con_carga * tiempo

    # Corriente que circula por las resistencias con carga
    I_con_carga = np.sqrt(P_con_carga / R1)

    # Trabajo realizado por las resistencias
    trabajo_resistencias = (I_sin_carga**2 - I_con_carga**2) * R1 * tiempo

    # Factor de onda longitudinal
    long_factor = onda_longitudinal_factor(phi, P_con_carga, P_sin_carga)

    # Potencial escalar
    potencial_escalar = calcular_potencial_escalar(voltaje, Z_load, R1, frecuencia, phi)

    # Ajuste del voltaje del emisor y los receptores de acuerdo con la carga en el sistema
    voltaje_ratio = P_con_carga / P_sin_carga
    voltaje_emisor_ajustado = voltaje * (1 - long_factor)
    voltaje_receptor_ajustado = voltaje * long_factor

    return P_sin_carga, P_con_carga, voltaje_ratio, voltaje_emisor_ajustado, voltaje_receptor_ajustado, potencial_escalar, trabajo_resistencias

resultados = []

for voltaje in voltajes:
    for diametro_bobina in diametros_bobina:
        for Z_load in Z_load_values:
            P_sin_carga, P_con_carga, voltaje_ratio, voltaje_emisor_ajustado, voltaje_receptor_ajustado, potencial_escalar, trabajo_resistencias = calcular_potencias(voltaje, Z_load, R1, frecuencia, n_receptores, phi)
            coef_reflexion = coeficiente_reflexion(Z_load, R1)
            energia_sin_carga = P_sin_carga * tiempo
            energia_con_carga = P_con_carga * tiempo
            consumo_sin_carga = P_sin_carga * tiempo
            consumo_con_carga = P_con_carga * tiempo
            mejor_potencial_y_consumo = (P_con_carga < P_sin_carga) and (consumo_con_carga < consumo_sin_carga)
            trabajo_resistencias = energia_sin_carga - (energia_con_carga - energia_sin_carga)
          
            resultados.append((voltaje, potencial_escalar, diametro_bobina, Z_load, coef_reflexion, consumo_sin_carga, consumo_con_carga, mejor_potencial_y_consumo, trabajo_resistencias))

# Crear un DataFrame con los resultados
columnas = ["Voltaje (V)", "Potencial escalar (V)", "Diámetro bobina (cm)", "Impedancia carga (ohmios)", "Coef. Reflexión", "Consumo sin carga (J)", "Consumo con carga (J)", "Mejor potencial y consumo", "Trabajo resistencias (J)"]
df_resultados = pd.DataFrame(resultados, columns=columnas)
df_resultados.to_csv('resultados.csv', index=False)


# Mostrar el DataFrame
display(df_resultados)