

# Importar las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt

# Definir las constantes del problema
P_em_max = 1 # Potencia máxima emitida por el emisor (arbitraria)
mu_0 = 4 * np.pi * 1e-7 # Permeabilidad magnética del vacío
epsilon_0 = 8.85e-12 # Permitividad eléctrica del vacío
A = 1 # Amplitud de la onda (arbitraria)
r = 0.1 # Radio del cilindro (arbitrario)
h = 0.2 # Altura del cilindro (arbitrario)

# Definir las funciones k y k
def k(P_em_max, mu_0, epsilon_0, omega, A, r, h):
    # Potencia máxima emitida por el emisor en función de los parámetros de la onda electromagnética longitudinal y del medio material
    return -P_em_max * mu_0 * epsilon_0 * omega / (A ** 2 * np.pi * r ** 2 * h)

def k_(A, epsilon_0, mu_0, omega):
    # Número de onda de la onda longitudinal deducido a partir de las ecuaciones de Maxwell
    return -mu_0 * epsilon_0 * omega * (1 + mu_0 * epsilon_0) / 8

# Crear un array de valores de omega (frecuencia angular) entre 0 y 10
omega = np.linspace(0, 10, 100)

# Calcular los valores de k y k para cada valor de omega
k_values = k(P_em_max, mu_0, epsilon_0, omega, A, r, h)
k__values = k_(A, epsilon_0, mu_0, omega)

# Calcular el coeficiente de correlación entre k y k usando numpy
corr = np.corrcoef(k_values, k__values)[0][1]

# Mostrar el coeficiente de correlación
print(f"El coeficiente de correlación entre k y k es {corr:.2f}")

# Crear una figura con matplotlib para mostrar la gráfica de k y k en función de omega
plt.figure()
plt.plot(omega, k_values, label="k")
plt.plot(omega, k__values, label="k'")
plt.xlabel("omega")
plt.ylabel("k")
plt.legend()
plt.title(f"Correlación entre k y k: {corr:.2f}")
plt.show()