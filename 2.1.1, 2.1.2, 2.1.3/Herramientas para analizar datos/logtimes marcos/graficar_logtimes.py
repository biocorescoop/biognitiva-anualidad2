#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import csv
import math
#import sys
import matplotlib.pyplot as plt


fileinput = "logtimes_3x3_0-100000_1-1-1.csv"
n = -1
centros = []
tiempo_hasta_c = []
tiempo_medio_por_matriz = []
num_matrices = 0

with open(fileinput) as File:
	#with open(fileoutput, 'w') as salida:
	reader = csv.reader(File, delimiter=',')
	k = 0
	for row in reader:
		if row[3] == "matrices" and row[2] != -1:
			num_matrices += int(row[2])
			centros.append(int(row[1]))
			tiempo_hasta_c.append(int(row[0]))
			if num_matrices > 0:
				tiempo_medio_por_matriz.append(int(row[0])/num_matrices)
			else:
				tiempo_medio_por_matriz.append(0)

fig, ax = plt.subplots(1, 2)

ax[0].set_xscale('log')
ax[0].set_yscale('log')

ax[0].plot(centros, tiempo_hasta_c, '.') # el parámetro de '.' nos hace un scatter en vez de un plot con líneas

ax[0].set_title('tiempo hasta completar las matrices con centro $\leq c$') 
ax[0].set_xlabel('primo central')
ax[0].set_ylabel('tiempo hasta completar c')

ax[1].plot(centros, tiempo_medio_por_matriz, '.')
ax[1].set_title('tiempo medio hasta completar las matrices con centro $\leq c$') 
ax[1].set_xlabel('primo central')
ax[1].set_ylabel('tiempo medio por matriz')

plt.grid(True, alpha = .3)
plt.show()

