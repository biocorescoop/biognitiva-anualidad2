# coding=utf-8

#No se repiten las matrices

import csv

k= 1
primos_matrices = {}

with open('matrices_5_primos.csv') as File:
	reader = csv.reader(File, delimiter=';')
	central = 0
	for row in reader:
		if central != str(int(row[12])):
			central = str(int(row[12]))
			primos_matrices[central]=[]
		elementos = []
		for i in row:
			elementos.append(int(i))
		elementos.sort()
		primos_matrices[central].append(elementos)
#print(primos_matrices)
for central in primos_matrices:
	k = 0
	print(central + " : " + str(len(primos_matrices[central])) + " matrices")
	if len(primos_matrices[central]) == 1:
		continue
	for primos in primos_matrices[central]:
		#print(primos)
		j=k+1
		for otro in primos_matrices[central][k+1:]:
			if primos == otro:
				print("las matrices " + str(k) + " y " + str(j) + " con primo central " + str(central) + " son iguales.\n")
			j = j+1
		k = k + 1
