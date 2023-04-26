#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:31:52 2023

@author: miguel
"""

#%% 1. Preliminaries

# =============================================================================
# Import modules
# =============================================================================

from my_functions import * # import from our own script
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from scipy import interpolate

# =============================================================================
# Set working directory
# =============================================================================

os.chdir('/home/miguel/Desktop/Miguel/Curro/Biocore/Supuesto/Scripts/Datos completos/')

# =============================================================================
# Set parameters
# =============================================================================

plot_parameters()

#%% 2. Pre-process data

# =============================================================================
# Obtain all 16 attributes (data is not sorted yet)
# =============================================================================

attr = None
header, content = primes_preprocessing(filename = '../../Documentos/Bases/compresion_buenabuena.csv', sorts = attr) # this does all the pre-processing for us
del attr

header = header[2:6] # get only n, i, j, k

# =============================================================================
# For the x-axis, generate a fake 'time' series to display the data
# =============================================================================

order_series = np.arange(0, len(content))

# =============================================================================
# And define the inputs (vectors and free variables, that is)
# =============================================================================

inputs = np.array([var for var in content[:, 2:6].T]) # need to iterate over the transpose of the matrix to get columns instead of rows 

del content 

# =============================================================================
# Decide the attribute to use
# =============================================================================

attribute = 'i'

original_series = inputs[header.index(attribute)]

del inputs

# =============================================================================
# Also get the interpolated data
# =============================================================================

order_series_intrpld, original_series_interpld = dict.values(cubic_spline_interpolation(order_series, 
                                                                                        original_series, 
                                                                                        fs = .125, 
                                                                                        bc_type = 'clamped'))

#%% 3. FFT

# =============================================================================
# Perform the FFT
# =============================================================================

series = original_series

freq, yhat, PSD = dict.values(fastFourierTransform(series, attribute))

# =============================================================================
# Let's obtain and denoise the phase
# =============================================================================

yhat_denoised = yhat.copy()

# Now detetect noise (very small numbers) and ignore them

threshold_denoised = np.max(np.abs(yhat)) / 4 # tolerance threshold

yhat_denoised[np.abs(yhat_denoised) < threshold_denoised] = 0 # mask out values below the threshold

phase = np.angle(yhat_denoised, deg = False) # False = radians, True = degrees

L = np.arange(0, np.floor(len(series) / 2), dtype = 'int')


# =============================================================================
# And plot
# =============================================================================

plot_parameters()

fig, axs = plt.subplots()

# fig.tight_layout(pad = 4) # adjusts spacing of subplots

plt.title('Espectro de ' + attribute)
plt.xlabel('Frecuencia')
plt.ylabel('Intensidad')

plt.plot(freq[L], PSD[L], c = 'firebrick')

limx = 1 / 8
plt.xlim(limx - .005, limx + .005)
plt.ylim(-.2e5, .7e6)

# plt.legend()
plt.grid(True, alpha = .3)
plt.show()

del fig, axs

#%% Cositas simetría

# PSD_entero = (yhat * np.conj(yhat) / len(series))

rango_puntos = 100

ind_simetrico_1 = len(PSD)//8
ind_simetrico_2 = len(PSD) - ind_simetrico_1

PSD_simetr=PSD.copy()

PSD_simetr[ind_simetrico_1 - rango_puntos: ind_simetrico_1 ]=PSD_simetr[ind_simetrico_1+1:ind_simetrico_1+ rango_puntos+1][::-1] # igualar parte izquierda con derecha
PSD_simetr[ind_simetrico_2+1:ind_simetrico_2+ rango_puntos+1]= PSD_simetr[ind_simetrico_2 - rango_puntos: ind_simetrico_2][::-1] # igualar parte derecha con izquierda


yhat_norm = yhat * np.sqrt(PSD) / np.sqrt(PSD_simetr)

L = np.arange(0, np.floor(len(series) / 2), dtype = 'int')

# =============================================================================
# Y ahora hacemos la inversa
# =============================================================================

peak_indices = (PSD > 0) & ((freq > .12) & (freq < .13))

# PSD_clean_sim, ffilt_sim = dict.values(cleanSignal(yhat_norm, PSD_simetr, peak_indices))
PSD_clean, ffilt = dict.values(cleanSignal(yhat, PSD, peak_indices))


# =============================================================================
# And plot
# =============================================================================

plot_parameters()

fig, axs = plt.subplots(3, 1)

fig.tight_layout(pad = 4) # adjusts spacing of subplots

plt.sca(axs[0])

plt.title(f'Distribución de {attribute} completada')
plt.xlabel('Progresión del valor', fontsize = 20)
plt.ylabel(f'{attribute}', fontsize = 20)
plt.scatter(order_series, original_series, marker = '.', c = 'steelblue')
plt.grid(alpha = .3)
plt.legend()

plt.sca(axs[1])
plt.title(f'Densidad espectral de {attribute}')
plt.xlabel('Frecuencia')
plt.ylabel('Densidad')
plt.plot(freq[L], PSD[L], c = 'firebrick', linewidth = 2, label = 'Ruido')
plt.plot(freq[L], PSD_clean[L], c = 'whitesmoke', linewidth = 1.5, label = 'Señal')
# plt.xlim(freq[L[0]], freq[L[-1]])
# plt.xlim(.124, .126)
plt.ylim(0, 1e6)
plt.grid(True, alpha = .3)
# plt.legend()

plt.sca(axs[2])
plt.title('Señal filtrada')
plt.xlabel('Progresión')
plt.ylabel('n')
plt.scatter(order_series, original_series * 2, marker = '.', c = 'firebrick', label = 'Señal ruidosa')
plt.plot(order_series, ffilt, c = 'whitesmoke', linewidth = 1, label = 'Señal filtrada')
# plt.scatter(order_series, ffilt, c = 'whitesmoke', marker = '.', label = 'Señal filtrada')
# plt.xlim(freq[L[0]], freq[L[-1]])
plt.grid(True, alpha = .3)
plt.legend()

plt.show()

#%% distancia entre puntos

fig = plt.figure()

distancia_puntos = np.abs(original_series*2 - np.real(ffilt_sim))

plot_parameters()

plt.title('Diferencia entre la señal sacada de la simetría y la original, punto por punto')
plt.xlabel('Progresión')
plt.ylabel('Diferencia absoluta')

plt.plot(distancia_puntos, '.', c = 'gold')
plt.grid(alpha = .3)
plt.show()

puntos_buenos = (np.where(distancia_puntos < .5))[0]

print(len(puntos_buenos))

#%%

plot_parameters()

fig = plt.figure()

plt.plot(freq, PSD_simetr, c = 'firebrick')

plt.title(f'Densidad espectral de {attribute}')
plt.xlabel('Frecuencia')
plt.ylabel('Densidad')

plt.xlim(.120, .130)
plt.ylim(-1e4, 3.5e5)

plt.grid(alpha = .3)

plt.show()

#%% quitar puntos pequeños

# PSD_peq = np.sort(PSD)[:100]

# PSD_sin_peq[np.where(PSD == PSD_peq)[0]] = 0

PSD_sort = np.sort(PSD)

clean2=PSD>PSD_sort[100]
PSD_clean2=PSD*clean2

# =============================================================================
# Plot
# =============================================================================
fig = plt.figure()

plt.plot(PSD_clean2)

#%%

"""

DE AQUÍ PARA ABAJO ES TODO CÓDIGO RÁPIDO PARA LA MEMORIA. CONTINUAR DESDE ARRIBA HACIENDO CÓDIGO LIMPIO

"""

# # =============================================================================
# # Use peaks in PSD to filter out noise and isolate signal
# # =============================================================================


# yhat_pocha = np.fft.fft(original_series, len(original_series))
# PSD_poch = yhat_pocha * np.conj(yhat_pocha) / len(original_series)

# indices = PSD > 2e6
# indices_poch = PSD_poch > 2e6


# PSDclean = PSD * indices # zeroes out all indices with smaller Fourier coefficients, keeps only with power greater than specified
# PSDclean_poch = PSD_poch * indices_poch # zeroes out all indices with smaller Fourier coefficients, keeps only with power greater than specified

# yhat_clean = indices_poch * yhat_pocha
# ffilt = np.fft.ifft(yhat_clean) # Inverse FFT for filtered time signal

# # =============================================================================
# # And plot
# # =============================================================================

# fig, axs = plt.subplots(3, 1)

# fig.tight_layout(pad = 4) # adjusts spacing of subplots

# plt.sca(axs[0])

# plt.title('Distribución de n')
# plt.xlabel('Progresión del valor', fontsize = 20)
# plt.ylabel('n', fontsize = 20)
# plt.scatter(order_series, original_series, marker = '.', c = 'firebrick')
# plt.grid(alpha = .3)
# plt.legend()

# plt.sca(axs[1])
# plt.title('Densidad espectral de n')
# plt.xlabel('Frecuencia')
# plt.ylabel('Densidad')
# plt.plot(freq, PSD, c = 'firebrick', linewidth = 2, label = 'Ruido')
# plt.plot(freq, PSDclean, c = 'whitesmoke', linewidth = 1.5, label = 'Señal')
# # plt.xlim(freq[L[0]], freq[L[-1]])
# # plt.xlim(.124, .126)
# # plt.ylim(0, 1e5)
# plt.grid(True, alpha = .3)
# plt.legend()

# plt.sca(axs[2])
# plt.title('Señal filtrada')
# plt.xlabel('Progresión')
# plt.ylabel('n')
# plt.scatter(order_series, original_series, marker = '.', c = 'firebrick', label = 'Señal ruidosa')
# plt.plot(order_series, ffilt, c = 'whitesmoke', linewidth = 1, label = 'Señal filtrada')
# # plt.scatter(order_series, ffilt, c = 'whitesmoke', marker = '.', label = 'Señal filtrada')
# # plt.xlim(freq[L[0]], freq[L[-1]])
# plt.grid(True, alpha = .3)
# plt.legend()

# plt.show()
