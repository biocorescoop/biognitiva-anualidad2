import numpy as np
import cupy as cp
import matplotlib.pyplot as plt

def is_prime_gpu(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True
"""
def find_nearest_primes_gpu(signal):
    nearest_primes = cp.zeros_like(signal, dtype=cp.int32)
    for i in range(signal.size):
        x = int(cp.round(signal[i]).get())
        if is_prime_gpu(x):
            nearest_primes[i] = x
        else:
            lower = x - 1
            upper = x + 1
            while True:
                if is_prime_gpu(lower):
                    nearest_primes[i] = lower
                    break
                elif is_prime_gpu(upper):
                    nearest_primes[i] = upper
                    break
                lower -= 1
                upper += 1
    return nearest_primes

def all_primes_in_range_gpu(nearest_primes, lower, upper):
    return all(is_prime_gpu(p) for p in cp.unique(nearest_primes[nearest_primes > 0]))

upper_bound = 100000
for start in range(2, upper_bound):
    for end in range(start+1, upper_bound):
        modulated_signal = cp.array([i * 0.01 for i in range(start, end+1)]) * 100
        nearest_primes = find_nearest_primes_gpu(modulated_signal)

        if all_primes_in_range_gpu(nearest_primes, start, end):
            print(f"Se encontraron todos los primos en el rango {start}-{end} utilizando la señal modulada {modulated_signal}")
            break
    else:
        continue
    break

"""

def find_modulated_signals_for_n_values(n, num_primes=10000):
    prime_count = 0
    primes = []
    i = 2
    while prime_count < num_primes:
        if is_prime_gpu(i):
            prime_count += 1
            primes.append(i)
        i += 1

    ranges_and_signals = []
    for start_idx in range(len(primes) - n + 1):
        end_idx = start_idx + n
        start = primes[start_idx]
        end = primes[end_idx - 1]
        modulated_signal = cp.array([i * 0.01 for i in range(start, end + 1)]) * 100
        nearest_primes = find_nearest_primes_gpu(modulated_signal)

        if all_primes_in_range_gpu(nearest_primes, start, end):
            ranges_and_signals.append((start, end, modulated_signal.get()))

    return ranges_and_signals

n_values = [10, 17, 31, 56, 100, 177, 316, 562, 1000, 1778, 3162, 5623, 10000]
results = {}

for n in n_values:
    result = find_modulated_signals_for_n_values(n)
    if result:
        results[n] = result
        print(f"Encontramos {len(result)} rangos y señales moduladas para n = {n}:")
        for start, end, modulated_signal in result:
            print(f"  Rango: {start}-{end}, Señal modulada: {modulated_signal}")
    else:
        print(f"No se encontraron rangos y señales moduladas exitosas para n = {n}.")


#código para dibujar las graficas de modulación por cada n-valores. Hay que colocar en la celda de arriba 

def plot_modulated_signals_and_primes(results):
    for n, ranges_and_signals in results.items():
        for idx, (start, end, modulated_signal) in enumerate(ranges_and_signals, start=1):
            plt.figure(figsize=(10, 5))
            plt.plot(modulated_signal, label="Señal modulada")
            plt.title(f"Señal modulada para n = {n}, Rango: {start}-{end}")

            primes_in_range = [x for x in range(start, end + 1) if is_prime_gpu(x)]
            for prime in primes_in_range:
                idx = int((prime / 100) - start)
                plt.plot(idx, modulated_signal[idx], 'ro', label=f"Primo {prime}")

            # Eliminar duplicados de etiquetas de leyenda
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())

            plt.xlabel("Índice")
            plt.ylabel("Valor")
            plt.show()

plot_modulated_signals_and_primes(results)