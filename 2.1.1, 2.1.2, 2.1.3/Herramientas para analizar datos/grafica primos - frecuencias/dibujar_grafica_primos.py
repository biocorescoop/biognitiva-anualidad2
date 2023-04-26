#!/usr/bin/python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import csv, sys

fileinput = ""
numfrecs = 1
numargs = len(sys.argv)
print("numargs = %d\n", numargs)
i = 0
while i < numargs:
	print("argumento", i, " :", sys.argv[i], "\n")
	
	if (sys.argv[i] == "-i"):
		fileinput = sys.argv[i+1]
		i += 2
		continue
	if (sys.argv[i] == "-numfrecs"):
		numfrecs = sys.argv[i+1]
		i += 2
		continue
	else:
		i += 1
		
if (fileinput == ""):
	print("No hay archivo de entrada\n")
	exit(0)

#primos = []
nums = []
frecuencias = [[] for i in range(numfrecs)]
medias = [[] for i in range(numfrecs)]
cont = 0
suma = 0
minimo = 0
maximo = 0

with open(fileinput) as File:
	reader = csv.reader(File, delimiter=',')
	for row in reader:
		#primos.append(int(row[0]))
		nums.append(cont)
		for i in range(numfrecs):
			frec = int(row[i+1])
			frecuencias[i].append(frec)
			suma += frec
		
		if frec < minimo or minimo == 0:
			minimo = frec
		
		if frec > maximo or maximo == 0:
			maximo = frec
		
		cont += 1
		if cont % 100 == 0:
			print("cont ", cont-100, "-", cont, ": maximo = ", maximo, " mínimo = ", minimo)
			media = suma/100
			print("media = ", media)
			#nums.append(cont/100)
			medias[i].append(media)
			suma = 0
			minimo = 0
			maximo = 0

#fig = plt.figure("Filtro")
if numfrecs == 4:
	#fig.subplots_adjust(hspace=0.5, wspace=0.5)
	for i in range(numfrecs):
		fig, ax = plt.subplots()
		#ax = fig.add_subplot(2, 2, i)
		ax.barh(nums, frecuencias[i])
		#plt.show()
elif numfrecs == 10:
	#fig.subplots_adjust(hspace=0.5, wspace=0.2)
	for i in range(numfrecs):
		fig, ax = plt.subplots()
		#ax = fig.add_subplot(2, 5, i)
		ax.barh(nums, frecuencias[i])
		#plt.show()

#fig, ax = plt.subplots()
#ax.barh(nums, frecuencias)
plt.show()

