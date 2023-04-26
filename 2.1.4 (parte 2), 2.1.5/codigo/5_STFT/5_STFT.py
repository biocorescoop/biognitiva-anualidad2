#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 12:04:35 2023

@author: miguel
"""

#%% 1. Preliminaries

# =============================================================================
# Import modules
# =============================================================================

import numpy as np
from my_functions import * # import from our own script 
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d
from scipy import signal

# =============================================================================
# Set working directory
# =============================================================================

os.chdir('/home/miguel/Desktop/Miguel/Curro/Biocore/Supuesto/Scripts/Datos completos/')

# =============================================================================
# Set parameters for plots
# =============================================================================

plt.style.use(['dark_background'])
plt.rcParams['figure.figsize'] = [33, 22]
plt.rcParams.update({'font.size': 32})

# Use scientific notation on axes

plt.rcParams['axes.formatter.limits'] = -3, 3 # sets range outside which notation is used
plt.rcParams['axes.formatter.use_mathtext'] = True # use x10^n instead of 1e^n

#%% 2. Pre-process data

# =============================================================================
# Obtain all 16 attributes (data is not sorted yet)
# =============================================================================

attribute = None

header, content = primes_preprocessing(filename = '../../Documentos/Bases/compresion_buenabuena.csv', sorts = attribute) # this does all the pre-processing for us

header = header[2:] # remove the first attribute (index) so it starts at 'n'

# =============================================================================
# Limit how many rows we are actually using
# =============================================================================
 
# row_limit = 1000 # max number of rows we are using 
# row_limit = len(content)

# content = content[:row_limit] # this one has all the old and new values

# =============================================================================
# For the x-axis, generate a fake 'time' series to display the data
# =============================================================================

order_series = np.arange(0, len(content))

# =============================================================================
# And define the inputs (n, i, j, k)
# =============================================================================

inputs = [var for var in content[:, 2:6].T] # need to iterate over the transpose of the matrix to get columns instead of rows 

spectrum = content[:, 8] # separates index of data by original (0) or extended (1) spectrum

del content

# =============================================================================
# Also, define only original spectrum
# =============================================================================

inputs_original = [inputs[val][np.where(spectrum == 0)[0]][:-843] for val in range(len(inputs))] # we remove last element bc the number of elements of original series is prime (xd)
order_series_original = np.arange(0, len(inputs_original[0]))

#%% 3. Plot distribution

# =============================================================================
# Define attribute to use
# =============================================================================

value = 'k'

series = inputs[header.index(value)]
series_original = inputs_original[header.index(value)]

# =============================================================================
# First visualise distribution in order to get an idea for windows and their length
# =============================================================================

fig, axs = plt.subplots()

plt.scatter(order_series, series, marker = '.', c = 'firebrick')

plt.title('Distribución de los valores de ' + value)
plt.xlabel('Progresión del valor')
plt.ylabel(value)

# plt.xlim(15000, 15200)

plt.legend()
plt.grid(True, alpha = .3)
plt.show()


fig, axs = plt.subplots()

plt.scatter(order_series_original, series_original, marker = '.', c = 'firebrick')

plt.title('Distribución de los valores originales de ' + value)
plt.xlabel('Progresión del valor')
plt.ylabel(value)

# plt.xlim(15000, 15200)

plt.legend()
plt.grid(True, alpha = .3)
plt.show()
 
#%% 4. Short Time Fourier Transform (STFT)

# =============================================================================
# Define parameters
# =============================================================================

window_length = len(series) // 42.5 # length of window. To choose it we find divisors (twice of window length needs to be divisor of length of series)
window_length_original = len(series_original) // 20

# =============================================================================
# And compute
# =============================================================================

sample_frequencies, segment_times, STFT = signal.stft(
    
                                                      series,
                                                      fs = 1,                   # sampling frequency
                                                      # scaling = 'psd',      # spectrum allows 
                                                      window = 'boxcar',        # type of window to use
                                                      nperseg = window_length,  # length of window segment
                                                      noverlap = None,          # amount to overlap by (None is nperseg // 2)
                                                      nfft = None,              # amount to zero-pad by the FFT on either side if desired
                                                      padded = True           # pads with zeros at end to make fit by window length
                                                            
                                                      )


sample_frequencies_original, segment_times_original, STFT_original = signal.stft(
    
                                                      series_original,
                                                      fs = 1,                   # sampling frequency
                                                      # scaling = 'psd',      # spectrum allows
                                                      window = 'boxcar',        # type of window to use
                                                      nperseg = window_length_original,  # length of window segment
                                                      noverlap = None,          # amount to overlap by (None is nperseg // 2)
                                                      nfft = None,              # amount to zero-pad by the FFT on either side if desired
                                                      padded = True            # pads with zeros at end to make fit by window length
                                                        
                                                      )

# =============================================================================
# Let's plot things in 2D
# =============================================================================

# Set a couple parameters

# window = signal.windows.boxcar(int(window_length), sym = True)    

# And plot

fig, ax = plt.subplots()

fig.tight_layout(pad = 4) # adjusts spacing of subplots

# spectrogram = plt.imshow(np.abs(STFT), cmap = 'gnuplot', origin='lower', aspect='auto', interpolation='none')
spectrogram = plt.pcolormesh(segment_times, sample_frequencies, np.abs(STFT), cmap = 'gnuplot', shading = 'auto')
cbar = fig.colorbar(spectrogram)
cbar.set_label('Intensidad', rotation = 90)
plt.title(f'STFT de los valores completos de {value}')
plt.xlabel('Progresión (equivalente a tiempo)')
plt.ylabel('Frecuencia')
# plt.xlim(2500, 2600)
# plt.ylim(0, .05)
# plt.legend()
# plt.grid(True, alpha = .5)

# plt.show()
plt.savefig(f'../../Gráficas/MEMORIA/STFT/stft_completos_{value}')

fig, ax = plt.subplots()

fig.tight_layout(pad = 4) # adjusts spacing of subplots

# spectrogram = plt.imshow(np.abs(STFT), cmap = 'gnuplot', origin='lower', aspect='auto', interpolation='none')
spectrogram_original = plt.pcolormesh(segment_times_original, sample_frequencies_original, np.abs(STFT_original), cmap = 'gnuplot', shading = 'auto')
cbar = fig.colorbar(spectrogram_original)
cbar.set_label('Intensidad', rotation = 90)
plt.title(f'STFT de los valores incompletos de {value}')
plt.xlabel('Progresión (equivalente a tiempo)')
plt.ylabel('Frecuencia')
# plt.xlim(2500, 2600)
# plt.ylim(0, .05)
# plt.legend()
# plt.grid(True, alpha = .5)

# plt.show()
plt.savefig(f'../../Gráficas/MEMORIA/STFT/stft_incompletos_{value}')


#%% 5. Inverse STFT

# # =============================================================================
# # First, let's find a threshold to get
# # =============================================================================

# threshold_rows = (sample_frequencies > .124) & (sample_frequencies < .126) # just the first dimension
# threshold = np.tile(threshold_rows, (len(segment_times), 1)).T # full matrix of trues and falses
# threshold_inverse = np.invert(threshold) # also get the inverse for plotting purposes

# stft_clean = np.abs(STFT) * threshold
# stft_clean_inverse = np.abs(STFT) * threshold_inverse # has zeroes
# stft_clean_inverse[stft_clean_inverse == 0] = 'nan' # turn to nans for plot

# del threshold_rows, threshold, threshold_inverse # not needed anymore

# # =============================================================================
# # Plot it
# # =============================================================================

# fig, ax = plt.subplots()

# fig.tight_layout(pad = 4) # adjusts spacing of subplots

# thresholded = plt.pcolormesh(segment_times, sample_frequencies, stft_clean, cmap = 'gnuplot', shading = 'auto', alpha = 1)
# spectrogram = plt.pcolormesh(segment_times, sample_frequencies, stft_clean_inverse, cmap = 'binary', shading = 'auto', alpha = 1)
# cbar = fig.colorbar(thresholded)
# cbar.set_label('Intensidad', rotation = 90)
# # plt.pcolormesh(segment_times, sample_frequencies, np.abs(STFT), cmap = 'gnuplot', vmin = 0, vmax = .5e3, shading = 'auto')
# plt.title('STFT')
# plt.xlabel('Progresión (equivalente a tiempo)')
# plt.ylabel('Frecuencia')
# # plt.xlim(2500, 2600)
# # plt.ylim(0, .05)
# # plt.legend()
# # plt.grid(True, alpha = .5)

# plt.show()

# # =============================================================================
# # Now, let's get to computing the iSTFT
# # =============================================================================

# _, iSTFT = signal.istft(stft_clean, fs = 1, window = 'boxcar', nperseg = window_length, noverlap = None) # first variable is _ (throwaway) bc it gives us a time series, which we already have

# # =============================================================================
# # And plot it
# # =============================================================================

# fig, ax = plt.subplots()

# plt.plot(order_series, iSTFT, c = 'firebrick')
# plt.plot(order_series, iSTFT, '.', c = 'whitesmoke')
# plt.plot(order_series, series, '.', c = 'gold')

# plt.title('iSTFT')
# plt.xlabel('Progresión del valor')
# plt.ylabel(value)

# # plt.xlim(15000, 15300)

# plt.legend()
# plt.grid(True, alpha = .5)
# fig.tight_layout(pad = 4)
# plt.show()

#%% 3D

# =============================================================================
# Create the meshgrid
# =============================================================================

times_3d, frequencies_3d = np.meshgrid(segment_times, sample_frequencies)

# =============================================================================
# ...and in 3D
# =============================================================================

fig = plt.figure()
ax = plt.axes(projection = '3d') # tells us to do a 3d plot
surface = ax.plot_surface(times_3d, frequencies_3d, np.abs(STFT), cmap = 'inferno')
# ax.scatter(times_3d, frequencies_3d, np.abs(STFT), c = np.abs(STFT), cmap = 'inferno')
# ax.plot(segment_times, sample_frequencies, np.abs(iSTFT))

fig.colorbar(surface, shrink=.5, aspect=10)
# ax.plot_surface(segment_times[None, :], sample_frequencies[:, None], np.abs(STFT), cmap = 'inferno')


# ax.set_ylim3d(bottom = .1, top = .2)

ax.set_xlabel('Progresión (equivalente a tiempo)', labelpad = 30)
ax.set_ylabel('Frecuencia', labelpad = 30)
ax.set_zlabel('Amplitud', labelpad = 30)


plt.title(f'Representación 3D de la STFT de {value}')
# ax.tick_params(axis='both', which='major', pad=50)

# ax.view_init(30, -90) # change rotation

# plt.show()
plt.savefig(f'../../Gráficas/MEMORIA/STFT/stft_3D_{value}')




# =============================================================================
# Cosas para el 3D
# =============================================================================

#%%

# indices = np.where((sample_frequencies < .13) & (sample_frequencies > .12))[0] # what frequency to plot

# test = np.full((1, len(segment_times)), sample_frequencies[indices[0]])


# fig, ax = plt.subplots()

# plt.pcolormesh(segment_times, sample_frequencies, np.abs(STFT), vmin = 0, vmax = .5e3, shading = 'auto')
# plt.plot(segment_times, test[0], 'firebrick')
# plt.title('STFT')
# plt.xlabel('Progresión (equivalente a tiempo)')
# plt.ylabel('Frecuencia')
# # plt.xlim(2500, 2600)
# plt.ylim(0.120, .130)
# plt.legend()
# # plt.grid(True, alpha = .5)

# plt.show()



# plt.plot(segment_times, np.abs(STFT[1, :]), '.-')
