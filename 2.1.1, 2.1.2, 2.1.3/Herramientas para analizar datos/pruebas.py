# coding=utf-8
import csv

with open('matrices_5_primos.csv') as File:
	reader = csv.reader(File, delimiter=';')
	num_filas = 0
	num_primos = 0
	num_matr = 0
	primo_anterior = 0
	anterior = [0]*9
	maxrepe = 0
	maxrepe_matriz = 0
	repe_matriz = 0

	for row in reader:
		if primo_anterior != int(row[12]):
			num_primos += 1
			primo_anterior = int(row[12])
			repe = 0
			repe_matriz = 0
			num_filas += 1
			continue
		
		if anterior[0] == int(row[6]) and anterior[1] == int(row[7]) and anterior[2] == int(row[8]) and anterior[3] == int(row[11]) and anterior[4] == int(row[12]) and anterior[5] == int(row[13]) and anterior[6] == int(row[16]) and anterior[7] == int(row[17]) and anterior[8] == int(row[18]):
			print(str(repe_matriz))
			repe_matriz += 1
			if repe_matriz < maxrepe_matriz:
				maxrepe_matriz = repe_matriz
		else:
			num_matr += 1
		repe +=1
		if repe > maxrepe:
			maxrepe = repe
		
		num_filas += 1

print("Número de filas: " + str(num_filas))
print("Número de primos: " + str(num_primos))
print("Número de matrices 3x3: " + str(num_matr))

print("Máximas repeticiones de un primo central: " + str(maxrepe))
print("Máximas repeticiones de una matriz 3x3: " + str(maxrepe_matriz))
print("Últim primo: " + str(row[12]))
