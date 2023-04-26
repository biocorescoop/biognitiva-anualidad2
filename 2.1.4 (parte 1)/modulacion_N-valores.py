import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import scipy.io.wavfile as wavfile
import soundfile as sf
from google.colab import files
import IPython.display as ipd


def normalize_values(values, min_output, max_output):
    min_value = min(values)
    max_value = max(values)
    return [min_output + (max_output - min_output) * (value - min_value) / (max_value - min_value) for value in values]

def generate_sin_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sin_wave = np.sin(freq * 2 * np.pi * t)
    return sin_wave

entropy_values = np.array([0.993233,1.562422,1.970693,2.278923,2.531461,2.742013,2.921626,3.079222,3.218745,3.343367,3.456308,3.559574,3.654328,3.741855,3.823200,3.899145])  # Tus valores de entropía
fractal_dimension_values = np.array([0.82352,0.803469,0.849336,0.842885,0.859618,0.864349,0.868156,0.874901,0.879378,0.882840,0.887097,0.891164,0.894360,0.897460,0.900485,0.903314])  # Tus valores de dimensión fractal

min_freq = 20
max_freq = 20000

normalized_entropy_values = normalize_values(entropy_values, min_freq, max_freq)
normalized_fractal_dimension_values = normalize_values(fractal_dimension_values, min_freq, max_freq)

duration = 100  # Duración de cada frecuencia en segundos
sampling_rate = 44100  # Tasa de muestreo
t = np.linspace(0, duration, duration * sampling_rate, endpoint=False)


audio_entropy = np.zeros(0)
audio_fractal_dimension = np.zeros(0)

for freq in normalized_entropy_values:
    sin_wave = generate_sin_wave(freq, duration, sampling_rate)
    audio_entropy = np.concatenate((audio_entropy, sin_wave))

for freq in normalized_fractal_dimension_values:
    sin_wave = generate_sin_wave(freq, duration, sampling_rate)
    audio_fractal_dimension = np.concatenate((audio_fractal_dimension, sin_wave))

print("Señal de audio basada en entropía (primeras 10 muestras):")
print(audio_entropy[:100])

print("\nSeñal de audio basada en dimensión fractal (primeras 10 muestras):")
print(audio_fractal_dimension[:100])

"""
# Parámetros de las señales
num_samples = len(entropy_values)
time = np.arange(num_samples)

# Generar la señal modulante (entropía)
modulating_signal = entropy_values

# Generar la señal portadora (dimensión fractal)
carrier_signal = fractal_dimension_values

# Generar la señal modulada (AM)
modulated_signal = (carrier_signal * modulating_signal) + carrier_signal

# Señal portadora (entropía)
#carrier_signal = audio_entropy

# Señal modulante (dimensión fractal)
#modulating_signal = audio_fractal_dimension

# Normalizar la señal modulante
#modulating_signal = (modulating_signal - np.min(modulating_signal)) / (np.max(modulating_signal) - np.min(modulating_signal))

# Parámetro de modulación (índice de modulación)
#modulation_index = 0.5
# Valores de entropía y dimensión fractal

#entropy_values = np.array([3.5, 3.7, 3.2, 3.6, 3.1, 3.8, 3.9, 3.4])
#fractal_dimension_values = np.array([1.5, 1.4, 1.6, 1.55, 1.45, 1.35, 1.65, 1.7])

# Parámetros de las señales
duration = 5
sampling_rate = 1000
time = np.linspace(0, duration, duration * sampling_rate)

# Generar la señal modulante (entropía)
modulating_freqs = np.linspace(1, 10, len(entropy_values))
modulating_signal = np.zeros_like(time)

for amp, freq in zip(entropy_values, modulating_freqs):
    modulating_signal += amp * np.sin(2 * np.pi * freq * time)

# Generar la señal portadora (dimensión fractal)
carrier_freqs = np.linspace(20, 100, len(fractal_dimension_values))
carrier_signal = np.zeros_like(time)

for amp, freq in zip(fractal_dimension_values, carrier_freqs):
    carrier_signal += amp * np.sin(2 * np.pi * freq * time)

# Generar la señal modulada (AM)
modulated_signal = (carrier_signal * modulating_signal) + carrier_signal
"""

"""
# Parámetros de las señales
duration = 5
sampling_rate = 1000
time = np.linspace(0, duration, duration * sampling_rate)

# Generar la señal modulante (entropía)
modulating_signal = np.mean(entropy_values) * np.sin(2 * np.pi * 5 * time)

# Generar la señal portadora (dimensión fractal)
carrier_signal = np.mean(fractal_dimension_values) * np.sin(2 * np.pi * 50 * time)

# Generar la señal modulada (AM)
modulated_signal = (carrier_signal * (1 + modulating_signal))
"""
# Señal modulante
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
modulating_freq = np.interp(t, np.linspace(0, duration, len(entropy_values)), entropy_values + fractal_dimension_values)
modulating_signal = np.sin(2 * np.pi * modulating_freq * t)

# Señal portadora
carrier_frequency = 440  # Frecuencia de la señal portadora en Hz (la nota A4)
carrier_signal = np.sin(2 * np.pi * carrier_frequency * t)

# Generar la señal modulada (AM)
modulated_signal = (carrier_signal * modulating_signal) + carrier_signal

print("Señal modulada (primeras 100 muestras):")
print(modulated_signal[:100])

num_samples = len(modulated_signal)
time = np.linspace(0, duration, num_samples)

# Limitar el rango de tiempo para visualizar mejor las señales sinusoidales
time_limit = 0.1

# Visualizar la señal modulada con la señal portadora y modulante en el mismo gráfico
plt.figure(figsize=(12, 4))
plt.plot(time[:100000], modulated_signal[:100000], label='Señal modulada (AM)')
plt.plot(time[:100000], carrier_signal[:100000], label='Señal portadora', linestyle='--', alpha=0.5)
plt.title("Señal modulada AM con señal portadora")
plt.xlabel("Tiempo (s)")
plt.legend()
plt.show()

# Visualizar la señal portadora
plt.figure(figsize=(12, 4))
plt.plot(time[:1000], carrier_signal[:1000])
plt.title("Señal portadora")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.show()

# Visualizar la señal modulante
plt.figure(figsize=(12, 4))
plt.plot(time[:1000], carrier_signal[:1000])
plt.title("Señal modulante")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.show()

# Visualizar la señal modulada
plt.figure(figsize=(12, 4))
plt.plot(time[:1000], carrier_signal[:1000])
plt.title("Señal modulada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.show()

sr = 44100  # Sample rate
# Guardar las señales como archivos .wav
sf.write('modulating_signal1.wav', modulating_signal, sampling_rate, subtype='PCM_24')
sf.write('carrier_signal1.wav', carrier_signal, sampling_rate, subtype='PCM_24')
sf.write('modulated_signal1.wav', modulated_signal, sampling_rate, subtype='PCM_24')

# Guardar la señal portadora en un archivo WAV
sf.write('carrier_signal.wav', carrier_signal, sr, subtype='PCM_16')

# Guardar la señal modulante en un archivo WAV
sf.write('modulating_signal.wav', modulating_signal, sr, subtype='PCM_16')

# Guardar la señal modulada en un archivo WAV
sf.write('modulated_signal.wav', modulated_signal, sr, subtype='PCM_16')

# Reproducir los archivos de audio en Colab

print("Señal modulante:")
ipd.display(ipd.Audio('modulating_signal1.wav'))

print("Señal portadora:")
ipd.display(ipd.Audio('carrier_signal1.wav'))

print("Señal modulada:")
ipd.display(ipd.Audio('modulated_signal1.wav'))
"""
files.download('modulating_signal.wav')
files.download('carrier_signal.wav')
files.download('modulated_signal.wav')
"""
