import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D

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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def nearest_prime(x):
    lower = x
    upper = x
    while not is_prime(lower) and not is_prime(upper):
        lower -= 1
        upper += 1
    return lower if is_prime(lower) else upper

def generate_gaussian_primes(mean, std_dev, num_samples):
    normal_samples = np.random.normal(mean, std_dev, num_samples)
    return [nearest_prime(int(sample)) for sample in normal_samples]

n_range = np.arange(1, 1001)
k_range = np.arange(2, 21)

r_values = np.zeros((len(n_range), len(k_range)))

for i, n in enumerate(n_range):
    for j, k in enumerate(k_range):
        r_values[i, j] = R(n, k)

# Generar números primos con distribución gaussiana en k
mean = np.mean(k_range)
std_dev = np.std(k_range)
num_samples = 50
gaussian_primes = generate_gaussian_primes(mean, std_dev, num_samples)

plt.figure(figsize=(10, 6))
plt.imshow(r_values.T, aspect='auto', origin='lower', extent=[n_range[0], n_range[-1], k_range[0], k_range[-1]])
plt.colorbar(label='R(n, k)')

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Crear gráfico de dispersión 3D con n, k y R(n, k) como ejes
for i, n in enumerate(n_range):
    for j, k in enumerate(k_range):
        ax.scatter(n, k, r_values[i, j], c='b', marker='o', alpha=0.3)

# Marcar números primos con distribución gaussiana en k
for prime in gaussian_primes:
    for n in n_range:
        ax.scatter(n, prime, 0, marker='x', color='red', s=20)

ax.set_xlabel('n')
ax.set_ylabel('k')
ax.set_zlabel('R(n, k)')
ax.set_title('Valores de R(n, k) para diferentes rangos de n y k\nNúmeros primos con distribución gaussiana marcados con cruces rojas')
plt.show()

Marcar números primos con distribución gaussiana en k
for prime in gaussian_primes:
    for n in n_range:
        plt.scatter(n, prime, marker='x', color='red', s=20)

plt.xlabel('n')
plt.ylabel('k')
plt.title('Valores de R(n, k) para diferentes rangos de n y k\nNúmeros primos con distribución gaussiana marcados con cruces rojas')
plt.show()
