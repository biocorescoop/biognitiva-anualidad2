import numpy as np
import random
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from scipy.stats import pearsonr

def compute_entropies(matrix):
    entropies = []
    for row in matrix:
        entropy = -np.sum([p * np.log2(p) for p in row if p > 0])
        entropies.append(entropy)
    return entropies

def compute_fractal_dimensions(matrix):
    fractal_dimensions = []
    for row in matrix:
        fractal_dimension = np.sum([2 * np.log2(p) for p in row if p > 0])
        fractal_dimensions.append(fractal_dimension)
    return fractal_dimensions

def random_matrix_correlation_analysis(n_values, entropies, fractal_dimensions, num_random_matrices=100):
    N = len(n_values)
    correlations = []

    for i in range(num_random_matrices):
        # 1. Crear una matriz de NxN con números aleatorios.
        random_matrix = np.random.rand(N, N)
        print(f"Matriz aleatoria {i + 1}:\n{random_matrix}\n")

        # 2. Calcular entropías y dimensiones fractales para cada fila de la matriz.
        entropies_random = compute_entropies(random_matrix)
        fractal_dimensions_random = compute_fractal_dimensions(random_matrix)

        # 3. Calcular las correlaciones entre las entropías y las dimensiones fractales.
        correlation_matrix = np.corrcoef(entropies_random, fractal_dimensions_random)
        correlation = correlation_matrix[0, 1]

        correlations.append(correlation)

    # Calcular la correlación promedio para todas las matrices aleatorias generadas.
    average_correlation = np.mean(correlations)

    return average_correlation

# 1. Ajusta un modelo de regresión polinomial a tus datos originales.
X_original = np.array(entropies).reshape(-1, 1)
y_original = np.array(fractal_dimensions)

degree = 3
model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
model.fit(X_original, y_original)

# 2. Calcula la correlación entre entropía y dimensión fractal en tus datos originales.
corr_original, _ = pearsonr(entropies, fractal_dimensions)
print(f"Correlación original: {corr_original}")

# 3. Genera matrices aleatorias para diferentes tamaños de N.
N_values = [100, 200, 300, 400, 500]

for N in N_values:
    # 4. Calcula la entropía y la dimensión fractal de cada matriz aleatoria.
    random_matrix = np.random.rand(N, N)
    entropies_random = compute_entropies(random_matrix)  # Asume que tienes una función para calcular entropías.
    fractal_dimensions_random = compute_fractal_dimensions(random_matrix)  # Asume que tienes una función para calcular dimensiones

# 5. Ajusta el modelo de regresión polinomial a los datos de la matriz aleatoria.
X_random = np.array(entropies_random).reshape(-1, 1)
y_random = np.array(fractal_dimensions_random)
model_random = make_pipeline(PolynomialFeatures(degree), LinearRegression())
model_random.fit(X_random, y_random)

correlation_original = np.corrcoef(entropies, fractal_dimensions)[0, 1]
average_correlation_random = random_matrix_correlation_analysis(n_values, entropies, fractal_dimensions, num_random_matrices=100)

print(f"Correlación original: {correlation_original}")
print(f"Correlación promedio para matrices aleatorias: {average_correlation_random}")
print(f"Diferencia de correlación: {abs(correlation_original - average_correlation_random)}")

# 6. Calcula la correlación entre la entropía y la dimensión fractal de cada matriz aleatoria.
corr_random, _ = pearsonr(entropies_random, fractal_dimensions_random)
print(f"Correlación para N = {N}: {corr_random}")

# 7. Compara la correlación de tus datos originales con la correlación de cada matriz aleatoria.
correlation_diff = abs(corr_original - corr_random)
print(f"Diferencia de correlación para N = {N}: {correlation_diff}")

# 8. Establece un umbral para determinar si la correlación entre entropía y dimensión fractal es similar en tus datos originales y en las matrices aleatorias.
threshold = 0.1

# 9. Si la diferencia entre las correlaciones está por debajo del umbral, considera que los agrupamientos de n-valores conservan la misma correlación entre entropía y dimensión fractal.
if correlation_diff < threshold:
    print(f"Para N = {N}, la correlación entre entropía y dimensión fractal es similar en los datos originales y en la matriz aleatoria.")
else:
    print(f"Para N = {N}, la correlación entre entropía y dimensión fractal NO es similar en los datos originales y en la matriz aleatoria.")

