#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import math
#import sys
import matplotlib.pyplot as plt
import scipy.optimize
from sklearn.metrics import r2_score


def func(x,a, b, c):
	#x = numpy.float128(x)
	return a * x**b + c

hilos = []
files = []

n = -1
centros = []
tiempo_hasta_c = []
tiempo_medio_por_matriz = []
num_matrices = 0

fig, ax = plt.subplots(3,3, sharex=True, sharey=True)

for i in [0]:
	for j in range(3):
		for k in range(3):
			fileinput = "perrogrande/logtimes_3x3_0-100000_%d-%d-%d.csv" %(i+1,j+1,k+1)
			with open(fileinput) as File:
				centros = []
				tiempo_hasta_c = []
				num_matrices = 0
				
				reader = csv.reader(File, delimiter=',')
				for row in reader:
					if row[3] == "matrices" and row[2] != -1:
						num_matrices += int(row[2])
						centros.append(int(row[1]))
						tiempo_hasta_c.append(int(row[0])/1000000) # pasamos de nanosegundos a milisegundos
						#if num_matrices > 0:
							#tiempo_medio_por_matriz.append(int(row[0])/num_matrices)
						#else:
							#tiempo_medio_por_matriz.append(0)
				#ax[j][k].set_xscale('log')
				#ax[j][k].set_yscale('log')
				
				xdata = centros
				ydata = tiempo_hasta_c
				ax[j][k].plot(xdata, ydata, '.', label="datos %d-%d-%d.csv" %(i+1,j+1,k+1)) # el parámetro de '.' nos hace un scatter en vez de un plot con líneas
				
				popt, pcov = scipy.optimize.curve_fit(func,  xdata, ydata, p0=[1, 1, 0])
				label = "$%f c^{ %f} + %d$" %(popt[0], popt[1], int(popt[2]))
				ax[j][k].plot(xdata, func(xdata, *popt), 'r-', label=label )

				#ax[j][k].set_title(fileinput) 
				ax[j][k].set_xlabel('máximo primo central')
				ax[j][k].set_ylabel('tiempo (ms)')
				ax[j][k].legend()
				#ax[j][k].
				
				print(fileinput)
				y_pred = func(xdata, *popt)
				R2=r2_score(ydata, y_pred)
				print(popt, R2)


plt.grid(True, alpha = .3)
plt.show()

