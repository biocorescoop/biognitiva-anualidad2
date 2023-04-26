#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 10:28:15 2023

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
import pywt

# =============================================================================
# Set working directory
# =============================================================================

os.chdir('/home/miguel/Desktop/Miguel/Curro/Biocore/Supuesto/Scripts/Datos completos/')

# =============================================================================
# Set parameters for plots
# =============================================================================

# General style

plt.style.use(['dark_background'])
plt.rcParams['figure.figsize'] = [33, 22]
plt.rcParams.update({'font.size': 32})

# Use scientific notation on axes

plt.rcParams['axes.formatter.limits'] = -3, 3 # sets range outside which notation is used
plt.rcParams['axes.formatter.use_mathtext'] = True # use x10^n instead of 1en


#%% 2. Pre-process data

# =============================================================================
# Obtain all 16 attributes (data is not sorted yet)
# =============================================================================

header, content = primes_preprocessing(filename = '../../Documentos/Bases/compresion_buenabuena.csv') # this does all the pre-processing for us

header = header[1:] # remove the first attribute (index) so it starts at 'n'

# =============================================================================
# Limit how many rows we are actually using
# =============================================================================
 
# # row_limit = 1000 # max number of rows we are using 
# row_limit = len(content)

# content = content[:row_limit] # this one has all the old and new values

# =============================================================================
# For the x-axis, generate a fake 'time' series to display the data
# =============================================================================

order_series = np.arange(0, len(content))

# =============================================================================
# And define the inputs (n, i, j, k)
# =============================================================================

inputs = [var for var in content[:, 1:6].T] # need to iterate over the transpose of the matrix to get columns instead of rows 

# del content

#%% 3. Continuous Wavelet Transform (CWT) using PyWavelets

# =============================================================================
# Wavelet objects
# =============================================================================

# Let's see what sort of wavelets are in the library first

print('The wavelet objects available in the library are:')
print(pywt.families(short = False))
print('...or:')
print(pywt.families(short = True))

print('We can also see each wavelet in each family:')
for family in pywt.families():

    print("%s family: " % family + ', '.join(pywt.wavelist(family)))

# Now, create a wavelet object using one of the provided ones in the library

wavelet_type = 'morl'

wavelet = pywt.ContinuousWavelet(wavelet_type) # for wavelets that do not allow for DWT
# wavelet = pywt.Wavelet(wavelet_type) # for wavelets that allow for DWT

(psi, x) = wavelet.wavefun(level = 8) # for DWT disallowed
# (phi, psi, x) = wavelet.wavefun(level = 8) # for DWT allowed

# phi is scaling function, psi is wavelet function, level is the level of refinement (how many points are used to characterise the wavelet)

# And plot it to see the one we are using!

fig, axs = plt.subplots()

plt.plot(np.linspace(0, 1, len(psi)), psi, c = 'gold', linewidth = 3)

plt.title('Wavelet de ' + wavelet_type)

plt.legend()
plt.grid(True, alpha = .5)
plt.show()

#%%

# =============================================================================
# And now, compute the CWT
# =============================================================================

# Define the value

value = 'n'

original_series = inputs[header.index(value)]

# And compute

points_to_use = len(original_series)
    
scaling_vector = np.linspace(2, points_to_use, 150) # linear
scaling_vector_log = np.log(scaling_vector) 

coefs, freqs = pywt.cwt(original_series, scales = scaling_vector_log, wavelet = wavelet_type, method = 'fft') 

freq_vec= pywt.scale2frequency(wavelet_type, scaling_vector)

# And plot

print('Plotting...')

fig, ax = plt.subplots()

plt.imshow(np.abs(coefs), aspect = 'auto', cmap = 'gnuplot')

plt.title('CWT de ' + value + ' usando ' + wavelet_type)
plt.xlabel('Progresión del valor')
plt.ylabel('Frecuencia')


# ax.set_yticks(freqs)

ax.set_yticks(np.linspace(0,coefs.shape[0],10),np.round(freq_vec[np.linspace(0, len(scaling_vector)-1, 10).astype(int)], 7))

plt.legend()
# plt.grid(True, alpha = .5)
# plt.show()
plt.savefig(f'../../Gráficas/MEMORIA/Wavelet/wavelet_{value}') 

