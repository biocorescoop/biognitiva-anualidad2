import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numba import jit
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def agrupar_valores_logaritmicos(n_valores, num_grupos):
    n_min = np.min(n_valores)
    n_max = np.max(n_valores)
    limites = np.logspace(np.log10(n_min), np.log10(n_max), num_grupos + 1)
    indices_grupos = np.digitize(n_valores, limites)
    return indices_grupos, limites


# Función lineal para el ajuste
def linear(x, m, b):
    return m * x + b

def ajuste_lineal(x, m, b):
    return m * x + b

def Q(n, k):
    if n % k == 0:
        return P(n, k)
    else:
        return 0

def P(n, k):
    count = 0
    while n % k == 0:
        count += 1
        n = n // k
    return count

def R(n, k):
    return Q(n, k)

def criba_fractal_subrange(start, end):
    L = []
    i = start
    while i <= end:
        flag = True
        for k in range(2, i):
            if R(i, k) != 0:
                flag = False
                break
        if flag:
            L.append(i)
        i += 1
    return L

def criba_fractal_parallel(n, num_threads=8):
    chunk_size = n // num_threads

    primos = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(criba_fractal_subrange, i * chunk_size + 1, (i + 1) * chunk_size) for i in range(num_threads)]

        for future in futures:
            primos.extend(future.result())

    return primos

def relacion_primos_n_parallel(n):
    primos = criba_fractal_parallel(n)
    cantidad_primos = len(primos)
    relacion = cantidad_primos / n
    return relacion

def calcular_probabilidades(relaciones):
    total_relaciones = sum(relaciones)
    probabilidades = [relacion / total_relaciones for relacion in relaciones]
    return probabilidades

def calcular_entropia(probabilidades):
    entropia = 0
    for probabilidad in probabilidades:
        if probabilidad != 0:
            entropia -= probabilidad * np.log2(probabilidad)
    return entropia

n_valores = [10, 17, 31, 56, 100, 177, 316, 562, 1000, 1778, 3162, 5623, 10000, 17782, 31622, 56234, 100000]
#n_valores = [10, 20, 42, 86, 178, 365, 750, 1540, 3162, 6493, 13335, 27384, 56234, 115478, 237137, 486967, 1000000]
#n_valores = [100, 133, 177, 237, 316, 241, 562, 749, 1000, 1333, 1778, 2371, 3162, 4216, 5624, 7499, 10000]

#n_valores = [10, 20, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
#n_valores = [20, 40, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
#n_valores = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20480, 40960, 81920, 163840, 327680]


tiempos = []
relaciones = []
dimensiones_fractales = []
entropias = []
dimensiones_fractales_normalizadas = []
entropias_normalizadas = []

# Valores de n a estudiar en la función escalar.
n_values = np.arange(2, 11)  # Puedes ajustar este rango según tus necesidades


for n in n_valores:
    start_time = time.time()
    relacion = relacion_primos_n_parallel(n)
    end_time = time.time()
    elapsed_time = end_time - start_time
    tiempos.append(elapsed_time)
    relaciones.append(relacion)

    if len(relaciones) > 1:
        relaciones_np = np.array(relaciones)
        division = np.divide(relaciones_np[1:], relaciones_np[:-1], out=np.zeros_like(relaciones_np[1:]), where=relaciones_np[:-1]!=0)
        dimension_fractal = np.mean(division)
        dimensiones_fractales.append(dimension_fractal)
        
        probabilidades = calcular_probabilidades(relaciones)
        entropia = calcular_entropia(probabilidades)
        entropias.append(entropia)
        
        dimension_fractal_normalizado = dimension_fractal / n
        dimensiones_fractales_normalizadas.append(dimension_fractal_normalizado)
        
        entropia_normalizada = entropia / n
        entropias_normalizadas.append(entropia_normalizada)
        
        print(f"n = {n}, relación = {relacion}, tiempo de ejecución = {elapsed_time:.2f} segundos, dimensión fractal = {dimension_fractal}, entropía = {entropia}, dimensión fractal normalizada = {dimension_fractal_normalizado}, entropía normalizada = {entropia_normalizada}")
    else:
        print(f"n = {n}, relación = {relacion}, tiempo de ejecución = {elapsed_time:.2f} segundos")


def agrupar_valores_logaritmicos(n_valores, num_grupos):
    n_min = np.min(n_valores)
    n_max = np.max(n_valores)
    limites = np.logspace(np.log10(n_min), np.log10(n_max), num_grupos + 1)
    indices_grupos = np.digitize(n_valores, limites)
    return indices_grupos, limites

def calcular_medias_por_grupo(valores, indices_grupos, num_grupos):
    medias = []
    for i in range(1, num_grupos + 1):
        grupo = [valores[j] for j in range(len(valores)) if indices_grupos[j] == i]
        if grupo:
            medias.append(np.mean(grupo))
        else:
            medias.append(0)
    return medias

num_grupos = 25
indices_grupos, limites = agrupar_valores_logaritmicos(n_valores[1:], num_grupos)

medias_dimensiones_fractales_normalizadas = calcular_medias_por_grupo(dimensiones_fractales_normalizadas, indices_grupos, num_grupos)
medias_entropias_normalizadas = calcular_medias_por_grupo(entropias_normalizadas, indices_grupos, num_grupos)

def ajuste_potencia(x, a, b):
    return a * x**b

def ajuste_potencia_log(x, a, b):
    return a + b * x

def entropy_adjusted(n):
    return 0.92 * n**0.14

def fractal_dimension_adjusted(n):
    return 0.70 * n**0.02

# Definir el rango de valores de n a explorar
n_values = np.logspace(1, 4, num=17)  # Valores de n en escala logarítmica entre 10^1 y 10^4

# Calcular entropía ajustada y dimensión fractal ajustada para cada valor de n
entropy_values = [entropy_adjusted(n) for n in n_values]
fractal_dimension_values = [fractal_dimension_adjusted(n) for n in n_values]

# Ajuste de potencias para la dimensión fractal y la entropía
log_n_valores = np.log10(n_valores[1:])
log_dimensiones_fractales = np.log10(dimensiones_fractales)
log_entropias = np.log10(entropias)

popt_dim, _ = curve_fit(ajuste_potencia_log, log_n_valores, log_dimensiones_fractales)
a_dim, b_dim = popt_dim

popt_ent, _ = curve_fit(ajuste_potencia_log, log_n_valores, log_entropias)
a_ent, b_ent = popt_ent

# Diferencia entre los exponentes de las potencias ajustadas
factor_escala = b_ent / b_dim

# Almacenar los valores ajustados de m y b
m_values = []
b_values = []
    
for n in n_values:
    # Cargar tus datos reales
    fractal_dimensions01 = np.array(dimensiones_fractales)  # Asegúrate de que esto coincida con el nombre de la lista que contiene las dimensiones fractales
    entropies01 = np.array(entropias)  # Asegúrate de que esto coincida con el nombre de la lista que contiene los valores de entropía

    # Ajustar la función lineal a los datos
    popt, _ = curve_fit(linear, dimensiones_fractales, entropias)
    m, b = popt
    
    # Almacenar los valores ajustados de m y b
    m_values.append(m)
    b_values.append(b)

# Suponiendo que ya tienes las listas de entropía y dimensión fractal
entropies01 = np.array(entropias)
fractal_dimensions01 = np.array(dimensiones_fractales)

# Crear la matriz de características y el vector objetivo
X = entropies01.reshape(-1, 1)
y = fractal_dimensions01

# Ajustar un modelo de regresión polinomial
degree = 1  # Puedes ajustar el grado del polinomio según lo requieras
model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
model.fit(X, y)

# Predecir la dimensión fractal para futuras entropías
future_entropies = np.array([1.5, 2.0, 2.5, 3.0, 3.5, 4, 4.5, 5, 5.5, 6, 7, 7.5, 8])  # Reemplaza estos valores con las entropías futuras que deseas predecir
future_entropies = future_entropies.reshape(-1, 1)
predicted_fractal_dimensions = model.predict(future_entropies)


# Gráfica de tiempo de ejecución
plt.plot(n_valores, tiempos, marker='o')
plt.xlabel('Valor de n')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Tiempo de ejecución por cada n_valores')
plt.grid()
plt.show()

# Gráfica de dimensiones fractales
plt.plot(n_valores[1:], dimensiones_fractales, marker='o', label='Dimensión Fractal')
plt.xlabel('Valor de n')
plt.ylabel('Dimensión Fractal')
plt.title('Variación de la Dimensión Fractal')
plt.grid()
plt.show()

# Gráfica de entropías
plt.plot(n_valores[1:], entropias, marker='o', label='Entropía')
plt.xlabel('Valor de n')
plt.ylabel('Entropía')
plt.title('Variación de la Entropía')
plt.grid()
plt.show()

# Gráfica cruzando las curvas de entropía y dimensión fractal
fig, ax1 = plt.subplots()

ax1.set_xlabel('Valor de n')
ax1.set_ylabel('Dimensión Fractal', color='tab:blue')
ax1.plot(n_valores[1:], dimensiones_fractales, marker='o', color='tab:blue', label='Dimensión Fractal')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Entropía', color='tab:red')
ax2.plot(n_valores[1:], entropias, marker='o', color='tab:red', label='Entropía')
ax2.tick_params(axis='y', labelcolor='tab:red')

fig.tight_layout()
plt.title('Gráfica cruzando las curvas de entropía y dimensión fractal')
plt.show()

# (Código relacionado con la gráfica cruzando las curvas de entropía y dimensión fractal)
plt.show()

# Ajuste lineal para la entropía y la dimensión fractal
x = np.array(dimensiones_fractales)
y = np.array(entropias)
popt, _ = curve_fit(ajuste_lineal, x, y)
m, b = popt

print(f"Función de ajuste lineal: Entropía = {m:.2f} * Dimensión Fractal + {b:.2f}")
print(f"Factor de escala: {factor_escala:.2f}")

# Imprimir los valores de n, entropía ajustada y dimensión fractal ajustada
for n, entropy, fractal_dim in zip(n_values, entropy_values, fractal_dimension_values):
    print(f"n: {n:.2f}, Entropía ajustada: {entropy:.4f}, Dimensión fractal ajustada: {fractal_dim:.4f}")

# Gráfica de ajuste lineal
plt.scatter(dimensiones_fractales, entropias, label="Datos")
plt.plot(x, ajuste_lineal(x, m, b), 'r', label=f"Ajuste lineal: y = {m:.2f}x + {b:.2f}")
plt.xlabel("Dimensión Fractal")
plt.ylabel("Entropía")
plt.title("Ajuste lineal entre la entropía y la dimensión fractal")
plt.legend()
plt.grid()
plt.show()


# Gráfica de dimensiones fractales normalizadas
plt.plot(n_valores[1:], dimensiones_fractales_normalizadas, marker='o', label='Dimensión Fractal Normalizada')
plt.xlabel('Valor de n')
plt.ylabel('Dimensión Fractal Normalizada')
plt.title('Variación de la Dimensión Fractal Normalizada')
plt.grid()
plt.show()

# Gráfica de entropías normalizadas
plt.plot(n_valores[1:], entropias_normalizadas, marker='o', label='Entropía Normalizada')
plt.xlabel('Valor de n')
plt.ylabel('Entropía Normalizada')
plt.title('Variación de la Entropía Normalizada')
plt.grid()
plt.show()

# Gráfica de medias de dimensiones fractales normalizadas
plt.plot(limites[:-1], medias_dimensiones_fractales_normalizadas, marker='o', label='Media Dimensión Fractal Normalizada')
plt.xscale('log')
plt.xlabel('Valor de n')
plt.ylabel('Media Dimensión Fractal Normalizada')
plt.title('Medias de la Dimensión Fractal Normalizada agrupadas en escala')
plt.grid()
plt.show()

# Gráfica de medias de entropías normalizadas
plt.plot(limites[:-1], medias_entropias_normalizadas, marker='o', label='Media Entropía Normalizada')
plt.xscale('log')
plt.xlabel('Valor de n')
plt.ylabel('Media Entropía Normalizada')
plt.title('Medias de la Entropía Normalizada agrupadas en escala')
plt.grid()
plt.show()

# Gráfica de las leyes de potencias ajustadas
x = np.logspace(np.log10(min(n_valores[1:])), np.log10(max(n_valores[1:])), 100)
y_dim = ajuste_potencia(x, 10**a_dim, b_dim)
y_ent = ajuste_potencia(x, 10**a_ent, b_ent)

plt.loglog(x, y_dim, 'b', label=f"Dimensión Fractal ajustada: y = {10**a_dim:.2f} * x^{b_dim:.2f}")
plt.loglog(x, y_ent, 'r', label=f"Entropía ajustada: y = {10**a_ent:.2f} * x^{b_ent:.2f}")
plt.xlabel("Valor de n")
plt.ylabel("Dimensión Fractal / Entropía")
plt.title("Comparación de las curvas ajustadas de dimensión fractal y entropía")
plt.legend()
plt.grid()
plt.show()

# Función de escala en base a los valores de n
def escala(n):
    return (10**a_ent * n**b_ent) / (10**a_dim * n**b_dim)

# Calcular los valores de la función de escala para cada n en n_valores[1:]
valores_escala = [escala(n) for n in n_valores[1:]]

# Gráfica de la función de escala en base a los valores de n
plt.plot(n_valores[1:], valores_escala, marker='o', label='Función de escala')
plt.xlabel('Valor de n')
plt.ylabel('Escala')
plt.title('Variación de la función de escala en base a los valores de n')
plt.grid()
plt.show()

print(f"Función de escala: Entropía = {m:.2f} * Dimensión Fractal + {b:.2f}")

# Imprimir los resultados
for n, m, b in zip(n_values, m_values, b_values):
    print(f"Para n = {n}, función de escala: Entropía = {m:.2f} * Dimensión Fractal + {b:.2f}")

# Imprimir los resultados de la proyección
print("Entropía\tDimensión fractal")
for ent, fd in zip(future_entropies, predicted_fractal_dimensions):
    print(f"{ent[0]:.2f}\t\t{fd:.2f}")



